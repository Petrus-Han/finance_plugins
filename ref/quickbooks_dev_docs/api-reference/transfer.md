# Transfer

> QuickBooks Online API Reference: Transfer Entity

A Transfer represents a transaction where funds are moved between two accounts from the company's QuickBooks chart of accounts.

## Business Rules

- `FromAccountRef`, `ToAccountRef`, and `Amount` are all **required**
- Both accounts must have `Account.Classification` set to `Asset`

## The Transfer Object

### Sample Response

```json
{
  "Transfer": {
    "Id": "145",
    "SyncToken": "0",
    "FromAccountRef": {
      "value": "35",
      "name": "Checking"
    },
    "ToAccountRef": {
      "value": "36",
      "name": "Savings"
    },
    "Amount": 1000.00,
    "TxnDate": "2024-01-15",
    "PrivateNote": "Monthly savings transfer",
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
| `FromAccountRef` | ReferenceType | **Required** | Source asset account |
| `ToAccountRef` | ReferenceType | **Required** | Destination asset account |
| `Amount` | Decimal | **Required** | Transfer amount |
| `TxnDate` | Date | Optional | Transaction date (defaults to server date) |
| `PrivateNote` | String | Optional | Memo (max 4000 chars) |
| `MetaData` | Object | Read-only | CreateTime and LastUpdatedTime |
| `RecurDataRef` | ReferenceType | Read-only | Recurring transaction template reference |

### Account Reference Format

```json
{
  "FromAccountRef": {
    "value": "35",
    "name": "Checking"
  },
  "ToAccountRef": {
    "value": "36",
    "name": "Savings"
  }
}
```

---

## Operations

### Create a Transfer

**Endpoint**: `POST /v3/company/{realmId}/transfer`

**Required Fields**:
- `FromAccountRef` - Source asset account
- `ToAccountRef` - Destination asset account
- `Amount` - Transfer amount

#### Request

```json
{
  "FromAccountRef": {
    "value": "35",
    "name": "Checking"
  },
  "ToAccountRef": {
    "value": "36",
    "name": "Savings"
  },
  "Amount": 1000.00,
  "TxnDate": "2024-01-15",
  "PrivateNote": "Monthly savings transfer"
}
```

#### Response

```json
{
  "Transfer": {
    "Id": "145",
    "SyncToken": "0",
    "FromAccountRef": {
      "value": "35",
      "name": "Checking"
    },
    "ToAccountRef": {
      "value": "36",
      "name": "Savings"
    },
    "Amount": 1000.00,
    "TxnDate": "2024-01-15",
    "PrivateNote": "Monthly savings transfer",
    "MetaData": {
      "CreateTime": "2024-01-15T10:00:00-08:00",
      "LastUpdatedTime": "2024-01-15T10:00:00-08:00"
    }
  },
  "time": "2024-01-15T10:00:00.000-08:00"
}
```

---

### Query Transfers

**Endpoint**: `GET /v3/company/{realmId}/query?query={selectStatement}`

#### Example Queries

```sql
-- All transfers
SELECT * FROM Transfer

-- Transfers by date range
SELECT * FROM Transfer WHERE TxnDate >= '2024-01-01' AND TxnDate <= '2024-01-31'

-- Transfers by amount
SELECT * FROM Transfer WHERE Amount > 1000

-- Recent transfers
SELECT * FROM Transfer ORDERBY TxnDate DESC STARTPOSITION 1 MAXRESULTS 50
```

---

### Read a Transfer

**Endpoint**: `GET /v3/company/{realmId}/transfer/{transferId}`

---

### Update a Transfer (Full Update)

**Endpoint**: `POST /v3/company/{realmId}/transfer`

```json
{
  "Id": "145",
  "SyncToken": "0",
  "FromAccountRef": {
    "value": "35",
    "name": "Checking"
  },
  "ToAccountRef": {
    "value": "36",
    "name": "Savings"
  },
  "Amount": 1500.00,
  "TxnDate": "2024-01-15",
  "PrivateNote": "Updated transfer amount"
}
```

### Sparse Update a Transfer

```json
{
  "Id": "145",
  "SyncToken": "0",
  "sparse": true,
  "Amount": 1500.00,
  "FromAccountRef": {
    "value": "35"
  },
  "ToAccountRef": {
    "value": "36"
  }
}
```

---

### Delete a Transfer

**Endpoint**: `POST /v3/company/{realmId}/transfer?operation=delete`

```json
{
  "Id": "145",
  "SyncToken": "1"
}
```

---

## Mercury Integration Notes

Mercury internal transfers between accounts should be recorded as QuickBooks Transfer objects, NOT as Purchase or Deposit.

### Identifying Transfers

A Mercury transaction is an internal transfer when:
- Both `fromAccount` and `toAccount` are Mercury accounts
- Or marked as `internalTransfer` type

### Mapping Mercury Transfers

| Mercury Field | QuickBooks Transfer Field |
|---------------|---------------------------|
| Transaction ID | `PrivateNote` |
| From Account | `FromAccountRef` |
| To Account | `ToAccountRef` |
| Amount | `Amount` (absolute value) |
| Date | `TxnDate` |
| Description | `PrivateNote` |

### Example: Create Transfer from Mercury

```python
def create_transfer_from_mercury(mercury_txn, qb_client):
    """Create QuickBooks Transfer from Mercury internal transfer."""
    
    # Get QuickBooks account IDs for Mercury accounts
    from_account = get_qb_account_for_mercury(mercury_txn.from_account_id)
    to_account = get_qb_account_for_mercury(mercury_txn.to_account_id)
    
    transfer = {
        "FromAccountRef": {
            "value": from_account.id,
            "name": from_account.name
        },
        "ToAccountRef": {
            "value": to_account.id,
            "name": to_account.name
        },
        "Amount": abs(mercury_txn.amount),
        "TxnDate": mercury_txn.posted_at.strftime("%Y-%m-%d"),
        "PrivateNote": f"Mercury Transfer ID: {mercury_txn.id}\n{mercury_txn.description}"
    }
    
    return qb_client.create_transfer(transfer)


def get_qb_account_for_mercury(mercury_account_id):
    """Find QuickBooks account corresponding to Mercury account."""
    # This could use a mapping table or search by account name/number
    account_map = {
        "mercury_checking_123": "35",  # QB Checking account ID
        "mercury_savings_456": "36",   # QB Savings account ID
        "mercury_treasury_789": "40"   # QB Other Current Asset ID
    }
    qb_id = account_map.get(mercury_account_id)
    if qb_id:
        return qb_client.get_account(qb_id)
    raise ValueError(f"No QuickBooks account mapped for Mercury account: {mercury_account_id}")
```

### When to Use Transfer vs Other Entities

| Scenario | Entity |
|----------|--------|
| Move money between company bank accounts | **Transfer** |
| Move money to/from external party | Purchase or Deposit |
| Refund from vendor | Deposit (or VendorCredit) |
| Payment to vendor | Purchase |
| Receipt from customer | Deposit |

### Handling Two-Sided Mercury Transfers

Mercury may show a transfer as two separate transactions (one outgoing, one incoming). You should:

1. **Detect paired transactions**: Match by amount, date, and counterparty account
2. **Create single Transfer**: Only create one QuickBooks Transfer for the pair
3. **Mark both as synced**: Track that both Mercury transactions are covered

```python
def is_transfer_pair(txn1, txn2):
    """Check if two Mercury transactions form a transfer pair."""
    return (
        abs(txn1.amount) == abs(txn2.amount) and
        txn1.from_account_id == txn2.to_account_id and
        txn1.to_account_id == txn2.from_account_id and
        abs((txn1.posted_at - txn2.posted_at).days) <= 1
    )
```
