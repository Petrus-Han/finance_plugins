# Privacy Policy - QuickBooks Payments Plugin

## Data Accessed

This plugin accesses the following data through the QuickBooks Payments API:

- Payment tokens (tokenized card and bank account representations)
- Charge records (credit card and debit card transaction details)
- Refund records (refund amounts, statuses, and references)
- Bank account records (account holder name, routing number, account number)

## Data Transmission

All communication with the QuickBooks Payments API is conducted over HTTPS (TLS-encrypted connections). Sensitive payment data such as card numbers and bank account numbers are tokenized by the API before processing. No data is transmitted over unencrypted channels.

## Data Storage

This plugin does **not** store any payment or financial data. It acts as a pass-through connector between Dify workflows and the QuickBooks Payments API. Payment data is submitted or retrieved on demand and returned directly to the workflow without intermediate persistence.

## Third-Party Services

This plugin connects exclusively to the **Intuit QuickBooks Payments API** (`api.intuit.com`). No data is shared with any other third-party services.

## Authentication and Credentials

- Authentication uses OAuth2 credentials (Client ID, Client Secret, and Access Token).
- Credentials are stored securely by the Dify platform using its built-in secret management and are never exposed in logs or API responses.
- The plugin supports sandbox and production environments for safe testing.

## User Consent

By installing and configuring this plugin, the user explicitly authorizes it to process payments, issue refunds, and manage bank accounts through the provided OAuth credentials. Users can revoke access at any time by removing the plugin or disconnecting the app in their Intuit account settings.
