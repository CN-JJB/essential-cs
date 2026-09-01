# M02 Shared Activity — 增长、权衡与正确性

> 这是 M02 的共享 **Lesson activity surface**，不是 Required Lab，也没有 Lab ID。

按 Lesson 顺序使用：L02-01 先做 counts；L02-02 在 canonical Trade-off introduction 后做 lookup comparison；L02-03 在 Specification/Invariant/Correctness canonical introduction 后再做 break/correction。README 只提供 activity contract，不取代这些 canonical definitions。

这个活动只使用一个进程内 record collection。它把同一批 records 暴露成两条 exact-key lookup 路径：

`records(list) → linear scan`

`records(list) + key→position index → key-based lookup`

这里不教授数据库、文件系统、持久性、缓存/局部性或 Python `dict` 内部实现。所有计数都是**明确指定的教学操作**，不是 elapsed milliseconds。

## 学习目标

你将用同一个 workload 完成：

`reset → baseline → predict counts → count → compare lookup paths → state spec/invariant → controlled break → correction → reset`

并保存足以复查的：operation counts、workload choice、Trade-off、Specification、Invariant、counterexample 与 limits explanation。

## 文件角色

- `activity.py`：deterministic record fixture、operation counting、两条 lookup path、controlled break、corrected update。
- `test_activity.py`：标准库 `unittest` 自动检查 exact counts、labels、invariant、counterexample 与 reset determinism。

没有第三方 package，没有网络请求，没有 privileged operation，也没有外部数据文件。

## Preflight

从仓库根目录运行：

```bash
cd labs/foundations/m02
python3 --version
```

把**实际** Python / OS / architecture 写入 M02 evidence template。不要把目标版本写成已验证版本。

## 1. Reset + baseline

```bash
python3 activity.py reset
python3 activity.py baseline
```

关键 baseline：

```text
BASELINE n=8
BASELINE invariant=True
BASELINE keys=r0000,r0001,r0002,r0003,r0004,r0005,r0006,r0007
```

`reset` 只重建确定性的进程内 fixture，不写数据库、不教授 storage mechanism。

## 2. Predict operation counts — 先写再跑

**现在先不要运行 `counts`。** 对 `n = 8, 16, 32, 64` 预测：

- one pass：每条 record 访问一次，count 是多少？
- nested pair comparisons：每一对不同 records 比一次，count 怎样增长？
- repeated halving：把 `n` 连续除以 2 直到 1，需要多少步？

然后运行：

```bash
python3 activity.py counts
```

你应观察：

```text
COUNTS 8 8 28 3
COUNTS 16 16 120 4
COUNTS 32 32 496 5
COUNTS 64 64 2016 6
COUNTS labels one_pass=O(n) nested_pairs=O(n^2) halving=O(log n)
```

列的单位分别是：record visits、pair comparisons、halving steps。**不是 ms。**

## 3. Predict lookup comparison

本活动对两条路径定义不同但明确的 counted operation：

- linear list scan：一次 `record.key == target` 算一次 **key comparison**；
- key-based index：一次 `index.get(key)` 算一次 **logical key probe**。

这不是说 hash、equality、memory access 或 Python execution 真的只要一条机器指令。

先预测 target 在最后一条 record 时，`n = 8 / 64 / 1024` 的 linear count。再预测 index build 需要多少次 key insertion。

运行：

```bash
python3 activity.py compare
```

关键 observation：

```text
LOOKUP 8 r0007 8 1 8
LOOKUP 64 r0063 64 1 64
LOOKUP 1024 r1023 1024 1 1024
LOOKUP note=indexed_count is a logical interface probe, not free machine work
```

不要把不同列直接当同一机器成本相加。这里要判断的是**增长、workload 与额外结构成本**。

## 4. Specification / Invariant checkpoint

在运行 break 前，用自己的话先写：

**Specification candidate**

- `lookup(k)`：存在 key 时返回那条 record；缺失时返回 `None`；lookup 不改变 collection。
- `update(k, v)`：key 存在时只更新该 key 的 value；key 缺失时返回失败且 state 不变。

**Invariant candidate**

- records 中每个 key 恰好出现一次；
- index 与 records 有完全相同的 key 集合；
- `index[k]` 总指向 records 中 key 为 `k` 的位置。

## 5. Controlled break — duplicate counterexample

先预测：如果错误 update 不是替换旧 record，而是**追加一个同 key record**，同时让 index 指向新位置，会发生什么？

运行：

```bash
python3 activity.py break
```

关键 observation：

```text
BREAK counterexample=duplicate-update key=r0002 new_value=999
BREAK after.invariant=False
BREAK linear=r0002:20 comparisons=3
BREAK indexed=r0002:999 logical_probes=1
BREAK paths_agree=False
```

这不是“随机 bug”。这是一个具体 counterexample：同一个 logical lookup，因为 invariant 被破坏，两条允许的实现路径返回不同 state。

## 6. Corrected path + missing boundary

运行：

```bash
python3 activity.py correct
```

关键 observation：

```text
CORRECT invariant=True
CORRECT linear=r0002:999 indexed=r0002:999
CORRECT paths_agree=True
CORRECT missing.updated=False unchanged=True
```

修正路径在既有位置替换 record；missing key 则不创建新 record。这正对应本活动的 bounded specification。

## 7. 一条命令复查完整 flow

```bash
python3 activity.py flow
```

它按顺序执行：

`reset → baseline → counts → compare → break → correct → reset`

末尾 reset 应再次显示：

```text
RESET invariant=True
RESET first=r0000:0 last=r0007:70
```

## 8. 自动检查

```bash
python3 -m unittest -v test_activity.py
```

自动检查包括：

- fixed one-pass / pairwise / halving counts；
- bounded asymptotic labels；
- last-key 与 missing-key exact counts；
- baseline invariant；
- duplicate counterexample 必然破坏 invariant；
- flawed state 下 linear/indexed lookup 必然 disagree；
- corrected update 恢复 agreement 并保持 invariant；
- missing update 不改变 state；
- two-reset determinism；
- 完整 flow 包含 required cycle。

## Transfer｜不要只背“hash 快”

换一个 workload：只有 `n=8`，collection 建好后只 lookup 一次，随后丢弃。你还会无条件先建 index 吗？

你的判断至少要写：

- workload；
- operation being optimized；
- expected gain；
- build/maintenance/memory cost；
- constraint；
- **When NOT to use**。

不要提前用 M04 的 cache/locality mechanism 解释 measured runtime。现在只需要承认 constants、layout、runtime effects 等 bounded implementation factors 可能影响具体 timing，因此 asymptotic label 不能替代所有 benchmark decision。

## 停止点

现在不要研究：

- Python hash-table internals；
- cache / locality mechanisms；
- CPU / memory hierarchy；
- database indexes；
- persistence / durability；
- concurrency；
- NP-completeness、reductions、Turing machines；
- formal correctness proof systems。

## Provenance / License

- Activity design/code are original Essential CS material for Issue #38, derived from the accepted Foundations/System Mechanics Research Dossier §§5, 8–9, 12 and Design §5/§8.
- External designer/source anchors are recorded in the Lessons: Open Data Structures, MIT Mathematics for Computer Science, Cornell CS2110, and Software Foundations.
- No third-party code, data, or figures are copied into this activity.
- D-016 applies: original code/tools use Apache-2.0; original educational prose/diagrams use CC BY-SA 4.0.
