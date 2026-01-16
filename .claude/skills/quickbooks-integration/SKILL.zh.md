# QuickBooks API 参考

QuickBooks Online API 参考文档，用于金融交易和会计实体管理。

## 何时使用此技能

- 创建 QuickBooks 工具插件
- 实现 Purchase/Deposit 实体
- 设置 QuickBooks OAuth 2.0
- 查询会计科目或供应商
- 映射 Mercury 交易到 QuickBooks

## API 基础

### Base URL 模式

```
https://quickbooks.api.intuit.com/v3/company/{realmId}/{entity}
```

**重要**: `realmId` 在所有请求中都是必需的，在 OAuth 回调中获取。

### 认证

```python
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
```

Token 刷新由 Dify OAuth 系统自动处理。

### 环境

| 环境 | Base URL |
|------|----------|
| Sandbox | `https://sandbox-quickbooks.api.intuit.com` |
| Production | `https://quickbooks.api.intuit.com` |

## 常用实体

### Purchase (费用)

```json
{
  "AccountRef": {"value": "35"},
  "PaymentType": "CreditCard",
  "EntityRef": {"value": "42", "type": "Vendor"},
  "TxnDate": "2025-12-26",
  "Line": [{
    "Amount": 150.00,
    "DetailType": "AccountBasedExpenseLineDetail",
    "AccountBasedExpenseLineDetail": {
      "AccountRef": {"value": "7"}
    }
  }]
}
```

### Deposit (收入)

```json
{
  "DepositToAccountRef": {"value": "35"},
  "TxnDate": "2025-12-26",
  "Line": [{
    "Amount": 1000.00,
    "DetailType": "DepositLineDetail",
    "DepositLineDetail": {
      "AccountRef": {"value": "79"},
      "Entity": {"value": "15", "type": "Customer"}
    }
  }]
}
```

### Vendor (供应商)

```json
{
  "DisplayName": "Acme Corp",
  "CompanyName": "Acme Corporation",
  "PrimaryEmailAddr": {"Address": "vendor@example.com"},
  "PrimaryPhone": {"FreeFormNumber": "555-1234"}
}
```

## 查询语言 (类 SQL)

```sql
-- 获取所有供应商
SELECT * FROM Vendor

-- 搜索供应商
SELECT * FROM Vendor WHERE DisplayName LIKE '%Staples%'

-- 按日期过滤
SELECT * FROM Purchase WHERE TxnDate >= '2025-01-01'

-- 分页
SELECT * FROM Entity STARTPOSITION 1 MAXRESULTS 100
```

## OAuth 配置

### Provider YAML

```yaml
identity:
  name: quickbooks
  label:
    en_US: QuickBooks Online

credentials_schema:
  - name: auth_type
    type: select
    options:
      - value: oauth
        label:
          en_US: OAuth 2.0

oauth:
  authorization_url: https://appcenter.intuit.com/connect/oauth2
  token_url: https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer
  scopes:
    - com.intuit.quickbooks.accounting
```

## 实现模式

### 1. 幂等性检查 (金融数据关键!)

```python
def create_purchase(self, mercury_txn_id: str, ...):
    # 检查是否已存在
    query = f"SELECT * FROM Purchase WHERE PrivateNote LIKE '%{mercury_txn_id}%'"
    existing = self._query(query)

    if existing:
        return {"status": "duplicate", "id": existing[0]["Id"]}

    # 创建新的 purchase
    # ... 在 PrivateNote 中存储 mercury_txn_id
```

### 2. 查找或创建供应商

```python
def find_or_create_vendor(self, vendor_name: str):
    # 搜索现有
    query = f"SELECT * FROM Vendor WHERE DisplayName LIKE '%{vendor_name}%'"
    vendors = self._query(query)

    if vendors:
        return vendors[0]

    # 创建新的
    response = requests.post(
        f"{BASE_URL}/{realm_id}/vendor",
        json={"DisplayName": vendor_name},
        headers=headers
    )
    return response.json()["Vendor"]
```

### 3. 错误处理

```python
# 常见错误
# 400: 无效数据 (检查必填字段)
# 401: Token 过期 (自动刷新)
# 409: 重复实体
# 429: 速率限制 (退避重试)
# 500: 服务器错误 (重试)

try:
    response = requests.post(...)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 409:
        return {"status": "duplicate"}
    elif e.response.status_code == 429:
        time.sleep(2)  # 速率限制退避
        # 重试...
    else:
        raise ToolProviderCredentialValidationError(str(e))
```

## Mercury → QuickBooks 映射

### 借记交易 (费用) → Purchase

```python
def map_debit_to_purchase(mercury_txn):
    return {
        "AccountRef": {"value": get_mercury_bank_account_id()},
        "PaymentType": "CreditCard",
        "EntityRef": {
            "value": find_or_create_vendor(mercury_txn["merchant"]),
            "type": "Vendor"
        },
        "TxnDate": mercury_txn["date"],
        "PrivateNote": f"Mercury: {mercury_txn['transaction_id']} - {mercury_txn['description']}",
        "Line": [{
            "Amount": abs(mercury_txn["amount"]),
            "DetailType": "AccountBasedExpenseLineDetail",
            "Description": mercury_txn["description"],
            "AccountBasedExpenseLineDetail": {
                "AccountRef": {"value": map_to_expense_account(mercury_txn)}
            }
        }]
    }
```

### 贷记交易 (收入) → Deposit

```python
def map_credit_to_deposit(mercury_txn):
    return {
        "DepositToAccountRef": {"value": get_mercury_bank_account_id()},
        "TxnDate": mercury_txn["date"],
        "PrivateNote": f"Mercury: {mercury_txn['transaction_id']}",
        "Line": [{
            "Amount": mercury_txn["amount"],
            "DetailType": "DepositLineDetail",
            "DepositLineDetail": {
                "AccountRef": {"value": get_income_account_id()},
            }
        }]
    }
```

## 测试

### 沙箱环境

1. 在 developer.intuit.com 创建沙箱公司
2. 获取沙箱 realm_id
3. 使用沙箱 OAuth 凭据
4. 测试所有实体创建
5. 在沙箱 QuickBooks 中验证数据

### 常见测试用例

```python
# 测试 1: 创建供应商
vendor = create_vendor("Test Vendor")
assert vendor["Id"] is not None

# 测试 2: 创建采购
purchase = create_purchase({
    "transaction_id": "test_txn_123",
    "amount": -100.00,
    "merchant": "Test Vendor",
    "date": "2025-12-26"
})
assert purchase["status"] == "created"

# 测试 3: 防重复
duplicate = create_purchase({...})  # 相同 txn_id
assert duplicate["status"] == "duplicate"

# 测试 4: 查询
results = query("SELECT * FROM Vendor WHERE DisplayName = 'Test Vendor'")
assert len(results) > 0
```

## 最佳实践

1. **始终检查重复** - 使用 PrivateNote 存储 Mercury 交易 ID
2. **缓存会计科目表** - 加载一次，重复使用
3. **处理速率限制** - 实现指数退避
4. **正确使用 realm_id** - 所有 API URL 都需要
5. **先在沙箱测试** - 不要用生产数据测试
6. **记录所有 API 调用** - 用于审计和调试
7. **发送前验证数据** - 检查必填字段
8. **使用 minorversion 参数** - `?minorversion=65` 获取最新功能

## 速率限制策略

```python
import time

MAX_REQUESTS_PER_SECOND = 5
request_times = []

def rate_limit():
    now = time.time()
    # 移除超过 1 秒的请求
    request_times[:] = [t for t in request_times if now - t < 1]

    if len(request_times) >= MAX_REQUESTS_PER_SECOND:
        sleep_time = 1 - (now - request_times[0])
        if sleep_time > 0:
            time.sleep(sleep_time)

    request_times.append(time.time())
```

## 快速参考

### 实体端点

| 实体 | 端点 |
|------|------|
| Vendor | `/v3/company/{realmId}/vendor` |
| Purchase | `/v3/company/{realmId}/purchase` |
| Deposit | `/v3/company/{realmId}/deposit` |
| Account | `/v3/company/{realmId}/account` |
| Query | `/v3/company/{realmId}/query?query={sql}` |

### OAuth Scopes

- `com.intuit.quickbooks.accounting` - 完整会计访问

### 必填字段

| 实体 | 必填字段 |
|------|----------|
| Purchase | `AccountRef`, `PaymentType`, `Line[]` |
| Deposit | `DepositToAccountRef`, `Line[]` |
| Vendor | `DisplayName` |

## 相关技能

- **01-design**: 设计阶段
- **02-api-reference**: 通用 API 参考收集指南
- **03-development**: 开发实现
- **04-testing**: 测试验证
- **05-packaging**: 打包发布

## 参考文档

- `archive/QuickBooks_API_Documentation.md` - 完整 API 参考
- `QuickBooks_Payments_API_Documentation.md` - Payments API 参考
- `archive/solution-design.md` - 架构和设计决策
