# M00–M01 Shared Activity — 路径、证据与表示

> 这是 M00–M01 的共享 **Lesson activity surface**，不是 Required Lab，也没有 Lab ID。

这个小活动只暴露本阶段需要观察的机制：

`输入 → 接口 → 进程内状态 → 表示/序列化 → 课程提供的 save/load 边界 → 输出`

其中 save/load 的内部机制在 M00–M01 **故意保持不透明**。你可以观察“另一次调用取回了数据”，但不要把它写成“已经证明持久性（durability）”。持久性的正式定义和机制在后续模块。

## 你会操作什么

活动基线记录：

```json
{
  "id": 513,
  "delta": -2,
  "text": "A中"
}
```

规范化的活动记录使用一个很小的字节格式：

| 字段 | 大小 | 本活动的解释 |
|---|---:|---|
| `magic` | 4 bytes | 固定 `ECS1` |
| `id` | 2 bytes | 无符号 16-bit integer，little-endian |
| `delta` | 2 bytes | 有符号 16-bit two's-complement integer，little-endian |
| `text_len` | 2 bytes | UTF-8 字节长度，little-endian |
| `text` | variable | UTF-8 bytes |

基线应得到 **14 bytes**：

```text
45 43 53 31 01 02 fe ff 04 00 41 e4 b8 ad
```

这串字节是教学活动自身的原创格式，不对应任何外部文件格式、协议或数据库格式。

## 预检

从仓库根目录进入活动目录：

```bash
cd labs/foundations/m00-m01
python3 --version
```

课程设计目标环境是 Python 3.12；若你的版本不同，先把实际版本记入 evidence template。这里的代码只使用 Python 标准库，不要求网络、管理员权限或第三方包。

## 基线

先恢复确定性基线：

```bash
python3 reset.py
python3 activity.py run
```

关键输出应包含：

```text
INPUT id=513 delta=-2 text='A中'
INTERFACE accept_record
STATE records=1 current_text='A中'
OUTPUT bytes=14 hex=45 43 53 31 01 02 fe ff 04 00 41 e4 b8 ad
ROUNDTRIP ok=True
```

## 检查一个边界

```bash
python3 activity.py inspect
```

你应看到字段 offset、每个字段的 exact bytes、UTF-8 code point/bytes 与字节计数。这里检查的是**序列化边界**，不是底层存储机制。

## 做且只做一个受控改动

先写下预测，然后运行：

```bash
python3 change.py
git diff -- input.json
python3 activity.py run
```

`change.py` 只会把 `text` 从 `A中` 改成 `A文`；如果基线不对，它会拒绝继续。保存 `git diff` 作为变更证据。

改动后的 payload 应仍为 14 bytes，但最后 4 个 text bytes 变为：

```text
41 e6 96 87
```

## 重置

```bash
python3 reset.py
git diff -- input.json
python3 activity.py run
```

重置后 `input.json` 应回到基线；若仓库原先干净，针对这个文件的 diff 应为空，活动输出也应回到基线字节。

## M01 观察命令

```bash
python3 activity.py ranges
python3 activity.py endian
python3 activity.py break-endian
python3 activity.py break-utf8
python3 activity.py break-record
python3 activity.py inspect
python3 activity.py load
```

这些命令分别提供：

- 16-bit signed/unsigned 范围与 `-2` 的 two's-complement bit pattern；
- 同一 `513` 在 little-endian / big-endian 下的不同 bytes；
- 用错误 byte order 解码得到 `258` 的安全失败；
- 截断 UTF-8 后得到 `UnicodeDecodeError` 的安全失败；
- 截断 compact record 后，因为声明长度与实际 payload 不一致而被拒绝；
- compact record 的 exact-byte inspection；
- 通过不透明 save/load 边界取回上一份记录的观察。

最后一项只说明**这个 fixture 在这次环境与操作下返回了之前保存的数据**，不说明它面对崩溃、断电或其他失败边界时有什么保证。

## 自动检查

```bash
python3 -m unittest -v test_activity.py
```

检查包括：

- 基线 exact bytes；
- UTF-8 expected bytes；
- 显式 little/big endian encode/decode；
- signed/unsigned 边界；
- bounded round trip；
- controlled change → changed bytes → deterministic reset；
- save/load 窄边界；
- truncated UTF-8 failure；
- truncated record / declared-length mismatch failure。

## 文件角色

- `activity.py`：学习者可观察的输入、接口、进程内状态、表示与输出路径。
- `input.json`：受控改动的 tracked input。
- `fixtures/baseline-input.json`：确定性 reset 基线。
- `change.py`：只修改一个字段的受控改动器。
- `reset.py`：恢复输入和课程提供的 fixture state。
- `opaque_store.py`：课程提供的 save/load 边界；M00–M01 不以其内部机制为学习对象。
- `test_activity.py`：标准库 `unittest` 自动检查。

## 停止点

现在不要研究：SQL、数据库内部、事务、日志/WAL、fsync/writeback、恢复、文件系统机制、存储层次、网络、并发或操作系统内部。它们都不是这个 activity 的前置知识。

## Provenance / License

- Activity design and code are original Essential CS material created for Issue #29.
- No third-party code, data, or figures are copied into this activity.
- Repository decision D-016 applies: original code/tools use Apache-2.0; original educational prose/diagrams use CC BY-SA 4.0.
- Technical source anchors used by the Lessons are recorded in the Lesson provenance sections; the activity's fixed record format itself is course-owned and intentionally synthetic.
