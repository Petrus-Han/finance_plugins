# Create and Start Developing Your App

> Source: https://developer.intuit.com/app/developer/qbo/docs/get-started/start-developing-your-app

Let's get started. The QuickBooks Online Accounting API gives you incredible flexibility to build creative solutions for key business and accounting workflows.

## Getting Started Options

- **[Browse the API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/account)** to see our library of API entities and develop your app from scratch
- **[Start building around common business use cases](https://developer.intuit.com/app/developer/qbo/docs/workflows)** for guided workflows
- **[Integrate with QuickBooks Desktop](https://developer.intuit.com/app/developer/qbdesktop/docs/get-started)** if you need desktop integration
- **[Integrate QuickBooks Payments API](https://developer.intuit.com/app/developer/qbpayments/docs/workflows/process-a-payment)** if your app needs payment processing

---

## Step 1: Get to Know the QuickBooks Online Accounting API Platform

Already familiar with our APIs? Feel free to skip ahead. If you're new, review our platform's capabilities:

- [Learn about our API platform](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api)
- [Learn how REST API works](https://developer.intuit.com/app/developer/qbo/docs/learn/rest-api-features)
- [Learn basic bookkeeping in QuickBooks](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping)
- [Learn about QuickBooks Online features](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-quickbooks-online-basics)

---

## Step 2: Set Up Your Developer Account

Go to the Intuit Developer Portal and **[create a developer account](https://developer.intuit.com/app/developer/myapps)**.

This profile is where you'll:
- Create apps
- Get app credentials
- Set up sandbox companies for testing

---

## Step 3: Create an App on the Intuit Developer Portal

The apps you create on our developer portal generate unique credentials and info you'll need during development.

1. **[Sign in](https://developer.intuit.com/dashboard)** to your developer account
2. Select **My Hub > App dashboard** from the upper-right corner of the toolbar
3. Select the app card with a **+** to create a new app
4. Follow the on-screen steps

### App Scopes

When you create apps, you'll **[pick your app's scopes](https://developer.intuit.com/app/developer/qbo/docs/learn/scopes)**. Scopes limit the type of data your app can access:

| Scope | Use Case |
|-------|----------|
| `accounting` | Access to accounting data only |
| `payments` | Access to payment data (add if needed) |

---

## Step 4: Create a Sandbox QuickBooks Online Company

When you create an Intuit Developer account, we give you a test company with sample data. We call this a **sandbox company**.

You can use this sandbox company to test your code. Here's how to **[create additional sandbox companies](https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes/manage-your-sandboxes)**.

---

## Step 5: Learn How to Get Your App's Credentials

During development, you'll need to **[use your app's credentials](https://developer.intuit.com/app/developer/qbo/docs/get-started/get-client-id-and-client-secret)** for various tasks such as authorization.

---

## Step 6: Authorize Your App

Use your credentials (i.e., **Client ID** and **Client Secret**) to **[connect your app to OAuth 2.0](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization)**. This grants access tokens your app can use to send requests to our APIs.

### Quick Sample API Call

You don't need to fully authenticate your app to test requests. Here's how to quickly call the `CompanyInfo` entity:

#### Get an Access Token

1. Visit the **[OAuth 2.0 Playground](https://developer.intuit.com/app/developer/playground)**
2. Select a sandbox company from the **Select app** dropdown
3. Follow the on-screen steps to get an **access token** (temporary token for testing only)
4. Copy the **Access token** and **Realm ID** (also known as Company ID)

#### Create a Sample Request

Replace the placeholders with your copied values:

```bash
curl -X GET 'https://sandbox-quickbooks.api.intuit.com/v3/company/REPLACE_WITH_SANDBOX_COMPANY_ID/companyinfo/REPLACE_WITH_SANDBOX_COMPANY_ID?minorversion=12' \
  -H 'accept: application/json' \
  -H 'authorization: Bearer REPLACE_WITH_ACCESS_TOKEN' \
  -H 'content-type: application/json'
```

The response for your request should return the company information.

---

## Step 7: Test Your Code

Check out **[QuickBooks and third-party testing tools](https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes)** you can use during development. We've configured tools, including Postman, to make testing with your sandbox company easier.

---

## Summary Checklist

| Step | Task | Status |
|------|------|--------|
| 1 | Learn the API platform | ⬜ |
| 2 | Create developer account | ⬜ |
| 3 | Create an app | ⬜ |
| 4 | Create sandbox company | ⬜ |
| 5 | Get app credentials | ⬜ |
| 6 | Authorize app (OAuth 2.0) | ⬜ |
| 7 | Test your code | ⬜ |

---

## Next Steps

- [Get Client ID and Client Secret](./get-client-id-and-client-secret.md)
- [Authentication and Authorization](../develop/authentication-and-authorization/oauth-2.0.md)
- [Create a Sandbox](../develop/sandboxes.md)
- [API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
