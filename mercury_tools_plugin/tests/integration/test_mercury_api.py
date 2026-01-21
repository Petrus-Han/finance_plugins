#!/usr/bin/env python3
"""
Integration tests for Mercury Tools Plugin

These tests make real API calls to the Mercury sandbox environment.
They require valid sandbox credentials in the .credentials file.

Run with: pytest tests/integration/test_mercury_api.py -v -s
"""

import json
import os
import sys
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

# Add plugin directory to path
PLUGIN_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PLUGIN_DIR))

# Load credentials from .credentials file
CREDENTIALS_FILE = PLUGIN_DIR / ".credentials"


def load_credentials() -> dict:
    """Load credentials from .credentials file."""
    if not CREDENTIALS_FILE.exists():
        pytest.skip(f"Credentials file not found: {CREDENTIALS_FILE}")

    with open(CREDENTIALS_FILE) as f:
        creds = json.load(f)

    if not creds.get("api_key"):
        pytest.skip("api_key not found in .credentials")

    return creds


def create_runtime(creds: dict) -> MagicMock:
    """Create a mock runtime with real credentials."""
    runtime = MagicMock()
    runtime.credentials = {
        "access_token": creds["api_key"],
        "api_environment": creds.get("environment", "sandbox")
    }
    return runtime


def create_session() -> MagicMock:
    """Create a mock session."""
    return MagicMock()


def get_json_data(result) -> dict:
    """Extract JSON data from ToolInvokeMessage."""
    if hasattr(result, 'message'):
        msg = result.message
        if hasattr(msg, 'json_object'):
            return msg.json_object
        if isinstance(msg, dict):
            return msg
    return {}


def get_message_text(result) -> str:
    """Extract text from ToolInvokeMessage."""
    if hasattr(result, 'message'):
        msg = result.message
        if hasattr(msg, 'text'):
            return msg.text
        return str(msg)
    return str(result)


# =============================================================================
# Fixtures
# =============================================================================
@pytest.fixture(scope="module")
def credentials():
    """Load and return credentials."""
    return load_credentials()


@pytest.fixture(scope="module")
def runtime(credentials):
    """Create a runtime with credentials."""
    return create_runtime(credentials)


@pytest.fixture(scope="module")
def session():
    """Create a session."""
    return create_session()


@pytest.fixture(scope="module")
def account_id(runtime, session):
    """Get the first account ID for testing."""
    from tools.get_accounts import GetAccountsTool

    tool = GetAccountsTool(runtime=runtime, session=session)
    results = list(tool._invoke({}))

    if results:
        data = get_json_data(results[0])
        accounts = data.get("accounts", [])
        if accounts:
            return accounts[0]["id"]

    pytest.skip("No accounts available for testing")


# =============================================================================
# GetAccountsTool Tests
# =============================================================================
class TestGetAccountsIntegration:
    """Integration tests for GetAccountsTool."""

    def test_get_accounts_returns_list(self, runtime, session):
        """Test that get_accounts returns a list of accounts."""
        from tools.get_accounts import GetAccountsTool

        tool = GetAccountsTool(runtime=runtime, session=session)
        results = list(tool._invoke({}))

        assert len(results) >= 1
        data = get_json_data(results[0])

        # Should return accounts list
        assert "accounts" in data
        accounts = data["accounts"]
        assert isinstance(accounts, list)

        # If we have accounts, verify structure
        if accounts:
            account = accounts[0]
            assert "id" in account
            assert "name" in account
            assert "type" in account
            assert "current_balance" in account
            print(f"\nFound {len(accounts)} account(s)")
            for acc in accounts:
                print(f"  - {acc['name']} ({acc['type']}): ${acc['current_balance']}")


# =============================================================================
# GetTransactionsTool Tests
# =============================================================================
class TestGetTransactionsIntegration:
    """Integration tests for GetTransactionsTool."""

    def test_get_transactions_for_account(self, runtime, session, account_id):
        """Test retrieving transactions for an account."""
        from tools.get_transactions import GetTransactionsTool

        tool = GetTransactionsTool(runtime=runtime, session=session)
        results = list(tool._invoke({
            "account_id": account_id,
            "limit": 10
        }))

        assert len(results) >= 1

        # Could be text message (no transactions) or JSON
        first_result = results[0]
        if hasattr(first_result, 'message') and hasattr(first_result.message, 'text'):
            print(f"\n{get_message_text(first_result)}")
        else:
            data = get_json_data(first_result)
            transactions = data.get("transactions", [])
            print(f"\nFound {len(transactions)} transaction(s)")
            for txn in transactions[:5]:  # Show first 5
                print(f"  - {txn.get('posted_at', 'N/A')}: ${txn.get('amount', 0)} - {txn.get('counterparty_name', 'N/A')}")

    def test_get_transactions_with_date_filter(self, runtime, session, account_id):
        """Test retrieving transactions with date filters."""
        from tools.get_transactions import GetTransactionsTool

        tool = GetTransactionsTool(runtime=runtime, session=session)
        results = list(tool._invoke({
            "account_id": account_id,
            "start_date": "2024-01-01",
            "end_date": "2024-12-31",
            "limit": 5
        }))

        assert len(results) >= 1
        print(f"\nFiltered transactions retrieved successfully")


# =============================================================================
# GetRecipientsTool Tests
# =============================================================================
class TestGetRecipientsIntegration:
    """Integration tests for GetRecipientsTool."""

    def test_get_recipients_returns_list(self, runtime, session):
        """Test retrieving recipients list."""
        from tools.get_recipients import GetRecipientsTool

        tool = GetRecipientsTool(runtime=runtime, session=session)
        results = list(tool._invoke({"limit": 20}))

        assert len(results) >= 1

        first_result = results[0]
        if hasattr(first_result, 'message') and hasattr(first_result.message, 'text'):
            print(f"\n{get_message_text(first_result)}")
        else:
            data = get_json_data(first_result)
            recipients = data.get("recipients", [])
            print(f"\nFound {len(recipients)} recipient(s)")
            for rcp in recipients[:5]:
                print(f"  - {rcp.get('name', 'N/A')} ({rcp.get('status', 'N/A')})")


# =============================================================================
# GetStatementsTool Tests
# =============================================================================
class TestGetStatementsIntegration:
    """Integration tests for GetStatementsTool."""

    def test_get_statements_for_account(self, runtime, session, account_id):
        """Test retrieving statements for an account."""
        from tools.get_statements import GetStatementsTool

        tool = GetStatementsTool(runtime=runtime, session=session)
        results = list(tool._invoke({"account_id": account_id}))

        assert len(results) >= 1

        first_result = results[0]
        if hasattr(first_result, 'message') and hasattr(first_result.message, 'text'):
            print(f"\n{get_message_text(first_result)}")
        else:
            data = get_json_data(first_result)
            statements = data.get("statements", [])
            print(f"\nFound {len(statements)} statement(s)")


# =============================================================================
# GetCardsTool Tests
# =============================================================================
class TestGetCardsIntegration:
    """Integration tests for GetCardsTool."""

    def test_get_cards_for_account(self, runtime, session, account_id):
        """Test retrieving cards for an account."""
        from tools.get_cards import GetCardsTool

        tool = GetCardsTool(runtime=runtime, session=session)
        results = list(tool._invoke({"account_id": account_id}))

        assert len(results) >= 1

        first_result = results[0]
        if hasattr(first_result, 'message') and hasattr(first_result.message, 'text'):
            print(f"\n{get_message_text(first_result)}")
        else:
            data = get_json_data(first_result)
            cards = data.get("cards", [])
            print(f"\nFound {len(cards)} card(s)")
            for card in cards:
                print(f"  - ****{card.get('last_four_digits', 'N/A')} ({card.get('status', 'N/A')})")


# =============================================================================
# GetEventsTool Tests
# =============================================================================
class TestGetEventsIntegration:
    """Integration tests for GetEventsTool."""

    def test_get_events_list(self, runtime, session):
        """Test retrieving events list."""
        from tools.get_events import GetEventsTool

        tool = GetEventsTool(runtime=runtime, session=session)
        results = list(tool._invoke({"limit": 10}))

        assert len(results) >= 1

        first_result = results[0]
        data = get_json_data(first_result)

        if data.get("success"):
            events = data.get("events", [])
            print(f"\nFound {data.get('count', 0)} event(s), has_more: {data.get('has_more', False)}")
            for evt in events[:5]:
                print(f"  - {evt.get('type', 'N/A')} ({evt.get('id', 'N/A')[:20]}...)")


# =============================================================================
# CustomerManagementTool Tests (AR - Accounts Receivable)
# Note: AR features require paid subscription, may not work in sandbox
# =============================================================================
class TestCustomerManagementIntegration:
    """Integration tests for CustomerManagementTool (AR)."""

    def test_list_customers(self, runtime, session):
        """Test listing AR customers (requires AR subscription)."""
        from tools.customer_management import CustomerManagementTool

        tool = CustomerManagementTool(runtime=runtime, session=session)

        try:
            results = list(tool._invoke({"operation": "list"}))

            assert len(results) >= 1

            data = get_json_data(results[0])
            if data.get("success"):
                customers = data.get("customers", [])
                print(f"\nFound {len(customers)} AR customer(s)")
                for cust in customers[:5]:
                    print(f"  - {cust.get('name', 'N/A')} ({cust.get('email', 'N/A')})")
            else:
                print(f"\nAR customers: {data.get('message', 'No data')}")
        except Exception as e:
            if "403" in str(e) or "subscriptions" in str(e).lower():
                pytest.skip("AR features require paid subscription - not available in sandbox")
            raise


# =============================================================================
# InvoiceManagementTool Tests (AR - Accounts Receivable)
# Note: AR features require paid subscription, may not work in sandbox
# =============================================================================
class TestInvoiceManagementIntegration:
    """Integration tests for InvoiceManagementTool (AR)."""

    def test_list_invoices(self, runtime, session):
        """Test listing AR invoices (requires AR subscription)."""
        from tools.invoice_management import InvoiceManagementTool

        tool = InvoiceManagementTool(runtime=runtime, session=session)

        try:
            results = list(tool._invoke({"operation": "list"}))

            assert len(results) >= 1

            data = get_json_data(results[0])
            if data.get("success"):
                invoices = data.get("invoices", [])
                print(f"\nFound {len(invoices)} AR invoice(s)")
                for inv in invoices[:5]:
                    print(f"  - {inv.get('id', 'N/A')[:20]}... - ${inv.get('amount', 0)} ({inv.get('status', 'N/A')})")
            else:
                print(f"\nAR invoices: {data.get('message', 'No data')}")
        except Exception as e:
            if "403" in str(e) or "subscriptions" in str(e).lower():
                pytest.skip("AR features require paid subscription - not available in sandbox")
            raise


# =============================================================================
# Error Handling Tests
# =============================================================================
class TestErrorHandling:
    """Test error handling with invalid inputs."""

    def test_invalid_account_id(self, runtime, session):
        """Test error handling with invalid account ID."""
        from tools.get_transactions import GetTransactionsTool

        tool = GetTransactionsTool(runtime=runtime, session=session)

        with pytest.raises(Exception) as exc_info:
            list(tool._invoke({"account_id": "invalid_account_12345"}))

        # Should raise an error for invalid account
        print(f"\nExpected error: {exc_info.value}")

    def test_missing_required_parameter(self, runtime, session):
        """Test error handling when required parameter is missing."""
        from tools.get_transactions import GetTransactionsTool

        tool = GetTransactionsTool(runtime=runtime, session=session)

        with pytest.raises(ValueError, match="Account ID is required"):
            list(tool._invoke({}))


# =============================================================================
# Full Workflow Test
# =============================================================================
class TestFullWorkflow:
    """Test a complete workflow using multiple tools."""

    def test_account_overview_workflow(self, runtime, session):
        """Test a workflow that gets account overview."""
        from tools.get_accounts import GetAccountsTool
        from tools.get_transactions import GetTransactionsTool

        print("\n=== Account Overview Workflow ===")

        # Step 1: Get all accounts
        accounts_tool = GetAccountsTool(runtime=runtime, session=session)
        account_results = list(accounts_tool._invoke({}))

        account_data = get_json_data(account_results[0])
        accounts = account_data.get("accounts", [])

        print(f"\n1. Found {len(accounts)} account(s)")

        if not accounts:
            print("   No accounts to analyze")
            return

        # Step 2: For each account, get recent transactions
        transactions_tool = GetTransactionsTool(runtime=runtime, session=session)

        for account in accounts[:2]:  # Limit to first 2 accounts
            print(f"\n2. Account: {account['name']}")
            print(f"   Balance: ${account['current_balance']}")

            txn_results = list(transactions_tool._invoke({
                "account_id": account["id"],
                "limit": 3
            }))

            first_result = txn_results[0]
            if hasattr(first_result, 'message') and hasattr(first_result.message, 'text'):
                print(f"   Transactions: {get_message_text(first_result)}")
            else:
                txn_data = get_json_data(first_result)
                transactions = txn_data.get("transactions", [])
                print(f"   Recent transactions: {len(transactions)}")
                for txn in transactions:
                    print(f"     - ${txn['amount']}: {txn.get('counterparty_name', 'N/A')}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
