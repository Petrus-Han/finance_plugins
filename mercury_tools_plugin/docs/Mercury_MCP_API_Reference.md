# Mercury MCP & API 开发参考文档

## 概述

Mercury 提供两种 API 访问方式：

| 类型 | 权限 | 用途 | 认证方式 |
|------|------|------|----------|
| **Mercury MCP** | 只读 | AI 工具集成、数据分析、账户监控 | OAuth2 |
| **Mercury API** | 读写 | 完整功能：支付、转账、发票等 | API Token / OAuth2 |

---

## 一、Mercury MCP 工具列表（只读）

Mercury MCP 是一个专为 AI 工具设计的托管服务器，通过 Model Context Protocol 提供安全的只读访问。

### 1.1 账户相关

| 工具名 | 描述 | 示例提示 |
|--------|------|----------|
| `getAccount` | 通过 ID 获取账户详情 | "What's the balance in my checking account?" |
| `getAccounts` | 获取所有账户列表 | "Show all my active accounts" |
| `getAccountCards` | 获取账户关联的卡片 | "What cards are linked to my main account?" |
| `getAccountStatements` | 获取账户对账单（支持日期过滤） | "Get my account statements from January through March" |

### 1.2 交易相关

| 工具名 | 描述 | 示例提示 |
|--------|------|----------|
| `listTransactions` | 列出交易记录（支持高级过滤、分页） | "Graph my last 6 months of transactions" |
| `getTransaction` | 通过 ID 获取交易详情 | "Get more details about transaction txn789" |

### 1.3 收款人相关

| 工具名 | 描述 | 示例提示 |
|--------|------|----------|
| `getRecipients` | 获取所有收款人列表 | "List all my payment recipients" |
| `getRecipient` | 通过 ID 获取收款人详情 | "What are the payment details for Acme Corp?" |

### 1.4 分类与组织

| 工具名 | 描述 | 示例提示 |
|--------|------|----------|
| `listCategories` | 获取自定义支出分类列表 | "What expense categories do I have set up?" |
| `getOrganization` | 获取组织/公司信息 | "What's my company's EIN?" |

### 1.5 信用与财库

| 工具名 | 描述 | 示例提示 |
|--------|------|----------|
| `listCredit` | 获取所有信用账户 | "How much credit do I have available?" |
| `getTreasury` | 获取财库账户 | "How much do I have in treasury?" |
| `getTreasuryTransactions` | 获取财库交易记录 | "Show me recent treasury account activity" |

---

## 二、Mercury API 完整接口

### 2.1 Accounts（账户）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/account/{accountId}` | 获取账户详情 |
| `GET` | `/api/v1/accounts` | 获取所有账户 |
| `GET` | `/api/v1/account/{accountId}/cards` | 获取账户卡片 |
| `GET` | `/api/v1/account/{accountId}/statements` | 获取账户对账单 |
| `GET` | `/api/v1/account/{accountId}/transaction/{transactionId}` | 获取交易详情 |
| `GET` | `/api/v1/account/{accountId}/transactions` | 列出账户交易 |
| `POST` | `/api/v1/account/{accountId}/transactions` | 创建交易（支付） |
| `POST` | `/api/v1/account/{accountId}/send-money` | 请求发送资金 |
| `POST` | `/api/v1/transfer` | 创建内部转账 |

#### 账户响应结构

```json
{
  "id": "uuid",
  "accountNumber": "string",
  "routingNumber": "string",
  "name": "string",
  "nickname": "string | null",
  "kind": "string",
  "type": "mercury | external | recipient",
  "status": "active | deleted | pending | archived",
  "currentBalance": 0,
  "availableBalance": 0,
  "legalBusinessName": "string",
  "dashboardLink": "string",
  "createdAt": "2016-07-22T00:00:00Z",
  "canReceiveTransactions": true
}
```

### 2.2 Transactions（交易）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/transactions` | 获取所有交易（跨账户） |
| `PATCH` | `/api/v1/transaction/{transactionId}` | 更新交易信息 |

#### 交易查询参数

| 参数 | 类型 | 描述 |
|------|------|------|
| `limit` | integer | 返回记录数量限制 |
| `offset` | integer | 分页偏移量 |
| `start` | string | 开始日期 (YYYY-MM-DD) |
| `end` | string | 结束日期 (YYYY-MM-DD) |
| `status` | string | 交易状态过滤 |
| `search` | string | 搜索关键词 |
| `mercuryCategory` | string | Mercury 内置分类过滤 |
| `categoryId` | string | 自定义分类 ID 过滤 |

### 2.3 Recipients（收款人）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/recipients` | 获取所有收款人 |
| `GET` | `/api/v1/recipient/{recipientId}` | 获取收款人详情 |
| `POST` | `/api/v1/recipients` | 创建收款人 |
| `PATCH` | `/api/v1/recipient/{recipientId}` | 更新收款人 |
| `DELETE` | `/api/v1/recipient/{recipientId}` | 删除收款人 |

### 2.4 Categories（分类）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/categories` | 获取所有自定义分类 |

### 2.5 Credit（信用）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/credit` | 获取信用账户列表 |

### 2.6 Treasury（财库）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/treasury` | 获取财库账户 |
| `GET` | `/api/v1/treasury/{treasuryId}/transactions` | 获取财库交易 |

### 2.7 Organization（组织）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/organization` | 获取组织信息 |

### 2.8 Users（用户）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/users` | 获取所有用户 |
| `GET` | `/api/v1/user/{userId}` | 获取用户详情 |

### 2.9 Statements（对账单）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/statement/{statementId}/pdf` | 下载对账单 PDF |

### 2.10 Send Money Requests（付款请求）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/send-money-request/{requestId}` | 获取付款请求详情 |

### 2.11 Accounts Receivable（应收账款 - Beta）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/accounts_receivable/invoices` | 获取发票列表 |
| `POST` | `/api/v1/accounts_receivable/invoices` | 创建发票 |
| `GET` | `/api/v1/accounts_receivable/invoice/{invoiceId}` | 获取发票详情 |

### 2.12 Webhooks（Webhook）

| 方法 | 端点 | 描述 |
|------|------|------|
| `GET` | `/api/v1/webhooks` | 获取 Webhook 配置 |
| `POST` | `/api/v1/webhooks` | 创建 Webhook |
| `DELETE` | `/api/v1/webhook/{webhookId}` | 删除 Webhook |

---

## 三、认证方式

### 3.1 API Token

```bash
curl --request GET \
  --url https://api.mercury.com/api/v1/accounts \
  --header 'Authorization: Bearer YOUR_API_TOKEN' \
  --header 'accept: application/json;charset=utf-8'
```

### 3.2 OAuth2 流程

1. **发起授权请求**
   ```
   GET https://mercury.com/oauth/authorize
   ?client_id=YOUR_CLIENT_ID
   &redirect_uri=YOUR_REDIRECT_URI
   &response_type=code
   &scope=read write
   ```

2. **获取 Access Token**
   ```bash
   POST https://api.mercury.com/oauth/token
   Content-Type: application/json
   
   {
     "client_id": "YOUR_CLIENT_ID",
     "client_secret": "YOUR_CLIENT_SECRET",
     "code": "AUTHORIZATION_CODE",
     "grant_type": "authorization_code",
     "redirect_uri": "YOUR_REDIRECT_URI"
   }
   ```

---

## 四、环境

| 环境 | Base URL |
|------|----------|
| **Production** | `https://api.mercury.com` |
| **Sandbox** | `https://sandbox.mercury.com` |

### Sandbox 特点
- 完全隔离的测试环境
- 预填充测试数据
- API Token 格式：`secret-token:mercury_sandbox_...`

---

## 五、MCP vs API 对比

| 特性 | MCP | API |
|------|-----|-----|
| 权限 | 只读 | 读写 |
| 认证 | OAuth2 | API Token / OAuth2 |
| 适用场景 | AI 助手、数据分析、监控 | 完整自动化、支付集成 |
| 安全性 | 高（无法发起付款） | 需谨慎管理权限 |

### 插件开发建议

1. **查询类功能** → 可参考 MCP 工具设计
2. **操作类功能** → 使用完整 API
3. **混合模式** → 查询用 MCP 思路，操作用 API

---

## 六、现有插件覆盖情况

### mercury_tools_plugin（已实现）

| 工具 | 状态 | 对应 MCP 工具 |
|------|------|--------------|
| `get_accounts` | ✅ | `getAccounts` |
| `get_account` | ✅ | `getAccount` |
| `get_transactions` | ✅ | `listTransactions` |

### 待开发功能

| 功能 | 优先级 | 对应接口 |
|------|--------|----------|
| 获取账户卡片 | 中 | `getAccountCards` |
| 获取收款人 | 中 | `getRecipients` |
| 获取分类 | 低 | `listCategories` |
| 获取对账单 | 低 | `getAccountStatements` |
| 创建交易（支付） | 高 | `createTransaction` |
| 内部转账 | 中 | `createInternalTransfer` |
| 管理收款人 | 中 | Recipients CRUD |

---

## 七、参考链接

- [Mercury API 官方文档](https://docs.mercury.com/reference)
- [Mercury MCP 指南](https://docs.mercury.com/docs/what-is-mercury-mcp)
- [MCP 工具列表](https://docs.mercury.com/docs/supported-tools-on-mercury-mcp)
- [Sandbox 使用指南](https://docs.mercury.com/docs/using-mercury-sandbox)
- [API Changelog](https://docs.mercury.com/changelog)
