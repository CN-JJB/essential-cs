# External Curriculum Coverage Audit v0.1

**Task:** Issue #2 — External Curriculum Coverage Audit v0.1
**Status:** READY FOR WEB LEAD REVIEW (not `VERIFIED`)
**Audit date:** 2026-08-30
**Repository snapshot:** `origin/main` at `7d67fd359130c97a7bf88308e22063497901b662`
**Scope owner:** Independent Curriculum Coverage Auditor; no concept or curriculum ownership claimed

GitHub status snapshot: [Issue #2](https://github.com/CN-JJB/essential-cs/issues/2) and Issues [#1](https://github.com/CN-JJB/essential-cs/issues/1), [#3](https://github.com/CN-JJB/essential-cs/issues/3), and [#4](https://github.com/CN-JJB/essential-cs/issues/4) were open on the audit date; the [pull-request list](https://github.com/CN-JJB/essential-cs/pulls) was empty when checked.

## 1. Audit scope and method

### Scope

This audit compares the current Essential CS **macro blueprint** with authoritative/comprehensive curriculum references and strong teaching traditions. The current repository contains a coarse Curriculum Map, Competency Matrix, Concept Registry structure, and governance policies; it does not yet contain the detailed Stage/Module/Lesson map from Issue #1.

The audit therefore makes two kinds of finding:

- **Macro-level finding:** a conclusion that can be justified from the current spine or horizontal-thread declarations.
- **Fine-grained finding:** a placement, dependency, or depth question that must be rechecked after Issue #1; these are marked `RECHECK-AFTER-ISSUE-1`.

This is not:

- an accreditation or degree-equivalence audit;
- a mechanical count of course titles or textbook chapters;
- a replacement for module Research Dossiers;
- final lab/source curation (Issue #4);
- Mini Cloud App design (Issue #3);
- a curriculum rewrite.

CS2023 is used as a reference model, not as a mandatory syllabus. Its CS Core / KA Core distinction, recommended hours, and knowledge areas are evidence about breadth and educational dependencies; they do not override Essential CS's stated goal of a complete shared modern-system world model without undergraduate-degree compression.

### Method

Each reference was normalized into five comparable layers:

1. **Concepts:** state, representation, abstraction, indirection, locality, caching, concurrency, isolation, consistency, failure, interface, correctness, invariants, specifications, and trade-offs.
2. **Mechanisms:** the transformations and control surfaces that make a system work, such as address translation, scheduling, indexing, retransmission, recovery, replication, query planning, and compilation.
3. **Competencies:** what the learner can do: Trace, Explain, Observe, Diagnose, Correctness, Judge, Estimate, and Learn-New-Tech. The audit also checks the CS2023 skill verbs Explain / Apply / Evaluate / Develop and professional dispositions.
4. **Systems capabilities:** following data/control/state, managing resources, handling failure, establishing trust, interoperating across interfaces, and operating a system over time.
5. **Recurring engineering judgments:** where time/data/state goes; what can fail; how to know; what must remain true; what complexity/cost is being moved; and at what scale a choice becomes worthwhile.

Course pages and labs were examined for actual topics, sequence, projects, writeups, and learning activities. A course title alone was not treated as evidence. Textbooks were used to identify durable conceptual dependencies and mechanisms, not to import every chapter into Core. Teaching projects were used to detect mechanism-level learning that a topic list can miss.

### Recommendation classes

Every material recommendation uses exactly one class:

- **CORE** — required for the first shared traversal or for a horizontal competency that every learner needs.
- **CURRENT CASE** — a current technology/practice used to expose a stable principle, with bounded scope and review.
- **DEEP DIVE** — valuable depth, implementation, formalism, or specialization after the shared model.
- **REJECT** — should not enter this curriculum's Core or is not justified for the stated goal.

Confidence means confidence in the audit finding, not confidence that the final architecture choice has already been made.

## 2. Reference set and provenance

All web resources below were checked or access-attempted on 2026-08-30; access caveats are stated where relevant. No third-party prose, diagrams, code, or lab solution was incorporated into this audit.

### 2.1 ACM / IEEE-CS / AAAI CS2023

| ID | Resource and publication state | Authoritative reference | Why selected / comparison claim |
|---|---|---|---|
| CS23-EXEC | *Computer Science Curricula 2023: Executive Summary*, official Final Report component. The official cover identifies the Final Report as **January 2024, Version 2024-04-28**. The report describes the Body of Knowledge as revised to 17 knowledge areas, with CS Core deliberately circumscribed and KA Core used for deeper study. | [CS2023 Final Report](https://csed.acm.org/final-report/); [Executive Summary PDF](https://csed.acm.org/wp-content/uploads/2024/04/1.1-Executive-Summary.pdf); [Official cover/version PDF](https://csed.acm.org/wp-content/uploads/2024/04/0.-Cover-Page.pdf) | Establishes the current authoritative framing and cautions against treating a traditional degree inventory as a single required Core. |
| CS23-KM | *Introduction to Knowledge Model*, official Final Report component. It defines CS Core, KA Core, Non-core, the 17 knowledge areas, cross-cutting SEP/MSF, competency areas, and recommended—not prescriptive—skill levels/hours. | [Knowledge Model PDF](https://csed.acm.org/wp-content/uploads/2024/04/1.3-Introduction-to-Knowledge-Model.pdf) | Supplies the broad external coverage baseline. The report states 270 instructional hours for CS Core, but that number is not adopted as an Essential CS syllabus target. |
| CS23-BOK | *Body of Knowledge*, official Final Report component. The summary table lists 162 knowledge units and CS Core hours by area: AI 12, AL 32, AR 9, DM 10, FPL 21, GIT 4, HCI 8, MSF 55, NC 7, OS 8, PDC 9, SDF 43, SE 6, SEC 6, SEP 18, SF 18, SPD 4. | [Body of Knowledge PDF](https://csed.acm.org/wp-content/uploads/2024/04/3.1-Body-of-Knowledge-1.pdf) | Detects areas that the current macro spine may only imply: mathematical reasoning, software-development fundamentals, HCI, AI literacy, and society/ethics/profession. It also separates foundational concepts from specialist breadth. |
| CS23-COMP | *Introduction to Competency Framework*, official Final Report component. It defines competency as task + competency statement + knowledge + skills + dispositions; sample competency areas include Software, Systems, and Applications. | [Competency Framework PDF](https://csed.acm.org/wp-content/uploads/2024/04/1.4-Introduction-to-Competency-Framework.pdf) | Supports auditing learner capability rather than topic presence. It is especially relevant to Trace/Observe/Diagnose/Judge and Learn-New-Tech. |
| CS23-PED | *Pedagogical Considerations*, official Final Report component. It discusses mathematics, algorithms, software engineering trade-offs, SEP integration, and the fast-changing AI area. | [Pedagogical Considerations PDF](https://csed.acm.org/wp-content/uploads/2024/04/4.1-Pedagogical-Considerations.pdf) | Provides caution against both mathematics avoidance and trend-driven AI/tool coverage, and supports integrated ethical/professional treatment. |

### 2.2 Representative classic textbooks

| ID | Edition / state | Authoritative reference | Durable mechanisms used in this audit |
|---|---|---|---|
| TXT-SICP | Abelson and Sussman, *Structure and Interpretation of Computer Programs*, 2nd ed. (MIT Press, 1996). The edition identity was checked against the cited MIT Press URL; the page returned HTTP 403 to this environment, so no current-page wording is treated as verified evidence. | [MIT Press edition page](https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/) | Abstraction, procedural/data representation, state and mutation, modularity, metalinguistic abstraction, interpreters, and the relation between language and machine. |
| TXT-ALGS | Sedgewick and Wayne, *Algorithms*, 4th ed. (Princeton, 2011; maintained companion site). | [Algorithms, 4th Edition](https://algs4.cs.princeton.edu/home/) | Abstract data types, searching/sorting, graphs, symbol tables, complexity, and the idea that representation choices change algorithmic cost. |
| TXT-CSAPP | Bryant and O'Hallaron, *Computer Systems: A Programmer's Perspective*, 3rd ed. (CMU companion site, 2015). | [CS:APP 3e](https://csapp.cs.cmu.edu/3e/home.html) | Bits/representation, machine code, linking, exceptional control flow, memory hierarchy, virtual memory, system I/O, networking, and concurrency as a programmer-facing chain. |
| TXT-OSTEP | Arpaci-Dusseau and Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*, online version 1.10 at the audited site. | [OSTEP](https://pages.cs.wisc.edu/~remzi/OSTEP/) | A compact organizing model—virtualization, concurrency, persistence—with concrete scheduling, memory, and filesystem mechanisms. |
| TXT-COD | Patterson and Hennessy, *Computer Organization and Design: The Hardware/Software Interface, RISC-V Edition*, 2nd ed., published December 11, 2020. | [Elsevier edition page](https://www.elsevier.com/books/computer-organization-and-design-risc-v-edition/patterson/978-0-12-820331-6) | ISA/software boundary, performance and energy, memory hierarchy, I/O, and why architecture cannot remain an opaque black box. |
| TXT-NET | Kurose and Ross, *Computer Networking: A Top-Down Approach*, 8th ed. (Pearson, 2021). The authors' current site also records that a 9th ed. was published in summer 2025; the 8th ed. is retained here as the classic course/text reference examined for the audit. | [Authors' networking site](https://gaia.cs.umass.edu/kurose_ross/index.php); [Pearson 8th-edition page](https://eu.pearson.com/computer-networking-a-top-down-approach-global-edition/9781292419978) | Layering, application-to-link dependencies, transport reliability/congestion, routing, wireless/multimedia context, and the value of a top-down mental model. |
| TXT-DDIA | Kleppmann, *Designing Data-Intensive Applications*. The author's maintained reference site was used for the enduring first-edition treatment; any later edition is not assumed to be a new curriculum authority. | [Author's DDIA site](https://dataintensive.net/) | Data models, encoding/evolution, storage/retrieval, replication, partitioning, transactions, batch/stream processing, and reliability/scalability/maintainability trade-offs. |

This set is intentionally not a prestige list. It spans language/abstraction, algorithms, machine/OS, networking, data-intensive systems, and architecture while leaving specialist graphics, robotics, and quantum material outside the first shared comparison.

### 2.3 Representative university courses and materials

| ID | Institution / current audited material | Evidence observed | Comparison use |
|---|---|---|---|
| UNI-CMU213 | Carnegie Mellon, **15-213 Introduction to Computer Systems, Fall 2026**. | Course objective connects execution, storage, communication, performance, portability, robustness, compilers, arithmetic, memory, networking, and concurrency. Labs include C, data, bomb, attack, cache, malloc, shell, proxy, and a simple filesystem; several require code review and an understanding check. | Shows how one systems course turns a broad chain into observable mechanisms and judged explanations, but its implementation load is not a Core-size prescription. |
| UNI-MIT1810 | MIT, **6.1810 Operating System Engineering, Fall 2025**. | The course explicitly uses xv6 and labs for system calls, page tables, traps, copy-on-write, network driver, locks, filesystem, and `mmap`, with software/hardware interaction. | Evidence for process/memory/kernel/I/O/concurrency/filesystem dependencies and for using a small real system to reveal mechanisms. |
| UNI-MIT5840 | MIT, **6.5840 Distributed Systems, Spring 2026**. | The course describes fault tolerance, replication, and consistency; the MapReduce lab requires a coordinator/worker system that handles failed workers, RPC, parallel work, and re-assignment. | Evidence that distributed systems is best taught through partial failure and case implementation, while also showing graduate-level prerequisite/complexity cost. |
| UNI-ST144 | Stanford, **CS144 Introduction to Computer Networking, Fall 2025**. | Checkpoints progress from reliable byte streams and TCP receiver/sender to real-world measurement, network interface, IP router, and a capstone Internet assembled from student stacks. | Strong evidence for bottom-up protocol mechanisms, measurement, layering, integration, and collaborative system debugging. |
| UNI-B186 | UC Berkeley, **CS186 Introduction to Database Systems, Fall 2026**. | The live calendar covers SQL, disks/buffers/files, cost models, B+ trees, buffer management, sorting/hashing, joins, relational algebra, query optimization, transactions/concurrency, recovery, parallel query, 2PC, Paxos, NoSQL, and MapReduce/Spark. | Shows the dependency chain inside data systems and the breadth that should be sampled rather than copied into Essential CS Core. |
| UNI-ST221 | Stanford, **CS221 Artificial Intelligence: Principles and Techniques, Spring 2026**. | Current assignments cover foundations, sentiment, route planning, Mountain Car, Pacman, scheduling, a car task, logic, and a project. | Evidence that AI literacy can be taught through problem formulation, search, learning, planning, evaluation, and applications rather than through a product catalogue. |
| UNI-MISSING | MIT, **The Missing Semester of Your CS Education, 2026**. | The current sequence includes shell, command-line/development tools, debugging and profiling, version control, packaging/shipping code, agentic coding, “beyond the code,” and code quality. | Direct evidence that shell/tool literacy, debugging, reproducibility, packaging, and source verification are competencies often absent from named CS courses. |

### 2.4 Classic/open teaching projects and labs

| ID | Project | Mechanism-level signal | Boundary for this audit |
|---|---|---|---|
| LAB-N2T | *From Nand to Tetris*, current project page with 12 projects across hardware and software. | A complete stack from Boolean logic, memory, architecture, machine language, assembler, VM, parsing, code generation, and OS. | Supports a vertical-slice view of the stack; full completion is too implementation-heavy to assume for Core. Candidate curation remains Issue #4's responsibility. |
| LAB-XV6 | MIT xv6 book/labs, linked from 6.1810. | Small real kernel makes system calls, traps, page tables, copy-on-write, locks, filesystems, and device interaction inspectable. | Supports Adopt/Adapt decisions, not a mandate to build a kernel in Core. |
| LAB-OSTEP | The authors' [OSTEP projects repository](https://github.com/remzi-arpacidusseau/ostep-projects). | Small OS projects expose scheduling, memory, concurrency, persistence, and system-call boundaries. | Used to identify learning mechanisms, not to select final labs. |
| LAB-ST144 | Stanford CS144 checkpoint set. | A single evolving network stack makes byte streams, TCP, interfaces, routing, measurement, and integration observable. | Strong candidate signal for Issue #4; this audit does not adopt it. |
| LAB-MIT5840 | MIT 6.5840 MapReduce and subsequent distributed-systems labs. | Worker failure, RPC, coordination, replication, and consistency are tested through implementation and case discussion. | Demonstrates both the value and the prerequisite cost of distributed implementation. |

## 3. Comparison framework applied to the current macro spine

The current spine is compared as a dependency chain, not as a list of course labels:

`Map → Information → Computation → Machine → PL/Runtime/Compiler → OS → Storage → Network → Web/Browser → Database → Concurrency → Distributed Systems → Modern Infrastructure → Security Synthesis → Systems Thinking/Judgment → Final System Defense`

At macro level, this is unusually coherent for Essential CS's stated goal. It exposes a learner to representations and computation before machine execution, then follows state and data through operating systems, storage, networks, web/browser, databases, concurrency, distribution, deployment, and security. It also explicitly names the modern cross-layer cases that a conventional “intro programming + algorithms + OS + networks” sequence can leave implicit.

The horizontal threads—correctness/invariants, failure, debugging, measurement/performance, security, cost/resource economics, technical literacy, API/interface design, software engineering, privacy/data responsibility, and napkin math—are the right normalization layer for comparing course labs. In the external references, the most valuable learning often appears as a repeated behavior: predict, observe, break, measure, explain, and defend a choice.

The main macro-level uncertainty is not whether the spine names the right areas. It is whether the future detailed architecture will give enough first-class space, prerequisites, labs, and assessments to the horizontal capabilities and to areas currently represented only by a broad label.

## 4. Coverage strengths

These are **macro-level strengths**, not claims that lesson-level coverage already exists.

### 4.1 Complete modern system journey

The Map → Information → Computation → Machine → language/runtime → OS sequence has a sound dependency direction. SICP, Algorithms, CS:APP, OSTEP, MIT 6.1810, and Nand2Tetris all support the educational value of following abstractions downward and back upward. The later Storage → Network → Web/Browser → Database → Concurrency → Distributed Systems → Infrastructure chain then makes state, data movement, failure, and resource trade-offs visible in increasingly integrated systems.

This is stronger than mechanically reproducing CS2023 knowledge-area names: the learner gets a causal route through the system.

### 4.2 Mechanism-first systems orientation

The explicit inclusion of machine, OS, storage, networking, browser, database, concurrency, and distributed systems is well supported by CMU 15-213, MIT 6.1810, Stanford CS144, Berkeley CS186, MIT 6.5840, CS:APP, OSTEP, and DDIA. The current map is therefore not underpowered merely because it does not mirror a four-year department course list.

### 4.3 Horizontal failure, correctness, measurement, security, and cost

The invariants and horizontal threads are well justified. OSTEP organizes systems around virtualization, concurrency, and persistence; MIT 6.5840 centers fault tolerance, replication, and consistency; Stanford CS144 includes a real-world measurement checkpoint; CMU's labs include performance, attack, cache, malloc, shell, proxy, and filesystem work; CS2023 integrates SEP and professional dispositions across knowledge areas.

Essential CS is right to make these recurring questions rather than late standalone chapters. The risk is execution: the detailed map must attach required observations, evidence, and judgment artifacts to actual modules and labs.

### 4.4 Browser and infrastructure as integrated cases

Web/Browser and Modern Infrastructure are not a traditional topic-list minimum, but they are justified by the project's modern-world-model goal. They are good synthesis cases for protocols, caching, isolation, identity, data, deployment, observability, supply chain, and cost. Their admission should remain principle-led: browser/cloud products are cases, not the canonical concepts.

### 4.5 Core/Deep Dive separation

The current Core/Deep Dive rule is consistent with CS2023's distinction between CS Core, KA Core, and Non-core. It permits Essential CS to retain important specialist knowledge without allowing every traditional degree topic to consume the first shared traversal.

### 4.6 Project and System Defense orientation

The evolving Mini Cloud App and final System Defense give the course a place to connect otherwise separate mechanisms and ask learners to defend trade-offs. This aligns with the competency-oriented references better than a final recall exam alone. Issue #3 must ensure that the app milestones actually expose the audited gaps rather than only exercise web-framework implementation.

## 5. Missing or underrepresented concepts

The following are gaps or risk areas in the **current macro declaration**. The absence of a named macro area does not prove the final course will omit the concept; it means the concept is not yet protected by an explicit architecture-level commitment.

### 5.1 Applied mathematical and statistical reasoning

**Finding: macro-level underrepresentation.** CS2023 assigns 55 CS Core hours to Mathematical and Statistical Foundations and places discrete mathematics, probability, and statistics as dependencies for other knowledge areas. Its MSF material includes sets/functions, recursion, proof techniques, counting, modular arithmetic, logic, graphs, order notation, and statistical reasoning. CS2023 also explicitly treats MSF as cross-cutting rather than merely a separate mathematics department prerequisite.

Essential CS has “Napkin Math” as a horizontal thread, but the current map does not yet state a visible applied toolkit or a dependency policy. Without one, learners may encounter complexity, probability of failure, concurrency interleavings, database selectivity, network capacity, cost, and AI evaluation as vocabulary rather than reasoning tools.

The recommendation is not a calculus-first mathematics course. Core should protect just-in-time discrete reasoning, asymptotic/scale estimates, basic probability and uncertainty, and enough statistics to interpret experiments and model evaluation. Proof-heavy mathematics and advanced linear algebra can remain Deep Dive.

### 5.2 Software-development fundamentals and tool fluency

**Finding: macro-level underrepresentation.** CS2023 gives Software Development Fundamentals 43 CS Core hours and Software Engineering 6 CS Core hours. CMU 15-213 makes labs the heart of the course and uses code reviews/understanding checks. MIT's 2026 Missing Semester directly teaches shell, development tools, debugging/profiling, Git, packaging/shipping, code quality, and AI-assisted workflows.

Essential CS declares technical literacy and software engineering horizontally, which is directionally correct, but the current spine does not show where a learner first becomes able to navigate a codebase, reproduce an environment, test a hypothesis, inspect a failure, review a change, package a result, and record evidence. These are not “professional extras” for a self-study systems curriculum; they are the operating interface for every later lab.

### 5.3 Human-computer interaction, accessibility, and user boundary conditions

**Finding: macro-level omission.** HCI is not named in the current macro spine, while CS2023 lists HCI as an 8-hour CS Core area and includes accessibility and DEIA topics in SEP. A modern system model that only follows code, data, and infrastructure can still miss whether people can understand, access, trust, and safely use the system.

The Core need not become a full HCI methods course. It should protect a small human-facing boundary: user goals and mental models, feedback/error recovery, accessibility, consent/privacy interaction, and the relationship between interface choices and system state. Usability research methods, visual design, interaction theory, and specialized HCI can be Deep Dive.

### 5.4 AI literacy and data/model judgment

**Finding: macro-level omission.** CS2023's AI area includes 12 CS Core hours and explicitly calls for basic AI literacy and critical thinking for every computer science student, including problem characteristics, search, machine learning, applications, societal impact, and limitations. Stanford CS221's current assignments show a mechanism-oriented route through search, sentiment, route planning, scheduling, logic, and application projects.

The current Essential CS spine contains algorithms, data, security, infrastructure, and judgment, but no explicit AI literacy anchor. For a modern computing-system world model, learners should be able to identify when an AI approach is appropriate, distinguish data/model/interface/system failure, interpret evaluation and uncertainty, estimate resource/cost implications, and judge societal/security/privacy effects. This can be a bounded, stable Core thread; it does not require a deep-learning specialization.

### 5.5 Data modeling, encoding/evolution, provenance, and derived data

**Finding: fine-grained risk; `RECHECK-AFTER-ISSUE-1`.** The Database macro area is strong, but the current label does not reveal whether it will cover data modeling, schema evolution, serialization compatibility, provenance, or batch/stream/derived-data trade-offs. Berkeley CS186's Fall 2026 sequence makes the internal dependency chain explicit: SQL, storage layout, cost models, indexes, joins, optimization, transactions, recovery, distributed transactions, and alternative data models. DDIA connects these to encoding/evolution, replication, partitioning, reliability, scalability, and maintainability.

Core should protect the stable data-system questions and one or two contrasting cases. Spatial/vector indexes, NoSQL families, MapReduce/Spark, and specialized data platforms should not automatically become Core requirements.

### 5.6 Computational models, limits, and the algorithm–language connection

**Finding: fine-grained risk; `RECHECK-AFTER-ISSUE-1`.** The current Computation & Algorithms label is promising, and CS2023's Algorithmic Foundations area explicitly includes computational models/formal languages, complexity, computability, and algorithms. However, the macro label does not show whether the learner will understand why some problems are tractable, expressible, decidable, or impossible, nor how these limits connect to language design and compilers.

Core should include an intuitive model-of-computation and limits boundary, complexity/scale reasoning, and the practical relation between representations, algorithms, and language/runtime mechanisms. Full automata theory, reductions, proof portfolios, and computability formalisms can be Deep Dive.

### 5.7 Physical, embedded, and real-time constraints

**Finding: macro-level underrepresentation but not necessarily a Core omission.** CS2023 includes Specialized Platform Development and Architecture material for embedded constraints, interrupts, sensors, and heterogeneous systems. MIT 6.1810 also uses software/hardware interaction and a RISC-V system. Essential CS's Machine area can give learners a sufficient abstract machine model without becoming an embedded curriculum.

The unresolved question is whether one short physical/real-time case materially improves the shared world model. Full embedded development, robotics, FPGA, and real-time scheduling belong in Deep Dive unless Issue #1 demonstrates a strong dependency.

### 5.8 AI-assisted development and primary-source verification

**Finding: current-practice risk; `RECHECK-AFTER-ISSUE-1`.** The repository already says AI is not an authority and includes Learn-New-Tech. MIT Missing Semester's 2026 material explicitly includes agentic coding and code quality, while CS2023 has a dedicated generative-AI curriculum section and treats AI as rapidly changing. The missing architectural question is how a learner repeatedly practices verifying generated code, documentation, benchmarks, APIs, and security claims against primary sources.

The stable Core is source literacy, contract extraction, small experiments, and evidence recording. Specific AI tools and agent workflows are Current Cases with short review cycles.

## 6. Missing or underrepresented competencies

The current eight competencies are well chosen. The audit does not recommend replacing them. It identifies behaviors that must be made explicit in module/lab/project outcomes so that topic labels do not masquerade as capability.

| Competency risk | External evidence | Essential CS implication | Status |
|---|---|---|---|
| Evidence-backed diagnosis | CMU labs include performance, cache, malloc, shell, proxy, attack, and understanding checks; Stanford CS144 includes “measuring the real world”; MIT Missing Semester includes debugging/profiling. | A Diagnose outcome should require a hypothesis, measurement plan, observation, competing explanation, and conclusion—not merely “run a tool.” | CORE; `RECHECK-AFTER-ISSUE-1` |
| Experimental validity | Systems labs use controlled checkpoints and tests; CS2023 connects knowledge to skills and dispositions rather than recall alone. | Observe/Estimate should include baseline, workload, warmup/steady state, repetitions or uncertainty where relevant, and the limit of the inference. | CORE; `RECHECK-AFTER-ISSUE-1` |
| Contract/specification/invariant communication | CS2023 competency statements separate the task from the technical competency; OSTEP/CSAPP/CS144 mechanisms are understood through explicit interfaces and invariants. | Trace/Explain/Correctness should require stating what must remain true at an interface and how evidence supports that claim. | CORE; `RECHECK-AFTER-ISSUE-1` |
| Technology judgment under constraints | CS2023 competency framework uses tasks and constraints; DDIA, CS186, CMU, and MIT distributed systems materials repeatedly expose trade-offs. | Judge/Estimate should include alternatives, complexity moved elsewhere, failure modes, scale threshold, and cost/resource consequences. | CORE; `RECHECK-AFTER-ISSUE-1` |
| Primary-source learning | CS2023 Learn-New-Tech analogue appears through task-based competency and professional dispositions; the Missing Semester makes tools and workflows explicit. | Learn-New-Tech should produce a small source map: contract, assumptions, version, experiment, uncertainty, and stopping point. | CORE; `RECHECK-AFTER-ISSUE-1` |
| Human/impact judgment | CS2023 gives SEP 18 CS Core hours, HCI 8, and explicit AI/social/accessibility concerns. | Explain/Judge should sometimes include affected users, privacy, accessibility, fairness, accountability, sustainability, and whether the system should be built. | CORE; `RECHECK-AFTER-ISSUE-1` |
| Maintainable technical communication | CMU code reviews, Stanford CS144 writeups/collaboration, and MIT Missing Semester code quality/package practices show that durable system work includes readable evidence and handoff. | Keep this as a behavior expressed through Explain, Correctness, Judge, and Learn-New-Tech rather than automatically adding a standalone “teamwork course.” | CORE; `RECHECK-AFTER-ISSUE-1` |
| AI-output verification | CS2023 treats generative AI as fast-changing; MIT Missing Semester teaches agentic coding in a tool-fluency context. | Add a Current Case pattern: generated output is an untrusted hypothesis; verify with tests, source, measurement, and security review. | CURRENT CASE; `RECHECK-AFTER-ISSUE-1` |

## 7. Possible over-weighting

These are not claims that the current blueprint is already overbuilt. They are guardrails for Issue #1's detailed architecture.

### 7.1 Modern Infrastructure becoming a product syllabus

Containers, cloud services, orchestration, deployment systems, and supply-chain tools are useful cases. They become baggage when learners memorize vendor commands without understanding isolation, packaging, scheduling, resource economics, observability, reproducibility, or trust boundaries. Core should teach those stable mechanisms; Kubernetes, a particular cloud provider, Terraform, or a changing CI platform should be Current Cases or Deep Dives.

### 7.2 Distributed consensus implementation

MIT 6.5840 is a graduate course with explicit prerequisites and substantial programming; Berkeley CS186's Fall 2026 calendar includes Paxos within a much broader database course. This is evidence that consensus is educationally important, not evidence that every Essential CS learner should implement Raft/Paxos in Core. The shared model needs partial failure, replication, consistency, leader/coordination trade-offs, and what consensus buys/costs. Full algorithm implementation and proof should be Deep Dive.

### 7.3 Full OS kernel construction

MIT xv6 is an excellent real mechanism because it is small enough to inspect, but the 6.1810 lab sequence still presupposes a substantial programming/systems context. Core should expose process abstraction, address translation, traps/syscalls, scheduling, synchronization, files/durability, isolation, and observation. A complete kernel extension sequence should be optional or Deep Dive.

### 7.4 Full networking-stack construction

Stanford CS144 demonstrates the value of implementing a stack, but it also spans multiple checkpoints and a substantial codebase. Core should preserve packet/byte-stream boundaries, addressing/routing, reliability, congestion/timeout intuition, TLS/HTTP placement, measurement, and failure. Implementing a complete TCP/IP/Ethernet stack is Deep Dive unless the detailed architecture proves a small vertical slice is the best shared experiment.

### 7.5 Database-internals breadth

The Berkeley CS186 calendar is a useful map of the field, but its coverage of spatial/vector indexes, multiple indexing families, NoSQL, distributed transactions, Paxos, MapReduce, and Spark should be sampled according to Essential CS's stable-principle goal. Core needs data models, SQL/relational algebra, storage/index/query cost, transactions/concurrency, recovery/durability, replication/partitioning, and one contrasting modern case. The rest is Current Case or Deep Dive.

### 7.6 Advanced algorithmic and mathematical inventory

Algorithms 4e and CS2023 AL/MSF show a large space of valuable material. Essential CS should not import every balanced-tree variant, advanced graph/string algorithm, formal proof technique, quantum algorithm, calculus sequence, or ML linear-algebra treatment. The Core test is whether the item materially improves Trace, Correctness, Judge, Estimate, or Learn-New-Tech across the shared system journey.

### 7.7 Compiler and language implementation

SICP and CSAPP justify teaching abstraction, representation, runtime, linking, memory, and source-to-machine flow. A full compiler, multiple language paradigms, advanced type theory, garbage collector, optimizer, and ABI implementation suite is a degree-style specialization. Keep the stable transformations in Core; put construction depth in Deep Dive.

## 8. Conventional-degree baggage

The following table explicitly separates “valuable somewhere in a degree” from “required in Essential CS Core.”

| Topic family | Why a degree may teach it | Essential CS position | Class |
|---|---|---|---|
| Full standalone discrete-math/calculus sequence | Supports broad theoretical and application specializations. | Teach an applied, just-in-time reasoning toolkit; do not make a long prerequisite chain the entry gate. | REJECT as Core packaging; selected applied topics remain CORE |
| Formal-language, automata, reductions, and computability proof portfolio | Prepares for theory, compilers, formal methods, and graduate study. | Preserve computational models, limits, and practical complexity intuition; move proof-heavy breadth after the shared traversal. | DEEP DIVE |
| Full compiler construction | Valuable for PL/compiler specialization and implementation practice. | Teach source → representation → runtime → machine and selected observations; no full compiler requirement in the first traversal. | DEEP DIVE |
| Complete OS/kernel implementation | Valuable for systems specialization and low-level programming. | Teach mechanisms through a small real system and targeted experiments; do not require a full kernel project. | DEEP DIVE |
| Complete TCP/IP/Ethernet stack | Strong capstone for a networking course. | Teach layer contracts, reliability, routing, timeouts, security placement, and measurement; full stack is optional. | DEEP DIVE |
| Raft/Paxos implementation and formal proof | Valuable in advanced distributed systems. | Teach failure/replication/consistency/coordination conceptually in Core; implementation belongs later. | DEEP DIVE |
| Exhaustive database engine/index family coverage | Useful for database specialization and research preparation. | Keep the stable storage/query/transaction/recovery chain; use modern families as bounded cases. | CURRENT CASE |
| Graphics, animation, robotics, FPGA, embedded-platform breadth | Supports application or platform specializations. | Retain only a small physical/resource-constrained case if it improves the shared system model. | DEEP DIVE |
| Quantum computing and quantum architecture | Legitimate emerging/specialist field; CS2023 includes related non-core material. | No evidence that it is necessary for the first shared modern-system model. | REJECT from v0.1 Core |
| Large-team Agile ceremony and project-management inventory | Useful for degree/team practice and professional preparation. | Retain version control, review, testing, communication, maintenance, and responsibility; avoid ceremony as curriculum content. | REJECT as Core topic inventory |
| Vendor-specific cloud/Kubernetes/CI certification content | Useful for job-specific onboarding. | Use vendor-neutral mechanisms and one replaceable Current Case. | CURRENT CASE, with product depth DEEP DIVE |

## 9. Recommendation table

| ID | Finding | External evidence | Essential CS consequence | Class | Confidence | Detailed #1 architecture required? |
|---|---|---|---|---|---|---|
| R1 | Applied discrete, probability, statistics, and scale reasoning are not yet protected by a visible Core dependency. | CS2023 MSF has 55 CS Core hours and cross-cutting requirements; AL, AI, systems, and course experiments rely on this reasoning. | Define a small just-in-time MSF toolkit tied to invariants, complexity, uncertainty, capacity, cost, and evaluation. | CORE | High | Yes — `RECHECK-AFTER-ISSUE-1` |
| R2 | Toolchain/software-development fundamentals are only horizontal labels today. | CS2023 SDF 43 / SE 6 CS Core hours; CMU lab code reviews; MIT Missing Semester 2026. | Give shell, code reading, debugging/profiling, version control, testing, packaging, and reproducibility explicit outcomes and practice. | CORE | High | Yes — `RECHECK-AFTER-ISSUE-1` |
| R3 | HCI/accessibility/user-boundary reasoning is not named in the macro spine. | CS2023 HCI 8 CS Core hours and SEP/DEIA accessibility material. | Add a bounded human-facing system case and assess feedback, error recovery, accessibility, consent, and user mental models. | CORE | Medium | Yes — `RECHECK-AFTER-ISSUE-1` |
| R4 | AI literacy is absent as an explicit modern-system capability. | CS2023 AI 12 CS Core hours and explicit basic AI literacy goal; Stanford CS221's current mechanism-oriented assignments. | Teach problem suitability, representation, search/learning distinction, data/model/evaluation failure, resource cost, and impact. | CORE | High | Yes — `RECHECK-AFTER-ISSUE-1` |
| R5 | Generative AI and agentic coding should be current evidence work, not a static tool chapter. | CS2023 generative-AI discussion; MIT Missing Semester 2026 agentic-coding and code-quality material. | Make generated output an untrusted hypothesis verified by source, tests, measurement, and security review. | CURRENT CASE | High | Yes — `RECHECK-AFTER-ISSUE-1` |
| R6 | Database macro area needs explicit data modeling, encoding/evolution, provenance, and derived-data decisions. | Berkeley CS186 sequence; DDIA's data-system mechanisms. | Protect stable data-system questions in Core; defer specialized index/data-platform breadth. | CORE | High | Yes — `RECHECK-AFTER-ISSUE-1` |
| R7 | Measurement/diagnosis needs a required experimental pattern, not only tool exposure. | Stanford CS144 “measuring the real world”; CMU performance labs; MIT debugging/profiling. | Require prediction, baseline, controlled change, observation, uncertainty/limits, and causal restraint in Observe/Diagnose/Estimate outcomes. | CORE | High | Yes — `RECHECK-AFTER-ISSUE-1` |
| R8 | Security, privacy, accountability, and accessibility may be too late if left only to Security Synthesis. | CS2023 SEC 6 and SEP 18 CS Core hours; SEP is intended to appear across areas. | Keep security/privacy/impact horizontal, with early concrete trust-boundary and data-responsibility cases plus final synthesis. | CORE | High | Yes — `RECHECK-AFTER-ISSUE-1` |
| R9 | Computational models and limits are a fine-grained risk inside Computation & Algorithms. | CS2023 AL includes models/formal languages, complexity, and computability; SICP/CSAPP connect language and machine representations. | Ensure the first traversal explains tractability/expressibility/limits and links them to PL/runtime/compiler. | CORE | Medium | Yes — `RECHECK-AFTER-ISSUE-1` |
| R10 | Consensus is important as a concept but expensive as an implementation requirement. | MIT 6.5840 is graduate-level with prerequisites and substantial labs; Berkeley CS186 uses Paxos among many DB topics. | Teach why coordination is hard, what consistency/failure trade-off is purchased, and where consensus fits; do not require full implementation in Core. | CORE | High | Yes — `RECHECK-AFTER-ISSUE-1` |
| R11 | Full consensus algorithms, proofs, and replicated-service implementation are specialist depth. | MIT 6.5840 lab structure and prerequisites; distributed case-study emphasis. | Reserve Raft/Paxos implementation and proof depth for an extension/source expedition. | DEEP DIVE | High | Yes — `RECHECK-AFTER-ISSUE-1` |
| R12 | A physical/embedded/real-time case may improve boundary understanding, but full platform breadth is not justified yet. | CS2023 SPD/AR; MIT 6.1810 software/hardware interaction and RISC-V xv6. | Ask whether one small resource/deadline/sensor case improves the shared model; do not add a platform track by default. | DEEP DIVE | Medium | Yes — `RECHECK-AFTER-ISSUE-1` |
| R13 | Cloud/orchestration products risk consuming Core attention. | CS2023 distinguishes broad knowledge areas from local competency focus; Essential's own Technology Evaluation Framework requires stable principles and scale thresholds. | Keep isolation, packaging, deployment, observability, supply chain, and resource economics in Core; use a replaceable product case. | CURRENT CASE | High | Yes — `RECHECK-AFTER-ISSUE-1` |
| R14 | Full kernel, full protocol stack, full compiler, and exhaustive DB-engine projects are degree-style implementation burdens. | MIT xv6, Stanford CS144, Nand2Tetris, Berkeley CS186, SICP, and CSAPP show their value but also their scope. | Adopt/adapt small mechanism slices; make complete implementations optional/deep. | DEEP DIVE | High | Yes — `RECHECK-AFTER-ISSUE-1` |
| R15 | Quantum and other specialist topic inventories do not yet clear the Essential CS Core test. | CS2023 places quantum material outside the universal Core in the cited body sections; the current goal is a shared modern computing-system model. | Preserve an explicit boundary so novelty or degree tradition cannot silently expand Core. | REJECT | Medium | Yes — `RECHECK-AFTER-ISSUE-1` |

### 9.1 Classification rationale for material recommendations

The table below makes the decision logic explicit for every material recommendation. “Prerequisite/complexity cost” includes learner prerequisites, implementation burden, maintenance burden, and opportunity cost in the first shared traversal.

| ID | Educational value | Relevance to Essential CS goals | Prerequisite / complexity cost | Why this class is appropriate |
|---|---|---|---|---|
| R1 | Gives learners the minimum reasoning tools needed to interpret complexity, uncertainty, capacity, cost, and experiments. | Directly strengthens Estimate, Correctness, Diagnose, and Judge across nearly every macro area. | A long standalone mathematics sequence creates an entry barrier; just-in-time discrete/probability/statistics still needs deliberate sequencing. | **CORE** because the capability is cross-cutting; defer exact placement until #1 detail is available. |
| R2 | Makes later source, lab, and project work independently executable and reproducible. | Directly enables Observe, Diagnose, Explain, Learn-New-Tech, and the self-study-first invariant. | Tool instruction can sprawl into product tutorials and version churn; it must be kept task-centered. | **CORE** because it is the learner's operating interface for the whole curriculum, not degree ceremony. |
| R3 | Prevents a technically correct system model from ignoring user goals, accessibility, error recovery, and human consequences. | Supports modern-system judgment, privacy/data responsibility, and the Mini Cloud App's human-facing boundary. | A full HCI methods/design sequence is large and changes the center of gravity; a bounded case is manageable. | **CORE** at bounded competency depth; specialized methods remain out of first traversal. |
| R4 | Provides enough AI literacy to recognize problem fit, representation/evaluation limits, and system/impact failure. | Necessary for a current computing-world model and for judging AI claims encountered in other modules. | Deep learning mathematics, training infrastructure, and fast-moving tooling are high-cost and time-sensitive. | **CORE** for stable literacy and judgment; product/model implementation depth is not required. |
| R5 | Teaches a durable way to use powerful but fallible AI-assisted tools. | Directly exercises Learn-New-Tech, Correctness, Diagnose, security, provenance, and technical judgment. | Specific tools change rapidly and can distract from source/test/measurement habits. | **CURRENT CASE** because the verification pattern is stable but the product/workflow examples require review. |
| R6 | Makes data a model/evolution/provenance problem, not only a SQL syntax problem. | Directly supports Trace, Correctness, Judge, failure reasoning, and the Mini Cloud App's evolving state. | Full database internals and platform breadth are substantial; learners need storage/algorithm foundations first. | **CORE** for stable data-system questions; specialized families remain bounded cases or Deep Dives. |
| R7 | Converts observation into causal diagnosis instead of tool-driven guesswork. | It is the clearest operational form of Observe, Diagnose, Estimate, and Explain. | Requires repeated controlled experiments and assessment design; adds time but little conceptual baggage. | **CORE** because it is a horizontal capability with evidence in strong systems labs. |
| R8 | Makes trust, privacy, responsibility, accessibility, and security part of design rather than cleanup. | Directly implements the invariant that security, privacy, failure, correctness, and responsibility recur horizontally. | Cross-module coordination is harder than a late standalone chapter; legal detail can become excessive. | **CORE** as recurring judgment patterns; jurisdiction-specific law and specialist security depth remain elsewhere. |
| R9 | Explains what computation can express or solve and why representation/algorithm/language choices matter. | Strengthens Explain, Correctness, Judge, and the Map → Computation → PL/Runtime/Compiler dependency. | Formal proofs and full theory sequences are high cognitive load for the shared first pass. | **CORE** for intuitive models, limits, and complexity; formal theory is Deep Dive. |
| R10 | Gives learners a usable model of why distributed coordination is hard and what guarantees cost. | Directly supports Trace, Failure, Correctness, Judge, and the distributed/infrastructure spine. | Distributed systems has a long prerequisite chain and many interacting failure cases. | **CORE** conceptually because the modern world model needs it, without requiring a full implementation. |
| R11 | Builds specialist ability to implement and reason formally about consensus and replicated services. | Valuable for advanced distributed-systems work and source expeditions. | Graduate-level prerequisites, substantial code, concurrency bugs, and proof burden are high. | **DEEP DIVE** because it improves depth after the shared model without being required for every learner. |
| R12 | A small physical/real-time case can reveal deadlines, interrupts, sensors, energy, and resource constraints. | Potentially strengthens Machine, Observe, Judge, and systems-boundary understanding. | Platform/toolchain setup and hardware variability can dominate the learning objective. | **DEEP DIVE** pending evidence that a bounded case improves the common traversal enough to justify the cost. |
| R13 | Concrete infrastructure cases make packaging, isolation, deployment, observability, and resource economics tangible. | Directly serves the modern-system world model and technology-evaluation framework. | Vendor APIs, cloud accounts, orchestration complexity, and rapid churn can overwhelm stable principles. | **CURRENT CASE** for a replaceable example; stable mechanisms stay CORE and product mastery stays DEEP DIVE. |
| R14 | Complete implementations can create unusually strong mechanism understanding and integration practice. | Supports Explain, Observe, Diagnose, and System Defense when chosen selectively. | Full kernel/stack/compiler/DB projects consume large amounts of time and assume prior depth. | **DEEP DIVE**: adopt/adapt small slices in Core, preserve full builds for optional depth. |
| R15 | Explicit exclusion protects attention for the shared world model and prevents novelty-driven scope creep. | Supports Complexity must justify itself and the Core/Deep Dive boundary. | Omitting specialist topics reduces breadth for learners pursuing those fields, but no shared dependency was established here. | **REJECT** from v0.1 Core; revisit only if the Lead identifies a concrete cross-cutting dependency. |

## 10. Open questions for the Web Lead

These are architecture questions for reconciliation; this audit does not decide them.

1. Should AI literacy be one explicit bounded module, or a spiral across algorithms, data, systems, security, and the Mini Cloud App?
2. Where is the first canonical home for applied MSF, and how will its later revisits avoid duplicating definitions?
3. What is the smallest visible SDF/toolchain slice that makes shell, debugging, Git, testing, packaging, and source verification reliable prerequisites?
4. Where should HCI/accessibility/user-boundary reasoning enter the system journey, and which parts belong to the Mini Cloud App versus independent labs?
5. What evidence artifact will prove that Security/Privacy/SEP are horizontal rather than merely named in a late synthesis stage?
6. What is the Core boundary for consensus: conceptual model, trace of a case, or a small implementation experiment?
7. Does the first shared traversal need one physical/embedded/real-time case, or is that better as a Deep Dive bridge?
8. Which database breadth is necessary for the complete modern world model, and which is only a current case?
9. How will the final System Defense require assumptions, uncertainty, alternatives, failure modes, cost, privacy, accessibility, and evidence—not only architecture vocabulary?
10. How should CS2023 skill levels and dispositions inform Essential CS assessment without importing its instructional-hour model?

## 11. Reconciliation checklist after Issue #1

When the detailed Stage/Module/Lesson map and dependency graph return, the Web Lead should:

- replace each macro finding with a Module/Lesson/Lab/Project location or mark it intentionally out of scope;
- verify that R1/R2/R3/R4/R6/R7/R8 have explicit outcomes, observations, and assessment evidence;
- check dependency order for MSF → algorithms/AI/data/system estimates, SDF/toolchain → systems work, and computation models → PL/runtime/compiler;
- confirm one primary teaching home for each canonical concept and no silent duplicate definitions;
- inspect whether security, privacy, cost, failure, measurement, and responsibility recur before the final synthesis;
- check that each Core addition improves at least one of Trace, Explain, Observe, Diagnose, Correctness, Judge, Estimate, or Learn-New-Tech;
- identify implementation-heavy tasks that should become optional, Current Cases, or Deep Dives;
- ensure Modern Infrastructure remains vendor-neutral and principle-led, with product cases reviewable and replaceable;
- coordinate lab adoption/adaptation with Issue #4 without pre-empting its candidate research;
- coordinate Mini Cloud App milestones with Issue #3 so the project exposes data evolution, security/privacy, observability, cost, failure, and user boundaries;
- record any change to Core scope, architecture, or invariants through the project's Open Question → RFC/Decision path;
- re-run this audit's recommendation table against the final detailed dependency graph before Blueprint v0.1 is declared complete.

## 12. Completion report

### Task / status

- Issue #2
- READY FOR WEB LEAD REVIEW

### Deliverables

- Created the requested external curriculum coverage audit.
- Included scope/method, provenance, normalized comparison framework, strengths, gaps, competency risks, over-weighting, degree baggage, classified recommendations, Web Lead questions, and Issue #1 reconciliation checklist.

### Files changed

- `meta/audits/external-curriculum-audit-v0.1.md`

### Reference set

- ACM / IEEE-CS / AAAI CS2023 official Final Report components: Executive Summary, Knowledge Model, Body of Knowledge, Competency Framework, and Pedagogical Considerations.
- Classic references: SICP 2e, Algorithms 4e, CS:APP 3e, OSTEP v1.10, Computer Organization and Design RISC-V 2e, and DDIA author-maintained reference material.
- Current university materials: CMU 15-213 Fall 2026; MIT 6.1810 Fall 2025; MIT 6.5840 Spring 2026; Stanford CS144 Fall 2025; UC Berkeley CS186 Fall 2026; Stanford CS221 Spring 2026; MIT Missing Semester 2026.
- Teaching projects/labs: Nand2Tetris, xv6, OSTEP projects, Stanford CS144 checkpoints, and MIT 6.5840 labs.

### Verification performed

- Fetched `origin` and used the current `origin/main` snapshot `7d67fd359130c97a7bf88308e22063497901b662`.
- Checked GitHub Issue #2 and all current repository issues on 2026-08-30: Issues #1–#4 are open; no pull requests were open at the time of checking.
- Verified the live CS2023 Final Report page and downloaded/inspected its official component PDFs, including the 17-area table, Core/KA Core definitions, competency framework, AI, AL, SEP, MSF, and curricular packaging sections.
- Verified university claims against live course pages and actual lab/project materials, not titles alone.
- Verified material textbook edition details where used; the Elsevier page identifies Computer Organization and Design RISC-V Edition 2nd Edition as published December 11, 2020; CMU/Princeton/Wisconsin/author pages identify the other cited editions or maintained versions.
- Checked that the audit treats CS2023 as evidence and a comparison framework, not a mandatory syllabus.
- Ran repository file/status inspection, `git diff --check`, required-section/class checks, and a custom check of all 16 unique external URLs. Fifteen returned HTTP 200; the MIT Press SICP page returned HTTP 403, and the CS2023 Body of Knowledge URL returned a transient HTTP 000 in the parallel link pass even though that PDF had already been downloaded and inspected successfully.

### What remains unverified

- Issue #1's future detailed architecture, lesson granularity, dependency graph, and final lab choices.
- Issue #3's Mini Cloud App milestones and whether they exercise the identified gaps.
- Issue #4's final classic-lab and Source Expedition candidates.
- Any claim about learner outcomes from the cited courses beyond what their public course pages/lab documents state.
- Live page wording from MIT Press's SICP URL; the environment returned HTTP 403. The edition/title URL and the text's established conceptual role are retained as contextual textbook evidence, not as a current-practice claim.

### Key findings

- Highest-impact omissions/risk areas: explicit applied MSF; visible SDF/toolchain competency; bounded AI literacy; HCI/accessibility/user boundary; and assessed experimental diagnosis/source verification.
- Highest-impact architecture guardrails: security/privacy/SEP must be assessed horizontally; consensus, kernel, protocol-stack, compiler, and database breadth must not silently become implementation-heavy Core; infrastructure must remain vendor-neutral and principle-led.

### Assumptions

- The audited macro files on `origin/main` are the current architecture baseline because Issue #1 has not yet returned its detailed map.
- “Core” means the first shared Essential CS traversal, not every concept that a conventional CS graduate may eventually encounter.
- Current-course pages dated Fall 2025/Spring 2026/Fall 2026 are valid evidence of teaching practice available in the current audit window; they are not permanent recommendations.

### Open questions

- See Section 10; all unresolved items are intentionally phrased as questions for Web Lead architecture reconciliation.

### Prompt deviations

- None.

### Out-of-scope necessary fixes

- None. The audit stayed within `meta/audits/` and did not modify curriculum architecture, concepts, status, decisions, maps, or matrices.

### Reconciliation needed

- All fine-grained findings require `RECHECK-AFTER-ISSUE-1`.
- R1–R15 should be reconciled against Issue #1's dependency graph and detailed map.
- R3/R4/R5/R8/R9 need coordination with Issue #3's Mini Cloud App evolution.
- Lab mechanism/depth recommendations should be reconciled with Issue #4.

### Recommended review focus

1. Whether the proposed applied MSF and toolchain/SDF coverage is enough to make later systems learning independently achievable.
2. Whether AI literacy and HCI/accessibility should be explicit Core competencies or spiral cases.
3. Whether the Core boundary for consensus, OS, networking, compiler, and database implementation is protected in Issue #1.
4. Whether the final assessment will make failure, measurement, security/privacy, cost, accessibility, uncertainty, and evidence visible.
5. Whether the audit's exclusions defend Essential CS's purpose without accidentally removing a necessary modern-system capability.
