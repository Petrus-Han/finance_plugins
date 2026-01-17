# Get the Client ID and Client Secret for Your App

> **Source**: https://developer.intuit.com/app/developer/qbo/docs/get-started/get-client-id-and-client-secret

## Overview

The [apps you create](https://developer.intuit.com/app/developer/qbo/docs/get-started/start-developing-your-app) on the Intuit Developer Portal get a unique set of credentials: a **client ID** and a **client secret**.

You'll use these credentials for tasks like authorization and connecting apps to third-party testing tools.

Each app has **two sets of credentials**:
- One for **live production** code
- Another for **sandbox and testing** environments

---

## Get Your App's Credentials

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.

2. Select **My Hub > App dashboard** from the upper-right corner of the toolbar.

3. Select and open an app.

4. Select **Keys and credentials** from the left navigation pane.

5. If you're connecting a [sandbox company](https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes/manage-your-sandboxes):
   - Choose **Development**
   - Turn on the **Show credentials** switch

6. If you're setting up a production app:
   - Choose **Production**
   - Turn on the **Show credentials** switch

7. Copy the **Client ID** and **Client secret**.

---

## Important Notes

> **Note**: The client ID and client secret will be accessible only after completing the **Production Key questionnaire** and its approval. For apps without a completed questionnaire, the questionnaire will be visible when you select **Production** in Step 6.

> **Tip**: Remember, the client ID and client secret for **Production** work only for live, in-production apps. Those for **Development** are only for your sandbox companies.

---

## Mercury Integration Notes

For the Mercury-QuickBooks sync plugin:

1. **Development vs Production**: During development and testing, use **Development** credentials with sandbox companies. Switch to **Production** credentials only when deploying to production.

2. **Credential Security**: The client ID and client secret must be stored securely:
   - Never commit credentials to source control
   - Use environment variables or secure credential storage
   - In Dify plugins, credentials are managed through the provider's `credentials_schema`

3. **OAuth 2.0 Flow**: These credentials are used in the OAuth 2.0 authorization flow to identify your application to the QuickBooks API.
