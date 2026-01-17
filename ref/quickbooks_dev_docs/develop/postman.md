# Set Up and Test Queries in Postman

> QuickBooks Online API - Postman Testing Guide

Besides the [sandbox environment](./sandboxes.md) tied to your developer account, you can use [Postman](https://www.postman.com/) to test REST API production code and endpoints.

> **Note**: Only use Postman for testing and prototyping API requests. Use a [QuickBooks Online Accounting API SDK](./sdks-and-samples.md) for production code.

---

## Step 1: Set Up Your App in the Developer Portal

If you haven't already:
1. [Sign in](https://developer.intuit.com/dashboard) to your developer account
2. [Create your app](../get-started/README.md)

---

## Step 2: Get Postman

[Download](https://www.postman.com/) and install Postman.

---

## Step 3: Get a Postman Collection

Download one of the Postman collections. Collections give you sets of pre-built requests to test with. All collections use OAuth 2.0.

| API | Collection Type |
|-----|-----------------|
| **QuickBooks Online Accounting API** | Individual resource endpoints |
| **QuickBooks Online Accounting** | Orchestrated collection based around specific use cases |
| **Payments API** | Individual resource endpoints + orchestrated collection |

---

## Step 4: Use Collections in Postman

In Postman, go to the **Collections** menu any time to see the types of sample requests you can make.

---

## Step 5: Get Your App's Authorization Keys and Set the Redirect URI

Postman needs your app's authorization keys to generate access tokens and connect to the QuickBooks Online API.

### Get Credentials

1. [Sign in](https://developer.intuit.com/dashboard) to your Intuit Developer Account.
2. Select **My Hub > App dashboard** from the upper-right corner of the toolbar.
3. Select and open your app.
4. Select **Keys and credentials** from the left navigation pane.
5. Select **Development** and turn on **Show Credentials**.
6. Copy your app's **Client ID** and **Client Secret**.

### Set Redirect URI

Before you leave the app, set the redirect URI:

1. Select **Settings** from the left navigation pane.
2. Select the **Redirect URIs** tab.
3. Select **Development**.
4. In the text box, enter: `https://www.getpostman.com/oauth2/callback`
5. Select **Save**.

---

## Step 6: Configure Your Testing Environment in Postman

1. In Postman, select the **Collections** menu.
2. Select a folder and endpoint you want to test.
3. Select the **Authorization** tab.
4. From the **Type** dropdown, select **OAuth 2.0**.
5. From the **Add authorization data** dropdown, select **Request Headers**.
6. Expand the **Configure New Access Token** section.

### OAuth 2.0 Configuration

Enter the following values:

| Data Field | What to Enter |
|------------|---------------|
| **Token Name** | A name for the token (appears in Existing Tokens list) |
| **Grant Type** | Select **Authorization Code** |
| **Callback URL** | `https://www.getpostman.com/oauth2/callback` |
| **Auth URL** | `https://appcenter.intuit.com/connect/oauth2` |
| **Access Token URL** | `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer` |
| **Client ID** | Your app's Client ID |
| **Client Secret** | Your app's Client Secret |
| **Scope** | See scopes below |
| **State** | Any useful info about your app (round-tripped by server) |
| **Client Authentication** | **Send client credentials in body** |

### OAuth 2.0 Scopes

| API | Scope |
|-----|-------|
| QuickBooks Online Accounting API | `com.intuit.quickbooks.accounting` |
| QuickBooks Payments | `com.intuit.quickbooks.payment` |

When you're done, select **Get new access token**. You may need to sign in and connect your Intuit Developer Account to Postman.

> **Tip**: You can also follow the [authorization steps from Postman](https://learning.postman.com/docs/sending-requests/authorization/).

---

## Step 7: Update the Test Environment

The collections you downloaded give you environment templates. Add details about your sandbox test company:

1. Get the **company ID** for your [sandbox test company](./sandboxes.md).
2. In Postman, go to the **Environments** menu.
3. Select an environment template.

### Environment Variables

| Data Field | What to Enter |
|------------|---------------|
| **baseurl** | See URLs below |
| **companyid** | Your sandbox test company's **company ID** |
| **minorversion** | The [minor version](../learn/rest-api-features.md) for your app |
| **UserAgent** | `QBOV3-OAuth2-Postman-Collection` |

### Base URLs

| API | Sandbox URL |
|-----|-------------|
| QuickBooks Online Accounting API | `sandbox-quickbooks.api.intuit.com` |
| QuickBooks Payments | `sandbox.api.intuit.com` |

---

## Step 8: Generate Tokens and Send a Test Query

Everything is ready to start testing. You should have an authorization token after setup. **Tokens are valid for 60 minutes**.

### Refresh a Token

1. Open a collection and folder. Then select an endpoint.
2. Go to the **Authorization** tab.
3. Select an available token, or **Get New Access Token**.

### Create a Test Request

1. Open a collection and folder. Then select an endpoint.
2. Review the request in the **Body** tab.
3. Select **Send**.

You'll see the server response in the Body tab.

---

## Quick Reference

### OAuth 2.0 URLs

| Purpose | URL |
|---------|-----|
| Authorization | `https://appcenter.intuit.com/connect/oauth2` |
| Token Exchange | `https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer` |
| Callback (Postman) | `https://www.getpostman.com/oauth2/callback` |

### API Base URLs

| Environment | Accounting API | Payments API |
|-------------|----------------|--------------|
| Sandbox | `sandbox-quickbooks.api.intuit.com` | `sandbox.api.intuit.com` |
| Production | `quickbooks.api.intuit.com` | `api.intuit.com` |

### Token Lifetimes

| Token Type | Validity |
|------------|----------|
| Access Token | 60 minutes |
| Refresh Token | 100 days |

---

## Example: Query Company Info

Once configured, you can test a simple query:

```
GET https://sandbox-quickbooks.api.intuit.com/v3/company/{companyId}/companyinfo/{companyId}
```

**Headers:**
```
Authorization: Bearer {access_token}
Accept: application/json
```

---

## Related Documentation

- [Sandbox Overview](./sandboxes.md)
- [Sandbox FAQ](./sandbox-faqs.md)
- [SDKs and Sample Code](./sdks-and-samples.md)
- [OAuth 2.0 Authentication](./authentication-and-authorization/oauth-2.0.md)
