# Privacy Policy - QuickBooks Online Accounting Plugin

## Data Accessed

This plugin accesses the following data through the QuickBooks Online API:

- Chart of accounts and account balances
- Vendor and customer records (names, contact details, balances)
- Invoices, bills, estimates, and credit memos
- Purchases, deposits, transfers, and journal entries
- Payment and bill payment records
- Sales receipts and refund receipts
- Purchase orders and attachable documents
- Items, employees, classes, and departments
- General entity queries via QuickBooks query language

## Data Transmission

All communication with the QuickBooks Online API is conducted over HTTPS (TLS-encrypted connections). No data is transmitted over unencrypted channels.

## Data Storage

This plugin does **not** store any accounting data. It acts as a pass-through connector between Dify workflows and the QuickBooks Online API. Data is fetched or submitted on demand and returned directly to the workflow without intermediate persistence.

## Third-Party Services

This plugin connects exclusively to the **Intuit QuickBooks Online API** (`quickbooks.api.intuit.com`). No data is shared with any other third-party services.

## Authentication and Credentials

- Authentication uses OAuth2 credentials (Client ID, Client Secret, and Access Token) along with a Realm ID (Company ID).
- Credentials are stored securely by the Dify platform using its built-in secret management and are never exposed in logs or API responses.
- The plugin supports sandbox and production environments for safe testing.

## User Consent

By installing and configuring this plugin, the user explicitly authorizes it to access and modify their QuickBooks Online accounting data through the provided OAuth credentials. Users can revoke access at any time by removing the plugin or disconnecting the app in their Intuit account settings.
