# Finance Plugins 完整测试指南

本文档提供 Finance Plugins 项目的完整测试指南，包括单元测试、集成测试和远程调试。

## 目录

- [环境准备](#环境准备)
- [插件概览](#插件概览)
- [单元测试](#单元测试)
- [集成测试](#集成测试)
- [远程调试](#远程调试)
- [Mock Server](#mock-server)
- [常见问题](#常见问题)

---

## 环境准备

### 1. 克隆仓库

```bash
git clone https://github.com/Petrus-Han/finance_plugins.git
cd finance_plugins
git checkout dev/alai-sudo
```

### 2. 创建虚拟环境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
# 或者使用 uv
uv sync
```

### 4. 验证安装

```bash
python -c "from dify_plugin import Plugin; print('dify_plugin OK')"
pytest --version
```

---

## 插件概览

| 插件 | 类型 | 描述 |
|------|------|------|
| mercury_trigger_plugin | Trigger | Mercury 银行 Webhook 触发器 |
| mercury_tools_plugin | Tool | Mercury 银行 API 工具集 |
| quickbooks_plugin | Tool | QuickBooks Online 会计工具集 |
| quickbooks_payments_plugin | Tool | QuickBooks Payments 支付工具 |

---

## 单元测试

### 运行所有单元测试

```bash
# 激活虚拟环境
source .venv/bin/activate

# Mercury Trigger 插件测试
pytest mercury_trigger_plugin/tests/unit/ -v

# Mercury Tools 插件测试
pytest mercury_tools_plugin/tests/unit/test_tools.py -v

# QuickBooks 插件测试
pytest quickbooks_plugin/tests/unit/ -v
```

### 测试覆盖率

```bash
pytest --cov=mercury_trigger_plugin --cov=mercury_tools_plugin --cov=quickbooks_plugin -v
```

### 预期测试结果

| 插件 | 测试数量 | 预期结果 |
|------|----------|----------|
| Mercury Trigger | 18 | 全部通过 |
| Mercury Tools | 12 | 全部通过 |
| QuickBooks | 15 | 全部通过 |

---

## 集成测试

### 1. 启动 Mock Server

```bash
# 在后台启动 Mock Mercury Server
python3 scripts/mock_mercury_server.py &

# 验证服务器运行
curl http://localhost:8765/health
# 预期返回: {"status": "healthy"}
```

### 2. 运行集成测试

```bash
# Mercury Trigger 集成测试
pytest mercury_trigger_plugin/tests/integration/ -v
```

### 3. 手动测试 Mock Server 端点

```bash
# 获取账户列表
curl -s http://localhost:8765/api/v1/accounts \
  -H "Authorization: Bearer mock_token_12345" | python3 -m json.tool

# 获取交易列表
curl -s "http://localhost:8765/api/v1/account/acc_mock_checking/transactions" \
  -H "Authorization: Bearer mock_token_12345" | python3 -m json.tool

# 测试发送付款
curl -s -X POST http://localhost:8765/api/v1/account/acc_123/request-send-money \
  -H "Authorization: Bearer mock_token_12345" \
  -H "Content-Type: application/json" \
  -d '{"recipientId": "rcp_456", "amount": 500, "paymentMethod": "ach"}'

# 测试内部转账
curl -s -X POST http://localhost:8765/api/v1/transfer \
  -H "Authorization: Bearer mock_token_12345" \
  -H "Content-Type: application/json" \
  -d '{"fromAccountId": "acc_123", "toAccountId": "acc_456", "amount": 1000}'
```

### 4. 测试 Webhook 模拟

```bash
# 模拟交易创建事件
curl -s -X POST http://localhost:8765/api/v1/simulate-event \
  -H "Authorization: Bearer mock_token_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "eventType": "transaction.created",
    "webhookUrl": "http://your-callback-url/webhook",
    "data": {
      "id": "txn_test_123",
      "amount": 1000,
      "status": "completed"
    }
  }'
```

---

## 远程调试

### 1. 配置 .env 文件

每个插件目录下需要一个 `.env` 文件：

```env
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=dify.greeep.com
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=your-debug-key
```

### 2. 获取调试密钥

#### 方法一：通过 Dify 控制台

1. 登录 Dify 控制台
2. 进入 **Plugins → 远程调试**
3. 复制调试密钥

#### 方法二：通过 API 自动获取

```bash
# Step 1: 登录获取 JWT 和 CSRF Token
# 注意：密码需要 Base64 编码
ENCODED_PASS=$(echo -n "your-password" | base64)

curl -X POST "https://dify.greeep.com/console/api/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"your-email\", \"password\": \"$ENCODED_PASS\"}" \
  -c /tmp/dify_cookies.txt

# Step 2: 获取调试密钥
CSRF=$(grep csrf_token /tmp/dify_cookies.txt | awk '{print $7}')

curl -s "https://dify.greeep.com/console/api/workspaces/current/plugin/debugging-key" \
  -b /tmp/dify_cookies.txt \
  -H "X-Csrf-Token: $CSRF"

# 返回: {"key": "your-debug-key", "host": "dify.greeep.com", "port": 5003}
```

#### 一键获取脚本

```bash
#!/bin/bash
# get_debug_key.sh

HOST="dify.greeep.com"
EMAIL="your-email"
PASSWORD="your-password"

PASS=$(echo -n "$PASSWORD" | base64)
curl -s -X POST "https://$HOST/console/api/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}" \
  -c /tmp/dify.txt > /dev/null

CSRF=$(grep csrf_token /tmp/dify.txt | awk '{print $7}')
curl -s "https://$HOST/console/api/workspaces/current/plugin/debugging-key" \
  -b /tmp/dify.txt -H "X-Csrf-Token: $CSRF"
```

### 3. 启动插件远程调试

```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动单个插件
cd mercury_trigger_plugin && python main.py

# 或者同时启动所有插件
cd mercury_trigger_plugin && python main.py > /tmp/mercury_trigger.log 2>&1 &
cd ../mercury_tools_plugin && python main.py > /tmp/mercury_tools.log 2>&1 &
cd ../quickbooks_plugin && python main.py > /tmp/quickbooks.log 2>&1 &
cd ../quickbooks_payments_plugin && python main.py > /tmp/quickbooks_payments.log 2>&1 &
```

### 4. 验证连接

```bash
# 检查日志确认连接成功
grep "Connected\|Installed" /tmp/*.log

# 预期输出:
# Connected to dify.greeep.com:5003
# Installed trigger provider: mercury_trigger
# Installed tool: mercury_tools
# Installed tool: quickbooks
# Installed tool: quickbooks_payments
```

### 5. 在 Dify 中测试

1. 登录 Dify 控制台
2. 创建新的 Workflow 或 Chatflow
3. 添加已安装的工具节点进行测试

---

## Mock Server

### Mock Server 端点列表

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | /health | 健康检查 |
| GET | /api/v1/accounts | 获取账户列表 |
| GET | /api/v1/account/{id} | 获取账户详情 |
| GET | /api/v1/account/{id}/transactions | 获取账户交易 |
| GET | /api/v1/recipients | 获取收款人列表 |
| GET | /api/v1/recipient/{id} | 获取收款人详情 |
| POST | /api/v1/recipient | 创建收款人 |
| GET | /api/v1/categories | 获取分类列表 |
| GET | /api/v1/web-hooks | 获取 Webhook 列表 |
| POST | /api/v1/web-hooks | 创建 Webhook |
| DELETE | /api/v1/web-hooks/{id} | 删除 Webhook |
| POST | /api/v1/simulate-event | 模拟 Webhook 事件 |
| POST | /api/v1/account/{id}/request-send-money | 发起付款请求 |
| POST | /api/v1/transfer | 创建内部转账 |

### Mock 认证

所有 API 请求需要携带 Authorization header：

```bash
-H "Authorization: Bearer mock_token_12345"
```

---

## 常见问题

### 1. ModuleNotFoundError: dify_plugin

```bash
pip install dify_plugin
# 或
uv add dify_plugin
```

### 2. Handshake Failed / Invalid Key

- 检查 `.env` 文件中的 `REMOTE_INSTALL_KEY` 是否正确
- 重新获取调试密钥
- 确保 Dify 版本 >= 1.10

### 3. YAML Validation Error

检查工具 YAML 文件是否包含所有必需字段：

```yaml
identity:
  name: tool_name
  author: your_name  # 必需
  label:
    en_US: Tool Label

parameters:
  - name: param_name
    type: string
    required: true
    label:           # 必需
      en_US: Label
    human_description:  # 必需
      en_US: Description
```

### 4. BrokenPipeError

通常表示调试密钥无效或已过期，重新获取密钥即可。

### 5. Port Already in Use

```bash
# 查找并杀死占用端口的进程
fuser -k 8765/tcp

# 重新启动 Mock Server
python3 scripts/mock_mercury_server.py &
```

### 6. 插件未在 Dify 中显示

1. 刷新 Dify 控制台页面
2. 检查日志确认连接成功
3. 注意：Trigger 类型插件在 "触发器" 部分显示，Tool 类型在 "工具" 部分显示

---

## 测试检查清单

### 发布前检查

- [ ] 所有单元测试通过
- [ ] 集成测试通过
- [ ] Mock Server 端点正常工作
- [ ] 远程调试连接成功
- [ ] 在 Dify 中能看到所有插件
- [ ] 工具可以正常调用
- [ ] YAML 配置文件验证通过

### 测试命令汇总

```bash
# 完整测试流程
source .venv/bin/activate

# 1. 单元测试
pytest mercury_trigger_plugin/tests/unit/ -v
pytest mercury_tools_plugin/tests/unit/test_tools.py -v
pytest quickbooks_plugin/tests/unit/ -v

# 2. 启动 Mock Server
python3 scripts/mock_mercury_server.py &
sleep 2

# 3. 集成测试
pytest mercury_trigger_plugin/tests/integration/ -v

# 4. 远程调试（可选）
# 确保 .env 文件配置正确
cd mercury_trigger_plugin && python main.py &
cd ../mercury_tools_plugin && python main.py &
cd ../quickbooks_plugin && python main.py &
cd ../quickbooks_payments_plugin && python main.py &

# 5. 查看日志
tail -f /tmp/*.log
```

---

## 联系与支持

- **仓库**: https://github.com/Petrus-Han/finance_plugins
- **分支**: dev/alai-sudo
- **问题反馈**: 在 GitHub 创建 Issue
