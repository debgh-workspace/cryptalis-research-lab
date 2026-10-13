"""Explicit snapshot observation; no lifecycle certification or journal writes."""
from uuid import UUID

from cryptalis.crypto.cf1 import FieldDescriptor, open_text
from cryptalis.crypto.keys import CryptoFailure, KeyUnavailable, CryptoBackendUnavailable
from cryptalis.migration import _stream, _prepare_chunk, TransitionFailure


def audit_snapshot(connection, plan, keys, row_limit, byte_limit):
    result = dict(status="CHECKED", scope="visible_nonnull_CF1_cells_at_snapshot",
                  rows_observed=0, nonnull_cells_authenticated=0, null_cells_observed=0,
                  estimated_byte_cost=0, row_limit=row_limit, byte_limit=byte_limit,
                  not_proven=["NULL substitution", "absent rows", "same-context replay or freshness",
                              "externally complete membership", "provider custody", "migration readiness"])
    try:
        for model in plan.document['lock']['models']:
            # Reuse the tested SQL-side byte-prefix admission with a payload-only
            # projection. This copied view never modifies the compiled plan.
            projection = {**model, 'fields': [{**f, 'column': f['payload_column']}
                                              for f in model['fields']], 'copied_columns': ()}
            descriptors = tuple(FieldDescriptor.from_compiled(f['descriptor'], f['descriptor_digest'])
                                for f in model['fields'])
            scoped = 'column' in model['tenancy']
            offset = 2 if scoped else 1
            cursor = None
            while True:
                remaining = byte_limit - result['estimated_byte_cost']
                if result['rows_observed'] >= row_limit or remaining <= 0:
                    if _stream(connection, projection, identity_only=True, after=cursor, limit=1):
                        result.update(status="PARTIAL", code="audit_budget_reached")
                        return result
                    break
                try:
                    rows = _stream(connection, projection, after=cursor, limit=1, byte_limit=remaining)
                except TransitionFailure as failure:
                    if failure.code == 'row_exceeds_chunk_byte_limit':
                        result.update(status="PARTIAL", code="audit_byte_budget_reached")
                        return result
                    raise
                if not rows:
                    break
                row = rows[0]
                tenant = row[1] if scoped else UUID(model['table_id'])
                frames = row[offset:]
                cost = (16 if model['record']['codec'] == 'uuid16/v1' else 8) + (16 if scoped else 0)
                cost += sum(2 * len(frame) + (74 if f['queries'] else 42)
                            for frame, f in zip(frames, model['fields']) if frame is not None)
                result['estimated_byte_cost'] += cost
                result['rows_observed'] += 1
                material = None
                for frame, descriptor in zip(frames, descriptors):
                    if frame is None:
                        result['null_cells_observed'] += 1
                        continue  # SQL NULL is visible metadata, not authenticated ciphertext.
                    if material is None:
                        # Preserve the same plan-bound policy and bounded lease
                        # preparation used by the admitted transition contract.
                        material = _prepare_chunk(keys, tenant, plan)
                    open_text(bytes(frame), descriptor, tenant, row[0], material)
                    result['nonnull_cells_authenticated'] += 1
                material = None
                cursor = str(row[0])
    except (KeyUnavailable, CryptoBackendUnavailable):
        result.update(status="UNAVAILABLE", code="audit_crypto_or_keys_unavailable")
    except CryptoFailure:
        result.update(status="REJECTED", code="ciphertext_authentication_or_context_invalid")
    except TransitionFailure:
        result.update(status="REJECTED", code="audit_key_policy_or_state_invalid")
    except Exception:
        # Host resolvers and providers may raise arbitrary errors. Do not echo
        # their message, plaintext, key material or credentials in diagnostics.
        result.update(status="UNAVAILABLE", code="ciphertext_audit_unavailable")
    return result
