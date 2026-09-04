#!/usr/bin/env python3
"""
Preflight verification script for Network & Web/Browser modules (M10-M12).
Evaluates and records host capabilities empirically without hardcoded version pinning.
"""

import argparse
import datetime
import json
import os
import platform
import shutil
import socket
import subprocess
import sys


def probe_os():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "architecture": platform.machine(),
    }


def probe_python():
    info = {
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
        "has_socket": False,
        "has_ssl": False,
        "ssl_version": None,
        "tls1_3_supported": False,
    }

    try:
        import socket  # noqa: F401
        info["has_socket"] = True
    except ImportError:
        info["has_socket"] = False

    try:
        import ssl
        info["has_ssl"] = True
        info["ssl_version"] = getattr(ssl, "OPENSSL_VERSION", None)
        # Check TLS 1.3 support
        has_tls13 = hasattr(ssl, "HAS_TLSv1_3") and ssl.HAS_TLSv1_3
        info["tls1_3_supported"] = bool(has_tls13)
    except ImportError:
        info["has_ssl"] = False

    return info


def probe_loopback_socket():
    result = {
        "can_bind_port_0": False,
        "assigned_port": None,
        "can_connect_loopback": False,
        "error": None,
    }

    server = None
    client = None
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        host, port = server.getsockname()
        result["can_bind_port_0"] = True
        result["assigned_port"] = port

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(2.0)
        client.connect(("127.0.0.1", port))
        result["can_connect_loopback"] = True
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        if client:
            try:
                client.close()
            except Exception:
                pass
        if server:
            try:
                server.close()
            except Exception:
                pass

    return result


def probe_resolver():
    """
    Empirically probe resolver observation capability using RFC 2606 .invalid TLD.
    Does not fabricate error text.
    """
    result = {
        "tested_host": "preflight-test.invalid",
        "resolver_available": False,
        "disposition": None,
        "exception_type": None,
        "details": None,
    }

    try:
        socket.getaddrinfo("preflight-test.invalid", 80, socket.AF_INET, socket.SOCK_STREAM)
        result["resolver_available"] = True
        result["disposition"] = "UNEXPECTED_RESOLUTION_SUCCESS"
    except socket.gaierror as exc:
        result["resolver_available"] = True
        result["disposition"] = "LIVE_DNS_FAILURE_OBSERVED"
        result["exception_type"] = type(exc).__name__
        result["details"] = {
            "errno": getattr(exc, "errno", None),
            "strerror": str(exc),
        }
    except Exception as exc:
        result["resolver_available"] = False
        result["disposition"] = "NO_LIVE_DNS_FAILURE_OBSERVATION"
        result["exception_type"] = type(exc).__name__
        result["details"] = str(exc)

    return result


def probe_tool_binary(tool_name, version_flags=("-v", "--version")):
    path = shutil.which(tool_name)
    if not path:
        return {"available": False, "path": None, "version": None}

    version_str = None
    for flag in version_flags:
        try:
            proc = subprocess.run(
                [path, flag],
                capture_output=True,
                text=True,
                timeout=2,
            )
            out = proc.stdout.strip() or proc.stderr.strip()
            if out:
                version_str = out.splitlines()[0]
                break
        except Exception:
            continue

    return {
        "available": True,
        "path": path,
        "version": version_str,
    }


def probe_tools():
    tools = {}

    # Linux routing / socket tools
    tools["ss"] = probe_tool_binary("ss", ["-V", "--version"])
    tools["ip_route"] = probe_tool_binary("ip", ["-V", "-Version"])

    # Optional network tracing / inspection tools
    tools["traceroute"] = probe_tool_binary("traceroute", ["--version", "-V"])
    if not tools["traceroute"]["available"]:
        tools["tracert"] = probe_tool_binary("tracert", ["/?"])

    # Packet capture tool capability
    tcpdump_probe = probe_tool_binary("tcpdump", ["--version"])
    if tcpdump_probe["available"]:
        tools["tcpdump"] = {
            "available": True,
            "version": tcpdump_probe["version"],
            "capture_capable": "UNKNOWN_WITHOUT_PRIVILEGE_TEST",
        }
    else:
        tshark_probe = probe_tool_binary("tshark", ["--version"])
        if tshark_probe["available"]:
            tools["tcpdump"] = {
                "available": True,
                "tool": "tshark",
                "version": tshark_probe["version"],
                "capture_capable": "UNKNOWN_WITHOUT_PRIVILEGE_TEST",
            }
        else:
            tools["tcpdump"] = {
                "available": False,
                "reason": "TOOL_UNAVAILABLE",
            }

    # External curl
    tools["curl"] = probe_tool_binary("curl", ["--version"])

    # OpenSSL CLI
    tools["openssl_cli"] = probe_tool_binary("openssl", ["version"])

    return tools


def probe_browser():
    """Generic detection for desktop browsers without asserting M10 acceptance."""
    candidates = ["google-chrome", "chrome", "chromium", "chromium-browser", "firefox"]
    detected = {}
    for name in candidates:
        path = shutil.which(name)
        if path:
            detected[name] = path
    return {
        "gui_detected": bool(detected),
        "detected_binaries": detected,
    }


def run_preflight():
    os_info = probe_os()
    py_info = probe_python()
    loopback_info = probe_loopback_socket()
    resolver_info = probe_resolver()
    tools_info = probe_tools()
    browser_info = probe_browser()

    m10_core_ready = (
        py_info["has_socket"]
        and loopback_info["can_bind_port_0"]
        and loopback_info["can_connect_loopback"]
    )

    status = "READY_M10_CORE" if m10_core_ready else "BLOCKED_M10_CORE"

    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "preflight_status": status,
        "os": os_info,
        "python": py_info,
        "loopback": loopback_info,
        "resolver": resolver_info,
        "tools": tools_info,
        "browser": browser_info,
    }


def main():
    parser = argparse.ArgumentParser(description="Network & Web Environment Preflight")
    parser.add_argument("--json", action="store_true", help="Print preflight report in JSON format")
    args = parser.parse_args()

    report = run_preflight()

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["preflight_status"].startswith("READY") else 1

    print("=" * 60)
    print(" Essential CS: Network & Web Preflight Capability Report")
    print("=" * 60)
    print(f" Timestamp:      {report['timestamp']}")
    print(f" Overall Status: {report['preflight_status']}")
    print("-" * 60)
    print(" [Host Operating System]")
    print(f"   System:       {report['os']['system']} {report['os']['release']} ({report['os']['architecture']})")
    print(f"   Version:      {report['os']['version']}")
    print("-" * 60)
    print(" [Python Runtime]")
    print(f"   Implementation: {report['python']['implementation']}")
    print(f"   Version:        {report['python']['version']}")
    print(f"   Socket Support: {'YES' if report['python']['has_socket'] else 'NO'}")
    print(f"   SSL Support:    {'YES' if report['python']['has_ssl'] else 'NO'} ({report['python'].get('ssl_version')})")
    print(f"   TLS 1.3:        {'YES' if report['python']['tls1_3_supported'] else 'NO'}")
    print("-" * 60)
    print(" [Loopback Socket Capability]")
    print(f"   Port 0 Bind:    {'YES' if report['loopback']['can_bind_port_0'] else 'NO'} (Assigned: {report['loopback']['assigned_port']})")
    print(f"   Loopback Conn:  {'YES' if report['loopback']['can_connect_loopback'] else 'NO'}")
    if report["loopback"]["error"]:
        print(f"   Error:          {report['loopback']['error']}")
    print("-" * 60)
    print(" [Resolver Observation Capability]")
    print(f"   Disposition:    {report['resolver']['disposition']}")
    print(f"   Available:      {report['resolver']['resolver_available']}")
    if report["resolver"]["details"]:
        print(f"   Details:        {report['resolver']['details']}")
    print("-" * 60)
    print(" [Optional / Auxiliary Tools]")
    for tool_name, tool_data in report["tools"].items():
        avail = tool_data.get("available", False)
        ver = tool_data.get("version") or tool_data.get("reason", "N/A")
        status_str = "AVAILABLE" if avail else "UNAVAILABLE"
        print(f"   {tool_name:14}: {status_str} ({ver})")
    print("=" * 60)

    return 0 if report["preflight_status"].startswith("READY") else 1


if __name__ == "__main__":
    sys.exit(main())
