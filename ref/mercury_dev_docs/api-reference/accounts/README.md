# Accounts API

Base URL: `https://api.mercury.com/api/v1`

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts` | Get all accounts |
| GET | `/account/{accountId}` | Get account by ID |
| GET | `/account/{accountId}/cards` | Get cards for account |
| GET | `/account/{accountId}/statements` | Get account statements |
| GET | `/account/{accountId}/transaction/{transactionId}` | Get transaction by ID |
| GET | `/account/{accountId}/transactions` | List account transactions |
| POST | `/account/{accountId}/transactions` | Create a transaction |
| POST | `/account/{accountId}/request-send-money` | Request to send money |
| POST | `/transfer` | Create an internal transfer |

---

## GET /accounts

Get all accounts for the authenticated organization.

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/accounts" \
  -H "Authorization: Bearer <token>"
```

### Response

```json
{
  "accounts": [
    {
      "id": "account_123",
      "name": "Checking Account",
      "type": "checking",
      "status": "active",
      "availableBalance": 50000.00,
      "currentBalance": 50000.00,
      "accountNumber": "****1234",
      "routingNumber": "123456789",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique account identifier |
| name | string | Account display name |
| type | string | Account type: `checking`, `savings` |
| status | string | Account status: `active`, `closed` |
| availableBalance | number | Available balance for transactions |
| currentBalance | number | Current balance including pending |
| accountNumber | string | Masked account number |
| routingNumber | string | Bank routing number |
| createdAt | string | ISO 8601 timestamp |

---

## GET /account/{accountId}

Get details for a specific account.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| accountId | string | Yes | Account ID |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/account/{accountId}" \
  -H "Authorization: Bearer <token>"
```

### Response

Same structure as individual account in `/accounts` response.

---

## GET /account/{accountId}/cards

Retrieve all debit and credit cards associated with a specific account.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| accountId | string | Yes | Account ID |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/account/{accountId}/cards" \
  -H "Authorization: Bearer <token>"
```

### Response

```json
{
  "cards": [
    {
      "id": "card_123",
      "type": "debit",
      "status": "active",
      "lastFourDigits": "1234",
      "expirationMonth": 12,
      "expirationYear": 2026,
      "cardholderName": "John Doe",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

## GET /account/{accountId}/statements

Retrieve monthly statements for a specific account. Supports date range filtering.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| accountId | string | Yes | Account ID |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start | string | No | Start date (YYYY-MM-DD) |
| end | string | No | End date (YYYY-MM-DD) |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/account/{accountId}/statements?start=2024-01-01&end=2024-12-31" \
  -H "Authorization: Bearer <token>"
```

### Response

```json
{
  "statements": [
    {
      "id": "stmt_123",
      "accountId": "account_123",
      "month": "2024-01",
      "startDate": "2024-01-01",
      "endDate": "2024-01-31",
      "openingBalance": 45000.00,
      "closingBalance": 50000.00,
      "createdAt": "2024-02-01T00:00:00Z"
    }
  ]
}
```

---

## GET /account/{accountId}/transaction/{transactionId}

Get details for a specific transaction.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| accountId | string | Yes | Account ID |
| transactionId | string | Yes | Transaction ID |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/account/{accountId}/transaction/{transactionId}" \
  -H "Authorization: Bearer <token>"
```

---

## GET /account/{accountId}/transactions

List all transactions for a specific account.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| accountId | string | Yes | Account ID |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Max results (default: 50) |
| offset | integer | No | Pagination offset |
| start | string | No | Start date (YYYY-MM-DD) |
| end | string | No | End date (YYYY-MM-DD) |
| status | string | No | Filter by status |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/account/{accountId}/transactions?limit=50" \
  -H "Authorization: Bearer <token>"
```

---

## POST /account/{accountId}/transactions

Create a transaction (send money). May require approval based on organization policies.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| accountId | string | Yes | Source account ID |

### Request Body

```json
{
  "recipientId": "recipient_123",
  "amount": 1000.00,
  "paymentMethod": "ach",
  "idempotencyKey": "unique_key_123",
  "note": "Invoice payment"
}
```

### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| recipientId | string | Yes | Recipient ID |
| amount | number | Yes | Amount in USD |
| paymentMethod | string | Yes | `ach`, `wire`, `check` |
| idempotencyKey | string | Yes | Unique key to prevent duplicates |
| note | string | No | Transaction memo |

### Request

```bash
curl -X POST "https://api.mercury.com/api/v1/account/{accountId}/transactions" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"recipientId": "recipient_123", "amount": 1000.00, "paymentMethod": "ach", "idempotencyKey": "unique_key_123"}'
```

---

## POST /account/{accountId}/request-send-money

Create a payment request that may require approval based on your organization's payment policies. Use this endpoint when you want admin approval before the payment is processed.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| accountId | string | Yes | Source account ID |

### Request Body

Same as POST `/account/{accountId}/transactions`

### Notes

- Does NOT require IP whitelist
- Payment will be queued for admin approval
- Use `RequestSendMoney` scope for custom tokens

---

## POST /transfer

Transfer funds between two accounts within the same organization. Creates paired debit and credit transactions.

### Request Body

```json
{
  "fromAccountId": "account_123",
  "toAccountId": "account_456",
  "amount": 5000.00,
  "idempotencyKey": "transfer_unique_key"
}
```

### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| fromAccountId | string | Yes | Source account ID |
| toAccountId | string | Yes | Destination account ID |
| amount | number | Yes | Amount in USD |
| idempotencyKey | string | Yes | Unique key to prevent duplicates |

### Request

```bash
curl -X POST "https://api.mercury.com/api/v1/transfer" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"fromAccountId": "account_123", "toAccountId": "account_456", "amount": 5000.00, "idempotencyKey": "transfer_123"}'
```

### Notes

- Requires `SendMoney` write scope
- Both accounts must belong to the same organization
