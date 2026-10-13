"""Synthetic, offline request/response controls; no SDK or custody claim."""

from dataclasses import FrozenInstanceError, replace
from contextlib import redirect_stderr, redirect_stdout
import io
import logging
import unittest
from uuid import UUID

from cryptalis.crypto import KeyContext, WrappedRoot
from experiments.kms_boundary import (
    KmsBinding, KmsBoundaryRejected, UnwrapRequest, WrapRequest,
    validate_unwrap_response, validate_wrap_response,
)


ARN = "arn:aws:kms:us-east-1:111122223333:key/12345678-1234-1234-1234-123456789abc"
OTHER_ARN = "arn:aws:kms:us-east-1:111122223333:key/22345678-1234-1234-1234-123456789abc"
PROVIDER = UUID("10000000-0000-0000-0000-000000000001")
DOMAIN = UUID("20000000-0000-0000-0000-000000000002")
TENANT = UUID("30000000-0000-0000-0000-000000000003")
ROOT_ID = UUID("40000000-0000-0000-0000-000000000004")
ROOT = b"SYNTHETIC_ROOT_NO_LOGGING".ljust(32, b"_")
BLOB = b"SYNTHETIC_KMS_BLOB_NOT_REAL_CRYPTO"
CONTEXT = KeyContext(DOMAIN, TENANT, "payload", ROOT_ID, 7)


def expected_context(context=CONTEXT, provider=PROVIDER):
    # Independent, explicit fixture contract. Provisional and synthetic only.
    return {
        "cryptalis:prototype": "kms-boundary/v0",
        "cryptalis:provider": str(provider),
        "cryptalis:domain": str(context.domain_id),
        "cryptalis:tenant": str(context.tenant_id),
        "cryptalis:purpose": context.purpose,
        "cryptalis:root": str(context.root_id),
        "cryptalis:generation": str(context.generation),
    }


class KmsBoundaryPrototypeTests(unittest.TestCase):
    def setUp(self):
        self.binding = KmsBinding(PROVIDER, ARN)
        self.wrap = WrapRequest(self.binding, CONTEXT, ROOT)
        self.wrapper = WrappedRoot(PROVIDER, CONTEXT, BLOB)
        self.unwrap = UnwrapRequest(self.binding, CONTEXT, self.wrapper)

    def reject(self, call, *args):
        with self.assertRaises(KmsBoundaryRejected) as caught:
            call(*args)
        failure = caught.exception
        self.assertFalse(failure.retryable)
        self.assertEqual(failure.effects, "none")
        safe = str(failure) + repr(failure.__dict__)
        for marker in (ROOT.decode(), BLOB.decode(), "PRIVATE_PROVIDER_MESSAGE", ARN):
            self.assertNotIn(marker, safe)

    def test_exact_requests_use_pinned_arn_bytes_and_expected_context(self):
        common = {"KeyId": ARN, "EncryptionAlgorithm": "SYMMETRIC_DEFAULT",
                  "EncryptionContext": expected_context()}
        self.assertEqual(self.wrap.arguments(), {**common, "Plaintext": ROOT})
        self.assertEqual(self.unwrap.arguments(), {**common, "CiphertextBlob": BLOB})
        self.assertEqual(len(ROOT), 32)
        # No grant creation, recipient mode, dry-run shortcut, or retry option.
        self.assertEqual(set(self.unwrap.arguments()),
                         {"KeyId", "EncryptionAlgorithm", "EncryptionContext", "CiphertextBlob"})

    def test_binding_rejects_unpinned_or_malformed_key_identifiers(self):
        for arn in (
            "alias/example", "arn:aws:kms:us-east-1:111122223333:alias/example",
            "12345678-1234-1234-1234-123456789abc", "", None,
            ARN.replace(":kms:", ":s3:"), ARN.replace(":us-east-1:", "::"),
            ARN.replace(":111122223333:", ":11112222333:"),
            ARN.replace("key/", "key/mrk-"), ARN + "\n",
            ARN.replace(":us-east-1:", ":" + "region-"*400 + "1:"),
        ):
            with self.subTest(arn=arn):
                self.reject(KmsBinding, PROVIDER, arn)
        for provider in (None, str(PROVIDER), UUID(int=0)):
            with self.subTest(provider=provider):
                self.reject(KmsBinding, provider, ARN)

    def test_binding_and_requests_are_immutable_and_arguments_are_fresh(self):
        for value, attribute, replacement in (
            (self.binding, "key_arn", OTHER_ARN),
            (self.wrap, "root", b"different"),
            (self.unwrap, "wrapper", None),
        ):
            with self.subTest(attribute=attribute):
                with self.assertRaises(FrozenInstanceError):
                    setattr(value, attribute, replacement)
        first = self.wrap.arguments()
        first["KeyId"] = OTHER_ARN
        first["EncryptionContext"]["cryptalis:tenant"] = "changed"
        second = self.wrap.arguments()
        self.assertEqual(second["KeyId"], ARN)
        self.assertEqual(second["EncryptionContext"], expected_context())

    def test_every_context_field_and_provider_affects_expected_aad(self):
        changes = (
            {"domain_id": UUID(int=11)}, {"tenant_id": UUID(int=12)},
            {"purpose": "search"}, {"root_id": UUID(int=13)}, {"generation": 8},
        )
        for change in changes:
            context = replace(CONTEXT, **change)
            with self.subTest(change=change):
                arguments = WrapRequest(self.binding, context, ROOT).arguments()
                self.assertEqual(arguments["EncryptionContext"], expected_context(context))
                self.assertNotEqual(arguments["EncryptionContext"], expected_context())
        binding = KmsBinding(UUID(int=14), ARN)
        self.assertEqual(WrapRequest(binding, CONTEXT, ROOT).arguments()["EncryptionContext"],
                         expected_context(provider=UUID(int=14)))

    def test_wrap_rejects_wrong_root_type_or_length_and_context(self):
        for root in (None, "PRIVATE_PROVIDER_MESSAGE", bytearray(ROOT), b"", ROOT[:-1], ROOT+b"x"):
            with self.subTest(root_type=type(root).__name__):
                self.reject(WrapRequest, self.binding, CONTEXT, root)
        self.reject(WrapRequest, self.binding, None, ROOT)
        self.reject(WrapRequest, None, CONTEXT, ROOT)

    def test_unwrap_rejects_wrapper_provider_or_expected_context_mismatch(self):
        self.reject(UnwrapRequest, self.binding, CONTEXT,
                    WrappedRoot(UUID(int=15), CONTEXT, BLOB))
        for change in (
            {"domain_id": UUID(int=11)}, {"tenant_id": UUID(int=12)},
            {"purpose": "search"}, {"root_id": UUID(int=13)}, {"generation": 8},
        ):
            with self.subTest(change=change):
                self.reject(UnwrapRequest, self.binding, replace(CONTEXT, **change), self.wrapper)
        self.reject(UnwrapRequest, self.binding, CONTEXT, None)
        self.reject(UnwrapRequest, None, CONTEXT, self.wrapper)

    def test_unwrap_applies_kms_blob_bound_before_any_transport(self):
        for size in (1, 6144):
            with self.subTest(size=size):
                wrapper = WrappedRoot(PROVIDER, CONTEXT, b"x"*size)
                self.assertEqual(UnwrapRequest(self.binding, CONTEXT, wrapper).arguments()["CiphertextBlob"],
                                 b"x"*size)
        self.reject(UnwrapRequest, self.binding, CONTEXT,
                    WrappedRoot(PROVIDER, CONTEXT, b"x"*6145))

    def test_valid_responses_preserve_exact_root_wrapper_and_context(self):
        wrapped = validate_wrap_response(self.wrap, {
            "KeyId": ARN, "EncryptionAlgorithm": "SYMMETRIC_DEFAULT", "CiphertextBlob": BLOB,
            "ResponseMetadata": {"RequestId": "synthetic"},
        })
        self.assertEqual(wrapped, self.wrapper)
        self.assertIs(validate_unwrap_response(self.unwrap, {
            "KeyId": ARN, "EncryptionAlgorithm": "SYMMETRIC_DEFAULT", "Plaintext": ROOT,
            "KeyMaterialId": "synthetic-material", "ResponseMetadata": {},
        }), ROOT)

    def test_response_key_and_algorithm_are_mandatory_and_exact(self):
        for validator, request, payload in (
            (validate_wrap_response, self.wrap, {"CiphertextBlob": BLOB}),
            (validate_unwrap_response, self.unwrap, {"Plaintext": ROOT}),
        ):
            good = {"KeyId": ARN, "EncryptionAlgorithm": "SYMMETRIC_DEFAULT", **payload}
            for key, value in (("KeyId", OTHER_ARN), ("KeyId", None),
                               ("KeyId", ARN.replace("us-east-1", "us-west-2")),
                               ("KeyId", ARN.replace("111122223333", "444455556666")),
                               ("KeyId", "alias/example"),
                               ("EncryptionAlgorithm", "RSAES_OAEP_SHA_256"),
                               ("EncryptionAlgorithm", None)):
                with self.subTest(validator=validator.__name__, key=key, value=value):
                    bad = {**good, key: value}
                    self.reject(validator, request, bad)
                    del bad[key]
                    self.reject(validator, request, bad)
            self.reject(validator, request, None)
            self.reject(validator, request, "PRIVATE_PROVIDER_MESSAGE")

    def test_sdk_response_shapes_reject_custom_equality_values(self):
        class SpoofedString(str):
            def __eq__(self, other):
                return True

            def __ne__(self, other):
                return False

        common = {"KeyId": ARN, "EncryptionAlgorithm": "SYMMETRIC_DEFAULT"}
        for key in ("KeyId", "EncryptionAlgorithm"):
            bad = {**common, key: SpoofedString("wrong")}
            with self.subTest(key=key):
                self.reject(validate_wrap_response, self.wrap, {**bad, "CiphertextBlob": BLOB})
                self.reject(validate_unwrap_response, self.unwrap, {**bad, "Plaintext": ROOT})

    def test_response_lengths_types_and_recipient_mode_fail_closed(self):
        common = {"KeyId": ARN, "EncryptionAlgorithm": "SYMMETRIC_DEFAULT"}
        for blob in (None, "PRIVATE_PROVIDER_MESSAGE", b"", bytearray(BLOB), b"x"*6145):
            with self.subTest(blob_type=type(blob).__name__):
                self.reject(validate_wrap_response, self.wrap, {**common, "CiphertextBlob": blob})
        for root in (None, "PRIVATE_PROVIDER_MESSAGE", b"", bytearray(ROOT), ROOT[:-1], ROOT+b"x"):
            with self.subTest(root_type=type(root).__name__):
                self.reject(validate_unwrap_response, self.unwrap, {**common, "Plaintext": root})
        self.reject(validate_wrap_response, self.wrap, common)
        self.reject(validate_unwrap_response, self.unwrap, common)
        self.reject(validate_unwrap_response, self.unwrap,
                    {**common, "Plaintext": ROOT, "CiphertextForRecipient": b"recipient"})

    def test_request_representations_omit_root_and_ciphertext(self):
        for value in (self.wrap, self.unwrap, self.wrapper):
            rendered = repr(value)
            self.assertNotIn(ROOT.decode(), rendered)
            self.assertNotIn(BLOB.decode(), rendered)
        # Only intentionally constructed SDK arguments contain material.
        self.assertEqual(self.wrap.arguments()["Plaintext"], ROOT)
        self.assertEqual(self.unwrap.arguments()["CiphertextBlob"], BLOB)

    def test_boundary_emits_no_output_with_a_sensitive_marker_control(self):
        capture = io.StringIO()
        logger = logging.getLogger()
        previous_level = logger.level
        handler = logging.StreamHandler(capture)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        try:
            logger.warning(ROOT.decode())
            self.assertIn(ROOT.decode(), capture.getvalue())
            capture.seek(0)
            capture.truncate()
            with redirect_stdout(capture), redirect_stderr(capture):
                self.wrap.arguments()
                self.unwrap.arguments()
                validate_wrap_response(self.wrap, {
                    "KeyId": ARN, "EncryptionAlgorithm": "SYMMETRIC_DEFAULT", "CiphertextBlob": BLOB,
                })
                validate_unwrap_response(self.unwrap, {
                    "KeyId": ARN, "EncryptionAlgorithm": "SYMMETRIC_DEFAULT", "Plaintext": ROOT,
                })
                self.reject(validate_unwrap_response, self.unwrap,
                            {"KeyId": OTHER_ARN, "Plaintext": ROOT})
            self.assertEqual(capture.getvalue(), "")
        finally:
            logger.removeHandler(handler)
            logger.setLevel(previous_level)
            handler.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
