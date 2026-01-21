# QuickBooks Plugin 开发笔记

## 工具概览

| 工具 | 功能 | 关键参数 |
|------|------|---------|
| `create_bill` | 创建应付账款 | vendor_id, line_items |
| `create_invoice` | 创建应收发票 | customer_id, line_items |
| `create_purchase` | 创建采购/费用 | account_id, line_items |
| `create_deposit` | 创建存款 | account_id, line_items |
| `create_transfer` | 账户转账 | from_account_id, to_account_id |
| `vendor_management` | 供应商管理 | action (search/create), name |
| `customer_management` | 客户管理 | action, name |
| `get_chart_of_accounts` | 获取会计科目 | account_type (可选) |

---

## Create Bill 使用指南

### 必需参数

1. **vendor_id** - 供应商 ID（通过 `vendor_management` 搜索获取）
2. **line_items** - JSON 格式的行项目数组

### Line Items 结构

```json
[
  {
    "amount": 500,           // 必填：金额
    "description": "描述",    // 可选：行描述
    "account_id": "15",      // 可选：费用账户 ID
    "customer_id": "123",    // 可选：客户 ID（可计费时）
    "billable_status": "Billable"  // 可选：Billable/NotBillable/HasBeenBilled
  }
]
```

### 使用示例

```json
{
  "vendor_id": "56",
  "line_items": "[{\"amount\": 200, \"description\": \"办公用品\", \"account_id\": \"15\"}, {\"amount\": 50, \"description\": \"快递费\", \"account_id\": \"31\"}]",
  "txn_date": "2026-01-20",
  "due_date": "2026-02-20",
  "doc_number": "INV-001"
}
```

---

## Chart of Accounts (会计科目表)

### 什么是 Chart of Accounts？

会计科目表是公司用来分类记录财务交易的账户列表。创建 Bill 时需要指定费用归属的账户。

### 常用费用账户 (Expense)

| ID | 名称 | 用途 |
|----|------|------|
| `15` | Office Expenses | 办公费用 |
| `20` | Supplies | 用品/耗材 |
| `7` | Advertising | 广告费 |
| `11` | Insurance | 保险 |
| `17` | Rent or Lease | 租金 |
| `24` | Utilities | 水电费 |
| `12` | Legal & Professional Fees | 法律/专业服务费 |
| `22` | Travel | 差旅费 |
| `31` | Uncategorized Expense | 未分类费用（默认） |

### 账户类型说明

| Type | 中文 | 说明 |
|------|------|------|
| `Expense` | 费用 | 日常支出，用于 Bill/Purchase |
| `Income` | 收入 | 销售/服务收入 |
| `Bank` | 银行 | 银行账户 |
| `Accounts Payable` | 应付账款 | 欠供应商的钱 |
| `Accounts Receivable` | 应收账款 | 客户欠的钱 |
| `Asset` | 资产 | 公司拥有的资产 |
| `Liability` | 负债 | 公司的债务 |
| `Equity` | 权益 | 所有者权益 |

---

## 待开发功能

### 1. Vendor 列表功能 (P1)

**当前问题**: `vendor_management` 的 search 功能必须提供名称，无法列出所有供应商。

**建议方案**: 添加 `list` action 或允许空名称搜索返回所有供应商。

```yaml
# vendor_management.yaml 修改建议
- name: action
  options:
  - value: search
  - value: create
  - value: list    # 新增
```

---

### 2. Accounting & Ledgers (会计与分类账) (P1)

#### 2.1 Journal Entry (日记账分录)

**用途**: 手工调账、期末调整、跨账户调整

**QuickBooks API**: `POST /v3/company/{realmId}/journalentry`

**参数设计**:
```yaml
parameters:
  - name: line_items      # 借贷方明细 (DebitAmount/CreditAmount)
  - name: txn_date        # 交易日期
  - name: doc_number      # 凭证号
  - name: private_note    # 内部备注
```

**Line Item 结构**:
```json
[
  {"account_id": "35", "amount": 1000, "posting_type": "Debit", "description": "银行存款增加"},
  {"account_id": "1", "amount": 1000, "posting_type": "Credit", "description": "服务收入"}
]
```

#### 2.2 General Ledger Query (总账查询)

**用途**: 查询指定账户的明细记录

**QuickBooks API**: `GET /v3/company/{realmId}/reports/GeneralLedger`

---

### 3. Employee & Payroll (员工与工资单) (P2)

#### 3.1 Employee Management (员工管理)

**QuickBooks API**:
- `GET /v3/company/{realmId}/query?query=select * from Employee`
- `POST /v3/company/{realmId}/employee`
- `GET /v3/company/{realmId}/employee/{employeeId}`

**功能**:
| Action | 说明 |
|--------|------|
| list | 列出所有员工 |
| search | 按名称搜索员工 |
| create | 创建新员工 |
| get | 获取员工详情 |

#### 3.2 Payroll (工资单) - 需要 Payroll 订阅

**注意**: QuickBooks Payroll API 需要额外订阅，基础版可能不支持。

**QuickBooks API**:
- `GET /v3/company/{realmId}/query?query=select * from PayrollItem`

---

### 4. Reporting (报表) (P2)

#### 4.1 Profit and Loss (损益表)

**QuickBooks API**: `GET /v3/company/{realmId}/reports/ProfitAndLoss`

**参数**:
```yaml
parameters:
  - name: start_date      # 开始日期
  - name: end_date        # 结束日期
  - name: accounting_method  # Cash / Accrual
  - name: summarize_column_by  # Total / Month / Week
```

#### 4.2 Balance Sheet (资产负债表)

**QuickBooks API**: `GET /v3/company/{realmId}/reports/BalanceSheet`

**参数**:
```yaml
parameters:
  - name: start_date
  - name: end_date
  - name: accounting_method
```

#### 4.3 Cash Flow (现金流量表)

**QuickBooks API**: `GET /v3/company/{realmId}/reports/CashFlow`

#### 4.4 Accounts Receivable Aging (应收账款账龄)

**QuickBooks API**: `GET /v3/company/{realmId}/reports/AgedReceivables`

#### 4.5 Accounts Payable Aging (应付账款账龄)

**QuickBooks API**: `GET /v3/company/{realmId}/reports/AgedPayables`

---

### 5. Customer Management 增强 (P2)

**现有功能**: list / search / create

**待添加**:
| 功能 | API | 说明 |
|------|-----|------|
| update | `POST /customer` | 更新客户信息 |
| delete | `POST /customer` (Active=false) | 停用客户 |
| get_balance | Query | 获取客户余额明细 |

---

## 开发优先级

| 优先级 | 功能 | 原因 |
|--------|------|------|
| P1 | Vendor 列表 | 创建 Bill 的前置依赖 |
| P1 | Journal Entry | 手工调账的核心功能 |
| P2 | 报表功能 | 财务分析常用 |
| P2 | 员工管理 | 工资相关场景 |
| P3 | Payroll | 需要额外订阅 |

---

## 调试方法

### 查看日志

```bash
tail -f /tmp/quickbooks_plugin.log
```

### 重启插件

```bash
pkill -f "quickbooks_plugin.*main"
cd /home/ubuntu/playground/finance_plugins/quickbooks_plugin
uv run python main.py > /tmp/quickbooks_plugin.log 2>&1 &
```

### 远程调试配置

`.env` 文件:
```
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=dify.greeep.com
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=<your-debug-key>
```

---

## QuickBooks API 环境

| 环境 | Base URL |
|------|----------|
| Sandbox | `https://sandbox-quickbooks.api.intuit.com/v3` |
| Production | `https://quickbooks.api.intuit.com/v3` |

### API 版本

所有请求使用 `minorversion=65` 参数。

---

## 关键文件

| 文件 | 说明 |
|------|------|
| `tools/create_bill.py` | 创建 Bill 逻辑 |
| `tools/create_bill.yaml` | Bill 参数定义 |
| `tools/vendor_management.py` | 供应商管理 |
| `tools/get_chart_of_accounts.py` | 获取会计科目 |
| `provider/quickbooks.yaml` | 凭证配置 |
