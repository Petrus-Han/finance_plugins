# Users API

Base URL: `https://api.mercury.com/api/v1`

The Users API allows you to retrieve information about users in your organization.

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | Get all users |
| GET | `/user/{userId}` | Get user by ID |

---

## GET /users

Retrieve a list of all users for your organization.

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/users" \
  -H "Authorization: Bearer <token>"
```

### Response

```json
{
  "users": [
    {
      "id": "user_123",
      "email": "john@company.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "admin",
      "status": "active",
      "createdAt": "2024-01-01T00:00:00Z"
    },
    {
      "id": "user_456",
      "email": "jane@company.com",
      "firstName": "Jane",
      "lastName": "Smith",
      "role": "member",
      "status": "active",
      "createdAt": "2024-01-15T00:00:00Z"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique user ID |
| email | string | User email address |
| firstName | string | First name |
| lastName | string | Last name |
| role | string | User role in organization |
| status | string | Account status |
| createdAt | string | ISO 8601 timestamp |

### User Roles

| Role | Description |
|------|-------------|
| admin | Full access, can manage users and settings |
| member | Standard access |
| view_only | Read-only access |
| accountant | Accounting and reporting access |

---

## GET /user/{userId}

Get details for a specific user.

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userId | string | Yes | User ID |

### Request

```bash
curl -X GET "https://api.mercury.com/api/v1/user/{userId}" \
  -H "Authorization: Bearer <token>"
```

### Response

Same structure as individual user in list response, potentially with additional details.
