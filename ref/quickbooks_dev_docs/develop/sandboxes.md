# Sandbox and Testing Tools

> QuickBooks Online API - Development Environment Guide

## Overview

There are multiple ways to test your app during development. You can start with the sandbox QuickBooks Online company connected to your Intuit Developer account. This gives you sample data to test with.

**Key Resources:**
- [Create and test with a sandbox company](#create-and-test-with-a-sandbox-company)
- [Test with Postman](./postman.md)
- [Sandbox FAQ](./sandbox-faqs.md)

You can also set up and configure third-party apps, like Postman, to work with our API frameworks.

---

## Create and Test with a Sandbox Company

When you create your developer profile, you automatically get a sandbox company.

Sandbox companies are **regionally-specific** QuickBooks Online companies with sample data. They look and act just like a normal QuickBooks Online experience.

Use it as a testing environment during development to see your code in action. You can also connect them to external testing tools like Postman or Insomnia.

> **Note**: Sandbox companies are for app development only. Intuit provides this environment, content, and sample data for non-commercial use and testing.

### Create a Sandbox Company

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select **My Hub > Sandboxes** from the upper-right corner of the toolbar.
3. Select **Add**, located on the right.
4. Select **QuickBooks Online Plus** or **QuickBooks Online Advanced**.
5. If you select QuickBooks Online Plus, select a country from the **Country** dropdown.
   > **Note**: Sandbox companies are region-specific. You can't change this later on.
6. Select **Create**.

**Limits:**
- You can create up to **10 sandbox companies**
- They're valid and active for **two years**

> **Tip**: Each QuickBooks Online SKU comes with specific features. We recommend you test with the one your users use the most. Develop your app for features the majority of your users have access to.

---

## Test Code with a Sandbox Company

There are a few ways to use your sandbox company:

- Sandboxes automatically connect to our testing tools, like the [OAuth 2.0 Playground](./authentication-and-authorization/oauth-2.0-playground.md)
- Connect them to third-party testing tools

### Get a Sandbox's Credentials

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select your app.
3. Select **Keys and credentials** from the left navigation pane.
4. Select **Development** and turn on **Show Credentials**.
5. Retrieve or copy the **Client ID** and **Client Secret**.

### Get the Sandbox Base URL

Use this base URL for sandbox companies:

```
https://sandbox-quickbooks.api.intuit.com/v3
```

**Production Base URL** (for comparison):
```
https://quickbooks.api.intuit.com/v3
```

### Open a Sandbox Company to See Your Code in Action

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Select the name of the sandbox company.

> **Tip**: You can't open multiple sandboxes or QuickBooks Online companies in the same browser at once. See [Sandbox FAQ](./sandbox-faqs.md) for workarounds.

---

## Clear Data and Reset the Sandbox

You can delete all sample data and anything else you've entered since you started. This deletes all the data, but keeps the sandbox company.

1. [Sign in](https://developer.intuit.com/dashboard) to your developer account.
2. Find the sandbox company on the list.
3. Select **Clear data and reset** from the button in the **Action** column.

### Delete a Sandbox Entirely

To completely delete a sandbox company if you no longer need it:

1. Select **Delete entire sandbox** from the button in the **Action** column.

---

## Environment Comparison

| Feature | Sandbox | Production |
|---------|---------|------------|
| Base URL | `sandbox-quickbooks.api.intuit.com` | `quickbooks.api.intuit.com` |
| Data | Sample/test data | Real customer data |
| API Version | v3 | v3 |
| Rate Limits | Same as production | Standard limits |
| Validity | 2 years | Unlimited |
| Max Companies | 10 per developer | N/A |

---

## Best Practices for Testing

1. **Use appropriate SKU**: Test with the QuickBooks Online SKU your users use most
2. **Reset regularly**: Clear data between test cycles to ensure clean state
3. **Test all regions**: If your app supports multiple countries, create sandbox companies for each
4. **Use Postman**: Set up [Postman collections](./postman.md) for repeatable API testing
5. **Validate OAuth flow**: Use the OAuth 2.0 Playground before implementing custom auth

---

## Getting Help

- Check the [Sandbox FAQ](./sandbox-faqs.md) for common questions
- Connect with developers on the [Intuit Developer community forum](https://developer.intuit.com/hub)
- [Contact developer support](https://help.developer.intuit.com/s/contactsupport) for additional help

---

## Related Documentation

- [Postman Setup Guide](./postman.md)
- [Sandbox FAQ](./sandbox-faqs.md)
- [OAuth 2.0 Authentication](./authentication-and-authorization/oauth-2.0.md)
- [Getting Started](../get-started/README.md)
