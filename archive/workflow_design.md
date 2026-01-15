# Dify Workflow Design: Mercury to QuickBooks Sync

This document describes how to connect the developed plugins within a Dify Workflow to achieve automated synchronization.

## 1. Triggers

- **Node**: Mercury Trigger
- **Event**: `transaction_created`
- **Output**: `{{mercury.amount}}`, `{{mercury.description}}`, `{{mercury.date}}`, etc.

## 2. Classification & Mapping (LLM Node)

This is the "Brain" of the workflow.

**Prompt Snippet**:

```markdown
You are a senior accountant. Based on the bank description, categorize the transaction.

Transaction: {{mercury.description}}
Amount: {{mercury.amount}}

Available Chart of Accounts (QuickBooks):
{{qb_accounts_list}}

Rules:

1. If Amount < 0, it is an Expense (Purchase).
2. If Amount > 0, it is Income (Deposit).

Output JSON:
{
"transaction_type": "purchase" | "deposit",
"account_id": "...",
"vendor_name": "...",
"confidence": 0-1
}
```

## 3. Vendor Logic (Conditional)

1. **Search Vendor**: Use `vendor_management` tool with `action="search"`.
2. **Found?**:
   - **Yes**: Use `Vendor.Id`.
   - **No**: Use `vendor_management` tool with `action="create"` to get a new `Id`.

## 4. Writing to QuickBooks

- **If Purchase**: Use `create_purchase`.
  - Pass `bank_account_id` (the one corresponding to Mercury).
  - Pass `expense_account_id` (from LLM).
  - Pass `vendor_id` (from previous step).
- **If Deposit**: Use `create_deposit`.

## 5. Error Handling & Notification

- Use a **Terminal Node** or **HTTP Node** to send a Slack/Email notification if the sync fails or if the LLM confidence is below 0.8.
- For low-confidence mapping, route the workflow to a **Question Node** (Manual Review) to let the accountant approve the categorization before writing to QuickBooks.
