#!/usr/bin/env python3
"""
M11 Automated Activity Test Suite.

Verifies:
1. Local TLS 1.3 fixture 3-case verification (valid cert, hostname mismatch, untrusted root).
2. HTTP semantics (Safe GET, Idempotent PUT, Non-idempotent POST, 200 != business success).
3. HTTP caching & validation (Freshness, ETag, 304 Not Modified with zero body bytes).
4. Idempotent reset and endpoint dormancy.

Strictly enforces Essential CS invariants:
- Port 0 dynamic allocation only;
- No verification bypass flags (verify=False / -k forbidden);
- No Content-Length: 0 requirement for 304;
- No hardcoded errno or fixed latency assertions.
"""

import unittest

from caching_observer import run_caching_observation
from http_semantics_observer import run_http_semantics_observation
from reset import run_reset
from tls_fixture import run_tls_fixture_cases


class TestM11TLSFixture(unittest.TestCase):
    """L11-01 tests: TLS 1.3, service identity, and trust anchors."""

    def test_tls_fixture_three_cases(self):
        results = run_tls_fixture_cases()

        # Case 1: Valid handshake succeeds
        c1 = results["case1_valid_handshake"]
        self.assertTrue(c1["success"], f"Valid handshake failed: {c1.get('error')}")
        self.assertEqual(c1["negotiated_version"], "TLSv1.3")
        self.assertIsNotNone(c1["cipher"])
        self.assertEqual(c1["payload_echoed"], "ECHO:PING_TLS13")

        # Case 2: Hostname mismatch rejected
        c2 = results["case2_mismatched_identity"]
        self.assertTrue(c2["rejected_as_expected"])
        self.assertEqual(c2["disposition"], "SERVICE_IDENTITY_REJECTED_BY_TLS_CLIENT")
        self.assertIsNotNone(c2["exception_type"])

        # Case 3: Untrusted root CA rejected
        c3 = results["case3_untrusted_anchor"]
        self.assertTrue(c3["rejected_as_expected"])
        self.assertEqual(c3["disposition"], "UNTRUSTED_ROOT_REJECTED_BY_TLS_CLIENT")
        self.assertIsNotNone(c3["exception_type"])
        self.assertTrue(results["server_thread_reaped"])


class TestM11HTTPSemantics(unittest.TestCase):
    """L11-02 tests: HTTP message structure, method semantics, protocol vs business outcome."""

    def test_http_semantics(self):
        results = run_http_semantics_observation()

        # Step 1: Safe GET
        s1 = results["step1_safe_get"]
        self.assertEqual(s1["status_code"], 200)
        self.assertEqual(s1["representation"]["item_id"], 42)

        # Step 2: Idempotent PUT
        s2 = results["step2_idempotent_put"]
        self.assertEqual(s2["status_code"], 200)
        self.assertTrue(s2["idempotency_verified"])

        # Step 3: Non-idempotent POST
        s3 = results["step3_non_idempotent_post"]
        self.assertEqual(s3["status_code"], 201)
        self.assertIsNotNone(s3["location_header"])

        # Step 4: Protocol 200 != Business success
        s4 = results["step4_protocol_vs_business_status"]
        self.assertEqual(s4["http_status_code"], 200)
        self.assertEqual(s4["business_status"], "FAILURE")
        self.assertEqual(s4["business_error_code"], "INSUFFICIENT_FUNDS")

        # Step 5: Wire framing CRLF
        s5 = results["step5_raw_wire_trace"]
        self.assertTrue(s5["crlf_delimiter_found"])
        self.assertTrue(results["server_thread_reaped"])
        self.assertEqual(s2["resulting_state"]["stock"], 10)


class TestM11CachingObserver(unittest.TestCase):
    """L11-03 tests: Cache freshness vs validation, 304 zero body, ETag opaque validator."""

    def test_caching_and_validation(self):
        results = run_caching_observation()

        # Step 1: Initial representation fetch
        s1 = results["step1_initial_fetch"]
        self.assertEqual(s1["status_code"], 200)
        self.assertEqual(s1["etag_received"], '"course-m11-v1"')
        self.assertGreater(s1["body_bytes_transferred"], 0)

        # Step 2: Conditional 304 with matching ETag
        s2 = results["step2_conditional_matching_etag"]
        self.assertEqual(s2["status_code"], 304)
        self.assertTrue(s2["zero_body_verified"])
        self.assertEqual(s2["wire_body_bytes_transferred"], 0)
        self.assertGreater(s2["representation_payload_bytes_avoided_in_fixture"], 0)

        # Step 3: Mismatched ETag returns 200 + representation
        s3 = results["step3_conditional_mismatched_etag"]
        self.assertEqual(s3["status_code"], 200)
        self.assertTrue(s3["full_body_sent"])
        self.assertTrue(results["server_thread_reaped"])


class TestM11Reset(unittest.TestCase):
    """Teardown and reset idempotency."""

    def test_reset_idempotent(self):
        r1 = run_reset()
        self.assertEqual(r1["status"], "CLEAN_NO_PERSISTENT_ARTIFACTS")
        r2 = run_reset()
        self.assertEqual(r2["status"], "CLEAN_NO_PERSISTENT_ARTIFACTS")
        self.assertTrue(r2["idempotent"])


if __name__ == "__main__":
    unittest.main()
