# QuickBooks API Use Cases

> Common workflow patterns for Mercury-QuickBooks integration

## Transaction Sync Workflows

### 1. Sync Mercury Outgoing Payment → QuickBooks Purchase

**When**: Mercury sends money out (ACH, wire, check)

```python
def sync_outgoing_payment(mercury_txn):
    # 1. Find or create vendor from counterparty
    vendor = find_or_create_vendor(mercury_txn.counterparty)
    
    # 2. Get Mercury bank account in QuickBooks
    bank_account = get_mercury_qb_account(mercury_txn.account_id)
    
    # 3. Determine expense category
    expense_account = get_expense_account(mercury_txn.category)
    
    # 4. Create Purchase
    purchase = {
        "PaymentType": get_payment_type(mercury_txn),  # Cash, Check, CreditCard
        "AccountRef": {"value": bank_account.id},
        "EntityRef": {"value": vendor.id, "type": "Vendor"},
        "TxnDate": mercury_txn.posted_at,
        "Line": [{
            "DetailType": "AccountBasedExpenseLineDetail",
            "Amount": abs(mercury_txn.amount),
            "AccountBasedExpenseLineDetail": {
                "AccountRef": {"value": expense_account.id}
            }
        }],
        "PrivateNote": f"Mercury ID: {mercury_txn.id}"
    }
    
    return qb.create_purchase(purchase)
```

### 2. Sync Mercury Incoming Payment → QuickBooks Deposit

**When**: Mercury receives money (customer payment, refund, interest)

```python
def sync_incoming_payment(mercury_txn):
    # 1. Find or create customer from counterparty
    customer = find_or_create_customer(mercury_txn.counterparty)
    
    # 2. Get Mercury bank account in QuickBooks
    bank_account = get_mercury_qb_account(mercury_txn.account_id)
    
    # 3. Determine income category
    income_account = get_income_account(mercury_txn.category)
    
    # 4. Create Deposit
    deposit = {
        "DepositToAccountRef": {"value": bank_account.id},
        "TxnDate": mercury_txn.posted_at,
        "Line": [{
            "DetailType": "DepositLineDetail",
            "Amount": abs(mercury_txn.amount),
            "DepositLineDetail": {
                "AccountRef": {"value": income_account.id},
                "Entity": {"value": customer.id, "type": "Customer"}
            }
        }],
        "PrivateNote": f"Mercury ID: {mercury_txn.id}"
    }
    
    return qb.create_deposit(deposit)
```

### 3. Sync Mercury Internal Transfer → QuickBooks Transfer

**When**: Money moves between Mercury accounts

```python
def sync_internal_transfer(mercury_txn):
    # 1. Get both Mercury accounts in QuickBooks
    from_account = get_mercury_qb_account(mercury_txn.from_account_id)
    to_account = get_mercury_qb_account(mercury_txn.to_account_id)
    
    # 2. Create Transfer
    transfer = {
        "FromAccountRef": {"value": from_account.id},
        "ToAccountRef": {"value": to_account.id},
        "Amount": abs(mercury_txn.amount),
        "TxnDate": mercury_txn.posted_at,
        "PrivateNote": f"Mercury ID: {mercury_txn.id}"
    }
    
    return qb.create_transfer(transfer)
```

---

## Entity Management Workflows

### Find or Create Vendor

```python
def find_or_create_vendor(name, email=None):
    # Search by name
    query = f"SELECT * FROM Vendor WHERE DisplayName = '{name}'"
    vendors = qb.query(query)
    
    if vendors:
        return vendors[0]
    
    # Create new vendor
    return qb.create_vendor({
        "DisplayName": name,
        "PrimaryEmailAddr": {"Address": email} if email else None
    })
```

### Find or Create Customer

```python
def find_or_create_customer(name, email=None):
    query = f"SELECT * FROM Customer WHERE DisplayName = '{name}'"
    customers = qb.query(query)
    
    if customers:
        return customers[0]
    
    return qb.create_customer({
        "DisplayName": name,
        "PrimaryEmailAddr": {"Address": email} if email else None
    })
```

### Map Mercury Account to QuickBooks

```python
def get_or_create_mercury_account(mercury_account):
    account_name = f"Mercury {mercury_account.name}"
    
    query = f"SELECT * FROM Account WHERE Name = '{account_name}'"
    accounts = qb.query(query)
    
    if accounts:
        return accounts[0]
    
    # Create new bank account
    return qb.create_account({
        "Name": account_name,
        "AccountType": "Bank",
        "AccountSubType": "Checking",
        "Description": f"Mercury Account: {mercury_account.id}"
    })
```

---

## Duplicate Prevention

### Using PrivateNote for Tracking

Store Mercury transaction ID in PrivateNote to prevent duplicates:

```python
def is_already_synced(mercury_txn_id, entity_type):
    query = f"SELECT * FROM {entity_type} WHERE PrivateNote LIKE '%Mercury ID: {mercury_txn_id}%'"
    results = qb.query(query)
    return len(results) > 0

def sync_transaction(mercury_txn):
    if is_already_synced(mercury_txn.id, "Purchase"):
        return "Already synced"
    # ... proceed with sync
```

---

## Batch Operations

For high-volume sync, use batch endpoint:

```python
def batch_create_purchases(purchases):
    batch_items = []
    for i, p in enumerate(purchases):
        batch_items.append({
            "bId": str(i),
            "operation": "create",
            "Purchase": p
        })
    
    return qb.batch({
        "BatchItemRequest": batch_items
    })
```

**Limits**:
- Max 30 items per batch (recommended)
- 40 batch requests/minute per realm

---

## Error Handling

```python
def safe_sync(mercury_txn):
    try:
        result = sync_transaction(mercury_txn)
        log_success(mercury_txn.id, result.id)
        return result
    except QuickBooksError as e:
        if e.code == "429":
            # Rate limited - wait and retry
            time.sleep(60)
            return safe_sync(mercury_txn)
        elif e.code == "401":
            # Token expired - refresh
            refresh_token()
            return safe_sync(mercury_txn)
        else:
            log_error(mercury_txn.id, e)
            raise
```
