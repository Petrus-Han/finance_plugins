# QuickBooks Online API Release Notes

These are the latest release notes for the QuickBooks Online Accounting API.

## December 2023
**Platform release 2023.12.12**
- Allow use of the tax override feature without company level restrictions.

## June 2023
**Platform release 2023.6.21**
- Fix provided for Unmasking vendor TaxIdentifier.

## January 2023
**Platform release 2023.1.12**
- Added `projectRef` to Transaction and TimeActivity.

## October 2022
**Platform release 2022.10.26**
- Added support for COA Detail types for beta launch - Contra types with minor version 68.

## September 2022
**Platform release 2022.9.14**
- Added a new detail account type for other debtors.
- Resolved issues: Fix provided for NPE thrown for `paymentMethodRef`.

## August 2022
**Platform release 2022.8.31**
- Resolved issues: Fix provided for `BillableStatus` updates but `LastUpdatedTime` does not get updated.

## April 2022
**Platform release 2022.4.6**
- Resolved issues: QBO Payment Methods Name considered as Date Type.
- Query parser used for parsing V3 query requests does support special characters, emojis.

## March 2022
**Platform release 2022.3.8**
- Resolved issues: Added two new attributes `RevenueRecognitionEnabled` and `RecognitionFrequencyType` under `ProductAndServicePrefs`.
- Support for parsing special characters, emojis on V3 query requests.

## December 2021
**Platform release 2021.12.1**
- Resolved issues: Fix for creating Payment through V3 API using/applying an existing credit card credit.

## November 2021
**Platform release 2021.11.3**
- Resolved issues: Fix for Invoice/Sales Receipt/Estimate where creating transaction with Line1 and Line2 information for BillAddr and ShipAddr failed.

## October 2021
**Platform release 2021.10.20**
- Added support for Cost Rate for Time Activity, Employee, and Vendor using `mv=63`.

**Platform release 2021.10.7**
- Resolved issues: Fixed issue related to Multi Currency Transaction Amount Displayed as Home Currency.

## August 2021
**Platform release 2021.8.11**
- Resolved issues: Fixed inconsistent results for V3 Item query response.

## July 2021
**Platform release 2021.7.14**
- Added support for `OriginalTaxRateId`.
- Enhance V3 Time Activity API to include seconds precision.
- Added documentation for FEC Report API for FR locale.

## May 2021
**Platform release 2021.5.5**
- Added support for V3 TaxPayment API for Canada locale.
- Resolved issues: Fixed issue to display correct TxnType for linked expenses.

## March 2021
**Platform release 2021.3.24**
- Added support for returning Timeactivity in CDC (Change Data Capture) API response.

**Platform release 2021.3.11**
- Added support for `source` field with `minorversion=59` in Customer, Vendor, and Item entity to support QuickBooks Commerce changes.
- Objects created by QuickBooks Commerce are read-only.
- Objects created by QuickBooks Commerce cannot be used when creating a new Transaction.

## February 2021
**Platform release 2021.2.24**
- Resolved issues: Fixed issue for imported Refund Receipts; Fixed issue for Account entity `AccNum` length.

**Platform release 2021.2.11**
- Resolved issues: Fixed issue for service date in group line item for Invoice.

## January 2021
**Platform release 2021.1.6**
- Added support for `TaxSlipType` on Vendor entity in CA region (`minorversion=56`).
- Resolved issues: Fixed issue for active filter in TaxCode.

## December 2020
**Platform release 2020.12.10**
- Added support for removing `ExpenseAccountRef` and setting `PurchaseCost` as 0 for Item.
- Resolved issues: Fixed issue for Duplicate doc number error message TxnType.

## September 2020
**Platform release 2020.9.23**
- Added support for **Reimburse Charge** entity.
- Added support for `TaxSlipType` on Vendor Entity (`minorversion=56`).

## August 2020
**Platform release 2020.8.27**
- Added support for new fields to `CreditCardPayment`: `VendorRef`, `CheckNum`, `PrintStatus`, and `Memo` (`minorversion=54`).

**Platform release 2020.8.13**
- Added support for Create and Delete operations for `RecurringTransaction`.
- Added support for TaxExclusive and TaxInclusive on `JournalEntry` for AU locale.

## June 2020
**Platform release 2020.6.30**
- Added support for new entity **RecurringTransaction** (`minorversion=52`).
- Added support for merge operation for Account entity.

## May 2020
**Platform release 2020.5.19**
- Added support for Hybrid Sales Tax experience (`minorversion=51`).

## February 2020
**Platform release 2020.2.13**
- Added support for new entity **TaxPayment** (`minorversion=47`).
- Added support for new entity **CreditCardPayment**.

## December 2017
- **Automated Sales Tax (AST)**: All new US companies manage sales tax via AST engine.
