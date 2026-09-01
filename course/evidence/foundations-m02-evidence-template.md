# Foundations M02 Evidence Template

> 只记录足以让别人复查你的判断的内容。M02 完成的是 S1 的 **Correctness + Judge + Estimate** 关键证据；它不是 learner-validation record，也不要求超出 Design scope 的形式化证明。

## A — Environment / Activity Header

- 日期：
- Repository / commit / working-tree context：
- OS / environment：
- CPU architecture：
- Python version：
- Git version：
- Activity path：`labs/foundations/m02/`
- Preflight result：`PASS / BLOCKED`
- 若 blocked，原始错误摘要：

> 版本写实际观察值。未运行 Ubuntu 24.04 / Python 3.12 时，不得声称已在该环境验证。

---

## D1 — Complexity Evidence

### Input + counted operation

- Question / workload fragment：
- Input size `n`：
- Dominant counted operation：
- Count unit（例如 key comparisons / record visits / pair comparisons / halving steps）：
- 为什么这个 operation model 与当前问题有关：

### Operation-count table

| `n` | observed / derived count | unit | note |
|---:|---:|---|---|
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

- Asymptotic classification：
- Assumptions：
- 这项 classification **不**表示什么（至少写明与 elapsed milliseconds 的区别）：

### Order-of-magnitude estimate

- Scenario：
- `n`：
- Estimated work：
- Units：
- Rough order of magnitude（例如 `~10^6 key comparisons`）：
- Assumptions / ignored costs：
- Bounded conclusion：

---

## D2 — Trade-off Evidence

- Stated workload：
- Operation being optimized：
- Input size / expected scale：
- Constraint：
- Selected structure/interface：
- Alternative：
- Expected gain：
- Growth assumption：
- Constants / implementation effects acknowledged but not modeled：
- Build / maintenance cost：
- Memory / complexity cost：
- Failure / correctness obligation introduced by the extra structure：
- **When NOT to use selected option：**
- Final Trade-off statement（必须把 gain 与 cost 放在同一个 constraint 下）：

### Transfer case

- New workload：
- Does the original choice still follow? Why / why not：
- What asymptotic notation alone cannot decide here：

---

## D3 — Correctness Evidence

### Specification

写成 bounded、可检查的 behavior/guarantee；不要只写 feature slogan。

- Assumptions / valid input domain：
- `lookup(k)` required behavior：
- `update(k, v)` required behavior：
- Missing-key behavior：
- Observable state-change boundary：

### Invariant

- Property that must remain true across every permitted transition：
- Why it matters to both lookup paths：
- Machine-checkable predicate / activity output used：

### Counterexample / controlled break

- Flawed operation：
- Small failing input / transition：
- Prediction before run：
- Observed violation：
- Which Specification / Invariant clause was violated：
- Why a previously passing example/test did not rule this out：

### Correction reasoning

- Corrected transition：
- Why it preserves the Invariant：
- Evidence after correction：
- Missing / boundary behavior checked：
- What remains an assumption or unproven generalization：

### Correctness statement

用一句话完成：

> 在 ________ assumptions / input domain 下，这个 implementation 的 observable behavior 满足 ________ Specification，并在 permitted transitions 后保持 ________ Invariant；这些 tests/counterexamples 是证据，但 ________。

---

## D4 — Limits Evidence

不要把下面三个概念画成同一条“越来越慢”的速度刻度。

### Representable / expressible

- 一个在本活动中可以明确表示的问题/输入：
- Representation / interface assumption：

### Computable but potentially expensive here

- Problem / procedure：
- Why a procedure exists：
- Why it may be too expensive under this workload / `n`：
- Work unit + rough scale：
- Is it generally decidable? `YES / NOT THE QUESTION HERE`

### Not generally decidable

- Bounded example/category：
- What “no general decision procedure” means in your own words：
- Why this is **not** the same as “too slow here”：
- Why this does **not** mean analysis/tests/proofs for particular cases are useless：

---

## G — Support / Uncertainty Metadata

对本 packet 中被评审的 artifact，记录最高 support level：

- `Independent`
- `Hint 1`
- `Hint 2`
- `Expected Observation`
- `Full Explanation`

**Highest support used：**

**如果看过 Full Explanation：**本次 artifact 是 remediation evidence；新的短 Transfer check：

**Remaining unknowns / next check：**

**Tool/environment issue vs concept issue：**

**Reviewer note（可选）：**
