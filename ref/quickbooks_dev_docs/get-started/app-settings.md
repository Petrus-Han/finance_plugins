# Change App Settings

> **Source**: https://developer.intuit.com/app/developer/qbo/docs/get-started/app-settings

## Overview

You can change the settings for each app you create on the Intuit Developer Portal.

Apps have **two sets of settings**:
- One for **live, in-production apps**
- Another for your **sandbox and testing environments**

---

## Change Basic App Settings

You can change things like your app's name, category, and where you plan to release it.

### Steps

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select **My Hub > App dashboard** from the upper-right corner of the toolbar.
3. Select and open an app.
4. Select **Settings** from the left navigation pane.
5. Adjust the following as required by navigating to the respective tabs:
   - **Basic app info**
   - **App URLs**
   - **App terms of service**
   - **App categories**
   - **Geolocation**
   - **Redirect URIs**
   - **Accepted connections**
6. To set the App URLs, choose **Development** for [sandbox and development environments](https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes/manage-your-sandboxes) or **Production** when your app is live in production.
7. To set the Redirect URL, choose **Development** for sandbox environments or **Production** when your app is live in production.

---

## Learn More About Each Setting

### Basic App Info

Add a descriptive, branded name that helps users identify your app. Upload a logo so it is immediately recognizable. Make sure the name and logo meet the [naming and logo guidelines](https://developer.intuit.com/app/developer/qbo/docs/go-live/list-on-the-app-store/naming-and-logo-guidelines).

### App URLs

Set your app's host domain, launch URL, and disconnect URL for both Development and Production environments.

### App Terms of Service

Include any customer-facing pages for your license agreement, privacy policy, and other info that tells users how your app uses their data.

### App Categories

Select up to four categories that describe what your app does. Selecting these categories helps users discover your app when you upload it to the QuickBooks Online App Marketplace.

### Geolocation

Tell us where your app is hosted. Select the country and add the IP address (optional). If your app is hosted in multiple countries, add all of them by selecting **Add a country**.

### Redirect URIs

Add redirect URIs for your app for both Development and Production environments.

### Accepted Connections

Select the countries where you've launched your app and can fully support. This means you've considered the following:

- Data privacy requirements
- Payment processing regulations
- Currency and conversion rules
- Tax implications
- Technical support for app users

This list isn't exhaustive and there may be additional requirements for specific regions. See the [list of countries we allow app connections from](https://developer.intuit.com/app/developer/qbo/docs/go-live/list-on-the-app-store).

### Scopes

These are essentially the permissions your app needs to get certain data from QuickBooks. Learn more [about scopes](https://developer.intuit.com/app/developer/qbo/docs/learn/scopes).

> **Note**: You can add additional scopes, but you can't remove existing ones.

---

## How to Set Your App URLs

Your app's host domain, launch URL, disconnect URL, and redirect URI depend on whether your app [implements the Intuit Single Sign-on feature](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/single-sign-on-models).

### For Apps That Use Intuit Single Sign-on

| Setting | Description |
|---------|-------------|
| **Host domain** | Add your app's site domain |
| **Launch URL** | Add a link to the page that [implements single sign-on](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/single-sign-on-models). This is the URL Intuit will call to start the OAuth 2.0 or OpenIdConnect authorization process |
| **Disconnect URL** | Add a link to the page users get redirected to if they decide to disconnect their QuickBooks Online company from your app. Similar to the launch URL, the disconnect URL should be OpenID enabled |

### For Apps That Don't Use Intuit Single Sign-on

| Setting | Description |
|---------|-------------|
| **Host domain** | Add your app's site domain |
| **Launch URL** | Add your app's sign-in page |
| **Disconnect URL** | Add any static page that tells a user they've disconnected their QuickBooks Online company from your app |

> **Tip**: You may want to add steps for reconnecting to your app, just in case the disconnect was unintentional.

---

## Mercury Integration Notes

For the Mercury-QuickBooks sync plugin:

1. **Redirect URIs**: The plugin will need a redirect URI configured for the OAuth flow. This is where users will be redirected after authorizing the connection.

2. **Scopes**: The Mercury sync plugin will need the **Accounting** scope at minimum to:
   - Create/read Purchases
   - Create/read Deposits
   - Create/read Vendors
   - Query Accounts

3. **Development vs Production**: Use Development settings for sandbox testing before switching to Production settings for live deployments.
