# Privacy Policy - Mercury Banking Trigger Plugin

## Data Accessed

This plugin receives the following data through Mercury Banking webhooks:

- Transaction event notifications (event ID, operation type)
- Transaction details (transaction ID, amount, status, posting date)
- Account identifiers (account ID)
- Counterparty and merchant names
- Transaction descriptions, notes, categories, and types

## Data Transmission

All webhook communication with the Mercury API is conducted over HTTPS (TLS-encrypted connections). Incoming webhook payloads are verified using a signing secret to ensure authenticity and prevent tampering.

## Data Storage

This plugin does **not** persistently store financial data. It uses a small amount of plugin storage solely for webhook subscription management (webhook IDs and signing secrets). Transaction event data is passed directly to Dify workflows without intermediate persistence.

## Third-Party Services

This plugin connects exclusively to the **Mercury Banking API** (`api.mercury.com`) for webhook subscription management. No data is shared with any other third-party services.

## Authentication and Credentials

- Authentication requires a Mercury API Access Token (with `webhooks:write` permission) or OAuth2 credentials (Client ID and Client Secret).
- Webhook signing secrets are used to verify the authenticity of incoming events.
- Credentials are stored securely by the Dify platform using its built-in secret management and are never exposed in logs or API responses.
- The plugin supports sandbox, production, and mock environments.

## User Consent

By installing and configuring this plugin, the user explicitly authorizes it to create webhook subscriptions on their Mercury account and receive real-time transaction events. Users can revoke access at any time by removing the plugin or revoking the API token in their Mercury account settings.
