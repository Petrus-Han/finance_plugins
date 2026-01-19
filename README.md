# Finance Plugins for Dify

Dify plugins for integrating Mercury Banking and QuickBooks accounting services.

## Project Status

| Plugin | Type | Status | Tests |
|--------|------|--------|-------|
| mercury_trigger_plugin | Trigger | Ready | 29/29 |
| mercury_tools_plugin | Tools | Ready | 12/12 |
| quickbooks_plugin | Tools | Ready | 6/6 |

## Project Structure

```
finance_plugins/
├── mercury_trigger_plugin/     # Mercury webhook trigger
│   ├── provider/               # Trigger provider implementation
│   ├── events/                 # Event handlers (transaction)
│   ├── tests/                  # Unit & integration tests
│   └── TESTING.md              # Testing guide
├── mercury_tools_plugin/       # Mercury API tools
│   ├── tools/                  # Tool implementations
│   │   ├── get_accounts.py
│   │   ├── get_account.py
│   │   ├── get_transactions.py
│   │   ├── get_transaction.py
│   │   ├── get_recipients.py
│   │   ├── get_recipient.py
│   │   ├── create_recipient.py
│   │   └── update_transaction.py
│   └── tests/                  # Unit tests
├── quickbooks_plugin/          # QuickBooks API tools
│   ├── tools/                  # Tool implementations
│   │   ├── get_chart_of_accounts.py
│   │   ├── vendor_management.py
│   │   ├── customer_management.py
│   │   ├── create_purchase.py
│   │   ├── create_deposit.py
│   │   └── create_transfer.py
│   └── tests/                  # Unit tests
├── scripts/                    # Development scripts
│   └── mock_mercury_server.py  # Mock Mercury API server
└── docs/                       # Documentation
```

## Quick Start

### 1. Start Mock Mercury Server

```bash
python3 scripts/mock_mercury_server.py
# Server runs on http://localhost:8765
# API Token: mock_token_12345
```

### 2. Run Tests

```bash
# All tests
.venv/bin/pytest */tests/ -v

# Mercury trigger tests
.venv/bin/pytest mercury_trigger_plugin/tests/ -v

# Mercury tools tests
.venv/bin/pytest mercury_tools_plugin/tests/ -v

# QuickBooks tools tests
.venv/bin/pytest quickbooks_plugin/tests/ -v
```

### 3. Remote Debug with Dify

```bash
# Configure .env in plugin directory
cat > mercury_trigger_plugin/.env << EOF
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=dify.greeep.com
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=<your-key>
PLUGIN_DEBUG=true
EOF

# Run plugin
cd mercury_trigger_plugin
dify plugin run .
```

## Mercury Trigger Plugin

Listens for Mercury banking webhooks and triggers Dify workflows.

**Features:**
- Webhook signature validation (HMAC-SHA256)
- Transaction event handling (created/updated)
- Operation filtering
- Automatic webhook subscription management

**Credentials:**
- `access_token`: Mercury API access token
- `api_environment`: `sandbox` or `production`

**Events:**
- `transaction`: Triggered on transaction.created or transaction.updated

**Output Variables:**
| Variable | Description |
|----------|-------------|
| event_id | Mercury event ID |
| transaction_id | Transaction ID |
| operation_type | created/updated |
| account_id | Account ID |
| amount | Transaction amount |
| status | Transaction status |
| counterparty_name | Counterparty name |

## Mercury Tools Plugin

Tools for interacting with Mercury Banking API.

| Tool | Description |
|------|-------------|
| get_accounts | List all Mercury accounts |
| get_account | Get single account details |
| get_transactions | List account transactions |
| get_transaction | Get transaction details |
| get_recipients | List payment recipients |
| get_recipient | Get recipient details |
| create_recipient | Create new recipient |
| update_transaction | Update transaction notes/category |

## QuickBooks Plugin

Tools for interacting with QuickBooks Online API.

| Tool | Description |
|------|-------------|
| get_chart_of_accounts | List chart of accounts |
| vendor_management | List/search/create vendors |
| customer_management | List/search/create customers |
| create_purchase | Create purchase transaction |
| create_deposit | Create bank deposit |
| create_transfer | Transfer between accounts |

## Mock Mercury Server

Full-featured mock server for local development and testing.

**Endpoints:**
- Mercury API: `/api/v1/accounts`, `/api/v1/webhooks`, etc.
- Simulation: `/simulate/transaction`, `/simulate/transaction/update`
- Utility: `/webhooks/list`, `/webhooks/clear`

**Usage:**
```bash
# List accounts
curl -H "Authorization: Bearer mock_token_12345" \
  http://localhost:8765/api/v1/accounts

# Create webhook
curl -X POST http://localhost:8765/api/v1/webhooks \
  -H "Authorization: Bearer mock_token_12345" \
  -H "Content-Type: application/json" \
  -d '{"url": "http://callback/webhook", "eventTypes": ["transaction.created"]}'

# Simulate event
curl -X POST http://localhost:8765/simulate/transaction \
  -d '{"amount": -500, "counterparty": "Test"}'
```

## Development

### Prerequisites

- Python 3.12+
- Dify CLI
- Access to Dify platform

### Virtual Environment

```bash
# Activate
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Testing Documentation

See `mercury_trigger_plugin/TESTING.md` for detailed testing instructions.

## License

MIT
