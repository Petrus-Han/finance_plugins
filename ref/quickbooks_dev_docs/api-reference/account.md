# Account

> QuickBooks Online API Reference: Account Entity

Accounts are what businesses use to track transactions. Accounts can track money coming in (income or revenue) and going out (expenses). They can also track the value of things (assets), like vehicles and equipment.

## Account Classifications

| Classification | Description |
|----------------|-------------|
| Asset | What the business owns |
| Liability | What the business owes |
| Equity | Owner's stake in the business |
| Income/Revenue | Money earned |
| Expense | Money spent |

## The Account Object

### Sample Response

```json
{
  "Account": {
    "Id": "94",
    "Name": "MyJobs",
    "FullyQualifiedName": "MyJobs",
    "Classification": "Asset",
    "AccountType": "Accounts Receivable",
    "AccountSubType": "AccountsReceivable",
    "CurrentBalance": 0,
    "CurrentBalanceWithSubAccounts": 0,
    "Active": true,
    "SubAccount": false,
    "SyncToken": "0",
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "MetaData": {
      "CreateTime": "2014-12-31T09:29:05-08:00",
      "LastUpdatedTime": "2014-12-31T09:29:05-08:00"
    },
    "domain": "QBO",
    "sparse": false
  },
  "time": "2014-12-31T09:29:05.717-08:00"
}
```

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `Id` | String | Read-only | Unique identifier for this object |
| `Name` | String | **Required** | User recognizable name (max 100 chars). Cannot contain `"` or `:` |
| `SyncToken` | String | Required for update | Version number for optimistic locking |
| `AcctNum` | String | Conditional | User-defined account number. Max: US/UK/IN=7, AU/CA=20 chars |
| `AccountType` | AccountTypeEnum | Conditional | Account type based on Classification. Required if AccountSubType not specified |
| `AccountSubType` | String | Conditional | Sub-type classification. Required if AccountType not specified |
| `Classification` | String | Read-only | Asset, Equity, Expense, Liability, Revenue |
| `Active` | Boolean | Optional | Whether account is active (default: true) |
| `Description` | String | Optional | User description (max 100 chars) |
| `CurrentBalance` | Decimal | Read-only | Current balance for Balance Sheet accounts |
| `CurrentBalanceWithSubAccounts` | Decimal | Read-only | Cumulative balance including sub-accounts |
| `FullyQualifiedName` | String | Read-only | Full path: `Parent:Account1:SubAccount1` |
| `SubAccount` | Boolean | Read-only | True if this is a sub-account |
| `ParentRef` | ReferenceType | Optional | Parent account ID if sub-account |
| `CurrencyRef` | CurrencyRef | Read-only | Currency for multi-currency companies |
| `TaxCodeRef` | ReferenceType | Optional | Default tax code (minorVersion: 3) |
| `MetaData` | Object | Read-only | CreateTime and LastUpdatedTime |

### AccountType Values

| Classification | AccountType Values |
|----------------|-------------------|
| Asset | Bank, Other Current Asset, Fixed Asset, Other Asset, Accounts Receivable |
| Liability | Accounts Payable, Credit Card, Other Current Liability, Long Term Liability |
| Equity | Equity |
| Income | Income, Other Income |
| Expense | Expense, Other Expense, Cost of Goods Sold |

---

## Operations

### Create an Account

**Endpoint**: `POST /v3/company/{realmId}/account`

**Required Fields**:
- `Name` - Account name
- `AccountType` OR `AccountSubType` - At least one required

#### Request

```json
{
  "Name": "MyJobs_test",
  "AccountType": "Accounts Receivable"
}
```

#### Response

```json
{
  "Account": {
    "Id": "94",
    "Name": "MyJobs_test",
    "FullyQualifiedName": "MyJobs_test",
    "Classification": "Asset",
    "AccountType": "Accounts Receivable",
    "AccountSubType": "AccountsReceivable",
    "CurrentBalance": 0,
    "CurrentBalanceWithSubAccounts": 0,
    "Active": true,
    "SubAccount": false,
    "SyncToken": "0",
    "CurrencyRef": {
      "name": "United States Dollar",
      "value": "USD"
    },
    "MetaData": {
      "CreateTime": "2014-12-31T09:29:05-08:00",
      "LastUpdatedTime": "2014-12-31T09:29:05-08:00"
    }
  },
  "time": "2014-12-31T09:29:05.717-08:00"
}
```

---

### Query Accounts

**Endpoint**: `GET /v3/company/{realmId}/query?query={selectStatement}`

**Content-Type**: `text/plain`

#### Example Query

```sql
SELECT * FROM Account WHERE Metadata.CreateTime > '2014-12-31'
```

#### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "maxResults": 3,
    "Account": [
      {
        "Id": "92",
        "Name": "Canadian Accounts Receivable",
        "FullyQualifiedName": "Canadian Accounts Receivable",
        "Classification": "Asset",
        "AccountType": "Accounts Receivable",
        "AccountSubType": "AccountsReceivable",
        "CurrentBalance": 0,
        "Active": true,
        "SyncToken": "0"
      }
    ]
  },
  "time": "2015-07-13T12:35:57.651-07:00"
}
```

#### Useful Queries

```sql
-- All active accounts
SELECT * FROM Account WHERE Active = true

-- Bank accounts only
SELECT * FROM Account WHERE AccountType = 'Bank'

-- Expense accounts
SELECT * FROM Account WHERE Classification = 'Expense'

-- Search by name
SELECT * FROM Account WHERE Name LIKE '%Checking%'
```

---

### Read an Account

**Endpoint**: `GET /v3/company/{realmId}/account/{accountId}`

#### Response

```json
{
  "Account": {
    "Id": "33",
    "Name": "Accounts Payable (A/P)",
    "FullyQualifiedName": "Accounts Payable (A/P)",
    "Classification": "Liability",
    "AccountType": "Accounts Payable",
    "AccountSubType": "AccountsPayable",
    "CurrentBalance": -1091.23,
    "CurrentBalanceWithSubAccounts": -1091.23,
    "Active": true,
    "SubAccount": false,
    "SyncToken": "0",
    "MetaData": {
      "CreateTime": "2014-09-12T10:12:02-07:00",
      "LastUpdatedTime": "2015-06-30T15:09:07-07:00"
    }
  },
  "time": "2015-07-13T12:50:36.72-07:00"
}
```

---

### Update an Account (Full Update)

**Endpoint**: `POST /v3/company/{realmId}/account`

**Required**: Include `Id` and `SyncToken` from read response.

#### Request

```json
{
  "Id": "33",
  "SyncToken": "0",
  "Name": "Accounts Payable (A/P)",
  "Description": "Description added during update.",
  "AccountType": "Accounts Payable",
  "AccountSubType": "AccountsPayable",
  "Classification": "Liability",
  "CurrentBalance": -1091.23,
  "Active": true,
  "SubAccount": false
}
```

#### Response

```json
{
  "Account": {
    "Id": "33",
    "Name": "Accounts Payable (A/P)",
    "Description": "Description added during update.",
    "SyncToken": "1",
    "MetaData": {
      "CreateTime": "2014-09-12T10:12:02-07:00",
      "LastUpdatedTime": "2015-07-13T15:35:13-07:00"
    }
  },
  "time": "2015-07-13T15:31:25.618-07:00"
}
```

---

### Delete an Account (Soft Delete)

To "delete" an account, set `Active` to `false`:

```json
{
  "Id": "33",
  "SyncToken": "1",
  "Active": false
}
```

**Note**: Accounts are not permanently deleted. They become inactive and hidden from most displays.

---

## Mercury Integration Notes

When syncing Mercury bank transactions to QuickBooks:

1. **Find or Create Bank Account**: Query for the Mercury checking account
   ```sql
   SELECT * FROM Account WHERE AccountType = 'Bank' AND Name LIKE '%Mercury%'
   ```

2. **Map Account Types**:
   - Mercury checking → QuickBooks Bank account
   - Mercury savings → QuickBooks Bank account
   - Mercury treasury → QuickBooks Other Current Asset

3. **Create if Not Exists**: If no matching account found, create one with appropriate `AccountType` and `AccountSubType`.
