# Manage Linked Transactions

> Source: https://developer.intuit.com/app/developer/qbo/docs/workflows/manage-linked-transactions

QuickBooks relates a sales or purchase transaction with its supporting transactions via the linked transaction mechanism. For example, a payment applied to a given invoice is considered a linked transaction to that invoice.

This tutorial shows how the QuickBooks Online API uses linked transactions and what information they supply to an Invoice object. It also explains what impact a linked transaction has on QuickBooks company accounts and how a customer's payment maps to linked transactions in the accounting model.

## Prerequisites

To follow along, you'll need a sandbox or another QuickBooks company populated with:
- A chart of accounts
- Customers
- Invoices
- Payments

---

## Linked Transaction Summary

A linked transaction is realized in the QuickBooks Online API with the `LinkedTxn` element. The example below shows an Invoice object (Id=147) with a linked transaction to its corresponding Payment object (Id=190) via the `LinkedTxn` element.

The linked transaction element provides the **type** and **ID** of the object. In order to get the complete details of the linked transaction, you must traverse the link to retrieve the object.

### Example: Retrieve Linked Payment

```http
GET https://quickbooks.api.intuit.com/v3/company/1386066315/payment/190
```

---

## Supported Linked Transactions

| Transaction | Supported LinkedTxn.TxnType | Comments |
|-------------|----------------------------|----------|
| **Bill** | `BillPaymentCheck` | Establish the Bill/BillPayment relationship through the BillPayment object. Read only; set by QuickBooks services when link has been established from the BillPayment object. Returned in `Bill.LinkedTxn` element. |
| **Bill** | `PurchaseOrder` | Establish the Bill/PurchaseOrder relationship through the Bill object. Multiple Purchase Orders can be linked to Bill. Create, read, and update operations are supported. |
| **BillPayment** | `Bill`, `VendorCredit`, `JournalEntry`, `Deposit` | One or more line-level links established with the `BillPayment.Line.LinkedTxn` element. Create, read, and update operations are supported. |
| **Deposit** | `Transfer`, `Payment`, `SalesReceipt`, `JournalEntry`, `BillPayment` | One or more line-level links established with the `Deposit.Line.LinkedTxn` element. Create, read, and update operations are supported. |
| **Estimate** | `Invoice` | One or more transaction-level links established with the `Estimate.LinkedTxn` element. Only one link can be made per Estimate. Progress Invoicing is not supported via the API. Create, read, and update operations are supported. |
| **Invoice** | `Estimate`, `TimeActivity` | One or more transaction-level links established with the `Invoice.LinkedTxn` element. Create, read, and update operations are supported. |
| **Invoice** | `Payment` | Establish the Invoice/Payment relationship through the Payment object. Read only; set by QuickBooks services when link has been established from the Payment object. Returned in the `Invoice.LinkedTxn` element. |
| **Invoice** | `ChargeCredit`, `StatementCharge` | The ReimburseCharge, ChargeCredit, or StatementCharge transaction resources are not supported by the QuickBooks Online API. Read only; set in the QuickBooks company file via the UI. Returned in `Invoice.LinkedTxn` element. |
| **Invoice** | `ReimburseCharge` | Details about a ReimburseCharge transaction are returned in `Invoice.Line.SalesItemLineDetail`. Read only; set in the QuickBooks company file via the UI. |
| **Payment** | `Invoice`, `Expense`, `CreditMemo`, `Check`, `CreditCardCredit`, `JournalEntry` | One or more line-level links established with the `Payment.Line.LinkedTxn` element. Create, read, and update operations are supported. |
| **PurchaseOrder** | `Bill` | One or more transaction-level links established with the `PurchaseOrder.LinkedTxn` element. Read-only; establish the PurchaseOrder/Bill relationship via the UI. |
| **JournalEntry** | `BillPayment` | One or more transaction-level links established with the `JournalEntry.LinkedTxn` element. Create, read, and update operations are supported. |
| **VendorCredit** | `BillPayment` | One or more transaction-level links established with the `VendorCredit.LinkedTxn` element. Create, read, and update operations are supported. |

---

## Notes About Linked Transactions in Invoice Objects

The Invoice object returns linked transaction information in the `Invoice.LinkedTxn` array element. Two types of relationships are supported:

### 1. Read-only Links (Payment Relationships)

Representing how it is paid, having a direct effect on the company's accounts.

- The `ReimburseCharge`, `ChargeCredit`, `StatementCharge`, or `Payment` objects can establish relationships to the Invoice object
- Of these, the QuickBooks Online API supports the **Payment** relationship only
- Other relationships must be established and managed through the UI
- For these relationships, the `Invoice.LinkedTxn` elements are **read-only** on the Invoice side

### 2. Read-Write Links (Supporting Information)

Representing supporting information for the invoice. They don't affect company accounts.

- The Invoice object can create, update, and delete relationships to `TimeActivity` and `Estimate` objects

### Reimbursable Charges

A reimbursable charge corresponds to an expense incurred on behalf of a customer for which the amount needs to be invoiced. This relationship is established in the QuickBooks UI and is **read-only** through the API.

Details for a reimbursable charge are sent in the Invoice object via `Line.SalesItemLineDetail`:

| Field | Description |
|-------|-------------|
| `Line.SalesItemLineDetail.ItemRef` | The id of the item object for the billable expense. If the expense does not correspond to an item, this is set to `1`. |
| `Line.SalesItemLineDetail.ItemAccountRef` | The account associated with the reimbursable expense. |
| `Line.SalesItemLineDetail.MarkupInfo.MarkupAccountRef` | The account associated with the markup expense. |

In addition, `ReimbursedCharge` is returned in the `Invoice.LinkedTxn` element.

---

## Linked Transactions with Voided Invoices

When an invoice is voided (either via the UI or QuickBooks Online API), the following operations are performed automatically:

1. All amounts and quantities in the Invoice object are zeroed
2. Each `Invoice.LinkedTxn` link is cleared
3. Each Payment object is reset to its unapplied state:
   - The voided payment amount is added back to the `Payment.UnappliedAmt` attribute
   - The `Payment.Line.LinkedTxn` elements related to the voided invoice are cleared

---

## Notes About Linked Transactions in Payment Objects

A Payment object represents funds collected from a customer, with a breakdown of how the funds are applied. The breakdown is a list of lines, with each item represented by a `Line.LinkedTxn` element.

| LinkedTxn.TxnType | Notes |
|-------------------|-------|
| **Invoice** | Create directly via QuickBooks Online UI or API. `Payment.Line.LinkedTxn.TxnType` is set to `Invoice`. To get details, read/query on Invoice resource using `Payment.Line.LinkedTxn.TxnId`. Create/update operations supported via API. |
| **CreditMemo** | Create directly via QuickBooks Online UI or API. `Payment.Line.LinkedTxn.TxnType` is set to `CreditMemo`. To get details, read/query on CreditMemo resource. Create/update operations supported via API. |
| **Expense** | Create as an Expense object via UI (set ACCOUNT to Accounts Receivable, AMOUNT to expense amount, CUSTOMER to customer). `Payment.Line.LinkedTxn.TxnType` is set to `Expense`; underlying API stores it as a Purchase object. Create via API as Purchase object, then link. |
| **Check** | Create as a Check object via UI (set ACCOUNT to Accounts Receivable). `Payment.Line.LinkedTxn.TxnType` is set to `Check`; stored as Purchase object. Create/update operations **not** supported via API. |
| **CreditCardCredit** | Create via UI (set ACCOUNT to Accounts Receivable). `Payment.Line.LinkedTxn.TxnType` is set to `CreditCardCredit`; stored as Purchase object. Create/update operations **not** supported via API. |
| **JournalEntry** | Create via UI or API on the credit-side line (`JournalEntry.Line.JournalEntryLineDetail.PostingType=Credit`). Set ACCOUNT to Accounts Receivable, AMOUNT to expense amount, CUSTOMER to customer. Create/update operations supported via API. |

---

## Notes About Linked Transactions in Expense Objects

An expense object represents purchases made from a vendor or customer. The breakdown is a list of lines, with each item represented by a `Line.LinkedTxn` element.

| LinkedTxn.TxnType | Notes |
|-------------------|-------|
| **BillPayment** | Create directly via QuickBooks Online UI or API. One or more line-level links established with `BillPayment.Line.LinkedTxn` element for: Bill, Deposit, JournalEntry, and VendorCredit. For Vendor entity, set ACCOUNT to Accounts Payable (A/P). |
| **JournalEntry** | One or more transaction-level links established with `JournalEntry.LinkedTxn` element for BillPayment. |
| **VendorCredit** | One or more transaction-level links established with `VendorCredit.LinkedTxn` element for BillPayment. |
| **PurchaseOrder** | One or more transaction-level links established with `PurchaseOrder.LinkedTxn` element for Bill. |
| **Bill** | One or more transaction-level and line level links established with `Bill.Line.LinkedTxn` and `Bill.LinkedTxn` element for PurchaseOrder. For Create scenario, Line.Id and Line.LineNum should not be present. For PurchaseOrder entity, `Line.LinkedTxn.TxnLineId` is mandatory. |

---

## Mercury Sync Application

For Mercury bank transaction sync, linked transactions are important for:

### 1. Deposit Linking

When syncing Mercury deposits to QuickBooks:
- Use `Deposit.Line.LinkedTxn` to link deposits to related Payments or SalesReceipts
- This ensures proper reconciliation between bank deposits and customer payments

### 2. Bill Payment Linking

When syncing Mercury bill payments:
- Use `BillPayment.Line.LinkedTxn` to link payments to original Bills
- This maintains the accounts payable flow

### Example: Creating a Linked Deposit

```python
# Link a Mercury deposit to existing payments
deposit_data = {
    "DepositToAccountRef": {"value": "mercury_bank_account_id"},
    "TxnDate": "2024-01-15",
    "Line": [
        {
            "Amount": 1000.00,
            "LinkedTxn": [
                {
                    "TxnId": "payment_id",
                    "TxnType": "Payment"
                }
            ]
        }
    ]
}
```

---

## Learn More

- [Invoice API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/invoice)
- [Payment API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/payment)
- [Deposit API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/deposit)
- [BillPayment API Reference](https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/billpayment)
