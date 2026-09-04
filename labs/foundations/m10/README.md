# Module M10 Activity Suite: Networking I (IP, DNS & Transport)

本活动套件服务于 **M10 — Networking I: IP, DNS & Transport**，为学习者提供严谨、安全、可复现的本地网络机制观察环境。

---

## 1. 核心安全与环境原则

- **Course-Owned Loopback Only**：所有监听端点默认严格绑定在 `127.0.0.1`；绝不向公网暴露服务。
- **Port 0 Dynamic Allocation**：所有测试套件请求操作系统内核动态分配可用临时端口（Ephemeral Port），杜绝硬编码固定端口引发的端口冲突。
- **No Root / Privilege Escalation**：所有活动均在普通无特权用户态执行；不需要 `sudo`、管理员特权、Packet Injection（原始套接字注入）或 ARP/DNS 污染。
- **No Brittle Assertions**：活动绝不硬编码假设 `ECONNREFUSED == 111`、特定异常文本、或固定的时延比率；所有测试如实记录宿主机的运行时表现与能力。

---

## 2. 文件清单与职责划分

| 文件名 | 对应课程 | 核心机制与职责 |
|---|---|---|
| `endpoint_observer.py` | `L10-01` | 绑定动态端口 0；观察 `getsockname()` 结果；验证名称、地址、路由与端口/进程解耦；执行 16 字节回显交互。 |
| `stream_framing.py` | `L10-02` | 观察 TCP 无结构有序字节流与分片/合并行为；运行定界/长度前缀解析循环；对比 UDP 报文边界与 IPv4/IPv6 校验和规则。 |
| `failure_fixture.py` | `L10-03` | 观察受控本地拒绝（未绑定端口）、已接受但静默超时（服务端握手后不发数据）、及保留域名 `.invalid` 的 DNS 解析失败；阐释部分失败歧义与重试风险。 |
| `reset.py` | 全部 | 幂等清理脚本；确保所有套接字安全关闭，检验端点不再服务。 |
| `test_activity.py` | 全部 | 自动化单元测试套件（`unittest`），验证全部机制不变式。 |

---

## 3. 快速上手指南

### 3.1 环境预检

在运行任何网络活动之前，先在项目根目录下运行预检脚本：

```bash
python tests/preflight_network_web.py
```

或输出结构化 JSON：

```bash
python tests/preflight_network_web.py --json
```

### 3.2 观察本地端点与端口解耦 (L10-01)

```bash
python labs/foundations/m10/endpoint_observer.py
```

观察输出中：
- 内核实际分配的非零临时端口；
- 当前进程 PID 与端口的区别；
- 宿主机可选工具（`ss`、`ip route`）的可用性状态。

### 3.3 观察 TCP 字节流重构与 UDP 边界 (L10-02)

```bash
python labs/foundations/m10/stream_framing.py
```

观察输出中：
- 接收端实际观测到的 `recv()` 分片（Partitions）；
- 应用层长度前缀定界循环如何跨越任意切片拼装出完整的消息；
- UDP 如何每次 `recvfrom()` 单独保留独立的报文边界。

### 3.4 观测网络故障谱系与部分失败 (L10-03)

```bash
python labs/foundations/m10/failure_fixture.py
```

观察三种不同的故障场景：
1. **未绑定端口连接拒绝**：如实记录宿主机抛出的 `ConnectionRefusedError`（或平台等价错误码）及瞬态耗时；
2. **已建连但静默超时**：客户端等待超过指定的 Read Deadline 后触发 `TimeoutError`；
3. **保留域名解析失败**：针对 RFC 2606 的 `.invalid` 保留顶级域名发起查询，如实记录解析器失败信息。

### 3.5 运行全量自动化测试与重置

```bash
python -m unittest discover -s labs/foundations/m10 -p "test_*.py" -v
python labs/foundations/m10/reset.py
```
