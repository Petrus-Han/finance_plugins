# Mercury Banking Trigger

Receive real-time Mercury transaction events via webhooks to trigger Dify workflows.

## Setup

1. Log in to [Mercury](https://mercury.com) → **Settings** → **API Tokens**
2. Create a token with `webhooks:write` permission
3. Install this plugin in Dify and enter your API token
4. Select API environment: **Sandbox** or **Production**
5. Add the trigger to a Dify workflow — it will provide a webhook URL
6. In Mercury Dashboard → **Webhooks**, create a webhook pointing to that URL
7. Copy the **Webhook Secret** from Mercury and enter it in the trigger configuration

## Trigger Output

When a transaction is created or updated, the trigger provides:

- `transaction_id`, `event_id`, `account_id`
- `amount` (negative = debit, positive = credit)
- `status` (`pending`, `posted`, etc.)
- `counterparty_name`, `bank_description`, `note`
- `transaction_type` (`debit` or `credit`)
- `posted_at` (ISO 8601 timestamp)
- `category`, `operation_type` (`created` or `updated`)

## Configuration Options

- **Event Types** — Filter by `transaction.created`, `transaction.updated`, or both
- **Filter Paths** — Only trigger on specific field changes (e.g., `status,amount`)

All incoming webhooks are verified using HMAC-SHA256 signature validation.
