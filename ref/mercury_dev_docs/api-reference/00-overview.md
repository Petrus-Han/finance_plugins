# Mercury API Reference

Base URL: `https://api.mercury.com/api/v1`

Sandbox URL: `https://api-sandbox.mercury.com/api/v1`

## Detailed Documentation

Each API category has detailed documentation with request/response examples:

| Category | Documentation |
|----------|---------------|
| Accounts | [accounts/README.md](./accounts/README.md) |
| Transactions | [transactions/README.md](./transactions/README.md) |
| Recipients | [recipients/README.md](./recipients/README.md) |
| Accounts Receivable | [accounts-receivable/README.md](./accounts-receivable/README.md) |
| Webhooks | [webhooks/README.md](./webhooks/README.md) |
| Events | [events/README.md](./events/README.md) |
| Treasury | [treasury/README.md](./treasury/README.md) |
| Users | [users/README.md](./users/README.md) |
| OAuth2 | [oauth2/README.md](./oauth2/README.md) |
| Misc (Categories, Credit, Org, Statements) | [misc/README.md](./misc/README.md) |

---

## Authentication

Use Bearer token authentication:

```http
Authorization: Bearer <your_api_token>
```

Or Basic authentication:

```bash
curl --user <api_token>:
```

---

## Accounts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/accounts` | Get all accounts |
| GET | `/account/{accountId}` | Get account by ID |
| GET | `/account/{accountId}/cards` | Get cards for account |
| GET | `/account/{accountId}/statements` | Get account statements |
| GET | `/account/{accountId}/transaction/{transactionId}` | Get transaction by ID |
| GET | `/account/{accountId}/transactions` | List account transactions |
| POST | `/account/{accountId}/transactions` | Create a transaction |
| POST | `/account/{accountId}/request-send-money` | Request to send money (requires approval) |
| POST | `/transfer` | Create an internal transfer |

---

## Transactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/transactions` | List all transactions (paginated) |
| GET | `/transactions/{transactionId}` | Get a transaction by ID |
| PATCH | `/transactions/{transactionId}` | Update transaction metadata |
| POST | `/transactions/{transactionId}/attachment` | Upload a transaction attachment |

---

## Recipients

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/recipients` | Get all recipients (paginated) |
| GET | `/recipient/{recipientId}` | Get recipient by ID |
| POST | `/recipients` | Add a new recipient |
| POST | `/recipient/{recipientId}` | Edit recipient information |
| POST | `/recipient/{recipientId}/attachment` | Upload a recipient attachment |
| GET | `/recipient/{recipientId}/attachments` | List all recipient attachments |

---

## Accounts Receivable

### Customers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | List all customers |
| POST | `/customers` | Create a customer |
| GET | `/customer/{customerId}` | Get a customer |
| POST | `/customer/{customerId}` | Update a customer |
| DELETE | `/customer/{customerId}` | Delete a customer |

### Invoices

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/invoices` | List all invoices |
| POST | `/invoices` | Create an invoice |
| GET | `/invoice/{invoiceId}` | Get an invoice |
| POST | `/invoice/{invoiceId}` | Update an invoice |
| POST | `/invoice/{invoiceId}/cancel` | Cancel an invoice |
| GET | `/invoice/{invoiceId}/attachments` | List invoice attachments |
| GET | `/invoice/{invoiceId}/pdf` | Download invoice PDF |

### Attachments

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/attachment/{attachmentId}` | Get an attachment |

---

## Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | List all categories |

---

## Credit

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/credit` | List all credit accounts |

---

## Events

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/events` | Get all events |
| GET | `/event/{eventId}` | Get event by ID |

---

## Organization

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/organization` | Get organization information |

---

## Send Money Requests

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/send-money-request/{requestId}` | Get send money approval request by ID |

---

## Statements

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/statement/{statementId}/pdf` | Download account statement PDF |

---

## Treasury

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/treasury` | Get all treasury accounts |
| GET | `/treasury/{treasuryId}/transactions` | Get treasury transactions |

---

## Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | Get all users |
| GET | `/user/{userId}` | Get user by ID |

---

## Webhooks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/webhooks` | Get webhook endpoints |
| GET | `/webhook/{webhookId}` | Get webhook endpoint by ID |
| POST | `/webhooks` | Create a new webhook endpoint |
| POST | `/webhook/{webhookId}` | Update an existing webhook endpoint |
| POST | `/webhook/{webhookId}/verify` | Verify a webhook endpoint |
| DELETE | `/webhook/{webhookId}` | Delete a webhook endpoint |

### Webhook Events

Webhooks allow you to receive real-time notifications when resources in your Mercury account change.

---

## OAuth2 API

Base URL: `https://oauth2.mercury.com`

Sandbox URL: `https://oauth2-sandbox.mercury.com`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/authorize` | Start OAuth2 web flow |
| POST | `/token` | Obtain the access token |

---

## Pagination

Many endpoints support cursor-based pagination with the following parameters:

- `start_after` - Cursor to start after
- `end_before` - Cursor to end before
- `limit` - Maximum number of results (default varies by endpoint)

---

## Error Responses

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid or missing token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |
