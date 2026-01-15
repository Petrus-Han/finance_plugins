---
name: quickbooks-integration
description: Integrate with QuickBooks Online API for creating purchases, deposits, vendors, and querying accounting data. Use when working with QuickBooks entities, OAuth authentication, or financial data synchronization.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# QuickBooks Integration

## Overview

Specialized Skill for QuickBooks Online API integration, focusing on creating financial transactions and managing accounting entities.

## When Claude Uses This Skill

- Creating QuickBooks tool plugins
- Implementing Purchase/Deposit entities
- Setting up QuickBooks OAuth 2.0
- Querying chart of accounts or vendors
- Mapping Mercury transactions to QuickBooks

## QuickBooks API Essentials

### Base URL Pattern

```
https://quickbooks.api.intuit.com/v3/company/{realmId}/{entity}
```

**Critical**: `realmId` is required for all requests. Obtained during OAuth callback.

### Authentication

```python
headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
```

Token refresh handled by Dify OAuth system automatically.

### Common Entities

**Purchase** (Expense):
```json
{
  "AccountRef": {"value": "35"},  # Bank account
  "PaymentType": "CreditCard",
  "EntityRef": {"value": "42", "type": "Vendor"},
  "TxnDate": "2025-12-26",
  "Line": [{
    "Amount": 150.00,
    "DetailType": "AccountBasedExpenseLineDetail",
    "AccountBasedExpenseLineDetail": {
      "AccountRef": {"value": "7"}  # Expense account
    }
  }]
}
```

**Deposit** (Income):
```json
{
  "DepositToAccountRef": {"value": "35"},
  "TxnDate": "2025-12-26",
  "Line": [{
    "Amount": 1000.00,
    "DetailType": "DepositLineDetail",
    "DepositLineDetail": {
      "AccountRef": {"value": "79"},  # Income account
      "Entity": {"value": "15", "type": "Customer"}
    }
  }]
}
```

### Query Language (SQL-like)

```sql
-- Get all vendors
SELECT * FROM Vendor

-- Search vendor
SELECT * FROM Vendor WHERE DisplayName LIKE '%Staples%'

-- Filter by date
SELECT * FROM Purchase WHERE TxnDate >= '2025-01-01'

-- Pagination
SELECT * FROM Entity STARTPOSITION 1 MAXRESULTS 100
```

## Tool Plugin Structure

```
quickbooks-plugin/
├── provider/
│   ├── quickbooks.yaml       # OAuth config
│   └── quickbooks.py         # Credential validation
├── tools/
│   ├── get_accounts/
│   ├── get_vendors/
│   ├── create_purchase/
│   ├── create_deposit/
│   └── query/               # Generic query tool
└── manifest.yaml
```

## OAuth Configuration

**In provider/quickbooks.yaml**:

```yaml
identity:
  name: quickbooks
  label:
    en_US: QuickBooks Online

credentials_schema:
  - name: auth_type
    type: select
    options:
      - value: oauth
        label:
          en_US: OAuth 2.0

oauth:
  authorization_url: https://appcenter.intuit.com/connect/oauth2
  token_url: https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer
  scopes:
    - com.intuit.quickbooks.accounting
```

## Implementation Patterns

### 1. Idempotency Check (Critical for Financial Data!)

```python
def create_purchase(self, mercury_txn_id: str, ...):
    # Check if already exists
    query = f"SELECT * FROM Purchase WHERE PrivateNote LIKE '%{mercury_txn_id}%'"
    existing = self._query(query)

    if existing:
        return {"status": "duplicate", "id": existing[0]["Id"]}

    # Create new purchase
    # ... store mercury_txn_id in PrivateNote
```

### 2. Find or Create Vendor

```python
def find_or_create_vendor(self, vendor_name: str):
    # Search existing
    query = f"SELECT * FROM Vendor WHERE DisplayName LIKE '%{vendor_name}%'"
    vendors = self._query(query)

    if vendors:
        return vendors[0]

    # Create new
    response = requests.post(
        f"{BASE_URL}/{realm_id}/vendor",
        json={"DisplayName": vendor_name},
        headers=headers
    )
    return response.json()["Vendor"]
```

### 3. Error Handling

```python
# Common errors
- 400: Invalid data (check required fields)
- 401: Token expired (refresh automatically)
- 409: Duplicate entity
- 429: Rate limit (retry with backoff)
- 500: Server error (retry)

# Handle gracefully
try:
    response = requests.post(...)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 409:
        return {"status": "duplicate"}
    elif e.response.status_code == 429:
        time.sleep(2)  # Rate limit backoff
        # Retry...
    else:
        raise ToolProviderCredentialValidationError(str(e))
```

## Mercury → QuickBooks Mapping

### Debit Transaction (Expense) → Purchase

```python
def map_debit_to_purchase(mercury_txn):
    return {
        "AccountRef": {"value": get_mercury_bank_account_id()},
        "PaymentType": "CreditCard",
        "EntityRef": {
            "value": find_or_create_vendor(mercury_txn["merchant"]),
            "type": "Vendor"
        },
        "TxnDate": mercury_txn["date"],
        "PrivateNote": f"Mercury: {mercury_txn['transaction_id']} - {mercury_txn['description']}",
        "Line": [{
            "Amount": abs(mercury_txn["amount"]),
            "DetailType": "AccountBasedExpenseLineDetail",
            "Description": mercury_txn["description"],
            "AccountBasedExpenseLineDetail": {
                "AccountRef": {"value": map_to_expense_account(mercury_txn)}
            }
        }]
    }
```

### Credit Transaction (Income) → Deposit

```python
def map_credit_to_deposit(mercury_txn):
    return {
        "DepositToAccountRef": {"value": get_mercury_bank_account_id()},
        "TxnDate": mercury_txn["date"],
        "PrivateNote": f"Mercury: {mercury_txn['transaction_id']}",
        "Line": [{
            "Amount": mercury_txn["amount"],
            "DetailType": "DepositLineDetail",
            "DepositLineDetail": {
                "AccountRef": {"value": get_income_account_id()},
                # Optionally link to customer
            }
        }]
    }
```

## Testing

### Sandbox Environment

1. Create sandbox company at developer.intuit.com
2. Get sandbox realm_id
3. Use sandbox OAuth credentials
4. Test all entity creations
5. Verify data in sandbox QuickBooks

### Common Test Cases

```python
# Test 1: Create vendor
vendor = create_vendor("Test Vendor")
assert vendor["Id"] is not None

# Test 2: Create purchase
purchase = create_purchase({
    "transaction_id": "test_txn_123",
    "amount": -100.00,
    "merchant": "Test Vendor",
    "date": "2025-12-26"
})
assert purchase["status"] == "created"

# Test 3: Duplicate prevention
duplicate = create_purchase({...})  # Same txn_id
assert duplicate["status"] == "duplicate"

# Test 4: Query
results = query("SELECT * FROM Vendor WHERE DisplayName = 'Test Vendor'")
assert len(results) > 0
```

## Reference Documents

- `QuickBooks_API_Documentation.md` - Complete API reference
- `solution-design.md` - Architecture and design decisions
- `开发计划.md` - Implementation plan

## Best Practices

1. **Always check for duplicates** - Use PrivateNote to store Mercury transaction ID
2. **Cache chart of accounts** - Load once, reuse for mappings
3. **Handle rate limits** - Implement exponential backoff
4. **Use realm_id correctly** - Required in all API URLs
5. **Test in sandbox first** - Never test with production data
6. **Log all API calls** - For audit and debugging
7. **Validate data before sending** - Check required fields
8. **Use minorversion parameter** - `?minorversion=65` for latest features

## Rate Limit Strategy

```python
import time

MAX_REQUESTS_PER_SECOND = 5
request_times = []

def rate_limit():
    now = time.time()
    # Remove requests older than 1 second
    request_times[:] = [t for t in request_times if now - t < 1]

    if len(request_times) >= MAX_REQUESTS_PER_SECOND:
        sleep_time = 1 - (now - request_times[0])
        if sleep_time > 0:
            time.sleep(sleep_time)

    request_times.append(time.time())
```

## Quick Reference

**Entity Endpoints**:
- Vendor: `/v3/company/{realmId}/vendor`
- Purchase: `/v3/company/{realmId}/purchase`
- Deposit: `/v3/company/{realmId}/deposit`
- Account: `/v3/company/{realmId}/account`
- Query: `/v3/company/{realmId}/query?query={sql}`

**OAuth Scopes**:
- `com.intuit.quickbooks.accounting` - Full accounting access

**Required Fields**:
- Purchase: `AccountRef`, `PaymentType`, `Line[]`
- Deposit: `DepositToAccountRef`, `Line[]`
- Vendor: `DisplayName`
