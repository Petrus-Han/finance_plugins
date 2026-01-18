# QuickBooks Online API Documentation

> Scraped from https://developer.intuit.com/app/developer/qbo/docs/

## Documentation Structure

```
quickbooks_dev_docs/
├── README.md                          # This file - main index
├── get-started/                       # Getting started guides (10 files)
├── learn/                             # Concepts and basics (12 files)
├── develop/                           # Development guides (9 files)
├── use-cases/                         # Workflow examples (7 files)
├── publish-and-list/                  # App Store publishing (20 files)
├── legal-agreements/                  # Terms of service and policies (4 files)
├── release-notes/                     # API and platform updates (4 files)
└── api-reference/                     # Entity & Report documentation (77 files)
```

## Quick Reference

### Base URLs

| Environment | URL |
|-------------|-----|
| **Production** | `https://quickbooks.api.intuit.com` |
| **Sandbox** | `https://sandbox-quickbooks.api.intuit.com` |

### URI Format

| Operation | Method | URI Pattern |
|-----------|--------|-------------|
| Create/Update | POST | `/v3/company/{realmId}/{entity}` |
| Read (single) | GET | `/v3/company/{realmId}/{entity}/{id}` |
| Query (multi) | GET | `/v3/company/{realmId}/query?query={sql}` |
| Delete | POST | `/v3/company/{realmId}/{entity}?operation=delete` |

### Required Headers

```http
Authorization: Bearer {access_token}
Content-Type: application/json
Accept: application/json
```

---

## Mercury-QuickBooks Sync - Key Entities

For the Mercury-QuickBooks sync plugin, these are the critical entities:

| Mercury Transaction | QuickBooks Entity | Documentation |
|---------------------|-------------------|---------------|
| Outgoing payment | **[Purchase](api-reference/purchase.md)** | Record expenses (Cash, Check, CreditCard) |
| Incoming payment | **[Deposit](api-reference/deposit.md)** | Record income/deposits |
| Payment recipient | **[Vendor](api-reference/vendor.md)** | Create/match payees |
| Payment sender | **[Customer](api-reference/customer.md)** | Create/match payers |
| Internal transfer | **[Transfer](api-reference/transfer.md)** | Move funds between accounts |
| Bank account | **[Account](api-reference/account.md)** | Map Mercury accounts |

---

## Complete File Index

### 1. Get Started
- [README](get-started/README.md)
- [App Settings](get-started/app-settings.md)
- [Build Your First App](get-started/build-your-first-app.md)
- [Create a Request](get-started/create-a-request.md)
- [Developer Account Settings](get-started/developer-account-settings.md)
- [Get Client ID and Client Secret](get-started/get-client-id-and-client-secret.md)
- [Get Started with the API Explorer](get-started/get-started-with-the-api-explorer.md)
- [Partner FAQ](get-started/partner-faq.md)
- [Share Workspace](get-started/share-workspace.md)
- [Start Developing Your App](get-started/start-developing-your-app.md)

### 2. Learn
- [README](learn/README.md)
- [Explore the QuickBooks Online API](learn/explore-the-quickbooks-online-api.md)
- [Batch](learn/explore-the-quickbooks-online-api/batch.md)
- [Change Data Capture](learn/explore-the-quickbooks-online-api/change-data-capture.md)
- [Data Queries](learn/explore-the-quickbooks-online-api/data-queries.md)
- [Minor Versions](learn/explore-the-quickbooks-online-api/minor-versions.md)
- [Learn About GraphQL](learn/learn-about-graphql.md)
- [Learn Basic Bookkeeping](learn/learn-basic-bookkeeping.md)
- [Learn Basic Field Definitions](learn/learn-basic-field-definitions.md)
- [Learn QuickBooks Online Basics](learn/learn-quickbooks-online-basics.md)
- [REST API Features](learn/rest-api-features.md)
- [Scopes](learn/scopes.md)

### 3. Develop
- [README](develop/README.md)
- [Authentication](develop/authentication.md)
- [OAuth 2.0](develop/authentication-and-authorization/oauth-2.0.md)
- [Postman](develop/postman.md)
- [Sandbox FAQs](develop/sandbox-faqs.md)
- [Sandboxes](develop/sandboxes.md)
- [SDKs and Samples](develop/sdks-and-samples.md)
- [Troubleshooting](develop/troubleshooting.md)
- [Webhooks](develop/webhooks.md)

### 4. Use Cases
- [README](use-cases/README.md)
- [Categorize Income and Expenses](use-cases/categorize-income-and-expenses.md)
- [Create Invoice](use-cases/create-invoice.md)
- [Manage Linked Transactions](use-cases/manage-linked-transactions.md)
- [Mercury Sync Patterns](use-cases/mercury-sync-patterns.md)
- [Run Reports](use-cases/run-reports.md)

### 5. API Reference (Entities & Transactions)
- [Account](api-reference/account.md)
- [Attachable](api-reference/attachable.md)
- [Batch](api-reference/batch.md)
- [Bill](api-reference/bill.md)
- [BillPayment](api-reference/billpayment.md)
- [ChangeDataCapture](api-reference/changedatacapture.md)
- [Class](api-reference/class.md)
- [CompanyCurrency](api-reference/companycurrency.md)
- [CompanyInfo](api-reference/companyinfo.md)
- [CreditCardPayment](api-reference/creditcardpayment.md)
- [CreditMemo](api-reference/creditmemo.md)
- [Customer](api-reference/customer.md)
- [CustomerType](api-reference/customertype.md)
- [Department](api-reference/department.md)
- [Deposit](api-reference/deposit.md)
- [Employee](api-reference/employee.md)
- [Entitlements](api-reference/entitlements.md)
- [Estimate](api-reference/estimate.md)
- [Exchangerate](api-reference/exchangerate.md)
- [InventoryAdjustment](api-reference/inventoryadjustment.md)
- [Invoice](api-reference/invoice.md)
- [Item](api-reference/item.md)
- [JournalCode](api-reference/journalcode.md)
- [JournalEntry](api-reference/journalentry.md)
- [Payment](api-reference/payment.md)
- [PaymentMethod](api-reference/paymentmethod.md)
- [Preferences](api-reference/preferences.md)
- [Purchase](api-reference/purchase.md)
- [PurchaseOrder](api-reference/purchaseorder.md)
- [RecurringTransaction](api-reference/recurringtransaction.md)
- [RefundReceipt](api-reference/refundreceipt.md)
- [ReimburseCharge](api-reference/reimbursecharge.md)
- [SalesReceipt](api-reference/salesreceipt.md)
- [TaxAgency](api-reference/taxagency.md)
- [TaxClassification](api-reference/taxclassification.md)
- [TaxCode](api-reference/taxcode.md)
- [TaxPayment](api-reference/taxpayment.md)
- [TaxRate](api-reference/taxrate.md)
- [TaxService](api-reference/taxservice.md)
- [Term](api-reference/term.md)
- [TimeActivity](api-reference/timeactivity.md)
- [Transfer](api-reference/transfer.md)
- [Vendor](api-reference/vendor.md)
- [VendorCredit](api-reference/vendorcredit.md)

### 6. API Reference (Reports)
- [AccountListDetail](api-reference/accountlistdetail.md)
- [APAgingDetail](api-reference/apagingdetail.md)
- [APAgingSummary](api-reference/apagingsummary.md)
- [ARAgingDetail](api-reference/aragingdetail.md)
- [ARAgingSummary](api-reference/aragingsummary.md)
- [BalanceSheet](api-reference/balancesheet.md)
- [Budget](api-reference/budget.md)
- [CashFlow](api-reference/cashflow.md)
- [CustomerBalance](api-reference/customerbalance.md)
- [CustomerBalanceDetail](api-reference/customerbalancedetail.md)
- [CustomerIncome](api-reference/customerincome.md)
- [FECReport](api-reference/fecreport.md)
- [GeneralLedger](api-reference/generalledger.md)
- [GeneralLedgerFR](api-reference/generalledgerfr.md)
- [InventoryValuationDetail](api-reference/inventoryvaluationdetail.md)
- [InventoryValuationSummary](api-reference/inventoryvaluationsummary.md)
- [JournalReport](api-reference/journalreport.md)
- [JournalReportFR](api-reference/journalreportfr.md)
- [ProfitAndLoss](api-reference/profitandloss.md)
- [ProfitAndLossDetail](api-reference/profitandlossdetail.md)
- [SalesByClassSummary](api-reference/salesbyclasssummary.md)
- [SalesByCustomer](api-reference/salesbycustomer.md)
- [SalesByDepartment](api-reference/salesbydepartment.md)
- [SalesByProduct](api-reference/salesbyproduct.md)
- [TaxSummary](api-reference/taxsummary.md)
- [TransactionList](api-reference/transactionlist.md)
- [TransactionListByCustomer](api-reference/transactionlistbycustomer.md)
- [TransactionListByVendor](api-reference/transactionlistbyvendor.md)
- [TransactionListWithSplits](api-reference/transactionlistwithsplits.md)
- [TrialBalance](api-reference/trialbalance.md)
- [VendorBalance](api-reference/vendorbalance.md)
- [VendorBalanceDetail](api-reference/vendorbalancedetail.md)
- [VendorExpenses](api-reference/vendorexpenses.md)

### 7. Legal Agreements
- [README](legal-agreements/README.md)
- [Intuit Developer Terms of Service](legal-agreements/intuit-terms-of-service-for-intuit-developer-services.md)
- [Intuit AppConnect Library Partner Sites](legal-agreements/intuit-appconnect-library-partner-sites.md)
- [Password Policy for Intuit Developer Services](legal-agreements/password-policy-for-intuit-developer-services.md)

### 8. Release Notes
- [README](release-notes/README.md)
- [General Release Notes](release-notes/general-release-notes.md)
- [Accounting API Release Notes](release-notes/platform-release-notes.md)
- [SDK and Client Library Release Notes](release-notes/sdk-release-notes.md)

---

## Authentication

QuickBooks uses **OAuth 2.0**. See [develop/authentication.md](develop/authentication.md) for full guide.

### Quick OAuth Flow

1. Redirect user to authorization URL
2. User approves, callback receives `code` and `realmId`
3. Exchange code for access token (1 hour) and refresh token (100 days)
4. Use access token in `Authorization: Bearer {token}` header
5. Refresh token before expiry

### Required Scope

```
com.intuit.quickbooks.accounting
```

---

## Official Resources

- [Intuit Developer Portal](https://developer.intuit.com/)
- [API Explorer](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account)
- [OAuth 2.0 Documentation](https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization)
- [Sandbox Documentation](https://developer.intuit.com/app/developer/qbo/docs/develop/sandboxes)
- [SDKs and Samples](https://developer.intuit.com/app/developer/qbo/docs/develop/sdks-and-samples)

---

*Last updated: 2025-01-17*
