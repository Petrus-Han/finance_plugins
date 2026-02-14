# Privacy Policy - Employee Roster Plugin

## Data Accessed

This plugin accesses the following data through Google Sheets:

- Employee names and email addresses
- Job titles and employment types
- Source system identifiers (Feishu or Deel)
- Source department and finance department assignments
- Employee status and notes
- Department mapping tables (source-to-finance department mappings)

## Data Transmission

All communication with the Google Sheets API is conducted over HTTPS (TLS-encrypted connections). CSV data imported into the roster is transmitted directly to the Google Sheets backend. No data is transmitted over unencrypted channels.

## Data Storage

This plugin does **not** independently store employee data. All roster data resides in the user-designated Google Spreadsheet. The plugin reads from and writes to that spreadsheet on demand, acting as a connector between Dify workflows and Google Sheets.

## Third-Party Services

This plugin connects exclusively to the **Google Sheets API** (`sheets.googleapis.com`). No data is shared with any other third-party services.

## Authentication and Credentials

- Authentication uses either OAuth2 credentials (Client ID, Client Secret, Access Token, and Refresh Token) or a GCP Service Account JSON key.
- A Google Spreadsheet ID is required to identify the target spreadsheet.
- Credentials are stored securely by the Dify platform using its built-in secret management and are never exposed in logs or API responses.

## User Consent

By installing and configuring this plugin, the user explicitly authorizes it to read and write employee roster data in the specified Google Spreadsheet. Users can revoke access at any time by removing the plugin, revoking OAuth access in their Google account, or removing the service account's access to the spreadsheet.
