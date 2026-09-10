# Post-v0.9 v1.0 Gap & Stabilization Plan v0.1

**Task:** Issue #140 — `[Audit] Post-v0.9 v1.0 gap & stabilization plan v0.1`
**Role:** Independent Post-v0.9 v1.0 Gap Auditor (Local Executor, audit-only)
**Canonical base:** `main @ 008c0407420bf44a9ea8f96645c366224f0fc333`
**Audit branch:** `audit/issue-140-post-v09-v10-gap-plan`
**Date (UTC):** 2026-09-10
**Status:** `READY FOR LEAD AUDIT REVIEW` (audit report only; not VERIFIED / RELEASED / v1.0)

---

## 1. Independence / non-repair statement

This audit was performed in the **Independent Post-v0.9 v1.0 Gap Auditor** role under Issue #140.
The auditor is not the author, repair Executor, or verifier of the material under audit,
and is not the Web Lead.

No file of the audited object was modified during this audit:

- no Lesson / lab / test / fixture / preflight / evidence-template change;
- no Research / Design / Registry / Matrix / Map / Decision / Open Question / PROJECT_STATUS change;
- no prior verification-report change;
- no tag / release / lifecycle-state change;
- Issue #34 was not closed, touched, or re-scoped.

Gaps found are classified and routed in this report. Nothing was silently repaired.
The only committed change allowed by the Task Contract is this file:

`meta/audits/post-v09-v10-gap-stabilization-plan-v0.1.md`

---

## 2. Audit method

### 2.1 Claim check (before work)

1. Issue #140 comments at audit start: **0 comments — no active claim**.
2. Open PRs in `CN-JJB/essential-cs` at audit start: **none** — no duplicate work.
3. Remote branch `audit/issue-140-post-v09-v10-gap-plan`: **absent** — no competing agent work.
4. Claim posted before audit work: `CLAIMED BY INDEPENDENT AUDITOR AI / Role: Post-v0.9 v1.0 Gap Auditor / Status: AUDIT STARTED`.

### 2.2 Base lock

- `git fetch origin` advanced `origin/main` `aee2677..008c040`.
- Local `main` fast-forwarded to `008c0407420bf44a9ea8f96645c366224f0fc333` (exact match with the Issue #140 canonical base).
- Branch `audit/issue-140-post-v09-v10-gap-plan` created at that exact SHA.
- Starting worktree: clean except pre-existing untracked `.commandcode/` (agent-session scratch, never committed)
  and pre-existing ignored `labs/lab-req-02-xv6-syscall/worktree/` (gitignored xv6 clone) plus ignored `__pycache__`
  artifacts. None is authored by this audit; none is used as audit evidence.

### 2.3 Evidence-type discipline

Every finding below distinguishes:

- **source/static evidence** — committed prose, maps, code, tree modes, blob identities, hashes, Issue/PR state;
- **executable evidence** — an actual test / smoke / QEMU / preflight run against an exact SHA;
- **operating evidence** — a workflow running over time (CI schedule, review cadence, errata handling, maintenance queue).

Document existence never counts as operating evidence. Mapping prose never counts as implementation.
AI evaluation never counts as learner evidence. Executor runtime is never relabeled as Lead runtime
or as this auditor's runtime.

### 2.4 Required evidence sources inspected

- `v0.9` annotated tag `f8e702ed5deda9d750414574feb95dbe3cf3eb97` → target `aee26770b177a6fbbd2039c90f4e0d110ebfb301`;
  GitHub Release `Essential CS v0.9 — Release Candidate` (`prerelease=true`, full non-claims + bounded findings V-129-02–V-129-05).
- Issues #129 (CLOSED), #131 (CLOSED), #133 (CLOSED), #135 (CLOSED), #137 (CLOSED), #139 (release operation)
  and their merged artifacts PRs #130 / #132 / #134 / #136 / #138.
- All three verification reports at their locked bases:
  `meta/verification/full-core-integration-v09-rc-readiness-v0.1.md` (base `d6641e8`),
  `meta/verification/v09-rc-readiness-reverification-v0.1.md` (base `e6b8a2f`),
  `meta/verification/lab-req-02-direct-invocation-recheck-v0.1.md` (base `8e86715`).
- Issue #34 (OPEN, 0 pilot sessions) and Issue #141 (Web Lead continuation handoff, canonical base `008c040`).
- `meta/RELEASE_AND_MAINTENANCE_POLICY.md` (v1.0 gate, stable environment, errata, learner validation).
- `meta/DEFINITION_OF_DONE.md` (Core item, Lab, VERIFIED, v1.0 = teachable).
- `meta/PROJECT_STATUS.md` at `008c040` (v0.9 PUBLISHED / POST-v0.9 STABILIZATION ACTIVE; full #129→#137 chain record).
- `meta/OPEN_QUESTIONS.md` (OQ-BP-001 / OQ-BP-003 / OQ-BP-006 OPEN; OQ-BP-007 + OQ-BP-002/004/005 CLOSED).
- `meta/DECISIONS.md` (D-024 v1.0 gate; D-027 build-first with deferred-but-mandatory validation).
- `meta/CURRICULUM_INVARIANTS.md` §20 (v1.0 = teachable: runnable labs, multi-role verification, learner validation, external audit, operating maintenance).
- Mini Cloud sources: `meta/blueprint/mini-cloud-app-evolution-v0.1.md` (P0–P9),
  `meta/blueprint/mini-cloud-curriculum-alignment-v0.1.md`, `meta/CURRICULUM_MAP.md`,
  `meta/blueprint/final-reconciliation-v0.1.md` §6; tree check `Test-Path project/` = **False**.
- External coverage sources: `meta/audits/external-curriculum-audit-v0.1.md` (Issue #2, snapshot `7d67fd3`, pre-Issue-#1 macro audit,
  all fine-grained findings `RECHECK-AFTER-ISSUE-1`); `meta/blueprint/audit-to-architecture-disposition-v0.1.md`;
  `meta/blueprint/final-exit-audit-v0.1.md` (30/30 Blueprint exit, not a v1.0 external audit).
- Maintenance/review sources: `meta/LIVING_CURRICULUM_POLICY.md`, `meta/REVIEW_POLICY.md`,
  `.github/` (templates only, no `workflows/`), `LICENSES/`, `ATTRIBUTION.md`, open-Issue list.
- Read-only tree inspections at `008c040`: 76 `book/**/*.md` files (70 learner Lessons + 6 companions),
  24 `labs/foundations/` directories (representing M00–M24), 5 Required Lab trees, 33 neutral evidence templates
  under `course/evidence/`, 4/4 LAB-REQ-02 entrypoints at Git mode `100755` with accepted content blobs,
  `LICENSES/Apache-2.0.txt` + `LICENSES/CC-BY-SA-4.0.txt` present.

### 2.5 Verification actually run by this auditor

- **Source/static inspections only** (read-only; no Lesson/lab/test modification):
  file/tree/mode/blob counts and cross-document consistency checks listed in §2.4 — **PASS** as inspections.
- **Executable test / lab reruns: NOT RUN.** This is an audit/planning task; rerunning the 296-test matrix,
  QEMU smoke, or preflights is out of scope, and the accepted #129/#133/#137 runtime baselines are cited
  as provenance, not relabeled as this audit's runtime.
- **Learner sessions: NOT RUN** (separate human gate; AI cannot satisfy it).
- **External re-audit: NOT RUN** (separate independent gate).

---

## 3. v1.0 gate matrix

Exactly one evidence status per gate. Exactly one next-action classification per non-satisfied gate.

Status vocabulary: `SATISFIED` / `PARTIALLY SATISFIED` / `UNSATISFIED` / `BLOCKED` / `NOT APPLICABLE`.
Classification vocabulary: `HUMAN EVIDENCE REQUIRED` / `IMPLEMENTATION REQUIRED` /
`INDEPENDENT AUDIT REQUIRED` / `OPERATING-EVIDENCE REQUIRED` /
`GOVERNANCE DECISION REQUIRED` / `ENVIRONMENT / PINNING REQUIRED`.

### Gate 1 — Complete Core spine teachable

**Status: `PARTIALLY SATISFIED` — next action: `INDEPENDENT AUDIT REQUIRED`.**

Authoring completeness (source/static) is established:

- 25 Core Modules M00–M24; 70 learner Lessons + 6 non-lesson companions (LAB-OPT-02/03/05, EXP-02/03/05) = 76 `book/` files.
- 24 `labs/foundations/` directories (M00–M01 combined + M02–M24) with activities, tests, preflights, resets.
- DAG stage-boundary sampling PASS, 18-concept first-home integrity PASS, 8-competency label PASS, evidence-template neutrality PASS — all per the accepted #129 audit of base `d6641e8`.
- Per-module Lead review consumed every batch (SIMPLE FIX / Direct Fix / Complex Rework where required); M00–M24 authoring declared complete.

“Teachable” for stable v1.0 is wider than “written” (Invariant 20; DEFINITION_OF_DONE v1.0):

- Stable `VERIFIED` promotion has not occurred for the full spine (every PROJECT_STATUS entry and every
  verification report states merge ≠ VERIFIED; author self-promotion is forbidden and did not happen).
- Independent executable coverage is v0.9-RC-scoped: #129 recorded 295/296 Python PASS with 1 WSL2-environment
  M10 failure; later narrow re-verifications closed only their routed blockers and explicitly did NOT rerun
  the full matrix. Lead final-head executable reruns are repeatedly `NOT RUN / ENVIRONMENT-BLOCKED`
  (no CI/check runs; Lead container could not resolve github.com). Known bounded debts persist as
  environment-classified items (M03 GDB three-point runtime, M06 official grader NOT RUN, WSL2 relay/timing
  specificity, Windows-only limits) — truthfully recorded, not resolved.
- Learner validation, stable environment, external audit, and operating maintenance are separate gates below;
  none may be borrowed to promote this gate.

The missing piece owned by this gate is therefore the **formal multi-role stable VERIFIED audit**
(technical accuracy + pedagogy + lab quality + curriculum integration) over the pinned stable content —
not a rewrite of the spine.

### Gate 2 — Mini Cloud App evolution complete

**Status: `UNSATISFIED` — next action: `IMPLEMENTATION REQUIRED`.**

- Source/static mapping exists and is internally consistent: P0–P9 evolution map, P0–P9 ↔ M00–M24 alignment
  (earliest-safe-entry / primary-home / mechanism-ownership with DAG authority preserved), CURRICULUM_MAP
  milestone references, final-reconciliation §6 detail. No mapping contradiction was found.
- Implementation does not exist: the repository contains **no `project/` directory and no deployable Mini Cloud
  tree** (`Test-Path` False at `008c040`). The accepted #129 report §13/V-129-04 records this explicitly and
  routes it as v1.0-tracked under D-024; the v0.9 release notes explicitly disclaim a complete deployable
  Mini Cloud App. The authoritative Blueprint treatment is a milestone-mapping surface, not a committed application.
- Mapping/prose must not be equated with implementation completion. No Mini Cloud completion is claimed.

### Gate 3 — All Required Labs runnable and documented

**Status: `PARTIALLY SATISFIED` — next action: `ENVIRONMENT / PINNING REQUIRED`.**

Documentation (source/static) is complete for all five Required Labs: goal, prerequisites, setup, prediction,
steps, expected observations, break/failure, cleanup/reset, exit criteria, provenance/license, and smoke
surfaces are present with neutral evidence templates.

v0.9-RC executability (provenance, not this audit's runtime) is closed:

- LAB-REQ-01 / 03 / 04 / 05 PASS at #129; LAB-REQ-02 mechanism PASS with committed-smoke FAIL (V-129-01) →
  repaired #131 (prompt-paced interaction, standalone-marker-only acceptance, echo self-check) →
  independently re-verified #133 (3/3 real QEMU PASS, byte-identical license gate) →
  mode repaired #135 (4 entrypoints `100644` → `100755`, 0 insertions/0 deletions) →
  direct-invocation re-checked #137 (Git tree 4/4 `100755`, content blobs intact,
  two fresh Linux materializations with no chmod, 2/2 real QEMU PASS, reset clean).
- At `008c040` the four entrypoints remain `100755` with blobs
  `912dd79` / `6851054` / `40d8156` / `2017347` (reconfirmed by this audit's `git ls-tree`).
  No known v0.9 technical/public-license blocker remains in that chain.

Stable reproducibility is not established (hence not SATISFIED):

- OQ-BP-006 is OPEN: no canonical Linux image digest, no pinned Python/SQLite/toolchain/browser matrix.
  Recorded versions are capability evidence only (e.g. CPython 3.12.3/3.13.1/3.13.5, gcc 13.3/14.2,
  sqlite3 CLI 3.45.1 provisioned-not-preinstalled per V-129-05, QEMU 8.2.2, curl 8.5.0/8.21.0,
  riscv64-linux-gnu-gcc 13.3.0, gdb 15.1, strace MISSING).
- No CI matrix reruns the labs; Lead final-head executable confirmation is `NOT RUN / ENVIRONMENT-BLOCKED`.
- Bounded environment items (V-129-02 WSL2 relay probe, V-129-03 Windows limits, V-129-05 provisioning gap,
  M03 GDB debt, M06 official-grader NOT RUN) are truthfully classified but unresolved as stable guarantees.

### Gate 4 — Provenance and licenses in order

**Status: `SATISFIED`.**

- V-129-06 closed by #131 and independently verified by #133: committed `LICENSES/Apache-2.0.txt` and
  `LICENSES/CC-BY-SA-4.0.txt` are byte/hash-identical to the official ASF and Creative Commons plaintexts;
  `LICENSES/README.md` points at the committed texts and names the same official URLs; no “to be added”
  language remains.
- `ATTRIBUTION.md` ledger (`No third-party material has been incorporated yet`) is truthful at base:
  `git ls-files labs` contains no vendored xv6/OSTEP/CS:APP/CS144 source; the LAB-REQ-02 xv6 tree is
  runtime-cloned at exact pin `35b088427ef37611c38afdeed5a52a278cae38f9` with upstream LICENSE checked;
  Optional labs (LAB-OPT-02/03/05) are Strictly Optional / link-only / zero-vendoring;
  M11 PKI material is labeled public localhost-only test fixture; LAB-REQ-02 pin is identical across
  README / SOURCE_PIN.md / setup.sh / smoke.sh.
- Per-lab provenance/license statements are present in all five Required Lab READMEs.
- This SATISFIED verdict covers static order at base. Preserving it through future changes is the job of
  Gate 8 (operating maintenance), not a second Gate 4 finding. No provenance repair is routed.

### Gate 5 — Independent multi-role verification

**Status: `PARTIALLY SATISFIED` — next action: `INDEPENDENT AUDIT REQUIRED`.**

What exists (strong for an RC, insufficient for stable):

- Independent Full-Core Integration Verification (#129: exact-base audit, 25/70/5 inventory, DAG/concept/
  competency/evidence/provenance/safety/hygiene audits, 296-test executable matrix with truthful
  environment classification, no-repair invariant honored, `NOT READY` honestly reported).
- Independent narrow re-verifications (#133 for smoke/license semantics + 3× QEMU; #137 for
  direct-invocation + 2× QEMU), each exact-base, each no-repair, each with explicit NOT RUN tables.
- Per-batch independent Lead review across all Research → Design → Implementation slices with Direct Fix /
  Complex Rework routing and expected-head protected merges.
- Blueprint Final Exit Audit (#23/#24, 30/30 after narrow Lead fixes).

What is missing for a stable multi-role gate (DEFINITION_OF_DONE VERIFIED = technical accuracy +
pedagogy + lab quality + curriculum integration; author self-approval insufficient):

- No formal full-spine multi-role VERIFIED promotion exists; every merge record correctly withholds it.
- Pedagogy / lab-quality / integration review at stable depth is not evidenced as a separate sign-off;
  most final-head Lead confirmations are static/source-based with executable `NOT RUN / ENVIRONMENT-BLOCKED`
  and no CI/check runs to close the gap.
- A stable-content re-verification on the pinned canonical environment (Gate 10 output) has not run —
  by sequencing necessity, not by omission.

### Gate 6 — Target-learner validation of key Core paths

**Status: `UNSATISFIED` — next action: `HUMAN EVIDENCE REQUIRED`.**

- Issue #34 is OPEN with **zero real learner sessions**; no `meta/validation/` directory exists;
  `course/evidence/` contains only neutral templates (including the M00–M01 pilot observation template),
  all unfilled. No filled learner evidence exists anywhere in the tree.
- D-027 defers validation during authoring (non-blocking for production) but D-024 keeps it mandatory
  before v1.0 / RELEASED; OQ-BP-007 records the same. Every verification report §21 and the v0.9 release
  notes explicitly disclaim learner validation. RELEASE_AND_MAINTENANCE_POLICY requires evidence from
  real target learners (basic programming, no formal CS) covering friction, misconceptions, environment
  failures, timing, and transfer — AI simulation is never evidence.
- Issue #34 must stay `HUMAN EVIDENCE REQUIRED`: it cannot be closed, downgraded, or satisfied by AI
  evaluation, proxy metrics, or this audit. No learner validation is claimed.

### Gate 7 — External final curriculum/coverage audit

**Status: `UNSATISFIED` — next action: `INDEPENDENT AUDIT REQUIRED`.**

- The only committed external audit is `meta/audits/external-curriculum-audit-v0.1.md` (Issue #2):
  audit date 2026-08-30, snapshot `7d67fd3`, scope explicitly the **macro Blueprint before Issue #1**,
  every fine-grained recommendation marked `RECHECK-AFTER-ISSUE-1`, status READY FOR LEAD REVIEW (not VERIFIED).
- Later Blueprint work (disposition matrix R1–R15, final reconciliation, Final Exit Audit 30/30) closed the
  Blueprint — it did not audit the authored M00–M24 learner spine, labs, or Mini Cloud state, and does not
  claim to. No post-authoring external coverage audit of the full Core exists at `008c040`.
- The early artifact must not be equated with final v1.0 external coverage. A new independent final audit
  against the stable content is required. No external-audit completion is claimed.

### Gate 8 — Maintenance and review workflows actually operating

**Status: `UNSATISFIED` — next action: `OPERATING-EVIDENCE REQUIRED`.**

- Written policy exists and is coherent: RELEASE_AND_MAINTENANCE_POLICY (versions, v1.0 gate, stable
  environment, Errata & Hotfix incl. Critical Content Bug process, no tag rewriting, learner-validation rule),
  LIVING_CURRICULUM_POLICY (STABLE/CURRENT/FRONTIER cadence, Technology Admission Test, lifecycle
  ACTIVE→LEGACY→HISTORICAL→RETIRED, maintenance queue), REVIEW_POLICY (claim-over-prose, VERIFIED gate,
  Direct Fix / Complex Rework / Architecture Escalation, Issue→PR handoff, Errata routing),
  plus Issue/PR templates with a no-self-VERIFIED checklist.
- Operating evidence is absent at base, and the absence is itself evidenced:
  `.github/` holds only issue templates and the PR template — **no `workflows/` directory, no CI definition,
  no Actions/check runs** (every PROJECT_STATUS entry and verification report records “no CI/check runs”);
  no errata log, no maintenance-queue execution record, no periodic CURRENT/FRONTIER review record,
  no lab CI/smoke schedule output, no patch-release drill. The v0.9 tag is correctly immutable, but
  immutability is not operation.
- Written maintenance policy must not be equated with an operating maintenance/review workflow.
  No “operating” claim is made. Proving operation requires a time window of real runs after CI is stood up.

### Gate 9 — No critical blockers

**Status: `PARTIALLY SATISFIED` — next action: `GOVERNANCE DECISION REQUIRED`.**

- No known **v0.9 technical/public-license blocker** remains in the accepted #129→#137 chain
  (V-129-01, V-129-06, V-133-01 all independently closed; V-129-02/03 ENVIRONMENT-informational;
  V-129-04/05 bounded v1.0-tracked, not defects). No open Critical Content Bug issue exists; no committed
  suite is known-failing at `008c040`.
- For **v1.0**, the unsatisfied gates above are the work program — they are tracked gaps, not surprise defects.
  Two hygiene items need a governance disposition so the blocker register stays truthful:
  (a) Issue #41 (`[Implementation] M03 …`) is OPEN with 0 comments while its delivery PR #42 is MERGED —
  a stale-open record, not a content blocker; (b) the bounded environment items in Gate 3
  (GDB/grader/relay/provisioning) need explicit stable-scope confirmation during the OQ-BP-006 pin.
- Web Lead ownership of the blocker register (confirm/close #41 hygiene, confirm no hidden critical defect
  before each later phase) is the routed action. No “zero blockers” claim for v1.0 is made.

### Gate 10 — Stable / reproducible canonical lab environment and key version strategy

**Status: `UNSATISFIED` — next action: `ENVIRONMENT / PINNING REQUIRED`.**

- OQ-BP-006 (`What versions define the first stable environment?`) is OPEN by design as an
  implementation-time pin. It is OPEN in `meta/OPEN_QUESTIONS.md`, every Research dossier, every
  verification report, PROJECT_STATUS, and the v0.9 release-notes non-claims. No Decision closes it;
  research proposals (e.g. Noble/Python-3.12 first-slice baseline, digest-pinned image at preflight
  implementation) are explicitly proposals, not pins.
- At base there is no canonical image definition: no Dockerfile/devcontainer, no immutable digest,
  no pinned Python/SQLite/PostgreSQL-case/Linux/toolchain/browser/container/observability matrix, no CI
  environment matrix, no documented provisioning step for the sqlite3 CLI gap. Observed versions across
  author/verifier/Lead environments differ legitimately (see Gate 3) and are recorded as observations,
  never as pins. Tests rightly prefer invariants/trends where versions differ — but that policy assumes a
  canonical reference that does not yet exist.
- v0.9 publication is explicitly not proof of a stable pin. No pin is claimed or inferred.

### Gate 11 — Unresolved Open Questions relevant to stable release

**Status: `PARTIALLY SATISFIED` — next action: `GOVERNANCE DECISION REQUIRED`.**

- Closed: OQ-BP-002 (applied foundations/toolchain homes), OQ-BP-004 (S4-before-S5 narrative preference),
  OQ-BP-005 (lab selection), OQ-BP-007 (build-first sequencing via D-027). Provenance intact.
- Open with safe interim states (do not weaken): OQ-BP-001 (bounded AI literacy — RFC-CAND-001; interim:
  AI output = untrusted hypothesis, Current Case practice at M00 L00-02 / M23 L23-02; no AI Core module),
  OQ-BP-003 (human-facing boundary — RFC-CAND-002; interim: P2/P9 evidence hooks without Core HCI admission),
  OQ-BP-006 (stable environment — implementation-time pin; see Gate 10).
- None was silently closed by this audit. For v1.0, governance must either (i) decide the two RFCs
  (admit with bounded implementation, or reject with interim states declared sufficient for the stable
  scope), or (ii) explicitly record them as post-v1.0 roadmap with the interim states normative.
  OQ-BP-006 must close via Gate 10. No Open Question decision is made here.

### Gate 12 — Lifecycle semantics for VERIFIED / RELEASED

**Status: `PARTIALLY SATISFIED` — next action: `GOVERNANCE DECISION REQUIRED`.**

- Semantics are defined and have been truthfully observed: lifecycle
  `IDEA → PLANNED → RESEARCHED → DRAFTED → VERIFIED → RELEASED → NEEDS_REVIEW` (PROJECT_STATUS);
  VERIFIED requires independent multi-role review (DEFINITION_OF_DONE; REVIEW_POLICY; AGENTS.md;
  EXECUTOR.md; PR-template checklist); v1.0 = teachable not merely written (Invariant 20);
  stable tags are never rewritten and patch releases are allowed (Errata & Hotfix).
- State discipline at base is truthful: v0.9 is a `prerelease=true` Release Candidate
  (first full Core traversal), never marked VERIFIED or stable RELEASED; every merge record withholds
  lifecycle promotion; no v1.0 tag exists; nothing was self-promoted.
- The stable transitions themselves (VERIFIED promotion, RELEASED/v1.0 decision, NEEDS_REVIEW operation)
  have not executed — correctly, because their gates are unsatisfied. Executing them is a future
  Web Lead governance act after Gates 1–11 close, with operating evidence under Gate 8.

---

## 4. Gate summary table

| # | v1.0 gate | Evidence status | Next-action classification |
|---|---|---|---|
| 1 | Complete Core spine teachable | `PARTIALLY SATISFIED` | `INDEPENDENT AUDIT REQUIRED` |
| 2 | Mini Cloud App evolution complete | `UNSATISFIED` | `IMPLEMENTATION REQUIRED` |
| 3 | All Required Labs runnable / documented | `PARTIALLY SATISFIED` | `ENVIRONMENT / PINNING REQUIRED` |
| 4 | Provenance / licenses in order | `SATISFIED` | — (preserve via Gate 8) |
| 5 | Independent multi-role verification | `PARTIALLY SATISFIED` | `INDEPENDENT AUDIT REQUIRED` |
| 6 | Target-learner validation of key Core paths | `UNSATISFIED` | `HUMAN EVIDENCE REQUIRED` |
| 7 | External final curriculum / coverage audit | `UNSATISFIED` | `INDEPENDENT AUDIT REQUIRED` |
| 8 | Maintenance / review workflows actually operating | `UNSATISFIED` | `OPERATING-EVIDENCE REQUIRED` |
| 9 | No critical blockers | `PARTIALLY SATISFIED` | `GOVERNANCE DECISION REQUIRED` |
| 10 | Stable / reproducible canonical lab environment + version strategy | `UNSATISFIED` | `ENVIRONMENT / PINNING REQUIRED` |
| 11 | Unresolved Open Questions relevant to stable release | `PARTIALLY SATISFIED` | `GOVERNANCE DECISION REQUIRED` |
| 12 | Lifecycle semantics for VERIFIED / RELEASED | `PARTIALLY SATISFIED` | `GOVERNANCE DECISION REQUIRED` |

Counts: 1 SATISFIED / 6 PARTIALLY SATISFIED / 5 UNSATISFIED / 0 BLOCKED / 0 NOT APPLICABLE.
No gate uses BLOCKED (nothing is externally jammed; all remaining work is ownable) and none uses
NOT APPLICABLE (every listed gate comes from repository policy: RELEASE_AND_MAINTENANCE_POLICY v1.0 gate,
Invariant 20, DEFINITION_OF_DONE, PROJECT_STATUS, or Issue #140/#141).

---

## 5. Recommended stabilization sequence (bounded)

Constraints honored: AI-executable work is separated from real-human work; Issue #34 stays a real-human
gate; parallelizable work is identified; true v1.0 dependencies are identified; no invented release gates.

### Phase 0 — Governance housekeeping (parallel, immediate)

- Web Lead confirms the blocker register: verifies Issue #41 is stale-open against merged PR #42 and
  closes #41 on hygiene grounds without content change; confirms Gates 1–12 routing in this plan.
- Owner: Web Lead (+ auditor support on evidence, no implementation).
- Blocks nothing else; cleans the signal for all later phases.

### Phase 1 — Stable environment pin / OQ-BP-006 (first true dependency)

- Decide and commit the canonical lab environment: base image by immutable digest, Linux/Python/SQLite-case/
  compiler/toolchain (incl. QEMU/RISC-V cross-toolchain)/browser-floor/optional container+observability
  versions, provisioning steps (sqlite3 CLI, strace scope, GDB floor), preflight recording rules, refresh cadence.
- Stand up the executable matrix: CI (or documented scheduled) runs of the full Python suite, shell/C flows,
  all four preflights, and the five Required Lab smokes on the pinned image; record versions per run.
- Owner: human/Lead Decision for the pin; AI Executor for image/docs/CI implementation; independent verifier.
- AI-executable after the Decision; the Decision itself is human governance.
- **Blocks:** stable lab acceptance (Gate 3), stable re-verification (Gate 5), Mini Cloud acceptance (Gate 2),
  maintenance operation (Gate 8).

### Phase 2 — Mini Cloud implementation P0–P9 (parallel design, acceptance after Phase 1)

- Implement the runnable Mini Cloud tree per the accepted evolution map + alignment (single process + SQLite
  baseline through instrumented service to System-Defense candidate state), each milestone with its invariant,
  controlled failure, observation/measurement, security/privacy decision, and simpler alternative; keep
  PostgreSQL/queue/cache/replica/proxy/vendor depth as bounded branches/cases per the justification cards.
- Mapping/design work can proceed in parallel with Phase 1; **final acceptance testing must run on the
  Phase 1 pinned environment**.
- Owner: AI Executor(s) in bounded issues; Lead review; independent smoke/integration check.
- **Blocked by:** Phase 1 for acceptance. **Blocks:** final external audit and VERIFIED promotion.

### Phase 3 — Stable-content independent re-verification (after Phases 1–2)

- Rerun the full-Core executable matrix + Required Lab smokes + preflights on the pinned environment via CI,
  with exact-base discipline; close or reclassify the bounded environment debts (GDB, grader, relay,
  provisioning) as stable-scope decisions with evidence.
- Formal multi-role VERIFIED audit (technical + pedagogy + lab quality + integration) over the stable content.
- Owner: independent verifier(s) + Web Lead; AI-executable verification, human-owned acceptance.
- **Blocked by:** Phases 1–2. **Blocks:** release decision.

### Phase 4 — External final curriculum/coverage audit (after stable content)

- Commission an independent external audit of the stable M00–M24 spine + labs + Mini Cloud state against
  authoritative references (CS2023 as reference model, classic texts/courses as mechanism evidence —
  same method family as the v0.1 audit, new snapshot, `RECHECK-AFTER-ISSUE-1` items closed with evidence).
- Owner: external independent auditor (human/external); repository supplies frozen stable snapshot + evidence packets.
- **Blocked by:** Phases 1–3 (auditing a moving target wastes the audit). Parallel preparation allowed.

### Phase 5 — Real learner validation (start early, finish before v1.0)

- Run Issue #34 (M00–M01 first pilot, ≥1 real target-learner session with the observation template,
  anonymized) and extend bounded pilots to the remaining key Core paths the Lead designates as
  release-gating (at minimum one path per stage-cluster touching Required Labs and the Mini Cloud baseline).
- Non-blocking for Phases 1–4 per D-027 (start immediately — lead time dominates); **blocking for the v1.0
  decision** per D-024. AI may organize/analyze real observations only; sessions, friction, misconception,
  timing, and transfer evidence must be human.
- Owner: human learners + human observer/recorder. **Not parallel-substitutable, not accelerable by AI.**

### Phase 6 — Maintenance operation shakedown (needs a time window)

- Operate the written policies visibly: CI/smoke schedule with history, CURRENT/FRONTIER review-tick records,
  maintenance-queue burn-down, one errata drill (file → fix on main → patch-note path without touching `v0.9`),
  review-routing records. Duration must be long enough that “operating” is evidenced, not asserted.
- Owner: Web Lead + Executors; CI infra from Phase 1.
- **Blocked by:** Phase 1 (infra) in the short term; calendar time in the long term. Start the clock as soon
  as CI lands; do not leave this phase last in planning even though its evidence matures last.

### Phase 7 — OQ-001 / OQ-003 RFC decisions (parallel governance)

- Resolve bounded AI literacy (OQ-BP-001) and human-facing boundary (OQ-BP-003) by RFC → Decision:
  admit as bounded Core (then implement + verify before Phase 3/4 close) or reject for v1.0 scope
  (then declare the interim states — AI-output verification practice; P2/P9 evidence hooks — normative
  for stable and move full admission to post-v1.0 roadmap).
- Owner: Web Lead governance with human judgment; AI supports research/drafting only.
- Parallel with Phases 1–6, but the decision must precede the Phase 3/4 closures if it admits new Core scope.

### Phase 8 — VERIFIED → RELEASED / v1.0 decision (Lead governance only)

- After Gates 1–11 are truthfully closed with evidence, Web Lead promotes the stable content to VERIFIED,
  cuts `v1.0` (never moving `v0.9`), publishes release notes with the same non-claim discipline as v0.9,
  and opens the NEEDS_REVIEW maintenance era.
- Owner: Web Lead only. No Executor self-promotion, no audit self-acceptance.

Dependency spine: **Phase 1 → (Phase 2 acceptance, Phase 3) → Phase 4 → Phase 8**;
**Phase 5 runs parallel from now until Phase 8**; **Phase 6 clock starts with Phase 1 infra and matures
into Phase 8**; **Phase 7 decides before Phase 3/4 close**; **Phase 0 is immediate**.

---

## 6. Explicit non-claims (binding on this audit)

Until supported by repository evidence, this audit does not claim:

- Issue #34 complete; real learner validation complete;
- stable `VERIFIED`; stable `RELEASED`; v1.0 ready;
- Mini Cloud complete; final external coverage audit complete;
- maintenance workflows operational; stable environment fully pinned;
- OQ-BP-001 / OQ-BP-003 / OQ-BP-006 closed;
- any Lesson/lab/test modification, repair, or improvement by this audit.

## 7. Residual risks / not-run work for Lead review

1. This auditor ran **no executable suite, smoke, QEMU, or preflight** (NOT RUN by Task Contract scope);
   all runtime citations are provenance from the accepted #129/#133/#137 reports at their locked bases,
   not evidence at `008c040` beyond the byte/mode/tree inspections listed.
2. Lead final-head executable confirmation remains `NOT RUN / ENVIRONMENT-BLOCKED` across the project
   history (no CI, Lead container GitHub resolution limit) — Phase 1 CI is the structural fix.
3. `book/` inventory was counted read-only (76 files = 70 Lessons + 6 companions); Lesson-prose quality
   was not re-judged — that belongs to the Phase 3 multi-role audit.
4. Pre-existing local state (untracked `.commandcode/`, ignored xv6 `worktree/`, ignored `__pycache__`)
   was preserved and is not audit evidence; the Lead should confirm the PR diff contains only this report.
5. If Web Lead review finds any gate status or citation wrong, the correction belongs as a bounded
   report-only Direct Fix on this branch/PR — not as a content repair, and not as a silent status change.

---

## 8. Final recommendation

**`V1.0 GAP PLAN READY FOR WEB LEAD REVIEW`**

Rationale: all twelve required v1.0 gates were audited against repository truth at the canonical base
with exactly-one status and exactly-one routed next action each; the five UNSATISFIED gates name their
real missing evidence (implementation, human sessions, external audit, operating history, environment pin)
without fabrication; the six PARTIALLY SATISFIED gates separate established RC strength from missing stable
guarantees without overclaiming; the one SATISFIED gate (provenance/licenses) is hash-evidenced and scoped
to base order rather than future operation. The sequencing plan is bounded, dependency-honest, keeps
Issue #34 human, and invents no new release gates. This recommendation means the **plan** is review-ready —
it does not mean v1.0 is ready, and no lifecycle promotion is implied.

---

## 9. Auditor execution trace (report-level)

- Base lock: `008c0407420bf44a9ea8f96645c366224f0fc333`; branch
  `audit/issue-140-post-v09-v10-gap-plan`; start HEAD equals base; worktree clean modulo pre-existing
  untracked/ignored scratch (see §2.2).
- Reads: Issues #140 (full), #141, #34, #139, #129/#131/#133/#135/#137 (state + bodies as cited),
  RELEASE_AND_MAINTENANCE_POLICY, DEFINITION_OF_DONE, PROJECT_STATUS (pre- and post-`008c040` diff),
  OPEN_QUESTIONS, DECISIONS, CURRICULUM_INVARIANTS, EXECUTOR guide, all three verification reports (full),
  external audit v0.1 (full scope/method/R-table), Mini Cloud evolution + alignment (full P0–P9),
  LIVING_CURRICULUM_POLICY, REVIEW_POLICY.
- Inspections: `gh` Issue/PR/release/tag state; `git ls-remote` (no competing audit branch);
  `git ls-tree` (4/4 `100755` + blob identities); `Test-Path project/` (False);
  `book/` + `labs/` + `course/evidence/` + `LICENSES/` + `.github/` + `meta/` inventories;
  `ATTRIBUTION.md` + `LICENSES/README.md` text; open-Issue list (4 open: #34, #41, #140, #141).
- Problems: initial `gh issue view` empty output (PowerShell `head` absent) → reran with `--jq` (resolved);
  `git cat-file` miss before `git fetch` (stale local) → fetched, base resolved (resolved);
  oversized directory listing truncated a combined inventory command → reran scoped (resolved).
  No problem was found in the audited material that required repair routing beyond the plan itself.
- Ownership: this file is the auditor's sole authored change. All cited Executor/Verifier/Lead work
  remains attributed to its original heads/merges; nothing is claimed here.
