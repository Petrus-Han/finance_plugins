# Mercury Webhook 调试计划

## 问题隔离：5个环节逐一排查

### 环节 1: Webhook 注册是否成功？

**验证方法**: 调用 Mercury API 查看已注册的 webhooks

```bash
# 用你的 Production API token
curl -X GET "https://api.mercury.com/api/v1/webhooks" \
  -H "Authorization: Bearer YOUR_MERCURY_API_TOKEN" \
  -H "Accept: application/json"
```

**预期结果**: 应该看到你注册的 webhook URL

**可能问题**:
- 空数组 `[]` → 注册失败
- URL 不是 Dify 的 webhook URL → 注册了错误的 URL

---

### 环节 2: Mercury 是否发送 Webhook？

**验证方法**: 用 webhook.site 创建临时接收端

1. 访问 https://webhook.site 获取一个临时 URL
2. 用该 URL 创建 Mercury webhook:

```bash
curl -X POST "https://api.mercury.com/api/v1/webhooks" \
  -H "Authorization: Bearer YOUR_MERCURY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://webhook.site/YOUR-UNIQUE-ID",
    "eventTypes": ["transaction.created", "transaction.updated"]
  }'
```

3. 在 Mercury 账户中触发一笔交易（转账、消费等）
4. 检查 webhook.site 是否收到请求

**预期结果**: webhook.site 应显示收到的 POST 请求

**可能问题**:
- 没收到任何请求 → Mercury 没有发送 webhook（可能是配置问题或 Mercury 延迟）
- 收到请求但 Dify 没收到 → Dify 端问题

---

### 环节 3: Dify 是否收到请求？

**验证方法**: 检查 Dify 日志

```bash
# 如果是 docker 部署
docker logs dify-api 2>&1 | grep -i webhook

# 如果是 k8s 部署
kubectl logs -l app=dify-api | grep -i webhook
```

**预期结果**: 应该看到 webhook 请求日志

---

### 环节 4: 签名验证是否通过？

**潜在问题**: Mercury webhook secret 的处理

代码中 (mercury.py:109-112):
```python
try:
    secret_bytes = base64.b64decode(secret)
except Exception:
    secret_bytes = secret.encode()  # 静默回退
```

**验证方法**: 在插件代码中添加调试日志

```python
# mercury.py _validate_signature 方法中添加
print(f"DEBUG: Received signature header: {request.headers.get('Mercury-Signature')}")
print(f"DEBUG: Stored webhook_secret: {secret[:10]}...")  # 只打印前10字符
print(f"DEBUG: Calculated signature: {expected}")
```

---

### 环节 5: 事件处理是否正确？

**已发现的问题**: `operation_filter` 参数定义了但没有使用！

文件: `events/transaction.py`

用户可以选择 "只处理 created" 或 "只处理 updated"，但代码没有实现过滤逻辑。

---

## 快速诊断脚本

创建一个诊断脚本来测试 Mercury API:

```python
#!/usr/bin/env python3
"""Mercury Webhook 诊断脚本"""

import requests
import sys

API_TOKEN = "YOUR_MERCURY_PRODUCTION_TOKEN"
BASE_URL = "https://api.mercury.com/api/v1"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def check_auth():
    """检查 API 认证"""
    print("1. 检查 API 认证...")
    resp = requests.get(f"{BASE_URL}/accounts", headers=headers, timeout=15)
    if resp.status_code == 200:
        accounts = resp.json().get("accounts", [])
        print(f"   ✅ 认证成功，找到 {len(accounts)} 个账户")
        return True
    else:
        print(f"   ❌ 认证失败: {resp.status_code} - {resp.text}")
        return False

def list_webhooks():
    """列出所有 webhooks"""
    print("\n2. 列出已注册的 webhooks...")
    resp = requests.get(f"{BASE_URL}/webhooks", headers=headers, timeout=15)
    if resp.status_code == 200:
        webhooks = resp.json().get("webhooks", resp.json())
        if isinstance(webhooks, list):
            print(f"   找到 {len(webhooks)} 个 webhook:")
            for wh in webhooks:
                print(f"   - ID: {wh.get('id')}")
                print(f"     URL: {wh.get('url')}")
                print(f"     Status: {wh.get('status')}")
                print(f"     Events: {wh.get('eventTypes')}")
        else:
            print(f"   响应: {webhooks}")
        return webhooks
    else:
        print(f"   ❌ 获取失败: {resp.status_code} - {resp.text}")
        return []

def create_test_webhook(url):
    """创建测试 webhook"""
    print(f"\n3. 创建测试 webhook: {url}")
    payload = {
        "url": url,
        "eventTypes": ["transaction.created", "transaction.updated"]
    }
    resp = requests.post(f"{BASE_URL}/webhooks", headers=headers, json=payload, timeout=15)
    if resp.status_code in [200, 201]:
        result = resp.json()
        print(f"   ✅ 创建成功:")
        print(f"   - ID: {result.get('id')}")
        print(f"   - Secret: {result.get('secret', 'N/A')[:20]}...")
        return result
    else:
        print(f"   ❌ 创建失败: {resp.status_code} - {resp.text}")
        return None

def delete_webhook(webhook_id):
    """删除 webhook"""
    print(f"\n删除 webhook: {webhook_id}")
    resp = requests.delete(f"{BASE_URL}/webhooks/{webhook_id}", headers=headers, timeout=15)
    if resp.status_code in [200, 204]:
        print(f"   ✅ 删除成功")
    else:
        print(f"   ❌ 删除失败: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    if not check_auth():
        sys.exit(1)

    webhooks = list_webhooks()

    # 如果需要创建测试 webhook，取消下面的注释
    # test_url = "https://webhook.site/your-unique-id"
    # create_test_webhook(test_url)
```

---

## 执行顺序

1. **运行诊断脚本** → 确认 API 认证和现有 webhook 状态
2. **用 webhook.site 测试** → 确认 Mercury 是否发送 webhook
3. **检查 Dify 日志** → 确认请求是否到达 Dify
4. **添加调试日志** → 定位签名验证或事件处理问题

---

## 下一步

确认哪个环节出问题后，针对性修复：

| 环节 | 如果失败 | 修复方案 |
|------|----------|----------|
| 1. 注册 | API 返回错误 | 检查 token 权限、URL 格式 |
| 2. 发送 | webhook.site 没收到 | 联系 Mercury 支持 |
| 3. 接收 | Dify 日志无记录 | 检查 Dify 网络配置 |
| 4. 验证 | 签名不匹配 | 修复 secret 编码逻辑 |
| 5. 处理 | 事件不触发 workflow | 修复 _on_event 逻辑 |

---

## 本地测试工具 (推荐)

由于 Mercury Sandbox 不支持 webhook，我们创建了完整的本地测试环境：

### 快速开始

```bash
# 终端 1: 启动 Mock Mercury 服务器
python scripts/mock_mercury_server.py

# 终端 2: 启动 Webhook 接收器
python scripts/webhook_receiver.py

# 终端 3: 运行自动化测试
python scripts/test_webhook_flow.py -v
```

### 工具说明

| 脚本 | 用途 |
|------|------|
| `mock_mercury_server.py` | 模拟完整 Mercury API，支持 webhook 注册和事件发送 |
| `webhook_receiver.py` | 模拟 Dify 端点，接收 webhook 并验证签名 |
| `test_webhook_flow.py` | 自动化端到端测试 |
| `diagnose_mercury_webhook.py` | 生产环境诊断工具 |

### 测试流程

1. **启动 mock 服务器** - 模拟 Mercury API
2. **注册 webhook** - 模拟 Dify plugin 的订阅流程
3. **触发事件** - `curl -X POST http://localhost:8765/simulate/transaction`
4. **验证接收** - 在 webhook_receiver 控制台查看

详见 `scripts/README.md`
