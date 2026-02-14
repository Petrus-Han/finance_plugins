# QuickBooks Online Plugin

Manage accounting operations in QuickBooks Online — record transactions, manage vendors and customers, handle invoicing, and query financial data.

## Setup

1. Register at [Intuit Developer Portal](https://developer.intuit.com) and create a QuickBooks app
2. Obtain **Client ID** and **Client Secret**
3. Install this plugin in Dify and enter the OAuth credentials
4. Authorize via the OAuth flow — the plugin automatically captures your Company ID (realm_id)
5. Select environment: **Sandbox** (testing) or **Production** (live accounting)

Required OAuth scope: `com.intuit.quickbooks.accounting`

## Tools

### Transactions
- **Record Deposit** — Record income deposits to bank accounts
- **Record Expense** — Record purchases and expenses
- **Transfer Between Accounts** — Move funds between accounts

### Journal Entries
- **Create Journal Entry** — Create a new journal entry
- **View Journal Entries** — Query existing journal entries
- **Edit Journal Entry** — Update a journal entry
- **Delete Journal Entry** — Remove a journal entry

### Invoicing & Billing
- **Create Invoice** — Create a customer invoice
- **Record Bill** — Record a vendor bill
- **Pay Vendor Bills** — Create bill payments
- **Manage Sales Receipts** — Create and query sales receipts
- **Manage Credit Memos** — Create and query credit memos
- **Manage Refunds** — Create and query refund receipts
- **Manage Estimates** — Create and query estimates
- **Manage Customer Payments** — Record customer payments

### People & Companies
- **Manage Vendors** — Search or create vendors
- **Manage Customers** — Search or create customers
- **Manage Employees** — Search or create employees

### Products & Accounts
- **View Account Categories** — Query chart of accounts with optional type filter (Bank, Income, Expense, etc.)
- **Manage Products & Services** — Search or create items
- **Manage Classes** — Search or create classes for categorization
- **Manage Locations** — Search or create departments/locations
- **Manage Purchase Orders** — Create and query purchase orders

### Other
- **Manage Attachments** — Upload and manage file attachments
- **Advanced Search** — Query any QuickBooks entity with custom filters
