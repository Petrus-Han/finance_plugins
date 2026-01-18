# QuickBooks Online Use Cases & Workflows

> Source: https://developer.intuit.com/app/developer/qbo/docs/workflows

This section contains official QuickBooks Online workflow documentation and Mercury-specific sync patterns.

---

## Official QuickBooks Workflows

### Transaction Workflows

| Workflow | Description | File |
|----------|-------------|------|
| [Create Basic Invoices](https://developer.intuit.com/app/developer/qbo/docs/workflows/create-an-invoice) | Create and manage invoices | [create-invoice.md](./create-invoice.md) |
| [Categorize Income and Expenses](https://developer.intuit.com/app/developer/qbo/docs/workflows/categorize-income-and-expenses) | Track business segments with class tracking | [categorize-income-and-expenses.md](./categorize-income-and-expenses.md) |
| [Manage Linked Transactions](https://developer.intuit.com/app/developer/qbo/docs/workflows/manage-linked-transactions) | Link related transactions (payments, bills, etc.) | [manage-linked-transactions.md](./manage-linked-transactions.md) |

### Product & Inventory

| Workflow | Description | Status |
|----------|-------------|--------|
| [Create Products, Services, and Inventory Items](https://developer.intuit.com/app/developer/qbo/docs/workflows/manage-inventory) | Manage products and services | Not scraped |

### Advanced Features

| Workflow | Description | Status |
|----------|-------------|--------|
| [Create Custom Fields](https://developer.intuit.com/app/developer/qbo/docs/workflows/create-custom-fields) | Add custom fields to transactions | Not scraped |
| [Manage Multiple Currencies](https://developer.intuit.com/app/developer/qbo/docs/workflows/manage-multiple-currencies) | Handle multi-currency transactions | Not scraped |
| [Calculate Sales Tax](https://developer.intuit.com/app/developer/qbo/docs/workflows/calculate-sales-tax) | Automated sales tax calculation | Not scraped |
| [Manage Business Units](https://developer.intuit.com/app/developer/qbo/docs/workflows/manage-business-units) | Location and department tracking | Not scraped |
| [Manage Projects](https://developer.intuit.com/app/developer/qbo/docs/workflows/manage-projects) | Project-based accounting | Not scraped |

### Attachments & Reports

| Workflow | Description | File |
|----------|-------------|------|
| [Attach Images and Notes](https://developer.intuit.com/app/developer/qbo/docs/workflows/attach-images-and-notes) | Attach files to transactions | Not scraped |
| [Run Reports](https://developer.intuit.com/app/developer/qbo/docs/workflows/run-reports) | Query financial reports | [run-reports.md](./run-reports.md) |

---

## Mercury Sync Patterns

Custom patterns for syncing Mercury bank transactions with QuickBooks Online.

| Pattern | Description | File |
|---------|-------------|------|
| Mercury Transaction Sync | Patterns for syncing Mercury transactions to QuickBooks | [mercury-sync-patterns.md](./mercury-sync-patterns.md) |

---

## Key Concepts for Mercury Integration

### Transaction Types

| Mercury Transaction | QuickBooks Entity | Notes |
|---------------------|-------------------|-------|
| Outgoing payment | `Purchase` | Use PaymentType: Cash, Check, or CreditCard |
| Incoming deposit | `Deposit` | Link to bank account |
| Wire transfer out | `Purchase` | Vendor payment |
| ACH transfer | `Transfer` | Between accounts |

### Entity Relationships

```
Mercury Transaction
    ↓
QuickBooks Purchase/Deposit
    ↓
Linked to:
  - Vendor (for payments)
  - Customer (for deposits)
  - Account (for categorization)
  - Class (for business segment tracking)
```

### Best Practices

1. **Idempotency**: Use Mercury transaction IDs as `DocNumber` to prevent duplicates
2. **Categorization**: Use Classes for business segment tracking
3. **Reconciliation**: Use Reports API to verify sync accuracy
4. **Linked Transactions**: Understand `LinkedTxn` for complex transaction flows

---

## Quick Links

### API Reference
- [Purchase](../api-reference/purchase.md) - For outgoing Mercury transactions
- [Deposit](../api-reference/deposit.md) - For incoming Mercury transactions
- [Vendor](../api-reference/vendor.md) - Payment recipients
- [Account](../api-reference/account.md) - Chart of accounts
- [Transfer](../api-reference/transfer.md) - Between accounts

### Development
- [Authentication](../develop/authentication-and-authorization/oauth-2.0.md)
- [Webhooks](../develop/webhooks.md)
- [Sandboxes](../develop/sandboxes.md)
