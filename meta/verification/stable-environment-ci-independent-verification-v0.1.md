# Stable Environment + CI Independent Verification v0.1

**Task:** Issue #147 — `[Verification] Canonical stable environment + CI independent verification v0.1`
**Role:** Independent Stable Environment / CI Verifier (verification-only)
**Exact base:** `main @ 4c2c87c20b8e43a606c5312708aaf42e47307b95`
**Verification branch:** `verification/issue-147-stable-environment-ci-independent`
**Date (UTC):** 2026-09-10
**Status:** `READY FOR LEAD STABLE ENVIRONMENT VERIFICATION REVIEW` (report only)

## 1. Independence / no-repair statement

This verification was performed in the Independent Verifier role: fresh base lock, fresh
materialization, independent image build, independent re-execution of every required surface,
no modification of the verified object, no test/preflight/workflow weakening. Two defects found
are recorded and routed; nothing was repaired.

**Disclosure:** the same AI harness previously executed Issues #140/#143/#145 in this session.
Functional independence for this task rests on: (a) a new canonical base (`4c2c87c`, which contains
6 Lead review commits this verifier did not author); (b) a fresh `git archive` materialization;
(c) an independent `docker build` (new image ID); (d) independent re-runs of the full campaign;
(e) a strict no-repair rule — including leaving the CI defect below broken for Lead routing.
Whether that satisfies the role-independence bar is for Web Lead disposition; all evidence is
reproducible from the recorded commands and SHAs either way.

## 2. Merge provenance (PR #146)

- PR #146 `[Implementation] Canonical stable environment + CI matrix v0.1 (#145)` — **MERGED**.
- Merge commit `4c2c87c` parents: `e53580f` (base) + `3f29784` (final reviewed head). Merge is well-formed.
- The branch carried 2 Executor commits plus **6 Lead Direct Fix commits** (`b85fcae` exact-head
  checkout/evidence retention, `926bd93` QEMU cleanup/retention hardening, `9c2b052` version-correct
  sort-V floors + arch fail-closed + lane tripwires, `48f9d49` candidate-vs-durable distinction,
  `de34c1d` CI-head/evidence-boundary corrections, `3f29784` whitespace).
- Base-to-merge delta is **exactly 7 added files, 794 insertions, 0 modifications**:
  `.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`,
  `.devcontainer/CANONICAL_ENVIRONMENT.md`, `.github/workflows/ci-fast.yml`,
  `.github/workflows/ci-qemu-lane.yml`,
  `meta/verification/stable-environment-ci-implementation-v0.1.md`,
  `scripts/canonical-env-capture.sh` (100755, blob intact).
  No `book/**`, learner-facing `labs/**`, `project/**`, Decisions/Open Questions/Status/policy,
  tag, release, or Issue #34 change. Forbidden-delta check: PASS.

## 3. Source / config audit at the exact base

| # | Check | Result |
|---|---|---|
| C1 | Dockerfile uses recorded immutable Ubuntu 24.04 base digest | PASS — `FROM ubuntu:24.04@sha256:224a1869…03082da254`, matching the documented manifest-list digest |
| C2 | No `ubuntu-latest` or hosted-runner-as-pin claim | PASS — `runs-on: ubuntu-24.04` only, with explicit moving-substrate comments; identity doc forbids both |
| C3 | D-032 floors correctly encoded (sort-V, arch fail-closed) | PASS — capture script v2: `version_ge` via `sort -V`, x86-64 fail-closed, all five floors + C11 surface probe |
| C4 | GDB required for canonical M03 evidence | PASS — capture `REQUIRED-present` floor ≥ 15.0; CI M03 step asserts `SMOKE result=PASS` + TRACE markers |
| C5 | QEMU/RISC-V exact distro identities (not bare upstream strings) | PASS — capture asserts `qemu-system-misc == 1:8.2.2+ds-0ubuntu1.18` and `gcc-riscv64-unknown-elf == 13.2.0-11ubuntu1+12` via `dpkg-query`, plus a broader dependency table |
| C6 | M10 not pre-quarantined | PASS — normal matrix step, no skip/quarantine language; "no quarantine" stated |
| C7 | m20 normal matrix release-relevant; triage explicitly non-evidence | PASS — matrix runs the trio normally; triage job is `continue-on-error` with diagnostic-only naming/summary |
| C8 | Exact-revision assertion in CI | PASS — PR head-SHA checkout + assert; dispatched-revision assert on scheduled/manual |
| C9 | Evidence upload configured, hidden logs retained | PASS — `include-hidden-files: true` on all three uploads (Lead fix; the pre-fix PR run uploaded 0 artifacts, the fixed runs upload correctly — independently confirmed, §7) |
| C10 | QEMU cleanup checks cannot self-match | PASS — bracket-trick `pgrep -f "[q]emu-system-riscv64"` in both workflows (Lead fix; the naive pattern self-matches, as this verifier independently reproduced) |
| C11 | `continue-on-error` scope | PASS — present only on the diagnostic triage job, never on release-relevant jobs |
| C12 | Forbidden learner-facing delta | PASS — §2 |

## 4. Independent environment identity observed

- Fresh `git archive 4c2c87c` materialization; independent `docker build` of the merged Dockerfile.
- Verifier-built image ID: `sha256:d75b65d2f81cc1224e8f2cada730c33e15f45188f6ae3886fc5ce94a2350e931`
  (amd64/linux) — a third distinct ID for the identical definition (see §8).
- In-image tool surface: Ubuntu 24.04.4, x86_64, CPython 3.12.3, SQLite engine + CLI 3.45.1,
  gcc 13.3.0, GDB 15.1, binutils 2.42, git 2.43.0, curl 8.5.0/OpenSSL 3.0.13, QEMU 8.2.2,
  riscv64-unknown-elf-gcc 13.2.0, riscv64-linux-gnu-gcc 13.3.0, strace 6.8.
- `scripts/canonical-env-capture.sh` (v2): **result=PASS** — arch, all floors, C11 surface,
  both lane exact-package tripwires.

## 5. Independent ACTUAL RUN table (fresh image, exact base)

| # | Surface | Verdict |
|---|---|---|
| R1 | 5 preflight surfaces | PASS (all REQUIRED; strace live PASS; REQ-02 RUNNABLE) |
| R2 | Full Python matrix, 26 suites + preflight discover | **27/27 PASS** |
| R3 | M10 normal required path | **PASS 10/10** (no quarantine, no relay failure where no relay exists) |
| R4 | m20 full suite + trio ×5 repeats | **36/36 + 5/5 PASS** (see §6) |
| R5 | M03 preflight/build/inspect/GDB three-point/failure/reset | PASS — `SMOKE result=PASS`, `gdb=PASS`, 9 TRACE lines with before-call/callee/after-return + `local=30`, SIGSEGV check, reset clean |
| R6 | REQ-01/03/04/05 harnesses + resets | PASS with clean resets |
| R7 | REQ-02 real QEMU lane (setup/pin/route/fixture/**smoke**/reset) | **Smoke PASS** — usage output, `sleep 10` return, standalone marker + prompt, reaped, PID clean; pin `35b0884…`, origin + LICENSE + route verified |
| R8 | Cleanup truth | Pin restored, worktree status empty, PID marker absent, bracket-trick pgrep empty |
| R9 | `git diff --check` / object-unchanged | PASS — verification branch clean; only this report will be added |

Provenance (not verifier runtime): #129/#133/#137 historical PASSes; Executor #145 local runs.
NOT RUN by this verifier: `grade-lab-util` (absent at pin, README-declared), live browser/OTel/psql/argon2
(optional by design), arm64 (non-gating), strace live-tracing beyond the probe.

## 6. M10 result + repeated m20 outcomes and bounded classification

- **M10:** 10/10 here and 10/10 on hosted CI (0.648 s). V-129-02 remains the correct classification of the
  *WSL-relay* observation only. No quarantine exists or is needed.
- **m20 trio:** 6/6 green on canonical Linux in this campaign (1 matrix + 5 repeats) plus 5/5 green in the
  hosted triage lane — 11 consecutive canonical greens across two substrates — versus 2–3 run-varying
  502/504 FAILs on loaded WSL2-relay. The failures correlate with the relay/shared-load environment on an
  identical tree; the container shares the WSL2 kernel but uses a real loopback namespace while unloaded.
- **Classification (bounded):** environment/load-correlated; **no repository defect demonstrated, and none
  claimed absent** — 11 greens bound the claim but cannot eliminate a latent load-sensitive race. The trio
  stays in the normal required matrix; the CI triage lane keeps accumulating statistics; any future
  canonical-CI failure is a first-class finding that must open a bounded Issue. No code, test, threshold,
  or preflight was touched.

## 7. Merged-main GitHub Actions audit (exact revision truth)

- Post-merge `canonical-fast` on main: run **34452047451**, headSha **`4c2c87c…`** (exact base),
  conclusion **success**. Substrate recorded in-run (`runner_image_version=20260831.293.1`, informational).
  CI-built image `sha256:495067c9…` (ephemeral build record, not a published pin).
- Matrix log: **26/26 SUITE_PASS** incl. m10 10/10 and m20 36/36; preflight discover 10/10;
  M03 `SMOKE result=PASS` + `gdb=PASS`; harnesses + hygiene done.
- Artifact metadata (not assumed from green): `canonical-fast-evidence`, id 10141970339,
  9233 bytes, digest `sha256:05796c84…`, expires 2026-12-09, head_sha `4c2c87c…` — downloaded and
  inspected: 8 files (snapshot v2 all-PASS incl. lane tripwires, full matrix log, M03 smoke log,
  preflight + harness logs). The pre-fix PR run (34439909872) uploaded **0 artifacts**, which
  independently confirms the Lead `include-hidden-files` correction was necessary and effective.
- Verifier-dispatched `canonical-qemu-lane` on main @ exact base (workflow_dispatch, permitted):
  run **34469175287**, conclusion **success** (both jobs). Triage artifact inspected: trio **5/5 PASS**
  with genuine unittest logs. **But the `qemu-smoke` job is vacuous (see §9 V-147-01):**
  its smoke step never executed, yet the job reported success. Actions QEMU-smoke evidence is therefore
  **NOT ESTABLISHED**; §5 R7 (independent local smoke in the identical image definition) is the only
  real-QEMU evidence at this base.

## 8. Durable-pin audit — separate from functional verification

- A pinned Ubuntu `FROM` digest is an immutable **base input**, not a durable built-environment pin:
  apt-floor packages resolve at build time, so identical-definition builds differ. Observed image IDs:
  implementer-local `9b862c…`, first Actions build `495067c9…`, this verifier's fresh build `d75b65d…` —
  three different IDs, directly proving non-byte-identicality.
- No built canonical container/artifact is published or otherwise retrievable by immutable digest:
  no push/login/publish step exists in either workflow, no registry/package artifact was found, and the
  identity document itself states none exists. Workflow logs recording image IDs are evidence about
  ephemeral builds, not retrievable pins. No equivalent immutable package snapshot/lock strategy exists
  beyond the two lane tripwires (which fail loudly on drift by design, but do not freeze the rest).
- **Audit result: the candidate is a validated floor-recipe plus ephemeral build records. The durable /
  retrievable built-environment identity required for OQ-BP-006 closure is still missing.** Per the Task
  Contract this is stated explicitly, not papered over: base digest ≠ final pin.

## 9. Findings (classified; routed, not repaired)

- **V-147-01 — CI QEMU-lane false-green (heredoc terminator). SIMPLE FIX / BLOCKING.**
  `.github/workflows/ci-qemu-lane.yml` lines 78/91: the `SLEEPEOF` (and `PYEOF`) terminators are indented
  inside the YAML block while the inner shell is `bash -c '...'` with `<<` (not `<<-`), so bash never finds
  them, swallows the remainder (including `./smoke.sh`) as heredoc text, and `cat` exits 0 with only a
  warning (`qemu-lane-outer.log` line 33: `here-document ... delimited by end-of-file (wanted 'SLEEPEOF')`).
  The `req02-smoke.log` artifact is absent; the job still reports success. The required CI smoke surface
  therefore never executes. Fix (bounded follow-up Issue, not here): write the fixture without an indented
  heredoc (e.g. python file-write or `printf`), and add a guard asserting the smoke PASS marker exists in
  `req02-smoke.log` so recurrence fails loudly. Re-verification can be narrow: one green lane run with the
  smoke artifact present. The underlying QEMU semantics are independently green (§5 R7), so no course-content
  repair is indicated.
- **V-147-02 — Durable built-identity still missing. COMPLEX REWORK (bounded follow-up) / BLOCKING pin closure.**
  Establish a durable/retrievable final built-environment digest (publish the built image from a trusted
  build, or an equivalently immutable package snapshot strategy) plus one independent matrix run against
  that realized identity. Route as a bounded follow-up implementation task; OQ-BP-006 closes only after it
  plus accepted runtime evidence.
- No other findings. No ARCHITECTURE finding (no curriculum/policy change indicated).
  No ENVIRONMENT finding beyond the already-classified WSL relay note (V-129-02, unchanged).

## 10. Residual risk / NOT RUN table

- CI QEMU smoke on committed automation: NOT ESTABLISHED (V-147-01) — verifier local smoke (§5 R7) is actual
  evidence for the semantics, not for the lane.
- Durable pin: NOT ESTABLISHED (V-147-02).
- `grade-lab-util`, live browser/OTel/psql/argon2, arm64, strace-beyond-probe: NOT RUN (by design/scope).
- Latent m20 race: not provable absent (bounded claim only, §6); covered by the retained triage lane and the
  first-failure-opens-Issue rule.
- Lead final-head executable re-run: NOT RUN by this session (Lead authority; recorded, not assumed).

## 11. OQ-BP-006 disposition recommendation (no self-closure)

**Do not close OQ-BP-006.** Recommended path: (1) bounded repair Issue for V-147-01 with a green,
artifact-complete lane run; (2) bounded follow-up for V-147-02 establishing the durable/retrievable
built identity; (3) narrow independent re-verification of exactly those two items against the realized
identity; (4) Web Lead pin closure only then. Two separate bounded issues are recommended so the trivial
CI-script fix is not held behind the artifact-strategy work.

## 12. Explicit non-claims

No v1.0, VERIFIED, or stable RELEASED claim. No lifecycle change. OQ-BP-006 stays OPEN.
Issue #34 untouched; no learner validation claimed; no AI output presented as learner evidence.
No Lesson/lab/test/preflight/workflow/script/course file was modified, weakened, or repaired.
Historical PASSes are provenance wherever not re-executed here.

## 13. Final recommendation

**`NOT VERIFIED — BLOCKERS REQUIRE REPAIR`**

Rationale: the environment image and every course surface are independently green at the exact base
(27/27 matrix, GDB-required M03, four harnesses, real QEMU smoke with cleanup truth, honest M10/m20
truth, green hosted fast run with inspected artifacts), and the source/config audit passes 12/12 —
but a required CI surface reports success without executing (V-147-01, false-green is the most corrosive
failure mode for a gate), and the durable built identity for pin closure does not exist (V-147-02).
Both blockers are bounded and routed; neither implicates course content. The honest verdict is therefore
not-verified with repair required, not a waiver.
