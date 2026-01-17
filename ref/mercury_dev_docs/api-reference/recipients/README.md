# Recipients API

Base URL: `https://api.mercury.com/api/v1`

Recipients are payees that you can send money to. You must create a recipient before initiating a payment.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recipients` | Get all recipients |
| GET | `/recipient/{recipientId}` | Get recipient by ID |
| POST | `/recipients` | Add a new recipient |
| POST | `/recipient/{recipientId}` | Update recipient |
| POST | `/recipient/{recipientId}/attachment` | Upload recipient attachment |
| GET | `/recipient/{recipientId}/attachments` | List recipient attachments |

---

## GET /recipients

Retrieve a paginated list of all recipients.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Max results (default: 50) |
| start_after | string | No | Cursor for pagination |
| end_before | string | No | Cursor for backward pagination |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/recipients?limit=50" \
  -H "Authorization: Bearer <token>"
```

### Response

```json
{
  "recipients": [
    {
      "id": "recipient_123",
      "name": "Acme Corp",
      "status": "active",
      "emails": ["payments@acme.com"],
      "paymentMethod": "ach",
      "electronicRoutingInfo": {
        "accountNumber": "****5678",
        "routingNumber": "123456789",
        "bankName": "Chase Bank",
        "accountType": "checking"
      },
      "address": {
        "address1": "123 Main St",
        "city": "San Francisco",
        "region": "CA",
        "postalCode": "94102",
        "country": "US"
      },
      "attachments": [
        {
          "id": "att_123",
          "fileName": "W9.pdf",
          "taxFormType": "W9",
          "uploadedAt": "2024-01-01T00:00:00Z",
          "presignedUrl": "https://..."
        }
      ],
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ],
  "hasMore": false
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique recipient ID |
| name | string | Recipient display name |
| status | string | `active`, `inactive` |
| emails | array | Contact email addresses |
| paymentMethod | string | Default payment method |
| electronicRoutingInfo | object | Bank account details |
| address | object | Mailing address |
| attachments | array | Tax forms and documents |
| createdAt | string | ISO 8601 timestamp |

---

## GET /recipient/{recipientId}

Get details for a specific recipient.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipientId | string | Yes | Recipient ID |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/recipient/{recipientId}" \
  -H "Authorization: Bearer <token>"
```

---

## POST /recipients

Create a new recipient for making payments.

### Request Body

```json
{
  "name": "Acme Corp",
  "emails": ["payments@acme.com"],
  "paymentMethod": "ach",
  "electronicRoutingInfo": {
    "accountNumber": "123456789",
    "routingNumber": "021000021",
    "accountType": "checking"
  },
  "address": {
    "address1": "123 Main St",
    "city": "San Francisco",
    "region": "CA",
    "postalCode": "94102",
    "country": "US"
  }
}
```

### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Recipient name |
| emails | array | No | Contact emails |
| paymentMethod | string | Yes | `ach`, `wire`, `check` |
| electronicRoutingInfo | object | Conditional | Required for ACH/wire |
| address | object | Conditional | Required for check |

### Electronic Routing Info

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| accountNumber | string | Yes | Bank account number |
| routingNumber | string | Yes | ABA routing number |
| accountType | string | Yes | `checking` or `savings` |

### Address Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| address1 | string | Yes | Street address |
| address2 | string | No | Apt/Suite |
| city | string | Yes | City |
| region | string | Yes | State/Province |
| postalCode | string | Yes | ZIP/Postal code |
| country | string | Yes | Country code (ISO 3166-1) |

### Request

```bash
curl -X POST "https://api.mercury.com/api/v1/recipients" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corp",
    "paymentMethod": "ach",
    "electronicRoutingInfo": {
      "accountNumber": "123456789",
      "routingNumber": "021000021",
      "accountType": "checking"
    }
  }'
```

---

## POST /recipient/{recipientId}

Edit information about a specific recipient.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipientId | string | Yes | Recipient ID |

### Request Body

Same structure as POST `/recipients`. Include only fields to update.

---

## POST /recipient/{recipientId}/attachment

Upload an attachment (tax form, contract, etc.) to a recipient.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipientId | string | Yes | Recipient ID |

### Request

Multipart form data with file upload.

```bash
curl -X POST "https://api.mercury.com/api/v1/recipient/{recipientId}/attachment" \
  -H "Authorization: Bearer <token>" \
  -F "file=@W9.pdf" \
  -F "taxFormType=W9"
```

### Form Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes | Document file |
| taxFormType | string | No | Tax form type: `W9`, `W8BEN`, `W8BENE` |

---

## GET /recipient/{recipientId}/attachments

List all attachments for a recipient.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| recipientId | string | Yes | Recipient ID |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/recipient/{recipientId}/attachments" \
  -H "Authorization: Bearer <token>"
```

### Response

```json
{
  "attachments": [
    {
      "id": "att_123",
      "fileName": "W9.pdf",
      "taxFormType": "W9",
      "uploadedAt": "2024-01-01T00:00:00Z",
      "presignedUrl": "https://..."
    }
  ]
}
```

### Notes

- Presigned URLs are ephemeral and expire after a short time
- Download attachments promptly after fetching
