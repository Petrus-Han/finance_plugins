# Miscellaneous APIs

Base URL: `https://api.mercury.com/api/v1`

This document covers smaller API endpoints: Categories, Credit, Organization, Statements, and Send Money Requests.

---

## Categories API

Custom expense categories for organizing transactions.

### GET /categories

List all custom expense categories for the organization.

```bash
curl -X GET "https://api.mercury.com/api/v1/categories" \
  -H "Authorization: Bearer <token>"
```

#### Response

```json
{
  "categories": [
    {
      "id": "cat_123",
      "name": "Software & Tools",
      "color": "#3B82F6",
      "createdAt": "2024-01-01T00:00:00Z"
    },
    {
      "id": "cat_456",
      "name": "Marketing",
      "color": "#10B981",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

> **Note:** These are custom categories, different from Mercury's built-in categories.

---

## Credit API

Manage credit accounts and credit lines.

### GET /credit

List all credit accounts for the organization.

```bash
curl -X GET "https://api.mercury.com/api/v1/credit" \
  -H "Authorization: Bearer <token>"
```

#### Response

```json
{
  "creditAccounts": [
    {
      "id": "credit_123",
      "name": "Mercury Credit Line",
      "status": "active",
      "creditLimit": 100000.00,
      "availableCredit": 75000.00,
      "currentBalance": 25000.00,
      "apr": 12.99,
      "minimumPayment": 500.00,
      "paymentDueDate": "2024-02-01",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Credit account ID |
| name | string | Account name |
| status | string | Account status |
| creditLimit | number | Total credit limit |
| availableCredit | number | Available to spend |
| currentBalance | number | Current outstanding balance |
| apr | number | Annual Percentage Rate |
| minimumPayment | number | Minimum payment due |
| paymentDueDate | string | Next payment due date |

---

## Organization API

Retrieve organization information.

### GET /organization

Get organization details including EIN, legal business name, and DBAs.

```bash
curl -X GET "https://api.mercury.com/api/v1/organization" \
  -H "Authorization: Bearer <token>"
```

#### Response

```json
{
  "id": "org_123",
  "legalName": "Acme Corporation",
  "dba": ["Acme", "Acme Corp"],
  "ein": "12-3456789",
  "entityType": "corporation",
  "address": {
    "address1": "123 Main St",
    "city": "San Francisco",
    "region": "CA",
    "postalCode": "94102",
    "country": "US"
  },
  "phone": "+1-555-123-4567",
  "website": "https://acme.com",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Organization ID |
| legalName | string | Legal business name |
| dba | array | Doing Business As names |
| ein | string | Employer Identification Number |
| entityType | string | Business entity type |
| address | object | Registered business address |
| phone | string | Business phone |
| website | string | Business website |

---

## Statements API

Download account statements.

### GET /statement/{statementId}/pdf

Download an account statement as PDF.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| statementId | string | Yes | Statement ID |

```bash
curl -X GET "https://api.mercury.com/api/v1/statement/{statementId}/pdf" \
  -H "Authorization: Bearer <token>" \
  -o statement.pdf
```

#### Response

Binary PDF file.

---

## Send Money Requests API

Track payment requests awaiting approval.

### GET /send-money-request/{requestId}

Get details for a send money approval request.

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| requestId | string | Yes | Request ID |

```bash
curl -X GET "https://api.mercury.com/api/v1/send-money-request/{requestId}" \
  -H "Authorization: Bearer <token>"
```

#### Response

```json
{
  "id": "smr_123",
  "accountId": "account_123",
  "recipientId": "recipient_456",
  "recipientName": "Acme Corp",
  "amount": 5000.00,
  "paymentMethod": "ach",
  "status": "pending_approval",
  "requestedBy": "user_789",
  "requestedAt": "2024-01-15T10:00:00Z",
  "note": "Invoice #1234 payment",
  "approvals": [
    {
      "userId": "user_001",
      "status": "approved",
      "approvedAt": "2024-01-15T10:30:00Z"
    }
  ],
  "requiredApprovals": 2
}
```

### Request Statuses

| Status | Description |
|--------|-------------|
| pending_approval | Awaiting admin approval |
| approved | All approvals received, processing |
| rejected | Request was rejected |
| completed | Payment sent successfully |
| failed | Payment failed after approval |
