# Exchangerate

Applicable only for those companies that enable multicurrency, the exchangerate resource provides the ability to query and set exchange rates available to the QuickBooks Online company. This entity works in combination with the companycurrency entity and the Currency Center in the QuickBooks Online UI to manage exchange rates for the company.

## The Exchangerate Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **SyncToken** | String | Required for update, read only, system defined | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. |
| **AsOfDate** | Boolean, filterable | Required for update | Date on which this exchange rate was set. |
| **SourceCurrencyCode** | String, filterable | Required for update | The source currency from which the exchange rate is specified. Specify as a three letter string representing the ISO 4217 code for the currency. For example, USD, AUD, EUR, and so on. For example, in the equation 65 INR = 1 USD, INR is the source currency. Exactly 3 chars. |
| **Rate** | Decimal | Required for update | The exchange rate between SourceCurrencyCode and TargetCurrencyCode on the AsOfDate date. |
| **CustomField** | CustomField | Optional | One of, up to three custom fields for the transaction. Available for custom fields so configured for the company. Check Preferences.SalesFormsPrefs.CustomField and Preferences.VendorAndPurchasesPrefs.POCustomField for custom fields currently configured. |
| **TargetCurrencyCode** | String | Optional | The target currency against which the exchange rate is specified. Specify as a three letter string representing the ISO 4217 code for the currency. For example, USD, AUD, EUR, and so on. For example, in the equation 65 INR = 1 USD, USA is the target currency. Exactly 3 chars. |
| **MetaData** | ModificationMetaData, filterable, sortable | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |

## Get an Exchangerate for an Individual Currency Code

- `currencycode` is the desired currency code. Required.
- `yyyy-mm-dd` is the desired effective date. If not specified, today's date is used.

### Returns

Returns the exchangerate object.

### Request URL

```
GET /v3/company/<realmID>/exchangerate?sourcecurrencycode=<currencycode>[&asofdate=<yyyy-mm-dd>]
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```
?sourcecurrencycode=<USA>&asofdate=<yyyy-mm-dd>
```

### Response

```json
{
  "ExchangeRate": {
    "SyncToken": "1",
    "domain": "QBO",
    "AsOfDate": "2015-07-07",
    "SourceCurrencyCode": "EUR",
    "Rate": 2.5,
    "sparse": false,
    "TargetCurrencyCode": "USD",
    "MetaData": {
      "LastUpdatedTime": "2015-07-08T09:24:02-07:00"
    }
  },
  "time": "2015-07-08T09:40:58.146-07:00"
}
```

## Query Exchangerate Objects

### Returns

Returns the results of the query.

### Request URL

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content type: text/plain
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
select * from exchangerate where sourcecurrencycode in ('EUR', 'INR') and asofdate='2015-07-07'
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "ExchangeRate": [
      {
        "SyncToken": "0",
        "AsOfDate": "2015-05-15",
        "SourceCurrencyCode": "INR",
        "Rate": 5,
        "TargetCurrencyCode": "USD",
        "MetaData": {
          "LastUpdatedTime": "2015-07-07T12:38:40-07:00"
        }
      },
      {
        "SyncToken": "0",
        "AsOfDate": "2015-07-07",
        "SourceCurrencyCode": "EUR",
        "Rate": 5,
        "TargetCurrencyCode": "USD",
        "MetaData": {
          "LastUpdatedTime": "2015-07-07T12:40:08-07:00"
        }
      }
    ],
    "maxResults": 2,
    "totalCount": 2
  },
  "time": "2015-07-08T09:19:44.495-07:00"
}
```

## Update an Exchangerate

- SourceCurrencyCode, Rate, and AsOfDate are mandatory fields.
- TargetCurrencyCode defaults to Home Currency if not supplied.
- Setting exchange rate to anything other than 1 for a case where SourceCurrencyCode=TargetCurrencyCode results in the exchange rate set to 1.
- Setting an exchange rate for the home currency, that is, where SourceCurrencyCode is set to the home currency results in a validation error.

### Request Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **SyncToken** | String | Required for update, read only, system defined | Version number of the object. |
| **AsOfDate** | Boolean, filterable | Required for update | Date on which this exchange rate was set. |
| **SourceCurrencyCode** | String, filterable | Required for update | The source currency from which the exchange rate is specified. Exactly 3 chars. |
| **Rate** | Decimal | Required for update | The exchange rate between SourceCurrencyCode and TargetCurrencyCode on the AsOfDate date. |
| **CustomField** | CustomField | Optional | One of, up to three custom fields for the transaction. |
| **TargetCurrencyCode** | String | Optional | The target currency against which the exchange rate is specified. Exactly 3 chars. |
| **MetaData** | ModificationMetaData, filterable, sortable | Optional | Descriptive information about the object. |

### Returns

The exchangerate response body.

### Request URL

```
POST /v3/company/<realmID>/exchangerate
Content type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "SyncToken": "0",
  "AsOfDate": "2015-07-08",
  "SourceCurrencyCode": "INR",
  "Rate": 7,
  "TargetCurrencyCode": "USD",
  "MetaData": {
    "LastUpdatedTime": "2015-07-07T12:38:40-07:00"
  }
}
```

### Response

```json
{
  "ExchangeRate": {
    "SyncToken": "0",
    "domain": "QBO",
    "AsOfDate": "2015-07-08",
    "SourceCurrencyCode": "INR",
    "Rate": 7,
    "sparse": false,
    "TargetCurrencyCode": "USD",
    "MetaData": {
      "LastUpdatedTime": "2015-07-08T09:21:46-07:00"
    }
  },
  "time": "2015-07-08T09:21:46.310-07:00"
}
```
