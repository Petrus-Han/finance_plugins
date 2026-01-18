# Vendor

> QuickBooks Online API Reference: Vendor Entity

The Vendor object represents the seller from whom your company purchases any service or product.

## Business Rules

- `DisplayName` must be **unique** across all Vendor, Customer, and Employee objects
- Names cannot contain: colon (`:`), tab (`\t`), or newline (`\n`)
- `PrimaryEmailAddr` must contain `@` and `.`
- Either `DisplayName` OR at least one of `Title`, `GivenName`, `MiddleName`, `FamilyName`, `Suffix` is required

## The Vendor Object

### Sample Response

```json
{
  "Vendor": {
    "Id": "42",
    "SyncToken": "0",
    "DisplayName": "ABC Supplies Inc",
    "CompanyName": "ABC Supplies Inc",
    "GivenName": "John",
    "FamilyName": "Smith",
    "PrintOnCheckName": "ABC Supplies Inc",
    "Active": true,
    "Vendor1099": false,
    "Balance": 500.00,
    "PrimaryPhone": {
      "FreeFormNumber": "(555) 555-1234"
    },
    "PrimaryEmailAddr": {
      "Address": "john@abcsupplies.com"
    },
    "WebAddr": {
      "URI": "https://www.abcsupplies.com"
    },
    "BillAddr": {
      "Line1": "123 Main Street",
      "City": "San Francisco",
      "CountrySubDivisionCode": "CA",
      "PostalCode": "94105",
      "Country": "USA"
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
| `Active` | Boolean | Optional | Is vendor active (default: true) |
| `Balance` | Decimal | Read-only | Open balance (unpaid amount) |
| `Vendor1099` | Boolean | Optional | Is 1099 contractor |
| `PrimaryPhone` | TelephoneNumber | Optional | Primary phone |
| `Mobile` | TelephoneNumber | Optional | Mobile phone |
| `Fax` | TelephoneNumber | Optional | Fax number |
| `AlternatePhone` | TelephoneNumber | Optional | Alternate phone |
| `PrimaryEmailAddr` | EmailAddress | Optional | Primary email |
| `WebAddr` | WebSiteAddress | Optional | Website URL |
| `BillAddr` | PhysicalAddress | Optional | Billing address |
| `TermRef` | ReferenceType | Optional | Payment terms reference |
| `CurrencyRef` | CurrencyRef | Optional | Currency (read-only after create) |
| `TaxIdentifier` | String | Optional | Tax ID (masked in response) |
| `AcctNum` | String | Optional | Account number (max 100 chars) |
| `CostRate` | Decimal | Optional | Pay rate |
| `BillRate` | Decimal | Optional | Hourly billing rate |
| `MetaData` | Object | Read-only | CreateTime and LastUpdatedTime |

### Address Format

```json
{
  "BillAddr": {
    "Line1": "123 Main Street",
    "Line2": "Suite 100",
    "Line3": "",
    "Line4": "",
    "Line5": "",
    "City": "San Francisco",
    "CountrySubDivisionCode": "CA",
    "PostalCode": "94105",
    "Country": "USA"
  }
}
```

### Phone Format

```json
{
  "PrimaryPhone": {
    "FreeFormNumber": "(555) 555-1234"
  }
}
```

### Email Format

```json
{
  "PrimaryEmailAddr": {
    "Address": "vendor@example.com"
  }
}
```

---

## Operations

### Create a Vendor

**Endpoint**: `POST /v3/company/{realmId}/vendor`

**Required**: Either `DisplayName` OR at least one name component

#### Request: Minimal (Company)

```json
{
  "DisplayName": "ABC Supplies Inc"
}
```

#### Request: Full Company Details

```json
{
  "DisplayName": "ABC Supplies Inc",
  "CompanyName": "ABC Supplies Inc",
  "PrintOnCheckName": "ABC Supplies Inc",
  "PrimaryPhone": {
    "FreeFormNumber": "(555) 555-1234"
  },
  "PrimaryEmailAddr": {
    "Address": "ap@abcsupplies.com"
  },
  "WebAddr": {
    "URI": "https://www.abcsupplies.com"
  },
  "BillAddr": {
    "Line1": "123 Main Street",
    "City": "San Francisco",
    "CountrySubDivisionCode": "CA",
    "PostalCode": "94105"
  },
  "Vendor1099": false
}
```

#### Request: Individual (Person)

```json
{
  "GivenName": "John",
  "FamilyName": "Smith",
  "DisplayName": "John Smith - Contractor",
  "PrimaryEmailAddr": {
    "Address": "john.smith@email.com"
  },
  "Vendor1099": true
}
```

#### Response

```json
{
  "Vendor": {
    "Id": "42",
    "SyncToken": "0",
    "DisplayName": "ABC Supplies Inc",
    "CompanyName": "ABC Supplies Inc",
    "Active": true,
    "Balance": 0,
    "MetaData": {
      "CreateTime": "2024-01-15T10:00:00-08:00",
      "LastUpdatedTime": "2024-01-15T10:00:00-08:00"
    }
  },
  "time": "2024-01-15T10:00:00.000-08:00"
}
```

---

### Query Vendors

**Endpoint**: `GET /v3/company/{realmId}/query?query={selectStatement}`

#### Example Queries

```sql
-- All vendors
SELECT * FROM Vendor

-- Active vendors only
SELECT * FROM Vendor WHERE Active = true

-- Search by display name
SELECT * FROM Vendor WHERE DisplayName LIKE '%ABC%'

-- Search by company name
SELECT * FROM Vendor WHERE CompanyName LIKE '%Supplies%'

-- Vendors with balance
SELECT * FROM Vendor WHERE Balance > 0

-- 1099 vendors
SELECT * FROM Vendor WHERE Vendor1099 = true

-- Recently updated
SELECT * FROM Vendor WHERE MetaData.LastUpdatedTime > '2024-01-01'

-- Pagination
SELECT * FROM Vendor ORDERBY DisplayName STARTPOSITION 1 MAXRESULTS 50
```

---

### Read a Vendor

**Endpoint**: `GET /v3/company/{realmId}/vendor/{vendorId}`

---

### Update a Vendor (Full Update)

**Endpoint**: `POST /v3/company/{realmId}/vendor`

**Required**: Include `Id` and `SyncToken` from read response, plus all writable fields.

```json
{
  "Id": "42",
  "SyncToken": "0",
  "DisplayName": "ABC Supplies Inc",
  "CompanyName": "ABC Supplies Inc - Updated",
  "PrimaryPhone": {
    "FreeFormNumber": "(555) 555-9999"
  },
  "PrimaryEmailAddr": {
    "Address": "newemail@abcsupplies.com"
  },
  "Active": true
}
```

---

### Deactivate a Vendor (Soft Delete)

Set `Active` to `false`:

```json
{
  "Id": "42",
  "SyncToken": "1",
  "sparse": true,
  "Active": false
}
```

---

## Mercury Integration Notes

When syncing Mercury transactions to QuickBooks, you need to match or create Vendor records for transaction counterparties.

### Mapping Mercury Recipients to Vendors

| Mercury Field | QuickBooks Vendor Field |
|---------------|-------------------------|
| Recipient Name | `DisplayName` |
| Recipient Email | `PrimaryEmailAddr.Address` |
| Account Number | `AcctNum` |
| (Business) | `CompanyName` |
| (Individual) | `GivenName`, `FamilyName` |

### Find or Create Vendor Strategy

```python
def find_or_create_vendor(mercury_recipient, qb_client):
    """Find existing vendor or create new one from Mercury recipient."""
    
    # 1. Try to find by display name (exact match)
    query = f"SELECT * FROM Vendor WHERE DisplayName = '{mercury_recipient.name}'"
    vendors = qb_client.query(query)
    
    if vendors:
        return vendors[0]
    
    # 2. Try fuzzy search if no exact match
    query = f"SELECT * FROM Vendor WHERE DisplayName LIKE '%{mercury_recipient.name}%'"
    vendors = qb_client.query(query)
    
    if vendors:
        # Return first match (or implement better matching logic)
        return vendors[0]
    
    # 3. Create new vendor if not found
    vendor_data = {
        "DisplayName": mercury_recipient.name,
        "Active": True
    }
    
    # Add email if available
    if mercury_recipient.email:
        vendor_data["PrimaryEmailAddr"] = {
            "Address": mercury_recipient.email
        }
    
    # Determine if company or individual
    if is_company_name(mercury_recipient.name):
        vendor_data["CompanyName"] = mercury_recipient.name
    else:
        # Try to split into first/last name
        parts = mercury_recipient.name.split()
        if len(parts) >= 2:
            vendor_data["GivenName"] = parts[0]
            vendor_data["FamilyName"] = parts[-1]
    
    return qb_client.create_vendor(vendor_data)


def is_company_name(name):
    """Simple heuristic to detect company names."""
    company_indicators = ['Inc', 'LLC', 'Corp', 'Ltd', 'Co.', 'Company', 'Services', 'Solutions']
    return any(indicator in name for indicator in company_indicators)
```

### Handling Duplicate Names

QuickBooks requires unique `DisplayName`. If a duplicate is detected:

1. **Option A**: Append identifier (e.g., "John Smith - Mercury")
2. **Option B**: Search more carefully for existing match
3. **Option C**: Use Mercury recipient ID in `AcctNum` for tracking

```python
def create_unique_vendor(name, qb_client, suffix=""):
    """Create vendor with unique display name."""
    display_name = f"{name}{suffix}" if suffix else name
    
    try:
        return qb_client.create_vendor({"DisplayName": display_name})
    except DuplicateNameError:
        # Add suffix and retry
        return create_unique_vendor(name, qb_client, f" - {uuid.uuid4().hex[:8]}")
```

### Vendor Caching

For performance, cache vendor lookups:

```python
class VendorCache:
    def __init__(self, qb_client):
        self.qb_client = qb_client
        self._cache = {}
        self._loaded = False
    
    def load_all(self):
        """Load all vendors into cache."""
        vendors = self.qb_client.query("SELECT * FROM Vendor WHERE Active = true")
        for v in vendors:
            self._cache[v['DisplayName'].lower()] = v
        self._loaded = True
    
    def find(self, name):
        """Find vendor by name (case-insensitive)."""
        if not self._loaded:
            self.load_all()
        return self._cache.get(name.lower())
    
    def add(self, vendor):
        """Add newly created vendor to cache."""
        self._cache[vendor['DisplayName'].lower()] = vendor
```

### When to Create vs Match

| Scenario | Action |
|----------|--------|
| Exact name match found | Use existing vendor |
| Fuzzy match with high confidence | Use existing (log for review) |
| No match found | Create new vendor |
| Multiple potential matches | Log for manual review |
