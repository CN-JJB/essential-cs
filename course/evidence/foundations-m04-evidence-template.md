# Foundations M04 Evidence Template

## A — Environment / preflight
- Commit / context:
- OS:
- Architecture:
- Timer API/source:
- Timer resolution / metadata:
- Compiler/build identifier:
- Build flags:
- `perf` status (optional):
- Preflight status:

## B — Hypothesis (write before data)
- Prediction:
- Why:

## C — Baseline / controlled change
- Baseline: row-major traversal of row-major contiguous storage.
- Controlled change: column-major traversal of the same storage.
- What changes:
- What stays fixed:

## D — Workload metadata
- Rows × columns:
- Element width/type:
- Total elements:
- Total bytes:
- Checksum semantics / defined-range note:
- Build mode:

## E — Warmup / trial order
- Untimed warmups per pattern (must be ≥2):
- Order method (counterbalanced AB/BA or fixed-seed randomized):
- Seed, if used:
- Reminder: warmup reduces obvious first-run/setup effects; it does not establish a known cache state.

## F — Raw trials
Attach or reference the raw CSV. It must contain ≥15 recorded trials per pattern and retain pattern, pattern-local trial number, execution order, monotonic elapsed time, dimensions, bytes, checksum/result, environment/preflight reference, and compiler/build+flags.

- Raw evidence path:
- Row trial count:
- Column trial count:
- Checksum equivalence:

## G — Summary
| Pattern | Median ns | Q1 ns | Q3 ns | IQR ns |
|---|---:|---:|---:|---:|
| row | | | | |
| column | | | | |

- Median ratio (column / row):
- Quartile method:

## H — Variation / outlier note
Compare between-pattern difference with within-pattern spread. Note visible outliers/instability; do not discard inconvenient raw values.

## I — Competing explanations
Record at least two and label each `controlled`, `checked`, `plausible`, or `unresolved`.

| Alternative / condition | Status | Evidence / note |
|---|---|---|
| scheduler / virtualization noise | | |
| CPU frequency / thermal changes | | |
| compiler optimization / vectorization | | |
| hardware prefetch | | |
| TLB / page effects | | |
| execution-order / cache-state effects | | |

## J — Bounded conclusion
Use this shape, adapting only to your evidence:

> Under the recorded environment/build/workload, changing traversal order changed the timing distribution in the predicted direction by an amount considered alongside observed run-to-run variation. The result is consistent with spatial-locality/cache-hierarchy effects. Without stronger mechanism evidence, this does not identify one exact cache level or prove a universal machine-independent speedup.

## K — Inference limits
Explicitly state what your evidence does **not** prove: exact miss counts, unique cache level, all CPUs/compilers/data sizes, production speedup, filesystem/storage effects, known cold-cache state, or causality from timing alone.

## L — Optional perf corroboration
- Used? yes / no
- If no: unavailable / restricted / not needed
- If yes: events, availability, multiplexing/restriction notes, interpretation limits.

Core completion does not require `perf`. Do not weaken security to obtain counters.

## M — Support metadata
- Question used?
- Hint 1 used?
- Hint 2 used?
- Expected Observation used?
- Full Explanation used?
- Where support was no longer needed:
