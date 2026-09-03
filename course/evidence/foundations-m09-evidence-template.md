# Foundations M09 Evidence Template

## A — Environment / Filesystem / Capability Preflight
- Dispatch / Working Commit:
- Operating System (uname / distribution):
- Kernel Version:
- Hardware Architecture:
- Python Implementation & Version:
- Filesystem Type for Synchronization Measurement:
- `os.fsync` Capability (`hasattr(os, "fsync")`):
- `os.fdatasync` Capability (`hasattr(os, "fdatasync")`):
- Timing Source Used (e.g. `time.perf_counter_ns`):
- Network / Curl Capability:
- Preflight Summary:

---

## B — EC-CON-016 Canonical First Home + Named Failure Model
- Canonical Concept ID: `EC-CON-016`
- First Home: M09 `L09-01`
- Canonical Definition: "A committed state survives a named restart or failure bound."
- Named Failure Model Requirement:
  - Bound 1: Process crash
  - Bound 2: Kernel panic / OS crash
  - Bound 3: Clean machine restart
  - Bound 4: Sudden power loss
  - Bound 5: Physical media destruction / disaster
- Why a durability claim is meaningless without an explicit named failure bound:

---

## C — Write / Runtime Flush / Sync Layer Mapping
- Layer 1: Application / Runtime buffer (e.g. Python `BufferedWriter`):
- Layer 2: Operating System Buffered State (Kernel Page Cache / Dirty RAM):
- Layer 3: Filesystem Data & Inode Metadata Handling:
- Layer 4: Storage Device Volatile Controller Cache:
- Layer 5: Physical Non-Volatile Storage Media:
- Why `write()`, `flush()`, and `close()` do not establish durability across power loss:

---

## D — Bounded Synchronization Measurement Raw Samples + Inference Limits
- Command Run: `python3 durability_observer.py`
- Payload Workload: `num_records` x `record_size_bytes` (Total logical bytes):
- Number of Trials:
- Raw Buffered Latency Samples (ns):
- Raw Synced Latency Samples (`os.fsync`) (ns):
- Mean Buffered Duration (ms):
- Mean Synced Duration (ms):
- Total `os.fsync` Calls Executed:
- Safety Caps Enforced (Max records, max record size, max payload):
- Inference Boundary Warning (Why Essential CS strictly forbids asserting universal latency ratios):

---

## E — fsync / fdatasync / File-Data / Directory-Metadata Boundaries
- `fsync(fd)` vs `fdatasync(fd)` Specification Boundary:
- File Data vs Inode Metadata Scope:
- Directory Entry Persistence Boundary:
  - Linux boundary: why `fsync(file_fd)` alone does not necessarily synchronize the containing directory entry:
  - Directory entries changed by the operation (new/create, same-directory rename, cross-directory rename):
  - Directory sync disposition(s): `PASS` or `ENVIRONMENT_LIMITED` with actual error evidence:
- Disaster Recovery Boundary (Why `fsync` is not a backup and does not protect against media destruction):

---

## F — WAL Ordering + Recovery Model Evidence
- Command Run: `python3 wal_model.py`
- Log Sequence Number (LSN) Monotonicity:
- Write-Ahead Invariant: `page_lsn <= flushed_lsn` verified prior to dirty data page disk flush:
- Crash Simulation Point:
- Recovery Model Boundary:
  - This activity is a bounded teaching model, **not full ARIES repeat-history**.
- Teaching Recovery Stages:
  - 1. Analysis Phase (Active vs Committed transactions identified):
  - 2. Simplified Redo Phase (committed updates reconstructed by this model):
  - 3. Undo Phase (surviving uncommitted updates rolled back):
- Full-ARIES distinction: repeat-history redo may include loser-transaction updates before Undo/CLR:
- Verified Recovered State Consistency:
- Why WAL is an ordering/recovery strategy rather than a magical durability primitive:

---

## G — Durability Policy Judgment + Acceptable Data-Loss Window
- Hypothetical Service Scenario:
- Chosen Durability Policy:
- Explicit Named Failure Bound:
- Defined Sync Point (`fsync` per transaction vs batched group commit):
- Acceptable Data-Loss Window (e.g., 0 for financial ledger, $\le 1\text{ s}$ for non-critical telemetry):
- Trade-off Analysis (Durability guarantee vs I/O throughput):

---

## H — HDD Mechanism Evidence
- Command Run: `python3 media_model.py`
- Mechanical Components: Spindle, Platters, Read/Write Head, Actuator Arm:
- Rotational Latency Calculation (RPM-dependent, e.g. 7200 RPM -> 4.17 ms average):
- Seek Latency Calculation (Mechanical arm movement, e.g. 8.5 ms average):
- Random 4 KiB Latency vs Sequential Streaming:
- Mechanical Constraint Boundary (No universal seek constant):

---

## I — SSD FTL / Invalidation / GC / Wear-Leveling Evidence
- NAND Flash Physics: Page Program (e.g. 4 KiB) vs Block Erase Granularity (e.g. 256 KiB - 4 MiB):
- Out-of-Place Update Mechanism:
- Flash Translation Layer (FTL) LBA-to-PBA Mapping:
- Page Invalidation on Overwrite:
- Garbage Collection (Victim selection, valid-page copying, block erase):
- Wear Leveling (Dynamic vs Static leveling):

---

## J — Bounded WAF Calculation / Model Evidence
- Label: `ILLUSTRATIVE MODEL EVIDENCE`
- Write Amplification Factor Definition: $\text{WAF} = \frac{\text{Bytes Written to Flash}}{\text{Bytes Written by Host}}$
- Scenario 1 (High Valid-Page Residency: 63 valid / 1 invalid page in 64-page block):
  - Host Bytes Written:
  - GC Copied Flash Bytes:
  - Total Flash Bytes Written:
  - Resulting WAF:
- Scenario 2 (Balanced Block: 32 valid / 32 invalid pages):
  - Resulting WAF:
- Scenario 3 (Sequential Append: 0 valid pages copied):
  - Resulting WAF:

---

## K — Media / Endurance Inference Limits
- Teaching Host-Write-Budget Formula (not a JESD218 rating): $\text{Budget}_{\text{TB}} = \frac{\text{Capacity}_{\text{GB}} \times \text{Assumed P/E Cycles}}{\text{WAF} \times 1000}$
- Illustrative Calculation (`ILLUSTRATIVE MODEL EVIDENCE`):
  - Drive Capacity: 1000 GB
  - Assumed P/E Cycles: 3000
  - Assumed WAF: 2.5
  - Calculated Illustrative Host-Write Budget:
- JEDEC Standards Reference (JESD218 endurance rating/test method; JESD219 workload):
- Manufacturer Product TBW / Warranty Reference if discussed:
- Inference Boundary Warning: teaching budget, JEDEC rating, manufacturer TBW, warranty terms, and physical failure date are not interchangeable:

---

## L — Block / File / Object Architecture Comparison
- Architecture Matrix:
  - Block Storage: block interface, attachment/coordination model, product/workload-specific latency, when-not-to-use
  - File Storage: path/file interface, local vs network semantics, multi-client coordination, when-not-to-use
  - Object Storage: object/key API, whole-object/versioned update semantics, provider/service constraints, when-not-to-use
- Architectural Trade-off Invariant:

---

## M — Current-Practice Assumptions: Source / Provider / Region / Checked Date + Cost Calculation
- Reference Data Source: `reference_assumptions.json`
- Provider: AWS
- Region: us-east-1
- Checked Date: 2026-09-02
- Rates Used:
  - Block (gp3): $0.08 / GB-month
  - File (EFS Standard): $0.30 / GB-month
  - Object (S3 Standard teaching snapshot): $0.023 / GB-month, $0.005 / 1k PUT, $0.0004 / 1k GET, first paid egress tier $0.09 / GB after the model's assumed 100 GB/month account-wide free allowance
- Evaluated Workload:
  - Capacity: 10,000 GB (10 TB)
  - Write Requests: 50,000
  - Read Requests: 1,000,000
  - Egress: 200 GB
- Cost Arithmetic Results:
  - Block Monthly Total: $800.00
  - File Monthly Total: $3,000.00
  - Object Monthly Total under committed assumptions: $239.65
- Account-Level Assumption: 100 GB free egress assumed otherwise unused; record billable egress.
- Model Omissions: provisioned IOPS/throughput, snapshots, replication/network charges, object/tier constraints, other services consuming free egress, higher transfer tiers, EFS throughput/access charges.

---

## N — Technology Evaluation Framework Judgment + When-Not-To-Use
- Technology Evaluated: Object Storage (Sample)
  - Problem:
  - Constraints:
  - Mechanism:
  - Gains:
  - Costs:
  - Failure Modes:
  - When NOT to use:

---

## O — Safety / Cleanup / Fact-vs-Inference / Concept Audit
- Safety Checks:
  - Root/sudo avoided:
  - Raw block devices avoided:
  - Host filesystem exhaustion avoided:
  - Hardware endurance stress avoided:
- Reset Utility: `python3 reset.py`
  - Cleanup verified: Zero leftover artifacts.
- Fact vs Inference Summary:
  - Direct Host Observations (Facts):
  - Illustrative Models & Calculations:
  - Current-Practice Cloud Pricing:
- Canonical Concept Audit:
  - `EC-CON-016 Durability` -> First Home in M09 `L09-01` [AUDIT: CONFIRMED]
  - Revisits Only: `EC-CON-006 Trade-off`, `EC-CON-010 Failure`, `EC-CON-012 Locality`, `EC-CON-003 Representation`, `EC-CON-002 Abstraction`, `EC-CON-005 Interface` [AUDIT: CONFIRMED]
  - New Concept IDs Created: NONE [AUDIT: CONFIRMED]
