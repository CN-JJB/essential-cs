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
    full_output = []
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
                lines = out.splitlines()
                version_str = lines[0]
                full_output = lines[:5]
                break
        except Exception:
            continue

    return {
        "available": True,
        "path": path,
        "version": version_str,
        "details": full_output,
    }


def probe_curl():
    """Specialized probe for curl to extract version, TLS backend, and features."""
    base = probe_tool_binary("curl", ["--version"])
    if not base["available"]:
        return {
            "available": False,
            "path": None,
            "version": None,
            "tls_backend": None,
            "features": None,
            "usable_for_lab": False,
            "version_probe_succeeded": False,
            "raw_version_output": [],
        }

    lines = base.get("details", [])
    v_line = lines[0] if len(lines) > 0 else base.get("version", "")
    tls_backend = "UNKNOWN"
    # curl 8.21.0 (Windows) libcurl/8.21.0 Schannel zlib/1.3.2 ...
    if "libcurl/" in v_line:
        parts = v_line.split("libcurl/")[1].split()
        if len(parts) > 1:
            tls_backend = parts[1]

    features = []
    for line in lines:
        if line.startswith("Features:"):
            features = line.replace("Features:", "").strip().split()

    version_probe_succeeded = bool(v_line)
    return {
        "available": True,
        "usable_for_lab": version_probe_succeeded,
        "path": base["path"],
        "version": v_line or None,
        "tls_backend": tls_backend if version_probe_succeeded else None,
        "features": features,
        "version_probe_succeeded": version_probe_succeeded,
        "raw_version_output": lines,
    }


def probe_tools():
    tools = {}

    tools["ss"] = probe_tool_binary("ss", ["-V", "--version"])
    tools["ip_route"] = probe_tool_binary("ip", ["-V", "-Version"])

    tools["traceroute"] = probe_tool_binary("traceroute", ["--version", "-V"])
    if not tools["traceroute"]["available"]:
        tools["tracert"] = probe_tool_binary("tracert", ["/?"])

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

    tools["curl"] = probe_curl()
    tools["openssl_cli"] = probe_tool_binary("openssl", ["version"])

    return tools


def probe_browser():
    """Probe browser binary presence and record GUI/observation capability truthfully."""
    candidates = ["google-chrome", "chrome", "chromium", "chromium-browser", "firefox", "msedge", "edge"]
    detected = {}

    for name in candidates:
        path = shutil.which(name)
        if path:
            detected[name] = {"path": path, "version": None}

    # On Windows, check standard installation directories if not already found in PATH
    if platform.system() == "Windows":
        win_candidates = [
            ("chrome", os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "Google", "Chrome", "Application", "chrome.exe")),
            ("chrome", os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"), "Google", "Chrome", "Application", "chrome.exe")),
            ("chrome", os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google", "Chrome", "Application", "chrome.exe")),
            ("msedge", os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "Microsoft", "Edge", "Application", "msedge.exe")),
            ("msedge", os.path.join(os.environ.get("PROGRAMFILES(X86)", "C:\\Program Files (x86)"), "Microsoft", "Edge", "Application", "msedge.exe")),
        ]
        for name, path in win_candidates:
            if path and os.path.exists(path) and name not in detected:
                detected[name] = {"path": path, "version": None}

    # Extract version without blocking
    for name, info in detected.items():
        p = info["path"]
        ver = None
        try:
            proc = subprocess.run([p, "--version"], capture_output=True, text=True, timeout=2)
            out = proc.stdout.strip() or proc.stderr.strip()
            if out:
                ver = out.splitlines()[0]
        except Exception:
            pass

        if not ver and platform.system() == "Windows":
            try:
                ps_cmd = f"(Get-Item '{p}').VersionInfo.ProductVersion"
                proc = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True, text=True, timeout=3)
                out = proc.stdout.strip()
                if out:
                    ver = out
            except Exception:
                pass
        info["version"] = ver

    # Live GUI capability and observation disposition
    # Do not declare browser live observation PASS without launching/observing a real browser context.
    # Essential CS truthfulness: automated non-interactive runs record NO LIVE BROWSER OBSERVATION.
    return {
        "browser_binary_detected": bool(detected),
        "detected_binaries": detected,
        "gui_capability_disposition": "NO LIVE BROWSER OBSERVATION",
        "cors_observation_disposition": "NO LIVE BROWSER CORS OBSERVATION",
        "devtools_observation_disposition": "NO LIVE DEVTOOLS OBSERVATION",
    }


def probe_chromium_source():
    """
    Empirically probe official Chromium source access (chromium.googlesource.com) for EXP-03.
    Does not fabricate commit hashes or source excerpts if unreachable.
    """
    import urllib.request
    url = "https://chromium.googlesource.com/chromium/src/+/refs/heads/main?format=JSON"
    result = {
        "available": False,
        "disposition": "NO LIVE CHROMIUM SOURCE RECHECK",
        "commit": None,
        "date": None,
        "error": None,
    }
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Essential-CS-Preflight/0.1"})
        with urllib.request.urlopen(req, timeout=5) as response:
            raw = response.read().decode("utf-8")
            # Gitiles prepends )]}' to JSON
            if raw.startswith(")]}'"):
                raw = raw[4:]
            data = json.loads(raw)
            result["available"] = True
            result["disposition"] = "LIVE_CHROMIUM_SOURCE_ACCESSIBLE"
            result["commit"] = data.get("commit")
            committer = data.get("committer", {})
            result["date"] = committer.get("time")
    except Exception as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"

    return result


def run_preflight():
    os_info = probe_os()
    py_info = probe_python()
    loopback_info = probe_loopback_socket()
    resolver_info = probe_resolver()
    tools_info = probe_tools()
    browser_info = probe_browser()
    source_info = probe_chromium_source()

    m10_core_ready = (
        py_info["has_socket"]
        and loopback_info["can_bind_port_0"]
        and loopback_info["can_connect_loopback"]
    )

    m11_core_ready = (
        m10_core_ready
        and py_info["has_ssl"]
        and py_info["tls1_3_supported"]
    )

    m12_core_ready = (
        py_info["has_socket"]
        and loopback_info["can_bind_port_0"]
        and loopback_info["can_connect_loopback"]
    )

    curl_ready = tools_info["curl"].get("usable_for_lab", False)

    if m11_core_ready and curl_ready and m12_core_ready:
        status = "READY_M10_M11_M12_CORE_AND_LAB_REQ_01"
    elif m11_core_ready and curl_ready:
        status = "READY_M11_CORE_AND_LAB_REQ_01"
    elif m11_core_ready and not curl_ready:
        status = "READY_M11_CORE_LAB_REQ_01_BLOCKED"
    elif m10_core_ready:
        status = "READY_M10_CORE"
    else:
        status = "BLOCKED_CORE"

    return {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "preflight_status": status,
        "m10_status": "READY" if m10_core_ready else "BLOCKED",
        "m11_status": "READY" if m11_core_ready else "BLOCKED",
        "m12_status": "READY" if m12_core_ready else "BLOCKED",
        "lab_req_01_status": (
            "READY"
            if curl_ready
            else "ENVIRONMENT_BLOCKED_NOT_RUN_CURL"
        ),
        "os": os_info,
        "python": py_info,
        "loopback": loopback_info,
        "resolver": resolver_info,
        "tools": tools_info,
        "browser": browser_info,
        "chromium_source": source_info,
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
    print(f" Timestamp:          {report['timestamp']}")
    print(f" Overall Status:     {report['preflight_status']}")
    print(f" M10 Core Status:    {report['m10_status']}")
    print(f" M11 Core Status:    {report['m11_status']}")
    print(f" M12 Core Status:    {report['m12_status']}")
    print(f" LAB-REQ-01 Status:  {report['lab_req_01_status']}")
    print("-" * 60)
    print(" [Host Operating System]")
    print(f"   System:           {report['os']['system']} {report['os']['release']} ({report['os']['architecture']})")
    print(f"   Version:          {report['os']['version']}")
    print("-" * 60)
    print(" [Python Runtime]")
    print(f"   Implementation:   {report['python']['implementation']}")
    print(f"   Version:          {report['python']['version']}")
    print(f"   Socket Support:   {'YES' if report['python']['has_socket'] else 'NO'}")
    print(f"   SSL Support:      {'YES' if report['python']['has_ssl'] else 'NO'} ({report['python'].get('ssl_version')})")
    print(f"   TLS 1.3:          {'YES' if report['python']['tls1_3_supported'] else 'NO'}")
    print("-" * 60)
    print(" [Loopback Socket Capability]")
    print(f"   Port 0 Bind:      {'YES' if report['loopback']['can_bind_port_0'] else 'NO'} (Assigned: {report['loopback']['assigned_port']})")
    print(f"   Loopback Conn:    {'YES' if report['loopback']['can_connect_loopback'] else 'NO'}")
    if report["loopback"]["error"]:
        print(f"   Error:            {report['loopback']['error']}")
    print("-" * 60)
    print(" [curl Capability (Required for LAB-REQ-01)]")
    curl_info = report["tools"]["curl"]
    if curl_info.get("usable_for_lab"):
        print(f"   Usable:           YES ({curl_info['path']})")
        print(f"   Version:          {curl_info['version']}")
        print(f"   TLS Backend:      {curl_info['tls_backend']}")
        print(f"   Features:         {', '.join(curl_info['features'])}")
    elif curl_info.get("available"):
        print(f"   Usable:           NO ({curl_info['path']}; curl --version did not yield usable evidence)")
    else:
        print("   Usable:           NO (TOOL MISSING: curl is required for LAB-REQ-01)")
    print("-" * 60)
    print(" [Browser & GUI Observation Disposition]")
    browser_info = report["browser"]
    print(f"   Binary Detected:  {'YES' if browser_info['browser_binary_detected'] else 'NO'}")
    for b_name, b_data in browser_info.get("detected_binaries", {}).items():
        print(f"     - {b_name}: {b_data.get('path')} (Version: {b_data.get('version') or 'N/A'})")
    print(f"   GUI Disposition:  {browser_info['gui_capability_disposition']}")
    print(f"   CORS Disposition: {browser_info['cors_observation_disposition']}")
    print(f"   DevTools Dispos:  {browser_info['devtools_observation_disposition']}")
    print("-" * 60)
    print(" [Chromium Source Reachability (EXP-03)]")
    src_info = report["chromium_source"]
    print(f"   Disposition:      {src_info['disposition']}")
    if src_info.get("commit"):
        print(f"   Current Commit:   {src_info['commit']}")
        print(f"   Commit Date:      {src_info.get('date')}")
    if src_info.get("error"):
        print(f"   Error:            {src_info['error']}")
    print("-" * 60)
    print(" [Resolver Observation Capability]")
    print(f"   Disposition:      {report['resolver']['disposition']}")
    print(f"   Available:        {report['resolver']['resolver_available']}")
    if report["resolver"]["details"]:
        print(f"   Details:          {report['resolver']['details']}")
    print("-" * 60)
    print(" [Optional / Auxiliary Tools]")
    for tool_name, tool_data in report["tools"].items():
        if tool_name == "curl":
            continue
        avail = tool_data.get("available", False)
        ver = tool_data.get("version") or tool_data.get("reason", "N/A")
        status_str = "AVAILABLE" if avail else "UNAVAILABLE"
        print(f"   {tool_name:14}: {status_str} ({ver})")
    print("=" * 60)

    return 0 if report["preflight_status"].startswith("READY") else 1


if __name__ == "__main__":
    sys.exit(main())
