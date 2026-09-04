# LAB-REQ-01: HTTP Intermediary Adapter, Conditional Caching & Upstream Failure Mapping

本实验为 **Essential CS Required Lab 01 (LAB-REQ-01)**，紧密衔接 **M11 — Networking II: TLS, HTTP, CDN & Proxies**。通过在本地构建确定性的源站（Origin Server）与中间人代理（Intermediary Adapter），学习者将通过真实的 `curl` 观测 HTTP 统一接口、逐跳首部剥除、代理 `Via` 注入、强 ETag 条件验证（`304 Not Modified` 零主体字节）以及上游故障映射（`502 Bad Gateway`）。

---

## 1. 实验架构与设计原则

```
+----------------+          HTTP/1.1          +--------------------------+          HTTP/1.1          +-------------------+
|                |  ----------------------->  |                          |  ----------------------->  |                   |
|  Client (curl) |                            |   Intermediary Adapter   |                            |   Origin Server   |
|                |  <-----------------------  |      (:proxy_port)       |  <-----------------------  |   (:origin_port)  |
+----------------+          Response          +--------------------------+          Response          +-------------------+
                                              - Injects Via: 1.1 ...                                  - /resource (200/304)
                                              - Strips hop-by-hop headers                             - /health (200)
                                              - Maps outage to 502                                    - ETag: "strong-v1"
```

### 核心设计原则

1. **Course-Owned Loopback Only**：所有监听器均严格绑定在 `127.0.0.1`，绝不暴露外部端口。
2. **Port 0 Dynamic Allocation**：Origin 与 Proxy 启动时均请求内核动态分配端口（Port 0），并在就绪时向 stdout 打印 `ORIGIN_READY_PORT=<port>` 和 `PROXY_READY_PORT=<port>`，彻底消除端口冲突。
3. **Strict HTTP Intermediary Semantics**：
   - 遵循 RFC 9110 Section 7.6.1，彻底剥除逐跳首部（`Connection`, `Keep-Alive`, `Proxy-Authenticate`, `Proxy-Authorization`, `TE`, `Trailers`, `Transfer-Encoding`, `Upgrade`），杜绝逐跳首部穿越代理层；
   - 注入中间人标识首部：`Via: 1.1 essential-cs-intermediary`；
   - 严格映射上游故障：当 Origin 无法连接或被终止时，Proxy 必须向客户端返回 `502 Bad Gateway`，不可静默崩溃或虚报 200。
4. **Conditional Caching & Zero Body Bytes**：
   - 当客户端在 `If-None-Match` 中携带匹配的强 ETag 时，Origin 与 Proxy 返回 `304 Not Modified`；
   - 遵循 RFC 9111 Section 4.1，`304` 响应报文绝对不携带任何正文数据（Body Bytes == 0）。

---

## 2. 文件清单与职责划分

| 文件 | 核心职责 |
|---|---|
| `origin_server.py` | 源站服务：动态绑定端口 0；打印 `ORIGIN_READY_PORT=<port>`；提供 `/resource`（返回 200 与强 ETag `"strong-v1"`；匹配 `If-None-Match` 时返回 304 零主体）和 `/health`。 |
| `intermediary_adapter.py` | 中间人反向代理：动态绑定端口 0；接收 `--origin-port` 参数；打印 `PROXY_READY_PORT=<port>`；转发请求并注入 `Via: 1.1 essential-cs-intermediary`；处理逐跳首部；在上游断连时返回 `502 Bad Gateway`。 |
| `harness.py` | 自动化编排器：按序启动 Origin 与 Proxy，捕获动态端口，使用宿主机真实的 `curl` 执行 4 步完整交互追踪，并在退出时可靠清理所有子进程（保证 0 孤儿进程）。 |
| `test_lab.py` | 自动化测试套件：覆盖 Origin 单体语义、Proxy 单体 502 故障映射、4 步全链路追踪以及重置脚本的幂等性。 |
| `reset.py` | 幂等清理脚本：验证无残留后台孤儿进程与持久状态，输出 `CLEAN_NO_PERSISTENT_ARTIFACTS`。 |
| `README.md` | 本实验指南与操作手册。 |
| `.gitignore` | 忽略 Python 缓存与临时文件。 |

---

## 3. 四步验证链路详解 (The 4-Step Trace)

编排器与学习者手动实验均覆盖以下 4 个阶段：

### 步骤 1：直接向源站发起无缓存请求 (Direct Origin Request)
- **命令示例**：
  ```bash
  curl -s -i http://127.0.0.1:<origin_port>/resource
  ```
- **预期现象**：
  - 状态码：`200 OK`
  - 响应首部包含强验证器：`ETag: "strong-v1"`
  - 响应主体为完整的 JSON 数据（如 `{"message": "Hello from origin server", ...}`）。

### 步骤 2：通过代理向源站发起请求 (Forwarded Proxy Request)
- **命令示例**：
  ```bash
  curl -s -i http://127.0.0.1:<proxy_port>/resource
  ```
- **预期现象**：
  - 状态码：`200 OK`
  - 响应首部注入了中间人链路信息：`Via: 1.1 essential-cs-intermediary`
  - 响应首部保留源站的 `ETag: "strong-v1"`
  - 响应主体与步骤 1 完全一致。

### 步骤 3：通过代理发起带验证器的条件请求 (Conditional 304 via Proxy)
- **命令示例**：
  ```bash
  curl -s -i -H 'If-None-Match: "strong-v1"' http://127.0.0.1:<proxy_port>/resource
  ```
- **预期现象**：
  - 状态码：`304 Not Modified`
  - 响应首部保留 `Via: 1.1 essential-cs-intermediary` 与 `ETag`
  - **关键机制**：响应主体长度严格为 **0 字节**（验证了缓存验证节省带宽的核心价值）。

### 步骤 4：源站下线后的故障映射观测 (Upstream Failure Mapping -> 502)
- **动作**：终止源站进程（模拟源站崩溃或网络分区）。
- **命令示例**：
  ```bash
  curl -s -i http://127.0.0.1:<proxy_port>/resource
  ```
- **预期现象**：
  - 状态码：`502 Bad Gateway`
  - 响应首部包含 `Via: 1.1 essential-cs-intermediary`
  - 响应主体包含结构化上游故障诊断信息（如 `{"error": "Bad Gateway", "reason": "Origin server unreachable..."}`）。

---

## 4. 运行与验证

### 4.1 自动化运行 4 步全链路追踪

直接运行自动化编排器：

```bash
python labs/lab_req_01/harness.py
```

或输出 JSON 格式供程序化消费：

```bash
python labs/lab_req_01/harness.py --json
```

### 4.2 运行测试套件与重置

```bash
# 运行单元与集成测试套件
python -m unittest discover -s labs/lab_req_01 -p "test_*.py" -v

# 执行幂等重置
python labs/lab_req_01/reset.py
```

### 4.3 常见排查提示

- **端口占用与权限**：本实验所有服务均绑定 `127.0.0.1` 且端口为 `0`，无需任何管理员特权。如遇防火墙拦截本地 loopback 连接，请配置本地环回放行。
- **curl 依赖**：编排器调用宿主机原生的 `curl` 命令。在运行前请确认 `tests/preflight_network_web.py` 显示 `curl` 可用。
