# QuickBooks Online Plugin

QuickBooks Online Accounting API integration for Dify - Automated accounting synchronization and transaction management.

## Overview

This plugin enables your Dify workflows to interact with QuickBooks Online for accounting operations. Create deposits, record purchases, manage vendors, and query chart of accounts programmatically.

## Features

### Transaction Management
- **Create Deposit** - Record income deposits to bank accounts
- **Create Purchase** - Record expenses and purchases

### Account Management
- **Get Chart of Accounts** - Query all accounts or filter by account type

### Vendor Operations
- **Vendor Management** - Search for existing vendors or create new ones

## Authentication

This plugin uses OAuth 2.0 authentication with QuickBooks Online.

**Required Scope**: `com.intuit.quickbooks.accounting`

### Setup Steps

1. Register at [Intuit Developer Portal](https://developer.intuit.com)
2. Create a QuickBooks Online app
3. Obtain Client ID and Client Secret
4. Configure redirect URI in Dify
5. Select environment (Sandbox for testing, Production for live accounting)

**Note**: During OAuth flow, QuickBooks will return a `realm_id` (Company ID) which is automatically captured and stored by the plugin.

## Tools Reference

### 1. Create Deposit

Create a deposit transaction in QuickBooks.

**Parameters:**
- `bank_account_id` (required): ID of the bank account receiving the deposit
- `amount` (required): Deposit amount
- `income_account_id` (required): ID of the income account
- `txn_date` (optional): Transaction date (YYYY-MM-DD)
- `description` (optional): Description of the deposit
- `note` (optional): Private note

**Example:**
```yaml
Tool: create_deposit
Parameters:
  bank_account_id: "35"
  amount: 1500.00
  income_account_id: "79"
  txn_date: "2026-01-14"
  description: "Client payment for services"
  note: "Invoice #12345"
```

**Returns:**
- Deposit ID
- Transaction date
- Total amount
- Account information
- Sync token

### 2. Create Purchase

Create a purchase/expense transaction in QuickBooks.

**Parameters:**
- `bank_account_id` (required): ID of the account used for payment
- `amount` (required): Purchase amount (will be converted to positive)
- `expense_account_id` (required): ID of the expense account
- `payment_type` (optional): Payment method (default: "CreditCard")
- `txn_date` (optional): Transaction date (YYYY-MM-DD)
- `description` (optional): Description of the purchase
- `note` (optional): Private note
- `vendor_id` (optional): ID of the vendor

**Example:**
```yaml
Tool: create_purchase
Parameters:
  bank_account_id: "35"
  amount: 250.00
  expense_account_id: "80"
  payment_type: "CreditCard"
  txn_date: "2026-01-14"
  description: "Office supplies"
  vendor_id: "56"
  note: "Monthly supplies order"
```

**Returns:**
- Purchase ID
- Transaction date
- Total amount
- Payment type
- Account and vendor information
- Sync token

### 3. Get Chart of Accounts

Retrieve accounts from the chart of accounts.

**Parameters:**
- `account_type` (optional): Filter by account type (e.g., "Bank", "Income", "Expense")

**Example:**
```yaml
Tool: get_chart_of_accounts
Parameters:
  account_type: "Bank"  # Optional: returns all accounts if not specified
```

**Returns:**
- Array of accounts with:
  - Account ID
  - Name
  - Type and sub-type
  - Active status
  - Current balance
  - Classification
  - Fully qualified name

### 4. Vendor Management

Search for or create vendors.

**Parameters:**
- `action` (required): "search" or "create"
- `name` (required): Vendor name to search for or create

**Example - Search:**
```yaml
Tool: vendor_management
Parameters:
  action: "search"
  name: "Staples"
```

**Example - Create:**
```yaml
Tool: vendor_management
Parameters:
  action: "create"
  name: "New Vendor Inc"
```

**Returns:**
- For search: Array of matching vendors with details
- For create: Newly created vendor information

## Usage Examples

### Example 1: Mercury → QuickBooks Integration

Sync Mercury transactions to QuickBooks automatically:

```yaml
Trigger: Mercury Transaction Trigger
  Event: transaction.created

Step 1: Condition
  IF: amount < 0 (debit transaction)

Step 2: Vendor Management (QuickBooks)
  action: search
  name: counterparty_name

Step 3: Create Purchase (QuickBooks)
  bank_account_id: "35"
  amount: abs(amount)
  expense_account_id: "80"
  vendor_id: {from step 2}
  txn_date: posted_at
  description: bank_description
  note: note
```

### Example 2: Record Daily Deposits

```yaml
Schedule: Daily at 9 AM

Step 1: Mercury Tools - Get Transactions
  Filter: Credits from yesterday

Step 2: Loop through transactions

Step 3: QuickBooks - Create Deposit
  bank_account_id: "35"
  amount: transaction.amount
  income_account_id: "79"
  txn_date: transaction.posted_at
  description: transaction.counterparty_name
```

### Example 3: Expense Categorization

```yaml
Trigger: Mercury Transaction Trigger
  Event: transaction.created
  Filter: debits only

Step 1: LLM - Categorize Expense
  Input: bank_description
  Output: expense_category, expense_account_id

Step 2: Get Chart of Accounts
  account_type: "Expense"

Step 3: Create Purchase
  bank_account_id: "35"
  amount: abs(amount)
  expense_account_id: {from LLM}
  description: bank_description
```

### Example 4: Vendor Auto-Creation

```yaml
Trigger: Mercury Transaction

Step 1: Vendor Management - Search
  action: search
  name: counterparty_name

Step 2: Condition
  IF: no vendors found

Step 3: Vendor Management - Create
  action: create
  name: counterparty_name

Step 4: Create Purchase
  vendor_id: {from step 3}
  # ... other parameters
```

## Environment Support

| Environment | Base URL | Use Case |
|-------------|----------|----------|
| **Sandbox** | `https://sandbox-quickbooks.api.intuit.com/v3` | Testing and development |
| Production | `https://quickbooks.api.intuit.com/v3` | Live accounting data |

**Important**: Always test in Sandbox environment before deploying to Production. Sandbox companies are completely separate from production data.

## Development & Testing

### Local Development

```bash
# Navigate to plugin directory
cd quickbooks_plugin

# Create virtual environment
uv venv
source .venv/bin/activate  # or .venv/Scripts/activate on Windows

# Install dependencies
uv pip install -r requirements.txt
```

### Remote Debugging

Configure `.env` file:
```env
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=debug.dify.ai
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=your-debug-key
```

Run the plugin:
```bash
python main.py
```

### Testing with Sandbox

1. Create a QuickBooks Sandbox company at https://developer.intuit.com
2. Configure OAuth with sandbox credentials
3. Use sandbox companies to test all operations
4. Verify workflows work correctly before production deployment

### Package Plugin

```bash
dify plugin package ./quickbooks_plugin
```

## Common Account Types

When using `get_chart_of_accounts` with filtering:

**Asset Types:**
- `Bank` - Bank accounts
- `Accounts Receivable` - Customer invoices
- `Other Current Asset` - Short-term assets

**Liability Types:**
- `Accounts Payable` - Bills to pay
- `Credit Card` - Credit card accounts
- `Other Current Liability` - Short-term liabilities

**Income Types:**
- `Income` - Revenue accounts

**Expense Types:**
- `Expense` - Operating expenses
- `Cost of Goods Sold` - Direct costs

## Troubleshooting

### Authentication Errors

1. **Token Expired**: OAuth tokens expire after 1 hour. The plugin automatically refreshes them, but if issues persist, re-authorize
2. **Wrong Environment**: Sandbox tokens don't work with Production and vice versa
3. **Missing Realm ID**: Ensure you completed the OAuth flow; realm_id is captured automatically

### Transaction Creation Failures

1. **Invalid Account ID**: Use `get_chart_of_accounts` to verify account IDs exist
2. **Inactive Account**: Check that the account is active in QuickBooks
3. **Permission Issues**: Verify your QuickBooks app has `com.intuit.quickbooks.accounting` scope

### Vendor Issues

1. **Duplicate Vendor Names**: QuickBooks prevents duplicate vendor display names
2. **Special Characters**: Some characters may need escaping in search queries

## API Reference

See [QuickBooks Online API Documentation](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities) for full API details.

### Endpoints Used

- `POST /company/{realmId}/deposit` - Create deposit
- `POST /company/{realmId}/purchase` - Create purchase
- `GET /company/{realmId}/query?query=...` - Query accounts/vendors
- `POST /company/{realmId}/vendor` - Create vendor
- `GET /company/{realmId}/companyinfo/{realmId}` - Validate credentials

## Related Plugins

- **Mercury Banking Trigger** (`mercury_trigger_plugin`): Receive real-time transaction events
- **Mercury Banking Tools** (`mercury_tools_plugin`): Query Mercury accounts and transactions
- **QuickBooks Payments** (`quickbooks_payments_plugin`): Process credit card and ACH payments

## Best Practices

1. **Use Sandbox First**: Always test workflows in sandbox before production
2. **Handle Errors Gracefully**: Add error handling in workflows for failed API calls
3. **Cache Account IDs**: Query chart of accounts once and reuse IDs
4. **Batch Operations**: For bulk imports, consider rate limiting and error recovery
5. **Track Sync Tokens**: Store sync_token for update operations (future feature)

## Version History

### v0.2.0 (2026-01-14)
- **Breaking Changes**: Complete rewrite with OAuth2 authentication
- Added environment selection (Sandbox/Production)
- Rewritten all tools with correct API patterns
- Improved error handling and error messages
- Uses httpx library for better async support
- Comprehensive documentation

### v0.1.0 (Initial)
- Basic tool implementations (deprecated)

## License

Copyright (c) 2026

## Support

For issues or questions, please refer to the Dify plugin documentation.
