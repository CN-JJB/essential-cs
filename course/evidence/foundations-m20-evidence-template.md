# Foundations M20 Evidence Template — Observability & Reliability Engineering

Use this template for **one actual learner observation**. Do not prefill or copy another learner's timestamps, port numbers, trace IDs, duration measurements, percentile values, budget results, or postmortem conclusions.

---

## A — Environment Capabilities & Preflight

- Execution commit / ref: `[Record actual HEAD commit SHA]`
- Host Operating System / kernel / platform: `[Record actual OS, release, architecture]`
- Python Implementation & Version: `[Record actual Python version]`
- Monotonic & Perf-Counter Clock Capability: `[Record time.get_clock_info('monotonic') and ('perf_counter') details]`
- Localhost Ephemeral Bind Capability (`127.0.0.1:0`): `[Record bind disposition and sample port]`
- Course-Owned Scratch Directory Readiness: `[Record scratch path writability status]`
- Optional OpenTelemetry SDK Disposition: `[Record OPTIONAL PACKAGE AVAILABLE or OPTIONAL PACKAGE NOT INSTALLED / FALLBACK TO ZERO-SAAS CORE]`
- OQ-BP-006 Environment Policy Status: `CLOSED (technical environment-definition/realization per #167; #158 re-check still required)`

---

## B — Telemetry Signal Selection & Missingness Boundary

- Stated Diagnostic Question: `[Record the specific engineering question being investigated]`
- Chosen Telemetry Signal(s): `[Record selection: Metrics / Structured Logs / Traces / Combination and rationale]`
- Actual Fields / Records Observed: `[Record summary of observed fields/series]`
- Diagnostic Missingness (What the Chosen Signal Cannot Establish):
  `[Learner explains what information the selected signal necessarily omits or cannot prove alone]`
- Cardinality & Privacy Considerations:
  `[Learner evaluates metric label cardinality risks or log privacy/storage constraints]`

---

## C — Clock Semantics & Monotonic Timing (EC-CON-001 State)

- Fake Wall-Clock Injected Step Input: `[Record configured simulated backward step, e.g. -5.0s]`
- Wall-Clock Readings Observed:
  - T0 (Wall Time): `[Record actual float timestamp]`
  - T1 (Wall Time after step): `[Record actual float timestamp]`
  - Wall Subtraction ($T_1 - T_0$): `[Record actual negative result, e.g. < 0s]`
- Monotonic Timer Readings Observed:
  - Monotonic $T_0$: `[Record actual float seconds]`
  - Monotonic $T_1$: `[Record actual float seconds]`
  - Monotonic Elapsed Duration: `[Record actual positive duration in ms]`
- Exact Clock Source Labels:
  - Event / Calendar Timestamps: `CLOCK_REALTIME / time.time()`
  - Elapsed Correctness-Sensitive Durations: `CLOCK_MONOTONIC / time.monotonic()`
- Mechanism Inference Limit:
  `[Learner articulates why the teaching adapter proves the wall-subtraction vulnerability without being a real NTP reproduction, and why real NTP can both step and rate-slew]`

---

## D — Distribution Statistics: Tail vs. Mean (EC-CON-015 Concurrency)

- Dataset / Workload Identity: `[Record synthetic or recorded workload dataset identity]`
- Sample Count & Window: `[Record sample count N and collection window]`
- Exact Percentile Convention: `nearest_rank (rank = ceil(p/100 * N), 1-based index)`
- Computed Distribution Statistics:
  - Sample Count ($N$): `[Record actual N]`
  - Mean Latency: `[Record actual mean in ms]`
  - Median ($p50$): `[Record actual p50 in ms]`
  - 90th Percentile ($p90$): `[Record actual p90 in ms]`
  - 95th Percentile ($p95$): `[Record actual p95 in ms]`
  - 99th Percentile ($p99$): `[Record actual p99 in ms]`
- Tail-vs-Mean Interpretation:
  `[Learner explains why the mean alone fails to reflect tail queueing/latency, and why p99 diverges from p50]`
- User Inference Limit:
  `[Learner confirms why a request percentile cannot be translated into a fixed percentage of unique users without an explicit 1:1 user-to-request model]`

---

## E — SLI / SLO & Error Budget Worksheet (EC-CON-010 Failure)

- Named Service & Scenario Behavior: `[Record service boundary and evaluated user journey]`

### Scenario A: Request-Based Event SLI / SLO (Event / Request Error Budget)
- Request SLI Definition & Denominator:
  - Good Requests ($G$): `[Record actual good requests count]`
  - Total Valid Requests ($V$): `[Record actual total valid requests count]`
  - Request SLI Formula: `(Good Requests / Total Valid Requests) * 100%`
  - Actual Request SLI Observed: `[Record computed SLI percentage]`
- Request SLO Target: `[Record scenario SLO target, e.g. 99.0% or 99.9%]`
- Request Error Budget Calculation:
  - Allowed Bad Requests Budget: `[Record calculated budget: Total Valid * (1 - SLO Target)]`
  - Actual Bad Requests Observed: `[Record actual bad requests: Total Valid - Good Requests]`
  - Remaining Request Error Budget: `[Record remaining budget in requests]`
  - Budget Consumed Percentage: `[Record percentage of request budget spent]`
  - Budget Status: `[Record mathematical status: EXHAUSTED or REMAINING]`
  - Policy Note on Budget Depletion:
    `[Learner distinguishes mathematical budget exhaustion from organizational policy response (e.g. release freeze vs sprint prioritization)]`

### Scenario B: Time-Based Availability SLI / SLO (Time / Downtime Error Budget)
- Time Availability SLI Definition:
  - Total Measurement Window: `[Record window duration, e.g. 30 days = 43,200 minutes]`
  - Measured Uptime Duration: `[Record actual uptime in minutes]`
  - Time SLI Formula: `(Uptime Minutes / Total Window Minutes) * 100%`
  - Actual Time Availability Observed: `[Record computed availability percentage]`
- Time Availability SLO Target: `[Record scenario SLO target, e.g. 99.9%]`
- Downtime Budget Calculation:
  - Allowed Downtime Minutes Budget: `[Record calculated budget: Window * (1 - SLO Target), e.g. 43.2 minutes]`
  - Actual Downtime Minutes Observed: `[Record actual downtime minutes in window]`
  - Remaining Downtime Budget: `[Record remaining downtime minutes]`
  - Downtime Budget Consumed Percentage: `[Record percentage of downtime budget spent]`

### Universal Definition & SLA Boundaries:
- Universal SLI Limit: `[Learner explains why good/valid ratio is one common SLI form, not the definition of every SLI]`
- Prohibition on Ratio-to-Downtime Conversion:
  `[Learner articulates why request-based SLI ratios must NEVER be converted directly into allowed downtime minutes]`
- SLA Distinction: `[Learner explains why an external contractual SLA with remedies differs from an internal SLO target, and why an SLA percentage is not an independent failure probability]`

---

## F — W3C Trace Context Level 1 version-00 (EC-CON-015 Concurrency)

- Actual Generated `traceparent` Header: `[Record raw 55-character header]`
- Parsed Trace Context Components:
  - Version: `[Record parsed 2-hex version, e.g. 00]`
  - Trace ID: `[Record parsed 32-hex trace_id]`
  - Parent ID / Span ID: `[Record parsed 16-hex parent_id]`
  - Trace Flags: `[Record parsed 2-hex flags and sampled boolean]`
- Cross-Service Propagation Evidence:
  - ServiceA Outgoing Parent ID: `[Record span_id generated by ServiceA]`
  - ServiceB Incoming Parent ID: `[Record parent_id parsed by ServiceB]`
  - ServiceB Outgoing Parent ID: `[Record span_id generated by ServiceB]`
  - ServiceC Incoming Parent ID: `[Record parent_id parsed by ServiceC]`
  - Trace ID Invariance: `[Confirm identical 32-hex trace_id observed across all three hops]`
- Malformed Input Handling:
  - All-Zero Trace ID Rejection: `[Record ValueError exception output]`
  - All-Zero Parent ID Rejection: `[Record ValueError exception output]`
  - Malformed Length / Characters Rejection: `[Record ValueError exception output]`
- Future Version & Security Boundary:
  - Version Scope: `[Learner notes that minimal version-00 parser does not implement future Level 2 or vendor extensions]`
  - Security Invariant: `[Learner articulates why trace IDs are diagnostic correlation identifiers, not authentication tokens or user identity]`

---

## G — Structured Logs & Correlation Engine (EC-CON-001 State)

- Actual Structured Records Emitted:
  - ServiceA Record: `[Record raw JSON log entry]`
  - ServiceB Record: `[Record raw JSON log entry]`
  - ServiceC Record: `[Record raw JSON log entry]`
- Timestamp vs. Duration Separation:
  - ISO UTC Calendar Field: `[Record timestamp_utc field]`
  - Monotonic Elapsed Duration Field: `[Record duration_ms field]`
- Log Privacy Audit:
  - Confirmation of Zero Secret Logging: `[Learner confirms authorization, cookies, passwords, and tokens are omitted or redacted]`
- Correlation Filter vs. Manual Inspection:
  - Total Uncorrelated Logs in Pool: `[Record count of total logs across concurrent requests]`
  - Correlated Logs Matched by Trace ID: `[Record count of logs filtered for this trace]`
  - Diagnostic Efficiency: `[Learner evaluates time/complexity difference between manual log searching and trace filtering]`

---

## H — Controlled Production Incident & Mitigation (EC-CON-010 Failure)

- Injected Fault Configuration:
  - Fault Mode: `[Record DELAY or HTTP_500]`
  - Target Service: `ServiceC (Storage Mock)`
  - Parameter Value: `[Record injected delay in ms or error code]`
- Upstream Symptom Observed at ServiceA:
  - Gateway Status Code: `[Record status code]`
  - Total Request Duration: `[Record elevated duration in ms]`
- Correlated Timeline Reconstruction:
  - Hop Durations Identified: `[Record duration_ms for ServiceA, ServiceB, ServiceC]`
  - Localized Bottleneck Component: `[Record localized component, e.g. ServiceC]`
- Safe Scenario Mitigation:
  - Mitigation Action Taken: `[Record mitigation, e.g. ServiceB local cache fallback enabled]`
  - Service Restoration Verification:
    - Mitigated Status Code: `[Record status code, e.g. 200]`
    - Mitigated Latency: `[Record normalized duration in ms]`
    - Recovery Verification Status: `[Record actual verified status: PASS / BLOCKED / NOT RUN]`
    - Recovery Verification Evidence: `[Record observed latency reduction and HTTP 200 verification]`
- Long-Term Resolution Tracking:
  - Resolution Action Status: `NOT PERFORMED / PROPOSED FOLLOW-UP`
  - Proposed Follow-Up Issue / Scope: `[Record proposed permanent architectural fix or investigation item]`
- Exact Inference Limits:
  `[Learner explains why ground-truth localization in this controlled scenario does not imply real-world socio-technical incidents always have a single root cause, and notes security/data-integrity exceptions where containment precedes traffic restoration]`

---

## I — Blameless Incident Postmortem Artifact (EC-CON-010 Failure)

- Incident Reference ID: `[Record incident ID, e.g. INC-2026-M20-001]`
- Summary of Customer Impact: `[Record observed latency and error impact]`
- Timeline of Phases:
  - Detection: `[Record detection timestamp and observed latency symptom (no fabricated alerts)]`
  - Triage: `[Record triage timestamp and trace correlation findings]`
  - Mitigation: `[Record mitigation timestamp and action]`
  - Resolution: `[Record resolution status: NOT PERFORMED / PROPOSED FOLLOW-UP, and proposed permanent fix plan]`
- Proximate Mechanism (Injected Symptom): `[Record proximate technical mechanism observed in fixture]`
- Contributing Systemic Conditions:
  `[Record at least 3 contributing conditions analyzing interfaces, tools, and safeguards without personal blame]`
- Recovery Verification:
  - Recovery Status: `[Record actual verified status: PASS / BLOCKED / NOT RUN]`
  - Recovery Evidence: `[Record observed latency normalization following mitigation]`
- Mitigation vs. Resolution vs. Prevention Distinction:
  `[Learner distinguishes temporary traffic restoration from permanent code defect resolution (unexecuted) and preventative hardening]`
- Action Items & Defensive Safeguards: `[Record concrete preventative engineering action items]`
- Unresolved Questions: `[Record open technical questions regarding boundaries or scaling]`

---

## J — Strictly Optional OpenTelemetry Route (EXP-04 & LAB-OPT-04)

- Optional Route Disposition: `[Record EXECUTED, INSPECTED ONLY, or BLOCKED / NOT RUN]`
- Pinned OpenTelemetry Release: `open-telemetry/opentelemetry-python @ v1.44.0 (2026-07-16)`
- EXP-04 Source Reading Findings:
  - API Boundary Path: `opentelemetry-api/src/opentelemetry/trace/span.py`
  - SDK Boundary Path: `opentelemetry-sdk/src/opentelemetry/sdk/trace/__init__.py`
  - Pinned Timestamp Implementation: `[Learner records that default _Span timestamps use imported time_ns()]`
  - Clock Semantic Contrast:
    `[Learner articulates why OpenTelemetry time_ns() is system epoch time and NOT evidence for the Core monotonic-duration invariant]`
  - Confirmed Claim: `[Record claim confirmed by pinned source]`
  - Conditional Claim: `[Record claim made conditional by pinned source]`
- LAB-OPT-04 Local Tracer Run (if executed):
  - Emitted Console Span JSON: `[Record sample span output showing parent-child link]`
  - Comparison with Core Structured Log: `[Learner contrasts OpenTelemetry span schema with Core JSON logs]`

---

## K — Synthesis, Verification & Visual Audit

- Cleanup Confirmation: `[Confirm reset.py executed cleanly twice; .scratch/ purged]`
- Concepts Revisited & Deepened:
  - `EC-CON-001 State`: `[Learner articulates how telemetry provides partial state observations]`
  - `EC-CON-015 Concurrency`: `[Learner articulates how correlation context resolves concurrent request interleaving]`
  - `EC-CON-010 Failure`: `[Learner articulates the incident lifecycle and blameless analysis]`
- Competencies Demonstrated:
  - L20-01: `Observe`, `Diagnose`, `Judge`
  - L20-02: `Diagnose`, `Observe`, `Explain`
- Required Visuals Checked:
  - `FIG-M20-01`: The Telemetry Triad & Clock Semantics Boundary: `[Learner confirms visual inspected and understood]`
  - `FIG-M20-02`: W3C Trace Context Propagation & The Incident Lifecycle: `[Learner confirms visual inspected and understood]`
- Authoritative Source Currentness Recheck:
  - Python `time` module documentation (`time.monotonic`, `time.time`): `[Learner notes latest audited standard status]`
  - W3C Trace Context Level 1 Recommendation (2021): `[Learner notes standard recommendation status]`
  - Google SRE Workbook (SLI/SLO & Postmortems): `[Learner notes methodology reference]`
  - OpenTelemetry Python release status: `[Learner notes pinned release audit status]`
