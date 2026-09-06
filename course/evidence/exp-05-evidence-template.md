# EXP-05 Evidence Template — MIT 6.033 Replication, Transactions & Logging

Use this template for **one actual source inspection and reading card completion**. Do not copy another learner's notes, diagram annotations, dates, or answers.

---

## 1 — Source Inspection Identity & License Audit

- Inspection Date / Time: `<actual inspection date/time>`
- Official Source Provider: `MIT OpenCourseWare (Spring 2018)`
- Course Title: `6.033 Computer System Engineering`
- Target Document 1 (Primary):
  - Lecture 14 (Fault Tolerance: Reliability via Replication):
    `https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/8eb16d3628bbd77ee7e8471b9871ec09_MIT6_033S18lec14.pdf`
  - Reachability / Access Status: `<actual source access disposition>`
- Target Document 2 (Comparative):
  - Lecture 15 (Fault Tolerance: Introduction to Transactions):
    `https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/df1526408e3ec6f7e43aadfa1ce5f944_MIT6_033S18lec15.pdf`
  - Reachability / Access Status: `<actual source access disposition>`
- Target Document 3 (Comparative):
  - Lecture 16 (Atomicity via Logging):
    `https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/76fa216e8e5a4c4722c315a84b8e09a8c_MIT6_033S18lec16.pdf`
  - Reachability / Access Status: `<actual source access disposition>`
- Lead Provenance Correction for View Server Comparison:
  - Lecture 19 (Availability via Replication):
    `https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/resources/mit6_033s18lec19/`
  - Official Lecture 19 Outline:
    `https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/pages/week-11/lecture-19-outline/`
  - Reachability / Access Status: `<actual source access disposition>`
- License Compliance Audit:
  - Source License: `CC BY-NC-SA 4.0 (with third-party rights reservation)`
  - Vendoring Audit: `<learner/source-audit disposition; record any issue instead of pre-filling PASS>`
  - Essential CS Format: `Link-and-Paraphrase Only`

---

## 2 — Guiding Questions & Reading Card Findings

### (1) Lecture 19 Primary / Backup State Tracking
- What state does the Primary maintain?
  `<Learner records state tracked by primary under Lecture 19>`
- What state does the Backup maintain?
  `<Learner records state tracked by backup>`
- How does the client identify where to send operations?
  `<Learner records client view lookup mechanism>`

### (2) Failure Detection Ambiguity
- What mechanism detects node silence?
  `<Learner notes periodic ping / timeout mechanism>`
- What can the detector NOT distinguish?
  `<Learner explicitly records the fundamental ambiguity: network partition / pause vs physical machine crash>`
- What is the danger if an unconfirmed primary continues executing mutations?
  `<Learner describes split-brain / dual-primary write conflict hazard>`

### (3) View Server Coordination & Sync Barrier
- What state does the View Server maintain?
  `<Learner records view number, primary node ID, backup node ID>`
- What is the View progression barrier?
  `<Learner explains why the View Server must not promote view v+1 until primary of view v acknowledges view v>`
- What happens if the View Server itself crashes?
  `<Learner identifies the single-point-of-coordination vulnerability of a centralized view server>`

### (4) Architectural Comparison: Lecture 19 View Server vs. Course Bounded Raft Trace
- Authority model comparison:
  `<Learner compares the centralized View Server authority with the course's replicated-voting trace; majority-set overlap must not be treated as the full Raft proof>`
- Partition/failure-model comparison:
  `<Learner compares the stated partition/failure assumptions of the Lecture 19 View Server model and the course 2 | 3 logical Raft trace>`
- Simpler Single-Node Alternative:
  `<Learner contrasts multi-node replication against a single node with durable storage and cold spare, evaluating MTBF/MTTR>`

---

## 3 — Learner Original Diagram Annotation

- Annotated Diagram Reference: `<learner original notes file or sketch reference>`
- Mandatory Elements Verified in Original Sketch:
  - Primary, Backup, View Server, and Client nodes explicitly distinguished: `<YES / NO>`
  - View progression acknowledgment message labeled: `<YES / NO>`
  - Network partition boundary isolating old primary clearly drawn: `<YES / NO>`
  - Split-brain prevention invariant stated: `<YES / NO>`

---

## 4 — Bounded Stopping Point Confirmation

- Bounded route respected (L14/L15/L16 plus narrow L19 provenance correction only): `<learner records actual disposition>`
- Zero external code downloaded or compiled: `<learner records actual disposition>`
- Zero MIT assignment solutions reproduced: `<learner records actual disposition>`
- Summary Judgment:
  `<Learner summarizes L14 replication foundations, L19 Primary/Backup + View Server, and the bounded comparison to the course Raft trace>`
