# 插件开发进度

## 当前迭代：全量 API 支持

**开始日期**: 2025-01-21
**目标**: Mercury 新增 10 tools, QuickBooks 新增 14 tools

---

## Mercury Tools Plugin

### Cards & Statements
- [x] `get_cards` - 获取账户信用卡列表 ✅
- [x] `get_statements` - 获取账单列表 ✅
- [x] `download_statement` - 下载账单 PDF ✅

### Accounts Receivable
- [x] `customer_management` - 客户 CRUD ✅
- [x] `invoice_management` - 发票 CRUD + 取消 ✅
- [x] `get_invoice_pdf` - 下载发票 PDF ✅

### Recipients & Transactions
- [x] `edit_recipient` - 编辑收款人 ✅
- [x] `get_events` - 获取事件列表 ✅
- [x] `upload_transaction_attachment` - 上传交易附件 ✅
- [x] `upload_recipient_attachment` - 上传收款人附件 ✅

**进度**: 10/10 ✅ 已完成

---

## QuickBooks Plugin

### 核心交易
- [x] `payment_management` - 收款管理 ✅
- [x] `bill_payment_management` - 付款管理 ✅
- [x] `journal_entry_management` - 日记账分录 ✅
- [x] `item_management` - 商品/服务管理 ✅
- [x] `attachable_management` - 附件管理 ✅

### 销售流程
- [x] `estimate_management` - 报价单管理 ✅
- [x] `sales_receipt_management` - 销售收据管理 ✅
- [x] `credit_memo_management` - 贷项凭单管理 ✅
- [x] `refund_receipt_management` - 退款收据管理 ✅

### 采购流程
- [x] `purchase_order_management` - 采购订单管理 ✅

### 组织管理
- [x] `employee_management` - 员工管理 ✅
- [x] `class_management` - 分类管理 ✅
- [x] `department_management` - 部门管理 ✅

### 通用功能
- [x] `query_entities` - 通用实体查询 ✅

**进度**: 14/14 ✅ 已完成

---

## Backlog

- [ ] Mercury Trigger: 支持 polling 模式

---

## 已完成

### 2025-01-21
- Mercury Tools: 全部 10 个新 tools 开发完成
- QuickBooks: 全部 14 个新 tools 开发完成

### 待完成
- [ ] 将新开发的 tools 添加到 git 并提交
- [ ] 测试验证
