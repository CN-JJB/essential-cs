# Module M11 Activity Suite: Networking II (TLS, HTTP, CDN & Proxies)

本活动套件服务于 **M11 — Networking II: TLS, HTTP, CDN & Proxies**，为学习者提供严谨、安全、可复现的现代网络协议与语义机制观察环境。

---

## 1. 核心安全与设计原则

- **Course-Owned Loopback Only**：所有监听端点严格绑定在 `127.0.0.1`，绝不向外部公网暴露。
- **Port 0 Dynamic Allocation**：所有套接字端点使用端口 `0` 由操作系统内核动态分配临时端口（Ephemeral Port），杜绝硬编码端口引发的冲突。
- **Strict Verification, Zero Bypass**：严格杜绝任何验证跳过标志（如 `verify=False`、`check_hostname=False`、`curl -k`）。验证必须通过显式加载受控测试根证书上下文（CA context）完成。
- **Identity vs Trust Path**：严格区分主体身份认证（Subject Alternative Name, SAN）与信任锚路径校验（CA 链签发信任）。
- **Protocol Outcome != Business Outcome**：HTTP 协议状态码（如 `200 OK`）表示传输请求被成功处理，并不等同于业务层面的成功（如业务错误 JSON）；HTTP 语义与业务载荷明确解耦。
- **Idempotence Semantics**：幂等（Idempotent）操作承诺多次重复执行与单次执行具有相同的服务端目标资源状态影响，但并不承诺在遇到部分失败（Partial Failure）或网络超时时可以无脑盲目重试。
- **Freshness vs Validation**：严格区分客户端/缓存本地的新鲜度判定（Freshness）与携带验证器（`If-None-Match: <ETag>`）发起的条件验证（Validation）。304 响应必须不包含报文主体（Zero Body Bytes）。强 ETag 为不透明验证器（Opaque Validator）。
- **No Universal Transport Winner**：HTTP/1.1、HTTP/2 与 HTTP/3 各自权衡，不存在全场景绝对优胜者。

---

## 2. 文件清单与职责划分

| 文件/目录 | 对应课程 | 核心机制与职责 |
|---|---|---|
| `certs/` | `L11-01` | 自包含受控测试 PKI：包含生成脚本 `generate_certs.py`、根 CA（`ca.pem`）、服务端证书（`server.pem`，SAN 包含 `localhost` 和 `127.0.0.1`）、未受信任 CA（`untrusted_ca.pem`）。有效期统一为 10 年（至 2036 年），符合 RFC 5280 扩展规范。 |
| `tls_fixture.py` | `L11-01` | 演示 TLS 1.3 握手与证书验证的三种关键路径：（1）受信任根 CA 下成功建立 TLS 1.3 握手；（2）主机名不匹配（如连接 `127.0.0.1` 却指定 `wrong.example.internal`）被拒绝并抛出 `SSLCertVerificationError`；（3）未受信任的根 CA 签发证书被拒绝并抛出 `SSLCertVerificationError`。零跳过标志。 |
| `http_semantics_observer.py` | `L11-02` | 观察 HTTP 统一接口语义：资源与表述解耦、安全（Safe GET）与幂等（Idempotent PUT vs Non-idempotent POST）语义、协议层状态码与业务层执行结果的区别（`200 OK` 与 `{"error": ...}` 并存）、原始 CRLF（`\r\n`）线缆帧结构。 |
| `caching_observer.py` | `L11-03` | 观察 HTTP 缓存机制：新鲜度（Freshness）与条件验证（Validation）、强 ETag 不透明验证器、`304 Not Modified` 响应报文零主体（Zero Body Bytes）、HTTP/1.1 / HTTP/2 / HTTP/3 架构权衡对比。 |
| `reset.py` | 全部 | 幂等重置脚本，清理临时文件与进程状态，报告 `CLEAN_NO_PERSISTENT_ARTIFACTS`。 |
| `test_activity.py` | 全部 | 自动化单元测试套件（`unittest`），覆盖 TLS 验证三路径、HTTP 语义、缓存与 304 零主体、重置幂等性。 |

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

输出应包含 `READY_M11_CORE_AND_LAB_REQ_01`。

### 3.2 运行 TLS 1.3 握手与证书校验机制观察 (L11-01)

```bash
python labs/foundations/m11/tls_fixture.py
```

观察输出中：
- 动态分配的 TLS 监听端口；
- TLS 1.3 协商协议与密码套件（Cipher Suite）；
- 主机名不匹配和未受信任根证书时的握手拒绝行为与异常类型。

### 3.3 观察 HTTP 语义与协议/业务解耦 (L11-02)

```bash
python labs/foundations/m11/http_semantics_observer.py
```

观察输出中：
- GET 请求的只读安全性与幂等性；
- PUT 重复执行对资源状态的一致性影响；
- POST 重复执行生成的递增资源标识符；
- 协议状态码 `200 OK` 下返回业务错误 `{"success": false, "code": "ERR_INSUFFICIENT_FUNDS"}`；
- 原始 HTTP/1.1 线缆首部结尾与空行严格由 `\r\n\r\n` 构成。

### 3.4 观察缓存新鲜度、ETag 条件验证与 304 (L11-03)

```bash
python labs/foundations/m11/caching_observer.py
```

观察输出中：
- 初次请求获取强 ETag（例如 `"v1-a1b2c3d4"`）；
- 客户端在验证期携带 `If-None-Match` 发起条件 GET 请求；
- 服务端返回 `304 Not Modified`，接收到的主体长度严格为 `0` 字节；
- 资源更新后，新请求获取到新 ETag 与更新后的主体。

### 3.5 运行全量自动化测试与重置

```bash
python -m unittest discover -s labs/foundations/m11 -p "test_*.py" -v
python labs/foundations/m11/reset.py
```
