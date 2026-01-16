# Mercury Banking Tools Plugin

Mercury Banking Tools plugin for Dify - Access Mercury accounts, transactions, and financial data via API.

## Overview

This plugin provides tools to interact with Mercury Banking API, allowing you to:
- Retrieve all bank accounts
- Get details for specific accounts
- Fetch transaction history with filtering

## Tools Included

### 1. Get Accounts
Retrieve all Mercury bank accounts associated with your API token.

**No parameters required**

**Returns:**
- Account ID
- Account name and type
- Current and available balance
- Routing and account numbers
- Status

### 2. Get Account
Get detailed information for a specific Mercury bank account.

**Parameters:**
- `account_id` (required): The unique identifier of the Mercury account

**Returns:**
- Full account details including balance, status, and account numbers

### 3. Get Transactions
Retrieve transaction history for a Mercury bank account with optional filtering.

**Parameters:**
- `account_id` (required): The unique identifier of the Mercury account
- `start_date` (optional): Start date for filtering (ISO 8601 format, e.g., 2026-01-01T00:00:00Z)
- `end_date` (optional): End date for filtering (ISO 8601 format)
- `limit` (optional): Maximum number of transactions to return (default 100)
- `offset` (optional): Number of transactions to skip for pagination (default 0)

**Returns:**
- List of transactions with details (amount, date, counterparty, status, etc.)
- Total count and pagination info

## Setup

### 1. Get Mercury API Token

1. Log in to your Mercury account
2. Go to **Settings** → **API Tokens**
3. Create a new token with the following permissions:
   - `read:accounts` - Access account information
   - `read:transactions` - Access transaction data
4. Copy the access token

### 2. Install Plugin in Dify

1. Upload the `mercury_tools_plugin.difypkg` to your Dify instance
2. Or use remote debugging (see below)

### 3. Configure Credentials

When using the tools, you'll be prompted to enter:
- **Mercury API Access Token**: The token you created in step 1

## Usage Examples

### Example 1: Get All Accounts

```yaml
Workflow Step: Use Tool
Tool: Get Accounts
Parameters: (none)
```

Output: List of all your Mercury accounts with balances

### Example 2: Get Specific Account Details

```yaml
Workflow Step: Use Tool
Tool: Get Account
Parameters:
  account_id: "acc_abc123xyz"
```

### Example 3: Get Recent Transactions

```yaml
Workflow Step: Use Tool
Tool: Get Transactions
Parameters:
  account_id: "acc_abc123xyz"
  start_date: "2026-01-01T00:00:00Z"
  end_date: "2026-01-31T23:59:59Z"
  limit: 50
```

### Example 4: Trigger + Tools Integration

```yaml
# Use Mercury Trigger to receive transaction events
# Then use Tools to fetch additional context

Trigger: Mercury Transaction Trigger
  → Receives transaction event

Step 1: Get Account (Tool)
  → Use account_id from trigger to get full account details

Step 2: Get Transactions (Tool)
  → Fetch recent transactions for context

Step 3: Your Business Logic
  → Process the data (e.g., sync to QuickBooks)
```

## Development & Testing

### Local Development

```bash
# Create virtual environment
cd mercury_tools_plugin
uv venv
source .venv/bin/activate  # or .venv/Scripts/activate on Windows

# Install dependencies
uv pip install -r requirements.txt

# Run with remote debugging
python main.py
```

### Remote Debugging

Configure `.env` file:
```
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=debug.dify.ai
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=your-debug-key
```

### Package Plugin

```bash
dify plugin package ./mercury_tools_plugin
```

## API Reference

See [Mercury API Documentation](https://docs.mercury.com) for full API details.

## Related Plugins

- **Mercury Trigger Plugin** (`mercury_plugin`): Receives real-time transaction events via webhooks

## License

Copyright (c) 2026

## Support

For issues or questions, please refer to the Dify plugin documentation.
