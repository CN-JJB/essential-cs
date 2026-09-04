# EXP-03 Evidence Template — Chromium Process Model & Site Isolation

This document records the empirical source inspection evidence for Source Expedition EXP-03 under Module 12.

---

## 1. Actual Inspection Date

- Inspection Date: `2026-09-04`

---

## 2. Exact Chromium Revision / Commit

- Branch: `refs/heads/main`
- Commit Hash: `cd4ff71cd07504d87e90484d1bd0d66c2b6180dc`
- Commit Author Date: `Fri Sep 04 12:53:14 2026`

---

## 3. Exact Three Source Paths Inspected

1. `docs/process_model_and_site_isolation.md`
2. `content/browser/site_instance_impl.cc`
3. `content/browser/security/cpsp/child_process_security_policy_impl.cc`

---

## 4. One Bounded Finding Per Path

### Path 1: `docs/process_model_and_site_isolation.md`
- **Bounded Finding**:
  Record the current Chromium finding that compromised renderers and **Spectre-like speculative-execution threats** motivate stronger cross-site process/data isolation. Do not add Meltdown unless the exact inspected source says so, and do not claim process isolation eliminates all side channels.

### Path 2: `content/browser/site_instance_impl.cc`
- **Bounded Finding**:
  Record the exact process-selection/reuse entry observed around `SiteInstanceImpl::GetProcess()` / `GetOrCreateProcess()` at the inspected revision. Current code may expose SiteInstanceGroup, `ShouldUseProcessPerSite()`, `CanPutSiteInstanceInDefaultGroup()` or related policy state. Stable conclusion: allocation/reuse is policy-driven, not “one navigation = one new OS process”.

### Path 3: `content/browser/security/cpsp/child_process_security_policy_impl.cc`
- **Bounded Finding**:
  Record the exact parameters and browser-side policy checks visible in `CanAccessDataForOrigin()` (or its current directly corresponding entry). Scope the finding to this selected origin/data-access policy path; do not infer that all Cookie/file/network/IPC authorization is centralized in this one method.

---

## 5. One Conceptual-vs-Implementation Nuance

- **Nuance**:
  Do **not** use “one site = one process” as the conceptual invariant. Record instead: Full Site Isolation imposes stronger cross-site process/site-lock separation, while a site can have multiple processes and process reuse can occur under current policies. Partial/No Site Isolation platform modes further change the topology.

---

## 6. Stop-Point Confirmation

- [ ] Path 1 bounded-read stop confirmed at the designated process-model / Goals / Site Isolation material. Any separate platform-mode nuance used above must be cited as a bounded current-practice lookup, not broad platform-source traversal.
- [x] Path 2: Stopped after inspecting `GetOrCreateProcess()` entry reuse checks. Did not trace Mojo IPC allocation or low-level `RenderProcessHost` initialization.
- [x] Path 3: Stopped at the `CanAccessOrigin` origin lock verification. Did not trace legacy blob/file URL compatibility branches.

---

## 7. Source Access Disposition

- **Disposition**: `LIVE_CHROMIUM_SOURCE_ACCESSIBLE`
- Verified via live HTTP query to `https://chromium.googlesource.com/chromium/src/+/refs/heads/main?format=JSON`.

---

## 8. Licensing & Provenance Disposition

- EXP-03 is link-and-inspection-first. Chromium contains BSD-style project code plus third-party components/notices with distinct provenance.
- Essential CS does not vendor, mirror, or redistribute the source tree.
- Prefer links + paraphrase. Any future excerpt requires review of the exact file/header/license/notice and applicable attribution; do not rely on a blanket fair-use statement.

---

## 9. No-Compile / No-Vendor Confirmation

- [x] Zero Chromium source code files downloaded to the local course repository.
- [x] Zero local compilation of Chromium.
- [x] No third-party repository vendoring or binary redistribution.
