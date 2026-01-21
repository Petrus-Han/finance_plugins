# 插件全量 API 支持开发计划

> 目标：作为通用集成平台，全面支持 Mercury 和 QuickBooks API

## 业务背景

- Mercury 信用卡：所有员工持有
- Mercury 储蓄卡：少部分人持有，用于工资发放和海外交易
- QuickBooks：记账

## 当前状态

| 插件 | 已实现 | 计划新增 |
|------|--------|----------|
| Mercury Tools | 13 tools | 7 tools |
| Mercury Trigger | webhook处理 | - |
| QuickBooks | 8 tools | 14 tools |
| QuickBooks Payments | 7 tools | - |

---

## Phase 1: Mercury Tools 扩展 (10 tools)

### Cards & Statements
| Tool | API | 状态 |
|------|-----|------|
| `get_cards` | `GET /account/{id}/cards` | ✅ 已完成 |
| `get_statements` | `GET /account/{id}/statements` | ✅ 已完成 |
| `download_statement` | `GET /statement/{id}/pdf` | ✅ 已完成 |

### Accounts Receivable (AR)
| Tool | API | 状态 |
|------|-----|------|
| `customer_management` | `/customers`, `/customer/{id}` | ✅ 已完成 |
| `invoice_management` | `/invoices`, `/invoice/{id}` | ✅ 已完成 |
| `get_invoice_pdf` | `GET /invoice/{id}/pdf` | ✅ 已完成 |

### Recipients & Transactions 补充
| Tool | API | 状态 |
|------|-----|------|
| `edit_recipient` | `POST /recipient/{id}` | ✅ 已完成 |
| `get_events` | `GET /events`, `/event/{id}` | ✅ 已完成 |
| `upload_transaction_attachment` | `POST /transactions/{id}/attachment` | ✅ 已完成 |
| `upload_recipient_attachment` | `POST /recipient/{id}/attachment` | ✅ 已完成 |

---

## Phase 2: QuickBooks 扩展 (14 tools)

### 核心交易 (T1)
| Tool | Entity | 状态 |
|------|--------|------|
| `payment_management` | Payment | ✅ 已完成 |
| `bill_payment_management` | BillPayment | ✅ 已完成 |
| `journal_entry_management` | JournalEntry | ✅ 已完成 |
| `item_management` | Item | ✅ 已完成 |
| `attachable_management` | Attachable | ✅ 已完成 |

### 销售流程 (T2)
| Tool | Entity | 状态 |
|------|--------|------|
| `estimate_management` | Estimate | ✅ 已完成 |
| `sales_receipt_management` | SalesReceipt | ✅ 已完成 |
| `credit_memo_management` | CreditMemo | ✅ 已完成 |
| `refund_receipt_management` | RefundReceipt | ✅ 已完成 |

### 采购流程 (T2)
| Tool | Entity | 状态 |
|------|--------|------|
| `purchase_order_management` | PurchaseOrder | ✅ 已完成 |

### 组织管理 (T2)
| Tool | Entity | 状态 |
|------|--------|------|
| `employee_management` | Employee | ✅ 已完成 |
| `class_management` | Class | ✅ 已完成 |
| `department_management` | Department | ✅ 已完成 |

### 通用查询 (T2)
| Tool | 说明 | 状态 |
|------|------|------|
| `query_entities` | 支持任意实体的 Query 查询 | ✅ 已完成 |

---

## 未来计划 (Backlog)

- [x] Mercury Trigger: 支持 polling 模式 ✅ (通过增强 get_events tool 实现)
- [ ] QuickBooks 报表类 API（BalanceSheet, P&L, CashFlow 等）
- [ ] QuickBooks 税务相关 API

---

## 决策记录

| 日期 | 决策 | 原因 |
|------|------|------|
| 2025-01-21 | 不实现 Mercury webhook 管理 | 未来用 polling 模式替代 |
| 2025-01-21 | 优先实现 Cards/Statements | 所有员工都用信用卡 |
