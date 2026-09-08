# Foundations M23 Evidence Template — Systems Thinking & Judgment

Use this template for **one actual learner observation**. Do not prefill or copy another learner's runtime values, candidate timings, percentiles, clock resolutions, cloud prices, technology decisions, or PASS/FAIL evaluations.

> **Evaluation Invariant**: Machine PASS != learner competency PASS. Automated checks prove mechanical correctness of code fixtures; learner competency requires conceptual mastery, honest boundary analysis, and sound architectural judgment.

---

## A — Environment Capabilities & Preflight

- Execution commit / ref: `[Record actual HEAD commit SHA]`
- Exact command(s) actually run: `[Record command text exactly, e.g. python tests/preflight_security_synthesis.py --module M23]`
- Exact runtime disposition for each command: `[Record PASS / FAIL / BLOCKED / NOT RUN; never infer PASS from capability absence]`
- Host Operating System / kernel / platform: `[Record actual OS, release, architecture]`
- Python Implementation & Version: `[Record actual Python implementation and version]`
- Timing API Probed (`time.monotonic_ns`, `time.get_clock_info`): `[Record REQUIRED CAPABILITY PASS or BLOCKED]`
- Actual Clock Characteristics Observed:
  - Monotonic clock implementation: `[Record actual clock info, e.g. QueryPerformanceCounter / clock_gettime(CLOCK_MONOTONIC)]`
  - Reported timer resolution: `[Record actual reported resolution in seconds, e.g. 1.00e-07 s]`
  - Monotonic flag: `[Record True/False]`
  - Adjustable flag: `[Record True/False]`
  - Note: `[Record: Integer nanosecond reporting units do not imply nanosecond hardware clock resolution]`
- Course-Owned Scratch Writability (`labs/foundations/m23/.scratch`): `[Record REQUIRED CAPABILITY PASS or BLOCKED]`
- OQ-BP-006 Environment Policy Status: `OPEN / UNRESOLVED (Capability-based evaluation; no course-wide CPython pin frozen in learner truth)`

---

## B — Measurement Protocol Card

Record the scientific measurement protocol designed for the system under test in `labs/foundations/m23/activity_l23_01.py`:

- Specific Engineering Question: `[State the exact empirical question to answer; reject generic benchmarks without a question]`
- Falsifiable Hypothesis: `[State the hypothesis in testable form, e.g. "Under an open arrival rate of 100 req/s, an uncoordinated synchronous client underestimates p99 latency during stalls because it couples request generation to response completion."]`
- Independent Variable(s): `[Identify independent variables manipulated, e.g. generator type (naive vs arrival-scheduled), injected synthetic stall duration]`
- Dependent Variable(s): `[Identify dependent variables measured, e.g. response latency, queue waiting time, p50, p90, p99 percentiles]`
- Workload Model Selection & Rationale: `[State whether Open or Closed arrival model was selected, and justify why based on the engineering question]`
- Arrival Assumptions: `[State assumptions regarding arrival schedule, inter-arrival distribution (Poisson, deterministic fixed interval), and independence from service completion]`
- Warm-Up Strategy Rationale: `[State whether warm-up iterations were discarded or retained, explaining the underlying mechanism (e.g. JIT, CPU frequency governor, buffer cache warming vs cold-start CLI benchmarking)]`
- Sample Size & Stopping Criterion Rationale: `[Explain sample count justification based on observed variance and required confidence bounds; reject universal constants such as "always run 30 times"]`
- Monotonic Clock Source: `[Record clock source API and why monotonic time is mandatory for elapsed duration over wall-clock calendar time]`
- Interference & Noise Assumptions: `[Document assumed sources of environmental noise: OS context switching, background daemons, thermal throttling, scheduler jitter]`

---

## C — Coordinated-Omission Comparison

Record the comparative latency observations from `labs/foundations/m23/activity_l23_01.py`:

- Synthetic Stall Parameter: `[Record synthetic pause duration in ms and request index where injected; explicitly mark as synthetic pause, not uninstrumented GC]`
- Target Scheduled Arrival Rate: `[Record scheduled inter-arrival delta in ms or req/sec]`

| Summary Metric | Naive Synchronous Loop (Service Time Only) | Arrival-Scheduled Generator (Queue + Service) | Omission Ratio (Sched / Naive) | What the Delta Proves |
| :--- | :--- | :--- | :--- | :--- |
| **Sample Count** | `[Record N]` | `[Record N]` | `[Record ratio]` | `[Explain sample preservation]` |
| **Minimum** | `[Record min ms]` | `[Record min ms]` | `[Record ratio]` | `[Explain baseline service latency]` |
| **p50 (Median)** | `[Record p50 ms]` | `[Record p50 ms]` | `[Record ratio]` | `[Explain typical user experience under load]` |
| **p90** | `[Record p90 ms]` | `[Record p90 ms]` | `[Record ratio]` | `[Explain queue backlog visibility in tail]` |
| **p95** | `[Record p95 ms]` | `[Record p95 ms]` | `[Record ratio]` | `[Explain tail degradation]` |
| **p99** | `[Record p99 ms]` | `[Record p99 ms]` | `[Record ratio]` | `[Explain catastrophic tail latency reveal]` |
| **Maximum** | `[Record max ms]` | `[Record max ms]` | `[Record ratio]` | `[Explain peak stall impact]` |
| **Mean** | `[Record mean ms]` | `[Record mean ms]` | `[Record ratio]` | `[Explain aggregate work & energy]` |
| **Standard Deviation** | `[Record stddev ms]` | `[Record stddev ms]` | `[Record ratio]` | `[Explain variance]` |

- Inference Limit: `[Record explicit statement of what this synthetic observation does and does not prove about real distributed systems under uninstrumented production GC]`

---

## D — Summary-Statistic Judgment

Analyze the appropriate use of summary metrics without dogmatic rules of thumb:

- Metric: `[e.g. p99 latency]`
  - Why chosen: `[Explain what specific SLO or tail behavior it evaluates]`
  - Question it answers: `[Explain user satisfaction or multi-tier fan-out risk]`
  - What it hides: `[Explain why p99 hides the shape of the remaining 1% and does not reveal total work done]`
- Metric: `[e.g. Mean & Total Count]`
  - Why chosen: `[Explain why mean is mandatory for capacity planning, energy consumption, and cloud billing]`
  - Question it answers: `[Explain throughput and aggregate resource consumption]`
  - What it hides: `[Explain why mean hides heavy-tailed degradation and bimodality]`
- Dogmatism Rejection: `[Explicitly articulate why "always use p99" and "mean is always wrong" are engineering misconceptions]`

---

## E — Decision D-015 12-Dimension Technology Evaluation Card

Record the evaluation audited by `labs/foundations/m23/activity_l23_02.py`:

- Candidate Technology Name: `[Record technology name, e.g. Redis / Apache Kafka / Proposed Service]`
- Evaluated Scenario Context: `[Record architectural context and target SLOs]`
- Final Engineering Decision: `[Record ADOPT / REJECT / DEFER / TRIAL; REJECT is a valid decision category, but machine structural PASS is not decision-quality PASS]`
- Overall Decision Justification: `[Summarize trade-off rationale]`

### 12-Dimension Evaluation Audit:

| Dimension | Evaluation Rationale & Evidence | Residual Risk / Non-Guarantee |
| :--- | :--- | :--- |
| **1. Problem & Requirement Clarity** | `[State exact bottleneck or failure mode]` | `[Identify risks if problem was misdiagnosed]` |
| **2. Data Model & Access Pattern Fit** | `[Analyze alignment with access patterns]` | `[Identify impedance mismatches]` |
| **3. Consistency & Durability Guarantees** | `[State ACID vs eventual consistency trade-offs]` | `[Identify data loss or stale read boundaries]` |
| **4. Failure Modes & Operational Complexity** | `[Identify cascades, split-brain, OOM, on-call]` | `[Identify new failure modes introduced]` |
| **5. Performance & Scalability Boundaries** | `[Quantify throughput/latency ceilings]` | `[Identify bottleneck shifts]` |
| **6. Observability & Debuggability** | `[State metrics, tracing, profiling mechanisms]` | `[Identify blind spots in production debugging]` |
| **7. Security, Trust & Isolation** | `[Evaluate attack surface, auth, network boundaries]` | `[Identify credential and isolation liabilities]` |
| **8. Ecosystem, Maintenance & Longevity** | `[Evaluate community, release cadence, bus factor]` | `[Identify maintenance abandonment risks]` |
| **9. Licensing & Governance** | `[Audit open-source license (BSD/Apache vs SSPL/BSL)]` | `[Identify legal and governance lock-in risks]` |
| **10. Cost Model: Infrastructure & Human** | `[Calculate server billing AND human on-call load]` | `[Acknowledge human cognitive overhead]` |
| **11. Migration & Reversibility / Exit Strategy** | `[Detail explicit exit strategy and decoupling plan]` | `[Identify technical debt if migration is delayed]` |
| **12. Alternatives Considered & Rejection Rationale** | `[Detail simpler mechanisms: B-Tree index, SQLite]` | `[Explain why simpler alternatives were chosen or rejected]` |

---

## F — Architecture Decision Record (ADR)

- Title: `ADR-[Number]: [Title of Decision, e.g. Rejection of Redis in Favor of Relational Database B-Tree Index]`
- Status: `[ACCEPTED / SUPERSEDED / REJECTED]`
- Context & Problem Statement: `[Detail technical context, read/write ratios, latency requirements, team operational budget]`
- Decision Drivers (Requirements): `[List primary SLOs, maintenance constraints, and durability invariants]`
- Considered Options: `[Option 1 (Chosen / Rejected), Option 2 (Alternative), Option 3 (Baseline)]`
- Decision Outcome: `[State chosen decision clearly, e.g. "We will REJECT Option 1 and implement Option 2..."]`
- Positive Consequences: `[Detail complexity avoided, cost saved, reliability gained]`
- Negative Consequences & Accepted Liabilities: `[Detail trade-offs accepted]`
- Reversibility & Exit Strategy: `[Detail trigger threshold where this decision would be revisited, and how to migrate]`
- Uncertain Facts Requiring Runtime Validation: `[Identify facts that must be empirically monitored]`

---

## G — Vendor / Documentation / Observation Claim Audit

Distinguish claim categories to prevent marketing self-deception:

| Technical Claim | Source Classification (Vendor Marketing / Official Docs / Local Observation) | Date / Version Checked | Empirical Non-Proof (What This Source Fails to Prove) | Impact on Architectural Decision |
| :--- | :--- | :--- | :--- | :--- |
| `[e.g. "Sub-millisecond latency"]` | `[Vendor Marketing / Docs]` | `[Date/Version]` | `[Fails to account for network hops, serialization, or client GC]` | `[Must be independently measured in local harness]` |
| `[e.g. "Zero memory fragmentation"]` | `[Vendor Docs]` | `[Date/Version]` | `[Fails to hold under high allocation churn and jemalloc arenas]` | `[Requires monitoring memory fragmentation ratio]` |
| `[e.g. "4ms B-Tree index lookup"]` | `[Local Empirical Observation]` | `[Date/Version]` | `[Observed on local SSD; does not prove performance under disk lock contention]` | `[Validates satisfying 20ms SLO on current hardware]` |

---

## H — AI Hypothesis Audit (If AI is Used)

- AI-Generated Claim / Recommendation: `[Record exact suggestion, e.g. "AI suggested migrating to Cassandra for infinite scale"]`
- Safe Classification: `UNTRUSTED CANDIDATE HYPOTHESIS (Per Curriculum Invariant 6 & OQ-BP-001 safe interim state)`
- Verification Route Executed:
  - Source / Specification Cross-Reference: `[Record finding from formal documentation]`
  - Quantitative Napkin-Math Check: `[Record Fermi calculation refuting or bounding the claim]`
  - Local Test / Prototype Observation: `[Record test result]`
- Verification Outcome: `[CONFIRMED / REFUTED / DEFERRED]`
- Architectural Conclusion: `[Explain how the AI suggestion was corrected or rejected based on engineering constraints]`
- OQ-BP-001 Policy Status: `OPEN / RFC-GATED (AI literacy remains safe candidate capability; zero Core AI module creep)`

---

## I — Fermi / Capacity Model

Record napkin-math capacity planning calculations using `labs/foundations/m23/fermi_cost.py`:

- Scenario Name: `[e.g. Photo Sharing Service / Notification Subsystem]`
- Core Input Assumptions (Explicitly Stated):
  - Daily Active Users (DAU): `[Record DAU]`
  - Actions per User per Day: `[Record action counts, e.g. uploads/day, views/day]`
  - Average Item Payload Size: `[Record size with explicit units: B, KB, KiB, MB, MiB]`
  - Replication Factor: `[Record factor, e.g. 3.0x]`
  - Indexing / Metadata Overhead Ratio: `[Record ratio, e.g. 0.15 for 15%]`
  - Retention Window: `[Record days, e.g. 90 days hot retention]`
  - Peak-to-Average Traffic Ratio: `[Record ratio, e.g. 3.0x]`
- Step-by-Step Arithmetic:
  - Daily Logical Data Volume: `[Show formula and result in GB/TB]`
  - Daily Physical Storage Ingestion: `[Show formula with replication in GB/TB]`
  - Total Retained Storage: `[Show formula over retention window in TB/TiB]`
  - Average Egress Bandwidth: `[Show formula: Total Bytes / 86400 * 8 in Mbps/Gbps]`
  - Peak Egress Bandwidth: `[Show formula: Avg Bandwidth * Peak Ratio in Mbps/Gbps]`
  - RAM Working Set Fit: `[Show formula: Active dataset vs Usable RAM]`
- Baseline Conclusion: `[State primary bottleneck resource (e.g. network egress vs disk I/O vs CPU)]`

---

## J — Bottleneck / Sensitivity Matrix

Evaluate architectural sensitivity under changed assumptions:

| System Resource | Baseline Utilization / Sizing | Changed Assumption (e.g. 10x Load / 365d Retention) | Resulting Projected Demand | Bottleneck Shift / Cliff | Architectural Mitigation / Trade-Off |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Compute (CPU)** | `[Baseline cores/utilization]` | `[10x request volume]` | `[Projected demand]` | `[Analyze CPU saturation]` | `[Connection pooling, caching, async worker]` |
| **Memory (RAM)** | `[Baseline RAM working set]` | `[5x active item count]` | `[Projected demand]` | `[Does dataset exceed physical RAM?]`| `[Eviction policy, tiered storage, sharding]` |
| **Storage (Disk)** | `[Baseline retained TB]` | `[365-day indefinite retention]` | `[Projected demand]` | `[Disk capacity exhaustion]` | `[Cold tier archiving, object storage, compression]` |
| **Network Egress** | `[Baseline Gbps bandwidth]` | `[10x views / uncompressed images]` | `[Projected demand]` | `[NIC saturation / cloud egress billing shock]`| `[Edge CDN caching, AVIF/WebP image compression]`|
| **Human Ops** | `[Baseline hours/month on-call]` | `[Added distributed cluster dependency]` | `[Projected on-call friction]`| `[Alert fatigue / team cognitive overload]` | `[Simpler monolithic architecture, managed service]` |

---

## K — Competencies, Concepts & Reviewer Judgment

### Primary Competencies Demonstrated:
- **`Estimate`**: Performed order-of-magnitude Fermi calculations; tracked units precisely (bits vs Bytes, decimal vs binary prefixes); made all scaling assumptions explicit.
- **`Judge`**: Evaluated candidate technologies using Decision D-015 across 12 dimensions; defended technology rejection as a superior engineering outcome; balanced multi-currency TCO.
- **`Diagnose`**: Identified coordinated omission in synchronous load generators; exposed misleading summary statistics; identified latency distribution heavy tails.
- **`Learn-New-Tech`**: Dissected unfamiliar technology claims; separated vendor marketing from documentation and empirical observation.
- **`Explain`**: Articulated why arrival-scheduled latency accounting exposes queuing delays hidden by completion-coupled generators; explained why adding a technology moves complexity.

### Canonical Formal Concept Revisits:
- **`EC-CON-007 Specification`** (First Home: M02 `L02-03`): Revisit. System requirements vs candidate technology specifications; schema conformance in technology evaluations.
- **`EC-CON-009 Correctness`** (First Home: M02 `L02-03`): Revisit. Correctness of empirical latency accounting; preventing coordinated omission distortions.
- **`EC-CON-010 Failure`** (First Home: M03 `L03-03`): Revisit. Tail latency degradation, resource exhaustion, and cascading failures under scaling cliffs.
- **`EC-CON-016 Durability`** (First Home: M09 `L09-01`): Revisit. Long-term storage capacity scaling and replication cost models.

### Lead Reviewer Competency Disposition:
- Learner Competency Evaluation Status: `[NOT RUN / PASS / FAIL]`
- Reviewer Notes & Feedback: `[Lead Reviewer durable comments]`

---

## L — Currentness, Provenance, Rights & Cleanup

### Authority Sources & Currentness Audit:
- Python Timing Semantics (`time.monotonic_ns`, `time.get_clock_info`): Checked against official Python 3 documentation (PSF license).
- Coordinated Omission: Gil Tene (Azul Systems). Foundational methodology for open workload measurement (STABLE).
- Systems Performance Methodology: Brendan Gregg, *Systems Performance: Enterprise and the Cloud*, 2nd Ed. (STABLE).
- Decision D-015: Essential CS Canonical Decision Registry (`meta/DECISIONS.md`).
- Numbers Every Programmer Should Know: Classical distributed systems latency reference (Jeff Dean / Peter Norvig). Noted as classical hardware baseline, not timeless universal truth.
- FinOps Framework: FinOps Foundation cloud cost governance methodology (CURRENT).

### Provenance & Rights Caveat:
- Curriculum prose, original diagrams, and evaluation rubrics: CC BY-SA 4.0.
- Lab test fixtures, benchmarking harnesses, and modeling tools: Apache-2.0.
- Zero copied third-party benchmark diagrams, proprietary pricing sheets, or external exercise text.

### Environment Cleanup Verification:
- Reset script executed: `python labs/foundations/m23/reset.py`
- Removed scratch artifacts count: `[Record count]`
- Repository status clean: `[Confirm git status shows no uncommitted scratch/pycache artifacts]`
- Unresolved Technical Uncertainties: `[Record any remaining questions]`
