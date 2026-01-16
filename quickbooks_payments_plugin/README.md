# QuickBooks Payments Plugin

QuickBooks Payments API integration for Dify, enabling secure payment processing for credit cards, debit cards, and bank accounts (ACH/eCheck).

## Features

### Payment Processing
- **Create Token** - Tokenize credit card or bank account information securely
- **Create Charge** - Process payments using payment tokens
- **Get Charge** - Retrieve payment transaction details
- **Create Refund** - Issue full or partial refunds

### Bank Account Management
- **Create Bank Account** - Save bank accounts for future ACH payments
- **Get Bank Accounts** - List all saved bank accounts for a customer
- **Delete Bank Account** - Remove bank accounts from customer profile

## Authentication

This plugin uses OAuth 2.0 authentication with QuickBooks Payments API.

**Required Scope**: `com.intuit.quickbooks.payment`

### Setup Steps

1. Register at [Intuit Developer Portal](https://developer.intuit.com)
2. Create a QuickBooks Payments app
3. Obtain Client ID and Client Secret
4. Configure redirect URI in Dify
5. Select environment (Sandbox for testing, Production for live payments)

## Usage

### 1. Tokenize Payment Method

First, create a secure token from credit card or bank account info:

```
Tool: create_token
Parameters:
  - payment_type: card
  - card_number: 4111111111111111
  - card_exp_month: 12
  - card_exp_year: 2026
  - card_cvc: 123
  - card_name: John Doe
```

### 2. Process Payment

Use the token to charge the payment:

```
Tool: create_charge
Parameters:
  - amount: "10.50"
  - token: <token_from_step_1>
  - currency: USD
  - capture: true
  - description: Payment for Invoice #1234
```

### 3. Issue Refund (if needed)

```
Tool: create_refund
Parameters:
  - charge_id: <charge_id_from_step_2>
  - amount: "10.50"
  - description: Customer requested refund
```

## Testing

### Sandbox Environment

Use these test credentials in sandbox mode:

**Test Credit Cards**:
- Visa: 4111111111111111
- Mastercard: 5105105105105100
- Amex: 378282246310005
- Discover: 6011111111111117

**Test Bank Account**:
- Routing Number: 322079353
- Account Number: Any 10-17 digits

### Test Scenarios

- **Successful Charge**: Use test card numbers above
- **Declined Card**: Use amount `5.01`
- **Insufficient Funds**: Use amount `5.02`

## Important Notes

1. **US Only**: QuickBooks Payments API is only available in the United States
2. **Token Expiration**: Payment tokens expire after 15 minutes and are single-use only
3. **PCI Compliance**: Tokenization keeps you PCI DSS compliant - never store raw card data
4. **Merchant Account**: Requires a QuickBooks Payments merchant account

## API Documentation

For complete API documentation, visit:
- [QuickBooks Payments API](https://developer.intuit.com/app/developer/qbpayments/docs/api/)
- [Getting Started Guide](https://developer.intuit.com/app/developer/qbpayments/docs/get-started)

## Security

- All payment data is tokenized before transmission
- OAuth 2.0 ensures secure API authentication
- No sensitive payment data is stored in your system
- Compliant with PCI DSS requirements

## Support

For issues or questions:
- [Intuit Developer Community](https://help.developer.intuit.com/)
- [API Reference](https://developer.intuit.com/app/developer/qbpayments/docs/api/resources/all-entities/charges)

## Version

Current version: 0.1.0

## License

This plugin is provided as-is for integration with Dify and QuickBooks Payments API.
