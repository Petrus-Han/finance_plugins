# Create Basic Requests

> Source: https://developer.intuit.com/app/developer/qbo/docs/get-started/create-a-request

Both the [QuickBooks Online Accounting API](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api) and the [QuickBooks Online Payments API](https://developer.intuit.com/app/developer/qbpayments/docs/learn/explore-the-quickbooks-payments-api) use JSON to send and receive information.

## Data Formats

| API | Request Format | Response Format |
|-----|----------------|-----------------|
| **QuickBooks Online Accounting API** | JSON or XML | JSON or XML |
| **QuickBooks Payments API** | JSON only | JSON only |

---

## Review API Reference Libraries

Check out the API Explorers to see all available entities, resources, and related operations:

- [QuickBooks Online Accounting API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [QuickBooks Payments API Explorer](https://developer.intuit.com/app/developer/qbpayments/docs/api/resources/all-entities/bankaccounts)

---

## Get Base URLs for API Calls

There are different base URLs for each API framework. There are also unique base URLs for sandbox companies (testing environments) and live, customer-facing QuickBooks Online companies.

### QuickBooks Online Accounting API

| Environment | Base URL |
|-------------|----------|
| **Sandbox/Testing** | `https://sandbox-quickbooks.api.intuit.com` |
| **Production** | `https://quickbooks.api.intuit.com` |

### QuickBooks Payments API

| Environment | Base URL |
|-------------|----------|
| **Sandbox/Testing** | `https://sandbox.api.intuit.com/quickbooks/v4/payments` |
| **Production** | `https://api.intuit.com` |

> **Tip**: The payments sandbox company should be attached to a US-based QuickBooks Online sandbox company.

---

## SDK Base URL Configuration

### .NET SDK

```csharp
ServiceContext context = new ServiceContext(appToken, realmId, IntuitServicesType.QBO, oauthValidator);
context.IppConfiguration.BaseUrl.Qbo = "https://sandbox-quickbooks.api.intuit.com/";
```

### Java SDK

```java
Config.setProperty(Config.BASE_URL_QBO, "https://sandbox-quickbooks.api.intuit.com/v3/company");
```

### PHP SDK

Edit the `sdk.config` file to use the new base URL: `https://sandbox-quickbooks.api.intuit.com/`

---

## API Endpoint Formats

Each API entity has a unique endpoint. Send requests to the specific API entities and related operations you need. The base URL is the same for all endpoints, but the entity and resource type varies.

> **Important**: Always set the request's content type to `application/json`.

### QuickBooks Online Accounting API

```
<OPERATION> <baseURL>/v3/company/<realmId>/<entity>?minorversion=<version>
```

### QuickBooks Payments API

```
<OPERATION> <baseURL>/quickbooks/v4/customers/<id>/<entity>
```

---

## Endpoint Examples

### Create an Invoice (Accounting API)

```http
POST https://quickbooks.api.intuit.com/v3/company/4620816365014867780/invoice?minorversion=63
Content-Type: application/json
```

### Create a Card (Payments API)

```http
POST https://api.intuit.com/quickbooks/v4/customers/<id>/cards
Content-Type: application/json
```

### Create a Charge (Payments Sandbox)

```http
POST https://sandbox.api.intuit.com/quickbooks/v4/payments/charges
Content-Type: application/json
```

---

## Basic Request Format

Calling our APIs involves request and response JSON pairs.

### Example: Create a Charge

```json
{
   "amount": "10.55",
   "card": {
      "expYear": "2020",
      "expMonth": "02",
      "address": {
         "region": "CA",
         "postalCode": "94086",
         "streetAddress": "1130 Kifer Rd",
         "country": "US",
         "city": "Sunnyvale"
      },
      "name": "emulate=0",
      "cvc": "123",
      "number": "4111111111111111"
   },
   "currency": "USD",
   "context": {
      "mobile": "false",
      "isEcommerce": "true"
   }
}
```

### Request Field Notes

- Each API entity has unique field:value pairs
- Some fields are **required**, some are **optional**
- Always review the API Explorer to see what's required
- The `isEcommerce` field identifies digital transactions

---

## Basic Response Format

### Example: Charge Response

```json
{
   "created": "2018-01-31T18:48:25Z",
   "status": "CAPTURED",
   "amount": "10.55",
   "currency": "USD",
   "card": {
      "number": "xxxxxxxxxxxx1111",
      "name": "emulate=0",
      "address": {
         "city": "Sunnyvale",
         "region": "CA",
         "country": "US",
         "streetAddress": "1130 Kifer Rd",
         "postalCode": "94086"
      },
      "cardType": "Visa",
      "expMonth": "02",
      "expYear": "2020",
      "cvc": "xxx"
   },
   "avsStreet": "Pass",
   "avsZip": "Pass",
   "cardSecurityCodeMatch": "NotAvailable",
   "id": "EAQX3720TN5J",
   "context": {
      "mobile": false,
      "deviceInfo": {},
      "recurring": false,
      "isEcommerce": true
   },
   "authCode": "139111"
}
```

### Response Field Notes

- `status`: Transaction status (e.g., "CAPTURED")
- `id`: Unique transaction identifier
- `authCode`: Authorization code from the payment processor
- Card number is masked for security (`xxxxxxxxxxxx1111`)

---

## Mercury Integration Notes

For Mercury bank transaction sync, use the **Accounting API** endpoints:

| Mercury Action | API Endpoint | Example |
|----------------|--------------|---------|
| Record expense | `POST /v3/company/{realmId}/purchase` | Outgoing payment |
| Record deposit | `POST /v3/company/{realmId}/deposit` | Incoming payment |
| Record transfer | `POST /v3/company/{realmId}/transfer` | Between accounts |

See [API Reference](../api-reference/) for detailed entity documentation.
