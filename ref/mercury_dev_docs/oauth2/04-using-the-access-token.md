# Using the access token

Call the Mercury API endpoints with the access token using the Bearer Authentication:

```http
Authorization: Bearer <access_token>
```

## Example Usage

### cURL

```bash
curl -X GET "https://api.mercury.com/api/v1/accounts" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json"
```

### Python

```python
import requests

access_token = "<access_token>"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

response = requests.get("https://api.mercury.com/api/v1/accounts", headers=headers)
```

---

## Navigation

- Previous: [Obtain the tokens](./03-obtain-the-tokens.md)
- Next: [What is Mercury MCP?](../mcp/01-what-is-mercury-mcp.md)
