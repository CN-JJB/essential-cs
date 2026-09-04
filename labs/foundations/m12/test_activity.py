#!/usr/bin/env python3
"""
Automated Test Suite for M12 Web & Browser Integrated Case Activities.

Verifies:
1. Rendering pipeline fixture (dynamic port 0, HTML/CSS/JS delivery, script delays);
2. Dual-origin CORS fixture (Origin A / Origin B dynamic ports, unauthorized vs authorized ACAO headers, preflight OPTIONS, non-browser contrast);
3. Event loop fixture (dynamic port 0, HTML delivery, safety caps);
4. Deterministic socket and thread lifecycle cleanup.

Invariants:
- Port 0 dynamic allocation only;
- No hardcoded ports (8000/9000 forbidden);
- Zero external dependencies (Python stdlib unittest + urllib);
- No requirement for a GUI browser.
"""

import json
import unittest
import urllib.request
import urllib.error

from rendering_fixture import RenderingServerFixture
from cors_fixture import DualOriginCORSFixture, fetch_from_non_browser_client
from event_loop_fixture import EventLoopServerFixture


class TestM12RenderingFixture(unittest.TestCase):
    """Tests for L12-02 rendering pipeline and script loading assets."""

    def test_rendering_fixture_endpoints(self):
        fixture = RenderingServerFixture()
        with fixture:
            port = fixture.port
            self.assertIsNotNone(port)
            self.assertGreater(port, 0)
            base_url = f"http://127.0.0.1:{port}"

            # 1. HTML index
            req = urllib.request.Request(f"{base_url}/")
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                self.assertEqual(resp.status, 200)
                self.assertIn("text/html", resp.headers.get("Content-Type", ""))
                body = resp.read().decode("utf-8")
                self.assertIn("Document Rendering Pipeline", body)
                self.assertIn("blocking.js", body)
                self.assertIn("deferred.js", body)

            # 2. CSS Stylesheet
            req = urllib.request.Request(f"{base_url}/style.css")
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                self.assertEqual(resp.status, 200)
                self.assertIn("text/css", resp.headers.get("Content-Type", ""))
                body = resp.read().decode("utf-8")
                self.assertIn("font-family", body)

            # 3. Parser-blocking JS with short delay
            req = urllib.request.Request(f"{base_url}/blocking.js?delay=0.1")
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                self.assertEqual(resp.status, 200)
                self.assertIn("application/javascript", resp.headers.get("Content-Type", ""))
                self.assertEqual(resp.headers.get("X-Simulated-Delay"), "0.1")
                body = resp.read().decode("utf-8")
                self.assertIn("blocking_script_executed", body)

            # 4. Deferred JS
            req = urllib.request.Request(f"{base_url}/deferred.js")
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                self.assertEqual(resp.status, 200)
                body = resp.read().decode("utf-8")
                self.assertIn("deferred_script_executed", body)

        self.assertTrue(fixture.last_stop_record["server_thread_reaped"])

    def test_rendering_fixture_rejects_non_loopback_bind(self):
        with self.assertRaises(ValueError):
            RenderingServerFixture("0.0.0.0")


class TestM12DualOriginCORS(unittest.TestCase):
    """Tests for L12-03 dual-origin CORS security model."""

    def test_dual_origin_cors_flow(self):
        fixture = DualOriginCORSFixture()
        with fixture:
            port_a = fixture.port_a
            port_b = fixture.port_b
            self.assertIsNotNone(port_a)
            self.assertIsNotNone(port_b)
            self.assertNotEqual(port_a, port_b)

            url_a = f"http://127.0.0.1:{port_a}"
            url_b = f"http://127.0.0.1:{port_b}"

            # 1. Origin A serves index page referencing Origin B
            with urllib.request.urlopen(f"{url_a}/", timeout=3.0) as resp:
                self.assertEqual(resp.status, 200)
                body = resp.read().decode("utf-8")
                self.assertIn(url_b, body)

            # 2. Case 1: Simple request without CORS permission
            req = urllib.request.Request(
                f"{url_b}/api/data?mode=unauthorized",
                headers={"Origin": url_a, "User-Agent": "CourseRawHTTPClient/1.0"}
            )
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                self.assertEqual(resp.status, 200)
                headers_lower = {k.lower(): v for k, v in resp.getheaders()}
                # Origin B does NOT include Access-Control-Allow-Origin
                self.assertNotIn("access-control-allow-origin", headers_lower)
                body = resp.read().decode("utf-8")
                data = json.loads(body)
                self.assertEqual(data["source"], "Origin B")

            # Verify that Origin B DID receive the request on the server side
            reqs = fixture.get_origin_b_requests()
            self.assertTrue(any(r["path"] == "/api/data?mode=unauthorized" for r in reqs))

            # 3. Case 2: Authorized cross-origin request
            req_auth = urllib.request.Request(
                f"{url_b}/api/data?mode=authorized",
                headers={"Origin": url_a, "User-Agent": "TestBrowserAgent/1.0"}
            )
            with urllib.request.urlopen(req_auth, timeout=3.0) as resp:
                self.assertEqual(resp.status, 200)
                headers_lower = {k.lower(): v for k, v in resp.getheaders()}
                self.assertIn("access-control-allow-origin", headers_lower)
                self.assertEqual(headers_lower["access-control-allow-origin"], url_a)

            # 4. Case 3: Preflighted request (OPTIONS check)
            opt_req = urllib.request.Request(
                f"{url_b}/api/preflighted",
                headers={
                    "Origin": url_a,
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "X-Course-Custom, Content-Type"
                },
                method="OPTIONS"
            )
            with urllib.request.urlopen(opt_req, timeout=3.0) as resp:
                self.assertEqual(resp.status, 204)
                headers_lower = {k.lower(): v for k, v in resp.getheaders()}
                self.assertEqual(headers_lower.get("access-control-allow-origin"), url_a)
                self.assertIn("POST", headers_lower.get("access-control-allow-methods", ""))
                self.assertIn("x-course-custom", headers_lower.get("access-control-allow-headers", "").lower())

            # 5. A mismatched-origin preflight is denied by course policy.
            bad_opt = urllib.request.Request(
                f"{url_b}/api/preflighted",
                headers={
                    "Origin": "http://127.0.0.1:1",
                    "Access-Control-Request-Method": "POST",
                    "Access-Control-Request-Headers": "X-Course-Custom, Content-Type",
                },
                method="OPTIONS",
            )
            with self.assertRaises(urllib.error.HTTPError) as ctx:
                urllib.request.urlopen(bad_opt, timeout=3.0)
            self.assertEqual(ctx.exception.code, 403)

            # 6. Non-browser client contrast: HTTP reachability only, not browser CORS evidence.
            non_browser = fetch_from_non_browser_client(f"{url_b}/api/data?mode=unauthorized")
            self.assertEqual(non_browser["status_code"], 200)
            self.assertFalse(non_browser["has_cors_header"])
            self.assertIn("course-data-token-42", non_browser["body"])

        self.assertTrue(fixture.last_stop_record["origin_a_thread_reaped"])
        self.assertTrue(fixture.last_stop_record["origin_b_thread_reaped"])

    def test_cors_fixture_rejects_non_loopback_bind(self):
        with self.assertRaises(ValueError):
            DualOriginCORSFixture("0.0.0.0")


class TestM12EventLoopFixture(unittest.TestCase):
    """Tests for L12-04 event loop and responsiveness fixture."""

    def test_event_loop_page_served(self):
        fixture = EventLoopServerFixture()
        with fixture:
            port = fixture.port
            self.assertIsNotNone(port)
            self.assertGreater(port, 0)
            url = f"http://127.0.0.1:{port}"

            with urllib.request.urlopen(f"{url}/", timeout=3.0) as resp:
                self.assertEqual(resp.status, 200)
                body = resp.read().decode("utf-8")
                self.assertIn("L12-04 Event Loop", body)
                self.assertIn("runOrderingTest", body)
                self.assertIn("triggerLongTask", body)
                self.assertIn("spin", body)
                self.assertIn("1500", body)
                self.assertIn("chunkSizeMs = 20", body)

        self.assertTrue(fixture.last_stop_record["server_thread_reaped"])

    def test_event_loop_fixture_rejects_non_loopback_bind(self):
        with self.assertRaises(ValueError):
            EventLoopServerFixture("0.0.0.0")


if __name__ == "__main__":
    unittest.main()
