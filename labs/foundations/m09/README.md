# M09 — Storage Engine & Durable Storage Lab Packet

This lab packet provides safe, bounded, machine-checkable experiments and illustrative models for durability boundaries, Write-Ahead Logging (WAL), storage media mechanics (HDD vs SSD), and storage architecture economics.

## Included Fixtures & Tools

1. **`durability_observer.py`** (Supports `L09-01`)
   - Establishes the canonical definition of **EC-CON-016 Durability (持久性)**: *"A committed state survives a named restart or failure bound."*
   - Identifies named failure bounds: process crash, kernel panic/OS crash, clean restart, sudden power loss, storage media destruction.
   - Measures raw timing samples comparing ordinary buffered writes against synchronized writes (`os.fsync`).
   - Sync call count and path are machine-observable within the program.
   - Demonstrates the Linux file-vs-directory synchronization boundary: file `fsync()` does not necessarily synchronize the containing directory entry; when the named failure model requires pathname persistence, the directories whose entries changed must be included in the sync protocol. Cross-directory rename requires reasoning about both parents, and directory-fsync capability/errors are recorded truthfully.
   - **Key Invariant**: Latency and ratios are empirical host observations, NOT universal constants. `fsync()` is a synchronization interface, not a substitute for backups or physical disaster recovery.

2. **`wal_model.py`** (Supports `L09-01`)
   - Demonstrates Write-Ahead Logging as an ordering and recovery strategy.
   - Enforces the Write-Ahead Invariant: log intent must reach durable storage before dirty main-state data pages may be flushed (`page_lsn <= flushed_lsn`).
   - Simulates a bounded crash model and a **simplified teaching recovery**, explicitly not full ARIES:
     - **Analysis**: distinguishes committed from active transactions in the surviving model log.
     - **Redo**: the teaching model reconstructs committed updates.
     - **Undo**: rolls back surviving uncommitted updates.
     - Full ARIES uses repeat-history redo before undoing losers.
   - **Key Invariant**: WAL is not durable merely because it is called a log; durability requires log synchronization before transaction commit acknowledgement.

3. **`media_model.py`** (Supports `L09-02`)
   - Provides pure calculation and illustrative simulations labeled **ILLUSTRATIVE MODEL EVIDENCE**.
   - Mechanical HDD model: Calculates seek, rotational, and transfer latency components, demonstrating why random I/O incurs heavy mechanical arm movement.
   - SSD Flash Translation model: Demonstrates NAND Flash constraints (page read/program vs block erase, out-of-place updates, invalidation, garbage collection, and wear leveling).
   - Write Amplification Factor ($\text{WAF} = \frac{\text{Bytes Written to Flash}}{\text{Bytes Written by Host}}$): Simulates GC block reclamation scenarios with varying valid-page densities.
   - Endurance arithmetic: computes an **illustrative host-write budget** from capacity, assumed P/E cycles and WAF. It is not a JESD218 rating; JESD218/JESD219, manufacturer TBW labels, and product warranty terms are kept distinct.

4. **`storage_economics.py` & `reference_assumptions.json`** (Supports `L09-03`)
   - Compares Block, File, and Object storage architectures at the mechanism and interface level.
   - Evaluates architectures using the **Technology Evaluation Framework** (Problem, Constraints, Mechanism, Gains, Costs, Failure Modes, When-not-to-use).
   - Parameterized monthly cost estimation across storage capacity, write/read requests, and data egress.
   - Uses committed current-practice reference assumptions (`reference_assumptions.json`, checked 2026-09-02), source URLs, region/currency metadata, a stated 100 GB account-wide free-egress assumption, and explicit omissions. Calculations remain parameterized and must be re-verified for production use.
   - Capability-gated network observation: Probes public HTTP headers if network is available; otherwise truthfully reports `SKIP / NO LIVE NETWORK OBSERVATION` with zero synthetic transcripts.

5. **`test_activity.py`**
   - Automated unit test suite verifying all invariants across `L09-01`, `L09-02`, and `L09-03`.

6. **`reset.py`**
   - Deterministically cleans up temporary test files and bytecode caches without wildcard-deleting arbitrary learner files.

## Preflight & Prerequisites

- **Host OS**: Linux (native, container, or WSL2) or POSIX-compliant host.
- **Python**: Python 3.10+ (tested on CPython 3.12.3).
- **Filesystem**: Standard local filesystem supporting `os.fsync` and directory descriptor sync.
- **Network (Optional)**: Internet access for optional HTTP header probe (if absent, tools truthfully report `NO LIVE NETWORK OBSERVATION`).

## Execution Commands

Run each tool individually:

```bash
cd labs/foundations/m09

# 1. Observe durability concept, fsync latency samples, and directory sync
python3 durability_observer.py

# 2. Observe Write-Ahead Logging ordering and crash recovery
python3 wal_model.py

# 3. Observe HDD mechanical latency and SSD WAF simulation
python3 media_model.py

# 4. Observe storage economics, cost modeling, and evaluation framework
python3 storage_economics.py
```

Run automated verification:

```bash
python3 test_activity.py
```

Clean up all temporary artifacts:

```bash
python3 reset.py
```

## Safety Guarantees

- **No Root / Sudo Required**: All tools run safely as an unprivileged user.
- **No Physical Hardware Stress**: Zero raw-device writes, no SSD endurance wear tests, no SMART mutations, no power-cut induction.
- **No Host Storage Exhaustion**: Payloads are strictly bounded (under 64 KiB), protected by programmatic safety caps.
- **No Cloud Credentials or Paid Resources**: All cloud economics calculations are parameterized in-memory models using local reference data.
- **No Mandatory External Network**: Network probes are strictly optional and capability-gated; never synthesizes fake network transcripts.
- **Deterministic Cleanup**: All test files reside in scoped directories and are removed immediately upon test completion.
