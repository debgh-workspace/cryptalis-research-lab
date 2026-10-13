"""Offline KMS boundary experiment, outside the installed Cryptalis package.

This is not a KeyProvider, transport, SDK, or approved production profile.
The provisional context serialization is exercised with synthetic identities
only. It exposes context UUIDs as metadata: using it with real identifiers in
CloudTrail requires a separate owner decision. No client is created or called.
"""

from dataclasses import dataclass, field
import re
from uuid import UUID

from cryptalis.crypto import CryptoFailure, KeyContext, WrappedRoot


_ARN = re.compile(
    r"arn:aws:kms:[a-z0-9]+(?:-[a-z0-9]+)+:[0-9]{12}:key/"
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    re.ASCII,
)
_ALGORITHM = "SYMMETRIC_DEFAULT"
_MAX_BLOB_BYTES = 6144


class KmsBoundaryRejected(CryptoFailure):
    stage = "provisional offline KMS boundary"
    remedy = "Check the synthetic pinned binding, exact context, and bounded SDK-shaped values. This experiment is not a production provider."


@dataclass(frozen=True, slots=True)
class KmsBinding:
    """A caller-pinned UUID and commercial-partition key ARN, not AWS evidence.

    The ARN grammar admits ordinary UUID key identifiers in this experiment.
    It does not establish that its account, Region or key exists, or approve a
    real client, workload identity, endpoint, key state, policy or custody type.
    """

    provider_id: UUID
    key_arn: str

    def __post_init__(self):
        if (type(self.provider_id) is not UUID or self.provider_id.int == 0
                or type(self.key_arn) is not str or not 1 <= len(self.key_arn) <= 2048
                or _ARN.fullmatch(self.key_arn) is None
                or UUID(self.key_arn.rsplit("/", 1)[1]).int == 0):
            raise KmsBoundaryRejected()


def _check_parts(binding, context):
    if type(binding) is not KmsBinding or type(context) is not KeyContext:
        raise KmsBoundaryRejected()


def _context(binding, context):
    # Provisional plaintext metadata, not a confidentiality encoding. The
    # current generic development-wrap AAD format is deliberately not reused.
    return {
        "cryptalis:prototype": "kms-boundary/v0",
        "cryptalis:provider": str(binding.provider_id),
        "cryptalis:domain": str(context.domain_id),
        "cryptalis:tenant": str(context.tenant_id),
        "cryptalis:purpose": context.purpose,
        "cryptalis:root": str(context.root_id),
        "cryptalis:generation": str(context.generation),
    }


@dataclass(frozen=True, slots=True)
class WrapRequest:
    binding: KmsBinding
    context: KeyContext
    root: bytes = field(repr=False)

    def __post_init__(self):
        _check_parts(self.binding, self.context)
        if type(self.root) is not bytes or len(self.root) != 32:
            raise KmsBoundaryRejected()

    def arguments(self):
        """Return fresh SDK-shaped arguments containing the root. Do not log."""
        return {
            "KeyId": self.binding.key_arn,
            "EncryptionAlgorithm": _ALGORITHM,
            "EncryptionContext": _context(self.binding, self.context),
            "Plaintext": self.root,
        }


@dataclass(frozen=True, slots=True)
class UnwrapRequest:
    binding: KmsBinding
    context: KeyContext
    wrapper: WrappedRoot = field(repr=False)

    def __post_init__(self):
        _check_parts(self.binding, self.context)
        if (type(self.wrapper) is not WrappedRoot
                or self.wrapper.provider_id != self.binding.provider_id
                or self.wrapper.context != self.context
                or not 1 <= len(self.wrapper.sealed) <= _MAX_BLOB_BYTES):
            raise KmsBoundaryRejected()

    def arguments(self):
        """Use expected caller authority, not blob metadata. Do not log."""
        return {
            "KeyId": self.binding.key_arn,
            "EncryptionAlgorithm": _ALGORITHM,
            "EncryptionContext": _context(self.binding, self.context),
            "CiphertextBlob": self.wrapper.sealed,
        }


def _check_response(binding, response):
    if (type(response) is not dict or type(response.get("KeyId")) is not str
            or response["KeyId"] != binding.key_arn
            or type(response.get("EncryptionAlgorithm")) is not str
            or response["EncryptionAlgorithm"] != _ALGORITHM):
        raise KmsBoundaryRejected()


def validate_wrap_response(request, response):
    if type(request) is not WrapRequest:
        raise KmsBoundaryRejected()
    _check_response(request.binding, response)
    blob = response.get("CiphertextBlob")
    if type(blob) is not bytes or not 1 <= len(blob) <= _MAX_BLOB_BYTES:
        raise KmsBoundaryRejected()
    return WrappedRoot(request.binding.provider_id, request.context, blob)


def validate_unwrap_response(request, response):
    if type(request) is not UnwrapRequest:
        raise KmsBoundaryRejected()
    _check_response(request.binding, response)
    root = response.get("Plaintext")
    if (type(root) is not bytes or len(root) != 32
            or "CiphertextForRecipient" in response):
        raise KmsBoundaryRejected()
    return root
