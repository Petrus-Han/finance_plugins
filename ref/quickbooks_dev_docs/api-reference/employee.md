# Employee

An Employee object represents a person working for the company. If you are looking to create a Contractor via API, refer to how to create a Vendor object, with Vendor1099 field set to true.

## Business Rules

- The DisplayName, Title, GivenName, MiddleName, FamilyName, Suffix, and PrintOnCheckName attributes must not contain colon (:), tab (\t), or newline (\n) characters.
- The DisplayName attribute must be unique across all other customer, employee, and vendor objects.
- The GivenName and FamilyName attributes are required (at least one).
- The PrimaryEmailAddress attribute must contain an at sign (@) and dot (.).

### QuickBooks Payroll Considerations

The full complement of read, create, delete via deactivation (active=false), and update operations are available both with and without QuickBooks Payroll enabled. However, when Payroll is enabled, support for some attributes is limited:

| Attribute | Payroll Enabled Behavior |
|-----------|-------------------------|
| **Title** | Not supported |
| **Suffix** | Not supported |
| **DisplayName** | Read-only, concatenation of GivenName MiddleName FamilyName |
| **PrintOnCheckName** | Not supported |
| **BillRate** | Not supported |
| **SSN** | Masked SSNs cannot be passed in a request; code must be removed before submitting |

### Determine if Company is Payroll Enabled

Query the CompanyInfo endpoint to determine if the company is payroll enabled:
1. Issue a Get operation to the CompanyInfo endpoint
2. Scan the response for: `{ "Name": "PayrollFeature", "Value": "true" }`
3. Payroll is enabled if Value is set to true

## The Employee Object

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String, read only, filterable, sortable | Unique identifier for this object. Sort order is ASC by default. *Required for update* |
| **SyncToken** | String, read only | Version number of the object. *Required for update* |
| **PrimaryAddr** | PhysicalAddress (max 30 chars) | Physical street address for this employee. If QuickBooks Payroll is enabled, City, CountrySubDivisionCode, and PostalCode are required. *Conditionally required* |
| **PrimaryEmailAddr** | EmailAddress | Primary email address. |
| **DisplayName** | String (max 500 chars), filterable, sortable | The name as displayed. If not supplied, system generates from name components. Read-only when Payroll is enabled. |
| **Title** | String (max 16 chars) | Title of the person. Not supported when Payroll is enabled. |
| **BillableTime** | Boolean | If true, this entity is currently enabled for use by QuickBooks. |
| **GivenName** | String (max 100 chars), filterable, sortable | Given name or first name. At least one of GivenName or FamilyName is required. |
| **BirthDate** | Date | Birth date of the employee. |
| **MiddleName** | String (max 100 chars), filterable, sortable | Middle name of the person. |
| **SSN** | String (max 100 chars) | Social security number. Masked in response with XXX-XX-XXXX. Cannot be passed when Payroll is enabled. |
| **PrimaryPhone** | TelephoneNumber (max 20 chars) | Primary phone number. |
| **Active** | Boolean, filterable | If true, this entity is currently enabled for use. |
| **ReleasedDate** | Date | Release date of the employee. |
| **MetaData** | ModificationMetaData | Descriptive information about the object. Read only. |
| **CostRate** | BigDecimal | Pay rate of the employee. |
| **Mobile** | TelephoneNumber (max 20 chars) | Mobile phone number. |
| **Gender** | String | Gender of the employee. Values: Male or Female. |
| **HiredDate** | Date | Hire date of the employee. |
| **BillRate** | BigDecimal | Can only be set if BillableTime is true. Not supported when Payroll is enabled. |
| **Organization** | Boolean | true–represents an organization. false–represents a person. |
| **Suffix** | String (max 16 chars), filterable, sortable | Suffix of the name (e.g., Jr.). Not supported when Payroll is enabled. |
| **FamilyName** | String (max 100 chars), filterable, sortable | Family name or last name. At least one of GivenName or FamilyName is required. |
| **PrintOnCheckName** | String (max 100 chars), filterable, sortable | Name as printed on a check. Not supported when Payroll is enabled. |
| **EmployeeNumber** | String (max 100 chars) | ID number of the employee in the employer's directory. |
| **V4IDPseudonym** | String, read only | Employee reference number. For internal use only. *minorVersion: 26* |

### Sample Object

```json
{
  "Employee": {
    "SyncToken": "0",
    "domain": "QBO",
    "DisplayName": "Bill Miller",
    "PrimaryPhone": {
      "FreeFormNumber": "234-525-1234"
    },
    "PrintOnCheckName": "Bill Miller",
    "FamilyName": "Miller",
    "Active": true,
    "SSN": "XXX-XX-XXXX",
    "PrimaryAddr": {
      "CountrySubDivisionCode": "CA",
      "City": "Middlefield",
      "PostalCode": "93242",
      "Id": "116",
      "Line1": "45 N. Elm Street"
    },
    "sparse": false,
    "BillableTime": false,
    "GivenName": "Bill",
    "Id": "71",
    "MetaData": {
      "CreateTime": "2015-07-24T09:34:35-07:00",
      "LastUpdatedTime": "2015-07-24T09:34:35-07:00"
    }
  },
  "time": "2015-07-24T09:35:54.805-07:00"
}
```

## Create an Employee

### Request

```
POST /v3/company/<realmID>/employee
Content-Type: application/json
```

**Production Base URL:** `https://quickbooks.api.intuit.com`
**Sandbox Base URL:** `https://sandbox-quickbooks.api.intuit.com`

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **GivenName** | String | Given name. At least one of GivenName or FamilyName is required. |
| **FamilyName** | String | Family name. At least one of GivenName or FamilyName is required. |
| **PrimaryAddr** | PhysicalAddress | Required when QuickBooks Payroll is enabled. *Conditionally required* |

### Sample Request Body

```json
{
  "GivenName": "John",
  "SSN": "444-55-6666",
  "PrimaryAddr": {
    "CountrySubDivisionCode": "CA",
    "City": "Middlefield",
    "PostalCode": "93242",
    "Id": "50",
    "Line1": "45 N. Elm Street"
  },
  "PrimaryPhone": {
    "FreeFormNumber": "408-525-1234"
  },
  "FamilyName": "Meuller"
}
```

### Sample Response

```json
{
  "Employee": {
    "SyncToken": "0",
    "domain": "QBO",
    "DisplayName": "John Meuller",
    "PrimaryPhone": {
      "FreeFormNumber": "408-525-1234"
    },
    "PrintOnCheckName": "John Meuller",
    "FamilyName": "Meuller",
    "Active": true,
    "SSN": "XXX-XX-XXXX",
    "PrimaryAddr": {
      "CountrySubDivisionCode": "CA",
      "City": "Middlefield",
      "PostalCode": "93242",
      "Id": "115",
      "Line1": "45 N. Elm Street"
    },
    "sparse": false,
    "BillableTime": false,
    "GivenName": "John",
    "Id": "70",
    "MetaData": {
      "CreateTime": "2015-07-24T09:24:57-07:00",
      "LastUpdatedTime": "2015-07-24T09:24:57-07:00"
    }
  },
  "time": "2015-07-24T09:24:57.907-07:00"
}
```

## Query an Employee

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: text/plain
```

### Sample Query

```sql
select * from Employee where DisplayName = 'Emily Platt'
```

### Sample Response

```json
{
  "QueryResponse": {
    "Employee": [
      {
        "SyncToken": "2",
        "domain": "QBO",
        "DisplayName": "Emily Platt",
        "MiddleName": "Jane",
        "FamilyName": "Platt",
        "Active": true,
        "PrintOnCheckName": "Emily Platt",
        "sparse": false,
        "BillableTime": false,
        "GivenName": "Emily",
        "Id": "55",
        "MetaData": {
          "CreateTime": "2014-09-17T11:21:48-07:00",
          "LastUpdatedTime": "2015-07-01T11:29:40-07:00"
        }
      }
    ],
    "startPosition": 1,
    "maxResults": 1
  },
  "time": "2015-07-24T08:56:55.808-07:00"
}
```

## Read an Employee

Retrieves the details of an Employee object that has been previously created.

### Request

```
GET /v3/company/<realmID>/employee/<employeeId>
```

### Sample Response

Returns the full Employee object as shown in the Sample Object section.

## Full Update an Employee

Use this operation to update any of the writable fields of an existing employee object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL.

### Request

```
POST /v3/company/<realmID>/employee
Content-Type: application/json
```

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String | Unique identifier. *Required for update* |
| **SyncToken** | String | Version number. *Required for update* |

### Sample Request Body

```json
{
  "SyncToken": "0",
  "domain": "QBO",
  "DisplayName": "Bill Miller",
  "PrimaryPhone": {
    "FreeFormNumber": "234-525-1234"
  },
  "PrintOnCheckName": "Bill Lee Miller",
  "FamilyName": "Miller",
  "Active": true,
  "SSN": "XXX-XX-XXXX",
  "PrimaryAddr": {
    "CountrySubDivisionCode": "CA",
    "City": "Middlefield",
    "PostalCode": "93242",
    "Id": "116",
    "Line1": "45 N. Elm Street"
  },
  "sparse": false,
  "BillableTime": false,
  "GivenName": "Bill",
  "Id": "71",
  "MetaData": {
    "CreateTime": "2015-07-24T09:34:35-07:00",
    "LastUpdatedTime": "2015-07-24T09:34:35-07:00"
  }
}
```

### Sample Response

```json
{
  "Employee": {
    "SyncToken": "1",
    "domain": "QBO",
    "DisplayName": "Bill Miller",
    "PrimaryPhone": {
      "FreeFormNumber": "234-525-1234"
    },
    "PrintOnCheckName": "Bill Lee Miller",
    "FamilyName": "Miller",
    "Active": true,
    "SSN": "XXX-XX-XXXX",
    "PrimaryAddr": {
      "CountrySubDivisionCode": "CA",
      "City": "Middlefield",
      "PostalCode": "93242",
      "Id": "116",
      "Line1": "45 N. Elm Street"
    },
    "sparse": false,
    "BillableTime": false,
    "GivenName": "Bill",
    "Id": "71",
    "MetaData": {
      "CreateTime": "2015-07-24T09:34:35-07:00",
      "LastUpdatedTime": "2015-07-24T09:37:39-07:00"
    }
  },
  "time": "2015-07-24T09:37:39.399-07:00"
}
```
