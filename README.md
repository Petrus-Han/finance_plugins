# Finance Plugins for Dify

Dify plugins for integrating Mercury Banking, QuickBooks accounting, and employee roster management.

## Project Status

| Plugin | Type | Status | Tests |
|--------|------|--------|-------|
| mercury_trigger_plugin | Trigger | Ready | 29/29 |
| mercury_tools_plugin | Tools | Ready | 12/12 |
| quickbooks_plugin | Tools | Ready | 6/6 |
| employee_roster_plugin | Tools | Ready | - |

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
├── employee_roster_plugin/     # Employee roster with Google Sheets
│   ├── provider/               # OAuth2 / Service Account auth
│   └── tools/                  # query, import CSV, dept mapping
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
uv run pytest */tests/ -v

# Mercury trigger tests
uv run pytest mercury_trigger_plugin/tests/ -v

# Mercury tools tests
uv run pytest mercury_tools_plugin/tests/ -v

# QuickBooks tools tests
uv run pytest quickbooks_plugin/tests/ -v
```

### 3. Package & Install to Dify

```bash
# Package a plugin
dify plugin package employee_roster_plugin

# Install to Dify instance
uv run python scripts/install_plugin.py employee_roster_plugin.difypkg
```

See [Development](#development) section below for full setup details.

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

## Employee Roster Plugin

Manages employee roster with finance department mappings using Google Sheets as backend. Replaces manual cross-referencing of Feishu and Deel exports.

**Auth**: OAuth2 (interactive) or Service Account (automation)

| Tool | Description |
|------|-------------|
| query_roster | Search employees by name/email (fuzzy match), returns finance department |
| import_roster_csv | Bulk import from Feishu/Deel CSV with dedup and finance field preservation |
| get_department_mapping | View source department to finance department mappings |

**Key design**: Import never overwrites `finance_department` and `notes` — these are maintained manually by the finance team.

See [docs/EMPLOYEE_ROSTER_DESIGN.md](docs/EMPLOYEE_ROSTER_DESIGN.md) for detailed architecture and workflow.

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
- [uv](https://docs.astral.sh/uv/) — Python package manager
- [Dify CLI](https://github.com/langgenius/dify-plugin-daemon) (v0.5.3+) — plugin packaging & debug
- Access to Dify platform

### Install Dify CLI

```bash
# Download latest dify CLI (replace arch as needed: linux-amd64, linux-arm64, darwin-arm64)
gh release download --repo langgenius/dify-plugin-daemon --pattern "dify-plugin-linux-arm64" --dir /tmp/
chmod +x /tmp/dify-plugin-linux-arm64
sudo mv /tmp/dify-plugin-linux-arm64 /usr/local/bin/dify

# Verify
dify version   # v0.5.3
```

### Setup Plugin Environment

```bash
# Create virtual environment and install dependencies with uv
cd <plugin_dir>
uv venv
uv pip install -r pyproject.toml

# Or install all dev dependencies
uv pip install -r pyproject.toml --group dev
```

### Run Tests

```bash
# All tests
uv run pytest */tests/ -v

# Single plugin
uv run pytest mercury_trigger_plugin/tests/ -v
uv run pytest quickbooks_plugin/tests/ -v
```

### Package & Deploy

```bash
# Package a single plugin
dify plugin package <plugin_dir>
# e.g. dify plugin package employee_roster_plugin

# Package all plugins
python3 scripts/build_mode.py package

# Package all in release mode (removes [DEBUG] labels)
python3 scripts/build_mode.py package --release

# Remote install to Dify instance (requires .credential file)
uv run python scripts/install_plugin.py <plugin>.difypkg
# e.g. uv run python scripts/install_plugin.py employee_roster_plugin.difypkg
```

The `.credential` file format (not committed to git):

```json
{
  "host": "https://your-dify-instance.com",
  "email": "admin@example.com",
  "password": "your-password"
}
```

### Remote Debug

```bash
# Configure .env in plugin directory
cat > <plugin_dir>/.env << EOF
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=your-dify-instance.com
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=<your-debug-key>
PLUGIN_DEBUG=true
EOF

# Run plugin in remote debug mode
cd <plugin_dir>
dify plugin run .
```

### Testing Documentation

See `mercury_trigger_plugin/TESTING.md` for detailed testing instructions.

## License

MIT
