# Privacy Policy - Mercury Banking Tools Plugin

## Data Accessed

This plugin accesses the following data through the Mercury Banking API:

- Bank account details (account ID, name, balance, status)
- Transaction records (amount, status, counterparty, dates, categories)
- Recipient/payee information (name, payment method, account details)
- Card information (cardholder name, card status)
- Account statements and invoice PDFs
- Customer and invoice records

## Data Transmission

All communication with the Mercury API is conducted over HTTPS (TLS-encrypted connections). No data is transmitted over unencrypted channels.

## Data Storage

This plugin does **not** store any financial data. It acts as a pass-through connector between Dify workflows and the Mercury Banking API. Data is fetched on demand and returned directly to the workflow without intermediate persistence.

## Third-Party Services

This plugin connects exclusively to the **Mercury Banking API** (`api.mercury.com`). No data is shared with any other third-party services.

## Authentication and Credentials

- Authentication requires a Mercury API Access Token or OAuth2 credentials (Client ID and Client Secret).
- Credentials are stored securely by the Dify platform using its built-in secret management and are never exposed in logs or API responses.
- The plugin supports sandbox and production environments for safe testing.

## User Consent

By installing and configuring this plugin, the user explicitly authorizes it to access their Mercury Banking data through the provided API credentials. Users can revoke access at any time by removing the plugin or revoking the API token in their Mercury account settings.
