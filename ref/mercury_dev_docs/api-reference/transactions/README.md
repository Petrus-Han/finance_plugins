# Transactions API

Base URL: `https://api.mercury.com/api/v1`

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/transactions` | List all transactions |
| GET | `/transactions/{transactionId}` | Get a transaction by ID |
| PATCH | `/transactions/{transactionId}` | Update transaction metadata |
| POST | `/transactions/{transactionId}/attachment` | Upload a transaction attachment |

---

## GET /transactions

Retrieve a paginated list of all transactions across all accounts. Supports advanced filtering by date ranges, status, categories, and cursor-based pagination.

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Max results per page (default: 50) |
| start_after | string | No | Cursor for pagination (transaction ID) |
| end_before | string | No | Cursor for backward pagination |
| start | string | No | Start date (YYYY-MM-DD) |
| end | string | No | End date (YYYY-MM-DD) |
| status | string | No | Filter: `pending`, `sent`, `cancelled`, `failed` |
| search | string | No | Search in description/notes |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/transactions?limit=50&start=2024-01-01" \
  -H "Authorization: Bearer <token>"
```

### Response

```json
{
  "transactions": [
    {
      "id": "txn_123abc",
      "accountId": "account_123",
      "amount": -1500.00,
      "status": "sent",
      "counterpartyName": "Acme Corp",
      "counterpartyId": "recipient_456",
      "note": "Invoice #1234",
      "postedAt": "2024-01-15T10:30:00Z",
      "createdAt": "2024-01-15T10:00:00Z",
      "kind": "externalTransfer",
      "externalMemo": "Payment for services",
      "trackingNumber": "ACH123456789",
      "details": {
        "electronicRoutingInfo": {
          "accountNumber": "****5678",
          "routingNumber": "123456789",
          "bankName": "Chase Bank"
        }
      },
      "attachments": []
    }
  ],
  "hasMore": true,
  "nextCursor": "txn_124abc"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique transaction ID |
| accountId | string | Associated account ID |
| amount | number | Amount (negative for debits) |
| status | string | Transaction status |
| counterpartyName | string | Name of counterparty |
| counterpartyId | string | Recipient ID (if applicable) |
| note | string | Internal note |
| postedAt | string | When transaction posted |
| createdAt | string | When transaction created |
| kind | string | Transaction type |
| externalMemo | string | External memo/description |
| trackingNumber | string | Network tracking ID (ACH trace, wire IMAD/OMAD, RTP ref) |
| details | object | Additional details |
| attachments | array | Attached documents |

### Transaction Kinds

| Kind | Description |
|------|-------------|
| externalTransfer | Payment to external recipient |
| internalTransfer | Transfer between own accounts |
| cardTransaction | Debit/credit card purchase |
| fee | Mercury fee |
| checkDeposit | Check deposited |
| achCredit | Incoming ACH credit |
| achDebit | Outgoing ACH debit |
| wireCredit | Incoming wire |
| wireDebit | Outgoing wire |

### Transaction Statuses

| Status | Description |
|--------|-------------|
| pending | Transaction initiated, not yet processed |
| sent | Successfully sent/completed |
| cancelled | Cancelled before processing |
| failed | Failed to process |

---

## GET /transactions/{transactionId}

Retrieve a single transaction by ID without needing the account ID.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| transactionId | string | Yes | Transaction ID |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/transactions/{transactionId}" \
  -H "Authorization: Bearer <token>"
```

### Response

Same structure as individual transaction in list response.

---

## PATCH /transactions/{transactionId}

Update transaction metadata (notes, category, etc.).

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| transactionId | string | Yes | Transaction ID |

### Request Body

```json
{
  "note": "Updated internal note",
  "categoryId": "category_123"
}
```

### Request

```bash
curl -X PATCH "https://api.mercury.com/api/v1/transactions/{transactionId}" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"note": "Updated note"}'
```

---

## POST /transactions/{transactionId}/attachment

Upload an attachment (receipt, invoice, etc.) to a transaction.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| transactionId | string | Yes | Transaction ID |

### Request

Multipart form data with file upload.

```bash
curl -X POST "https://api.mercury.com/api/v1/transactions/{transactionId}/attachment" \
  -H "Authorization: Bearer <token>" \
  -F "file=@receipt.pdf"
```

### Supported File Types

- PDF
- PNG
- JPG/JPEG
- GIF

### Response

```json
{
  "attachmentId": "att_123",
  "fileName": "receipt.pdf",
  "fileSize": 102400,
  "mimeType": "application/pdf",
  "uploadedAt": "2024-01-15T10:30:00Z"
}
```

---

## Pagination

Transactions API uses cursor-based pagination for efficient traversal of large result sets.

### Forward Pagination

```bash
# First page
GET /transactions?limit=50

# Next page (use nextCursor from response)
GET /transactions?limit=50&start_after=txn_124abc
```

### Backward Pagination

```bash
GET /transactions?limit=50&end_before=txn_100abc
```

### Best Practices

1. Always use cursor pagination for large datasets
2. Store cursors for resumable iteration
3. Use date filters to limit result scope
4. Check `hasMore` to know if more results exist
