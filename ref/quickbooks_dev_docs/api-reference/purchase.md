# Purchase

> QuickBooks Online API Reference: Purchase Entity

A Purchase object represents an expense, such as a purchase made from a vendor.

## Key Points

- **You must specify an AccountRef** for all purchases
- **TotalAmt must equal** the sum of all `Line.Amount` values
- **Three payment types**: Cash, Check, and CreditCard

| PaymentType | Description | AccountRef Type |
|-------------|-------------|-----------------|
| `Cash` | Payment made in cash | Bank account |
| `Check` | Payment made by check | Bank account |
| `CreditCard` | Credit card charge or refund | Credit card account |

## The Purchase Object

### Sample Response

```json
{
  "Purchase": {
    "Id": "123",
    "SyncToken": "0",
    "PaymentType": "Check",
    "AccountRef": {
      "value": "35",
      "name": "Checking"
    },
    "EntityRef": {
      "value": "42",
      "name": "ABC Vendor",
      "type": "Vendor"
    },
    "TxnDate": "2024-01-15",
    "DocNumber": "1001",
    "TotalAmt": 150.00,
    "Line": [
      {
        "Id": "1",
        "DetailType": "AccountBasedExpenseLineDetail",
        "Amount": 150.00,
        "AccountBasedExpenseLineDetail": {
          "AccountRef": {
            "value": "54",
            "name": "Office Supplies"
          }
        }
      }
    ],
    "PrivateNote": "Office supplies for Q1",
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
| `PaymentType` | String | **Required** | `Cash`, `Check`, or `CreditCard` |
| `AccountRef` | ReferenceType | **Required** | Bank or credit card account reference |
| `Line` | Line[] | **Required** | Individual expense line items |
| `TxnDate` | Date | Optional | Transaction date (defaults to server date) |
| `DocNumber` | String | Optional | Reference/check number (max 21 chars) |
| `PrivateNote` | String | Optional | Memo (max 4000 chars) |
| `TotalAmt` | Decimal | Read-only | Total amount (calculated by QuickBooks) |
| `EntityRef` | ReferenceType | Optional | Vendor, Customer, or Employee reference |
| `Credit` | Boolean | Optional | `true` = refund (CreditCard only) |
| `PrintStatus` | String | Optional | Check only: `NotSet`, `NeedToPrint`, `PrintComplete` |
| `RemitToAddr` | PhysicalAddress | Read-only | Payment address (Check only) |
| `CurrencyRef` | CurrencyRefType | Conditional | Required if multicurrency enabled |
| `ExchangeRate` | Decimal | Optional | Currency exchange rate |
| `DepartmentRef` | ReferenceType | Optional | Department/location reference |
| `PaymentMethodRef` | ReferenceType | Optional | Payment method reference |
| `TxnTaxDetail` | TxnTaxDetail | Optional | Tax details |
| `GlobalTaxCalculation` | Enum | Optional | `TaxExcluded`, `TaxInclusive`, `NotApplicable` |
| `MetaData` | Object | Read-only | CreateTime and LastUpdatedTime |

### Line Types

#### AccountBasedExpenseLineDetail

For expenses categorized by account:

```json
{
  "Id": "1",
  "DetailType": "AccountBasedExpenseLineDetail",
  "Amount": 100.00,
  "Description": "Office supplies",
  "AccountBasedExpenseLineDetail": {
    "AccountRef": {
      "value": "54",
      "name": "Office Supplies"
    },
    "BillableStatus": "NotBillable",
    "TaxCodeRef": {
      "value": "NON"
    }
  }
}
```

#### ItemBasedExpenseLineDetail

For expenses tracked by inventory item:

```json
{
  "Id": "2",
  "DetailType": "ItemBasedExpenseLineDetail",
  "Amount": 200.00,
  "ItemBasedExpenseLineDetail": {
    "ItemRef": {
      "value": "11",
      "name": "Printer Ink"
    },
    "Qty": 2,
    "UnitPrice": 100.00
  }
}
```

---

## Operations

### Create a Purchase

**Endpoint**: `POST /v3/company/{realmId}/purchase`

**Required Fields**:
- `PaymentType` - Cash, Check, or CreditCard
- `AccountRef` - Bank or credit card account
- `Line` - At least one expense line

#### Request: Cash Purchase

```json
{
  "PaymentType": "Cash",
  "AccountRef": {
    "value": "35",
    "name": "Checking"
  },
  "EntityRef": {
    "value": "42",
    "name": "ABC Vendor",
    "type": "Vendor"
  },
  "TxnDate": "2024-01-15",
  "Line": [
    {
      "DetailType": "AccountBasedExpenseLineDetail",
      "Amount": 150.00,
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {
          "value": "54",
          "name": "Office Supplies"
        }
      }
    }
  ],
  "PrivateNote": "Office supplies"
}
```

#### Request: Check Purchase

```json
{
  "PaymentType": "Check",
  "AccountRef": {
    "value": "35",
    "name": "Checking"
  },
  "EntityRef": {
    "value": "42",
    "name": "ABC Vendor",
    "type": "Vendor"
  },
  "DocNumber": "1001",
  "TxnDate": "2024-01-15",
  "PrintStatus": "PrintComplete",
  "Line": [
    {
      "DetailType": "AccountBasedExpenseLineDetail",
      "Amount": 500.00,
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {
          "value": "60",
          "name": "Rent Expense"
        }
      }
    }
  ]
}
```

#### Request: Credit Card Purchase

```json
{
  "PaymentType": "CreditCard",
  "AccountRef": {
    "value": "41",
    "name": "Mastercard"
  },
  "EntityRef": {
    "value": "55",
    "name": "Amazon",
    "type": "Vendor"
  },
  "TxnDate": "2024-01-15",
  "Line": [
    {
      "DetailType": "AccountBasedExpenseLineDetail",
      "Amount": 99.99,
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {
          "value": "54",
          "name": "Office Supplies"
        }
      }
    }
  ]
}
```

#### Request: Credit Card Refund

```json
{
  "PaymentType": "CreditCard",
  "Credit": true,
  "AccountRef": {
    "value": "41",
    "name": "Mastercard"
  },
  "EntityRef": {
    "value": "55",
    "name": "Amazon",
    "type": "Vendor"
  },
  "TxnDate": "2024-01-20",
  "Line": [
    {
      "DetailType": "AccountBasedExpenseLineDetail",
      "Amount": 99.99,
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {
          "value": "54",
          "name": "Office Supplies"
        }
      }
    }
  ],
  "PrivateNote": "Refund for returned item"
}
```

---

### Query Purchases

**Endpoint**: `GET /v3/company/{realmId}/query?query={selectStatement}`

#### Example Queries

```sql
-- All purchases
SELECT * FROM Purchase

-- Purchases by date range
SELECT * FROM Purchase WHERE TxnDate >= '2024-01-01' AND TxnDate <= '2024-01-31'

-- Purchases by payment type
SELECT * FROM Purchase WHERE PaymentType = 'Check'

-- Purchases by amount
SELECT * FROM Purchase WHERE TotalAmt > 1000 ORDERBY TotalAmt DESC

-- Recent purchases with pagination
SELECT * FROM Purchase ORDERBY TxnDate DESC STARTPOSITION 1 MAXRESULTS 50
```

---

### Read a Purchase

**Endpoint**: `GET /v3/company/{realmId}/purchase/{purchaseId}`

---

### Update a Purchase (Full Update)

**Endpoint**: `POST /v3/company/{realmId}/purchase`

**Required**: Include `Id` and `SyncToken` from read response, plus all writable fields.

```json
{
  "Id": "123",
  "SyncToken": "0",
  "PaymentType": "Check",
  "AccountRef": {
    "value": "35",
    "name": "Checking"
  },
  "TxnDate": "2024-01-15",
  "DocNumber": "1001",
  "Line": [
    {
      "Id": "1",
      "DetailType": "AccountBasedExpenseLineDetail",
      "Amount": 175.00,
      "AccountBasedExpenseLineDetail": {
        "AccountRef": {
          "value": "54",
          "name": "Office Supplies"
        }
      }
    }
  ],
  "PrivateNote": "Updated memo"
}
```

---

### Delete a Purchase

**Endpoint**: `POST /v3/company/{realmId}/purchase?operation=delete`

```json
{
  "Id": "123",
  "SyncToken": "1"
}
```

---

## Mercury Integration Notes

When syncing Mercury bank transactions (outgoing/expenses) to QuickBooks:

### Mapping Mercury Transactions to Purchase

| Mercury Field | QuickBooks Field |
|---------------|------------------|
| Transaction ID | `DocNumber` or `PrivateNote` |
| Amount | `Line[0].Amount` |
| Date | `TxnDate` |
| Counterparty | `EntityRef` (Vendor) |
| Description | `PrivateNote` |
| Bank Account | `AccountRef` (find Mercury checking account) |

### PaymentType Selection

| Mercury Transaction Type | QuickBooks PaymentType |
|--------------------------|------------------------|
| ACH transfer | `Cash` |
| Wire transfer | `Cash` |
| Check | `Check` |
| Card payment | `CreditCard` |

### Example: Create Purchase from Mercury Transaction

```python
def create_purchase_from_mercury(mercury_txn, qb_client):
    # Find or create vendor
    vendor = find_or_create_vendor(mercury_txn.counterparty)
    
    # Get Mercury checking account in QuickBooks
    mercury_account = get_mercury_account()
    
    # Determine expense account (could be from category mapping)
    expense_account = get_expense_account(mercury_txn.category)
    
    purchase = {
        "PaymentType": "Cash",  # or "Check" based on transaction type
        "AccountRef": {
            "value": mercury_account.id,
            "name": mercury_account.name
        },
        "EntityRef": {
            "value": vendor.id,
            "name": vendor.display_name,
            "type": "Vendor"
        },
        "TxnDate": mercury_txn.posted_at.strftime("%Y-%m-%d"),
        "Line": [
            {
                "DetailType": "AccountBasedExpenseLineDetail",
                "Amount": abs(mercury_txn.amount),
                "Description": mercury_txn.description,
                "AccountBasedExpenseLineDetail": {
                    "AccountRef": {
                        "value": expense_account.id,
                        "name": expense_account.name
                    }
                }
            }
        ],
        "PrivateNote": f"Mercury Transaction ID: {mercury_txn.id}"
    }
    
    return qb_client.create_purchase(purchase)
```

### Handling Refunds

For Mercury refunds (positive amounts on outgoing transactions), set `Credit: true` for CreditCard PaymentType, or create a Deposit instead.
