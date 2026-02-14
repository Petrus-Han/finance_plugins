# QuickBooks Payments Plugin

Process credit card and ACH payments through the QuickBooks Payments API.

## Setup

1. Register at [Intuit Developer Portal](https://developer.intuit.com) and create a QuickBooks Payments app
2. Obtain **Client ID** and **Client Secret**
3. Install this plugin in Dify and enter the OAuth credentials
4. Authorize via the OAuth flow
5. Select environment: **Sandbox** (testing) or **Production** (live payments)

Required OAuth scope: `com.intuit.quickbooks.payment`

**Note**: QuickBooks Payments API is only available in the United States and requires a QuickBooks Payments merchant account.

## Tools

### Payments
- **Prepare Payment Method** — Tokenize a credit card or bank account for secure payment processing
- **Process Payment** — Charge a payment using a token
- **View Payment Details** — Look up a completed charge
- **Refund Payment** — Issue a full or partial refund on a charge

### Bank Accounts
- **Save Bank Account** — Store a bank account for a customer (ACH/eCheck)
- **List Saved Bank Accounts** — View all saved bank accounts for a customer
- **Remove Bank Account** — Delete a saved bank account

## Payment Flow

1. **Tokenize** → Create a single-use token from card or bank account info (tokens expire in 15 minutes)
2. **Charge** → Process the payment using the token
3. **Refund** (if needed) → Issue a refund against the charge

## Sandbox Testing

Test card numbers for sandbox:
- Visa: `4111111111111111`
- Mastercard: `5105105105105100`
- Amex: `378282246310005`

Use amount `5.01` to simulate a declined card, `5.02` for insufficient funds.
