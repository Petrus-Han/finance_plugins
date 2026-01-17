# Minor Versions of Our API

> Source: https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api/minor-versions

The QuickBooks Online Accounting API supports past versions of our API through "minor versions" to make incremental changes.

You can use minor version queries to access a specific version of an API entity that's stable with your app. Using minor versions is optional.

> **Important**: We will be discontinuing support for minor versions 1 through 74 beginning **August 1, 2025**. Review your app's usage and make necessary updates before July 31, 2025.

---

## How Minor Versions Work

- You can use the minor version of any API entity
- Recommended: Work with only one minor version at a time to avoid schema conflicts
- Access minor versions on a per resource basis
- If you don't use a minor version, you'll use the **base version** by default
- SDKs automatically use the latest version of the API schema

---

## How to Use Minor Versions with SDKs

The SDK version automatically gives you the latest features and all prior versions.

### .NET SDK

```csharp
ServiceContext context = new ServiceContext(appToken, realmId, intuitServiceType, reqvalidator);
context.IppConfiguration.MinorVersion.Qbo = "28";
```

### Java SDK

```java
context = new Context(oauth, appToken, ServiceType.QBO, realmID);
context.setMinorVersion("8");
```

> **Important**: SDKs default to the latest API version unless you reference a specific minor version.

---

## How to Use Minor Versions Without an SDK

Use the minor version query parameter:

```
https://quickbooks.api.intuit.com/v3/company/<realmId>/<apiEntity>/entityId?minorversion=<#>
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `realmId` | Company ID of the QuickBooks Online company |
| `apiEntity` | Name of the entity |
| `#` | Minor version number |

### Example

```
https://quickbooks.api.intuit.com/v3/company/123456789/journalentry/entityId?minorversion=1
```

---

## Current Minor Versions (Latest)

| Minor Version | Release Date | Key Features |
|---------------|--------------|--------------|
| **75** | Dec 16, 2024 | Added `DefaultTimeZone` field to CompanyInfo entity |
| **74** | Dec 5, 2024 | API update to use company's default service item if item ID not provided in TimeActivity |
| **73** | Jun 24, 2024 | API support for project estimate |
| **71** | Mar 21, 2024 | Added support for TimeActivity TimeChargeId field |
| **70** | Dec 12, 2023 | Override sales tax without company level restrictions (US) |
| **69** | Jan 12, 2023 | Query support for projectRef filter |
| **68** | Oct 26, 2022 | MTD COA Detail types for beta launch |
| **67** | Sep 14, 2022 | New detail account type for other debtors |
| **65** | May 11, 2022 | RevenueRecognitionEnabled, RecognitionFrequencyType; special characters/emojis in queries |
| **63** | Oct 20, 2021 | Cost Rate for Time Activity, Employee, and Vendor |
| **62** | Jul 14, 2021 | OriginalTaxRateId in TaxRate; seconds precision in Time Activity |

---

## Key Historical Minor Versions

| Minor Version | Features |
|---------------|----------|
| **59** | Source field on list entities |
| **55** | ReimburseCharge entity support |
| **53** | Recurring Transaction Create/Delete; GlobalTaxCalculation for AU |
| **52** | Recurring Transaction Read |
| **47** | Tax Payment Service (AU/UK only) |
| **44** | Override sales tax (US with company settings) |
| **41** | Associate Class with Item |
| **38** | Link BillPayment to JournalEntry; Bill to multiple Purchase Orders |
| **36** | Payment link for Invoices via API |
| **35** | ShipFromAddr for Automated Sales Tax |
| **33** | GST compliant invoices for India |
| **21** | Preferences parity with UI; FreeFormAddress |
| **14** | Invoice deposit validation |
| **8** | CC and BCC email addresses in Invoice |
| **4** | Enhanced inventory (Item.Sku, NonInventory, line-level discounts) |

---

## Recommended Minor Version

For new applications, use the **latest minor version** (currently 75) to access all features.

For existing applications:
- If using SDK: Update SDK to get latest features
- If not using SDK: Specify `minorversion=75` in requests

---

## Learn More

- [API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [REST API Features](../rest-api-features.md)
