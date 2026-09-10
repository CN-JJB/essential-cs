# Stable Environment Pin Decision Packet v0.1

**Task:** Issue #143 — `[Research] Stable environment pin decision packet v0.1`
**Role:** Independent Stable Environment Pin Researcher / Decision-Prep Auditor (Local Executor, research-only)
**Canonical base:** `main @ 65309dd319e92ffbac9c27d3603b3eef1d532417`
**Research branch:** `research/issue-143-stable-environment-pin-decision-packet`
**Date (UTC):** 2026-09-10
**Status:** `READY FOR LEAD ENVIRONMENT REVIEW` (decision preparation only)
**OQ-BP-006:** remains OPEN. This packet does not close it, does not pin anything, and does not decide.

---

## 1. Authority / boundary statement

This is **research + decision preparation**, not environment implementation and not a governance decision.

- No Lesson / lab / test / preflight was modified; no `.github/workflows/` was created;
  no Docker/devcontainer/environment implementation was added.
- `meta/DECISIONS.md`, `meta/OPEN_QUESTIONS.md`, `meta/PROJECT_STATUS.md`, and
  `meta/RELEASE_AND_MAINTENANCE_POLICY.md` were read, never edited.
- The Executor does not select the canonical stable pin. The Web Lead owns the final pin disposition.
  The recommendation in §6 is input to that decision, not the decision.
- Issue #34 (real-learner validation) is a separate human gate and is out of scope here.
- Nothing in this packet claims v1.0, VERIFIED, or stable RELEASED.

## 2. Method and evidence tiers

### 2.1 Claim and base lock

- Issue #143 comments at start: **0 — no active claim**. Open PRs repo-wide: **none — no duplicate**.
  Recommended branch absent remotely — no competing work.
- Claim posted before research: `CLAIMED BY INDEPENDENT ENVIRONMENT RESEARCHER AI / Status: RESEARCH STARTED`.
- `git fetch origin` confirmed `origin/main == 65309dd319e92ffbac9c27d3603b3eef1d532417` (exact match);
  local `main` fast-forwarded (`008c040..65309dd`: merged audit PR #142 + Lead report-only Direct Fix + status commit);
  research branch created at that exact SHA. Starting worktree clean except pre-existing untracked
  `.commandcode/` (never committed, never evidence).

### 2.2 Three evidence tiers used below

- **ACTUAL RUN (this audit, exact base):** checks this researcher executed on a fresh LF materialization
  (`git archive HEAD` → `/tmp/env143`, tar SHA-256 `3104b587…`, 6215680 bytes) of `65309dd`, with exact
  versions recorded in §2.3. Nothing was committed; the materialization is ephemeral.
- **HISTORICAL PROVENANCE:** accepted #129/#133/#137 runtime at their locked bases, cited as provenance only,
  never relabeled as this audit's runtime and never treated as a pin.
- **NOT RUN / ENVIRONMENT-BLOCKED:** explicitly marked where this runtime could not execute
  (LAB-REQ-02 QEMU smoke) or where function does not exist yet (CI workflows).

### 2.3 Runtime identity for every ACTUAL RUN below

| Layer | Value |
|---|---|
| Host OS | Ubuntu 24.04.4 LTS, `6.18.33.2-microsoft-standard-WSL2`, x86_64, 24 cores |
| Python | CPython 3.12.3, embedded SQLite 3.45.1 |
| sqlite3 CLI | 3.45.1 (`/usr/bin/sqlite3`) |
| C toolchain | gcc 13.3.0, binutils 2.42, gdb 15.1, git 2.43.0, perl 5.38.2, bc 1.07.1, bash 5.2.21 |
| Network/TLS | curl 8.5.0, OpenSSL 3.0.13 |
| RISC-V lane | QEMU 8.2.2, riscv64-linux-gnu-gcc 13.3.0, riscv64-unknown-elf-gcc 13.2.0 |
| Absent | strace (MISSING), psql (absent), live browser (absent), Docker daemon (client present, daemon not probed) |
| Windows host (context only) | Python 3.13.1 / 3.11.9, MinGW gcc 14.2.0, no sqlite3 CLI, no QEMU, curl.exe 8.21.0 |

No historical verifier version is adopted as a pin anywhere below merely because a verifier once used it;
every recommendation cites a reproducibility or maintenance reason.

## 3. Candidate compatibility evidence

### 3.1 Shared preflights — ACTUAL RUN, all REQUIRED PASS

| Preflight | Result on fresh tree at `65309dd` |
|---|---|
| `tests/preflight_network_web.py` | REQUIRED PASS (loopback bind/connect, curl gate YES 8.5.0, openssl available; no live browser/CORS/DevTools — capability-gated as designed; `.invalid` resolver probe observes DNS failure truthfully) |
| `tests/preflight_data_concurrency.py` | REQUIRED PASS (embedded 3.45.1, sqlite3 CLI 3.45.1 REQUIRED PASS, writable FS + VFS locking PASS, gcc 13.3 `-std=c11 -pthread` PASS, C11 atomics PASS, mutex/cond PASS, watchdog PASS; psql unavailable = OPTIONAL SKIP; Docker PASS; TSan PASS; EXP-02 no live recheck) |
| `tests/preflight_distributed_infra.py` | READY M16–M20 (socket, loopback :0, sqlite 3.45.1, watchdog, M17 trace, M18 coordination, M19 Linux read-only, M20 observability all PASS; CS144/MIT sources link-only SKIP; OTel package absent → zero-SaaS core) |
| `tests/preflight_security_synthesis.py --module M21/M22` | REQUIRED PASS both (stdlib crypto, KDF, sqlite3, loopback bind, scratch, symlink; argon2/PyCA-crypto optional as designed) |
| `scripts/preflight-m05-m09.sh` | M06/M07/M08/M09 host PASS; LAB-REQ-02 RUNNABLE; strace MISSING (truthful); QEMU 8.2.2 + riscv pair present |

### 3.2 Full Python test surface — ACTUAL RUN: 24/26 suites PASS, 10/10 preflight discover PASS

Runner: `python3 -m unittest discover -s <dir> -p 'test_*.py'` per suite, CPython 3.12.3, 2026-09-10T04:14Z.

PASS (counts): m00-m01, m02 (9), m05 (9), m06 (7), m07 (4), m08 (12), m09 (16), m11 (4), m12 (6),
m13 (4), m14 (5), m15 (4), m16 (5), m17 (15), m18 (14), m19 (20), m21 (15), m22 (20), m23 (23), m24 (23),
lab_req_01 (6), lab_req_03 (8), lab_req_04 (6), lab_req_05 (7). Preflight discover 10/10 OK.

Two deviations, both recorded as environment/timing findings for CI design — not repaired here:

1. **m10 `test_dynamic_port_and_loopback_exchange` — 1 FAIL, known-environment signature.**
   `AssertionError: True is not false : {... 'connection_established': True ... 'UNEXPECTED_CONNECTION_ESTABLISHED'}`.
   Identical to accepted finding **V-129-02** (WSL2 localhost-relay teardown window; same suite passes 10/10 on
   non-relayed loopback). Classification carried forward: ENVIRONMENT, informational for CI (prefer non-relayed
   Linux runners; keep the probe, do not weaken it).
2. **m20 `TestThreeServicePipelineIntegration` — 2–3 FAILs, run-varying membership.**
   First run: 3 failures; re-run: 2 failures (`test_fault_injection_delay_and_relative_localization`: 502 != 200;
   `test_safe_mitigation_recovers_latency`: 504 != 200; `test_normal_end_to_end_request` failed in one run,
   passed in the next). The changing membership demonstrates **nondeterministic behavior in this WSL/shared-host run**, but it does not by itself distinguish runner load/threshold sensitivity from isolation problems or a real race/defect in the repository. Routed outcome: CI implementation must reproduce and triage this trio on the canonical environment before stable Gate 3/5 evidence is claimed. A temporary separately reported rollout lane is acceptable for diagnosis; silent waiver as stable-green evidence is not. No threshold or course code was changed here.

### 3.3 Representative C/shell flows — ACTUAL RUN

- M03 (`labs/foundations/m03`): `./preflight.sh` PASS (cc 13.3.0, objdump 2.42, gdb 15.1, git 2.43.0,
  python 3.12.3, bash 5.2.21); `./build.sh` PASS with canonical flags
  (`-std=c11 -Wall -Wextra -Wpedantic -g3 -O0 -fno-omit-frame-pointer -fno-inline -no-pie`);
  `./inspect.sh` shows `helper`/`main` symbols and bounded disassembly; `./reset.sh` clean.
- Shell syntax: `bash -n` PASS on all four LAB-REQ-02 entrypoints plus `scripts/preflight-m05-m09.sh`
  and M03 `preflight.sh` (6/6).

### 3.4 Required Lab smokes — mixed tier, stated per lab

| Lab | This audit | Historical provenance |
|---|---|---|
| LAB-REQ-01 | Suite 6/6 PASS (ACTUAL RUN); 4-step real-curl harness trace | PASS at #129 (real curl 8.5.0). Post-implementation CI must rerun harness. |
| LAB-REQ-02 | `./preflight.sh` PASS + `./setup.sh` PASS (ACTUAL RUN: clone of `https://github.com/mit-pdos/xv6-riscv.git`, checkout pin `35b088427ef37611c38afdeed5a52a278cae38f9`, LICENSE present, `verify_source_route.py` PASS incl. `SYS_pause == 13`, dispatcher, `sys_pause(void)`, stub `a7→ecall→ret`, `scause 8`, `uservec`) | QEMU smoke: NOT RUN here; 5× real-QEMU PASS provenance at identical toolchain (3× #133 + 2× #137, blobs `40d8156…`, modes `100755`). |
| LAB-REQ-03 | Suite 8/8 PASS (ACTUAL RUN, gcc 13.3 `-pthread`) | Runner 5/5 CP PASS at #129. |
| LAB-REQ-04 | Suite 6/6 PASS (ACTUAL RUN, CLI 3.45.1) | Harness PASS at #129 (SCAN→SEARCH, hash equivalence, symmetric timing, write/storage delta). |
| LAB-REQ-05 | Suite 7/7 PASS (ACTUAL RUN) | Runner 5/5 CP PASS at #129. |

Network note: this WSL egress reaches github.com (setup clone succeeded), unlike the historical WSL TLS-broken
environment — a reminder that CI must not assume a proxy; the packet's cache strategy (§4, §7) treats network
as required-only-for-fetch with pin verification, never for test correctness.

## 4. Required evidence packet — component contract matrix

Contract vocabulary (exactly one per row): `EXACT PIN` / `VERSION FLOOR` / `CAPABILITY-GATED` /
`OPTIONAL / NOT RELEASE-GATING` / `NOT REQUIRED`.

| Component | Recommended contract | Evidence and rationale |
|---|---|---|
| Canonical Linux base + image/digest strategy | `EXACT PIN` | Ubuntu 24.04 LTS (Noble) remains the recommended base family, but the **standard GitHub-hosted `ubuntu-24.04` runner is not the immutable pin**: GitHub updates hosted images regularly and `runs-on: ubuntu-24.04` selects the moving OS label, not a selectable runner-image digest/version. Lead freshness review on 2026-09-10 found hosted image `20260907.300.1` on Ubuntu 24.04.5, already newer than this research runtime's 24.04.4 / image-20260831 comparison. The canonical release environment should therefore be a digest-addressed Ubuntu-24.04-based learner/test image (or equivalently reproducible image artifact) whose build inputs are committed; a standard hosted runner may execute that image but is only the substrate. Never use `ubuntu-latest` as the canonical contract. |
| Python interpreter | `VERSION FLOOR` | Floor **3.12.x** (stdlib-only course; full surface green on 3.12.3 here and historically on 3.13.x, so no 3.13-only syntax is load-bearing). CI reference: system 3.12.3; record exact per run; allow patch updates freely. Rationale against EXACT PIN: patch churn buys nothing; against floating: learner 3.11-vs-3.12 `sqlite3`/error-text drift is real (this host's 3.11 embeds sqlite 3.45.1 vs 3.13's 3.45.3 — same engine line, but pin the floor, record the rest). |
| SQLite embedded engine | `VERSION FLOOR` | Floor **≥ 3.45**, record exact. Taught features (transactions, locking, EQP shapes, rollback journal) are stable across this line; EQP/timing assertions are already observation-gated, not version-literal. |
| `sqlite3` CLI | `VERSION FLOOR` | Floor **≥ 3.45**, REQUIRED learner gate per LAB-REQ-04 README (no Python-module substitution allowed). Provision via apt on Noble and runners (both ship 3.45.1); document the provisioning step because bare/Windows hosts lack it. |
| C compiler / toolchain | `VERSION FLOOR` | Floor **gcc ≥ 13 with `-std=c11`**; CI reference 13.3.0. M03 canonical flags build identically on 13.3 (Linux) and 14.2 (Windows) historically; disassembly text is observation evidence, never asserted literal across compilers. binutils/gdb versions recorded per run, not pinned. |
| GDB | `VERSION FLOOR` | **Required in the canonical stable environment**, not optional: M03 `preflight.sh` marks missing GDB BLOCKED, the learner README says canonical activity requires it, and `smoke-test.sh` is only PASS when both GDB and preflight PASS. Use a conservative Noble-compatible floor of **GDB >= 15.0** (this ACTUAL RUN used 15.1), record the exact package/version per run, and keep the three-point trace + debugger-failure evidence release-relevant. Convenience hosts without GDB may remain PARTIAL/BLOCKED, but the canonical v1.0 environment may not waive it. |
| strace | `CAPABILITY-GATED` | MISSING on Noble default and on historical runners; installable via apt; preflight already reports MISSING/RESTRICTED truthfully and M06/M08 degrade to observation fallbacks by design. CI installs it but keeps capability-gated verdicts (seccomp on hosted runners may restrict live tracing — verify in implementation). |
| QEMU + RISC-V cross-toolchain (LAB-REQ-02 lane) | `EXACT PIN` | Lane-scoped exactness is justified, with the current validated candidate **QEMU 8.2.2 + riscv64-unknown-elf-gcc 13.2.0** plus xv6 pin `35b0884` and accepted smoke blob `40d8156…`. Pin the **actual distro package identities / image digest**, not only the upstream binary-version strings: Ubuntu package revisions can change while `qemu-system-riscv64 --version` still reports 8.2.2. The implementation task must record the full package versions resolved into the canonical image and re-run the real QEMU smoke before accepting any refresh. Do not assume `apt install package=8.2.2` is a valid immutable lock. |
| Browser / web runtime | `OPTIONAL / NOT RELEASE-GATING` | No live browser needed: M12/CORS/DevTools evidence is truthfully capability-gated; EXP-03 Chromium recheck is opt-in. Never gate releases on a browser version. |
| Shell / core utilities (bash, coreutils, git, make, perl, bc, curl, openssl CLI, iproute2, procps, procfs) | `VERSION FLOOR` | Noble + runners converge (bash 5.2.21, git 2.43.0-class, make 4.3, perl 5.38.2, bc 1.07.1, curl 8.5.0, OpenSSL 3.0.13). curl is REQUIRED for LAB-REQ-01 (real-curl trace; note Schannel-vs-OpenSSL backend differences — canonical evidence is the Linux build). Floors, not pins: these move with the image digest. |
| PostgreSQL (server + psql CLI) | `OPTIONAL / NOT RELEASE-GATING` | LAB-OPT-03 strictly Optional; EXP-02 is a reachability/revision check (course ref `7344937cbe64`, 2026-09-04), not a live-server dependency. Runners ship MySQL/postgres-adjacent bits but the course must not depend on them. psql CLI: OPTIONAL / NOT RELEASE-GATING; server: NOT REQUIRED. |
| Containers (Docker/Podman) | `OPTIONAL / NOT RELEASE-GATING` | M19 container work is an optional comparison; native Linux path is canonical. Runner Docker availability is convenience, not a gate. |
| Observability backends (OTel collector, vendor SaaS) | `NOT REQUIRED` | M20 core is zero-SaaS and green without them (this run); OTel live route is Optional. CI must assert the zero-SaaS default. |
| Architecture | `EXACT PIN` (x86-64 canonical) + arm64 `OPTIONAL / NOT RELEASE-GATING` | All ISA/ABI/disassembly evidence is x86-64; runners and WSL here are x86_64. arm64 (ubuntu-24.04-arm) as forward-test only for the Python suite — never release-gating, since x86-specific observations cannot transfer. |
| Package provisioning | `VERSION FLOOR` (policy) | Noble archive via apt; version locks only inside the QEMU lane; **no pip** (stdlib-only course — PEP 668 externally-managed restrictions are therefore irrelevant); per-run `apt list --installed` snapshot recorded as provenance. |
| Refresh cadence + forward-test | policy (§4.1) | Digest re-pin quarterly or on security need; Python minor floor revisited as 3.12 approaches EOL (Oct 2028); `main` forward-tests newer toolchains without moving the pin; R11 latency constants stay CURRENT (6–12 mo per Living Curriculum Policy). |
| CI runner feasibility | feasible on standard hosted `ubuntu-24.04` **as execution substrate** (see §7) | Standard hosted runners are convenient and currently supply most non-QEMU prerequisites, but their image contents move over time and are not the canonical pin. Release-relevant commands should execute inside the canonical digest-addressed environment; every run should also capture the hosted runner image version. QEMU/RISC-V/strace may be baked into that canonical image rather than re-resolved from floating apt metadata on every job. No browser/GPU/self-hosted requirement is established by this packet. |
| Cache / artifact / network assumptions | fetch-pinned, cache-rest | xv6 fetched by exact SHA (shallow fetch of the pin suffices — full clone is waste); apt packages cached via `actions/cache`; no build artifacts committed (worktree is gitignored); tests must pass offline after fetch (no test may require live network except the explicitly-marked reachability probes, which SKIP offline). |
| License / provenance of image/toolchain choice | no new obligations | Noble archive packages are toolchain *use*, not vendoring — no ATTRIBUTION rows. xv6 stays runtime-fetched MIT with the existing LICENSE check. The runner/container image is infrastructure, not distributed content; record its digest as provenance, not as a license event. |

### 4.1 Pin lifecycle rule (for the Decision)

`EXACT PIN` items move only by re-pinning the image/lane definition + a green CI run at the new digest;
`VERSION FLOOR` items move by raising the floor with evidence that the full surface still passes;
`CAPABILITY-GATED` verdicts may only change disposition with a preflight + test-evidence pair, never by prose.
`main` may forward-test newer versions at any time without changing the canonical contract.

## 5. What the packet deliberately does not do

- Does not adopt any historical verifier's versions as pins (every row above carries its own reason; where a
  version coincides with a verifier env — e.g. QEMU 8.2.2 — the reason is timing-sensitivity + validation
  history, stated explicitly).
- Does not close OQ-BP-006, does not write a Decision, does not mark anything VERIFIED/RELEASED/v1.0.
- Does not fix the m10 relay probe or the m20 timing trio. M10 remains an environment-classified WSL finding that should run normally on canonical non-WSL CI; m20 is routed to temporary implementation-stage triage until its nondeterminism is explained (§7).

## 6. Required decision options

### Option A — Tightly pinned Noble image with version-locked lanes (maximum exactness)

Pin the full image digest **and** apt-version-lock every tool (Python patch, sqlite3 patch, gcc patch, QEMU,
binutils, curl). CI runs one immutable stack.

- Reproducibility benefit: highest — every byte of toolchain identical per digest.
- Maintenance cost: highest — digest churn + lock-file upkeep on every security update; stale locks break installs.
- Learner friction: lowest variance (“use digest D”), but heaviest image/pull burden.
- CI feasibility: trivial to define; brittle over time (locks rot between refreshes).
- Stale/brittle-pin risk: highest — a single yanked apt patch version red-blocks CI until someone edits locks.
- Effect on current labs: none functionally (all green on Noble), but locks add no extra passing power.
- Migration/refresh burden: full re-verification per digest bump, even for irrelevant patches.

### Option B — Pinned OS/Python floor with capability gates, exactness only where timing-sensitive (recommended)

Pin a **digest-addressed Ubuntu 24.04-based canonical learner/test environment**; use standard GitHub-hosted `ubuntu-24.04` only as the moving execution substrate. Set compatibility **floors** (Python ≥ 3.12, sqlite ≥ 3.45, gcc ≥ 13, curl ≥ 8.5, GDB ≥ 15.0); keep only genuinely optional/degradable surfaces capability-gated (for example strace/browser/OTel/psql); preserve **lane-scoped exactness for LAB-REQ-02** (validated QEMU 8.2.2 + riscv64-unknown-elf-gcc 13.2.0 + xv6 `35b0884`, represented by full package/image identities in implementation).

- Reproducibility benefit: high where it matters (OS baseline identical; timing-sensitive lane exact; everything else floor-bounded with per-run version capture).
- Maintenance cost: lowest compatible with stability — security patches flow inside floors; only digest + lane need scheduled attention.
- Learner friction: low — any Noble-class host with floors met works; preflights tell the truth otherwise.
- CI feasibility: compatible with standard hosted runners as the host substrate; reproducibility comes from the canonical digest-addressed environment, not from freezing the hosted runner image.
- Stale/brittle-pin risk: low — floors age gracefully toward the 2029/2028 horizons with a defined revisit.
- Effect on current labs: no redesign is indicated by the compatibility evidence. The ACTUAL RUN supports the proposed Noble/tool-floor choices, but it did **not** execute inside the not-yet-built digest-addressed canonical image, so it is evidence for the option rather than proof of the final artifact.
- Migration/refresh burden: digest re-pin quarterly + lane re-validation; floors rise only with evidence.

A considered-and-rejected third sketch, `ubuntu-latest` floating plus a `setup-python` version matrix, is
documented here so the Lead need not rediscover it: it maximizes variance on the release-gating path
(the label has already migrated 22→24 and will migrate to 26), contradicts the stable-environment policy,
and converts every upstream runner-image refresh into an unplanned curriculum event. Rejected.

### Recommendation

**Recommend Option B.** Reasons: (1) this packet's ACTUAL RUNs support the underlying Noble + tool-floor compatibility, while the digest-addressed canonical artifact still requires implementation and independent runtime proof; (2) it matches the repository's existing architecture — preflights are gates rather than universal patch pins; (3) it concentrates explicit component-level exactness where timing/history justify it while the canonical environment digest records the resolved stack; (4) it is compatible with standard hosted runners as substrate without pretending their image is frozen; (5) its maintenance curve fits a living curriculum (floors + cadence). **This recommendation is input, not a Decision — the pin is the Web Lead's to choose.**

## 7. Required CI execution-matrix proposal (design input — no workflows created here)

Jobs may use standard GitHub-hosted `ubuntu-24.04` as the host substrate, but **that runner label is not digest-pinnable**. Release-relevant commands execute in the canonical digest-addressed Ubuntu-24.04-based environment selected by the Web Lead. Capture both the hosted runner image version and the canonical environment digest, plus (`os/python/sqlite/cli/gcc/binutils/gdb/git/apt-list`) inside the canonical environment. Every job ends with its owned reset + a no-stray-process/artifact check.

| Job | Contents | Trigger | Gate rule |
|---|---|---|---|
| `python-matrix` | all 26 unittest suites + `tests/preflight*.py` discover | per-PR + nightly | Green required on canonical CI. M10 is not pre-quarantined; m20 may be temporarily separated only during rollout triage and cannot count as stable green until resolved or evidence-classified. |
| `preflights` | 4 Python preflights + `scripts/preflight-m05-m09.sh` | per-PR | All REQUIRED PASS; optionals informational |
| `shell-c` | `bash -n` over entrypoints; M03 preflight/build/inspect/reset; M04 run; `git diff --check` | per-PR | Green required |
| `lab-smokes` | REQ-01/03/04/05 harnesses + resets | per-PR (or nightly if slow) | Green required; CLI-provisioning step explicit |
| `qemu-lane` | run from the canonical image carrying the recorded full QEMU/RISC-V package identities → REQ-02 preflight/setup/source-route/smoke/reset, longer timeout; if packages are provisioned outside that image, lock their **full distro package versions/snapshot**, not bare upstream version strings | nightly + manual + pre-release (per-PR optional) | Green required on its schedule; network-fetch failures may be retried once as infrastructure failures, while smoke-semantic failures remain course findings |
| `version-capture` | folded into every job (snapshot artifact) | always | Informational, retained per run |
| capability-gated | browser/OTel/psql/argon2 probes | always | SKIP allowed, never FAIL; must not gate |

Temporary rollout-triage rule: do **not** pre-quarantine the M10 relay probe on the canonical Linux CI merely because it failed under WSL2; V-129-02 is a WSL relay signature and the canonical non-WSL runner should be expected to pass it. The m20 `TestThreeServicePipelineIntegration` timing trio may initially run in a separately reported triage step while the implementation task determines whether the nondeterminism comes from thresholds, runner load, isolation, or a real test/product race. Changing failure membership between identical runs demonstrates nondeterminism; it does **not** rule out a repository defect. Any temporary non-blocking treatment is implementation-stage only and cannot count as stable green evidence for Gate 3/5 or v1.0 until the failures are resolved or explicitly environment-classified with evidence. GDB is release-relevant in the canonical environment and its historical debt closes only when the canonical CI trace is green; strace remains capability-gated and must be verified, not assumed.

## 8. Completion criteria — direct answers

1. **What exactly should be pinned:** a digest-addressed Ubuntu-24.04-based canonical learner/test environment (distinct from the moving standard GitHub-hosted runner image) + the LAB-REQ-02 lane's resolved full QEMU/RISC-V package identities, xv6 `35b088427ef37611c38afdeed5a52a278cae38f9`, smoke blob expectations, and x86-64 as canonical arch. Everything else is governed by a floor or a genuine capability/optional classification.
2. **What should only have a floor:** Python 3.12.x, SQLite engine + CLI ≥ 3.45, gcc ≥ 13 (`-std=c11`),
   shell/core toolchain (curl ≥ 8.5 et al.).
3. **What should remain capability-gated/optional:** strace, browser/Chromium, OTel live route, psql/PostgreSQL, Docker/Podman, EXP source reachability, arm64 forward-test. **GDB is excluded from this list because it is required for canonical M03 evidence.**
4. **Which candidate best fits:** revised Option B on Noble — supported by this packet's ACTUAL RUNs. Hosted-runner contents are only a compatibility/substrate observation, not pin evidence; Lead freshness review already observed the hosted Ubuntu-24.04 image moving from the report's 20260831/24.04.4 snapshot to 20260907.300.1/24.04.5.
5. **What the next Executor must create:** the canonical digest-addressed environment definition/build inputs, provisioning manifest with full resolved package identities for the QEMU lane, the §7 workflow files, hosted-runner + canonical-environment version capture, temporary m20 triage routing, and a refresh-cadence note — acceptance: §9 evidence on the new stack.
6. **What independent runtime evidence is required after implementation:** full 26-suite matrix + preflights + shell/C gates + 5 lab smokes incl. real QEMU on the pinned stack, version snapshots, idempotent-cleanup proof, and exact-head Lead review. M10 must be green on canonical non-WSL CI; the m20 nondeterminism must be resolved or explicitly environment-classified with evidence before it can contribute stable-green proof.
7. **Residual uncertainty:** m20 trio root cause (runner load/thresholds vs isolation vs repository race/defect — needs triage, §3.2); strace live-tracing under hosted-runner/container restrictions (verify, don't assume); arm64 scope confirmation; full-package/image pin refresh mechanics for the QEMU lane; Docker-daemon reliance (none required — M19 stays optional).

## 9. Final recommendation

**`ENVIRONMENT PIN DECISION PACKET READY FOR WEB LEAD REVIEW`**

Rationale: the packet answers all seven completion questions from evidence — ACTUAL RUNs on a fresh materialization of the exact canonical base (preflights green, 24/26 suites green with two honestly-routed deviations, M03 flow green, REQ-02 fetch/pin/route green with smoke honestly NOT RUN and historically provenanced), hosted-runner feasibility research corrected by Lead freshness review, a classified per-component contract, two full options plus a rejected sketch with a reasoned recommendation, and a minimal CI matrix that can turn static policy into future operating evidence after the canonical artifact exists. No pin was made by the researcher, OQ-BP-006 stays open until Lead disposition is persisted, and no lifecycle state is claimed.

---

## 10. Explicit non-claims

No stable environment is pinned here. No Decision is made. OQ-BP-006 remains OPEN. No Lesson/lab/test/
preflight was changed. No workflow, image, or environment implementation was added. No v1.0, VERIFIED, or
stable RELEASED state is claimed or implied. No learner validation is claimed. Historical PASSes are
provenance, not this packet's runtime where marked NOT RUN.

## 11. Researcher execution trace (report-level)

- Base lock `65309dd`, branch `research/issue-143-stable-environment-pin-decision-packet`, start HEAD == base,
  worktree clean modulo pre-existing untracked `.commandcode/`.
- Reads: Issue #143 (full); Issue #140 + merged audit report incl. Lead Direct Fix `bfd0ad7`;
  RELEASE_AND_MAINTENANCE_POLICY; DEFINITION_OF_DONE; OPEN_QUESTIONS (OQ-BP-006); DECISIONS (D-008/D-024/D-027);
  PROJECT_STATUS at `65309dd`; verification reports #129/#133/#137 (environment matrices, blocker registers);
  all four Python preflights + shell preflight (full); LAB-REQ-02 README/SOURCE_PIN/setup; LAB-REQ-04 README gate;
  GH runner-image software lists (ubuntu-24.04 Full/Arm64/Slim, image 20260831) + Ubuntu release-cycle lifecycle.
- Runs (ephemeral `/tmp/env143` only, repo untouched): archive materialization; 5 preflight surfaces;
  26 unittest suites + preflight discover; M03 preflight/build/inspect/reset; REQ-02 preflight/setup/source-route;
  `bash -n` ×6. QEMU smoke: NOT RUN (heavyweight; historical 5× PASS cited). No committed file was executed
  in place on the Windows checkout (CRLF-safety); all Linux execution used the LF materialization.
- Problems: PowerShell/`wsl` quoting truncations (resolved via script files); `git diff --check` inside the
  archive tree correctly refused (not a repo — method note, not a finding); m10 1 known-env FAIL and m20 2–3
  run-varying FAILs (recorded + routed, not repaired); `gh pr list` empty at claim time because PR #142 had
  just been merged by the Lead (confirmed MERGED — no conflict).
- Ownership: this file is the researcher's sole authored change. All cited Executor/Verifier/Lead results keep
  their original attribution. Pre-existing local state (`.commandcode/`, ignored xv6 `worktree/`,
  `__pycache__`) is preserved and is not evidence.
