# What Customers Can Do with QuickBooks Online

> **Source**: https://developer.intuit.com/app/developer/qbo/docs/learn/learn-quickbooks-online-basics

## Overview

The [QuickBooks Online Accounting API](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api) lets you build apps that can access most customer-facing QuickBooks features small businesses use to do their accounting.

This guide explains features that are unique to QuickBooks Online. For info about the API and how it's modeled, see the [overview of the QuickBooks Online Accounting API](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api).

---

## Basic Bookkeeping in QuickBooks Online

Before you learn about specific QuickBooks Online features, we recommend you [learn basic bookkeeping and accounting concepts](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping).

---

## Unique QuickBooks Online Concepts and Features

As you develop, you'll encounter many accounting concepts. Most are based on general accounting knowledge. However, some are specific to or behave in ways that are unique to QuickBooks Online.

### Company Files

When users first sign up for QuickBooks Online, they create what's called a **"company file."** They use company files to organize all of their business activities and accounting data. Think of them like "profiles" for their business.

Company files store everything related to QuickBooks:
- Transactions
- Lists
- Sales forms
- Customer profiles
- Financial reports
- And much more

Company files usually track the activities for a single business. It's uncommon for a business to have multiple company files. Learn more [about company files](https://quickbooks.intuit.com/learn-support/en-us/manage-intuit-account/create-or-add-another-company/00/185919).

**How this relates to app development:**

All QuickBooks Online users have a company file. It's where all their data gets stored and the accounting happens.

> **Tip**: In our documentation, we sometimes refer to company files as a user's "company."

When users connect to your app and authorize it, they're connecting their company files, and its data, to your app. It's also what gives your app the access and refresh tokens needed to make API calls.

---

### Company Settings

Company settings define the attributes of a QuickBooks Online company file. This includes:
- Settings like the default currency or accounts for features
- Preferences and customizations like personalized account names

Users adjust their company settings in QuickBooks Online by selecting the **gear icon** and then **Account and settings**.

**How this relates to app development:**

While users call this their "company settings," the corresponding APIs use different names. Familiarize yourself with the available company settings and how they impact other APIs' behaviors. We note these effects [in the API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/most-commonly-used/account).

Use the [Preferences](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/preferences) and [CompanyInfo](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/companyinfo) entities to adjust company settings.

#### Common Preferences to Be Aware Of

| Preference | Description |
|------------|-------------|
| `Preferences.AccountingInfoPrefs.CustomerTerminology` | The term used by a company file for its customers. This string is used in many places throughout the QuickBooks UI related to sales activities. |
| `Preferences.AccountInfoPrefs.TrackDepartments` | A flag indicating whether department location is tracked on transactions. If enabled (true), the `DepartmentRef` attribute is available for transaction entities. |
| `Preferences.CurrencyPrefs.HomeCurrency` | The currency of the country where the business is physically located. This appears in the `CurrencyRef` attribute of transaction entities. |
| `Preferences.AccountInfoPrefs.ClassTrackingPerLine` and `ClassTrackingPerTxn` | Settings for [class tracking](https://developer.intuit.com/app/developer/qbo/docs/workflows/manage-business-units) on transaction entities. |
| `Preferences.SalesFormsPrefs.CustomTxnNumbers` | Lets apps specify custom transaction numbers. Transaction numbers surface in the `DocNumber` attribute of certain transaction resources. |
| `Preferences.ProductAndServicesPrefs` | A container with settings to enable and manage inventory tracking. |

---

### Financial Accounts

Financial accounts (often referred to as just "accounts") are how QuickBooks categorizes and organizes transactions.

The list of accounts a business uses to track transactions is known as [the chart of accounts](https://quickbooks.intuit.com/r/accounting-money/chart-accounts/). While there are many common accounts, each business will have a unique chart of accounts based on their industry and needs.

Learn more [about financial accounts](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping/accounts) in QuickBooks Online.

---

### People (Customers and Vendors)

Businesses constantly interact with two groups of people:
- **Customers**: Who they sell products and services to
- **Vendors**: Who they buy products or services from, including contractors

QuickBooks keeps customer and vendor lists so businesses always know who's connected to each transaction.

Learn more [about customers and vendors](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping/customers) in QuickBooks Online.

---

### Inventory

Some [versions of QuickBooks Online (also known as SKUs)](https://quickbooks.intuit.com/accounting/inventory/) come with inventory tracking and management features.

**Inventory items** are products a business sells and tracks quantities for in QuickBooks. Some businesses sell items that they don't track quantities for - these are considered **non-inventory**. This distinction is important since inventory items are tied to specific accounts.

Key inventory features:
- QuickBooks tracks the cost of individual items so users know their inventory's total value
- If inventory items are added to sales forms, purchase orders, and refund transactions, QuickBooks automatically adjusts the quantity on-hand

Learn more about [how inventory works in QuickBooks](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping/manage-inventory).

**How this relates to app development:**

Learn how to [create items and implement inventory features for your app](https://developer.intuit.com/app/developer/qbo/docs/workflows/manage-inventory).

---

### Sales and Purchase Tax

Taxes are tricky. Familiarize yourself with your region's tax laws so you can utilize tax features correctly.

**How this relates to app development:**

QuickBooks Online handles sales and purchase taxes in particular ways. The QuickBooks Online API tax model is a set of resources for managing taxes for transactions such as invoices, bills, purchase orders, and sales receipts. Refer to the [TaxCode](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/taxcode), [TaxRate](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/taxrate), and [TaxAgency](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/taxagency) entities.

These entities behave differently between US and non-US editions of QuickBooks Online:

- Learn more [about managing US-based sales tax](https://developer.intuit.com/app/developer/qbo/docs/workflows/calculate-sales-tax/automated-sales-tax-for-us-locales)
- Learn more [about the hybrid sales tax model](https://blogs.intuit.com/blog/2020/05/27/support-for-hybrid-sales-tax-available-in-the-api/)
- Learn more [about managing global (non-US) regional taxes](https://developer.intuit.com/app/developer/qbo/docs/workflows/calculate-sales-tax/automated-sales-tax-for-non-us-locales)

---

## Basic Accounting Workflows in QuickBooks Online

As an app developer, you may want to create tools that streamline one or more accounting tasks into a seamless experience for end-users.

Accounting involves many related tasks that follow specific sequences. We can call these groups of tasks **"workflows."** Some workflows involve only a few tasks while others involve more than a dozen.

We've created [guides for common workflows](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping) you can build your app around.

---

## Mercury Integration Notes

For the Mercury-QuickBooks sync plugin:

1. **Company Files**: When users authorize the Mercury plugin, they're connecting their QuickBooks company file. The plugin will store data (transactions, vendors) in their company file.

2. **Vendors**: Mercury payees (recipients of payments) should be created as QuickBooks Vendors. Use the Vendor entity to manage these.

3. **Accounts**: The plugin will need to map Mercury accounts to QuickBooks financial accounts:
   - Mercury bank accounts → QuickBooks Bank accounts
   - Expense categories → QuickBooks Expense accounts

4. **Preferences to Check**:
   - `Preferences.CurrencyPrefs.HomeCurrency` - Ensure currency matches Mercury transactions (typically USD)
   - `Preferences.AccountInfoPrefs.TrackDepartments` - If enabled, transactions can be categorized by department
