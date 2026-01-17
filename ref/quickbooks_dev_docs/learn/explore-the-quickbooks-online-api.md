# What You Can Do with the QuickBooks Online Accounting API

> Source: https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api

The QuickBooks Online Accounting API uses the [REST framework](./rest-api-features.md). It uses standard HTTP methods and JSON for input and output.

Generally, our APIs let apps utilize most customer-facing features in QuickBooks Online.

> **Tip**: This guide covers QuickBooks Online and its APIs. It doesn't include:
> - [QuickBooks Payments API](https://developer.intuit.com/app/developer/qbpayments/docs/get-started)
> - [QuickBooks Desktop API](https://developer.intuit.com/app/developer/qbdesktop/docs/get-started)
> - [QuickBooks Time API](https://quickbooks.intuit.com/time-tracking/) (formally T-Sheets)

---

## The QuickBooks Online Accounting API Resource Model

The QuickBooks Online Accounting API lets your apps utilize key features and data in QuickBooks Online.

Individual API entities correspond with forms, lists, and other tools in the customer-facing QuickBooks Online UI. For instance, apps can use the [Invoice](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/invoice) entity to create, read, or send invoices in your users' QuickBooks Online companies.

---

## Choosing API Entities to Build Your App

When you start building your app:
1. Decide generally what you want it to do
2. Pick the specific API entities needed to use the relevant features and data
3. Visit the [API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account) to learn more about specific entities

If you don't want to start from scratch, you can [build your app around one of workflow examples](https://developer.intuit.com/app/developer/qbo/docs/workflows).

---

## Basic API Resources and Resource Categories

By "resources," we mean the API entities your app can use to create or update data in QuickBooks Online. These entities correspond to data points businesses use for accounting:
- Forms (invoices, bills, receipts)
- Accounts (bank, expense, tax, etc.)
- Groups (lists, inventory items, etc.)

### List Entities/Resources

Lists used to track individuals or accounts commonly referenced in transactions. Also called "name lists."

| API Entity | Description |
|------------|-------------|
| [Account](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/account) | Chart of accounts |
| [Customer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/customer) | Customers/clients |
| [Vendor](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/vendor) | Suppliers/payees |
| [Employee](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/employee) | Employees |

### Transaction Entities/Resources

Sales forms used for transactions.

| API Entity | Description |
|------------|-------------|
| [Invoice](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/invoice) | Customer invoices |
| [Bill](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/bill) | Vendor bills |
| [Payment](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/payment) | Customer payments |
| [BillPayment](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/billpayment) | Bill payments |
| [Refund](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/refundreceipt) | Refund receipts |

### Reports Entities/Resources

Reports used to track business metrics.

| API Entity | Description |
|------------|-------------|
| [ProfitAndLoss](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/profitandlossdetail) | Income statement |
| [GeneralLedger](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/generalledger) | General ledger |
| [CashFlow](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/report-entities/cashflow) | Cash flow statement |

### Inventory Entities/Resources

| API Entity | Description |
|------------|-------------|
| [Item](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/item) | Products, services, inventory hierarchies, and bundles |

### Journal Entry

A type of record that accountants use to make corrections or major changes to a chart of accounts, such as year-end adjustments or errors. **Use sparingly.**

| API Entity | Description |
|------------|-------------|
| [JournalEntry](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/journalentry) | General journal entries |

---

## Basic Operations

Visit the [QuickBooks Online Accounting API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account) to see the specific operations each entity supports.

### Single Requests

You can send single requests. The server individually processes and responds to single requests.

### Query Requests

You can send a query via the [Intuit Developer SQL-like query language](./explore-the-quickbooks-online-api/data-queries.md). The server returns the data in a single response or paged as needed.

### Batch Operations

You can call multiple API entities and perform multiple operations at once. For example, you can use a single batch request to:
- Create a new customer
- Update an invoice
- Read an account

Batch requests improve app performance by decreasing network round trips and increasing throughput. Learn more about [batch operations](./explore-the-quickbooks-online-api/batch.md).

> **Important**: Use batch operations for **transactions only**. Don't use it for list resources like customers, vendors, items, etc.

### Change Data Capture Operations

This operation returns the list of entities that have changed within a specific timeframe.

Change data capture operations are useful for apps that:
- Periodically poll QuickBooks Online companies
- Refresh local copies of entity data

Learn more about [change data capture operation](./explore-the-quickbooks-online-api/change-data-capture.md).

---

## Update Operations

There are two ways to update entities:

| Type | Use Case |
|------|----------|
| **Sparse updates** | Change specific subsets of fields |
| **Full updates** | Make broad changes |

> **Note**: You must serially perform updates and additions to list entities (customers, accounts, vendors, classes, etc.).

### Why Use Sparse Updates

| Advantage | Description |
|-----------|-------------|
| **Prevent unintended overwrites** | Full updates clear fields that weren't sent. Sparse updates only change specified fields. |
| **Reduce request payload sizes** | Especially useful for mobile apps with spotty connections. |
| **Facilitate future field additions** | Acts as a "merge" for existing entities without clearing existing fields. |

### Making Sparse Updates

Sparse update operations let you update specific fields of an existing entity.

1. Specify the writable properties you want to update in the request body
2. Include the `sparse="true"` attribute in the request body
3. Missing attributes are **not** updated or cleared

### Making Full Updates

Full update operations update **all** writable attributes of an existing entity.

1. Use the `id` field to specify the entity you want to update
2. If a writable attribute is omitted, it's cleared and set to `NULL`

> **Tip**: Read-only values are ignored and replaced by defaults. No error is returned.

---

## Delete Operations

There are two ways to delete entities:

| Type | Entities | Description |
|------|----------|-------------|
| **Soft deletes** | List entities (customers, accounts, vendors, etc.) | Deactivates the entity. Can reactivate later. |
| **Hard deletes** | Transaction entities (invoices, estimates, etc.) | Permanently deletes. Cannot undo. |

### Soft Deletes

Soft deletes mark an entity as inactive. It doesn't delete the record—just hides it for display purposes. References to inactive entities remain intact.

To soft delete:
1. Use an update operation
2. Set `active` field to `false`

To reactivate:
1. Use an update operation
2. Set `active` field back to `true`

> **Note**: Queries without "inactive" filter only return "active" entities.

### Hard Deletes

Hard deletes permanently delete the entire entity. **Cannot be undone.**

**Simplified delete** (for Bill, BillPayment, CreditMemo, Estimate, Invoice, JournalEntry, Payment, Purchase, PurchaseOrder, RefundReceipt, SalesReceipt, TimeActivity, VendorCredit):
- Enter the `id` and `syncToken` in the request body

**Full payload delete** (for all other transaction entities):
- Include the full payload as returned in a read response

---

## Learn More

- [REST API Features](./rest-api-features.md)
- [Data Queries](./explore-the-quickbooks-online-api/data-queries.md)
- [Batch Operations](./explore-the-quickbooks-online-api/batch.md)
- [Change Data Capture](./explore-the-quickbooks-online-api/change-data-capture.md)
- [Basic Bookkeeping](./learn-basic-bookkeeping.md)
