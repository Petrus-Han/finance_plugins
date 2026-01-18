# Mercury API Changelog

## January 2025

### Attachment uploads API now available
*1 day ago*

Added the ability to upload attachments to both [transactions](/reference/uploadtransactionattachment) and [recipients](/reference/uploadtransactionattachment) via API. Also added an endpoint to [list all recipient attachments](/reference/listrecipientsattachments) (tax docs) for your organization.

### Webhooks now available
*11 days ago*

Added support for [Webhooks](/reference/webhooks) to receive real-time HTTP notifications when things happen in your Mercury account (e.g., transaction updates) instead of polling the API. Webhook payloads use the same event structure as the [Events API](/reference/events) and follow the JSON Merge Patch standard.

---

## December 2024

### Recipients will now return associated attachments
*About 1 month ago*

All `/recipients` response objects will return a recipient's associated attachments as an ephemeral pre-signed url as well as the corresponding `taxFormType`, `fileName`, and uploaded `dateTime` info if available.

### Internal Transfers API now available
*About 1 month ago*

Added new endpoint `/transfer` that allows you to programmatically move money between your accounts. This endpoint requires a `SendMoney` write scope.

### Users API now available
*About 1 month ago*

Expanded the Mercury API with two new `/api/v1/users` endpoints that make it easier to retrieve user information for your organization.

---

## November 2024

### Get Transaction by Id
*About 2 months ago*

Retrieve a single transaction without an `accountId` path parameter with the new `GET` endpoint `/transactions/:transactionId`

### Get Organization details
*2 months ago*

Retrieve organization information such as EIN, legal business name, and DBAs via the new `GET` endpoint `/api/v1/organization`.

---

## October 2024

### Events API now available
*3 months ago*

The new [Events API](/reference/events) provides visibility into changes to your Mercury resources through a pull-based event log. Query and replay historical changes to your transactions for backfills, reconciliation, and audit trails.

**Features:**
- Pull-based model for on-demand event queries
- Reliable event replay and backfill scenarios
- Currently supports Transaction resource type
- Additional resource types (Accounts, Cards, etc.) coming in future updates

### Invoicing API now available
*3 months ago*

The new Invoicing API simplifies managing invoices and customers by allowing seamless integration with Mercury invoicing into your existing systems.

> **Note:** Only available to Mercury users on a subscription plan. Visit [mercury.com/pricing](https://mercury.com/pricing) to upgrade.

### Tracking Number now available on Transaction response
*4 months ago*

All `Transaction` responses now return an optional `trackingNumber`: A unique identifier assigned by payment networks to trace transactions (e.g., RTP reference ID, ACH trace number, wire IMAD/OMAD). The field will be `null` if nonexistent.

---

## Earlier Updates

For historical changelog entries, visit the [official Mercury API changelog](https://docs.mercury.com/changelog).
