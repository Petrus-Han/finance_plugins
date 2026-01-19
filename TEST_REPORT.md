# Finance Plugins Test Report

**Generated:** 2026-01-19
**Branch:** dev/alai-sudo

## Summary

| Plugin | Unit Tests | Integration Tests | Status |
|--------|------------|-------------------|--------|
| Mercury Trigger | 18/18 | 14/14 | PASS |
| Mercury Tools | 12/12 | - | PASS |
| QuickBooks | 15/15 | - | PASS |
| QuickBooks Payments | No tests | - | N/A |

**Total: 59 tests passed, 0 failed**

---

## Mercury Trigger Plugin

### Unit Tests (18/18 passed)

| Test Class | Test Name | Status |
|------------|-----------|--------|
| TestTransactionEvent | test_on_event_basic | PASS |
| TestTransactionEvent | test_on_event_with_operation_filter_created | PASS |
| TestTransactionEvent | test_on_event_with_operation_filter_updated | PASS |
| TestTransactionEvent | test_on_event_with_operation_filter_all | PASS |
| TestTransactionEvent | test_on_event_empty_merge_patch | PASS |
| TestSignatureValidation | test_valid_signature | PASS |
| TestSignatureValidation | test_invalid_signature | PASS |
| TestSignatureValidation | test_missing_signature_header | PASS |
| TestPayloadParsing | test_parse_valid_payload | PASS |
| TestPayloadParsing | test_parse_empty_payload | PASS |
| TestEventTypeResolution | test_resolve_transaction_event | PASS |
| TestEventTypeResolution | test_resolve_unknown_resource_type | PASS |
| TestSubscriptionConstructor | test_get_api_base_url_production | PASS |
| TestSubscriptionConstructor | test_get_api_base_url_sandbox | PASS |
| TestSubscriptionConstructor | test_get_api_base_url_default | PASS |
| TestSubscriptionConstructor | test_get_api_base_url_mock | PASS |
| TestSubscriptionConstructor | test_get_api_base_url_mock_with_trailing_slash | PASS |
| TestSubscriptionConstructor | test_get_api_base_url_mock_missing_url | PASS |

### Integration Tests (14/14 passed)

| Test Class | Test Name | Status |
|------------|-----------|--------|
| TestAPIKeyValidation | test_valid_api_key | PASS |
| TestAPIKeyValidation | test_invalid_api_key | PASS |
| TestWebhookSubscription | test_create_webhook | PASS |
| TestWebhookSubscription | test_list_webhooks | PASS |
| TestWebhookSubscription | test_get_webhook_details | PASS |
| TestWebhookSubscription | test_delete_webhook | PASS |
| TestWebhookSubscription | test_delete_nonexistent_webhook | PASS |
| TestEventSimulation | test_simulate_transaction_created | PASS |
| TestEventSimulation | test_simulate_transaction_updated | PASS |
| TestMercuryAPIEndpoints | test_get_accounts | PASS |
| TestMercuryAPIEndpoints | test_get_account_details | PASS |
| TestMercuryAPIEndpoints | test_get_account_transactions | PASS |
| TestMercuryAPIEndpoints | test_get_recipients | PASS |
| TestMercuryAPIEndpoints | test_get_categories | PASS |

---

## Mercury Tools Plugin

### Unit Tests (12/12 passed)

| Test Class | Test Name | Status |
|------------|-----------|--------|
| TestGetAccountsTool | test_get_accounts_success | PASS |
| TestGetAccountsTool | test_get_accounts_auth_error | PASS |
| TestGetAccountsTool | test_missing_token | PASS |
| TestGetRecipientsTool | test_get_recipients_success | PASS |
| TestCreateRecipientTool | test_create_recipient_ach_success | PASS |
| TestCreateRecipientTool | test_create_recipient_missing_routing_info | PASS |
| TestGetTransactionTool | test_get_transaction_success | PASS |
| TestGetTransactionTool | test_get_transaction_not_found | PASS |
| TestUpdateTransactionTool | test_update_transaction_success | PASS |
| TestUpdateTransactionTool | test_update_transaction_no_fields | PASS |
| TestAPIEnvironment | test_sandbox_url | PASS |
| TestAPIEnvironment | test_production_url | PASS |

### New Tools Added

1. **SendMoneyTool** (`tools/send_money.py`)
   - Request to send money from a Mercury account
   - Supports ACH, wire, and check payments
   - Parameters: account_id, recipient_id, amount, payment_method, note, external_memo

2. **InternalTransferTool** (`tools/internal_transfer.py`)
   - Create internal transfers between Mercury accounts
   - Parameters: from_account_id, to_account_id, amount, note

---

## QuickBooks Plugin

### Unit Tests (15/15 passed)

| Test Class | Test Name | Status |
|------------|-----------|--------|
| TestGetChartOfAccountsTool | test_get_accounts_success | PASS |
| TestGetChartOfAccountsTool | test_get_accounts_filter_by_type | PASS |
| TestGetChartOfAccountsTool | test_missing_credentials | PASS |
| TestVendorManagementTool | test_search_vendors_success | PASS |
| TestVendorManagementTool | test_create_vendor_success | PASS |
| TestCustomerManagementTool | test_list_customers_success | PASS |
| TestCustomerManagementTool | test_create_customer_success | PASS |
| TestCustomerManagementTool | test_create_customer_missing_name | PASS |
| TestCreatePurchaseTool | test_create_purchase_success | PASS |
| TestCreatePurchaseTool | test_create_purchase_missing_required | PASS |
| TestCreateDepositTool | test_create_deposit_success | PASS |
| TestCreateTransferTool | test_create_transfer_success | PASS |
| TestCreateTransferTool | test_create_transfer_missing_required | PASS |
| TestAPIEnvironment | test_sandbox_url | PASS |
| TestAPIEnvironment | test_production_url | PASS |

### New Tools Added

1. **CreateInvoiceTool** (`tools/create_invoice.py`)
   - Create invoices (accounts receivable) in QuickBooks
   - Parameters: customer_id, line_items, txn_date, due_date, doc_number, customer_memo, bill_email

2. **CreateBillTool** (`tools/create_bill.py`)
   - Create bills (accounts payable) in QuickBooks
   - Parameters: vendor_id, line_items, txn_date, due_date, doc_number, private_note, ap_account_id

---

## Mock Server Endpoints

The mock Mercury server (`scripts/mock_mercury_server.py`) supports the following endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/accounts | List all accounts |
| GET | /api/v1/account/{id} | Get account details |
| GET | /api/v1/account/{id}/transactions | Get account transactions |
| GET | /api/v1/recipients | List recipients |
| GET | /api/v1/recipient/{id} | Get recipient details |
| POST | /api/v1/recipient | Create recipient |
| GET | /api/v1/categories | List categories |
| GET | /api/v1/web-hooks | List webhooks |
| POST | /api/v1/web-hooks | Create webhook |
| DELETE | /api/v1/web-hooks/{id} | Delete webhook |
| POST | /api/v1/simulate-event | Simulate webhook event |
| POST | /api/v1/account/{id}/request-send-money | Request to send money |
| POST | /api/v1/transfer | Create internal transfer |

### Endpoint Verification

```bash
# Send Money endpoint
curl -X POST http://localhost:8765/api/v1/account/acc_123/request-send-money \
  -H "Authorization: Bearer mock_token_12345" \
  -H "Content-Type: application/json" \
  -d '{"recipientId": "rcp_456", "amount": 500, "paymentMethod": "ach"}'

# Response:
{
    "id": "smr_...",
    "transactionId": "txn_...",
    "status": "pending_approval",
    "amount": 500.0,
    "recipientId": "rcp_456",
    "accountId": "acc_123",
    "paymentMethod": "ach"
}

# Internal Transfer endpoint
curl -X POST http://localhost:8765/api/v1/transfer \
  -H "Authorization: Bearer mock_token_12345" \
  -H "Content-Type: application/json" \
  -d '{"fromAccountId": "acc_123", "toAccountId": "acc_456", "amount": 1000}'

# Response:
{
    "id": "txn_...",
    "status": "sent",
    "amount": 1000.0,
    "fromAccountId": "acc_123",
    "toAccountId": "acc_456",
    "kind": "internalTransfer"
}
```

---

## Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all Mercury trigger tests
pytest mercury_trigger_plugin/tests/ -v

# Run Mercury tools unit tests
pytest mercury_tools_plugin/tests/unit/ -v

# Run QuickBooks unit tests
pytest quickbooks_plugin/tests/unit/ -v

# Run integration tests with mock server
python scripts/mock_mercury_server.py &
pytest mercury_trigger_plugin/tests/integration/ -v
```

---

## Conclusion

All 59 unit and integration tests pass successfully. The plugins are ready for deployment.

### What's New

1. **Mercury Tools Plugin**
   - Added `send_money` tool for requesting payments
   - Added `internal_transfer` tool for transfers between accounts

2. **QuickBooks Plugin**
   - Added `create_invoice` tool for accounts receivable
   - Added `create_bill` tool for accounts payable

3. **Mock Server**
   - Added `/api/v1/account/{id}/request-send-money` endpoint
   - Added `/api/v1/transfer` endpoint

4. **Testing Infrastructure**
   - Fixed vendor management tests to use correct parameters
   - All tests now pass with proper mocking
