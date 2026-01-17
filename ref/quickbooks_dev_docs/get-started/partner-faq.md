# Intuit App Partner Program FAQ

> **Source**: https://developer.intuit.com/app/developer/qbo/docs/get-started/partner-faq

## General Program

### What is the new Intuit App Partner Program?

The Intuit App Partner Program is a transformative update to our platform, designed to accommodate partners of all sizes with different levels of engagement. It introduces four distinct partner tiers, with a set of benefits tailored to different levels of engagement. The program introduces an improved developer experience, access to new APIs, go-to-market support, and the implementation of platform service fees*.

*Geographical availability of the Intuit App Partner Program varies, and different rates may apply. Feature availability varies by tier, with some benefits requiring onboarding that may delay activation. Additional terms, fees, eligibility requirements, and conditions apply.*

### When did the Intuit App Partner Program officially launch?

The new program launched in the US on July 28, 2025. On November 3, 2025, we're expanding the Intuit App Partner Program to our partners in the United Kingdom, Australia, and Canada (excluding Quebec).

### Are all apps automatically part of the Intuit App Partner Program? Can I opt out?

All apps are automatically enrolled in the Intuit App Partner Program at the Builder tier. Currently, there's no method to opt out, but the Builder tier is an uncharged tier. However, the Builder tier is subject to a capped limit of CorePlus API calls.

### My team has a strategic integration with Intuit. Will my app be subject to platform fees?

Contact your Partner Development Manager at Intuit to determine whether your app will be subject to platform service fees under the Intuit App Partner Program.

### What's the difference between the QuickBooks Solution Provider program and the new Intuit App Partner Program?

The Intuit App Partner Program and the Intuit QuickBooks Solution Provider (QSP) program are two separate programs that provide unique benefits and features. If you are both an Intuit QuickBooks Solution Provider and an Intuit App Developer, contact your QSP representative at Intuit to learn how these programs compare.

---

## Tiers and Benefits

### Partner Tier Overview

The program includes four tiers: **Builder**, **Silver**, **Gold**, and **Platinum**. Each tier offers a unique set of benefits designed to provide the resources, support, and growth opportunities needed to thrive in our ecosystem. For the full list of benefits and features, see the Intuit App Partner Program Guide.

### What happens if I'm currently listed on the Intuit App Marketplace but am not a Silver, Gold, or Platinum partner?

If you're currently listed on the Intuit App Marketplace but you are a Builder partner, your app listing will temporarily remain in place, but is subject to removal from the Intuit App Marketplace. To avoid a delisting, you must subscribe to Silver.

### How do I know what partner tier my app is in?

Your partner tier will be displayed on the Intuit Developer Portal. As long as you meet the tier requirements, you are eligible to subscribe to that tier.

**Tier Requirements:**
- **Compliance**: You must complete an Intuit-approved app assessment questionnaire, accept the updated Intuit Developer Terms of Service, and comply with the Intuit App Partner Program.
- **Payment method**: You must provide and maintain a valid payment method (credit card, ACH, Pre-authorized Debit, or Direct Debit).
- **App Marketplace listing**: You must have an active listing on the Intuit App Marketplace in at least one region. *This requirement is temporarily deferred until August 1, 2026.*
- **Active connections**: Defined as individual QuickBooks Online or Intuit Enterprise Suite companies with active subscriptions and valid, non-expired OAuth tokens.

### Are the partner tiers determined at the app level or at the workspace level?

The partner tiers are determined at the **workspace level**. If you have multiple production apps under one workspace, the connections will be aggregated and used to determine tier qualification.

### How do I qualify for the next partner tier?

If you meet the eligibility requirements of a higher tier, you can request an upgrade at any time. However, Program Eligibility Checkpoints occur twice per year. For details, see the Intuit App Partner Program Guide.

### Do I automatically get upgraded to the next tier if I meet the tier requirements?

- Partners in the **Builder tier** can choose to subscribe to the **Silver tier** and be automatically upgraded upon providing a valid payment method.
- Upgrades to the **Gold and Platinum tiers** are not automatic and require review.

### Can I cancel my subscription?

Yes. You can cancel your subscription from within the Intuit Developer Portal at any time. If you cancel, you can continue to use your tier's benefits until your next Billing Cycle, at which point you will be placed into the Builder tier.

---

## New APIs

### Will there be new APIs released as part of the Intuit App Partner Program?

Yes! We recently launched several useful new premium APIs:

| API | Description |
|-----|-------------|
| **Projects API** | Create Projects and track profitability (available in QBO Plus, Advanced, Accountant, and Intuit Enterprise Suite) |
| **Custom Fields API** | Access up to 12 custom fields that can be used across different transactions |
| **Sales Tax API** | Automatically calculate correct sales tax for invoices and other transactions |
| **Payroll Compensation API** | Access multiple pay types (salary, hourly, overtime, holiday, etc.) for enhanced Time Tracking |
| **Inventory Adjustment API** | Change quantity of inventory items for damage, stock write-off, shrinkage, or expiration |

---

## Fees

### What types of fees will my app be subject to?

Platform Service Fees consist of two components:
1. **Monthly Program Fee**: A flat monthly fee that differs per partner tier, unlocking specific benefits and CorePlus API credits
2. **Variable API Fee**: Charged for usage of certain APIs above the CorePlus API credits available to your tier

The **Builder tier** is not charged and is excluded from Platform Service Fees.

### What's the difference between Core and CorePlus APIs?

| Type | Description | Metering |
|------|-------------|----------|
| **Core API calls** | Most data-in operations (creating/updating invoices, bills, customers, vendors, etc.) | Unmetered and uncharged |
| **CorePlus API calls** | Most data-out operations (reading accounts, querying company info, fetching reports) | Metered, charges may apply |

### What's the maximum number of API calls at the uncharged tier?

By default, all partners begin in the **Builder tier** and are afforded **500,000 CorePlus API calls per month** without incurring any charges. Calls above this allotment will be blocked. To make additional calls, upgrade to the Silver tier.

### Are there APIs where fees do not apply?

Yes. The following APIs will not be metered and will not be subject to variable API fees:
- Payments API
- Desktop API
- Payroll API
- All OAuth endpoints (discovery document, access token, refresh, revoke, userinfo, JWKS)
- All sandbox endpoints

---

## Usage and Metrics

### When will Intuit start to track my API usage?

CorePlus API metering begins November 3, 2025, for partners in the US, Canada (excluding Quebec), UK, and Australia.

### Where can I find metrics on my API usage?

An API usage chart is available on the Intuit Developer Portal. Under each app, navigate to the **Analytics tab** to view API calls by category (Core and CorePlus).

### Will calls to the sandbox API be metered and charged?

**No.** Only production API calls will be metered and charged.

### Will API calls to QuickBooks Online free trial accounts be metered and charged?

**Yes.** All production API calls will be metered regardless of the subscription status of the QuickBooks Online company.

### Will calls that error out be metered and charged?

**No.** Intuit will only meter and charge for successful API calls in production.

### Is API usage metered at the app or workspace level?

API usage is metered at the **app level** and aggregated at the **workspace level**. If you have multiple production apps within one workspace, all usage will be aggregated.

---

## Billing

### What is the billing cycle for the Developer Platform Service Fees?

A Billing Cycle date is defined from the date you enter a payment method and subscribe to a paid tier:
- **Flat Program Fees** are charged monthly in advance
- **Variable API Fees** are charged at the end of the Billing Cycle

### What payment methods are accepted?

- Credit Card
- ACH (US)
- Pre-authorized Debit (PAD) (Canada)
- Direct Debit (UK, Australia)

### Do I need to provide credit card information if I'm at the Builder tier?

**No.** You don't need to provide a payment method if you are at the Builder tier. However, if you make more than 500,000 CorePlus API calls in a one-month period, you will need to upgrade to the Silver tier to continue calling APIs at the same rate.

### If I have multiple apps, will I get a separate bill for each app?

A bill is sent for each **workspace**. If you have three apps in one workspace, you receive one bill with usage aggregated across all three apps. If you have three workspaces with an app in each, you receive three separate invoices.

---

## Resources

### How do I access the Partner Resource Center?

As part of the program, you'll gain access to the Intuit Partner Resource Center (PRC), designed to support your QuickBooks marketing needs. Feature and benefit availability varies by tier, with some benefits requiring onboarding. Look for a Welcome email from no-reply@partnerprogram.intuit.com to set up your license.

---

## Mercury Integration Notes

For the Mercury-QuickBooks sync plugin:

1. **API Tier Considerations**: The Mercury sync plugin will primarily make CorePlus API calls (reading accounts, querying existing vendors, etc.). Monitor usage to stay within the Builder tier's 500,000 monthly limit or plan for Silver tier subscription.

2. **Core vs CorePlus Classification**:
   - **Core (free)**: Creating Purchases, creating Deposits, creating Vendors
   - **CorePlus (metered)**: Querying Vendors, reading Accounts, fetching CompanyInfo

3. **Sandbox Testing**: Sandbox API calls are not metered, so development and testing are free.

4. **Optimization**: To minimize CorePlus API usage, cache frequently-accessed data (like account mappings and vendor lists) rather than querying on every transaction sync.
