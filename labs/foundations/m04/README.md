# M04 Controlled Measurement Activity

This activity compares two traversals of the same 4096 × 4096 contiguous `uint32_t` dataset (64 MiB). Row-major is the baseline; column-major is the controlled source-level change. Both execute the same unsigned-to-`uint64_t` checksum addition over every element. The maximum possible sum is well below `UINT64_MAX`, so the checksum path has defined C semantics.

## Core run

```bash
cd labs/foundations/m04
sh reset.sh
python3 run.py
```

`run.py` requires Python 3 plus an ordinary C compiler. It compiles with `-O2 -fno-tree-vectorize -fno-unroll-loops` to reduce an obvious compiler-transformation confound, performs two untimed warmups per pattern, then records 15 trials per pattern in counterbalanced AB/BA pairs. Timing is taken inside one process with `clock_gettime(CLOCK_MONOTONIC)`; allocation and initialization are outside each timed interval.

Outputs are under `out/`:

- `preflight.json`: OS/architecture/runtime/compiler/flags/timer and optional `perf` status;
- `raw-trials.csv`: pattern, pattern-local trial number, execution order, elapsed ns, dimensions, bytes, checksum, preflight reference, timer, compiler ID, and build flags;
- `summary.json`: median, Q1/Q3, IQR, min/max and column/row median ratio. Quartiles use Python `statistics.quantiles(..., method="inclusive")`.

`perf` is optional corroboration only. Preflight checks whether it is installed/usable; the Core run never requires privilege changes or counters.

## Inspect the generated build

Use your platform's disassembler, for example:

```bash
objdump -d out/m04-benchmark | less
```

Confirm that both traversal paths remain real loads and additions, and note compiler transformations that could complicate the intended locality interpretation. The supplied flags reduce vectorization/unrolling as a confound but do not isolate every machine variable.

## What the experiment can support

Compare the between-pattern median difference with each pattern's IQR and any visible outliers. A result in the predicted direction is **consistent with** spatial-locality/cache-hierarchy effects under the recorded build/workload/environment. It does not identify one cache level, establish exact miss counts, guarantee the ratio elsewhere, or predict a production workload. Scheduler/virtualization noise, frequency/thermal changes, prefetch behavior, TLB/page effects and execution-order/cache-state effects can remain plausible or unresolved.

## Break / repair

An unfair experiment would run each pattern once, warm only one pattern, change dimensions together with traversal order, or use different arithmetic. Identify the violated control, then repair it before treating the output as evidence.

## Reset

```bash
sh reset.sh
```

Reset only removes generated `out/` artifacts.
