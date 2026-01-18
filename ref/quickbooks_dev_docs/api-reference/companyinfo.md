# CompanyInfo

The CompanyInfo object contains basic company information. In QuickBooks, company info and preferences are displayed in the same place under preferences, so it may be confusing to figure out from user interface which fields may belong to this object. But in general, properties such as company addresses or name are considered company information. Some attributes may exist in both CompanyInfo and Preferences objects.

## The CompanyInfo Object

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String, read only, filterable, sortable | Unique identifier for this object. Sort order is ASC by default. |
| **SyncToken** | String, read only | Version number of the object. *Required for update* |
| **CompanyName** | String (max 1024 chars) | The name of the company. *Required for update* |
| **CompanyAddr** | PhysicalAddress | Company Address as described in preference. *Required for update* |
| **LegalAddr** | PhysicalAddress | Legal Address given to the government for any government communication. |
| **SupportedLanguages** | String | Comma separated list of languages. |
| **Country** | String | Country name to which the company belongs for financial calculations. |
| **Email** | EmailAddress (max 100 chars) | Default email address. |
| **WebAddr** | WebSiteAddress (max 1000 chars) | Website address. |
| **NameValue** | NameValue[] | Any other preference not covered with the standard set of attributes. See Data Services Extensions below for special reserved name/value pairs. |
| **FiscalYearStartMonth** | MonthEnum | The start month of fiscal year. |
| **CustomerCommunicationAddr** | PhysicalAddress | Address of the company as given to their customer. |
| **PrimaryPhone** | TelephoneNumber | Primary phone number. |
| **LegalName** | String (max 1024 chars) | The legal name of the company. |
| **EmployerId** | String | If your QuickBooks company has defined an EIN in company settings, this value is returned. |
| **MetaData** | ModificationMetaData | Descriptive information about the object. Read only. |
| **CompanyStartDate** | DateTime, read only | DateTime when company file was created. Same as Metadata.CreateTime. |

### Data Services Extensions (NameValue pairs)

The following are reserved name/value pairs available in the NameValue array:

| Name | Description |
|------|-------------|
| **NeoEnabled** | Whether the company has new experience enabled |
| **IndustryType** | The industry type of the company |
| **IndustryCode** | The NAICS industry code |
| **SubscriptionStatus** | The subscription status (e.g., PAID) |
| **OfferingSku** | The QuickBooks edition (e.g., QuickBooks Online Plus) |
| **PayrollFeature** | Whether payroll is enabled (true/false) |
| **AccountantFeature** | Whether accountant features are enabled |
| **IsQbdtMigrated** | Whether migrated from QuickBooks Desktop |
| **MigrationDate** | The date of migration from QBD |
| **QBOIndustryType** | The QuickBooks Online industry type |
| **ItemCategoriesFeature** | Whether categories are enabled for items |

### Sample Object

```json
{
  "CompanyInfo": {
    "SyncToken": "4",
    "domain": "QBO",
    "LegalAddr": {
      "City": "Mountain View",
      "Country": "US",
      "Line1": "2500 Garcia Ave",
      "PostalCode": "94043",
      "CountrySubDivisionCode": "CA",
      "Id": "1"
    },
    "SupportedLanguages": "en",
    "CompanyName": "Larry's Bakery",
    "Country": "US",
    "CompanyAddr": {
      "City": "Mountain View",
      "Country": "US",
      "Line1": "2500 Garcia Ave",
      "PostalCode": "94043",
      "CountrySubDivisionCode": "CA",
      "Id": "1"
    },
    "sparse": false,
    "Id": "1",
    "WebAddr": {},
    "FiscalYearStartMonth": "January",
    "CustomerCommunicationAddr": {
      "City": "Mountain View",
      "Country": "US",
      "Line1": "2500 Garcia Ave",
      "PostalCode": "94043",
      "CountrySubDivisionCode": "CA",
      "Id": "1"
    },
    "PrimaryPhone": {
      "FreeFormNumber": "(650)944-4444"
    },
    "LegalName": "Larry's Bakery",
    "CompanyStartDate": "2015-06-05",
    "EmployerId": "123456789",
    "Email": {
      "Address": "donotreply@intuit.com"
    },
    "NameValue": [
      {
        "Name": "NeoEnabled",
        "Value": "true"
      },
      {
        "Name": "IndustryType",
        "Value": "Bread and Bakery Product Manufacturing"
      },
      {
        "Name": "IndustryCode",
        "Value": "31181"
      },
      {
        "Name": "SubscriptionStatus",
        "Value": "PAID"
      },
      {
        "Name": "OfferingSku",
        "Value": "QuickBooks Online Plus"
      },
      {
        "Name": "PayrollFeature",
        "Value": "true"
      },
      {
        "Name": "AccountantFeature",
        "Value": "false"
      }
    ],
    "MetaData": {
      "CreateTime": "2015-06-05T13:55:54-07:00",
      "LastUpdatedTime": "2015-07-06T08:51:50-07:00"
    }
  },
  "time": "2015-07-10T09:38:58.155-07:00"
}
```

## Query CompanyInfo

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: text/plain
```

**Production Base URL:** `https://quickbooks.api.intuit.com`
**Sandbox Base URL:** `https://sandbox-quickbooks.api.intuit.com`

### Sample Query

```sql
select * from CompanyInfo
```

### Sample Response

Returns the CompanyInfo object as shown in the Sample Object section.

## Read CompanyInfo

Retrieves the details of the CompanyInfo object.

### Request

```
GET /v3/company/<realmID>/companyinfo/<realmID>
```

### Sample Response

Returns the full CompanyInfo object as shown in the Sample Object section.

## Full Update CompanyInfo

Available with minor version 11. Use this operation to update any of the writable fields of the companyinfo object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL.

### Request

```
POST /v3/company/<realmID>/companyinfo
Content-Type: application/json
```

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **SyncToken** | String | Version number. *Required for update* |
| **CompanyName** | String | The name of the company. *Required for update* |
| **CompanyAddr** | PhysicalAddress | Company Address. *Required for update* |

### Sample Request Body

The full request body should include all fields from the CompanyInfo object returned from a Read operation, with the fields you want to update modified.

### Sample Response

Returns the updated CompanyInfo object with incremented SyncToken.

## Sparse Update CompanyInfo

Sparse updating provides the ability to update a subset of properties for a given object; only elements specified in the request are updated. Missing elements are left untouched. Available with minor version 11.

### Request

```
POST /v3/company/<realmID>/companyinfo
Content-Type: application/json
```

### Sample Request Body

```json
{
  "SyncToken": "3",
  "CompanyName": "Larry's Bakery",
  "CompanyAddr": {
    "City": "Mountain View",
    "Country": "US",
    "Line1": "2500 Garcia Ave",
    "PostalCode": "94043",
    "CountrySubDivisionCode": "CA",
    "Id": "1"
  },
  "sparse": true,
  "LegalName": "Larry Smith's Bakery",
  "Id": "1"
}
```

### Sample Response

```json
{
  "CompanyInfo": {
    "SyncToken": "4",
    "domain": "QBO",
    "LegalAddr": {
      "City": "Mountain View",
      "Country": "US",
      "Line1": "2500 Garcia Ave",
      "PostalCode": "94043",
      "CountrySubDivisionCode": "CA",
      "Id": "1"
    },
    "SupportedLanguages": "en",
    "CompanyName": "Larry's Bakery",
    "Country": "US",
    "CompanyAddr": {
      "City": "Mountain View",
      "Country": "US",
      "Line1": "2500 Garcia Ave",
      "PostalCode": "94043",
      "CountrySubDivisionCode": "CA",
      "Id": "1"
    },
    "sparse": false,
    "Id": "1",
    "FiscalYearStartMonth": "January",
    "PrimaryPhone": {
      "FreeFormNumber": "(650)944-4444"
    },
    "LegalName": "Larry Smith's Bakery",
    "CompanyStartDate": "2015-06-05",
    "EmployerId": "123456789",
    "Email": {
      "Address": "donotreply@intuit.com"
    },
    "MetaData": {
      "CreateTime": "2015-06-05T13:55:54-07:00",
      "LastUpdatedTime": "2015-07-06T08:51:50-07:00"
    }
  },
  "time": "2015-07-10T09:38:58.155-07:00"
}
```

## Useful NameValue Checks

### Check if Payroll is Enabled

```javascript
// Look for this in the NameValue array:
{ "Name": "PayrollFeature", "Value": "true" }
// Payroll is enabled if Value is "true"
```

### Check if Categories are Enabled

```javascript
// Look for this in the NameValue array:
{ "Name": "ItemCategoriesFeature", "Value": "true" }
// Categories are enabled if Value is "true"
```
