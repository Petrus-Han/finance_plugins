# Treasury API

Base URL: `https://api.mercury.com/api/v1`

Treasury accounts are interest-bearing accounts for your organization's funds.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/treasury` | Get all treasury accounts |
| GET | `/treasury/{treasuryId}/transactions` | Get treasury transactions |

---

## GET /treasury

Get all treasury accounts associated with the authenticated organization.

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/treasury" \
  -H "Authorization: Bearer <token>"
```

### Response

```json
{
  "treasuryAccounts": [
    {
      "id": "treasury_123",
      "name": "Treasury Account",
      "status": "active",
      "balance": 500000.00,
      "apy": 4.50,
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique treasury account ID |
| name | string | Account display name |
| status | string | Account status |
| balance | number | Current balance |
| apy | number | Annual Percentage Yield |
| createdAt | string | ISO 8601 timestamp |

---

## GET /treasury/{treasuryId}/transactions

Get paginated treasury transactions for a specific treasury account.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| treasuryId | string | Yes | Treasury account ID |

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| limit | integer | No | Max results per page |
| start_after | string | No | Cursor for pagination |
| start | string | No | Start date (YYYY-MM-DD) |
| end | string | No | End date (YYYY-MM-DD) |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/treasury/{treasuryId}/transactions?limit=50" \
  -H "Authorization: Bearer <token>"
```

### Response

```json
{
  "transactions": [
    {
      "id": "txn_treasury_123",
      "treasuryId": "treasury_123",
      "type": "interest",
      "amount": 1500.00,
      "balance": 501500.00,
      "description": "Monthly interest",
      "postedAt": "2024-01-31T00:00:00Z"
    },
    {
      "id": "txn_treasury_124",
      "treasuryId": "treasury_123",
      "type": "transfer_in",
      "amount": 100000.00,
      "balance": 500000.00,
      "description": "Transfer from checking",
      "postedAt": "2024-01-15T00:00:00Z"
    }
  ],
  "hasMore": false
}
```

### Transaction Types

| Type | Description |
|------|-------------|
| interest | Interest payment |
| transfer_in | Transfer from checking account |
| transfer_out | Transfer to checking account |
| fee | Account fee |
