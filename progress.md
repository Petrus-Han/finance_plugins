# 插件开发进度

## 当前迭代：全量 API 支持

**开始日期**: 2025-01-21
**目标**: Mercury 新增 10 tools, QuickBooks 新增 14 tools

---

## Mercury Tools Plugin

### Cards & Statements
- [ ] `get_cards` - 获取账户信用卡列表
- [ ] `get_statements` - 获取账单列表
- [ ] `download_statement` - 下载账单 PDF

### Accounts Receivable
- [ ] `customer_management` - 客户 CRUD
- [ ] `invoice_management` - 发票 CRUD + 取消
- [ ] `get_invoice_pdf` - 下载发票 PDF

### Recipients & Transactions
- [ ] `edit_recipient` - 编辑收款人
- [ ] `get_events` - 获取事件列表
- [ ] `upload_transaction_attachment` - 上传交易附件
- [ ] `upload_recipient_attachment` - 上传收款人附件

**进度**: 0/10

---

## QuickBooks Plugin

### 核心交易
- [ ] `payment_management` - 收款管理
- [ ] `bill_payment_management` - 付款管理
- [ ] `journal_entry_management` - 日记账分录
- [ ] `item_management` - 商品/服务管理
- [ ] `attachable_management` - 附件管理

### 销售流程
- [ ] `estimate_management` - 报价单管理
- [ ] `sales_receipt_management` - 销售收据管理
- [ ] `credit_memo_management` - 贷项凭单管理
- [ ] `refund_receipt_management` - 退款收据管理

### 采购流程
- [ ] `purchase_order_management` - 采购订单管理

### 组织管理
- [ ] `employee_management` - 员工管理
- [ ] `class_management` - 分类管理
- [ ] `department_management` - 部门管理

### 通用功能
- [ ] `query_entities` - 通用实体查询

**进度**: 0/14

---

## Backlog

- [ ] Mercury Trigger: 支持 polling 模式

---

## 已完成

(开发中...)
