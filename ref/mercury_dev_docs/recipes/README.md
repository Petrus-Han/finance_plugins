# Mercury API Recipes

This section contains practical examples and use cases for the Mercury API.

> Note: The Recipes section on Mercury's documentation site is currently minimal. Check the [official documentation](https://docs.mercury.com/recipes) for updates.

## Common Use Cases

### 1. Fetch All Transactions

```python
import requests

token = "your_api_token"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(
    "https://api.mercury.com/api/v1/transactions",
    headers=headers
)
transactions = response.json()
```

### 2. Create a Payment

```python
import requests

token = "your_api_token"
account_id = "your_account_id"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
    "recipientId": "recipient_id",
    "amount": 100.00,
    "paymentMethod": "ach",
    "idempotencyKey": "unique_key_123"
}

response = requests.post(
    f"https://api.mercury.com/api/v1/account/{account_id}/transactions",
    headers=headers,
    json=payload
)
```

### 3. Internal Transfer Between Accounts

```python
import requests

token = "your_api_token"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
    "fromAccountId": "source_account_id",
    "toAccountId": "destination_account_id",
    "amount": 500.00,
    "idempotencyKey": "transfer_123"
}

response = requests.post(
    "https://api.mercury.com/api/v1/transfer",
    headers=headers,
    json=payload
)
```

### 4. Set Up a Webhook

```python
import requests

token = "your_api_token"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
    "url": "https://your-server.com/webhook",
    "events": ["transaction.created", "transaction.updated"]
}

response = requests.post(
    "https://api.mercury.com/api/v1/webhooks",
    headers=headers,
    json=payload
)
```

### 5. Paginate Through Recipients

```python
import requests

token = "your_api_token"
headers = {"Authorization": f"Bearer {token}"}

all_recipients = []
cursor = None

while True:
    params = {"limit": 100}
    if cursor:
        params["start_after"] = cursor
    
    response = requests.get(
        "https://api.mercury.com/api/v1/recipients",
        headers=headers,
        params=params
    )
    data = response.json()
    recipients = data.get("recipients", [])
    
    if not recipients:
        break
    
    all_recipients.extend(recipients)
    cursor = recipients[-1]["id"]

print(f"Total recipients: {len(all_recipients)}")
```

---

## Related Resources

- [API Reference](../api-reference/00-overview.md)
- [Getting Started](../guides/02-getting-started.md)
- [OAuth2 Integration](../oauth2/01-integrations-with-oauth2.md)
