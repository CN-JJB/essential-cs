# Foundations M00–M01 Evidence Template

> 只记录足以复查学习证据的内容。不要把它变成长日志。若某字段与当前任务无关，留空或写 `N/A`。

## A — Environment / Preflight Header

- 日期：
- 仓库 / commit 或 working-tree context：
- OS / environment：
- CPU architecture：
- Python version：
- Git version：
- Activity path：`labs/foundations/m00-m01/`
- Preflight result：`PASS / BLOCKED`
- 若 blocked，原始错误摘要：

> 版本必须写实际观察值。目标环境与实际环境不同，不要改写成“已在目标版本验证”。

---

## B — M00 System / P0 Path Trace

### B1. Question + Prediction

**Question / claim：**

**Prediction（运行前）：**

### B2. Bounded path

用一行或小图记录：

`input → interface → process-local state → representation/output → course-supplied opaque save/load boundary (if used)`

- Input：
- Interface / boundary：
- Process-local state：
- Output：
- Intentionally opaque mechanism / model limit：

### B3. Baseline observation

- Command / action：
- Relevant output excerpt：

**Observation only：**

### B4. Exactly one controlled change

- Changed variable：
- Before：
- After：
- `git diff` excerpt / reference：
- Changed-condition command：
- Relevant output excerpt：

### B5. Explanation + uncertainty

**Explanation candidate：**

**Competing explanation or unresolved uncertainty：**

**Bounded conclusion：**

### B6. Reset

- Reset command：
- Evidence that baseline was restored：

### B7. Source-layer judgment

- Claim being checked：
- Chosen evidence layer：`SPECIFICATION / official docs / implementation source / experiment`
- Why this layer fits the claim：
- What this layer does **not** establish：

---

## C — M01 Representation Trace

### C1. Information vs Representation

- Information / value / text：
- Representation rule(s)：
- Exact bytes / hex：
- Width / range assumptions：

### C2. Integer boundary trace

- Integer width：
- unsigned range：
- signed range：
- Boundary case checked：
- Observation：
- Representation claim vs language-semantics boundary：

### C3. UTF-8 trace

- Text：
- Code point(s), if needed：
- UTF-8 bytes：
- Byte count：
- Human-visible character note for this example：
- Stopping-point warning（grapheme / normalization if relevant）：

### C4. Endianness trace

- Logical value：
- little-endian bytes：
- big-endian bytes：
- Wrong-order decode observation：

### C5. Serialization / size / round trip

- Field layout：
- Pre-run size estimate + assumptions：
- Observed size：
- Round-trip observation：
- One controlled break / failure：
- What the round trip does **not** prove：

### C6. P0 boundary note, if used

- Learner-owned process-local / representation work：
- Course-supplied opaque boundary：
- Later-load observation, if any：
- Explicit non-claim: `This is not evidence of durability.`

---

## G — Support / Uncertainty Metadata

对本 packet 中需要 review 的 artifact，记录最高 support level：

- `Independent`
- `Hint 1`
- `Hint 2`
- `Expected Observation`
- `Full Explanation`

**Highest support used：**

**如果看过 Full Explanation：**本次 artifact 作为 remediation evidence；新的短 Transfer check：

**Remaining unknowns / next check：**

**Tool/environment issue vs concept issue：**

**Reviewer note（可选）：**
