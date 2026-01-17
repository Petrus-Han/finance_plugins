# Query Operations and Syntax

> Source: https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/data-queries

You can use the query operation to get details about a specific API entity.

---

## How Query Operations Work

You can query most API entities. The query operation is similar to a SQL SELECT statement with limitations to ensure requests don't overload server-side resources:

### Supported Features
- Server responses return all attributes for each API entity
- Server responses only return attributes with values
- Wildcard character "%" supported for LIKE clauses

### Not Supported
- Projections
- OR operations in WHERE clauses
- GROUP BY clauses
- JOIN clauses
- Special characters

---

## Using the Query Operation

### Method 1: GET with URI Parameter

```http
GET https://quickbooks.api.intuit.com/v3/company/<realmId>/query?query=<select_statement>
```

### Method 2: POST with Request Body

```http
POST https://quickbooks.api.intuit.com/v3/company/<realmId>/query
Content-Type: application/text

SELECT * FROM Customer WHERE Metadata.LastUpdatedTime > '2011-08-10T10:20:30'
```

---

## Select Statement Syntax

```sql
SELECT * | count(*) FROM IntuitEntity
   [WHERE WhereClause]
   [ORDERBY OrderByClause]
   [STARTPOSITION Number] [MAXRESULTS Number]
```

### Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `SELECT *` | | All fields are returned |
| `count(*)` | | Returns the number of records that satisfy the query criteria |
| `Entity` | Customer, Vendor, Invoice, etc | The name of the queried entity (case sensitive). **Only one entity at a time** |
| `WhereClause` | PropertyName, Operator Value [AND WhereClause] | Filters returned data. Multiple clauses use AND. **OR not supported** |
| `Operator` | IN, =, <, >, <=, >=, LIKE | LIKE supports "%" wildcard only |
| `Value` | (Value [,Value]), 'value_in_quote', value_without_quote, true, false, ' ' | Null is represented as ' ' (space within single quotes) |
| `OrderByClause` | PropertyName [ASC, DESC] | Sorts the result |
| `Number` | | Must be a positive integer |

---

## Server Responses

Server responses contain a `<QueryResponse>` element with the matching API entities.

### Response Attributes

| Attribute | Description |
|-----------|-------------|
| `startposition` | Starting point of the response for pagination |
| `maxresults` | Number of entities in the response. **Max: 1000**, Default: 100 |
| `sparse` | True if response doesn't return all attributes |

### Example Response (XML)

```xml
<IntuitResponse xmlns="http://schema.intuit.com/finance/v3" time="2013-04-03T10:22:55.766Z">
   <QueryResponse startPosition="10" maxResults="2">
      <Customer>
         <Id>2123</Id>
         <SyncToken>0</SyncToken>
         <GivenName>Srini</GivenName>
      </Customer>
      <Customer>
         <Id>2124</Id>
         <SyncToken>0</SyncToken>
         <GivenName>Peter</GivenName>
      </Customer>
   </QueryResponse>
</IntuitResponse>
```

---

## Query Syntax

### Case Sensitivity

Reserved words, entity names, and attribute names are **not case sensitive**. Attribute values are also not case sensitive.

```sql
-- These are equivalent:
SELECT * FROM Customer WHERE GivenName = 'greg' STARTPOSITION 10
SELECT * from cUstomer where givenname = 'Greg' Startposition 10
```

### Escape Character

Use backslash (`\`) to escape special characters like apostrophes (`'`).

```sql
SELECT * FROM Customer WHERE CompanyName = 'Adam\'s Candy Shop'
```

---

## Query Language Operations

### Filters (WHERE Clause)

Filter criteria is based on attribute values.

```sql
-- Invoices with TotalAmt > 1000
SELECT * FROM Invoice WHERE TotalAmt > '1000.0'

-- Invoices for a specific customer
SELECT * FROM Invoice WHERE CustomerRef = '123'

-- All active and inactive customers
SELECT * FROM Customer WHERE Active IN (true, false)

-- Customer by ID
SELECT * FROM Customer WHERE Id = '123456'

-- Name starts with "K", ends with "h"
SELECT * FROM Customer WHERE GivenName LIKE 'K%h'

-- Date range
SELECT * FROM Invoice WHERE TxnDate > '2011-01-01' AND TxnDate <= CURRENT_DATE
```

> **Note**: ID field only supports `=` and `IN` operators, not `>`, `<`, `>=`, `<=`, `!=`, or `LIKE`.

### Multiple Filters

Use `AND` to combine filters. **OR is not supported**.

```sql
-- Time range filter
SELECT * FROM Invoice 
WHERE MetaData.CreateTime >= '2009-10-14T04:05:05-07:00' 
AND MetaData.CreateTime <= '2012-10-14T04:05:05-07:00'

-- Multiple conditions
SELECT * FROM Invoice 
WHERE id in ('64523', '18761', '35767') 
AND MetaData.CreateTime >= '1990-12-12T12:50:30Z' 
AND MetaData.LastUpdatedTime <= '1990-12-12T12:50:30Z'
```

### Sorting (ORDERBY)

```sql
-- Ascending (default)
SELECT * FROM Customer ORDERBY FamilyName

-- Descending
SELECT * FROM Customer ORDERBY FamilyName DESC
```

### Pagination

Use `STARTPOSITION` and `MAXRESULTS` to page through results.

```sql
-- Get invoices 1-10
SELECT * FROM Invoice STARTPOSITION 1 MAXRESULTS 10

-- Get invoices 11-20
SELECT * FROM Invoice STARTPOSITION 11 MAXRESULTS 10

-- Get invoices 21-25
SELECT * FROM Invoice STARTPOSITION 21 MAXRESULTS 10
```

### Count

Use `COUNT(*)` to get the total number of entities.

```sql
SELECT COUNT(*) FROM Customer
```

---

## Common Query Examples

| Use Case | Query |
|----------|-------|
| All customers | `SELECT * FROM Customer` |
| Active customers only | `SELECT * FROM Customer WHERE active = true` |
| Customer by ID | `SELECT * FROM Customer WHERE Id = '123'` |
| Invoices for customer | `SELECT * FROM Invoice WHERE CustomerRef = '123'` |
| Recent invoices | `SELECT * FROM Invoice WHERE TxnDate > '2024-01-01'` |
| Search by name | `SELECT * FROM Customer WHERE GivenName LIKE 'John%'` |
| Count customers | `SELECT COUNT(*) FROM Customer` |
| Paginated results | `SELECT * FROM Invoice STARTPOSITION 1 MAXRESULTS 100` |

---

## Mercury Integration Notes

For Mercury bank transaction sync, common queries include:

```sql
-- Find existing vendor by name
SELECT * FROM Vendor WHERE DisplayName LIKE '%Mercury%'

-- Find bank account
SELECT * FROM Account WHERE AccountType = 'Bank'

-- Recent purchases
SELECT * FROM Purchase WHERE TxnDate > '2024-01-01'

-- Recent deposits  
SELECT * FROM Deposit WHERE TxnDate > '2024-01-01'
```

---

## Learn More

- [API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [Batch Operations](./batch.md)
- [Change Data Capture](./change-data-capture.md)
