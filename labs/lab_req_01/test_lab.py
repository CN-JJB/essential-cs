#!/usr/bin/env python3
"""LAB-REQ-01 Automated Test Suite.

Verifies:
1. Origin server standalone semantics (200 OK + ETag, 304 Not Modified with zero body bytes).
2. Intermediary adapter standalone failure mapping (502 Bad Gateway on unreachable origin).
3. Full 4-step end-to-end trace with dynamic ports and curl.
4. Idempotent reset.
"""

from __future__ import annotations

import http.client
import os
import subprocess
import sys
import threading
import unittest
from http.server import ThreadingHTTPServer

# Local imports
from origin_server import ETAG_RESOURCE, OriginRequestHandler
from intermediary_adapter import make_proxy_handler
from harness import run_lab_req_01_trace
from reset import reset_lab_req_01


class TestOriginServer(unittest.TestCase):
    """Test origin server in isolation."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), OriginRequestHandler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()

    def test_origin_resource_and_caching(self) -> None:
        # 1. Uncached GET /resource -> 200 OK + ETag
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3.0)
        conn.request("GET", "/resource")
        resp = conn.getresponse()
        self.assertEqual(resp.status, 200)
        etag = resp.getheader("ETag")
        self.assertEqual(etag, ETAG_RESOURCE)
        body = resp.read()
        self.assertGreater(len(body), 0)
        self.assertIn(b"Hello from origin server", body)
        conn.close()

        # 2. Conditional GET with matching ETag -> 304 Not Modified + 0 body bytes
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3.0)
        conn.request("GET", "/resource", headers={"If-None-Match": etag})
        resp = conn.getresponse()
        self.assertEqual(resp.status, 304)
        self.assertEqual(resp.getheader("ETag"), ETAG_RESOURCE)
        body_304 = resp.read()
        self.assertEqual(len(body_304), 0, "RFC 9111 304 response must not carry body bytes")
        conn.close()

    def test_origin_health(self) -> None:
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3.0)
        conn.request("GET", "/health")
        resp = conn.getresponse()
        self.assertEqual(resp.status, 200)
        body = resp.read()
        self.assertIn(b'"status": "ok"', body)
        conn.close()


class TestIntermediaryAdapter(unittest.TestCase):
    """Test intermediary adapter failure mapping."""

    def test_proxy_upstream_down_yields_502(self) -> None:
        # Pick an unbound loopback port for upstream
        dummy = ThreadingHTTPServer(("127.0.0.1", 0), OriginRequestHandler)
        unbound_port = dummy.server_port
        dummy.server_close()

        # Start proxy pointing to unbound upstream port
        handler_class = make_proxy_handler("127.0.0.1", unbound_port)
        proxy = ThreadingHTTPServer(("127.0.0.1", 0), handler_class)
        proxy_port = proxy.server_port
        thread = threading.Thread(target=proxy.serve_forever, daemon=True)
        thread.start()

        try:
            conn = http.client.HTTPConnection("127.0.0.1", proxy_port, timeout=3.0)
            conn.request("GET", "/resource")
            resp = conn.getresponse()
            self.assertEqual(resp.status, 502)
            via = resp.getheader("Via")
            self.assertIsNotNone(via)
            self.assertIn("essential-cs-intermediary", via)
            body = resp.read()
            self.assertIn(b"Bad Gateway", body)
            conn.close()
        finally:
            proxy.shutdown()
            proxy.server_close()


class TestLabHarnessIntegration(unittest.TestCase):
    """Test the full 4-step curl harness execution."""

    def test_full_trace_execution(self) -> None:
        results = run_lab_req_01_trace()
        self.assertEqual(results["status"], "ALL_STEPS_PASSED")
        self.assertTrue(results["steps"]["step_1_direct_origin"]["pass"])
        self.assertTrue(results["steps"]["step_2_proxy_forward"]["pass"])
        self.assertTrue(results["steps"]["step_3_conditional_304"]["pass"])
        self.assertTrue(results["steps"]["step_4_upstream_failure_502"]["pass"])
        # Step 3 must have strictly zero body bytes
        self.assertEqual(results["steps"]["step_3_conditional_304"]["body_bytes_len"], 0)


class TestLabReset(unittest.TestCase):
    """Test lab reset script idempotency."""

    def test_reset_is_idempotent(self) -> None:
        res1 = reset_lab_req_01()
        res2 = reset_lab_req_01()
        self.assertEqual(res1, "CLEAN_NO_PERSISTENT_ARTIFACTS")
        self.assertEqual(res2, "CLEAN_NO_PERSISTENT_ARTIFACTS")


if __name__ == "__main__":
    unittest.main()
