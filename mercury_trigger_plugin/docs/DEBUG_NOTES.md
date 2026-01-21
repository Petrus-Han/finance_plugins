# Mercury Trigger Plugin 调试笔记

## 已修复问题

### 1. Webhook 签名验证失败 (2026-01-20)

**问题现象**:
```
[MERCURY] ERROR: Invalid webhook signature
TriggerValidationError: Invalid webhook signature
```

**根本原因**:
签名验证代码错误地对 Mercury 返回的 secret 进行了 base64 解码。

**错误代码** (`provider/mercury.py`):
```python
try:
    secret_bytes = base64.b64decode(secret)  # 错误！
except Exception:
    secret_bytes = secret.encode()
```

**修复方案**:
Mercury 官方文档明确说明签名验证时应**直接使用 secret 字符串**，不需要 base64 解码。

```python
# Mercury uses the secret key directly (not base64 decoded)
# See: https://docs.mercury.com/reference/verifying-webhook-signatures
secret_bytes = secret.encode()
```

**参考文档**: https://docs.mercury.com/reference/verifying-webhook-signatures

---

## Mercury Webhook 签名验证机制

### 签名格式

Header: `Mercury-Signature: t=<timestamp>,v1=<signature>`

- `t` = Unix 时间戳（秒）
- `v1` = HMAC-SHA256 签名（十六进制）

### 验证步骤

1. 从 `Mercury-Signature` header 提取 timestamp 和 signature
2. 构造签名载荷: `{timestamp}.{request_body}`
3. 使用 secret **直接** 计算 HMAC-SHA256
4. 比较计算结果与收到的签名

### Python 实现

```python
import hmac
import hashlib

def verify_signature(body: str, signature_header: str, secret: str) -> bool:
    # 解析 header
    parts = dict(p.split("=", 1) for p in signature_header.split(","))
    timestamp = parts.get("t")
    signature = parts.get("v1")

    # 构造签名载荷
    signed_payload = f"{timestamp}.{body}"

    # 计算签名 - 直接使用 secret，不解码
    expected = hmac.new(
        secret.encode(),  # 直接 encode，不 base64 decode
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected)
```

---

## 调试方法

### 1. 查看日志

```bash
tail -f /tmp/mercury_trigger.log
```

### 2. 重启插件

```bash
# 杀掉旧进程
pkill -f "mercury_trigger_plugin.*main"

# 启动新进程
cd /home/ubuntu/playground/finance_plugins/mercury_trigger_plugin
uv run python main.py > /tmp/mercury_trigger.log 2>&1 &
```

### 3. 检查连接状态

```bash
grep "Connected" /tmp/mercury_trigger.log
```

### 4. 手动验证签名

```python
import hmac
import hashlib

# 从日志获取这些值
body = '{"id":"xxx",...}'
timestamp = "1768910555"
received_signature = "8ea8ab11d2c975f8..."
secret = "zkQ8Fta/F9RwZIFxRtUWOS1S3qin1V/oOvlnBYpkQyg="

signed_payload = f"{timestamp}.{body}"
computed = hmac.new(
    secret.encode(),
    signed_payload.encode(),
    hashlib.sha256
).hexdigest()

print(f"Received:  {received_signature}")
print(f"Computed:  {computed}")
print(f"Match: {received_signature == computed}")
```

---

## 关键文件

| 文件 | 说明 |
|------|------|
| `provider/mercury.py` | Trigger 主逻辑，包含签名验证 |
| `provider/mercury.yaml` | Provider 配置，定义凭证 |
| `.env` | 远程调试配置 |

---

## 远程调试配置

`.env` 文件内容:
```
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=dify.greeep.com
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=<your-debug-key>
PLUGIN_DEBUG=true
```

获取新的 debug key 后需要更新此文件并重启插件。

---

## Mock Server 测试

```bash
# 启动 mock server
cd /home/ubuntu/playground/finance_plugins
python scripts/mock_mercury_server.py

# Mock API Token
mock_token_12345

# 模拟 webhook 事件
curl -X POST http://localhost:8765/simulate/transaction
```

注意: Mock server 的签名实现需要与 Mercury 官方保持一致（直接使用 secret）。
