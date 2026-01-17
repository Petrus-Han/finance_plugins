# Make your app available in QuickBooks Online Accountant

When you [list your app in the QuickBooks App Store](/app/developer/qbo/docs/go-live/list-on-the-app-store), it also appears in the Apps tab in QuickBooks Online. This lets users quickly find and download your app from multiple places.

However, apps don't automatically appear in QuickBooks Online Accountant.

If you want to make your app available to accountants so they can recommend it to their clients, you need to set up Intuit Single Sign-on (SSO). Intuit Single Sign-on lets users with multiple QuickBooks Online companies connect to apps using the same user profile. It also lets accountants using QuickBooks Online Accountant support and create multiple QuickBooks Online companies for their clients.

## Step 1: Understand multiple company connections

If you [set up Intuit Single Sign-on](/app/developer/qbo/docs/develop/authentication-and-authorization/single-sign-on-models), your app needs to be able to manage multiple QuickBooks company connections from the same user profile. Map connections based on each company's **realmID**.

In this example, John the accountant has three companies connected to the same Intuit identity: one for his accounting firm, one for Sue's Bakery, and another for Bill's Butcher.

Apps need to maintain mappings (in the diagram, we call this the "mapped ID") between each **realmID** and the connected company's admin user. Index using the **realmID**.

## Step 2: Set up Intuit Single Sign-on via OpenID Connect

If you haven't already, [set up Intuit Single Sign-on](/app/developer/qbo/docs/develop/authentication-and-authorization/single-sign-on-models). This [requires OpenID Connect](https://developer.intuit.com/app/developer/qbpayments/docs/develop/authentication-and-authorization/identity).

> **Important**: You need to implement Intuit Single Sign-on if you want your app to appear in QuickBooks Online Accountant.

Also review the "accountant-ready" [technical requirements for Intuit Single Sign-on](/app/developer/qbo/docs/go-live/publish-app/technical-requirements).

## Step 3: Enable the "Accountant ready" option

1. [List your app in the QuickBooks App Store](/app/developer/qbo/docs/go-live/list-on-the-app-store).
2. In the **Do you support Intuit Single Sign-on** section, select **Yes**.
3. Fill out the **Connect Request URL** fields.
4. In the **Is your app QuickBooks Online Accountant ready** section, select **Yes**.
5. Select **Save**.

Now, users with multiple companies (or accountants managing multiple companies for their clients) can sign in and connect to your app using the same user profile.

## Step 4: See who's connected to your app

Need to know if the admin user who connected their company to your app is also connected to QuickBooks Online Accountant?

Use the [entitlements](/app/developer/qbo/docs/api/accounting/all-entities/entitlements) entity to get info about the company. Review the `name` and `term` fields in the response:

```xml
<Entitlement id="52">
   <name>Accountant Menu</name>
   <term>On</term>
</Entitlement>
```
