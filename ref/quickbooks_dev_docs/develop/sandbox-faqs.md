# Sandbox FAQ

> QuickBooks Online API - Sandbox Frequently Asked Questions

Here are more details about sandbox companies and how to use them to test code as you develop.

---

## Which QuickBooks Online SKUs can I create sandbox companies for?

You can create sandboxes for:
- **QuickBooks Online Plus**
- **QuickBooks Online Advanced**

> **Tip**: Each [QuickBooks Online SKU](https://quickbooks.intuit.com/pricing/) comes with specific features. We recommend you test with the one your users use the most. Develop your app for features the majority of your users have access to.

---

## How many sandbox companies can I have at a time?

You can have a maximum of **10 sandbox companies**.

You automatically start with a US-based sandbox when you create your developer account.

---

## How long are sandbox companies valid?

Sandbox companies are valid for **two years**.

When they expire, you'll get a subscription cancellation message. You'll need to [create a new sandbox company](./sandboxes.md#create-a-sandbox-company).

**If you see a cancellation message before two years:**

1. Close the message.
2. In the open sandbox company, select the **Gear** icon and then **Account and settings**.
3. Go to the **Billing & subscription** tab.
4. Follow the steps to resubscribe.

> **Important**: If your sandbox company expires, you may be asked to enter payment info. **Don't enter anything**. You can't renew expired sandbox companies. You'll need to create a new one.

---

## Which Client ID and Client Keys should I use for my sandbox company?

Always use the credentials in the **Development** section of your developer account for sandbox companies.

The credentials in the **Production** section are only for live, in production apps and QuickBooks Online companies.

| Environment | Use For |
|-------------|---------|
| Development credentials | Sandbox companies, testing |
| Production credentials | Live apps, real QuickBooks companies |

---

## What's the throttle limit for requests to sandbox companies?

Apps can make **500 requests per minute** to sandbox companies.

| Limit Type | Value |
|------------|-------|
| Requests per minute | 500 |
| Same as production | Yes |

---

## How many emails can I send from Sandbox companies for test purposes?

You can send a total of **40 emails per day** from a Sandbox company for test purposes.

---

## Can I reset or delete sandbox data?

**No.** You can't reset the sample data in sandbox companies.

However, you can delete all of the data and completely start over. Follow the steps in [Clear data and reset the sandbox](./sandboxes.md#clear-data-and-reset-the-sandbox) to delete the original data and anything else you've added.

---

## Why do I get an error after deleting sandbox data?

In rare cases, you may get a "duplicate objects" message when you try to add new data. This is likely a caching issue.

**Solution:**
1. In the open sandbox company, select your **Profile icon**
2. Select **Sign out**
3. Sign back in

This should clear the cache.

---

## Can I create region-specific sandbox companies?

**Yes.** Each sandbox company is tied to one region. You can have multiple sandboxes for different regions. Sandboxes come with region-specific sample data. This lets you comfortably test your app in an environment tailored to your user-base.

### Regional Availability

| SKU | Available Regions |
|-----|-------------------|
| **QuickBooks Online Advanced** | US only |
| **QuickBooks Online Plus** | AU, CA, FR, IN, UK, US |

**QuickBooks Online Plus sandbox regions:**
- Australia (AU)
- Canada (CA)
- France (FR)
- India (IN)
- United Kingdom (UK)
- United States (US)

---

## Can I change the SKU or region of an existing sandbox company?

**No.** Once you create a sandbox, you can't change the region or SKU. You'll need to [create a new one](./sandboxes.md#create-a-sandbox-company).

---

## Why do I keep opening the same sandbox, no matter which one I select?

You can't open multiple sandboxes or QuickBooks Online companies in the same browser at once.

**Workarounds:**
- Use completely separate brands of browsers (e.g., Chrome for sandbox, Firefox for production)
- Use private or incognito browser windows
- Switch between companies directly from the QuickBooks Online UI:
  1. In the open sandbox company, select the **Gear icon**
  2. Select **Switch Company**

**To switch to a different sandbox company:**
1. In the open sandbox company, select the **Gear icon**
2. Select **Switch company**
3. Select another sandbox company

> **Note**: By default, browsers will open the last open sandbox, or the last one on the list in your developer account.

---

## Why do I see a blank page when I try to enable Payroll for my sandbox company?

**Payroll isn't a supported feature for sandbox companies.**

---

## Why do I get an error when I try to link an online bank account?

While sandboxes provide sample online banking data, **you can't connect live bank accounts**. This functionality isn't supported in sandbox environments.

---

## Can I import or export data from sandbox companies?

**No.** You can't import or export data to or from sandbox companies.

---

## Quick Reference

| Feature | Sandbox Support |
|---------|-----------------|
| API Testing | Yes |
| OAuth 2.0 | Yes |
| Sample Data | Yes |
| Region-Specific Data | Yes |
| Payroll | No |
| Live Bank Connections | No |
| Data Import/Export | No |
| Multiple Companies per Browser | No |

---

## Related Documentation

- [Sandbox Overview](./sandboxes.md)
- [Postman Setup](./postman.md)
- [OAuth 2.0 Playground](./authentication-and-authorization/oauth-2.0-playground.md)
