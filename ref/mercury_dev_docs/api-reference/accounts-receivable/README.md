# Accounts Receivable API

Base URL: `https://api.mercury.com/api/v1`

> **Note:** Invoicing API is only available to Mercury users on a subscription plan. Visit [mercury.com/pricing](https://mercury.com/pricing) to upgrade.

The Accounts Receivable API allows you to manage customers, invoices, and attachments for invoicing.

## Customers

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | List all customers |
| POST | `/customers` | Create a customer |
| GET | `/customer/{customerId}` | Get a customer |
| POST | `/customer/{customerId}` | Update a customer |
| DELETE | `/customer/{customerId}` | Delete a customer |

---

### GET /customers

List all customers for your organization.

#### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/customers" \
  -H "Authorization: Bearer <token>"
```

#### Response

```json
{
  "customers": [
    {
      "id": "cust_123",
      "name": "Acme Corp",
      "email": "billing@acme.com",
      "phone": "+1-555-123-4567",
      "address": {
        "address1": "123 Main St",
        "city": "San Francisco",
        "region": "CA",
        "postalCode": "94102",
        "country": "US"
      },
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ]
}
```

---

### POST /customers

Create a new customer.

#### Request Body

```json
{
  "name": "Acme Corp",
  "email": "billing@acme.com",
  "phone": "+1-555-123-4567",
  "address": {
    "address1": "123 Main St",
    "city": "San Francisco",
    "region": "CA",
    "postalCode": "94102",
    "country": "US"
  }
}
```

---

### GET /customer/{customerId}

Get a specific customer by ID.

---

### POST /customer/{customerId}

Update customer information.

---

### DELETE /customer/{customerId}

Delete a customer. Cannot delete customers with unpaid invoices.

---

## Invoices

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/invoices` | List all invoices |
| POST | `/invoices` | Create an invoice |
| GET | `/invoice/{invoiceId}` | Get an invoice |
| POST | `/invoice/{invoiceId}` | Update an invoice |
| POST | `/invoice/{invoiceId}/cancel` | Cancel an invoice |
| GET | `/invoice/{invoiceId}/attachments` | List invoice attachments |
| GET | `/invoice/{invoiceId}/pdf` | Download invoice PDF |

---

### GET /invoices

List all invoices.

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | string | No | Filter: `draft`, `sent`, `paid`, `cancelled`, `overdue` |
| customerId | string | No | Filter by customer |
| start | string | No | Start date (YYYY-MM-DD) |
| end | string | No | End date (YYYY-MM-DD) |

#### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/invoices?status=sent" \
  -H "Authorization: Bearer <token>"
```

#### Response

```json
{
  "invoices": [
    {
      "id": "inv_123",
      "invoiceNumber": "INV-001",
      "customerId": "cust_123",
      "customerName": "Acme Corp",
      "status": "sent",
      "currency": "USD",
      "subtotal": 1000.00,
      "tax": 80.00,
      "total": 1080.00,
      "amountDue": 1080.00,
      "amountPaid": 0.00,
      "dueDate": "2024-02-15",
      "issueDate": "2024-01-15",
      "lineItems": [
        {
          "description": "Consulting services",
          "quantity": 10,
          "unitPrice": 100.00,
          "amount": 1000.00
        }
      ],
      "createdAt": "2024-01-15T00:00:00Z"
    }
  ]
}
```

---

### POST /invoices

Create a new invoice.

#### Request Body

```json
{
  "customerId": "cust_123",
  "invoiceNumber": "INV-001",
  "issueDate": "2024-01-15",
  "dueDate": "2024-02-15",
  "lineItems": [
    {
      "description": "Consulting services",
      "quantity": 10,
      "unitPrice": 100.00
    }
  ],
  "taxRate": 0.08,
  "notes": "Payment due within 30 days"
}
```

#### Request Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| customerId | string | Yes | Customer ID |
| invoiceNumber | string | No | Custom invoice number |
| issueDate | string | Yes | Issue date (YYYY-MM-DD) |
| dueDate | string | Yes | Due date (YYYY-MM-DD) |
| lineItems | array | Yes | Invoice line items |
| taxRate | number | No | Tax rate (0.08 = 8%) |
| notes | string | No | Additional notes |

---

### GET /invoice/{invoiceId}

Get invoice details.

---

### POST /invoice/{invoiceId}

Update an invoice. Only draft invoices can be updated.

---

### POST /invoice/{invoiceId}/cancel

Cancel an invoice.

#### Request

```bash
curl -X POST "https://api.mercury.com/api/v1/invoice/{invoiceId}/cancel" \
  -H "Authorization: Bearer <token>"
```

---

### GET /invoice/{invoiceId}/attachments

List all attachments for an invoice.

---

### GET /invoice/{invoiceId}/pdf

Download invoice as PDF.

#### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/invoice/{invoiceId}/pdf" \
  -H "Authorization: Bearer <token>" \
  -o invoice.pdf
```

---

## Attachments

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/attachment/{attachmentId}` | Get an attachment |

---

### GET /attachment/{attachmentId}

Get attachment details and download URL.

#### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/attachment/{attachmentId}" \
  -H "Authorization: Bearer <token>"
```

#### Response

```json
{
  "id": "att_123",
  "fileName": "contract.pdf",
  "fileSize": 102400,
  "mimeType": "application/pdf",
  "presignedUrl": "https://...",
  "expiresAt": "2024-01-15T11:00:00Z"
}
```

### Notes

- Presigned URLs expire after a short time
- Download files immediately after fetching the URL
