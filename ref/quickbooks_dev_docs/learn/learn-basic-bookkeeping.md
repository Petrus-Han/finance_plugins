# Learn Basic Bookkeeping and Accounting in QuickBooks Online

> **Source**: https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping

## Overview

The [QuickBooks Online Accounting API](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api) lets you access most of the customer-facing features small businesses use to do their accounting.

This guide covers basic accounting concepts. For info about the API and how it's modeled, see the [overview of the QuickBooks Online Accounting API](https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api).

---

## Basic Bookkeeping in QuickBooks Online

QuickBooks Online gives users powerful tools to track all of their financial activities. Here's an overview of fundamental features:

- **[Sales forms](https://quickbooks.intuit.com/learn-support/en-us/customize-forms/description-of-quickbooks-online-forms/00/188609)**: Let them start and track sales transactions
- **[Lists](https://www.youtube.com/watch?v=o37ubBaS1Lk)**: Keep track of their customers, vendors, inventory, etc.
- **[Financial accounts](https://quickbooks.intuit.com/learn-support/en-us/manage-fixed-assets/understand-the-chart-of-accounts-in-quickbooks/00/203681)**: QuickBooks records and categorizes transactions into these
- **[Chart of accounts](https://quickbooks.intuit.com/r/accounting-money/chart-accounts/)**: All financial accounts make up this
- **[General ledger](https://quickbooks.intuit.com/r/bookkeeping/whats-general-ledger-need-one/)**: Keeps a record of all business activities

### Double-Entry Bookkeeping

QuickBooks is based on **double-entry bookkeeping**. This is a very common accounting system in the US and many other countries.

With double-entry bookkeeping, all records involve two (or more) related accounts. Accounts serve as reference points for transactions. Any time a user creates or updates a record in QuickBooks, it **increases** the value of one account and **decreases** the same value of a corresponding account.

**Examples:**

- When a small business sells a product or service, its "Cash" account increases by the profit from the sale. The income account that tracks income from sales also increases by this amount.
- Additionally, if the business sold a product, the account that tracks product inventory (usually called the "Inventory Asset" account) decreases by one item.
- When a small business pays rent, its "Cash" account decreases by the amount spent. The expense account that tracks rent expenses, in this case called the "Rent or lease" account, increases by the same amount.

> **Tip**: These increases and decreases are often called "debits" and "credits." Debits and credits can either increase or decrease the value of an account. What gets debited or credited depends on the types of transactions and accounts involved. Learn more about [debits and credits](https://quickbooks.intuit.com/r/bookkeeping/debit-vs-credit/).

Since double-entry bookkeeping tracks both increases and decreases, businesses get a comprehensive view of their finances. Learn more about [double-entry bookkeeping](https://quickbooks.intuit.com/r/bookkeeping/complete-guide-to-double-entry-bookkeeping/).

### Additional Resources

- [Learn common accounting terms from QuickBooks Online Support](https://quickbooks.intuit.com/learn-support/en-us/accounting-topics/learn-common-accounting-terms/00/186089)
- [Learn about basic accounting from the QuickBooks Resource Center](https://quickbooks.intuit.com/r/accounting-money/)
- [Learn about basic bookkeeping from the QuickBooks Resource Center](https://quickbooks.intuit.com/r/bookkeeping/)

---

## Common Accounting Workflows in QuickBooks Online

As an app developer, you may want to create tools that streamline one or more accounting tasks into a seamless experience for end-users.

Accounting involves many interrelated tasks that follow specific sequences. We can call these groups of tasks **"workflows."** Some workflows involve only a few tasks while others involve more than a dozen.

We've created [guides for common workflows](https://developer.intuit.com/app/developer/qbo/docs/workflows) you can use as foundations for your app.

---

## Learn More About Specific Accounting Concepts

### Invoicing

Creating and sending invoices to customers, adding items, accepting payments, and more.

**Learn more:**
- [Learn the concept](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping/invoicing)
- [Integrate basic invoicing features](https://developer.intuit.com/app/developer/qbo/docs/develop/basic-implementations/basic-invoicing-implementation)

**Key tasks:**
- Create invoices
- Add items to invoices
- Assign income and sales accounts
- Email invoices to customers
- Receive payments for invoices

---

### Reporting

Creating and analyzing financial reports.

**Learn more:**
- [Learn the concept](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping/business-analytics)
- [Integrate basic reporting features](https://developer.intuit.com/app/developer/qbo/docs/develop/basic-implementations/basic-reporting-implementation)

**Key tasks:**
- Run reports
- Customize reports
- Understand reports types (balance sheet, profit and loss, year-end reports)

---

### Items and Inventory

Creating items (inventory, non-inventory, service), tracking quantities, reordering, and more.

**Learn more:**
- [Learn the concept](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping/manage-inventory)
- [Integrate basic inventory features](https://developer.intuit.com/app/developer/qbo/docs/develop/basic-implementations/basic-inventory-implementation)

**Key tasks:**
- Enter items into QuickBooks
- Create inventory items
- Create invoices for inventory items
- Understand cost of goods sold (COGS) and quantity on-hand

---

### Bills and Expenses

Creating bills and linking bill payments.

**Learn more:**
- [Learn the concept](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping/pay-bills)
- [Integrate basic billing features](https://developer.intuit.com/app/developer/qbo/docs/develop/basic-implementations/basic-billing-implementation)

**Key tasks:**
- Create bills
- Assign expense accounts
- Create bill payments to pay for bills
- Add vendor credits for excess payments

---

### Financial Accounts and Customers

Creating and managing accounts and customers so you can associate them with transactions.

**Learn more:**
- [Learn about accounts](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping/accounts)
- [Learn about customers and vendors](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-basic-bookkeeping/customers)

**Key tasks:**
- Create accounts
- Assign account types and detail types
- Enter customer info into QuickBooks

---

## Mercury Integration Notes

For the Mercury-QuickBooks sync plugin:

1. **Double-Entry Bookkeeping**: When syncing Mercury transactions:
   - **Purchases** (expenses): Decrease "Bank" account, Increase "Expense" account
   - **Deposits** (income): Increase "Bank" account, Increase "Income" account

2. **Key Entities for Mercury Sync**:
   - **Purchase**: Record Mercury outgoing transactions
   - **Deposit**: Record Mercury incoming transfers
   - **Vendor**: Create/manage payees from Mercury transactions
   - **Account**: Map Mercury accounts to QuickBooks bank accounts

3. **Chart of Accounts**: Users will need to map their Mercury bank account to a corresponding QuickBooks Bank account in their chart of accounts.

4. **Vendor Management**: Mercury payees should be created as QuickBooks Vendors before creating Purchases referencing them.
