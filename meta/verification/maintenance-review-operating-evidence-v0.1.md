# Maintenance + Review Operating Evidence v0.1

**Task:** Issue #156 — `[Verification] Maintenance + review operating evidence v0.1`

**Role:** Web Lead / Operating-Evidence Recorder

**Canonical base:** `main @ d8b6305b6849cec69a5ef3a089256414f49f6bb7`

**Conclusion:** `MAINTENANCE / REVIEW OPERATING EVIDENCE PASS`

This report addresses only the v1.0 gate that maintenance/review workflows are **actually operating**. It does not establish learner validation, final external audit, stable multi-role verification, `VERIFIED`, `RELEASED`, or v1.0 readiness.

## 1. Policy versus operation

Written policy exists in:

- `meta/LIVING_CURRICULUM_POLICY.md`;
- `meta/REVIEW_POLICY.md`;
- `meta/RELEASE_AND_MAINTENANCE_POLICY.md`.

Policy existence alone is not counted as operating evidence. The evidence below is observed repository operation.

## 2. Review workflow is operating

The repository has repeatedly exercised the Issue → bounded branch/PR → exact-head Lead review → bounded Direct Fix where needed → re-lock final head → expected-head merge pattern.

Representative recent examples:

- Issue #140 / PR #142 — independent post-v0.9 gap audit accepted and merged; gaps were routed rather than silently repaired inside the audit.
- Issue #145 / PR #146 — canonical stable-environment implementation reviewed at exact head; Web Lead applied bounded CI fixes and accepted final exact-head runtime evidence.
- Issue #147 / PR #148 — independent-verification report was accepted as a truthful **failed verification / blocker discovery** rather than forced green; V-147-01 and V-147-02 were routed separately.
- Issue #149 / PR #151 — QEMU false-green repair; final exact-head real-QEMU evidence was inspected before expected-head merge.
- Issue #150 / PR #152 — durable canonical environment pin implementation; Web Lead narrowed GHCR package permissions by Direct Fix, re-locked the new exact head, checked fresh fast/QEMU evidence and artifacts, then expected-head merged.
- PR #154 — Mini Cloud P0–P9 implementation; Web Lead discovered trust/failure/atomicity defects, applied bounded Direct Fixes on the same branch, required fresh exact-head CI, downloaded artifacts, and merged only the reviewed final head `7cae4be28aab4c3f6c3ccd0555e704b765f1d1d1` as merge commit `d8b6305b6849cec69a5ef3a089256414f49f6bb7`.

These are observed review operations, not a statement of policy intent.

## 3. Continuous executable maintenance is operating

Current `.github/workflows/` contains four active workflow definitions:

- `ci-fast.yml`;
- `ci-qemu-lane.yml`;
- `publish-canonical-environment.yml`;
- `ci-mini-cloud.yml`.

Recent observed exact-head runs include:

### Canonical fast lane

- PR #154 final-head run: `34679423472` — SUCCESS at `7cae4be28aab4c3f6c3ccd0555e704b765f1d1d1`.
- Exact checkout assertion, immutable canonical digest consumption, canonical floor capture, shared preflights, shell gates, full 26-suite surface, M03 real GDB, REQ-01/03/04/05, hygiene, and evidence upload all succeeded.
- Retained artifact: `canonical-fast-evidence`, ID `10294016173`, GitHub digest `sha256:f1998dfa0714a990f0d69739984922dd0b6e3066e220dd7d19e47ad27ad6610b`.
- Web Lead downloaded and inspected the artifact rather than relying only on upload success.

### Mini Cloud lane

- PR #154 final-head run: `34679423473` — SUCCESS at the same exact head.
- Immutable canonical digest was consumed; 66 Python tests passed; benchmark/race demonstrations passed; real subprocess + real HTTP smoke passed; reset and hygiene passed.
- Retained artifact: `mini-cloud-evidence`, ID `10293412291`, GitHub digest `sha256:1443f3928146c79bfb1db6afffe1f1279720aeb9ecd0e424b2e5f3f9ea7bbac5`.
- Web Lead downloaded and inspected its inventory and logs.

### QEMU lane

- Final durable-pin implementation evidence included workflow-dispatch run `34675978745` at exact accepted head `4599707550960beab82bd726e77ba42bb840f2ce`.
- Real learner-owned LAB-REQ-02 `./smoke.sh` executed under QEMU; standalone `LAB_REQ_02_OK`, `QEMU_SMOKE_STATUS: PASS`, `QEMU_REAPED: TRUE`, `PID_MARKER_CLEAN: YES`, fail-closed evidence completion, and reset-to-pin truth were retained.
- Artifact `canonical-qemu-evidence`, ID `10292820980`, digest `sha256:b0708a05b2238a7afb55e74e7d4fbe15ab98f5f2d6f0b5ab19dabf90cc1a3515`, was downloaded and inspected by Web Lead.

### Canonical environment publication / retrieval

The durable environment publication path has also executed rather than merely existing as YAML. Candidate publication, digest retrieval, committed-pin verification, and least-privilege package permissions were exercised during #150 / PR #152. The accepted canonical identity remains:

`ghcr.io/cn-jjb/essential-cs/canonical@sha256:766ce07ba3073cc28049ff07d6d4f643bd6e3cc7a7967a3ebd2bb8738219e460`

## 4. Evidence retention and fail-closed behavior are operating

Recent workflows retain artifacts with IDs, sizes and SHA-256 digests. Lead review has repeatedly downloaded and inspected artifacts. The #147 QEMU false-green incident is especially important operating evidence: a nominally successful workflow was rejected because its retained artifact lacked the required real smoke evidence and the raw log exposed a heredoc warning. The system then routed a repair instead of treating a green status as sufficient truth.

That incident demonstrates the review workflow is capable of detecting CI/evidence failure modes rather than mechanically trusting status color.

## 5. Maintenance queue is operating

At this report's base, the remaining stable-gate queue is explicitly tracked in GitHub rather than hidden in prose:

- Issue #34 — mandatory real-human learner validation;
- Issue #153 — independent durable canonical-environment-pin verification;
- Issue #155 — deferred v1.0 Core-scope governance disposition;
- Issue #156 — this operating-evidence task;
- Issue #157 — final external curriculum/coverage audit;
- Issue #158 — final stable multi-role verification, dependency-gated on earlier independent work.

This is consistent with `LIVING_CURRICULUM_POLICY.md`, which requires a maintenance queue for broken labs, source/spec change, environment drift, stale material, and errata.

## 6. Cadence truth

`LIVING_CURRICULUM_POLICY.md` defines suggested review cadence:

- STABLE: 18–24 months or after relevant major change;
- CURRENT: 6–12 months;
- FRONTIER: 3–6 months;
- Labs: continuous CI/smoke plus periodic human/AI review.

The repository's current production/stabilization cycle is only weeks old. No 6–12 month CURRENT or 3–6 month FRONTIER scheduled review is yet overdue merely by elapsed time. Therefore absence of an elapsed-period refresh cannot truthfully be counted as a missed cadence at this date.

Labs and the canonical environment already have repeated executable CI/smoke evidence during the current stabilization cycle.

## 7. Errata / Hotfix readiness

The stable Errata/Hotfix process is specified in `meta/RELEASE_AND_MAINTENANCE_POLICY.md`: confirm impact, identify canonical concept/revisits, fix `main`, patch stable users where affected, record errata/release notes, notify learners when material, and never rewrite historical tags.

There has not yet been a stable v1.0 user incident because v1.0 has not been released. A fabricated patch incident is neither necessary nor valid evidence. The v0.9 and stabilization history does, however, show the repository operating the analogous confirm → route → repair → independently recheck pattern for real defects such as LAB-REQ-02 smoke and QEMU false-green findings.

## 8. Limitations / non-claims

This PASS means the repository has concrete observed evidence that maintenance and review mechanisms are functioning now. It does **not** prove that future 6–24 month review cadences will be met indefinitely. Future maintenance must continue to create repository evidence as items become due.

It also does not close:

- Issue #34 learner validation;
- Issue #153 / OQ-BP-006;
- final external audit;
- final stable multi-role verification;
- lifecycle promotion.

## Final conclusion

`MAINTENANCE / REVIEW OPERATING EVIDENCE PASS`
