# Mercury Banking Tools

Access Mercury Bank accounts, transactions, recipients, and payments through the Mercury API.

## Setup

1. Log in to [Mercury](https://mercury.com) → **Settings** → **API Tokens**
2. Create a token with the permissions you need (e.g., `read:accounts`, `read:transactions`, `write:recipients`)
3. Install this plugin in Dify and enter your API token
4. Select API environment: **Sandbox** (testing) or **Production** (live data)

## Tools

### Accounts
- **Get Bank Accounts** — List all accounts with balances
- **Get Account Details** — View a specific account's full details

### Transactions
- **Get Transactions** — Query transaction history with date range, status, and pagination filters
- **Get Transaction Details** — View a single transaction
- **Add Note to Transaction** — Attach a note to a transaction
- **Attach File to Transaction** — Upload an attachment to a transaction

### Payments
- **Send Payment** — Send money to a recipient (ACH, wire, or check)
- **Internal Transfer** — Transfer funds between your Mercury accounts

### Recipients
- **Get Recipients** — List all saved recipients
- **Get Recipient Details** — View a specific recipient
- **Add New Recipient** — Create a new payment recipient
- **Edit Recipient** — Update recipient details
- **Attach File to Recipient** — Upload a document to a recipient profile

### Cards
- **Get Employee Cards** — List debit cards issued to employees

### Statements
- **Get Statements** — List available bank statements
- **Download Statement PDF** — Download a statement as PDF

### Invoicing
- **Manage Invoices** — Create, search, and manage invoices
- **Manage Invoicing Customers** — Create and search invoice customers
- **Download Invoice PDF** — Download an invoice as PDF

### Activity
- **Get Activity Log** — View account activity events
