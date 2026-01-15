# Mercury to Quickbooks 同步解决方案设计文档

## 1. 项目概述

### 1.1 业务目标
帮助财务人员实现 Mercury 银行账单/交易数据自动同步到 QuickBooks 会计系统，提升财务数据处理效率，减少手工录入错误。

### 1.2 用户角色
- 主要用户：财务人员
- 技术能力：熟悉财务系统操作，无需编程能力
- 使用场景：定期同步 Mercury 银行交易记录到 QuickBooks 进行会计处理

### 1.3 技术方案
通过 Dify 平台开发两个工具插件：
- Mercury 工具插件：负责从 Mercury API 获取交易数据
- QuickBooks 工具插件：负责将数据写入 QuickBooks
- 在 Dify 工作流中连接两个插件，数据映射逻辑由 LLM 或财务人员在工作流中配置

---

## 2. 整体架构设计

### 2.1 系统架构图

```
┌─────────────────┐
│  Mercury Bank   │
│   (Data Source) │
└────────┬────────┘
         │ OAuth 2.0
         │ REST API
         ▼
┌─────────────────────────────────────────────────────────┐
│                    Dify Platform                        │
│  ┌────────────────────────────────────────────────┐    │
│  │              Dify Workflow                      │    │
│  │                                                  │    │
│  │  ┌──────────────┐   ┌──────────────┐          │    │
│  │  │  Mercury     │   │  Data        │          │    │
│  │  │  Tool Plugin │──▶│  Transform   │          │    │
│  │  │  (获取交易)   │   │  (LLM/Rules) │          │    │
│  │  └──────────────┘   └──────┬───────┘          │    │
│  │                             │                   │    │
│  │                             ▼                   │    │
│  │                     ┌──────────────┐           │    │
│  │                     │  QuickBooks  │           │    │
│  │                     │  Tool Plugin │           │    │
│  │                     │  (写入记录)   │           │    │
│  │                     └──────────────┘           │    │
│  │                                                  │    │
│  │  ┌──────────────────────────────────┐          │    │
│  │  │  Error Handling & Retry Logic    │          │    │
│  │  └──────────────────────────────────┘          │    │
│  └────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
         │ OAuth 2.0
         │ REST API
         ▼
┌─────────────────┐
│   QuickBooks    │
│  (Data Target)  │
└─────────────────┘
```

### 2.2 数据流向

1. **数据提取阶段**
   - 用户在 Dify 工作流中配置同步参数（日期范围、账户等）
   - Mercury 插件调用 API 获取交易数据
   - 返回标准化的交易数据列表

2. **数据转换阶段**
   - 通过 LLM 节点或规则引擎进行数据映射
   - 将 Mercury 交易字段映射到 QuickBooks 所需格式
   - 财务人员可在工作流中配置映射规则

3. **数据加载阶段**
   - QuickBooks 插件接收转换后的数据
   - 调用 API 创建交易记录（Purchase/Expense/Deposit）
   - 返回同步结果和错误信息

4. **结果反馈阶段**
   - 记录同步状态（成功/失败/部分成功）
   - 对失败记录进行重试或人工审核
   - 生成同步报告

---

## 3. 插件设计方案

### 3.1 Mercury 工具插件

#### 3.1.1 核心功能
- **认证管理**：支持 OAuth 2.0 授权流程
- **交易查询**：根据账户 ID、日期范围获取交易列表
- **单笔查询**：根据交易 ID 获取详细信息
- **数据标准化**：将 API 响应转换为统一格式

#### 3.1.2 API 端点映射

| 功能 | Mercury API 端点 | 方法 |
|------|-----------------|------|
| 获取账户列表 | `/api/v1/accounts` | GET |
| 获取交易列表 | `/api/v1/account/:id/transactions` | GET |
| 获取单笔交易 | `/api/v1/transactions/:transactionId` | GET |

#### 3.1.3 工具定义（Tools）

**Tool 1: get_accounts**
```yaml
name: get_accounts
description: 获取 Mercury 账户列表
parameters: []
returns:
  - id: 账户 ID
  - name: 账户名称
  - accountNumber: 账户号码
  - status: 账户状态
```

**Tool 2: get_transactions**
```yaml
name: get_transactions
description: 获取指定账户的交易记录
parameters:
  - account_id: 账户 ID (required)
  - start_date: 开始日期 (optional, format: YYYY-MM-DD)
  - end_date: 结束日期 (optional, format: YYYY-MM-DD)
  - limit: 返回数量限制 (optional, default: 100)
  - offset: 偏移量 (optional, default: 0)
returns:
  - id: 交易 ID
  - amount: 金额
  - createdAt: 创建时间
  - bankDescription: 银行描述
  - counterpartyName: 交易对手名称
  - status: 交易状态
  - kind: 交易类型 (credit/debit)
  - trackingNumber: 追踪号（可选）
```

**Tool 3: get_transaction_detail**
```yaml
name: get_transaction_detail
description: 获取单笔交易详细信息
parameters:
  - transaction_id: 交易 ID (required)
returns:
  - [完整交易信息，包含 details 对象]
```

#### 3.1.4 OAuth 配置

```yaml
oauth_schema:
  client_schema:
    - name: client_id
      type: string
      required: true
    - name: client_secret
      type: string
      required: true
      secret: true

  credentials_schema:
    - name: access_token
      type: string
      required: true
      secret: true
    - name: refresh_token
      type: string
      required: true
      secret: true
    - name: expires_at
      type: number
      required: true

authorization_url: https://app.mercury.com/oauth/authorize
token_url: https://api.mercury.com/api/v1/oauth/token
scopes:
  - offline_access  # 支持 refresh token
  - read:accounts
  - read:transactions
```

#### 3.1.5 数据输出格式

```json
{
  "transactions": [
    {
      "id": "txn_xxx",
      "amount": -1500.00,
      "currency": "USD",
      "date": "2025-12-15",
      "description": "Office Supplies - Staples",
      "counterparty": {
        "id": "cp_xxx",
        "name": "Staples Inc.",
        "nickname": null
      },
      "type": "debit",
      "status": "settled",
      "category": null,
      "trackingNumber": "TRK123456",
      "metadata": {
        "dashboardLink": "https://app.mercury.com/transactions/txn_xxx"
      }
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 100,
    "offset": 0,
    "hasMore": true
  }
}
```

---

### 3.2 QuickBooks 工具插件

#### 3.2.1 核心功能
- **认证管理**：支持 OAuth 2.0 授权流程
- **创建费用**：创建 Purchase/Expense 记录
- **创建存款**：创建 Deposit 记录
- **查询科目**：获取会计科目列表（用于映射）
- **查询供应商**：获取供应商列表（用于映射）
- **查询客户**：获取客户列表（用于映射）

#### 3.2.2 API 端点映射

| 功能 | QuickBooks API 端点 | 方法 |
|------|---------------------|------|
| 创建费用 | `/v3/company/:realmId/purchase` | POST |
| 创建存款 | `/v3/company/:realmId/deposit` | POST |
| 查询科目 | `/v3/company/:realmId/query?query=SELECT * FROM Account` | GET |
| 查询供应商 | `/v3/company/:realmId/query?query=SELECT * FROM Vendor` | GET |
| 查询客户 | `/v3/company/:realmId/query?query=SELECT * FROM Customer` | GET |

#### 3.2.3 工具定义（Tools）

**Tool 1: get_accounts**
```yaml
name: get_accounts
description: 获取 QuickBooks 会计科目列表
parameters:
  - account_type: 科目类型 (optional, 如 Expense, Bank, Income)
returns:
  - Id: 科目 ID
  - Name: 科目名称
  - AccountType: 科目类型
  - AccountSubType: 科目子类型
  - Active: 是否激活
```

**Tool 2: get_vendors**
```yaml
name: get_vendors
description: 获取供应商列表
parameters:
  - active_only: 仅返回激活的供应商 (optional, default: true)
returns:
  - Id: 供应商 ID
  - DisplayName: 显示名称
  - CompanyName: 公司名称
  - Active: 是否激活
```

**Tool 3: create_purchase**
```yaml
name: create_purchase
description: 创建 Purchase 记录（用于费用/采购）
parameters:
  - account_ref_id: 银行账户 ID (required)
  - payment_type: 支付方式 (required, 如 Cash, Check, CreditCard)
  - txn_date: 交易日期 (required, format: YYYY-MM-DD)
  - vendor_ref_id: 供应商 ID (optional)
  - lines: 行项目数组 (required)
    - amount: 金额 (required)
    - description: 描述 (optional)
    - account_ref_id: 费用科目 ID (required)
    - detail_type: 明细类型 (required, 如 AccountBasedExpenseLineDetail)
  - private_note: 备注 (optional)
returns:
  - Id: 创建的 Purchase ID
  - SyncToken: 同步令牌
  - MetaData: 元数据（创建时间等）
```

**Tool 4: create_deposit**
```yaml
name: create_deposit
description: 创建 Deposit 记录（用于收入）
parameters:
  - account_ref_id: 银行账户 ID (required)
  - txn_date: 交易日期 (required, format: YYYY-MM-DD)
  - lines: 行项目数组 (required)
    - amount: 金额 (required)
    - description: 描述 (optional)
    - account_ref_id: 收入科目 ID (required)
    - entity_ref_id: 客户/供应商 ID (optional)
  - private_note: 备注 (optional)
returns:
  - Id: 创建的 Deposit ID
  - SyncToken: 同步令牌
  - MetaData: 元数据（创建时间等）
```

**Tool 5: search_entity**
```yaml
name: search_entity
description: 根据名称模糊搜索实体（供应商/客户）
parameters:
  - entity_type: 实体类型 (required, Vendor 或 Customer)
  - search_term: 搜索关键词 (required)
returns:
  - Id: 实体 ID
  - DisplayName: 显示名称
  - MatchScore: 匹配度分数 (0-100)
```

#### 3.2.4 OAuth 配置

```yaml
oauth_schema:
  client_schema:
    - name: client_id
      type: string
      required: true
    - name: client_secret
      type: string
      required: true
      secret: true

  credentials_schema:
    - name: access_token
      type: string
      required: true
      secret: true
    - name: refresh_token
      type: string
      required: true
      secret: true
    - name: expires_at
      type: number
      required: true
    - name: realm_id
      type: string
      required: true  # QuickBooks 公司 ID

authorization_url: https://appcenter.intuit.com/connect/oauth2
token_url: https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer
scopes:
  - com.intuit.quickbooks.accounting  # 会计数据访问
```

#### 3.2.5 数据输入格式示例

```json
{
  "AccountRef": {
    "value": "35"  // 银行账户 ID
  },
  "PaymentType": "CreditCard",
  "TxnDate": "2025-12-15",
  "EntityRef": {
    "value": "56",  // 供应商 ID
    "type": "Vendor"
  },
  "Line": [
    {
      "Amount": 1500.00,
      "DetailType": "AccountBasedExpenseLineDetail",
      "Description": "Office Supplies - Staples",
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {
          "value": "8"  // 费用科目 ID
        }
      }
    }
  ],
  "PrivateNote": "Synced from Mercury - txn_xxx"
}
```

---

## 4. Dify 工作流设计

### 4.1 工作流架构

```
开始
  │
  ├─ [输入节点] 配置同步参数
  │   ├─ Mercury 账户 ID
  │   ├─ 日期范围
  │   ├─ QuickBooks 公司 ID
  │   └─ 映射配置
  │
  ├─ [Mercury 工具] 获取交易列表
  │   └─ 输出: transactions[]
  │
  ├─ [迭代节点] 遍历每笔交易
  │   │
  │   ├─ [LLM 节点] 数据映射与分类
  │   │   ├─ 输入: 单笔交易数据 + 映射规则
  │   │   ├─ 处理:
  │   │   │   ├─ 判断交易类型 (借方/贷方 → Purchase/Deposit)
  │   │   │   ├─ 匹配供应商/客户
  │   │   │   ├─ 分配会计科目
  │   │   │   └─ 生成 QuickBooks 请求体
  │   │   └─ 输出: mapped_transaction
  │   │
  │   ├─ [条件节点] 检查映射结果
  │   │   ├─ 成功 → 继续
  │   │   └─ 失败 → 记录错误，跳过
  │   │
  │   ├─ [QuickBooks 工具] 创建交易记录
  │   │   ├─ create_purchase (借方交易)
  │   │   └─ create_deposit (贷方交易)
  │   │
  │   └─ [错误处理节点]
  │       ├─ 成功 → 记录到成功列表
  │       └─ 失败 → 记录到失败列表，触发重试
  │
  ├─ [汇总节点] 生成同步报告
  │   ├─ 总计: X 笔
  │   ├─ 成功: Y 笔
  │   ├─ 失败: Z 笔
  │   └─ 失败详情
  │
  └─ [输出节点] 返回结果
```

### 4.2 数据映射策略

#### 4.2.1 自动映射（LLM 驱动）

通过 LLM 节点自动处理映射逻辑：

```yaml
LLM Prompt Template:
  系统提示: |
    你是一个财务数据映射专家。根据 Mercury 交易数据，生成对应的 QuickBooks 记录。

    映射规则：
    1. 交易类型判断：
       - amount < 0 → Purchase (费用支出)
       - amount > 0 → Deposit (收入/存款)

    2. 供应商/客户匹配：
       - 使用 counterpartyName 匹配 QuickBooks 中的 Vendor/Customer
       - 如果找不到精确匹配，返回最相似的实体（相似度 > 80%）
       - 如果相似度 < 80%，标记为需要人工审核

    3. 会计科目分配：
       - 根据 description 关键词推断科目类型
       - 默认科目配置：
         * "Office Supplies" → 费用科目: Office Expense
         * "Software" → 费用科目: Software & Subscriptions
         * "Travel" → 费用科目: Travel Expense
         * 其他 → 费用科目: General Expense

    4. 输出格式：
       严格按照 JSON Schema 返回结果

  用户输入: |
    Mercury 交易数据：
    {{transaction}}

    可用的 QuickBooks 科目列表：
    {{qb_accounts}}

    可用的供应商列表：
    {{qb_vendors}}

    请生成对应的 QuickBooks 记录。

  输出 Schema:
    {
      "transaction_type": "purchase|deposit",
      "qb_account_ref_id": "银行账户 ID",
      "payment_type": "CreditCard|Check|Cash",
      "txn_date": "YYYY-MM-DD",
      "entity_ref": {
        "id": "供应商/客户 ID",
        "type": "Vendor|Customer",
        "name": "名称",
        "match_confidence": 0-100
      },
      "lines": [
        {
          "amount": 金额,
          "description": "描述",
          "account_ref_id": "费用/收入科目 ID",
          "account_name": "科目名称"
        }
      ],
      "private_note": "备注",
      "needs_review": true|false,
      "review_reason": "原因说明"
    }
```

#### 4.2.2 手动映射配置

财务人员可在工作流中预先配置映射规则：

```yaml
# 映射配置文件示例
mapping_config:
  # 默认科目映射
  default_accounts:
    bank_account_id: "35"  # Mercury 对应的 QB 银行账户
    default_expense_account_id: "8"  # 默认费用科目
    default_income_account_id: "12"  # 默认收入科目

  # 供应商名称映射
  vendor_mapping:
    "Staples": "56"  # Mercury counterpartyName → QB Vendor ID
    "AWS": "89"
    "Google Cloud": "91"

  # 关键词科目映射
  keyword_account_mapping:
    - keywords: ["office", "supplies", "staples"]
      account_id: "8"
      account_name: "Office Expense"

    - keywords: ["aws", "cloud", "server", "hosting"]
      account_id: "15"
      account_name: "IT & Cloud Services"

    - keywords: ["flight", "hotel", "travel", "uber"]
      account_id: "22"
      account_name: "Travel Expense"

  # 金额范围规则
  amount_rules:
    - min: 0
      max: 100
      account_id: "8"  # 小额支出 → 杂项费用

    - min: 10000
      needs_approval: true  # 大额交易需审批
```

#### 4.2.3 混合策略

结合 LLM 智能映射和手动规则：

1. **优先使用手动规则**：如果供应商名称在映射表中，直接使用
2. **LLM 辅助决策**：对于未配置的情况，LLM 推断并给出置信度
3. **人工审核机制**：置信度低于阈值的记录标记为待审核

---

## 5. 错误处理机制

### 5.1 错误分类

| 错误类型 | 描述 | 处理策略 |
|---------|------|---------|
| **认证错误** | OAuth token 过期或无效 | 自动刷新 token，重试 |
| **网络错误** | API 请求超时或连接失败 | 指数退避重试（最多 3 次） |
| **数据验证错误** | 必填字段缺失、格式错误 | 记录错误详情，跳过该记录 |
| **业务规则错误** | QB 科目不存在、供应商重复 | 标记为待审核，通知财务人员 |
| **API 限流** | 超出 API 调用频率限制 | 等待后重试，调整批处理大小 |
| **重复记录** | 同一交易已同步过 | 跳过，记录到日志 |

### 5.2 重试机制

```python
# 伪代码示例
def sync_transaction_with_retry(transaction, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = quickbooks_plugin.create_purchase(transaction)
            return {"status": "success", "result": result}

        except OAuthError as e:
            # 认证错误，刷新 token
            refresh_token()
            continue

        except NetworkError as e:
            # 网络错误，指数退避
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            sleep(wait_time)
            continue

        except ValidationError as e:
            # 数据验证错误，不重试
            return {"status": "validation_error", "error": str(e)}

        except RateLimitError as e:
            # 限流错误，等待重置时间
            wait_until_reset(e.reset_time)
            continue

    # 所有重试失败
    return {"status": "failed", "error": "Max retries exceeded"}
```

### 5.3 错误日志与通知

```yaml
# 错误记录格式
error_log:
  timestamp: "2025-12-19T10:30:00Z"
  transaction_id: "txn_xxx"
  error_type: "validation_error"
  error_message: "Missing required field: AccountRef"
  retry_count: 0
  needs_manual_review: true
  mercury_data: { ... }
  attempted_qb_data: { ... }

# 通知机制
notification:
  channels:
    - email: finance@company.com
    - slack: #finance-automation

  triggers:
    - event: sync_completed
      template: "同步完成：成功 {{success_count}}/{{total_count}} 笔"

    - event: high_error_rate
      condition: error_rate > 10%
      template: "警告：同步错误率过高 ({{error_rate}}%)"

    - event: needs_review
      template: "{{review_count}} 笔交易需要人工审核"
```

---

## 6. 关键技术挑战与解决方案

### 6.1 挑战 1：OAuth 认证管理

**挑战**：
- Mercury 和 QuickBooks 都需要 OAuth 2.0 授权
- Access token 有效期短（1小时），需要自动刷新
- QuickBooks 需要额外的 realm_id（公司 ID）

**解决方案**：
1. **Dify OAuth 支持**：
   - 利用 Dify v1.7.1+ 的 OAuth 插件功能
   - 在插件 manifest 中定义 oauth_schema
   - 实现 `get_authorization_url()`, `get_credentials()`, `refresh_credentials()` 方法

2. **Token 自动刷新**：
   ```python
   # 在每次 API 调用前检查 token 有效性
   def check_and_refresh_token(credentials):
       if credentials.expires_at < time.now() + 300:  # 提前5分钟刷新
           new_credentials = refresh_oauth_token(credentials.refresh_token)
           save_credentials(new_credentials)
           return new_credentials
       return credentials
   ```

3. **Realm ID 管理**：
   - 在 QuickBooks OAuth 回调中获取 realm_id
   - 存储在 credentials_schema 中，与 token 一起持久化

---

### 6.2 挑战 2：数据映射复杂性

**挑战**：
- Mercury 交易字段与 QuickBooks 实体字段不直接对应
- 需要将单一交易映射到多个 QB 字段（科目、供应商、行项目）
- 不同公司的会计科目结构不同

**解决方案**：
1. **LLM 智能映射**：
   - 使用 Dify LLM 节点进行语义理解
   - 根据描述推断科目类型
   - 模糊匹配供应商/客户名称

2. **可配置映射规则**：
   - 财务人员在工作流中配置映射表
   - 支持关键词匹配、正则表达式
   - 优先使用手动规则，LLM 作为兜底

3. **映射置信度机制**：
   - 每个映射结果附带置信度分数
   - 低置信度 (<80%) 标记为待审核
   - 财务人员审核后更新映射规则

---

### 6.3 挑战 3：API 限流与性能

**挑战**：
- Mercury API 和 QuickBooks API 都有请求频率限制
- QuickBooks API 限制：500 请求/分钟/应用
- 大批量同步可能触发限流

**解决方案**：
1. **批处理控制**：
   - 分批次处理交易（每批 20-50 笔）
   - 批次间添加延迟（如每批后等待 2 秒）

2. **速率限制器**：
   ```python
   # 令牌桶算法
   class RateLimiter:
       def __init__(self, rate=500, per=60):  # 500/分钟
           self.rate = rate
           self.per = per
           self.tokens = rate
           self.last_update = time.now()

       def acquire(self):
           # 补充令牌
           now = time.now()
           elapsed = now - self.last_update
           self.tokens = min(self.rate, self.tokens + elapsed * (self.rate / self.per))
           self.last_update = now

           if self.tokens >= 1:
               self.tokens -= 1
               return True
           else:
               # 计算等待时间
               wait_time = (1 - self.tokens) * (self.per / self.rate)
               sleep(wait_time)
               return self.acquire()
   ```

3. **异步处理**：
   - 对于大批量同步，使用后台任务
   - 实时返回任务 ID，财务人员可查询进度
   - 完成后发送通知

---

### 6.4 挑战 4：重复数据检测

**挑战**：
- 避免重复同步同一笔交易
- Mercury 交易 ID 与 QuickBooks 记录 ID 不同
- 需要建立关联关系

**解决方案**：
1. **唯一标识映射**：
   - 在 QuickBooks PrivateNote 或 CustomField 中存储 Mercury 交易 ID
   - 示例：`PrivateNote: "Synced from Mercury - txn_abc123"`

2. **同步状态追踪**：
   ```yaml
   # 维护同步记录表（可存储在 Dify 数据库或外部存储）
   sync_records:
     - mercury_txn_id: "txn_abc123"
       qb_purchase_id: "456"
       sync_date: "2025-12-19T10:30:00Z"
       status: "success"

     - mercury_txn_id: "txn_def456"
       qb_purchase_id: null
       sync_date: "2025-12-19T10:31:00Z"
       status: "failed"
       error: "Vendor not found"
   ```

3. **增量同步**：
   - 每次同步只获取上次成功同步后的新交易
   - 使用 `start_date` 参数过滤（基于上次同步时间戳）

---

### 6.5 挑战 5：多币种处理

**挑战**：
- Mercury 支持多币种账户
- QuickBooks 可能配置为单一货币或多币种
- 汇率转换逻辑复杂

**解决方案**：
1. **币种一致性检查**：
   - 在同步前检查 Mercury 交易币种与 QuickBooks 设置
   - 如果不一致，标记为待审核

2. **汇率处理**（如果 QB 启用多币种）：
   - QuickBooks API 支持 ExchangeRate 字段
   - 可从第三方 API 获取实时汇率
   - 或使用 Mercury 提供的汇率（如有）

3. **简化方案**（MVP）：
   - 初期只支持单一币种（如 USD）
   - 非 USD 交易标记为需人工处理

---

## 7. 架构选择讨论

### 7.1 数据映射：LLM vs 规则引擎

**选项 A：纯 LLM 驱动**
- 优点：灵活，无需预配置，可处理复杂语义
- 缺点：成本高，结果不稳定，可能产生错误
- 适用场景：交易描述清晰，科目体系标准化

**选项 B：纯规则引擎**
- 优点：精确，成本低，可预测
- 缺点：配置复杂，需要大量初始化工作，灵活性差
- 适用场景：交易类型固定，映射关系明确

**选项 C：混合模式（推荐）**
- 优先使用规则，LLM 作为兜底
- 财务人员可逐步完善规则库
- 平衡成本与准确性

**建议**：采用选项 C，并提供置信度反馈，让财务人员决定是否信任 LLM 结果。

---

### 7.2 同步模式：实时 vs 批量

**选项 A：实时同步**
- 触发：Mercury webhook（如果支持）或定时轮询（如每5分钟）
- 优点：数据实时性强
- 缺点：API 调用频繁，成本高，可能触发限流

**选项 B：批量同步**
- 触发：财务人员手动触发或定时任务（如每日）
- 优点：高效，可批量优化，减少 API 调用
- 缺点：数据滞后

**选项 C：混合模式**
- 小额交易批量同步（每日）
- 大额交易实时同步（金额 > 阈值）

**建议**：初期采用选项 B（批量），根据用户反馈评估是否需要实时同步。

---

### 7.3 错误处理：自动修复 vs 人工审核

**选项 A：激进自动修复**
- 使用 LLM 猜测缺失字段
- 自动创建缺失的供应商/科目
- 优点：减少人工干预
- 缺点：可能产生脏数据，后期清理困难

**选项 B：保守人工审核**
- 任何不确定的记录都标记为待审核
- 财务人员手动完成映射
- 优点：数据质量高
- 缺点：工作量大，自动化程度低

**选项 C：分级处理（推荐）**
- 高置信度（>95%）：自动同步
- 中置信度（80-95%）：同步但发送通知供事后检查
- 低置信度（<80%）：暂停并等待人工审核

**建议**：采用选项 C，随着系统运行逐步提高自动化比例。

---

### 7.4 数据存储：无状态 vs 有状态

**选项 A：无状态**
- 每次同步从零开始，不记录历史状态
- 优点：简单，无需额外存储
- 缺点：无法防重，无法追溯

**选项 B：有状态（推荐）**
- 维护同步记录表，记录每笔交易的同步状态
- 优点：支持增量同步、防重、审计
- 缺点：需要额外存储（可使用 Dify 数据库或外部 DB）

**建议**：采用选项 B，存储最少信息（Mercury ID → QB ID 映射）。

---

### 7.5 插件粒度：粗粒度 vs 细粒度

**选项 A：粗粒度工具**
- Mercury 插件提供一个 `sync_to_quickbooks` 工具
- 内部封装所有逻辑（获取、映射、写入）
- 优点：简单易用
- 缺点：不灵活，难以自定义

**选项 B：细粒度工具（推荐）**
- Mercury 插件提供 `get_accounts`, `get_transactions` 等独立工具
- QuickBooks 插件提供 `create_purchase`, `get_vendors` 等独立工具
- 在 Dify 工作流中组合使用
- 优点：灵活，可复用，可自定义
- 缺点：工作流配置复杂

**建议**：采用选项 B，但提供预配置的模板工作流供快速上手。

---

## 8. 实施路线图

### Phase 1：MVP（最小可行产品）- 2-3周
**目标**：验证技术可行性，完成基础同步功能

- [ ] Mercury 插件开发
  - [ ] OAuth 认证
  - [ ] get_accounts 工具
  - [ ] get_transactions 工具

- [ ] QuickBooks 插件开发
  - [ ] OAuth 认证
  - [ ] get_accounts 工具（QB 科目）
  - [ ] get_vendors 工具
  - [ ] create_purchase 工具

- [ ] Dify 工作流
  - [ ] 基础同步流程
  - [ ] 简单规则映射（手动配置）
  - [ ] 错误日志记录

- [ ] 测试
  - [ ] 测试账户授权
  - [ ] 同步 10 笔测试交易
  - [ ] 验证 QuickBooks 记录准确性

**交付物**：
- 可运行的 Dify 工作流
- 基础文档（安装、配置指南）

---

### Phase 2：增强功能 - 2周
**目标**：提升用户体验，增加智能化功能

- [ ] LLM 智能映射
  - [ ] Prompt 工程与优化
  - [ ] 置信度评分机制
  - [ ] 供应商名称模糊匹配

- [ ] 批量处理
  - [ ] 迭代节点优化
  - [ ] 进度追踪
  - [ ] 批次暂停/恢复

- [ ] 同步状态管理
  - [ ] 记录 Mercury ID → QB ID 映射
  - [ ] 增量同步支持
  - [ ] 防重机制

- [ ] 通知机制
  - [ ] 邮件通知
  - [ ] Slack 集成
  - [ ] 同步报告生成

---

### Phase 3：生产就绪 - 1-2周
**目标**：达到生产环境要求

- [ ] 性能优化
  - [ ] API 调用优化
  - [ ] 速率限制处理
  - [ ] 异步处理大批量数据

- [ ] 错误处理完善
  - [ ] 全面的错误分类
  - [ ] 重试机制
  - [ ] 错误恢复策略

- [ ] 安全加固
  - [ ] 敏感信息加密
  - [ ] 审计日志
  - [ ] 权限控制

- [ ] 文档与培训
  - [ ] 用户手册
  - [ ] 故障排查指南
  - [ ] 视频教程

---

### Phase 4：持续优化（可选）
- [ ] 多币种支持
- [ ] Deposit（收入）记录同步
- [ ] 自动供应商创建
- [ ] 机器学习优化映射规则
- [ ] Dashboard 数据可视化

---

## 9. 成功指标（KPIs）

| 指标 | 目标值 | 测量方法 |
|-----|--------|---------|
| **同步成功率** | > 95% | 成功记录数 / 总记录数 |
| **自动映射准确率** | > 90% | 无需人工修正的记录数 / 总记录数 |
| **处理速度** | < 5s/笔 | 从获取到写入的平均时间 |
| **错误恢复时间** | < 1 小时 | 从错误发生到人工介入的平均时间 |
| **用户满意度** | > 4/5 | 用户反馈评分 |

---

## 10. 风险评估

| 风险 | 影响 | 概率 | 缓解措施 |
|-----|------|------|---------|
| Mercury API 授权申请被拒 | 高 | 中 | 提前与 Mercury 沟通，准备详细用例说明 |
| QuickBooks API 限流 | 中 | 高 | 实施速率限制器，批量处理优化 |
| LLM 映射错误率高 | 中 | 中 | 提供规则引擎兜底，人工审核机制 |
| 多币种汇率复杂性 | 低 | 中 | 初期仅支持 USD，后续扩展 |
| 用户配置复杂度高 | 中 | 中 | 提供预配置模板，详细文档 |

---

## 11. 参考资料

### Mercury API
- [Welcome to Mercury's API docs](https://docs.mercury.com/reference/welcome-to-mercury-api)
- [Mercury API Transactions Endpoint](https://docs.mercury.com/reference/transactions-1)
- [Mercury OAuth Integration](https://docs.mercury.com/docs/integrations-with-oauth2)
- [Mercury API Authentication](https://docs.mercury.com/reference/using-the-access-token)

### QuickBooks API
- [Exploring the Quickbooks Online Accounting API](https://www.apideck.com/blog/exploring-the-quickbooks-online-accounting-api)
- [QuickBooks API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/account)
- [QuickBooks Deposit API](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/deposit)
- [Quickbooks Online API Integration Guide](https://www.getknit.dev/blog/quickbooks-online-api-integration-guide-in-depth)

### Dify Plugin Development
- [Welcome to Dify Plugin Development](https://docs.dify.ai/plugin-dev-en/0111-getting-started-dify-plugin)
- [Dify Plugin System: Design and Implementation](https://dify.ai/blog/dify-plugin-system-design-and-implementation)
- [Add OAuth Support to Your Tool Plugin](https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-oauth)
- [Dify Official Plugins Repository](https://github.com/langgenius/dify-official-plugins)
- [Dify Plugins Marketplace](https://github.com/langgenius/dify-plugins)

---

## 12. 附录

### A. Mercury 交易数据示例

```json
{
  "id": "txn_abc123",
  "amount": -1500.00,
  "kind": "debit",
  "status": "settled",
  "createdAt": "2025-12-15T10:30:00Z",
  "postedAt": "2025-12-15T10:30:00Z",
  "bankDescription": "STAPLES ONLINE",
  "counterpartyId": "cp_xyz789",
  "counterpartyName": "Staples Inc.",
  "counterpartyNickname": null,
  "estimatedDeliveryDate": null,
  "trackingNumber": "TRK123456",
  "dashboardLink": "https://app.mercury.com/transactions/txn_abc123",
  "note": null,
  "externalMemo": null
}
```

### B. QuickBooks Purchase 请求示例

```json
{
  "AccountRef": {
    "value": "35",
    "name": "Business Checking"
  },
  "PaymentType": "CreditCard",
  "TxnDate": "2025-12-15",
  "EntityRef": {
    "value": "56",
    "name": "Staples Inc.",
    "type": "Vendor"
  },
  "Line": [
    {
      "Id": "1",
      "Amount": 1500.00,
      "DetailType": "AccountBasedExpenseLineDetail",
      "Description": "STAPLES ONLINE - Office Supplies",
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {
          "value": "8",
          "name": "Office Expense"
        },
        "BillableStatus": "NotBillable",
        "TaxCodeRef": {
          "value": "NON"
        }
      }
    }
  ],
  "PrivateNote": "Synced from Mercury - txn_abc123"
}
```

### C. Dify 工作流 JSON 示例（简化）

```json
{
  "nodes": [
    {
      "id": "start",
      "type": "start",
      "data": {
        "variables": [
          {"name": "mercury_account_id", "type": "string"},
          {"name": "start_date", "type": "string"},
          {"name": "end_date", "type": "string"}
        ]
      }
    },
    {
      "id": "get_mercury_txns",
      "type": "tool",
      "data": {
        "provider": "mercury",
        "tool": "get_transactions",
        "inputs": {
          "account_id": "{{start.mercury_account_id}}",
          "start_date": "{{start.start_date}}",
          "end_date": "{{start.end_date}}"
        }
      }
    },
    {
      "id": "iterate_txns",
      "type": "iteration",
      "data": {
        "input": "{{get_mercury_txns.transactions}}"
      }
    },
    {
      "id": "map_to_qb",
      "type": "llm",
      "parent": "iterate_txns",
      "data": {
        "model": "gpt-4",
        "prompt": "映射 Mercury 交易到 QuickBooks..."
      }
    },
    {
      "id": "create_qb_record",
      "type": "tool",
      "parent": "iterate_txns",
      "data": {
        "provider": "quickbooks",
        "tool": "create_purchase",
        "inputs": "{{map_to_qb.output}}"
      }
    },
    {
      "id": "end",
      "type": "end",
      "data": {
        "outputs": [
          {"name": "success_count"},
          {"name": "failed_count"},
          {"name": "errors"}
        ]
      }
    }
  ]
}
```

---

**文档版本**：v1.0
**创建日期**：2025-12-19
**作者**：Dify Solution Architect
**状态**：待审核
