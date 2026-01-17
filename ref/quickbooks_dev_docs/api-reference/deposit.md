# Deposit

> QuickBooks Online API Reference: Deposit Entity

A Deposit object is a transaction that records one or more deposits into a bank account.

## Deposit Types

| Type | Description | How to Create |
|------|-------------|---------------|
| **Direct Deposit** | New deposit directly recorded | Use `Line.DepositLineDetail.AccountRef` |
| **Linked Deposit** | Deposit from existing transaction (Payment, SalesReceipt, etc.) | Use `Line.LinkedTxn` |

## Business Rules

- Must include at least one line item
- Any transaction that funds Undeposited Funds can be linked
- Linkable transactions: Transfer, Payment, SalesReceipt, RefundReceipt, JournalEntry

## The Deposit Object

### Sample Response

```json
{
  "Deposit": {
    "Id": "123",
    "SyncToken": "0",
    "DepositToAccountRef": {
      "value": "35",
      "name": "Checking"
    },
    "TxnDate": "2024-01-15",
    "TotalAmt": 1500.00,
    "Line": [
      {
        "Id": "1",
        "LineNum": 1,
        "Amount": 1000.00,
        "DetailType": "DepositLineDetail",
        "DepositLineDetail": {
          "AccountRef": {
            "value": "79",
            "name": "Sales"
          },
          "Entity": {
            "value": "58",
            "name": "ABC Customer",
            "type": "Customer"
          }
        }
      },
      {
        "Id": "2",
        "LineNum": 2,
        "Amount": 500.00,
        "DetailType": "DepositLineDetail",
        "DepositLineDetail": {
          "AccountRef": {
            "value": "45",
            "name": "Interest Income"
          }
        }
      }
    ],
    "PrivateNote": "January deposits",
    "MetaData": {
      "CreateTime": "2024-01-15T10:00:00-08:00",
      "LastUpdatedTime": "2024-01-15T10:00:00-08:00"
    }
  },
  "time": "2024-01-15T10:00:00.000-08:00"
}
```

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| `Id` | String | Read-only | Unique identifier |
| `SyncToken` | String | Required for update | Version number for optimistic locking |
| `DepositToAccountRef` | ReferenceType | **Required** | Bank account to deposit into (AccountType: Bank or Other Current Asset) |
| `Line` | Line[] | **Required** | Individual deposit line items |
| `TxnDate` | Date | Optional | Transaction date (defaults to server date) |
| `PrivateNote` | String | Optional | Memo (max 4000 chars) |
| `TotalAmt` | Decimal | Read-only | Total amount (calculated by QuickBooks) |
| `CurrencyRef` | CurrencyRefType | Conditional | Required if multicurrency enabled |
| `ExchangeRate` | Decimal | Optional | Currency exchange rate |
| `DepartmentRef` | ReferenceType | Optional | Department/location reference |
| `CashBack` | CashBackInfo | Optional | Cash back information |
| `TxnTaxDetail` | TxnTaxDetail | Optional | Tax details |
| `GlobalTaxCalculation` | Enum | Conditional | Required for non-US companies |
| `MetaData` | Object | Read-only | CreateTime and LastUpdatedTime |
| `HomeTotalAmt` | Decimal | Read-only | Amount in home currency (multicurrency) |

### Line Types

#### DepositLineDetail (Direct Deposit)

For recording new income/deposits:

```json
{
  "Id": "1",
  "LineNum": 1,
  "Amount": 1000.00,
  "DetailType": "DepositLineDetail",
  "DepositLineDetail": {
    "AccountRef": {
      "value": "79",
      "name": "Sales"
    },
    "Entity": {
      "value": "58",
      "name": "ABC Customer",
      "type": "Customer"
    },
    "PaymentMethodRef": {
      "value": "1",
      "name": "Cash"
    },
    "CheckNum": "1234",
    "TxnType": "CashSale"
  }
}
```

| Field | Description |
|-------|-------------|
| `AccountRef` | Income account to credit |
| `Entity` | Customer or Vendor reference |
| `PaymentMethodRef` | Payment method (Cash, Check, etc.) |
| `CheckNum` | Check number if applicable |
| `TxnType` | Transaction type (CashSale, etc.) |

#### LinkedTxn (Linked Deposit)

For depositing from Undeposited Funds:

```json
{
  "LineNum": 1,
  "Amount": 500.00,
  "LinkedTxn": [
    {
      "TxnId": "42",
      "TxnType": "Payment"
    }
  ]
}
```

---

## Operations

### Create a Deposit

**Endpoint**: `POST /v3/company/{realmId}/deposit`

**Required Fields**:
- `DepositToAccountRef` - Bank account
- `Line` - At least one deposit line

#### Request: Direct Deposit (Income)

```json
{
  "DepositToAccountRef": {
    "value": "35",
    "name": "Checking"
  },
  "TxnDate": "2024-01-15",
  "Line": [
    {
      "Amount": 1500.00,
      "DetailType": "DepositLineDetail",
      "DepositLineDetail": {
        "AccountRef": {
          "value": "79",
          "name": "Sales of Product Income"
        },
        "Entity": {
          "value": "58",
          "name": "ABC Customer",
          "type": "Customer"
        }
      }
    }
  ],
  "PrivateNote": "Payment from ABC Customer"
}
```

#### Request: Multiple Income Sources

```json
{
  "DepositToAccountRef": {
    "value": "35",
    "name": "Checking"
  },
  "TxnDate": "2024-01-15",
  "Line": [
    {
      "Amount": 1000.00,
      "DetailType": "DepositLineDetail",
      "DepositLineDetail": {
        "AccountRef": {
          "value": "79",
          "name": "Sales"
        }
      }
    },
    {
      "Amount": 50.00,
      "DetailType": "DepositLineDetail",
      "DepositLineDetail": {
        "AccountRef": {
          "value": "45",
          "name": "Interest Income"
        }
      }
    },
    {
      "Amount": 200.00,
      "DetailType": "DepositLineDetail",
      "DepositLineDetail": {
        "AccountRef": {
          "value": "46",
          "name": "Other Income"
        }
      }
    }
  ]
}
```

#### Request: Linked Deposit (from Payment)

```json
{
  "DepositToAccountRef": {
    "value": "35",
    "name": "Checking"
  },
  "TxnDate": "2024-01-15",
  "Line": [
    {
      "Amount": 500.00,
      "LinkedTxn": [
        {
          "TxnId": "42",
          "TxnType": "Payment"
        }
      ]
    }
  ]
}
```

---

### Query Deposits

**Endpoint**: `GET /v3/company/{realmId}/query?query={selectStatement}`

#### Example Queries

```sql
-- All deposits
SELECT * FROM Deposit

-- Deposits by date range
SELECT * FROM Deposit WHERE TxnDate >= '2024-01-01' AND TxnDate <= '2024-01-31'

-- Deposits by amount
SELECT * FROM Deposit WHERE TotalAmt > 1000 ORDERBY TotalAmt DESC

-- Recent deposits with pagination
SELECT * FROM Deposit ORDERBY TxnDate DESC STARTPOSITION 1 MAXRESULTS 50
```

---

### Read a Deposit

**Endpoint**: `GET /v3/company/{realmId}/deposit/{depositId}`

---

### Update a Deposit (Full Update)

**Endpoint**: `POST /v3/company/{realmId}/deposit`

**Required**: Include `Id` and `SyncToken` from read response, plus all writable fields.

```json
{
  "Id": "123",
  "SyncToken": "0",
  "DepositToAccountRef": {
    "value": "35",
    "name": "Checking"
  },
  "TxnDate": "2024-01-15",
  "Line": [
    {
      "Id": "1",
      "Amount": 1600.00,
      "DetailType": "DepositLineDetail",
      "DepositLineDetail": {
        "AccountRef": {
          "value": "79",
          "name": "Sales"
        }
      }
    }
  ],
  "PrivateNote": "Updated deposit"
}
```

---

### Sparse Update a Deposit

**Endpoint**: `POST /v3/company/{realmId}/deposit`

Include `sparse: true` to update only specified fields:

```json
{
  "Id": "123",
  "SyncToken": "0",
  "sparse": true,
  "PrivateNote": "Updated memo only"
}
```

---

### Delete a Deposit

**Endpoint**: `POST /v3/company/{realmId}/deposit?operation=delete`

```json
{
  "Id": "123",
  "SyncToken": "1"
}
```

---

## Mercury Integration Notes

When syncing Mercury bank transactions (incoming/income) to QuickBooks:

### Mapping Mercury Transactions to Deposit

| Mercury Field | QuickBooks Field |
|---------------|------------------|
| Transaction ID | `PrivateNote` (include for tracking) |
| Amount | `Line[0].Amount` |
| Date | `TxnDate` |
| Counterparty | `Line[0].DepositLineDetail.Entity` |
| Description | `PrivateNote` |
| Bank Account | `DepositToAccountRef` (Mercury checking account) |

### Income Account Selection

For Mercury incoming transactions, determine the appropriate income account:

| Mercury Category/Type | QuickBooks Income Account |
|-----------------------|---------------------------|
| Customer payment | Sales of Product Income |
| Interest | Interest Income |
| Refund | Other Income (or original expense account) |
| Transfer | Transfer (not Deposit) |

### Example: Create Deposit from Mercury Transaction

```python
def create_deposit_from_mercury(mercury_txn, qb_client):
    # Get Mercury checking account in QuickBooks
    mercury_account = get_mercury_account()
    
    # Find or create customer (if from customer)
    customer = None
    if mercury_txn.counterparty:
        customer = find_or_create_customer(mercury_txn.counterparty)
    
    # Determine income account based on transaction type
    income_account = get_income_account(mercury_txn.category)
    
    line_detail = {
        "AccountRef": {
            "value": income_account.id,
            "name": income_account.name
        }
    }
    
    # Add customer reference if available
    if customer:
        line_detail["Entity"] = {
            "value": customer.id,
            "name": customer.display_name,
            "type": "Customer"
        }
    
    deposit = {
        "DepositToAccountRef": {
            "value": mercury_account.id,
            "name": mercury_account.name
        },
        "TxnDate": mercury_txn.posted_at.strftime("%Y-%m-%d"),
        "Line": [
            {
                "Amount": abs(mercury_txn.amount),
                "DetailType": "DepositLineDetail",
                "DepositLineDetail": line_detail
            }
        ],
        "PrivateNote": f"Mercury Transaction ID: {mercury_txn.id}\n{mercury_txn.description}"
    }
    
    return qb_client.create_deposit(deposit)
```

### Handling Different Income Types

```python
def get_income_account(mercury_category):
    """Map Mercury category to QuickBooks income account."""
    category_map = {
        "sales": "Sales of Product Income",
        "services": "Services",
        "interest": "Interest Earned",
        "refund": "Other Income",
        "other": "Other Income"
    }
    
    account_name = category_map.get(mercury_category, "Other Income")
    return query_account_by_name(account_name)
```

### When to Use Deposit vs Other Entities

| Scenario | QuickBooks Entity |
|----------|-------------------|
| General income receipt | **Deposit** |
| Customer payment on invoice | Payment → Deposit |
| Refund from vendor | **Deposit** (or VendorCredit) |
| Internal transfer | **Transfer** (not Deposit) |
| Sales receipt | SalesReceipt → Deposit |
