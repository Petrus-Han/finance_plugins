# QuickBooks Payments API Documentation

> **Source**: Compiled from https://developer.intuit.com/app/developer/qbpayments/docs/api/ (2026-01-14)

## Overview

QuickBooks Payments API is a RESTful API that enables payment processing for credit cards, debit cards, bank accounts (ACH/eChecks), and other payment methods. This API is separate from the QuickBooks Online Accounting API and focuses specifically on payment transaction processing.

**Key Difference**:
- **Accounting API**: Manages accounting data (invoices, customers, vendors, etc.)
- **Payments API**: Processes actual payment transactions (charges, refunds, etc.)

## Authentication

### OAuth 2.0 Flow

QuickBooks Payments uses OAuth 2.0 for secure authentication.

**Setup Steps**:
1. Register application at https://developer.intuit.com
2. Create QuickBooks Payments app
3. Select "QuickBooks Payments" scope
4. Obtain Client ID and Client Secret
5. Configure Redirect URI

**OAuth Endpoints**:
- Authorization URL: `https://appcenter.intuit.com/connect/oauth2`
- Token URL: `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer`

**Required Scopes**:
- `com.intuit.quickbooks.payment` - Payments API access

**Important Notes**:
- Payments API is **US only**
- Requires separate merchant account setup
- Different from Accounting API scope

**Authentication Header**:
```
Authorization: Bearer <access_token>
```

---

## Base URL

### Production
```
https://api.intuit.com/quickbooks/v4/payments
```

### Sandbox
```
https://sandbox.api.intuit.com/quickbooks/v4/payments
```

---

## Core Concepts

### Tokenization

For security, the Payments API uses tokenization:
1. Sensitive payment data (card number, bank account) is sent to `/tokens` endpoint
2. API returns a secure token (unique identifier)
3. Token is used for subsequent payment operations
4. Original sensitive data is never stored or transmitted again

**Benefits**:
- PCI DSS compliance
- Reduced security risk
- No storage of sensitive payment data

---

## Core Endpoints

### 1. Tokens

#### Create Payment Token
```
POST /tokens
```

**Purpose**: Tokenize credit card or bank account information for secure storage.

**Request Body (Credit Card)**:
```json
{
  "card": {
    "number": "4111111111111111",
    "expMonth": "12",
    "expYear": "2026",
    "cvc": "123",
    "name": "John Doe",
    "address": {
      "streetAddress": "123 Main St",
      "city": "San Francisco",
      "region": "CA",
      "country": "US",
      "postalCode": "94102"
    }
  }
}
```

**Request Body (Bank Account)**:
```json
{
  "bankAccount": {
    "routingNumber": "322079353",
    "accountNumber": "1234567890",
    "accountType": "PERSONAL_CHECKING",
    "name": "John Doe"
  }
}
```

**Response**:
```json
{
  "value": "emV5J0V3YQUATDFyEZIckr87t6qQtfJnIxYjY0ZC00",
  "createdAt": "2026-01-14T10:30:00Z"
}
```

**Token Properties**:
- Single use only (for charges)
- Expires after 15 minutes if not used
- Cannot be retrieved or reused

---

### 2. Charges

#### Create Charge
```
POST /charges
```

**Purpose**: Process a payment using a token.

**Request Body**:
```json
{
  "amount": "10.50",
  "currency": "USD",
  "token": "emV5J0V3YQUATDFyEZIckr87t6qQtfJnIxYjY0ZC00",
  "context": {
    "mobile": false,
    "isEcommerce": true
  },
  "capture": true,
  "description": "Payment for Invoice #1234",
  "customer": {
    "id": "ABC123"
  }
}
```

**Request Parameters**:
- `amount` (required): Amount to charge (decimal string)
- `currency` (required): Currency code (USD only for US)
- `token` (required): Payment token from /tokens endpoint
- `capture` (optional): Auto-capture payment (default: true)
- `description` (optional): Transaction description
- `context` (required): Transaction context

**Response**:
```json
{
  "id": "ECH123456789",
  "created": "2026-01-14T10:35:00Z",
  "status": "CAPTURED",
  "amount": "10.50",
  "currency": "USD",
  "authCode": "123456",
  "cardSecurityCodeMatch": "MATCHED",
  "avsStreetMatch": "MATCHED",
  "avsZipMatch": "MATCHED",
  "card": {
    "number": "xxxxxxxxxxxx1111",
    "name": "John Doe",
    "cardType": "Visa"
  }
}
```

**Charge Status**:
- `AUTHORIZED`: Payment authorized but not captured
- `CAPTURED`: Payment successfully captured
- `SETTLED`: Payment settled to merchant account
- `VOIDED`: Payment voided before settlement
- `DECLINED`: Payment declined

#### Get Charge
```
GET /charges/{chargeId}
```

**Purpose**: Retrieve details of a specific charge.

**Response**: Same as Create Charge response

---

### 3. Bank Accounts

#### Create Bank Account
```
POST /customers/{customerId}/bank-accounts
```

**Purpose**: Create a reusable bank account for a customer.

**Request Body**:
```json
{
  "routingNumber": "322079353",
  "accountNumber": "1234567890",
  "accountType": "PERSONAL_CHECKING",
  "name": "John Doe",
  "phone": "555-1234"
}
```

**Account Types**:
- `PERSONAL_CHECKING`
- `PERSONAL_SAVINGS`
- `BUSINESS_CHECKING`
- `BUSINESS_SAVINGS`

**Response**:
```json
{
  "id": "BA_1234567890",
  "created": "2026-01-14T10:40:00Z",
  "routingNumber": "322079353",
  "accountNumber": "xxxxxxxxxxxx7890",
  "accountType": "PERSONAL_CHECKING",
  "name": "John Doe",
  "phone": "555-1234"
}
```

#### Get Bank Account
```
GET /customers/{customerId}/bank-accounts/{bankAccountId}
```

**Purpose**: Retrieve a specific bank account.

#### List Bank Accounts
```
GET /customers/{customerId}/bank-accounts
```

**Purpose**: List all bank accounts for a customer.

**Response**:
```json
[
  {
    "id": "BA_1234567890",
    "routingNumber": "322079353",
    "accountNumber": "xxxxxxxxxxxx7890",
    "accountType": "PERSONAL_CHECKING",
    "name": "John Doe"
  }
]
```

#### Delete Bank Account
```
DELETE /customers/{customerId}/bank-accounts/{bankAccountId}
```

**Purpose**: Remove a bank account from a customer.

---

### 4. Cards

#### Create Card
```
POST /customers/{customerId}/cards
```

**Purpose**: Create a reusable credit/debit card for a customer.

**Request Body**:
```json
{
  "number": "4111111111111111",
  "expMonth": "12",
  "expYear": "2026",
  "name": "John Doe",
  "address": {
    "streetAddress": "123 Main St",
    "city": "San Francisco",
    "region": "CA",
    "country": "US",
    "postalCode": "94102"
  },
  "commercialCardCode": "L2",
  "cvc": "123"
}
```

**Response**:
```json
{
  "id": "CC_1234567890",
  "created": "2026-01-14T10:45:00Z",
  "number": "xxxxxxxxxxxx1111",
  "expMonth": "12",
  "expYear": "2026",
  "name": "John Doe",
  "cardType": "Visa",
  "address": {
    "streetAddress": "123 Main St",
    "city": "San Francisco",
    "region": "CA",
    "country": "US",
    "postalCode": "94102"
  }
}
```

#### Get Card
```
GET /customers/{customerId}/cards/{cardId}
```

#### List Cards
```
GET /customers/{customerId}/cards
```

#### Delete Card
```
DELETE /customers/{customerId}/cards/{cardId}
```

---

### 5. Refunds

#### Create Refund
```
POST /charges/{chargeId}/refunds
```

**Purpose**: Refund a previously captured charge.

**Request Body**:
```json
{
  "amount": "10.50",
  "description": "Refund for order #1234"
}
```

**Request Parameters**:
- `amount` (optional): Amount to refund (defaults to full charge amount)
- `description` (optional): Reason for refund

**Response**:
```json
{
  "id": "ERF123456789",
  "created": "2026-01-14T11:00:00Z",
  "status": "ISSUED",
  "amount": "10.50",
  "description": "Refund for order #1234",
  "chargeId": "ECH123456789"
}
```

**Refund Status**:
- `PENDING`: Refund initiated
- `ISSUED`: Refund processed
- `SETTLED`: Refund settled to customer

#### Get Refund
```
GET /charges/{chargeId}/refunds/{refundId}
```

---

## Payment Methods

### Supported Payment Types

1. **Credit Cards**
   - Visa
   - Mastercard
   - American Express
   - Discover

2. **Debit Cards**
   - All major networks

3. **Bank Accounts (ACH)**
   - Personal Checking
   - Personal Savings
   - Business Checking
   - Business Savings

4. **eChecks**
   - Same as bank account processing

---

## Error Handling

### Common Error Codes

| Code | Message | Description |
|------|---------|-------------|
| `PMT-1000` | Invalid token | Token expired or invalid |
| `PMT-2000` | Insufficient funds | Customer has insufficient funds |
| `PMT-3000` | Card declined | Card was declined by issuer |
| `PMT-4000` | Invalid routing number | Bank routing number is invalid |
| `PMT-5000` | Duplicate transaction | Transaction already processed |
| `PMT-6000` | Invalid amount | Amount must be greater than 0 |

### Error Response Format

```json
{
  "errors": [
    {
      "code": "PMT-3000",
      "detail": "Card declined by issuer",
      "infoLink": "https://developer.intuit.com/errors/PMT-3000"
    }
  ]
}
```

---

## Rate Limiting

**Limits**:
- Production: 100 requests per minute per merchant
- Sandbox: 50 requests per minute

**Rate Limit Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1610640000
```

---

## Security Best Practices

1. **Never Store Card Data**
   - Use tokenization for all card transactions
   - Tokens are single-use only

2. **Use HTTPS Only**
   - All API calls must use HTTPS
   - HTTP requests will be rejected

3. **Validate Webhooks**
   - Use webhook signatures to verify authenticity
   - Check timestamp to prevent replay attacks

4. **PCI Compliance**
   - Tokenization keeps you PCI DSS compliant
   - No sensitive card data touches your servers

5. **Secure OAuth Tokens**
   - Store access tokens securely
   - Refresh before expiration
   - Never expose in client-side code

---

## Testing

### Sandbox Environment

**Base URL**:
```
https://sandbox.api.intuit.com/quickbooks/v4/payments
```

### Test Card Numbers

| Card Type | Number | CVC | Expiry |
|-----------|--------|-----|--------|
| Visa | 4111111111111111 | 123 | Any future date |
| Mastercard | 5105105105105100 | 123 | Any future date |
| Amex | 378282246310005 | 1234 | Any future date |
| Discover | 6011111111111117 | 123 | Any future date |

### Test Bank Account

- Routing Number: `322079353`
- Account Number: Any 10-17 digits

### Test Scenarios

1. **Successful Charge**: Use test card numbers above
2. **Declined Card**: Use amount `5.01`
3. **Insufficient Funds**: Use amount `5.02`
4. **Invalid Card**: Use card number `4000000000000002`

---

## Webhooks (Future Feature)

QuickBooks Payments supports webhooks for real-time event notifications:

**Supported Events**:
- `charge.created`
- `charge.captured`
- `charge.failed`
- `refund.created`
- `refund.issued`

**Webhook Payload**:
```json
{
  "eventType": "charge.captured",
  "eventId": "evt_123456",
  "timestamp": "2026-01-14T12:00:00Z",
  "data": {
    "id": "ECH123456789",
    "amount": "10.50",
    "status": "CAPTURED"
  }
}
```

---

## Integration Examples

### Example 1: Charge a Credit Card

```python
# Step 1: Create token
token_response = requests.post(
    "https://api.intuit.com/quickbooks/v4/payments/tokens",
    headers={"Authorization": f"Bearer {access_token}"},
    json={
        "card": {
            "number": "4111111111111111",
            "expMonth": "12",
            "expYear": "2026",
            "cvc": "123",
            "name": "John Doe"
        }
    }
)
token = token_response.json()["value"]

# Step 2: Create charge
charge_response = requests.post(
    "https://api.intuit.com/quickbooks/v4/payments/charges",
    headers={"Authorization": f"Bearer {access_token}"},
    json={
        "amount": "10.50",
        "currency": "USD",
        "token": token,
        "context": {"mobile": False, "isEcommerce": True}
    }
)
charge = charge_response.json()
```

### Example 2: Charge a Bank Account

```python
# Step 1: Create token for bank account
token_response = requests.post(
    "https://api.intuit.com/quickbooks/v4/payments/tokens",
    headers={"Authorization": f"Bearer {access_token}"},
    json={
        "bankAccount": {
            "routingNumber": "322079353",
            "accountNumber": "1234567890",
            "accountType": "PERSONAL_CHECKING",
            "name": "John Doe"
        }
    }
)
token = token_response.json()["value"]

# Step 2: Create charge (eCheck)
charge_response = requests.post(
    "https://api.intuit.com/quickbooks/v4/payments/charges",
    headers={"Authorization": f"Bearer {access_token}"},
    json={
        "amount": "100.00",
        "currency": "USD",
        "token": token,
        "context": {"mobile": False, "isEcommerce": False}
    }
)
charge = charge_response.json()
```

### Example 3: Process Refund

```python
# Refund a charge
refund_response = requests.post(
    f"https://api.intuit.com/quickbooks/v4/payments/charges/{charge_id}/refunds",
    headers={"Authorization": f"Bearer {access_token}"},
    json={
        "amount": "10.50",
        "description": "Customer requested refund"
    }
)
refund = refund_response.json()
```

---

## Resources

- [Official Payments API Documentation](https://developer.intuit.com/app/developer/qbpayments/docs/api/)
- [Getting Started Guide](https://developer.intuit.com/app/developer/qbpayments/docs/get-started)
- [Charges API Reference](https://developer.intuit.com/app/developer/qbpayments/docs/api/resources/all-entities/charges)
- [Bank Accounts API Reference](https://developer.intuit.com/app/developer/qbpayments/docs/api/resources/all-entities/bankaccounts)
- [Postman Collection](https://documenter.getpostman.com/view/3967924/RW1dEx9e)
- [PHP Payments SDK](https://github.com/intuit/PHP-Payments-SDK)

---

## Comparison: Payments API vs Accounting API

| Feature | Payments API | Accounting API |
|---------|--------------|----------------|
| **Base URL** | `api.intuit.com/quickbooks/v4/payments` | `quickbooks.api.intuit.com/v3/company/{realmId}` |
| **OAuth Scope** | `com.intuit.quickbooks.payment` | `com.intuit.quickbooks.accounting` |
| **Purpose** | Process payment transactions | Manage accounting data |
| **Use Cases** | Charge cards, ACH, refunds | Invoices, bills, reports |
| **Availability** | US only | Global |
| **Requires** | Merchant account | QuickBooks company |

---

## Next Steps

1. Register for QuickBooks Payments API access
2. Set up merchant account
3. Configure OAuth application with payment scope
4. Test in sandbox environment
5. Implement tokenization for payment security
6. Process test transactions
7. Go live in production

---

**Last Updated**: 2026-01-14
**API Version**: v4
