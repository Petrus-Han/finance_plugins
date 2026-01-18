# Learn About Scopes

> **Source**: https://developer.intuit.com/app/developer/qbo/docs/learn/scopes

## Overview

Scopes determine the types of data, and by extension API entities, your app can read and update in QuickBooks Online.

Essentially, Intuit uses scopes to define data types and manage data access for third-party apps. We categorize different types of data into distinct "buckets." Some bucket accounting data, others only bucket user info data.

When you set scopes, you're requesting permission to utilize one or more of these defined data types. Another way to look at it, scopes limit the data types (entities and resources) your app gets access to. This makes it clear what data your app needs to function, which increases trust and transparency with your users.

---

## Scopes for App Authorization

When you [set up OAuth 2.0](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0), you'll list one or more scopes in your authorization request. This tells us what type of data your app needs to access so we can grant the correct permissions.

Scopes also tell your end-users which areas of their QuickBooks Online companies your app will work with. [During the authorization flow](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0#redirect-to-server), users will see the requested scopes on the authorization page. They're essentially agreeing to let your app access the data types as defined by the scopes.

If users grant your app access, the Intuit OAuth 2.0 Server will send access tokens to your app. Access tokens are limited by the granted scopes.

> **Tip**: Instead of requesting access to all scopes upfront, we recommend requesting them incrementally based on your app's current data requirements.

Each time you update your app's scopes, you [need to restart the authorization flow](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0#redirect-to-server) so users can reauthorize your app. You'll need to list the new scopes and get new access tokens.

---

## Current Scopes for the QuickBooks Online Accounting API

| Scope | Description |
|-------|-------------|
| `com.intuit.quickbooks.accounting` | Grants access to the [QuickBooks Online Accounting API](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account), which focuses on accounting data. |
| `com.intuit.quickbooks.payment` | Grants access to the [QuickBooks Payments API](https://developer.intuit.com/app/developer/qbpayments/docs/api/resources/all-entities/bankaccounts), which focuses on payments processing. |
| `openid` | Grants access to [OpenID Connect](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/openid-connect) features. Include one or more of the following capabilities: |

### OpenID Connect Capabilities

When using the `openid` scope, you can request additional user information:

| Capability | Description |
|------------|-------------|
| `profile` | User's given and family names info |
| `email` | User's email address info |
| `phone` | User's phone number info |
| `address` | User's physical address info |

---

## Current Scopes for the QuickBooks Online GraphQL API

| Scope | Description |
|-------|-------------|
| `app-foundations.custom-field-definitions.read` | Grants access to read [Custom Fields](https://developer.intuit.com/app/developer/qbo/docs/workflows/create-custom-fields) definition data. |
| `app-foundations.custom-field-definitions` | Grants access to read and write [Custom Fields](https://developer.intuit.com/app/developer/qbo/docs/workflows/create-custom-fields) definitions data. |
| `project-management.project` | Grants access to read and write [Project](https://developer.intuit.com/app/developer/qbo/docs/workflows/manage-projects) data. |
| `indirect-tax.tax-calculation.quickbooks` | Grants access to the [Sales Tax API](https://developer.intuit.com/app/developer/qbo/docs/workflows/calculate-sales-tax). |
| `payroll.compensation.read` | Grants read access to pay types (i.e., compensation) using the [Time API](https://developer.intuit.com/app/developer/payroll-time/docs/workflows/use-cases-track-time). Compensation data can only be queried for customers using QuickBooks Payroll. |

---

## Mercury Integration Notes

For the Mercury-QuickBooks sync plugin:

### Required Scope

The Mercury sync plugin requires the **`com.intuit.quickbooks.accounting`** scope to:

- Create and read **Purchase** entities (for recording expenses)
- Create and read **Deposit** entities (for recording income)
- Create and read **Vendor** entities (for managing payees)
- Query **Account** entities (for mapping to chart of accounts)
- Read **CompanyInfo** (for company settings and currency)

### OAuth Authorization Request Example

When implementing the OAuth flow for the plugin, include the accounting scope:

```
scope=com.intuit.quickbooks.accounting
```

### Optional Scopes

If the plugin needs user profile information (e.g., for display purposes), you could also request:

```
scope=com.intuit.quickbooks.accounting openid profile email
```

This would grant access to accounting data plus the user's name and email address.
