#!/usr/bin/env python3
import csv
import json
import os
import platform
import shutil
import statistics
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
BIN = OUT / "m04-benchmark"
RAW = OUT / "raw-trials.csv"
RAW_BASE = OUT / "raw-trials-base.csv"
PREFLIGHT = OUT / "preflight.json"
SUMMARY = OUT / "summary.json"
CFLAGS = ["-std=c11", "-O2", "-Wall", "-Wextra", "-Wpedantic", "-fno-tree-vectorize", "-fno-unroll-loops"]


def run(cmd, **kw):
    return subprocess.run(cmd, text=True, check=True, **kw)


def compiler():
    for name in (os.environ.get("CC"), "cc", "gcc", "clang"):
        if name and shutil.which(name):
            return name
    raise SystemExit("No C compiler found; Core activity needs an ordinary C toolchain.")


def perf_status():
    exe = shutil.which("perf")
    if not exe:
        return {"available": False, "status": "not-installed"}
    p = subprocess.run([exe, "stat", "-e", "cycles", "--", "true"], text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {"available": True,
            "status": "usable" if p.returncode == 0 else "restricted-or-unusable",
            "returncode": p.returncode}


def quartiles(xs):
    q1, _, q3 = statistics.quantiles(xs, n=4, method="inclusive")
    return q1, q3


def main():
    OUT.mkdir(exist_ok=True)
    cc = compiler()
    version = subprocess.run([cc, "--version"], text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT).stdout.splitlines()[0]
    flags = CFLAGS[:]
    preflight = {
        "os": platform.platform(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "compiler": cc,
        "compiler_version": version,
        "cflags": flags,
        "timer": "clock_gettime(CLOCK_MONOTONIC)",
        "perf": perf_status(),
        "preflight_status": "PASS",
    }
    PREFLIGHT.write_text(json.dumps(preflight, indent=2) + "\n")
    run([cc, *flags, str(ROOT / "benchmark.c"), "-o", str(BIN)])
    meta = run([str(BIN), str(RAW_BASE)], stdout=subprocess.PIPE).stdout.strip()

    base_rows = list(csv.DictReader(RAW_BASE.open()))
    fieldnames = list(base_rows[0].keys()) + ["preflight_ref", "timer", "compiler_id", "build_flags"]
    with RAW.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in base_rows:
            r.update({
                "preflight_ref": "out/preflight.json",
                "timer": preflight["timer"],
                "compiler_id": preflight["compiler_version"],
                "build_flags": " ".join(flags),
            })
            writer.writerow(r)
    RAW_BASE.unlink()

    rows = list(csv.DictReader(RAW.open()))
    if len(rows) != 30:
        raise SystemExit(f"Expected 30 recorded trials, got {len(rows)}")
    by = {"row": [], "column": []}
    checksums = set()
    for r in rows:
        by[r["pattern"]].append(int(r["elapsed_ns"]))
        checksums.add(r["checksum"])
    if len(by["row"]) != 15 or len(by["column"]) != 15:
        raise SystemExit("Need 15 trials per pattern")
    if len(checksums) != 1:
        raise SystemExit("Checksum equivalence failed")

    result = {
        "metadata_line": meta,
        "trial_count": len(rows),
        "order_method": "counterbalanced AB/BA pairs",
        "quartile_method": "statistics.quantiles inclusive",
        "patterns": {},
        "median_ratio_column_over_row": None,
    }
    for name, xs in by.items():
        q1, q3 = quartiles(xs)
        med = statistics.median(xs)
        result["patterns"][name] = {
            "median_ns": med,
            "q1_ns": q1,
            "q3_ns": q3,
            "iqr_ns": q3 - q1,
            "min_ns": min(xs),
            "max_ns": max(xs),
        }
    result["median_ratio_column_over_row"] = (
        result["patterns"]["column"]["median_ns"] / result["patterns"]["row"]["median_ns"]
    )
    SUMMARY.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
