# QuickBooks Online API Documentation

> **Source**: Compiled from developer.intuit.com and integration guides (2025-12-26)

## Overview

QuickBooks Online API provides programmatic access to accounting data including customers, vendors, invoices, bills, purchases, deposits, and financial reports.

## Authentication

### OAuth 2.0 Flow

QuickBooks uses OAuth 2.0 for secure authentication.

**Setup Steps**:
1. Register application at https://developer.intuit.com
2. Create QuickBooks Online app
3. Select "QuickBooks Online Accounting" scope
4. Obtain Client ID and Client Secret
5. Configure Redirect URI

**OAuth Endpoints**:
- Authorization URL: `https://appcenter.intuit.com/connect/oauth2`
- Token URL: `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer`
- Revoke URL: `https://developer.api.intuit.com/v2/oauth2/tokens/revoke`

**Required Scopes**:
- `com.intuit.quickbooks.accounting` - Full accounting API access

**Optional Security**:
- OpenID Connect for additional authentication layer

**Token Details**:
- Access tokens expire in 1 hour
- Refresh tokens valid for 100 days
- Must refresh before expiration

**Authentication Header**:
```
Authorization: Bearer <access_token>
```

---

## Base URL

```
https://quickbooks.api.intuit.com/v3/company/{realmId}
```

**Realm ID**: Company identifier returned during OAuth callback. Required for all API requests.

---

## Core Entities

### Account (Chart of Accounts)

#### Query Accounts
```
GET /v3/company/{realmId}/query?query=select * from Account
```

**Query Examples**:
```sql
-- Get all accounts
SELECT * FROM Account

-- Get specific account type
SELECT * FROM Account WHERE AccountType = 'Expense'

-- Search by name
SELECT * FROM Account WHERE Name LIKE '%Office%'
```

**Response Fields**:
- `Id` - Account ID (string)
- `Name` - Account name
- `AccountType` - Type (Asset, Liability, Expense, Revenue, Equity)
- `AccountSubType` - Sub-type classification
- `AcctNum` - Account number
- `CurrentBalance` - Current balance
- `Active` - Active status

**Common Account Types for Banking**:
- `Bank` - Bank accounts
- `CreditCard` - Credit card accounts
- `Expense` - Expense accounts
- `Cost of Goods Sold` - COGS accounts
- `Other Expense` - Other expense categories

---

### Vendor

#### Query Vendors
```
GET /v3/company/{realmId}/query?query=select * from Vendor
```

#### Search Vendor
```sql
SELECT * FROM Vendor WHERE DisplayName LIKE '%Staples%'
```

#### Create Vendor
```
POST /v3/company/{realmId}/vendor
```

**Request Body**:
```json
{
  "DisplayName": "Staples Inc",
  "PrimaryEmailAddr": {
    "Address": "[email protected]"
  },
  "PrimaryPhone": {
    "FreeFormNumber": "(555) 123-4567"
  },
  "WebAddr": {
    "URI": "http://www.staples.com"
  },
  "CompanyName": "Staples Inc"
}
```

**Response**:
- Returns created Vendor object with `Id`

---

### Purchase (Expense Transaction)

The **Purchase** entity represents money spent using a bank account or credit card.

#### Create Purchase
```
POST /v3/company/{realmId}/purchase
```

**Request Body**:
```json
{
  "AccountRef": {
    "value": "35",
    "name": "Checking Account"
  },
  "PaymentType": "CreditCard",
  "EntityRef": {
    "value": "42",
    "name": "Staples Inc",
    "type": "Vendor"
  },
  "TxnDate": "2025-12-19",
  "PrivateNote": "Office supplies - Q4",
  "Line": [
    {
      "Id": "1",
      "Amount": 150.00,
      "DetailType": "AccountBasedExpenseLineDetail",
      "Description": "Office supplies",
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {
          "value": "7",
          "name": "Office Expenses"
        },
        "BillableStatus": "NotBillable",
        "TaxCodeRef": {
          "value": "NON"
        }
      }
    }
  ]
}
```

**Key Fields**:
- `AccountRef` (required) - Bank/Credit Card account being debited
  - `value` - Account ID
  - `name` - Account name (optional, for reference)
- `PaymentType` (required) - Payment method
  - Values: `Cash`, `Check`, `CreditCard`
- `EntityRef` (optional) - Vendor reference
  - `value` - Vendor ID
  - `type` - Must be "Vendor"
- `TxnDate` (optional) - Transaction date (defaults to today)
- `DocNumber` (optional) - Reference number (can use "AUTO_GENERATE")
- `PrivateNote` (optional) - Internal memo
- `Line` (required) - Array of line items
  - `Amount` - Line amount
  - `DetailType` - Must be "AccountBasedExpenseLineDetail" or "ItemBasedExpenseLineDetail"
  - `Description` - Line description
  - `AccountBasedExpenseLineDetail.AccountRef` - Expense account

**Important Notes**:
- Use `AccountBasedExpenseLineDetail` for direct expense categorization
- Use `ItemBasedExpenseLineDetail` for inventory items
- Total amount calculated from line items
- For Mercury sync: Store Mercury transaction_id in `PrivateNote` for idempotency

**Example with Multiple Lines**:
```json
{
  "AccountRef": {"value": "35"},
  "PaymentType": "CreditCard",
  "EntityRef": {"value": "42", "type": "Vendor"},
  "TxnDate": "2025-12-19",
  "Line": [
    {
      "Amount": 100.00,
      "DetailType": "AccountBasedExpenseLineDetail",
      "Description": "Printer paper",
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {"value": "7"}
      }
    },
    {
      "Amount": 50.00,
      "DetailType": "AccountBasedExpenseLineDetail",
      "Description": "Pens and markers",
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {"value": "7"}
      }
    }
  ]
}
```

---

### Deposit (Income Transaction)

The **Deposit** entity represents money received into a bank account.

#### Create Deposit
```
POST /v3/company/{realmId}/deposit
```

**Request Body**:
```json
{
  "DepositToAccountRef": {
    "value": "35",
    "name": "Checking Account"
  },
  "TxnDate": "2025-12-19",
  "PrivateNote": "Client payment",
  "Line": [
    {
      "Amount": 1000.00,
      "DetailType": "DepositLineDetail",
      "Description": "Payment for services",
      "DepositLineDetail": {
        "AccountRef": {
          "value": "79",
          "name": "Sales Income"
        },
        "Entity": {
          "value": "15",
          "name": "ABC Company",
          "type": "Customer"
        }
      }
    }
  ]
}
```

**Key Fields**:
- `DepositToAccountRef` (required) - Bank account receiving the deposit
  - `value` - Account ID (must be Asset/Bank account)
- `TxnDate` (optional) - Deposit date (defaults to today)
- `DocNumber` (optional) - Reference number
- `PrivateNote` (optional) - Internal memo
- `Line` (required) - Array of deposit line items
  - `Amount` - Line amount
  - `DetailType` - Must be "DepositLineDetail"
  - `Description` - Line description
  - `DepositLineDetail.AccountRef` - Income account
  - `DepositLineDetail.Entity` - Customer reference (optional)

**Important Notes**:
- Use for undeposited funds or direct deposits
- Can link to customers via Entity
- Total amount calculated from line items
- For Mercury sync: Store Mercury transaction_id in `PrivateNote`

---

### Customer

#### Query Customers
```
GET /v3/company/{realmId}/query?query=select * from Customer
```

#### Search Customer
```sql
SELECT * FROM Customer WHERE DisplayName LIKE '%ABC%'
```

#### Create Customer
```
POST /v3/company/{realmId}/customer
```

**Request Body**:
```json
{
  "DisplayName": "ABC Company",
  "PrimaryEmailAddr": {
    "Address": "[email protected]"
  },
  "PrimaryPhone": {
    "FreeFormNumber": "(555) 987-6543"
  },
  "CompanyName": "ABC Company"
}
```

---

## API Patterns

### HTTP Methods

- `GET` - Read/retrieve data
- `POST` - Create new entities
- `POST` (with query parameter) - Update entities
  - Full Update: `POST /v3/company/{realmId}/entity?operation=update`
  - Sparse Update: Include `SyncToken` and only changed fields
- `POST` (delete operation) - Soft delete entities
  - `POST /v3/company/{realmId}/entity?operation=delete`

### Query Language

QuickBooks uses SQL-like query syntax:

```sql
-- Basic query
SELECT * FROM Entity

-- Filter
SELECT * FROM Entity WHERE Field = 'Value'

-- LIKE operator
SELECT * FROM Entity WHERE Name LIKE '%search%'

-- Multiple conditions
SELECT * FROM Entity WHERE Field1 = 'Value' AND Field2 > 100

-- Date filtering
SELECT * FROM Transaction WHERE TxnDate >= '2025-01-01'

-- Pagination
SELECT * FROM Entity STARTPOSITION 1 MAXRESULTS 100
```

**Query Endpoint**:
```
GET /v3/company/{realmId}/query?query={sql_query}
```

**Minorversion Parameter**: Add `?minorversion=65` for latest API features

---

## Rate Limits

**Official Limits** (as of 2025):
- QuickBooks imposes rate limits on API requests
- Specific limits not publicly disclosed
- 429 status code returned when exceeded

**Best Practices**:
- Implement exponential backoff
- Batch requests when possible
- Use async/background processing
- Cache frequently accessed data
- Monitor API usage

**Recommended Approach**:
- Token bucket algorithm for rate limiting
- Max 5-10 requests per second
- Implement queue for background syncing

---

## Error Handling

### Common HTTP Status Codes

- `200` - Success
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (invalid/expired token)
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict (duplicate entity)
- `429` - Too Many Requests
- `500` - Internal Server Error
- `503` - Service Unavailable

### Error Response Format

```json
{
  "Fault": {
    "Error": [
      {
        "Message": "Error message description",
        "Detail": "Detailed error information",
        "code": "error_code"
      }
    ],
    "type": "ValidationFault"
  }
}
```

**Error Types**:
- `ValidationFault` - Invalid data/parameters
- `AuthenticationFault` - Auth failure
- `AuthorizationFault` - Permission denied
- `SystemFault` - Server error

---

## Data Validation & Best Practices

### Idempotency

To prevent duplicate transactions:
1. Store Mercury `transaction_id` in QuickBooks `PrivateNote`
2. Before creating, query for existing record:
   ```sql
   SELECT * FROM Purchase WHERE PrivateNote LIKE '%txn_123abc%'
   ```
3. Skip if already exists

### Data Mapping Best Practices

1. **Vendor Matching**:
   - Search by DisplayName (fuzzy match)
   - Create vendor if not found
   - Cache vendor mappings

2. **Account Mapping**:
   - Pre-load chart of accounts
   - Use LLM for intelligent categorization
   - Provide manual override

3. **Date Handling**:
   - Use ISO 8601 format: `YYYY-MM-DD`
   - Respect QuickBooks fiscal period locks

4. **Amount Handling**:
   - QuickBooks uses positive amounts for both purchases and deposits
   - Direction determined by entity type (Purchase vs Deposit)

### Sandbox Environment

QuickBooks provides sandbox environments:
- Separate realm ID for testing
- Test data doesn't affect production
- Same API endpoints with sandbox credentials

**To use sandbox**:
1. Create sandbox company in Intuit Developer portal
2. Obtain sandbox realm ID
3. Use same API but with sandbox OAuth tokens

---

## Integration Example: Mercury to QuickBooks

### Mapping Mercury Debit to QuickBooks Purchase

```python
def create_purchase_from_mercury(mercury_txn, qb_client):
    """
    Convert Mercury transaction to QuickBooks Purchase
    """

    # 1. Check for duplicate
    existing = qb_client.query(
        f"SELECT * FROM Purchase WHERE PrivateNote LIKE '%{mercury_txn['id']}%'"
    )
    if existing:
        return {"status": "duplicate", "id": existing[0]['Id']}

    # 2. Find or create vendor
    vendor = find_or_create_vendor(
        qb_client,
        mercury_txn['counterpartyName']
    )

    # 3. Map to expense account (using LLM or rules)
    expense_account = map_to_account(
        mercury_txn['description'],
        mercury_txn.get('category', '')
    )

    # 4. Create Purchase
    purchase = {
        "AccountRef": {"value": "35"},  # Mercury bank account in QBO
        "PaymentType": "CreditCard",
        "EntityRef": {
            "value": vendor['Id'],
            "type": "Vendor"
        },
        "TxnDate": mercury_txn['date'],
        "PrivateNote": f"Mercury: {mercury_txn['id']} - {mercury_txn['description']}",
        "Line": [{
            "Amount": abs(mercury_txn['amount']),  # Remove negative sign
            "DetailType": "AccountBasedExpenseLineDetail",
            "Description": mercury_txn['description'],
            "AccountBasedExpenseLineDetail": {
                "AccountRef": {"value": expense_account['Id']}
            }
        }]
    }

    response = qb_client.post(f"/v3/company/{realm_id}/purchase", purchase)
    return {"status": "created", "id": response['Purchase']['Id']}
```

---

## Additional Resources

- **Official Documentation**: https://developer.intuit.com/app/developer/qbo/docs/api
- **API Reference**: https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities
- **OAuth Guide**: https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization
- **Developer Portal**: https://developer.intuit.com
- **Postman Collection**: https://documenter.getpostman.com/view/3967924/RW1dEx9d
- **Support**: https://help.developer.intuit.com

---

## Notes for Dify Plugin Development

### For QuickBooks Tool Plugin:

1. **Tools to Implement**:
   - `get_accounts` - Query chart of accounts
   - `get_vendors` - Query vendors
   - `search_vendor` - Search vendor by name
   - `create_vendor` - Create new vendor
   - `search_entity` - Generic search (vendors/customers)
   - `create_purchase` - Create purchase/expense
   - `create_deposit` - Create deposit
   - `query` - Generic query tool

2. **OAuth Configuration**:
   - Configure in `provider/quickbooks.yaml`
   - Dify v1.7.0+ handles token refresh
   - Store realm_id as credential or variable

3. **Error Handling**:
   - Check for 409 (duplicate) - skip gracefully
   - Retry on 429 with backoff
   - Refresh token on 401
   - Validate data before sending

4. **Best Practices**:
   - Always include realm_id in URLs
   - Cache chart of accounts
   - Implement idempotency checks
   - Log all API calls for audit

---

*Last Updated: 2025-12-26*
*Note: Based on QuickBooks Online API v3. Check official documentation for latest updates.*
