# Audit → Architecture Disposition v0.1

**Task:** Issue #10 — [Blueprint Reconcile] Audit recommendations → architecture disposition matrix
**Feeds:** Issue #9 — [Blueprint] Reconcile Issues #1–#4 into Blueprint v0.1 maps
**Status:** READY FOR LEAD REVIEW — proposal only, NOT `VERIFIED`, not canonical
**Base branch:** `origin/main` at `3d53caac24672e9b31cca0a2a09b38e1b9a5dab0` (fetched and confirmed before work)
**Date:** 2026-08-30

## 1. Purpose and authority

This artifact proposes a single, evidence-backed disposition for every material audit recommendation R1–R15 from `meta/audits/external-curriculum-audit-v0.1.md`. It feeds the Issue #9 integration task; it is **not** a canonical architecture decision.

It does not edit and must not be treated as editing the canonical files: Curriculum Map, Competency Matrix, Concept Registry, Decisions, Open Questions, Project Status, Curriculum Invariants, the Stage/Module/Lesson proposal, the dependency graph, Mini Cloud App maps, or the Lab/Source Selection Map. All canonical integration is performed by the Web Lead / Issue #9 integrator after this proposal is reviewed.

The accepted reconciliation artifacts merged after Issue #10 was created are **inputs, not ignorable history**:

- `meta/blueprint/mini-cloud-curriculum-alignment-v0.1.md` (Issue #11 / PR #14)
- `meta/blueprint/competency-concept-integration-v0.1.md` (Issue #13 / PR #15)
- `meta/blueprint/lab-source-selection-map-v0.1.md` (Issue #12 / PR #16)

This document therefore differs from any pre-merge draft: every disposition below states which parts of the recommendation are already solved by #14/#15/#16 and which parts remain open for #9.

## 2. Decision criteria

The six dispositions are applied as follows:

1. **INTEGRATE EXISTING CORE** — The capability is already conceptually inside the accepted Core (Module map, dependency graph, or a completed/merged reconciliation artifact). The recommendation mainly needs an explicit learning outcome, clearer placement, assessment evidence, horizontal-thread visibility, or a small extension to an existing Module. This must not create a new Module or Stage.
2. **BOUNDED CORE ADDITION** — There is a genuine missing Core capability that requires new material, but it can be bounded inside an existing Module/thread without creating a professional specialization. Used only with: exact boundary, explicit exclusions, proposed home, what existing content shrinks, competency gain, and bloat-control.
3. **CURRENT CASE** — Valuable modern/current practice for reality awareness, but not a stable shared-Core concept. It must survive pedagogically if the current product/workflow disappears (Living Curriculum Policy; Technology Evaluation Framework).
4. **DEEP DIVE** — Valuable depth that belongs after the complete shared world model because of specialization/depth, implementation, formalism, or platform burden.
5. **REJECT** — Insufficient educational value for Essential CS, or a simpler concept provides the same capability, or it adds degree-style baggage / scope distortion / product training. Rejection is never because a topic is hard.
6. **ARCHITECTURE ESCALATION** — Accepting/rejecting would materially change Core identity, Core scope, curriculum philosophy, major Stage/Module architecture, Curriculum Invariants, or the meaning of the shared world model. Deciding is deferred with an Open Question framing, evidence requirements, RFC need, options, and integration-blocked status.

Guardrails applied to every row:

- CS2023 inclusion, university coverage, or "industry relevance" is never sufficient grounds for Core admission.
- Every Core inclusion must name at least one competency improved (Trace / Explain / Observe / Diagnose / Correctness / Judge / Estimate / Learn-New-Tech). Terminology-only additions do not enter Core.
- Every Core addition states its bloat-control / explicit exclusion.
- The Module DAG is authoritative and is not altered here. No S4→S5 hard edge is created or implied; Stage narrative is not dependency.
- Teach Once → Revisit Many (Invariant 11, D-010): every proposed concept has one first home and later application revisits; no duplicate canonical definitions. Product names, individual commands, and ephemeral frameworks receive no stable Concept IDs.
- The audit and the accepted artifacts use different recommended-class vocabularies (CORE/CURRENT CASE/DEEP DIVE/REJECT in the audit; six dispositions here). The audit's class is evidence for the direction; the disposition is the architecture consequence for Essential CS. Where the two coincide, one row.

## 3. R1–R15 disposition matrix

Every recommendation appears exactly once as a primary row. Confidence follows the audit's own column (`external-curriculum-audit-v0.1.md`, §9) and is re-labeled only where this task's live verification changes it.

| Recommendation | Problem/gap found | Disposition | Proposed home | Competency gain | Dependency impact | Canonical concept impact | Bloat-control action | Evidence/confidence |
|---|---|---|---|---|---|---|---|---|
| R1 Applied discrete, probability, statistics, and scale reasoning | Macro-level underrepresentation; no visible just-in-time toolkit or dependency policy; hidden prerequisite risk (DAG §6 stats flag) | **BOUNDED CORE ADDITION** | M02 `L02-01` (discrete/asymptotic/counting; already the complexity first home) + M04 `L04-02` (measurement variant: distribution/median/percentiles/uncertainty, canonical first intro for the statistical toolkit); revisits M09, M10, M13, M16, M17, M19, M20, M23 | Estimate, Correctness, Diagnose, Judge | No new H edge; subset S-level bridge at first measurement use (M04), revisited at M16/M17/M20/M23; availability/failure probability stays just-in-time inside M16/M17. No math gate. | No new Registry ID. Uses existing Estimate/Measurement capability; M04 owns "measured variation + inference limit"; "statistical reasoning" is a tool pattern, not a Big Idea (aligns with #15 §8.3) | One compact toolkit + one reusable evidence worksheet; explicitly no probability course, no calculus, no inferential statistics sequence, no linear algebra, no proof portfolio | Audit: High (gap confidence; placement marked `RECHECK-AFTER-ISSUE-1`); live-verified NIST measurement-uncertainty concept page; final first home remains OQ-BP-002 territory. Sub-points (discrete; probability; statistics; scale) all resolved inside this row — see §4.1 |
| R2 Toolchain/software-development fundamentals | Horizontal labels only; no protected first observable outcome; DAG §6 flags shell/git as hidden-prerequisite risk | **INTEGRATE EXISTING CORE** | M00 `L00-02` canonical home (shell, code reading, debugger-light, Git evidence, environment manifest, small reproducible investigation); lab-entry gate at every REQUIRED lab; revisits M03/M04/M06/M07/M10/M11/M13/M15/M19 (packaging `L19-03`), M20, M23 | Observe, Diagnose, Explain, Learn-New-Tech, Correctness | No new edge; elevate L00-02 and environment preflight to an explicit prerequisite for REQUIRED labs (already the direction in DAG §6 and #16 lab prerequisites); Git internals, shell implementation stay non-prerequisite | No new Registry ID; tooling is explicitly not a Concept Registry subject (#15 §6.2) | One repeatable investigation + evidence artifact, task-centered tool slices; no "Linux commands encyclopedia", no CI-vendor syllabus, no Agile ceremony inventory, no Software Engineering course | Audit: High. Live-verified MIT Missing Semester 2026 index incl. shell, dev tools, debugging/profiling, Git, code quality. #15/#16 already require the evidence — this row makes outcomes/gate explicit |
| R3 HCI/accessibility/user-boundary reasoning | Macro-level omission; user goals, mental models, feedback/error recovery, accessibility, consent/privacy interaction, human-facing failure not named in spine | **ARCHITECTURE ESCALATION** | Provisional (only if RFC admits): M00 `L00-01` boundary vocabulary; M12 `L12-03`/`L12-04` browser-facing accessibility mechanics; evidence hooks at P2 (denial/error/privacy interaction) and P9 (affected users, accessibility, consent, recovery) per #14 | (conditional) Explain, Judge, Diagnose, Correctness, Trace | No edge change before RFC; no hidden prerequisite. Project evidence hooks already added by #14 without Core admission | No HCI/accessibility/consent IDs are assigned (#15 §8.2); OQ-BP-003 remains open | If admitted: user goals, feedback/error recovery, keyboard/AT awareness, consent/privacy interaction, one human-evaluation checkpoint. Excluded: visual/UX design, interaction history, usability-research methods, design systems, exhaustive WCAG, legal survey | Audit: Medium. Live-verified W3C intro (accessibility = perceiving/understanding/navigating/interacting; last updated 3 Feb 2026) and W3C evaluation page (no tool alone determines accessibility; knowledgeable human evaluation required). See §6.1 |
| R4 Bounded AI literacy and data/model judgment | Macro-level omission; no explicit AI anchor despite CS2023 basic-AI-literacy goal | **ARCHITECTURE ESCALATION** | Provisional (only if RFC admits): M02 `L02-03` (problem formulation, search-vs-learning, rule vs learned distinction); M13 `L13-03` (data quality, labels/features, train/eval separation, schema/provenance); M23 `L23-02` (suitability, uncertainty, resource cost, security/privacy/impact, when-not-to-use) | (conditional) Judge, Explain, Diagnose, Estimate, Learn-New-Tech | No new hard edge; candidates reuse M02/M13/M20/M21–M23 existing edges; no ML math, no LLM architecture, no model-training prerequisite | No AI/model/evaluation IDs assigned (#15 §8.1); OQ-BP-001 remains open; safe interim pattern = source/test/measurement verification of an AI-generated claim | If admitted: problem suitability, data/model/evaluation failure, uncertainty, resource cost, impact. Excluded: Transformer/ML theory, gradient math, training infra, prompt-engineering catalogs, vendor/model surveys, fast-decaying API tutorials | Audit: High. Live-verified CS2023 Final Report index (incl. "Generative AI and the Curriculum" section) and NIST AI RMF/AI Resource Center (AI RMF 1.0 under revision; GenAI profile NIST-AI-600-1; 2026-04-07 critical-infrastructure concept note) — evidence of system-level AI risk areas, not an AI-literacy syllabus. See §6.2 |
| R5 Generative AI and agentic coding as current evidence work | Current-practice risk; stable verification pattern vs fast-changing tools distinguished | **CURRENT CASE** | M00 `L00-02` verification principle (generated output = untrusted hypothesis); M23 `L23-02` technology evaluation revisit; policy-level integration into tool/source-verification (#14 §7 R5 row) | Learn-New-Tech, Correctness, Diagnose, Explain, Judge | None; no mandatory AI tool; every Core task completable AI-free; if AI used, same evidence/review gates apply | Not a canonical concept ("prompting" is not a Registry subject); verification of delegated/generated work is the stable anchor, first taught as the M00 source-verification habit | One or two bounded tasks (explain a generated patch; test a generated claim); no tool comparisons, no prompt recipes, no autonomous-agent ops, no product certification; review cadence 6–12 months | Audit: High. Live-verified Missing Semester 2026 Agentic Coding + Code Quality lectures (agent feedback loop; "AI can make mistakes"; code review) — a current-practice signal, not a syllabus |
| R6 Data modeling, encoding/evolution, provenance, derived data | Fine-grained risk `RECHECK-AFTER-ISSUE-1`: DB label doesn't reveal modeling/evolution/compatibility/provenance coverage | **BOUNDED CORE ADDITION** | M13 `L13-03` extended as canonical first home (schema invariant → schema evolution; readers/writers; migration/backfill choice; source-of-truth vs derived); M01 `L01-04`/M13 `L13-02` representation/model distinction; revisits M16 `L16-02` (serialization compatibility), M18 (derived/event data), M19/M23 (supply-chain/source provenance), P0/P4/P6/P9 evidence | Trace, Correctness, Judge, Diagnose, Learn-New-Tech | No new edge; M08/M09→M13 existing H edges suffice; M16/M18 remain revisits/applications; no S4↔S5 change | No new canonical ID in first population (mirrors #15 §8.4 deferral). Exercises existing Representation/State/Interface/Invariant concepts in the schema-evolution context; "schema evolution" is an application pattern, not a Big Idea | One evolving schema + one derived view in the existing DB surface; no Data Engineering stage; no PROV ontology, no schema-registry ops, no lineage platform, no data-lake/warehouse catalog, no NoSQL family survey, no stream framework | Audit: High. Live-verified W3C PROV-DM (entities/activities/agents/derivation/responsibility; core vs extended) — conceptual boundary only; Apache Avro reader/writer schema resolution is cited via the official specification as one concrete current example (spec not re-fetched this session — marked secondary/uncertain; see §12). See §4.6 |
| R7 Experimental measurement/diagnosis needs a required pattern, not tool exposure | Competency evidence pattern under-specified | **INTEGRATE EXISTING CORE** | M04 `L04-02` first explicit pattern home (question/hypothesis/baseline/controlled change/metric/environment/workload/repetitions/observation/limit); M20 `L20-01/02` production-signal revisit; M23 `L23-01` consolidated methodology | Observe, Diagnose, Estimate, Explain | Existing edges M03→M04, M19/M16→M20, M20→M23 sufficient; add the graph-proposed light clock-semantics bridge (monotonic vs wall clock) at M20 (`L20-01`) or M23 without any formal stats prerequisite | No new concept IDs. Measurement/Estimate competencies already own it; the evidence-pattern vocabulary (baseline, warmup, distribution, limit) becomes assessable | One reusable measurement record + small representative set of experiments; no scientific-method course, no benchmark-per-Module requirement, no formal causal-inference theory | Audit: High. Live-verified Python `time` docs (monotonic non-decreasing clock vs wall-clock `time()` vs perf_counter short-duration; 3.14.7 docs current 2026-08-30). #15 evidence packet (Prediction/Break/Judge) and #16 §1.2 measurement rule already institutionalize this — this row upgrades M04 to the first assessed home |
| R8 Security, privacy, accountability, responsibility may be too late if left to Security Synthesis | Late-synthesis risk | **INTEGRATE EXISTING CORE** | Preserve first intros: M07 `L07-01` (isolation), M11 `L11-01` (transport crypto), M12 `L12-03` (origin/CORS/CSP); M19 `L19-03` (supply chain/deployment trust); M21/M22 synthesis; M23/M24 judgment. Evidence already required at P0/P2/P3/P4/P6/P7/P8/P9 (#14) | Trace, Correctness, Diagnose, Judge | Existing H edges M07/M11/M12→M21/M22 retained; no new late-only dependency | Trust Boundary ID already proposed (#15, EC-CON-017, M21 first home); no security-specific IDs beyond that; SEP remains horizontal behavior, not a Chapter | Recurring boundary questions + one safe local target; no legal/compliance curriculum, no exploitation track, no crypto implementation, no vulnerability catalog, no certification survey; accessibility is NOT resolved here (stays in R3) | Audit: High. Live-verified CS2023 component index; #14 §7 R8 row + #15 stage evidence requirements already implement the horizontal-evidence claim. See §4.8 |
| R9 Computational models, limits, algorithm–language connection | Fine-grained risk `RECHECK-AFTER-ISSUE-1`: tractability/expressibility/limits/decidability intuition not protected; connection to PL/runtime/compiler implicit | **INTEGRATE EXISTING CORE** | M02 `L02-01/02/03` (intuitive model of computation, tractability/limits, representation→cost); M05 `L05-01/02` revisit (source→representation→runtime→machine; language construct → runtime mechanism) | Explain, Correctness, Judge, Learn-New-Tech | Existing M01/M02→M03→M05 edges correct; no formal-theory prerequisite | No new IDs; Computation/Complexity and Specification already canonical homes (#15); automata/computability remain Deep Dive | Small operational boundary: models, abstraction, representation, complexity, tractability/decidability intuition, language/runtime connection. Excluded: full automata theory, reductions, computability proofs, formal-language portfolio, advanced complexity theory | Audit: Medium. Matches #1's M02/M05 design and #15 §3 guardrail (M05 exit = trace + justified claim, not parser vocabulary). See §4.9 |
| R10 Consensus important as concept, expensive as implementation | Concept vs implementation ambiguity | **INTEGRATE EXISTING CORE** | M17 `L17-01` (replication/quorum/durability context), `L17-02` (consensus concept, leader election, bounded state-machine trace — canonical first intro), `L17-03` (consistency models, CAP-style framing); M18/M23/M24 revisits | Explain, Trace, Diagnose, Judge | Existing H edges M16→M17, M14→M17 retained; no implementation prerequisite; #16 keeps M17 as concept/observation case, full Raft Deep Dive | No Registry ID for Consensus in first population (#15 §8.5 deferral); consistency concept already owned at M14/M17 | Requirement: worked trace + failure scenario + judgment artifact, not a Raft/Paxos build; no replicated-service project for M17 exit | Audit: High. #16 LAB map M17 boundary wording ("full Raft/Paxos implementation is Deep Dive"); #14 §7 R10 row. See §4.10 |
| R11 Full consensus algorithms, proofs, replicated-service implementation | Specialist depth at graduate-level prerequisite cost | **DEEP DIVE** | Optional S6 Source Expedition or post-S7 distributed Deep Dive, coordinated with #4/#16; do not add to Core exit criteria | (deep dive only) Trace, Correctness, Diagnose, Judge | No Core edge; no new required codebase; explicit stopping point | No Core concept changed; protects the M17 conceptual boundary | One optional algorithm + one explicit stopping point; no graduate distributed-systems course, no proof portfolio, no mandatory replicated service | Audit: High. #16 records MIT 6.5840 as graduate-level evidence; #14 §7 R11 row |
| R12 Physical, embedded, real-time boundary case | Underrepresentation but not proven Core necessity | **DEEP DIVE** (pending evidence) | Optional small resource/deadline/sensor case as Source Expedition after M03/M04 or later Deep Dive; no hardware dependency | (if selected) Observe, Explain, Judge, Estimate | No new Stage/edge; no board/FPGA/toolchain requirement; abstract machine model remains sufficient | No new concept IDs | One reproducible emulator or carefully bounded case; excluded: embedded platform track, firmware breadth, robotics, FPGA/HDL, real-time scheduling theory, device-driver engineering | Audit: Medium. #14 §7 R12 row explicitly keeps this an architecture question (no P0–P9 dependency). See §4.12 |
| R13 Cloud/orchestration product breadth risks consuming Core attention | Product-vendor-command risk | **CURRENT CASE** (stable mechanisms remain Core) | M19 `L19-01..03` stable mechanisms (namespaces/cgroups, images, containers, VM vs container, deployment, CI/CD concept, IaC concept, observability); one replaceable product case chosen via Technology Admission Test; M20 revisits, M23 evaluates | Explain, Trace, Diagnose, Estimate, Learn-New-Tech | Preserve M06/M07/M08/M16→M19 and M19→M20 edges; Kubernetes/cloud account/Terraform/CI provider are not curriculum prerequisites | No product/model Family Registry IDs; Container/Deployment mechanism remains a Module-level case, not a Big Idea | One product-neutral mechanism surface + one removable case; orchestration narrowed to the smallest feature exposing scheduling/isolation/packaging/failure/cost; Kubernetes administration, service mesh, cloud certification → Deep Dive/job-specific | Audit: High. #14 Technology Admission section: container = optional P7 comparison; Kubernetes/service-mesh/orchestration = not canonical; native Linux path canonical. See §4.13 |
| R14 Full kernel, protocol stack, compiler, database-engine projects | Degree-style implementation burden | **DEEP DIVE** (small slices per Adopt → Adapt → Build) | Core adopts/adapts small real-mechanism slices only: xv6 `sleep` trace (LAB-REQ-02), SQLite query/index + transaction/recovery (LAB-REQ-04/05 — Build after rights-blocked course projects), RFC 9110 HTTP trace (LAB-REQ-01), POSIX threads (LAB-REQ-03); full xv6, TCP/IP, compiler, DB-engine builds remain optional/source-expedition | (slices) Observe, Diagnose, Explain, Correctness, Trace; (full builds) not Core | Existing DAG kept; #16 selection map is the authoritative proposal; no broad "complete implementation" path before M06/M10/M13/M17 | No change; mechanism concept IDs unaffected | Mechanism-to-competency justification per slice; explicit stopping point; remove overlapping implementation; no bundled third-party lab material with unresolved license; sacrifice construction breadth for complete shared model | Audit: High. #16 reworked selection (5 Required / 5 Optional / 5 Source Expeditions) is the resolved Lab outcome; CS:APP Attack Lab rejected from Core. See §4.14 |
| R15 Quantum and other specialist topic inventories | No demonstrated shared-model dependency; novelty/tradition expansion risk | **REJECT** | No Core, project, or Expedition admission; explicit boundary preserved | None claimed (omission protects Trace/Explain judgment chain) | None | No Concept IDs; boundary recorded so novelty cannot expand Core | Explicitly excluded: quantum algorithms/hardware, and any specialist inventory without a demonstrated cross-cutting dependency; learner interest → future Deep Dive list only after an RFC demonstrates a concrete dependency | Audit: Medium. Live-verified CS2023 Final Report component index (quantum material is specialist/non-required); #14 §7 R15 row. Reopen only via Open Question → RFC with evidence and bloat trade-off. See §4.15 |

## 4. Detailed rationale by recommendation

The matrix is the summary. This section records the reasoning the #9 integrator needs without repeating all source research. Where a recommendation contains sub-points, they are addressed inside the recommendation's own block (no R16/R17 invented).

### 4.1 R1 — Applied discrete, probability, statistics, and scale reasoning — BOUNDED CORE ADDITION

This is the highest-attention architecture item. The accepted policy is "just-in-time theory" (D-002; OQ-BP-002). The audit's MSF evidence is cross-cutting coverage; it is **not** a recommendation for a mathematics Stage, and its own §8 rejects a full discrete-math/calculus sequence as Core packaging.

**What the learner actually needs** (three distinct layers, kept separate):

1. **Essential applied reasoning (Core):** counting and size reasoning (M01/M02 already have it); asymptotic growth and order-of-magnitude scheduling (M02 `L02-01` already); measured variation as distributions, median/percentiles, repeated measurements, and the limit of an inference (M04 `L04-02` — the only genuinely new canonical first home); availability/failure-probability estimates at M16/M17 as one-session applications; latency distributions at M20/M23; selectivity/cost estimates in M13; cloud cost/scale in M19.
2. **Useful but optional formal depth (Deep Dive boundary):** proof techniques, combinatorics beyond counting, formal probability, p-value machinery, formal inference.
3. **Not needed for the shared model:** calculus, linear algebra, advanced distribution theory.

**Boundary and exclusions:** no standalone probability course; no statistics sequence; no "math prerequisite gate" before M01. The toolkit is a horizontal thread (an applied counterpart to Napkin Math) with one first home for measurement uncertainty (M04) and later revisits; definitions are never re-taught.

**What shrinks / is reframed:** nothing existing is removed, but the temptation to insert an applied-math Module at the front must be rejected; the DAG's existing "statistics bridge" flag is resolved by placing the first teaching at M04 (where measurement first requires it) rather than a late M23-only home. OQ-BP-002 leaves final home/depth to #9; this proposal argues M04 is strictly better than M23-alone because the learner measures in M04 before reaching M23.

**Evidence:** NIST's measurement page frames measurement as a process producing a value attributable to a quantitative property with explicit uncertainty — the lesson should teach measurand/units/uncertainty/limits, not formulas. [NIST](https://www.nist.gov/itl/sed/topic-areas/measurement-uncertainty) (live-checked). The audit's DAG cross-check already flags this as a hidden-prerequisite risk (`dependency-graph-v0.1.md`, §6).

### 4.2 R2 — Toolchain and software-development fundamentals — INTEGRATE EXISTING CORE

**Why not BOUNDED CORE ADDITION:** the structure already exists and is already being enforced by #15 and #16 — #15 Stage S1/S3 require "tool fluency … explicit lab prerequisite, not an unassessed M00 mention" and an "applied toolchain bridge"; every selected lab in #16 names M00 shell/Git/reset discipline as a prerequisite. The only remaining work is explicitness and a gate. That is exactly the INTEGRATE semantics.

**Proposed explicit outcomes (for #9):**
- M00 `L00-02`: the learner runs one reproducible investigation — read an unfamiliar file, run a command, make a controlled change, record it in Git, run the test, and save an environment/version/evidence record.
- Lab-entry gate: obtain repository, run documented preflight check, reproduce baseline, save evidence record. Required for LAB-REQ-01..05, staged at M06/M13/M15 boundaries (environment repetition per DAG §6).
- Revisit homes: debugging/profiling at M03 (`gdb`/`objdump`), M04 (`perf`), M06 (`strace`), M07 (sanitizers), M10 (`ss`/`nc`), M13 (`EXPLAIN`), M15 (race stress), M20 (observability); packaging/deployment at M19 `L19-03`; source verification at M23 `L23-02`.

**Exclusions:** shell implementation, Git object model internals, every build system, vendor CI syntax, Agile ceremony, production package-publish policy, exhaustive debugger/profiler mastery. Tooling is explicitly not a Concept Registry subject (#15 §6.2).

**Evidence:** MIT Missing Semester 2026 (live-verified index: shell, command-line environment, development environment and tools, debugging and profiling, version control/Git, packaging and shipping code, agentic coding, beyond the code, code quality). CMU 15-213 lab code reviews / understanding checks (audit §2.3).

### 4.3 R3 — HCI, accessibility, user boundary — ARCHITECTURE ESCALATION

Full framing in §6.1. Key point: #14 already provides **evidence-only hooks** (P2 denial/error/privacy interaction; P9 affected users/accessibility/consent/recovery where relevant) and explicitly says this does not settle Core scope. #15 §8.2 assigns no HCI/accessibility/consent IDs. OQ-BP-003 remains the decision point. Adding an explicit Core human-facing boundary would change what a "complete modern computing-system world model" means (Invariant 1/9), so it must not be decided in a disposition matrix.

### 4.4 R4 — Bounded AI literacy and data/model judgment — ARCHITECTURE ESCALATION

Full framing in §6.2. Project decision (quoted in the task) says AI/LLM is not automatically a Core topic; using AI to produce/maintain the curriculum does not make AI a Core subject. #14 preserves OQ-BP-001 and routes AI-claim verification to a CURRENT CASE pattern; #15 §8.1 assigns no AI IDs and names the safe interim pattern. A bounded "AI-output verification / technical-literacy capability" (AI output is not authority; verify claims; source/evidence checking; code review/testing; model limitations in technical investigation) can be taught **without** teaching ML theory, transformers, LLM architecture, prompt engineering, or AI product development. The remaining question — thread vs bounded module vs Current Case — is exactly the Core-scope decision that requires RFC/Decision.

### 4.5 R5 — Generative AI / agentic coding as current evidence work — CURRENT CASE

Sub-points: (a) generated code/docs/claims as untrusted hypotheses: part of the M00 source-verification habit, with the evidence gates of #16 already in place (each selected lab requires a prediction step and a source/version record); (b) agentic workflows as current practice: a bounded, replaceable case — reading a generated patch, testing a generated claim — reviewed every 6–12 months; (c) code quality: covered by the Software Engineering horizontal thread and #16's observation records.

The durable capability is verification of delegated/generated work; it is already owned by Correctness/Diagnose/Judge/Learn-New-Tech. No new concept; no new Module; no L (L22/L23) change.

### 4.6 R6 — Data modeling, encoding/evolution, provenance, derived data — BOUNDED CORE ADDITION

Sub-points and where each lands:

- **Data modeling / representation boundaries:** M01 `L01-04` (serialization round-trip invariant) + M13 `L13-02` (relational model) already cover it; needs a visible "source-of-truth vs derived" distinction in M13.
- **Encoding/evolution:** M13 `L13-03` extension is the canonical first home — changing fields, readers/writers, migration/backfill choice, failure when representations disagree. Concrete current evidence: Apache Avro reader/writer schema resolution (official spec, live-verified as authoritative specification — cited as evidence, not required product).
- **Provenance (lightweight):** W3C PROV-DM gives a compact, correct vocabulary (entities, activities, agents, derivation, responsibility) — used as conceptual boundary only. A bounded provenance record = where the value came from, which activity produced it, which version/assumptions shaped it. Reused at M19/M23 (dependency/source provenance) and P6/P9 (backup/restore provenance).
- **Derived data:** M18 event/derived-data revisits (queue/stream contexts), P9 scenario judgment; no batch/stream framework.

**Why BOUNDED and not INTEGRATE:** the accepted map's M13 lesson labels do not protect schema evolution/provenance; #15 §8.4 explicitly records this as "needs a reconciliation decision about whether schema evolution receives an explicit Core lesson". This row answers that: yes, as an extension of `L13-03`, no new Module. #14 already narrowed the project side (P6 migrations only when there is an actual evolution need; backup/restore before managed recovery).

**Boundary:** one evolving schema, one derived view, one provenance record in the existing project surface. Exclusions: full PROV ontology, schema-registry operation, every serialization format, exhaustive NoSQL families, data-lake/warehouse architecture, lineage platforms, custom storage engines. Not a Data Engineering specialization (a "data-model decision" is Core; "data platform operations" is not).

### 4.7 R7 — Experimental measurement and diagnosis — INTEGRATE EXISTING CORE

The capability is already a declared horizontal philosophy (`Observe → Hypothesize → Measure → Locate → Explain → Judge`, M04/M20/M23 homes; #15 evidence packet; #16 measurement rule). What remains is to make M04 `L04-02` the **first assessed home** of the pattern (it is currently labeled `FI: performance measurement methodology` but its pattern elements are not enumerated), and to resolve the DAG §6 clock-semantics flag (monotonic vs wall clock) at M20/M23.

**Minimum pattern (for #9 to state once):** question/hypothesis → baseline and expected direction → controlled change → metric, environment, workload, timing semantics → repetitions/distribution where relevant → observation with competing explanation → conclusion limited to evidence (this matches #16 §1.2's measurement rule; no duplication of doctrine is required, just one place where the pattern is named as a Core requirement).

No second Module; no dedicated statistical course; no per-module benchmark requirement. Correlation vs causality is treated as the inference-limit statement, not a formal statistics topic.

### 4.8 R8 — Horizontal security, privacy, accountability, responsibility — INTEGRATE EXISTING CORE

The audit's question is enforcement, not coverage: the current map already distributes first intros (M07 isolation, M11 TLS/data-in-transit/cookies, M12 origin/CORS/CSP, M19 supply chain) with M21/M22 synthesis and M23/M24 judgment; #14 requires a security/privacy decision per project milestone; #15 requires M07/M11/M12 early evidence. The sub-points:

- Early trust boundaries: covered by M07/M11/M12 first intros + P2 early authorization fixture (#14: "a fixed-user authorization fixture is not the pre-canonical security synthesis" — intentionally bounded).
- Privacy/logging: M11 (cookies), M12 (third-party storage), P2/P8 evidence; #14's P8 telemetry redaction rule.
- Supply chain: M19 `L19-03` + M22 `L22-03` (pinning, provenance light).
- Secure composition/failure containment: M22 (composition failures), M20 (incident/containment), M09/M14 (durability boundary).
- Authorization: M22 canonical; P2 integration surface only.
- Human/process/system interaction: routed to R3 (do not silently resolve here — accessibility is *not* counted as resolved by R8; #15 §8 and the audit itself keep it under the HCI Open Question).

**Exclusions:** no penetration-testing track (accepted: CS:APP Attack Lab rejected from Core in #16 candidates; M22 is defense-first safe-target); no jurisdiction law; no OWASP-encyclopedia; no crypto implementation; no formal security proofs.

### 4.9 R9 — Computational models, limits, algorithm–language connection — INTEGRATE EXISTING CORE

Sub-points: (a) intuitive model-of-computation and expressibility/tractability boundary → M02; (b) why some problems are hard/impossible (decidability intuition) → M02, kept intuitive; (c) algorithm–language/runtime connection → M05 (source→IR→runtime→machine) and `L05-03` (types as invariants). The distinctive teaching goal: represent a problem correctly, then state why an apparent solution changes cost or expressibility.

The audit's own §8 classifies the full theory portfolio as DEEP DIVE and the applied boundary as Core. #1 already gives M02 and M05 the required roles; #15 guards M05 against vocabulary-only assessment. No new concept IDs. Confirmed no DAG change needed (M01/M02→M03→M05 chain already correct).

### 4.10 R10 — Consensus as Core concept — INTEGRATE EXISTING CORE

Sub-points: (a) why coordination is hard (partial failure, ambiguity): M16 `L16-01` already first-introduces partial failure; (b) what consensus buys/costs: M17 `L17-02`; (c) when replication/consistency choices apply: M17 `L17-03`, M18, M23/M24; (d) the Audit's caution that full implementation is expensive: routed to R11 (DEEP DIVE) rather than weakening the concept.

The Core boundary is: demonstrate concept — a worked leader/follower trace, a partition scenario, a consistency trade-off judgment. #16's Lab map keeps M17 as an "Adopt/Adapt small three-node observation or case analysis only after #4 and #9 resolve the Core boundary" — i.e., the lab decision is still open but the concept is already Core. No implementation is required for M17 exit. This row therefore confirms the existing structure; it does not add material.

### 4.11 R11 — Full consensus implementation — DEEP DIVE

Both sub-points (formal algorithms/proofs; replicated-service implementation) belong here. Evidence: MIT 6.5840 is a graduate prerequisite-heavy course (audit §7.2, live course comparison 2026); Berkeley CS186's Paxos appears within a much broader DB course. Candidate home: optional S6 Source Expedition coordinated with #16's Lab map (which defers "full Raft/Paxos implementation is Deep Dive"). Explicit stopping point: one algorithm's specification, compared with the Core mental model.

### 4.12 R12 — Physical, embedded, real-time case — DEEP DIVE (pending evidence)

Sub-points: (a) resource/deadline/sensor boundaries — a small case could strengthen Observe/Explain/Judge/Estimate; (b) platform/toolchain breadth — hardware dependency, board procurement, firmware breadth, real-time scheduling theory are the excluded cost. The audit marks this Medium confidence and its §8 class keeps only "a small physical/resource-constrained case if it improves the shared system model". #14's R12 row: "Deep Dive pending evidence; no P0–P9 dependency or feature". No evidence yet shows the common traversal improves enough to justify setup cost; the current abstract machine model suffices for Core pending learner validation.

### 4.13 R13 — Cloud/orchestration product breadth — CURRENT CASE

Sub-points: (a) stable infrastructure mechanisms (isolation, packaging, deployment, observability, supply chain, resource economics, reproducibility) → stay Core in M19/M20 — these are already in the accepted map and lab structure; (b) product names / vendor commands (Kubernetes, service mesh, Terraform, one cloud provider, specific CI) → replaceable CURRENT CASE via the Technology Evaluation Framework (D-015) and admitted only through the Technology Admission Test (already done in #14: container = optional P7 comparison; orchestration = not canonical); (c) certification/ops mastery → Deep Dive (/job-specific).

The recommendation is precisely about the risk that products consume Core attention; the disposition is to keep the mechanism/principle Core and the product replaceable — which the merged artifacts (#14 admission table, #16 M19 optional container comparison, #15 M19 guardrail "do not turn the module into Docker or Kubernetes certification") already implement. If the current case product disappears, M19's lesson survives because it teaches namespaces/cgroups/images/artifacts/deployment semantics.

### 4.14 R14 — Full kernel/protocol-stack/compiler/DB-engine projects — DEEP DIVE with small Adopt/Adapt/Build slices

Sub-points: (a) OS kernel construction (xv6 full) → the accepted #16 map adapts only the user-level `sleep` syscall trace (LAB-REQ-02) and keeps xv6 course-page licensing scoped separately; (b) full network stack (CS144 TCP) → not selected as Required in #16 (CS144 remains an optional/source/adapt candidate; RFC 9110 trace LAB-REQ-01 is the adopted HTTP mechanism case); (c) compiler construction → M05 pipeline only; Nand2Tetris stays a Deep Dive / optional excursion (map §9); (d) DB-engine implementation (BusTub/SimpleDB/RookieDB) → not adopted; #16 builds SQLite-based mechanism labs (LAB-REQ-04/05) where course projects are rights-blocked or course-sized.

**Why the disposition is DEEP DIVE even though Core contains small slices:** the *slices* are already the accepted Core hands-on selection (see #16); this row's subject is the full-implementation *recommendation*, which belongs after the shared model. #9 must not re-expand the small slices into complete builds, and must not bundle any third-party material while its license remains unresolved (explicit in #16 decisions).

### 4.15 R15 — Quantum and specialist inventories — REJECT

Sub-points: (a) quantum computing/architecture: no demonstrated dependency on the shared Map→representation→machine→OS→network→data→distributed→judgment chain; CS2023 places it in non-required specialist material (live-verified report component index); (b) "other specialist topic inventories": included by the recommendation's own phrasing — the rebuttal is the same: no concrete cross-cutting capability; (c) novelty/tradition expansion risk: protected by Invariant 8 (complexity must justify itself), Invariant 9 (complete shared model), Invariant 10 (modern does not mean trendy).

Rejection is of v0.1 Core and of the project path; it is not a content veto — an interested learner can be routed to a Deep Dive reading list. Reopen condition: an Open Question → RFC with a concrete cross-cutting dependency and a bloat trade-off.

## 5. Core additions / integrations summary (non-escalated)

| Area | Disposition | Stage | Module / Lesson | Thread(s) | New? |
|---|---|---|---|---|---|
| Applied MSF toolkit | BOUNDED CORE ADDITION (R1) | S1 + S2 | M02 `L02-01` discrete/asymptotic (strengthen existing); **M04 `L04-02` first statistical/uncertainty home (new canonical material)** | Measurement & Performance; Napkin Math; (new) applied-uncertainty pattern | Partially new: M04 home; rest is explicit outcomes |
| Toolchain / reproducibility | INTEGRATE EXISTING CORE (R2) | S1 | M00 `L00-02` (make explicit); lab-entry gate; environment preflight at M03/M06 | Technical Literacy; Software Engineering; Debugging | Explicit outcomes + gate only |
| Schema evolution / provenance / derived data | BOUNDED CORE ADDITION (R6) | S5 | M13 `L13-03` (extend); revisits M01/M16/M18/M19/M23 | Correctness & Invariants; API/Interface Design; Learn-New-Tech; Privacy | New canonical material only inside M13 |
| Experimental measurement pattern | INTEGRATE EXISTING CORE (R7) | S2/S6/S7 | M04 `L04-02` first assessed; M20 `L20-01`; M23 `L23-01` | Measurement & Performance; Diagnosis; Napkin Math | Pattern enumerated, no new Module |
| Security/privacy horizontal evidence | INTEGRATE EXISTING CORE (R8) | S3/S4/S6/S7 | M07 `L07-01`; M11 `L11-01`; M12 `L12-03`; M19 `L19-03`; M21–M24; P0–P9 evidence rules | Security; Privacy/Data Responsibility; Correctness | Evidence enforcement only |
| Computational models/limits | INTEGRATE EXISTING CORE (R9) | S1/S2 | M02 `L02-01..03`; M05 `L05-01..03` | Correctness; Judge; Learn-New-Tech | Outcome explicitness only |
| Consensus concept | INTEGRATE EXISTING CORE (R10) | S6 | M17 `L17-01..03` (already first-home structure) | Failure; Correctness; Judge | Confirmation + lab boundary, no new material |
| Cloud/orchestration stable mechanisms | CURRENT CASE core retention (R13) | S6 | M19 `L19-01..03`; M20 | Cost; Failure; Learn-New-Tech; Technical Literacy | Case replacement discipline only |
| AI-generated output verification | CURRENT CASE (R5) | S1/S7 | M00 `L00-02`; M23 `L23-02`; source-verification policy | Learn-New-Tech; Correctness; Judge | Replaceable case + policy |
| HCI/accessibility | ESCALATION (R3) | — | Provisional (P2/P9 evidence hooks already exist) | — | Blocked pending RFC |
| AI literacy | ESCALATION (R4) | — | Provisional | — | Blocked pending RFC |

## 6. Architecture escalations

### 6.1 R3 — Bounded human-facing system boundary

- **Proposed Open Question:** the existing `OQ-BP-003` ("What bounded human-facing system boundary belongs in Core?") — this proposal adds framing: "Does an explicit Core requirement for user goals, feedback/error recovery, accessibility (keyboard/assistive-technology awareness), consent/privacy interaction, and human-facing failure belong in the first shared traversal, and where is the one canonical first home?"
- **Why ordinary integration is insufficient:** accepting would change what counts as a "complete shared modern-system world model" (Invariant 1, 9), adding an explicit human-facing dimension absent from the macro spine; rejecting outright would ignore a genuine gap in modern-system judgment (the audit, and W3C's framing that accessibility is a system property requiring knowledgeable human evaluation). Neither choice is a local placement decision.
- **Options:** (A) spiral — M00 boundary vocabulary + M12 browser mechanics + P2/P9 evidence hooks + M23/M24 judgment; (B) one bounded M12 module with the browser visible interface; (C) project/journal-rubric only (current state via #14 P2/P9 hooks, no Core admission); (D) CURRENT CASE only.
- **Evidence:** W3C [Introduction to Web Accessibility](https://www.w3.org/WAI/fundamentals/accessibility-intro/) (live-checked 2026-08-30; accessibility = perceive/understand/navigate/interact) and [Evaluating Web Accessibility](https://www.w3.org/WAI/test-evaluate/) (tools assist but cannot alone determine accessibility; human evaluation required). These support a bounded system-boundary competency; they do not determine Core scope.
- **RFC need:** lightweight RFC (Open Question + targeted research + decision record), proceeding through Invariant 19 architecture process. A full RFC is warranted because the choice changes Core scope.
- **Integration state:** NOT blocked for #9's other work — #14's P2/P9 evidence hooks and #15's "no canonical IDs" stance are interim-safe and do not harden a premature decision.

### 6.2 R4 — Bounded AI literacy / data-model judgment

- **Proposed Open Question:** the existing `OQ-BP-001` with this framing: "For a 2026 systems-world curriculum, should bounded AI-output verification / technical literacy be (A) a named Core thread spiraled through M02/M13/M20/M21/M23, (B) one bounded M23 technology-judgment module, (C) a CURRENT CASE only, or (D) both A and C (stable literacy thread + replaceable-tool case)?" The stable capability to decide on: problem suitability vs data vs model vs evaluation vs interface vs system failure; reading a bounded evaluation; resource/cost and privacy/security implications; and explicit when-not-to-use reasoning.
- **Why ordinary integration is insufficient:** this is the single sensitivity item. The project Decision explicitly states AI/LLM is not automatically a Core topic, yet the audit (High confidence) finds a real modern-world-model gap, and #14/#15 deliberately left the Core answer unresolved while routing AI-claim verification to the CURRENT CASE pattern. Deciding it in a disposition table would silently expand Core; rejecting it would silently drop a reported coverage gap.
- **Options:** (A) Core thread (justification: the gap is cross-system judgment, not a product); (B) bounded M23 module (justification: one first home, minimal new material, judgment synthesis already exists there); (C) CURRENT CASE only (justification: tools decay; the verification habit is already taught); (D) A + C combination. Evidence to weigh: CS2023's explicit basic-AI-literacy goal (report component, live-verified) vs the Invariants (10: modern does not mean trendy; 8: complexity must justify itself) and the learner profile (no ML prerequisite).
- **Evidence:** live-verified CS2023 final report generator; NIST [AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) (live-checked: AI RMF 1.0 (Jan 2023), GenAI Profile NIST-AI-600-1 (Jul 2024), AI RMF 1.0 being revised as of 2026-04; concept note on critical-infrastructure profile 2026-04-07) and [AI Resource Center](https://airc.nist.gov/). NIST evidence supports *system/risk judgment* vocabulary (trustworthiness, measurement, risk), not a specific Core curriculum shape; the detailed framework content was not needed to inspect beyond the overview for this proposal.
- **RFC need:** required — this is Core-scope; an RFC should specify the stable learner capability, first home, evidence artifact, review cadence, and explicit exclusions before any canonical map or Registry change. Interim safe pattern (already accepted in #15): generated claims as untrusted hypotheses verified by source/test/measurement/security review.
- **Integration state:** NOT blocked — existing M23 technology-judgment module and the CURRENT CASE verification pattern provisionally cover the practical need without expanding Core.

## 7. Dependency and first-introduction impact

**Rule kept:** the Module DAG (`dependency-graph-v0.1.md`, corrected semantics) is authoritative; no new H edge, no Stage reorder, no S4/S5 relabel. The default narrative S1→S2→S3→(S4|S5)→S6→S7 remains a preference, not a hard chain; M14→M16 soft, M14→M17 hard, per the corrected graph (as recorded in PROJECT_STATUS).

| Proposed teaching point | Edge effect | Type |
|---|---|---|
| M04 `L04-02` statistical-lite bridge | none (inside existing M04; M03→M04 H already in place) | preview at M04; canonical M04; revisits M13/M16/M17/M19/M20/M23 |
| M02 `L02-01` counting/asymptotics reinforcement | none (already in M02) | canonical (existing) |
| M00 `L00-02` investigation loop + lab gate | none — gate is a course/lab discipline requirement, not a DAG edge; elevate per DAG §6 | first introduction; required for all REQUIRED labs |
| M13 `L13-03` schema evolution + provenance extension | none (M08/M09→M13 H already) | canonical for schema evolution; M16 compatibility is a revisit (not new first-home); M18 derived data revisit; M19/M23 provenance revisits |
| M23 measurement methodology | none (M20/M21→M23 H existing) | consolidation, not first intro |
| R3 provisional M00/M12 placement | none until RFC decides; must not create hidden prerequisite for M23/M24 | preview-if-admitted |
| R4 provisional M02/M13/M23 placement | none until RFC; must not create ML/math prerequisite | preview-if-admitted; candidates use existing edges |
| M17 consensus concept | existing edges only (M16→M17 H; M14→M17 H; M09→M17 S) | first intro M17; no implementation prerequisite |
| M19 stable mechanisms | existing edges (M06/M07/M08/M16→M19 H; M19→M20 H) | canonical as designed; product case evaluated via Technology Admission Test |

**First-introduction summary:** one genuinely new canonical first home proposed (M04 for statistical/uncertainty literacy); one extended canonical first home (M13 `L13-03` for schema evolution/representation compatibility); everything else is explicitness, evidence, or revisits. No proposed addition forces a new hard prerequisite, creates a cycle, or reorders any Module. If a future RFC admits R3/R4, only then are first homes for those concepts assigned — and those first-home decisions must be re-reviewed against the final DAG.

## 8. Competency impact

| Recommendation | Trace | Explain | Observe | Diagnose | Correctness | Judge | Estimate | Learn-New-Tech | Weak-justification flag |
|---|---|---|---|---|---|---|---|---|---|
| R1 MSF | | ● | | ● | ● | ● | ● | | none |
| R2 Toolchain | | ● | ● | ● | ●(evidence) | | | ● | none |
| R3 HCI (conditional) | ● | ● | | ● | ● | ● | | | must clear RFC; evidence hooks currently claim no competency mandate |
| R4 AI literacy (conditional) | | ● | | ● | | ● | ● | ● | must clear RFC; same caution |
| R5 AI verification | | ● | | ● | ● | ● | | ● | none (current case) |
| R6 Data evolution/provenance | ● | | | ● | ● | ● | | ● | none |
| R7 Measurement | | ● | ● | ● | | | ● | | none |
| R8 Security/privacy | ● | | | ● | ● | ● | | | none |
| R9 Models/limits | | ● | | | ● | ● | | ● | none |
| R10 Consensus | ● | ● | | ● | | ● | | | none |
| R11 Consensus impl. (DD) | ● (depth) | | | ● (depth) | ● (depth) | ● (depth) | | | Deep Dive — no Core claim |
| R12 Physical case (DD) | | ● | ● | | | ● | ● | | Deep Dive pending evidence — no Core claim |
| R13 Cloud products | | ● | | ● | | ● | ● | ● | stable-mechanism side strong; product side is Current Case |
| R14 Full projects (DD) | ● (slices) | | ● | ● | ● | ● | | | Deep Dive; slices already selected by #16 |
| R15 Quantum | — | — | — | — | — | — | — | — | not admitted; no competency claim |

**No Core admission is made without a named competency.** The flag column shows the two escalations (R3/R4) plus the deep-dive rows where competency claims are depth-only; none of them is being added to Core by this proposal. The only non-escalated row needing the closest #9 attention for competency evidence is R1 (M04 must produce an evidence artifact with a stated inference limit, matching #15's evidence-packet rules) and R6 (schema-evolution reasoning must produce a trace of a reader/writer mismatch or migration decision, not vocabulary).

## 9. Bloat-control / exclusions (what is NOT being added)

- **Mathematics:** no discrete-math, calculus, statistics, or linear-algebra course; no proof portfolio; no "math gate" before M01. Only the M04 measurement-uncertainty bridge + in-context estimation.
- **Tooling:** no Linux-commands encyclopedia; no shell-implementation or Git-internals course; no comprehensive build-system survey; no team-Agile ceremony; no vendor CI/DevOps syllabus.
- **HCI:** no UX-research method sequence; no visual/interaction design instruction; no design-system or WCAG-exhaustive training; no accessibility law survey. (If admitted: one bounded human-evaluation checkpoint.)
- **AI:** no ML/LLM architecture module; no linear algebra/gradient math; no training-infrastructure lesson; no prompt-engineering catalog; no model-vendor survey; no autonomous-agent operations; no AI product development. (If admitted: bounded verification/judgment capability only.)
- **Data:** no data-engineering pipeline course; no PROV ontology; no schema-registry operations; no lineage platform; no data-lake platform catalog; no NoSQL family survey; no stream/event-framework training; no storage-engine implementation.
- **Security:** no penetration-testing / exploit-development track; no crypto implementation; no legal/compliance curriculum; no vulnerability catalog; no certification prep.
- **Distributed/infrastructure:** no required Raft/Paxos implementation; no Kubernetes administration; no service mesh; no cloud-provider certification; no mandatory cloud account/model; no mandatory queue/broker/product in the project (per #14 admission table).
- **Implementation projects:** no full kernel, full TCP/IP stack, full compiler, or full DB engine; no Nand2Tetris completion in Core; no bundled third-party lab text/code while license is unresolved; no per-Module benchmark requirement.
- **Specialist inventories:** no quantum, FPGA/robotics/platform-track, graphics/animation, or embedded breadth.

## 10. Reconciliation with merged #14/#15/#16 (Issues #11/#13/#12)

These artifacts were merged after Issue #10 was created; the dispositions above were decided *with* them, so several recommendations are already partly solved. For each, what was already accepted and what remains:

| Rec. | Already accepted (point to artifact) | Still open for #9 |
|---|---|---|
| R1 | #15 §5.1/§8.3: applied-statistics/uncertainty is a competency requirement, no Registry IDs; evaluate via Estimate/Diagnose evidence. #14 §7 R1: "just-in-time horizontal toolkit, not standalone prerequisite"; P4/P8/M23 uncertainty expectations. #16 §1.2: measurement rule requires distribution/repetition/limits in every measuring lab. | Explicit first home (this proposal: M04 `L04-02`), minimum toolkit content, and assessment wording. OQ-BP-002 remains. |
| R2 | #15 §2 S1 "tool fluency … explicit lab prerequisite"; §5.2 "M05–M06 need an applied toolchain bridge". #16: every lab lists M00 shell/Git/reset prerequisite. #14 P7 native reproducibility. | Explicit learner outcome sentences and the lab-entry gate wording. |
| R3 | #14 §7 R3: bounded user-facing checks at P2/P9; OQ-BP-003 preserved; no Web syllabus invented. #15 §8.2: no HCI/accessibility/consent IDs; M12/M22/P2 evidence conditional. | Core-scope decision (RFC), canonical first home if admitted. |
| R4 | #14 §7 R4: Core placement not decided in project artifact; AI claims as CURRENT CASE. #15 §8.1: no AI IDs; safe interim pattern named. | Core thread vs module vs Current Case (RFC). |
| R5 | #14 §7 R5: "any generated code/config/claim is an untrusted hypothesis checked by source, test, measurement, and security review" — integrated into tool/source-verification policy. | Review cadence + one or two chooseable bounded tasks; content of the M00/M23 case. |
| R6 | #14 §7 R6: integrate into M01/M13/M14/M16 + P0/P4/P6/P9; P6 migrations only with real need; backup-before-managed. #15 §8.4: reconciliation decision explicitly requested; no IDs assigned yet. #16 LAB-REQ-05: real SQLite transaction/isolation/rollback/recovery evidence exists. | This proposal answers #15's "first home and revisit path": M13 `L13-03`. |
| R7 | #15 §5.3 assessment architecture (evidence packet: prediction, observation, explanation, invariant/uncertainty, judgment) + #16 §1.2 measurement rule. | Enumerate the pattern at M04 as first assessed home; resolve clock-semantics flag (DAG §6) at M20/M23. |
| R8 | #14 §7 R8: horizontal evidence required at P0–P9 (data minimization, telemetry redaction, backups, provenance); #15 stage evidence gates. | No material work beyond #9's transcription into map/DoD. Accessibility remains external (R3). |
| R9 | #15 §3 M05 guardrail + M02 canonical Specification/Invariant/Correctness homes. | Outcome sentences for the limits/expressibility intuition at M02; no Registry IDs needed. |
| R10 | #15 §8.5: Consensus/Replication deferred as IDs until #4/#9 boundary; #16: M17 stays concept/observation; full Raft Deep Dive. | Lab boundary: whether an optional small 3-node observation becomes a selected lab (already deferred to #16/#9; not required by this row). |
| R11 | #16: "full Raft/Paxos implementation is Deep Dive"; #15 deferral; #14 R11 row. | None beyond coordination with final Lab map. |
| R12 | #14 §7 R12: Deep Dive pending evidence; no P0–P9 dependency. | None beyond learner-validation evidence trigger. |
| R13 | #14 Technology Admission section: container optional/project P7 comparison; Kubernetes/orchestration/service-mesh not canonical; #15 M19 guardrail. | Choose the one replaceable product case when the Technology Admission Test is run; keep it removable. |
| R14 | #16: 5 Required (LAB-REQ-01 HTTP/RFC trace, LAB-REQ-02 xv6 `sleep`, LAB-REQ-03 POSIX threads Build, LAB-REQ-04/05 SQLite Build), 5 Optional, 5 Source Expeditions; Attack Lab rejected; xv6 page license scoped separately from MIT-licensed software. | Complete-implementation Deep Dives remain for #4/#9 final map; license/version pinning continues. |
| R15 | #14 §7 R15: reject from v0.1 Core/project path. | Only an RFC with a demonstrated cross-cutting dependency reopens it. |

**Two places where the merged artifacts deliberately left architecture unresolved and this proposal preserves that:** (1) #15's proposal of 18 provisional concepts (15 Big Ideas + Process, Durability, Trust Boundary) is a proposal needing #9 acceptance — nothing in this document adds IDs or presumes that population; (2) #15's "M05 vocabulary risk", "M18 queue evidence", "M21–M22 distinction" guardrails are preserved as #9 review items, not overridden here.

## 11. Recommended Issue #9 actions (checklist for the integrator)

1. **Accept the dispositions** except where the two escalations (R3, R4) are rerouted to the Open Question → RFC → Decision path. Carry R3 → `OQ-BP-003`, R4 → `OQ-BP-001`, with the framing and options from §6.
2. **Add the M04 `L04-02` applied-uncertainty bridge** (R1) as the canonical first home of the statistical/measured-variation toolkit; keep M23 as consolidation. Do not add a math Module or a math prerequisite.
3. **Write the M00 `L00-02` explicit outcomes + REQUIRED-lab entry gate** (R2); record lab-entry discipline in the Lab Map/DoD; keep tooling out of the Concept Registry.
4. **Extend M13 `L13-03`** to schema evolution, reader/writer compatibility, source-of-truth vs derived, and one lightweight provenance record (R6); confirm M16/M18/M19/M23 remain revisits.
5. **State the R7 evidence pattern once** (M04 first assessed home; M20; M23 consolidation) and resolve the DAG §6 clock-semantics flag in the measurement lesson(s).
6. **Transcribe R8 horizontal evidence requirements** into Stage/Module/DoD wording; do NOT treat accessibility as resolved by security (R3 owns it).
7. **Confirm R9/R10 need no new material** — M02/M05 (models/limits) and M17 (concept) already own them; keep R11/R12/R14 in Deep Dive/optional per #16; keep R15 excluded.
8. **Keep R5 and R13 as CURRENT CASE discipline** (source-verification policy; Technology Admission Test record; removable product case); no product names in the Concept Registry.
9. **Do not re-expand #16's Lab selection** — the small-slice design (LAB-REQ-01..05 + optional + Source Expeditions) is the accepted Shape; this matrix adds no Labs.
10. **Preserve the corrected DAG** (S4/S5 partial independence; M14→M16 soft, M14→M17 hard; no S4→S5 Stage edge) while finalizing the S4/S5 narrative per `OQ-BP-004`.
11. **Re-run R1–R15 once more against the final reconciled maps** immediately before any canonical file edit (cheap consistency check).
12. **No lesson, lab, project, or Registry bulk writing in this step** — the above are architecture/outcome dispositions only.

## 12. Completion Report

### Status

`READY FOR LEAD REVIEW` (not `VERIFIED`; not merged; no canonical file changed).

### Deliverable

`meta/blueprint/audit-to-architecture-disposition-v0.1.md` — disposition matrix + detailed rationale + reconciliations for R1–R15.

### Files changed

- `meta/blueprint/audit-to-architecture-disposition-v0.1.md` (only file; see Git verification below).

No canonical file (Curriculum Map, Competency Matrix, Concept Registry, Decisions, Open Questions, Project Status, Curriculum Invariants, dependency graph, Stage/Module/Lesson proposal, Mini Cloud App maps, Lab/Source Selection Map) was modified.

### Disposition counts (total = 15)

- INTEGRATE EXISTING CORE: **5** (R2, R7, R8, R9, R10)
- BOUNDED CORE ADDITION: **2** (R1, R6)
- CURRENT CASE: **2** (R5, R13)
- DEEP DIVE: **3** (R11, R12, R14)
- REJECT: **1** (R15)
- ARCHITECTURE ESCALATION: **2** (R3, R4)

### Architecture escalations

1. **R3 — bounded human-facing system boundary** (user goals/mental models, feedback/error recovery, accessibility, consent/privacy interaction, human-facing failure). Open Question: `OQ-BP-003`. Options: M00-anchored spiral / bounded M12 module / project rubric only (current) / CURRENT CASE. RFC: lightweight but Core-scope. Integration: not blocked; P2/P9 evidence hooks already accepted.
2. **R4 — bounded AI literacy & data/model judgment.** Open Question: `OQ-BP-001`. Options: Core thread / bounded M23 module / CURRENT CASE only / thread + case. RFC: required. Integration: not blocked; verification-of-claims pattern already accepted as CURRENT CASE.

### Most important proposed Core changes

1. M04 `L04-02` becomes the canonical first home of the applied measurement-uncertainty toolkit (R1) — the only genuinely new canonical first-introduction.
2. M13 `L13-03` extended to schema evolution / representation compatibility / source-of-truth and derived data / lightweight provenance (R6).
3. M00 `L00-02` + a lab-entry gate make tooling/reproducibility an explicit, assessed prerequisite discipline (R2) — explicitness, not new Module.
4. R7's experiment pattern enumerated once at M04 and consolidated at M23 (assessment reinforcement).
5. R8 horizontal security/privacy evidence transcribed into Stage/Module/DoD wording (enforcement, no new Module).

### Recommendations already resolved by #14/#15/#16

- R2 was moved from "at risk" to "mostly solved" by #15 (explicit lab prerequisite; toolchain bridge) and #16 (lab prerequisites in every selected LAB). Remaining: outcome sentences + gate.
- R7 was largely solved by #15 (evidence packet, §5.3) and #16 (measurement rule, §1.2). Remaining: M04 first-home enumeration + clock-semantics flag.
- R8 was largely solved by #14 (per-milestone security/privacy decisions; telemetry redaction; P0–P9 evidence) and #15 (stage evidence gates). Remaining: transcription.
- R10's Core concept and R11's Deep Dive boundary were fixed by #16's M17 wording; #15 deferred the Consensus Registry ID.
- R13 was solved by #14's Technology Admission table (container optional; orchestration not canonical) and #15's M19 guardrail.
- R14 was solved by #16's selection map (small slices only; Attack Lab rejected; xv6 licensing scoping).
- R15 was solved by #14's R15 row.
- R3/R4 evidence hooks were added by #14/#15 but the Core decision was deliberately left open — retained as escalations by this proposal.

### Dependency impacts

None on the authoritative DAG. No new H edge, no cycle, no Stage reorder, no S4→S5 relabel. The only "prerequisite" change is the lab-entry gate discipline (course-level, by design not a DAG edge) and the DAG §6 clock-semantics flag resolution point (M20/M23).

### Research verification (live checks 2026-08-30)

- MIT Missing Semester 2026 index (shell, dev tools, debugging/profiling, Git, packaging, agentic coding, code quality) + Agentic Coding / Code Quality lecture pages.
- W3C Introduction to Web Accessibility (updated 3 Feb 2026) — accessibility = perceive/understand/navigate/interact; W3C evaluating page — no single tool determines accessibility.
- W3C PROV-DM (W3C Recommendation, 30 Apr 2013) — entities/activities/agents/derivation/responsibility, core vs extended structures.
- Python `time` documentation (3.14.7, current 2026-08-30) — monotonic vs `time()` wall clock vs `perf_counter`.
- CS2023 Final Report component index (Executive Summary, Knowledge Model, Body of Knowledge, Competency Framework, Pedagogical Considerations, Generative AI and the Curriculum).
- NIST AI Risk Management Framework page (AI RMF 1.0 Jan 2023; GenAI Profile NIST-AI-600-1 Jul 2024; 1.0 under revision; critical-infrastructure concept note 2026-04-07) + AI Resource Center.
- NIST measurement-uncertainty topic page (concept framing; not quoted verbatim).
- Secondary (used via the audit and accepted artifacts, not re-fetched as primary): Apache Avro specification (R6 evidence), CMU 15-213 / MIT 6.1810 / 6.5840 / Stanford CS144 / UC Berkeley CS186 course pages (audit §2.3, 2026-08-30 — contained in the audit's own provenance register).

### Assumptions

1. Current `origin/main` (`3d53caa`) is the correct baseline; merged #14/#15/#16 artifacts are complete through the date above.
2. The audit's R1–R15 table (`external-curriculum-audit-v0.1.md`, §9) is the authoritative recommendation set; the audit's `RECHECK-AFTER-ISSUE-1` markings are all resolved here against current artifacts.
3. "Core" means the first shared Essential CS traversal with complete shared world model (Invariant 9), not degree-equivalent coverage.
4. Module/Lesson ID references are proposal-level anchors for #9, not locked lesson names or IDs.
5. M17's Lab boundary (small 3-node observation vs case analysis) remains a #9/#16 decision; this matrix does not select a Lab.
6. The 18-concept Registry proposal (#15) remains a proposal; this document adds no IDs and presumes none accepted.
7. Current claims beyond the verified list above are attributed to the audit's live register dated 2026-08-30.

### Open questions

- OQ-BP-001 (bounded AI literacy placement) and OQ-BP-003 (human-facing boundary) — carried with RFC framing from §6.
- OQ-BP-002 (applied foundations/toolchain first homes and depth) — this matrix recommends M04 + M00-L gate; Lead confirms.
- OQ-BP-004 (S4/S5 narrative) — unaffected; recommendation is to preserve partial independence.
- OQ-BP-005 (final lab adoption details) — belongs to #16/#9; this matrix adds none.
- OQ-BP-006 (environment versions) — untouched; pinning deferred to dossier/lab implementation.
- Whether the M04 statistical bridge should also carry a percentile-of-latency vocabulary — flagged for #9 (leans yes, as application, not new theory).

### Prompt deviations

None.

### Out-of-scope necessary fixes

None. (The pre-existing untracked copy of this document was based on pre-merge `origin/main`; it was replaced in full by this version, which is the only change made.)

### Recommended #9 integrator review focus

1. **R1 vs R4 boundary:** confirm that adding the M04 uncertainty bridge does not drift into probability-course territory, and that the AI literacy disposition (RFC-gated) stays separate — Do not let "AI" become a synonym for "modern".
2. **R3 decision risk:** is a human-facing boundary a *Core requirement*, or is the #14 P2/P9 evidence sufficient for v0.1? Whichever the Lead picks, the first-home placement needs one canonical explanation to honor Invariant 11.
3. **R2 gate:** does a REQUIRED-lab entry gate conflict with the self-study-first invariant (D-014/Invariant 14)? The recommendation: gate = evidence preservation, not a third-party course sequence — please scrutinize the absence of a required "environment course".
4. **R6 scope:** does the M13 `L13-03` extension risk becoming "schema-registry training"? The boundary stated (one evolving schema + one derived view) should be enforced at design time.
5. **Lab-size check:** this matrix enumerates no Labs; if any disposal seems to require a Lab, it should be resolved by #16's map — flag any conflict back here.
6. **Concept Registry hygiene:** confirm no product name, command, or ephemeral framework ID slips in due to R5/R13 example material.
7. **DAG audit:** re-run the acyclic check after any first-home acceptance (especially if the R1 bridge lands in M04 and M23 consolidation changes — intra-Stage only, should stay acyclic).
