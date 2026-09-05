#!/usr/bin/env python3
"""
Activity L15-03: Thread or async?
Evaluates concurrency execution models: OS Preemptive Threads, Cooperative Async Event Loops,
and CPython Runtime Reality (GIL-enabled vs. Free-threaded builds).

Revisits:
EC-CON-007 Specification, EC-CON-013 Isolation (synchronization scope)
"""

import asyncio
import dis
import io
import sys
import sysconfig
import time
from concurrent.futures import ThreadPoolExecutor

CURRENTNESS_CHECKPOINT = {
    "inspection_date": "2026-09-05",
    "source_authority": "https://docs.python.org/3.14/howto/free-threading-python.html & PEP 779",
    "official_status": "CPython 3.14 / PEP 779 free-threaded build is officially supported phase II (optional build configuration).",
    "runtime_rules": (
        "Free-threading remains an optional build, NOT a universal Python language invariant. "
        "A free-threaded binary may run with the GIL enabled at runtime, and importing an extension "
        "not explicitly marked free-threading-safe will cause the GIL to be enabled."
    ),
}

EVALUATION_LABEL = "NO UNIVERSAL WINNER — WORKLOAD/RUNTIME DRIVEN"


def probe_python_runtime():
    """Inspects the current Python runtime build and GIL configuration."""
    py_impl = getattr(sys, "implementation", None)
    impl_name = py_impl.name if py_impl else "unknown"
    version_str = sys.version.replace("\n", " ")

    gil_disabled_var = sysconfig.get_config_var("Py_GIL_DISABLED")
    if gil_disabled_var is None:
        gil_disabled_str = "NOT AVAILABLE / NOT APPLICABLE (not configured in sysconfig)"
    else:
        gil_disabled_str = str(gil_disabled_var)

    if hasattr(sys, "_is_gil_enabled"):
        try:
            gil_enabled = sys._is_gil_enabled()
            gil_enabled_str = str(gil_enabled)
        except Exception as exc:
            gil_enabled_str = f"ERROR ({exc})"
    else:
        gil_enabled_str = "NOT AVAILABLE / NOT APPLICABLE (probe absent in this runtime)"

    return {
        "implementation": impl_name,
        "version": version_str,
        "py_gil_disabled_config": gil_disabled_str,
        "is_gil_enabled_runtime": gil_enabled_str,
    }


def capture_bytecode_disassembly():
    """Disassembles x += 1 and captures actual opcodes for the current runtime."""
    code_obj = compile("x += 1", "<string>", "exec")
    out = io.StringIO()
    dis.dis(code_obj, file=out)
    raw_dis = out.getvalue().strip()

    # Extract opcode names
    opcodes = []
    for instr in dis.get_instructions(code_obj):
        opcodes.append({
            "opname": instr.opname,
            "argval": instr.argval,
            "argrepr": instr.argrepr,
        })

    return {
        "raw_disassembly": raw_dis,
        "opcodes": opcodes,
        "opcode_count": len(opcodes),
        "is_single_instruction": len(opcodes) <= 2,  # Normally 5 opcodes: RESUME, LOAD_NAME, LOAD_CONST, BINARY_OP, STORE_NAME, RETURN_CONST
        "multi_step_inference": (
            "Even in GIL-enabled CPython, compound update 'x += 1' compiles to multiple distinct bytecode operations "
            "(load, compute, store). Thread preemption can interleave between opcodes, proving that the GIL does NOT "
            "make application-level multi-step operations thread-safe."
        ),
    }


def blocking_io_simulation(duration_ms=50):
    """Simulates a blocking operation that would stall an event loop if not delegated."""
    time.sleep(duration_ms / 1000.0)
    return f"Completed blocking task ({duration_ms}ms)"


async def async_event_loop_demo():
    """
    Demonstrates cooperative multitasking in a single event loop:
    - Tasks execute cooperatively without preemption between await expressions.
    - Blocking tasks are delegated to an executor to avoid stalling the loop.
    """
    timeline = []
    loop = asyncio.get_running_loop()

    async def cooperative_task(task_id, steps):
        for s in range(steps):
            timeline.append(f"Task {task_id}: step {s}")
            await asyncio.sleep(0.01)  # explicit cooperative suspension point
        return f"Task {task_id} done"

    # Run cooperative tasks concurrently
    t1 = asyncio.create_task(cooperative_task(1, 3))
    t2 = asyncio.create_task(cooperative_task(2, 3))

    # Run blocking work delegated to thread executor
    with ThreadPoolExecutor(max_workers=2) as executor:
        t3 = loop.run_in_executor(executor, blocking_io_simulation, 30)
        res1, res2, res3 = await asyncio.gather(t1, t2, t3)

    return {
        "cooperative_timeline": timeline,
        "task1_result": res1,
        "task2_result": res2,
        "delegated_blocking_result": res3,
        "cooperative_interleaving_observed": len(timeline) == 6,
    }


def build_architectural_matrix():
    """Returns the structural evaluation matrix comparing execution models."""
    return {
        "label": EVALUATION_LABEL,
        "models": {
            "OS Preemptive Threads": {
                "scheduling": "Kernel preemptive scheduler",
                "memory_per_task": "High (~8MB stack default on Linux, ~1MB on Windows)",
                "cpu_parallelism": "Yes, across multiple cores (native/C extensions, or free-threaded Python)",
                "coordination_scope": "Explicit synchronization required (mutex, cond, atomics)",
                "sweet_spot": "CPU-bound parallelism, blocking native libraries, multi-threaded pipelines",
            },
            "Cooperative Async Event Loop": {
                "scheduling": "User-space cooperative event loop (await points)",
                "memory_per_task": "Very low (coroutine objects ~few KB)",
                "cpu_parallelism": "No within loop; delegates CPU work to ProcessPoolExecutor / sub-interpreters",
                "coordination_scope": "Cooperative between awaits; suspension points require logical coordination",
                "sweet_spot": "High-connection network I/O, Web APIs, chat/gateway servers, streaming",
            },
            "CPython GIL-Enabled": {
                "scheduling": "OS threads serialized on Python bytecode by GIL",
                "memory_per_task": "Thread stack + Python interpreter structures",
                "cpu_parallelism": "Only via native C extensions releasing GIL or multi-process architecture",
                "coordination_scope": "GIL protects interpreter internals; application data still requires locks",
                "sweet_spot": "I/O-bound multi-threading with moderate thread count",
            },
            "CPython Free-Threaded (PEP 779)": {
                "scheduling": "OS threads executing Python bytecode concurrently without GIL",
                "memory_per_task": "Thread stack + per-thread runtime state",
                "cpu_parallelism": "Yes, Python bytecode parallel on multi-core if GIL remains disabled",
                "coordination_scope": "Explicit locks/synchronization mandatory for all shared Python state",
                "sweet_spot": "Pure-Python CPU-bound parallelism without IPC overhead",
            },
        },
    }


def run_activity_l15_03(verbose=True):
    """Executes L15-03 hands-on activity."""
    runtime_info = probe_python_runtime()
    dis_info = capture_bytecode_disassembly()
    async_info = asyncio.run(async_event_loop_demo())
    arch_matrix = build_architectural_matrix()

    result = {
        "currentness_checkpoint": CURRENTNESS_CHECKPOINT,
        "runtime_info": runtime_info,
        "disassembly": dis_info,
        "async_demo": async_info,
        "architectural_matrix": arch_matrix,
        "inference_limits": (
            "Bytecode disassembly of x += 1 demonstrates that compound operations are multi-step in CPython, "
            "but does not guarantee a specific lost-update manifestation rate. A single asyncio event loop "
            "eliminates preemption between await points, but multi-step operations spanning await expressions "
            "still require logical coordination."
        ),
    }

    if verbose:
        print("=" * 70)
        print(" Activity L15-03: Concurrency Execution Models & Runtime Reality")
        print("=" * 70)
        print(f" Currentness Inspection: {CURRENTNESS_CHECKPOINT['inspection_date']} ({CURRENTNESS_CHECKPOINT['source_authority']})")
        print(f" Official Status:        {CURRENTNESS_CHECKPOINT['official_status']}")
        print("-" * 70)
        print(" [Named Python Runtime]:")
        print(f"   Implementation:       {runtime_info['implementation']}")
        print(f"   Version:              {runtime_info['version']}")
        print(f"   Py_GIL_DISABLED:      {runtime_info['py_gil_disabled_config']}")
        print(f"   _is_gil_enabled():    {runtime_info['is_gil_enabled_runtime']}")
        print("-" * 70)
        print(" [Bytecode Disassembly: x += 1]:")
        for instr in dis_info["opcodes"]:
            print(f"   {instr['opname']:<22} {instr['argrepr']}")
        print(f"   Opcode Count:         {dis_info['opcode_count']}")
        print(f"   Multi-step Analysis:  {dis_info['multi_step_inference']}")
        print("-" * 70)
        print(" [Cooperative Async Event Loop + Executor Delegation]:")
        for step in async_info["cooperative_timeline"]:
            print(f"   {step}")
        print(f"   Delegated Blocking:   {async_info['delegated_blocking_result']}")
        print("-" * 70)
        print(f" [Architectural Selection]: {arch_matrix['label']}")
        for model_name, props in arch_matrix["models"].items():
            print(f"   * {model_name}:")
            print(f"       Scheduling:    {props['scheduling']}")
            print(f"       Parallelism:   {props['cpu_parallelism']}")
            print(f"       Sweet Spot:    {props['sweet_spot']}")
        print("=" * 70)

    return result


if __name__ == "__main__":
    run_activity_l15_03(verbose=True)
