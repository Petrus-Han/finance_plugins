# QuickBooks Online Release Notes

These are the latest QuickBooks Online release notes, including new features and changes to APIs, the app store, and documentation.

## September 2025

### Updated technical requirements
We’ve updated the technical requirements documentation for listing your app on the QuickBooks App Store. See [Technical requirements](../publish-and-list/publish-app/technical-requirements.md).

### New documentation for Payroll and Time API
We’ve enhanced our Payroll and Time API documentation. To start developing your Payroll and Time app, see Get started with the Payroll and Time API.

## August 2025

### Deprecated fields
The `source` field in the [Customer](../api-reference/customer.md) and [Vendor](../api-reference/vendor.md) entities is no longer supported and will no longer be returned in the API response. This field will be deprecated in production on September 15, 2025, and was deprecated in sandbox on August 15, 2025.

### Updated API call limits and throttles
API call limits and throttles have been updated. See [API call limits and throttles](../learn/rest-api-features.md#limits-and-throttles).

## July 2025

### New features

#### Intuit Partner Program
The Intuit Partner Program provides a new paradigm for app development and deployment, including new APIs and a new usage structure. For more information, see the [Intuit App Partner Program FAQ](../get-started/partner-faq.md).

#### App Partner Program menu
The App Partner Program menu, accessible in your Developer Portal, provides links to an overview and tiers and pricing pages.

#### New APIs
We’ve introduced four new GraphQL APIs:
- **Project API**: Build app integrations to manage and track projects.
- **Custom Fields API**: Improved support for custom fields. Depending on your QuickBooks Online product, you can add up to 12 custom fields.
- **Sales Tax API**: Automatically calculate sales tax.
- **Time API with Payroll Compensation**: Enhanced time tracking with multiple pay types.

#### Notable documentation changes

- **New Learning GraphQL section**: Background information on using GraphQL.
- **New Develop with GraphQL section**: Section to help integrate with the new GraphQL APIs.

## June 2025

### New Intuit App Partner Program features and documentation
- Tiers, benefits, and a program guide are now available.
- Subscription and billing workflows are now available. See the [Intuit App Partner Program FAQ](../get-started/partner-faq.md).

### API usage chart
Created an API usage chart to monitor and analyze API calls over time.

### Updated terms of service
The QuickBooks Online terms of service has been updated. See [Intuit Developer Terms of Service](../legal-agreements/intuit-terms-of-service-for-intuit-developer-services.md).

## May 2025

### FAQ for the Intuit App Partner Program
See the [Intuit App Partner Program FAQ](../get-started/partner-faq.md).

## February 2025

### Notable documentation changes
Added a new page describing how to use webhooks with the Payroll API.

## January 2025

### New minor versions
Added new minor versions 74 and 75. See [Minor version summary](../learn/explore-the-quickbooks-online-api/minor-versions.md#minor-version-summary).

### Notable documentation changes
- Clarified usage of request ID and batch ID.
- Updated payment processing information to include eCheck transactions.

## December 2024

### Notable documentation changes
Clarified throttling limits for sandbox and production servers.

## November 2024

### Updated terms of service
See [Intuit Terms of Service](../legal-agreements/intuit-terms-of-service-for-intuit-developer-services.md).

### Notable documentation changes
- Added additional permitted operations that support webhooks.
- Added documentation for additional CompanyInfo name/value pairs: `IsQbdtMigrated`, `MigrationDate`, `QBOIndustryType`, and `AssignedTime`. See [CompanyInfo](../api-reference/companyinfo.md).

## October 2024

### Notable documentation changes
- Clarifications for `GlobalTaxCalculation`.
- Improvements to SDK documentation.
- Added details for `TransactionList` fields.
- Clarifications for `invalid_grant` errors.
- Updates to Industry and Language requirements.

## September 2024

### New features

#### New Intuit Developer portal
Enhanced experience with a more intuitive design.

#### New Inventory Adjustment endpoint
Allows ensuring inventory quantities reflect correctly. See [InventoryAdjustment](../api-reference/inventoryadjustment.md).

### Notable documentation changes
New documentation for shared workspace. See [Create a workspace team](../get-started/share-workspace.md).

## July 2024

### Notable documentation changes
- Enhanced item inventory documentation.
- New reference information for [InventoryValuationDetail](../api-reference/inventoryvaluationdetail.md).
- Reorganized release notes.

## June 2024

### Notable documentation changes
New Payroll API documentation.

## April 2024

### Feature changes
Industry and language are now required for app listing.

### Notable documentation changes
Updated information on how to use the `realmID` and `revoke` endpoint.
