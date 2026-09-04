#!/usr/bin/env python3
"""
M11 Lesson 1 Activity: Local Course TLS 1.3 Fixture.

Demonstrates:
1. TLS 1.3 secure channel establishment with dedicated course test CA (RFC 9846).
2. Service-identity verification matching SAN hostname (RFC 9525).
3. Certificate-path validation failure when hostname does not match.
4. Trust-anchor rejection when root CA is untrusted in dedicated context.
5. Strict non-bypass discipline: verify=False / check_hostname=False strictly forbidden.
"""

import argparse
import json
import os
import socket
import ssl
import sys
import threading
import time


def get_cert_paths():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    certs_dir = os.path.join(base_dir, "certs")
    return {
        "ca_cert": os.path.join(certs_dir, "ca.pem"),
        "ca_key": os.path.join(certs_dir, "ca.key"),
        "server_cert": os.path.join(certs_dir, "server.pem"),
        "server_key": os.path.join(certs_dir, "server.key"),
        "untrusted_ca": os.path.join(certs_dir, "untrusted_ca.pem"),
    }


def run_tls_fixture_cases():
    paths = get_cert_paths()

    if not os.path.exists(paths["server_cert"]) or not os.path.exists(paths["ca_cert"]):
        raise FileNotFoundError("Course certificates not found. Run certs/generate_certs.py first.")

    # 1. Start Server on 127.0.0.1:0
    server_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    server_ctx.load_cert_chain(certfile=paths["server_cert"], keyfile=paths["server_key"])

    raw_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raw_server.bind(("127.0.0.1", 0))
    raw_server.listen(5)
    bound_host, bound_port = raw_server.getsockname()

    server_running = True
    server_errors = []

    def server_worker():
        while server_running:
            try:
                raw_server.settimeout(0.5)
                conn, _ = raw_server.accept()
            except socket.timeout:
                continue
            except Exception:
                break

            sconn = None
            try:
                sconn = server_ctx.wrap_socket(conn, server_side=True)
                data = sconn.recv(1024)
                if data:
                    sconn.sendall(b"ECHO:" + data)
            except Exception as exc:
                server_errors.append(str(exc))
            finally:
                if sconn:
                    try:
                        sconn.close()
                    except Exception:
                        pass
                else:
                    try:
                        conn.close()
                    except Exception:
                        pass

    srv_thread = threading.Thread(target=server_worker, daemon=True)
    srv_thread.start()

    results = {
        "endpoint": f"{bound_host}:{bound_port}",
        "case1_valid_handshake": {
            "description": "Trusted course CA + matching service identity ('localhost')",
            "success": False,
            "negotiated_version": None,
            "cipher": None,
            "payload_echoed": None,
            "error": None,
        },
        "case2_mismatched_identity": {
            "description": "Trusted course CA + mismatched service identity ('mismatch.invalid')",
            "rejected_as_expected": False,
            "disposition": None,
            "exception_type": None,
            "error": None,
        },
        "case3_untrusted_anchor": {
            "description": "Untrusted root anchor (dedicated context does not trust course CA)",
            "rejected_as_expected": False,
            "disposition": None,
            "exception_type": None,
            "error": None,
        },
    }

    try:
        # Case 1: Valid handshake
        c1_ctx = ssl.create_default_context(cafile=paths["ca_cert"])
        # Invariant: verify_mode must be CERT_REQUIRED, check_hostname True
        assert c1_ctx.verify_mode == ssl.CERT_REQUIRED
        assert c1_ctx.check_hostname is True

        s1 = socket.socket()
        s1.settimeout(3.0)
        s1.connect((bound_host, bound_port))
        ss1 = c1_ctx.wrap_socket(s1, server_hostname="localhost")
        ss1.sendall(b"PING_TLS13")
        res1 = ss1.recv(1024)

        results["case1_valid_handshake"]["success"] = (res1 == b"ECHO:PING_TLS13")
        results["case1_valid_handshake"]["negotiated_version"] = ss1.version()
        results["case1_valid_handshake"]["cipher"] = ss1.cipher()[0] if ss1.cipher() else None
        results["case1_valid_handshake"]["payload_echoed"] = res1.decode("ascii", errors="replace")
        ss1.close()

        # Case 2: Mismatched hostname
        c2_ctx = ssl.create_default_context(cafile=paths["ca_cert"])
        s2 = socket.socket()
        s2.settimeout(3.0)
        s2.connect((bound_host, bound_port))
        try:
            ss2 = c2_ctx.wrap_socket(s2, server_hostname="mismatch.invalid")
            results["case2_mismatched_identity"]["error"] = "UNEXPECTED SUCCESS: Mismatched hostname was accepted!"
            ss2.close()
        except Exception as exc:
            results["case2_mismatched_identity"]["rejected_as_expected"] = True
            results["case2_mismatched_identity"]["disposition"] = "SERVICE_IDENTITY_REJECTED"
            results["case2_mismatched_identity"]["exception_type"] = type(exc).__name__
            results["case2_mismatched_identity"]["error"] = str(exc)
        finally:
            try:
                s2.close()
            except Exception:
                pass

        # Case 3: Untrusted root anchor
        c3_ctx = ssl.create_default_context(cafile=paths["untrusted_ca"])
        s3 = socket.socket()
        s3.settimeout(3.0)
        s3.connect((bound_host, bound_port))
        try:
            ss3 = c3_ctx.wrap_socket(s3, server_hostname="localhost")
            results["case3_untrusted_anchor"]["error"] = "UNEXPECTED SUCCESS: Untrusted CA was accepted!"
            ss3.close()
        except Exception as exc:
            results["case3_untrusted_anchor"]["rejected_as_expected"] = True
            results["case3_untrusted_anchor"]["disposition"] = "UNTRUSTED_ROOT_REJECTED"
            results["case3_untrusted_anchor"]["exception_type"] = type(exc).__name__
            results["case3_untrusted_anchor"]["error"] = str(exc)
        finally:
            try:
                s3.close()
            except Exception:
                pass

    finally:
        server_running = False
        try:
            raw_server.close()
        except Exception:
            pass
        srv_thread.join(timeout=1.0)

    return results


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(description="M11 Local Course TLS 1.3 Fixture")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    args = parser.parse_args()

    results = run_tls_fixture_cases()

    all_passed = (
        results["case1_valid_handshake"]["success"]
        and results["case2_mismatched_identity"]["rejected_as_expected"]
        and results["case3_untrusted_anchor"]["rejected_as_expected"]
    )

    if args.json:
        print(json.dumps(results, indent=2))
        return 0 if all_passed else 1

    print("=" * 60)
    print(" M11-01 Local Course TLS 1.3 Verification Suite")
    print("=" * 60)
    print(f" Target Endpoint: {results['endpoint']}")
    print("-" * 60)
    print(" [Case 1: Valid Dedicated Trust Anchor & Service Identity]")
    c1 = results["case1_valid_handshake"]
    print(f"   Status:             {'PASS' if c1['success'] else 'FAIL'}")
    print(f"   Negotiated TLS:     {c1['negotiated_version']}")
    print(f"   Cipher Suite:       {c1['cipher']}")
    print(f"   Payload Echoed:     {c1['payload_echoed']}")
    print("-" * 60)
    print(" [Case 2: Deliberate Service Identity Mismatch ('mismatch.invalid')]")
    c2 = results["case2_mismatched_identity"]
    print(f"   Rejected As Expected: {'YES' if c2['rejected_as_expected'] else 'NO'}")
    print(f"   Disposition:          {c2['disposition']}")
    print(f"   Exception Caught:     {c2['exception_type']}")
    print("-" * 60)
    print(" [Case 3: Untrusted Root Anchor]")
    c3 = results["case3_untrusted_anchor"]
    print(f"   Rejected As Expected: {'YES' if c3['rejected_as_expected'] else 'NO'}")
    print(f"   Disposition:          {c3['disposition']}")
    print(f"   Exception Caught:     {c3['exception_type']}")
    print("-" * 60)
    print(" [Normative Claim Invariants]")
    print("   No Bypass Flags:      verify=False and -k are strictly forbidden")
    print("   Identity vs Trust:    Path validation != business legitimacy")
    print("   Forward Secrecy:      Ephemeral DHE keys protect past sessions; static PSK does not")
    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
