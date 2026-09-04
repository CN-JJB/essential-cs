# EXP-03 Evidence Template — Chromium Process Model & Site Isolation

Use this form for **one actual source inspection**. Do not copy another learner's
revision, date, function details, platform mode, or findings. Chromium is a
fast-changing implementation source.

## 1 — Inspection identity

- Inspection date/time: `<actual>`
- Official source host: `chromium.googlesource.com`
- Branch/ref inspected: `<actual>`
- Exact Chromium commit/revision: `<actual>`
- Source-access disposition:
  - `LIVE_CHROMIUM_SOURCE_ACCESSIBLE`, or
  - `NO LIVE CHROMIUM SOURCE RECHECK / EXP-03 LIVE SOURCE OBSERVATION NOT RUN`

If live source access is unavailable, stop the live-source claim here. Repository
Research/Design may be used as **REFERENCE EVIDENCE ONLY**; never invent a commit
hash or current source excerpt.

## 2 — Exact bounded route

Record whether each target exists at the exact inspected revision:

1. `docs/process_model_and_site_isolation.md`
   - Exists: `<actual>`
   - Exact revision link/reference: `<actual>`
2. `content/browser/site_instance_impl.cc`
   - Exists: `<actual>`
   - Exact revision link/reference: `<actual>`
3. `content/browser/security/cpsp/child_process_security_policy_impl.cc`
   - Exists: `<actual>`
   - Exact revision link/reference: `<actual>`

A path/function move is evidence. Do not silently substitute a different source
route if it materially changes the accepted expedition.

## 3 — Architecture-document finding

In the bounded process-model / Goals / Site Isolation material, record:

- one current claim about compromised-renderer defense: `<actual paraphrase>`
- one current claim about Spectre-like / same-process threat motivation:
  `<actual paraphrase>`
- current Site Isolation mode/platform nuance, if inspected within the bounded
  current-practice lookup: `<actual>`
- what the source **does not** establish: `<actual inference limit>`

Guardrail: do not add Meltdown unless the exact inspected source passage says so,
and do not claim process isolation eliminates all side channels.

## 4 — Process-selection finding

At `SiteInstanceImpl::GetProcess()` / `GetOrCreateProcess()` or the current
directly corresponding entry, record:

- exact symbol(s) found: `<actual>`
- one current process-selection/reuse condition: `<actual>`
- one implementation nuance that disproves “one navigation = one new process”:
  `<actual>`
- stopping point reached before broad `RenderProcessHost` / IPC traversal:
  `YES / NO + note`

Function/member names are **revision-specific Chromium implementation evidence**.

## 5 — Browser-side security-policy finding

At `CanAccessDataForOrigin()` or the current directly corresponding bounded
origin/data-access path, record:

- exact symbol/signature observed: `<actual>`
- calling child/process identity input: `<actual>`
- target origin/security-policy input: `<actual>`
- one opaque-origin/process-lock/current-state behavior actually visible:
  `<actual>`
- inference limit: this selected method is not claimed to centralize every
  Cookie/file/network/IPC permission: `<learner explanation>`

## 6 — Conceptual vs implementation nuance

Explain why **Full Site Isolation does not mean “one site = one process”**:

- what cross-site process/site-lock separation the current source supports:
  `<actual>`
- one way multiple processes for one site or process reuse can occur:
  `<actual>`
- one platform/resource/current-mode qualification:
  `<actual>`

Do not convert current Chromium thresholds or modes into Web Platform invariants.

## 7 — Stop-rule audit

- [ ] Did not clone/download the full Chromium repository.
- [ ] Did not compile Chromium.
- [ ] Did not follow broad callees beyond the three accepted anchors.
- [ ] Did not inspect Blink/V8/GPU internals beyond the bounded M12 need.
- [ ] Did not turn Android/platform-specific implementation into a Core
      cross-platform requirement.
- [ ] Recorded any separate platform-mode lookup explicitly instead of hiding it
      inside the Path 1 bounded-read claim.

Notes: `<actual>`

## 8 — Licensing / provenance

- Link-and-inspection-first used: `<YES/NO>`
- Chromium source vendored/mirrored into Essential CS: expected **NO**
- Source excerpt copied into submission: `<NO / if YES, exact file + lines>`
- If an excerpt was used, exact file/header/license/NOTICE/third-party provenance
  reviewed: `<actual>`
- Required attribution/notice retained: `<actual>`

Prefer links + learner-authored paraphrase. Do not rely on a blanket “Chromium is
BSD” or blanket fair-use statement for arbitrary files.

## 9 — Reviewer synthesis

Write one paragraph answering:

1. What did the current Chromium source confirm?
2. What did it make more conditional than the simple teaching model?
3. Which statement is Web Platform/specification reasoning, and which is
   Chromium implementation/current-practice evidence?
4. What would need to be rechecked at a future release review?

This evidence is not learner validation, VERIFIED, or RELEASED status.
