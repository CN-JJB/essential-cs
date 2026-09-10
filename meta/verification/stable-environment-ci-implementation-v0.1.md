# Stable Environment + CI Matrix Implementation Evidence v0.1

**Task:** Issue #145 — `[Implementation] Canonical stable environment + CI matrix v0.1`
**Role:** Stable Environment / CI Executor (bounded implementation + runtime evidence only)
**Canonical base:** `main @ e53580fcce2c32d0785cf43f0d42e98ca8a78ea5`
**Implementation branch:** `implementation/issue-145-stable-environment-ci-v0.1`
**Governance:** D-032. **OQ-BP-006 remains OPEN** — this implementation does not close it;
closure belongs to Web Lead acceptance. No v1.0 / VERIFIED / stable RELEASED claim is made.

---

## 1. What was implemented (allowed scope only)

| File | Purpose |
|---|---|
| `.devcontainer/Dockerfile` | Digest-pinned Ubuntu 24.04 base + required tools + lane-locked QEMU/RISC-V |
| `.devcontainer/devcontainer.json` | Minimal learner container entry (build + workspace mount) |
| `.devcontainer/CANONICAL_ENVIRONMENT.md` | Identity record: base digest, build inputs, resolved packages, refresh runbook |
| `scripts/canonical-env-capture.sh` (100755) | Floor gate + version snapshot (D-032 floors, fail-closed exit 3) |
| `.github/workflows/ci-fast.yml` | Per-PR/push fast matrix in the canonical container (no quarantine) |
| `.github/workflows/ci-qemu-lane.yml` | Nightly/manual QEMU lane (required) + m20 triage (diagnostic, non-blocking) |

Nothing else was touched: no `book/**`, no learner-facing `labs/**`, no `project/**`,
no Decisions/Open Questions/Status/policy, no tags/releases, no Issue #34 evidence.

## 2. Canonical image / artifact identity

- **Base reference + immutable digest:**
  `ubuntu:24.04@sha256:224a1869083a311ef3f13648a154ba79832fbef6364d31493642ca03082da254`
  (manifest-list digest, retrieved 2026-09-10 via Registry API; independently confirmed the same day:
  `docker pull ubuntu:24.04` resolved to the identical digest).
- **Canonical build inputs:** `.devcontainer/Dockerfile` at the implementation head (Layer 1 floors,
  Layer 2 lane locks `qemu-system-misc=1:8.2.2+ds-0ubuntu1.18` and
  `gcc-riscv64-unknown-elf=13.2.0-11ubuntu1+12` as intentional tripwires).
- **Locally built candidate identity (2026-09-10, implementer runtime):**
  image ID `sha256:9b862cb417234bb72e7c1869eb8d33e3cd8c98eda6c9628eb811ba13af907d32`
  (local tag `essential-cs-canonical:v0.1-issue145`, amd64/linux, 1.53 GB).
  This tag is **not published** and therefore not durable — it is reproducible evidence, not the pin.
  The durable pin is the §2 base digest plus the committed definition.
- **Reconstruction:** `docker build -f .devcontainer/Dockerfile -t <name>:<tag> .`
  (re-query the registry first; any base-digest drift forces conscious re-pinning per the refresh runbook).
- **Publication:** no container/package artifact was published (only repository-free infrastructure is
  permitted and none was needed at this candidate stage). The first CI build on hosted infrastructure
  produces the first independently retrievable build record (see §8).
- **Hosted runner image (substrate, NOT the pin):** recorded per run from the runner itself;
  observed moving (Lead review: 20260831/24.04.4 → 20260907.300.1/24.04.5), which is exactly why the
  substrate is never cited as identity.

## 3. Full tool / version / package identity (inside the built image)

Observed surface: Ubuntu 24.04.4 LTS, x86_64, CPython 3.12.3, embedded SQLite 3.45.1,
`sqlite3` CLI 3.45.1, gcc 13.3.0, GDB 15.1, binutils 2.42, git 2.43.0, curl 8.5.0 / OpenSSL 3.0.13,
perl 5.38.2, bc 1.07.1, bash 5.2.21, QEMU 8.2.2, riscv64-unknown-elf-gcc 13.2.0,
riscv64-linux-gnu-gcc 13.3.0, strace 6.8 present. All D-032 floors met
(`scripts/canonical-env-capture.sh` → `CANONICAL_ENV_CAPTURE result=PASS`).

Resolved distro identities (`dpkg -l`, `ii` rows): bash 5.2.21-2ubuntu4, bc 1.07.1-3ubuntu4,
binutils 2.42-4ubuntu2.10, build-essential 12.10ubuntu1, ca-certificates 20260601~24.04.1,
curl 8.5.0-2ubuntu10.13, gcc-riscv64-linux-gnu 4:13.2.0-7ubuntu1,
gcc-riscv64-unknown-elf 13.2.0-11ubuntu1+12, gdb 15.1-1ubuntu1~24.04.1,
git 1:2.43.0-1ubuntu7.3, make 4.3-4.1build2, perl 5.38.2-3.2ubuntu0.4,
python3 3.12.3-0ubuntu2.1, qemu-system-misc 1:8.2.2+ds-0ubuntu1.18,
sqlite3 3.45.1-1ubuntu2.7, strace 6.8-0ubuntu2.

## 4. Workflows / jobs / triggers added

**`ci-fast.yml`** (`canonical-fast`; pull_request + push(main) + manual; job timeout 45 min):
substrate-identity capture → build canonical image (digest/ID recorded) → LF archive tree →
floor gate + snapshot → 5 preflight surfaces → shell-syntax gates → full 26-suite matrix
(M10 normal, m20 normal, **no quarantine**) → M03 full smoke incl. GDB (REQUIRED) →
REQ-01/03/04/05 harnesses + resets → hygiene (`git diff --check`, no stray QEMU, no PID markers) →
evidence-bundle upload. Every release-relevant command runs inside the canonical container;
course execution uses the archive copy so the checkout stays pristine.

**`ci-qemu-lane.yml`** (`canonical-qemu-lane`; nightly 02:00 UTC + manual):
`qemu-smoke` (REQUIRED on its schedule: build → floors → REQ-02 preflight/setup/source-route/
automated-learner-fixture/smoke/reset → cleanup truth: pin restored, worktree clean, no PID marker,
no stray QEMU; 60 min timeout) and `m20-timing-triage` (TEMPORARY diagnostic, `continue-on-error`,
trio ×5 with per-run table + step summary; explicitly **never stable-green evidence**; removable only
by a bounded follow-up Issue after resolution or evidence-classification).

## 5. Exact checks actually run + outcomes (implementer runtime, container, head `757aa2d`)

Method: fresh LF materialization (`git archive 757aa2d…`) executed inside the §2 built image.
The report file itself is the only delta between the tested tree and the final head; it affects no
executable surface.

| # | Check | Outcome |
|---|---|---|
| 1 | Floor gate + snapshot | PASS — all D-032 floors met, full identities captured |
| 2 | 5 preflight surfaces | PASS (network/data/distributed/M21/M22 REQUIRED; shell M06–M09 PASS, REQ-02 RUNNABLE; **strace live PASS** in container) |
| 3 | Shell syntax (entrypoints + preflights + M03 scripts) | 6/6 PASS (`bash -n`; YAML of both workflows parsed OK) |
| 4 | Full Python matrix, 26 suites + preflight discover | **27/27 PASS**, incl. **m10 10/10** and **m20 36/36** (see §6) |
| 5 | M03 canonical evidence | PASS — preflight, build, baseline 37, symbols, disassembly, failure rc=139, **GDB three-point trace** (9 TRACE lines; before-call/callee/after-return + `local=30`), failure SIGSEGV check, reset clean. Note: GDB prints `warning: Error disabling address space randomization: Operation not permitted` (container restriction) — non-fatal; all markers captured |
| 6 | REQ-01/03/04/05 harnesses + resets | PASS with clean resets (endpoints reaped, 4 C artifacts removed, DB files removed) |
| 7 | REQ-02 real QEMU lane | **Smoke PASS** — `Usage: sleep ticks` observed as output, `sleep 10` returned to prompt, standalone `LAB_REQ_02_OK` + prompt, `QEMU_REAPED: TRUE`, `PID_MARKER_CLEAN: YES`; pin `35b0884…`, origin + LICENSE verified, route (`SYS_pause == 13` … `uservec`) verified |
| 8 | Cleanup truth | Pin restored, worktree `status --porcelain` empty, PID marker absent, no stray QEMU (bracket-trick `pgrep -f "[q]emu-system-riscv64"` empty; an earlier naive pattern self-matched the wrapping shell — check-method artifact, documented, not a stray) |
| 9 | m20 trio repeats (classification) | **5/5 PASS** (see §6) |
| 10 | `git diff --check` + scope | PASS; branch diff contains only the 7 allowed files |

## 6. M10 outcome + repeated m20 outcomes + classification

- **M10 `test_dynamic_port_and_loopback_exchange`: PASS 10/10 on canonical non-WSL Linux.**
  The historical WSL2-relay failure signature (V-129-02, `UNEXPECTED_CONNECTION_ESTABLISHED`) did not
  reproduce where no relay exists. Per the Task Contract it was **not pre-quarantined** — it ran in the
  normal matrix and passed. V-129-02 remains the correct classification of the *WSL* observation only.
- **m20 `TestThreeServicePipelineIntegration`: 6/6 green on canonical Linux** (1× full-matrix 36/36 run
  + 5× dedicated trio repeats, all PASS), versus 2–3 run-varying FAILs (502/504 on delay/latency-budget
  paths) on loaded WSL2 with relay networking.
- **Classification (bounded — no course code was touched):** failure correlates with the WSL
  relay/shared-load environment on an identical tree; the container shares the WSL2 kernel but uses a
  real loopback namespace and was unloaded, isolating network-namespace + load as the differentiating
  factors. This does **not** prove the absence of a latent load-sensitive race — 6 greens bound the claim
  but cannot eliminate it. Disposition: the trio stays in the **normal required matrix** (no quarantine);
  the temporary CI triage lane accumulates scheduled-run statistics; **any future canonical-CI failure of
  this trio is a first-class finding** (possible real race) and must open a bounded repair/triage Issue —
  it may never be waived as "known flaky". No repair is smuggled here; none was needed for green.

## 7. Five Required Lab outcomes (explicit)

- REQ-01: harness PASS + reset clean (real-curl trace surface green in §5 runs).
- REQ-02: **real QEMU smoke PASS** (§5.7) + cleanup truth (§5.8). Grader `grade-lab-util` NOT RUN
  (absent at pin; README-declared).
- REQ-03: suite 8/8 + runner harness PASS + reset clean.
- REQ-04: suite 6/6 + harness PASS (CLI 3.45.1) + reset clean.
- REQ-05: suite 7/7 + runner PASS + reset clean.
- Nothing was modified in `labs/**` to obtain green; the m03/REQ-02 fixtures used are the documented
  learner inputs, created ephemerally and removed by resets.

## 8. GitHub Actions runs on this PR

- Workflows are committed here for the first time, so no historical runs exist.
- After PR creation the `canonical-fast` workflow triggers on the PR event; observed runs are recorded
  in the PR body Completion Report (run IDs/URLs + job outcomes), which is editable without changing the
  reviewed head. **No Actions run means no Actions run** — the local container evidence in §5 stands on its
  own either way, and nothing below is claimed from CI until a run exists.

## 9. Unresolved / not-run work

- Live GitHub Actions outcomes (pending PR creation; see §8).
- Published-image durability: no artifact published (permitted; not needed at candidate stage). The first
  CI build produces the first independently retrievable build record.
- `grade-lab-util` NOT RUN (out of scope at pin). Live browser/OTel/psql/argon2 NOT RUN (optional by design).
- strace *live-tracing* beyond the preflight probe was not exercised (capability-gated; preflight proves presence).
- arm64 forward-test was not run (optional, non-gating).

## 10. Problems encountered + bounded diagnosis

1. `docker pull`/build initially failed (`connection reset by peer` to registry-1.docker.io): the dockerd
   process lacked the host proxy env (`127.0.0.1:10808`), while user-shell curl worked. Diagnosis: environment
   proxying, not a definition defect. Fix (host-only): restarted dockerd with proxy env; pull then resolved
   to the exact §2 digest, confirming the pin independently. No repo impact.
2. No `dockerd` binary initially (`docker.service` absent): installed `docker.io` via apt (host tooling only).
3. B4 stray-QEMU check appeared to fail: `pgrep -f qemu-system-riscv64` self-matched the wrapping `bash -c`
   command line. Diagnosis: check-method artifact. Fix: bracket-trick pattern; re-check empty. No stray existed.
4. A draft triage command had mangled quoting (`tr \n |;`): rewritten cleanly; rerun green. Helper-only.
5. GDB ASLR-disable warning in container: recorded as non-fatal restriction (§5.5), not a defect.

## 11. Ownership boundary

Executor-authored: the 7 files in §1 + this report + the PR body. All course content, pins, smoke semantics,
and historical Executor/Verifier/Lead results keep their original attribution. Pre-existing local state
(`.commandcode/`, ignored xv6 `worktree/`, `__pycache__`, prior branches, host docker setup) is preserved,
unclaimed, and — except the built local image ID cited as evidence — not part of the delivery.

## 12. Explicit statements

- OQ-BP-006 remains OPEN for Web Lead closure; this PR supplies the realization evidence, not the Decision.
- This PR does not claim v1.0, VERIFIED, or stable RELEASED; it does not modify lifecycle state.
- Issue #34 is untouched. No learner validation is claimed. No AI output is presented as learner evidence.
- M10 was not quarantined; m20 was not waived; no test, preflight, lab, or threshold was weakened.

## 13. Final recommendation

**`STABLE ENVIRONMENT CANDIDATE READY FOR INDEPENDENT VERIFICATION`**

Rationale: the digest-pinned definition builds reproducibly; the built image meets every D-032 floor with
recorded full package identities; the complete matrix (27/27), GDB-required M03 evidence, four lab harnesses,
a real QEMU smoke with cleanup truth, and 6/6 m20 trio greens were all observed inside that image at the
implementation head without touching course content; M10/m20 truth was established without quarantine or
waiver; CI workflows encode the same gates for independent re-execution. Verification — including a live
Actions run and Lead exact-head review — is still required before anyone closes OQ-BP-006.
