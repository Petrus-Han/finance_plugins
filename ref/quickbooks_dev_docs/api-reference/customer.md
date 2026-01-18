# Customer

> QuickBooks Online API Reference: Customer Entity

A customer is a consumer of the service or product that your business offers.

## Key Concepts

### Sub-Customers and Jobs

Customers can have nested structures:
- **Parent Customer**: Top-level customer object
- **Sub-Customer**: Nested customer (e.g., team members, properties)
- **Job**: Specific project or task (e.g., kitchen remodel, car repair)

Use `ParentRef` and `Job` attributes to create hierarchy (up to 4 levels).

## Business Rules

- `DisplayName` must be **unique** across all Customer, Vendor, and Employee objects
- Names cannot contain: colon (`:`), tab (`\t`), or newline (`\n`)
- `PrimaryEmailAddr` must contain `@` and `.`
- Either `DisplayName` OR at least one of `Title`, `GivenName`, `MiddleName`, `FamilyName`, `Suffix` is required

## The Customer Object

### Sample Response

```json
{
  "Customer": {
    "Id": "58",
    "SyncToken": "0",
    "DisplayName": "ABC Corporation",
    "CompanyName": "ABC Corporation",
    "GivenName": "John",
    "FamilyName": "Doe",
    "FullyQualifiedName": "ABC Corporation",
    "PrintOnCheckName": "ABC Corporation",
    "Active": true,
    "Job": false,
    "Taxable": true,
    "Balance": 1500.00,
    "BalanceWithJobs": 1500.00,
    "PrimaryPhone": {
      "FreeFormNumber": "(555) 555-1234"
    },
    "PrimaryEmailAddr": {
      "Address": "john@abccorp.com"
    },
    "BillAddr": {
      "Line1": "123 Main Street",
      "City": "San Francisco",
      "CountrySubDivisionCode": "CA",
      "PostalCode": "94105"
    },
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
| `DisplayName` | String | Conditional | Display name (max 500 chars). Must be unique. |
| `GivenName` | String | Conditional | First name (max 100 chars) |
| `MiddleName` | String | Conditional | Middle name (max 100 chars) |
| `FamilyName` | String | Conditional | Last name (max 100 chars) |
| `Title` | String | Conditional | Title (max 16 chars) |
| `Suffix` | String | Conditional | Suffix (max 16 chars) |
| `CompanyName` | String | Optional | Company name (max 100 chars) |
| `PrintOnCheckName` | String | Optional | Name on checks (max 100 chars) |
| `FullyQualifiedName` | String | Read-only | Full hierarchy path (e.g., "Parent:Child") |
| `Active` | Boolean | Optional | Is customer active (default: true) |
| `Job` | Boolean | Optional | Is this a job (default: false) |
| `ParentRef` | ReferenceType | Optional | Reference to parent customer (for sub-customers/jobs) |
| `Level` | Integer | Read-only | Depth in hierarchy (0-4) |
| `Balance` | Decimal | Read-only | Open balance amount |
| `BalanceWithJobs` | Decimal | Read-only | Balance including jobs |
| `Taxable` | Boolean | Optional | Is customer taxable |
| `PrimaryPhone` | TelephoneNumber | Optional | Primary phone |
| `Mobile` | TelephoneNumber | Optional | Mobile phone |
| `Fax` | TelephoneNumber | Optional | Fax number |
| `PrimaryEmailAddr` | EmailAddress | Optional | Primary email |
| `WebAddr` | WebSiteAddress | Optional | Website URL |
| `BillAddr` | PhysicalAddress | Optional | Billing address |
| `ShipAddr` | PhysicalAddress | Optional | Shipping address |
| `Notes` | String | Optional | Notes about customer |
| `TermRef` | ReferenceType | Optional | Payment terms reference |
| `PaymentMethodRef` | ReferenceType | Optional | Default payment method |
| `CurrencyRef` | CurrencyRef | Optional | Currency (read-only after create) |
| `PreferredDeliveryMethod` | String | Optional | `Print`, `Email`, `None` |
| `MetaData` | Object | Read-only | CreateTime and LastUpdatedTime |

---

## Operations

### Create a Customer

**Endpoint**: `POST /v3/company/{realmId}/customer`

**Required**: Either `DisplayName` OR at least one name component

#### Request: Company

```json
{
  "DisplayName": "ABC Corporation",
  "CompanyName": "ABC Corporation",
  "PrimaryPhone": {
    "FreeFormNumber": "(555) 555-1234"
  },
  "PrimaryEmailAddr": {
    "Address": "info@abccorp.com"
  },
  "BillAddr": {
    "Line1": "123 Main Street",
    "City": "San Francisco",
    "CountrySubDivisionCode": "CA",
    "PostalCode": "94105"
  }
}
```

#### Request: Individual

```json
{
  "GivenName": "John",
  "FamilyName": "Doe",
  "DisplayName": "John Doe",
  "PrimaryEmailAddr": {
    "Address": "john.doe@email.com"
  }
}
```

#### Request: Sub-Customer (Job)

```json
{
  "DisplayName": "Kitchen Remodel 2024",
  "Job": true,
  "ParentRef": {
    "value": "58"
  }
}
```

---

### Query Customers

**Endpoint**: `GET /v3/company/{realmId}/query?query={selectStatement}`

#### Example Queries

```sql
-- All customers
SELECT * FROM Customer

-- Active customers only
SELECT * FROM Customer WHERE Active = true

-- Search by display name
SELECT * FROM Customer WHERE DisplayName LIKE '%ABC%'

-- Search by email
SELECT * FROM Customer WHERE PrimaryEmailAddr LIKE '%@example.com%'

-- Customers with balance
SELECT * FROM Customer WHERE Balance > 0

-- Parent customers only (not jobs)
SELECT * FROM Customer WHERE Job = false

-- Sub-customers/jobs under a parent
SELECT * FROM Customer WHERE ParentRef = '58'

-- Recently updated
SELECT * FROM Customer WHERE MetaData.LastUpdatedTime > '2024-01-01'

-- Pagination
SELECT * FROM Customer ORDERBY DisplayName STARTPOSITION 1 MAXRESULTS 50
```

---

### Read a Customer

**Endpoint**: `GET /v3/company/{realmId}/customer/{customerId}`

---

### Update a Customer (Full Update)

**Endpoint**: `POST /v3/company/{realmId}/customer`

```json
{
  "Id": "58",
  "SyncToken": "0",
  "DisplayName": "ABC Corporation",
  "CompanyName": "ABC Corporation - Updated",
  "PrimaryPhone": {
    "FreeFormNumber": "(555) 555-9999"
  },
  "Active": true
}
```

### Sparse Update a Customer

```json
{
  "Id": "58",
  "SyncToken": "0",
  "sparse": true,
  "PrimaryPhone": {
    "FreeFormNumber": "(555) 555-9999"
  }
}
```

---

### Deactivate a Customer (Soft Delete)

```json
{
  "Id": "58",
  "SyncToken": "1",
  "sparse": true,
  "Active": false
}
```

---

## Mercury Integration Notes

When syncing Mercury incoming transactions (deposits), you may need to match or create Customer records for payers.

### Mapping Mercury Payers to Customers

| Mercury Field | QuickBooks Customer Field |
|---------------|---------------------------|
| Payer Name | `DisplayName` |
| Payer Email | `PrimaryEmailAddr.Address` |
| (Business) | `CompanyName` |
| (Individual) | `GivenName`, `FamilyName` |

### Find or Create Customer Strategy

```python
def find_or_create_customer(mercury_payer, qb_client):
    """Find existing customer or create new one from Mercury payer."""
    
    # 1. Try to find by display name (exact match)
    query = f"SELECT * FROM Customer WHERE DisplayName = '{mercury_payer.name}'"
    customers = qb_client.query(query)
    
    if customers:
        return customers[0]
    
    # 2. Try fuzzy search if no exact match
    query = f"SELECT * FROM Customer WHERE DisplayName LIKE '%{mercury_payer.name}%'"
    customers = qb_client.query(query)
    
    if customers:
        return customers[0]
    
    # 3. Create new customer if not found
    customer_data = {
        "DisplayName": mercury_payer.name,
        "Active": True
    }
    
    if mercury_payer.email:
        customer_data["PrimaryEmailAddr"] = {
            "Address": mercury_payer.email
        }
    
    if is_company_name(mercury_payer.name):
        customer_data["CompanyName"] = mercury_payer.name
    else:
        parts = mercury_payer.name.split()
        if len(parts) >= 2:
            customer_data["GivenName"] = parts[0]
            customer_data["FamilyName"] = parts[-1]
    
    return qb_client.create_customer(customer_data)
```

### When to Use Customer vs Vendor

| Scenario | Entity |
|----------|--------|
| You sell to them | **Customer** |
| You buy from them | **Vendor** |
| Both (customer & supplier) | Create BOTH entities |

For Mercury transactions:
- **Incoming money (Deposit)** → Use Customer
- **Outgoing money (Purchase)** → Use Vendor
