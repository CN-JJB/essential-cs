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
  In the *Goals* and *Site Isolation* sections, Chromium articulates that multi-process architecture and locked renderer processes exist to defend against compromised renderer processes and hardware-level speculative execution side-channel attacks (**Spectre and Meltdown**), which would otherwise allow untrusted JavaScript to read cross-origin memory within the same process address space.

### Path 2: `content/browser/site_instance_impl.cc`
- **Bounded Finding**:
  In `SiteInstanceImpl::GetProcess()` and `GetOrCreateProcess()`, process assignment evaluates `has_group()`, checks whether `ShouldUseProcessPerSite()` applies to update `process_reuse_policy_`, and checks `CanPutSiteInstanceInDefaultGroup()`. An existing renderer process from the default group is reused whenever permitted by policy, rather than unconditionally allocating a new OS process per navigation.

### Path 3: `content/browser/security/cpsp/child_process_security_policy_impl.cc`
- **Bounded Finding**:
  In `ChildProcessSecurityPolicyImpl::CanAccessDataForOrigin(int child_id, const url::Origin& origin)`, the centralized browser process evaluates the calling child process ID and the target origin (extracting precursor tuples for opaque origins) against the process lock registered in `process_states_`, refusing data access and recording crash keys if a process locked to one site attempts to access another site's committed data.

---

## 5. One Conceptual-vs-Implementation Nuance

- **Nuance**:
  While the conceptual teaching model frames Site Isolation as "one site = one process", actual Chromium engineering accommodates memory constraints and platform differences. On memory-constrained devices or under OS process count limits, Chromium applies process reuse fallbacks (such as the default `SiteInstanceGroup` or partial site isolation for login-only domains), balancing security blast radius against system memory exhaustion.

---

## 6. Stop-Point Confirmation

- [x] Path 1: Stopped immediately after the introduction and Site Isolation motivation sections. Did not read Android WebView or embedder-specific branches.
- [x] Path 2: Stopped after inspecting `GetOrCreateProcess()` entry reuse checks. Did not trace Mojo IPC allocation or low-level `RenderProcessHost` initialization.
- [x] Path 3: Stopped at the `CanAccessOrigin` origin lock verification. Did not trace legacy blob/file URL compatibility branches.

---

## 7. Source Access Disposition

- **Disposition**: `LIVE_CHROMIUM_SOURCE_ACCESSIBLE`
- Verified via live HTTP query to `https://chromium.googlesource.com/chromium/src/+/refs/heads/main?format=JSON`.

---

## 8. Licensing & Provenance Disposition

- Chromium source code is authored by The Chromium Authors and licensed under BSD-style terms with third-party components.
- EXP-03 is link-and-inspection-only. Essential CS does not vendor, mirror, or redistribute the Chromium source tree.
- Any citations in learner guides are minimal fair-use quotations strictly for pedagogical verification.

---

## 9. No-Compile / No-Vendor Confirmation

- [x] Zero Chromium source code files downloaded to the local course repository.
- [x] Zero local compilation of Chromium.
- [x] No third-party repository vendoring or binary redistribution.
