#!/usr/bin/env python3
"""
Unit tests for Mercury Tools Plugin

Tests all tool implementations with mocked HTTP responses.
"""

import json
import sys
import os
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

# Add plugin directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def create_mock_runtime(credentials: dict = None):
    """Create a mock runtime object for testing."""
    runtime = MagicMock()
    runtime.credentials = credentials or {
        "access_token": "test_token",
        "api_environment": "sandbox"
    }
    return runtime


def create_mock_session():
    """Create a mock session object."""
    session = MagicMock()
    return session


def get_message_text(result) -> str:
    """Extract text from ToolInvokeMessage."""
    if hasattr(result.message, 'text'):
        return result.message.text
    return str(result.message)


def get_json_data(result) -> dict:
    """Extract JSON data from ToolInvokeMessage."""
    if hasattr(result.message, 'json_object'):
        return result.message.json_object
    elif hasattr(result, 'message') and isinstance(result.message, dict):
        return result.message
    # Try to parse the message content
    msg = result.message
    if hasattr(msg, 'json_object'):
        return msg.json_object
    return {}


class TestGetAccountsTool:
    """Tests for GetAccountsTool."""

    @patch('httpx.get')
    def test_get_accounts_success(self, mock_get):
        """Test successful accounts retrieval."""
        from tools.get_accounts import GetAccountsTool

        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "accounts": [
                {
                    "id": "acc_123",
                    "name": "Mercury Checking",
                    "kind": "checking",
                    "currentBalance": 10000.00,
                    "availableBalance": 9500.00,
                    "type": "mercury",
                    "status": "active"
                }
            ]
        }
        mock_get.return_value = mock_response

        tool = GetAccountsTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({}))

        assert len(results) == 1
        json_data = get_json_data(results[0])
        # get_accounts returns a list directly, not {"accounts": ..., "count": ...}
        assert isinstance(json_data, list)
        assert len(json_data) == 1
        assert json_data[0]["id"] == "acc_123"

    @patch('httpx.get')
    def test_get_accounts_auth_error(self, mock_get):
        """Test authentication error handling."""
        from tools.get_accounts import GetAccountsTool

        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response

        tool = GetAccountsTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({}))

        assert len(results) == 1
        assert "Authentication failed" in get_message_text(results[0])

    def test_missing_token(self):
        """Test error when token is missing."""
        from tools.get_accounts import GetAccountsTool

        runtime = create_mock_runtime({"api_environment": "sandbox"})
        tool = GetAccountsTool(runtime=runtime, session=create_mock_session())
        results = list(tool._invoke({}))

        assert len(results) == 1
        assert "Access Token is required" in get_message_text(results[0])


class TestGetRecipientsTool:
    """Tests for GetRecipientsTool."""

    @patch('httpx.get')
    def test_get_recipients_success(self, mock_get):
        """Test successful recipients retrieval."""
        from tools.get_recipients import GetRecipientsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "recipients": [
                {
                    "id": "recipient_123",
                    "name": "Acme Corp",
                    "status": "active",
                    "emails": ["pay@acme.com"],
                    "paymentMethod": "ach",
                    "createdAt": "2024-01-01T00:00:00Z"
                }
            ],
            "hasMore": False
        }
        mock_get.return_value = mock_response

        tool = GetRecipientsTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"limit": 50}))

        assert len(results) == 1
        json_data = get_json_data(results[0])
        assert json_data["count"] == 1
        assert json_data["recipients"][0]["name"] == "Acme Corp"


class TestCreateRecipientTool:
    """Tests for CreateRecipientTool."""

    @patch('httpx.post')
    def test_create_recipient_ach_success(self, mock_post):
        """Test successful ACH recipient creation."""
        from tools.create_recipient import CreateRecipientTool

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "recipient_new",
            "name": "New Vendor",
            "status": "active",
            "paymentMethod": "ach",
            "createdAt": "2024-01-15T00:00:00Z"
        }
        mock_post.return_value = mock_response

        tool = CreateRecipientTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "name": "New Vendor",
            "payment_method": "ach",
            "account_number": "123456789",
            "routing_number": "021000021",
            "account_type": "checking"
        }))

        assert len(results) == 1
        json_data = get_json_data(results[0])
        assert json_data["success"] is True
        assert json_data["id"] == "recipient_new"

    def test_create_recipient_missing_routing_info(self):
        """Test error when routing info missing for ACH."""
        from tools.create_recipient import CreateRecipientTool

        tool = CreateRecipientTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "name": "New Vendor",
            "payment_method": "ach"
            # Missing account_number and routing_number
        }))

        assert len(results) == 1
        assert "Account number and routing number are required" in get_message_text(results[0])


class TestGetTransactionTool:
    """Tests for GetTransactionTool."""

    @patch('httpx.get')
    def test_get_transaction_success(self, mock_get):
        """Test successful transaction retrieval."""
        from tools.get_transaction import GetTransactionTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "txn_123",
            "accountId": "acc_001",
            "amount": -500.00,
            "status": "sent",
            "counterpartyName": "Vendor Inc",
            "note": "Test payment",
            "postedAt": "2024-01-15T10:00:00Z"
        }
        mock_get.return_value = mock_response

        tool = GetTransactionTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"account_id": "acc_001", "transaction_id": "txn_123"}))

        assert len(results) == 1
        json_data = get_json_data(results[0])
        assert json_data["id"] == "txn_123"
        assert json_data["amount"] == -500.00

        # Verify correct API endpoint path
        call_args = mock_get.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get('url', '')
        assert "/account/acc_001/transaction/txn_123" in url, f"Incorrect endpoint: {url}"

    @patch('httpx.get')
    def test_get_transaction_not_found(self, mock_get):
        """Test transaction not found."""
        from tools.get_transaction import GetTransactionTool

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        tool = GetTransactionTool(runtime=create_mock_runtime(), session=create_mock_session())

        with pytest.raises(ValueError) as excinfo:
            list(tool._invoke({"account_id": "acc_001", "transaction_id": "txn_invalid"}))
        assert "not found" in str(excinfo.value)

    @patch('httpx.get')
    def test_get_transaction_without_account_id(self, mock_get):
        """Test transaction retrieval without account_id uses /transaction/{id} endpoint."""
        from tools.get_transaction import GetTransactionTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "txn_123",
            "accountId": "acc_001",
            "amount": -500.00,
            "status": "sent",
        }
        mock_get.return_value = mock_response

        tool = GetTransactionTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"transaction_id": "txn_123"}))

        assert len(results) == 1

        # Verify uses /transaction/{id} endpoint (without account_id)
        call_args = mock_get.call_args
        url = call_args[0][0] if call_args[0] else call_args[1].get('url', '')
        assert "/transaction/txn_123" in url, f"Incorrect endpoint: {url}"
        assert "/account/" not in url, f"Should not include account in path: {url}"

    def test_get_transaction_missing_transaction_id(self):
        """Test error when transaction_id is missing."""
        from tools.get_transaction import GetTransactionTool

        tool = GetTransactionTool(runtime=create_mock_runtime(), session=create_mock_session())

        with pytest.raises(ValueError) as excinfo:
            list(tool._invoke({"account_id": "acc_001"}))
        assert "Transaction ID is required" in str(excinfo.value)


class TestUpdateTransactionTool:
    """Tests for UpdateTransactionTool."""

    @patch('httpx.patch')
    def test_update_transaction_success(self, mock_patch):
        """Test successful transaction update."""
        from tools.update_transaction import UpdateTransactionTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "txn_123",
            "note": "Updated note",
            "status": "sent"
        }
        mock_patch.return_value = mock_response

        tool = UpdateTransactionTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "transaction_id": "txn_123",
            "note": "Updated note"
        }))

        assert len(results) == 1
        json_data = get_json_data(results[0])
        assert json_data["success"] is True

    def test_update_transaction_no_fields(self):
        """Test error when no fields provided."""
        from tools.update_transaction import UpdateTransactionTool

        tool = UpdateTransactionTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"transaction_id": "txn_123"}))

        assert len(results) == 1
        assert "At least one field" in get_message_text(results[0])


class TestAPIEnvironment:
    """Tests for API environment URL selection."""

    @patch('httpx.get')
    def test_sandbox_url(self, mock_get):
        """Test sandbox environment uses correct URL."""
        from tools.get_accounts import GetAccountsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"accounts": []}
        mock_get.return_value = mock_response

        runtime = create_mock_runtime({
            "access_token": "test",
            "api_environment": "sandbox"
        })
        tool = GetAccountsTool(runtime=runtime, session=create_mock_session())
        list(tool._invoke({}))

        # Check the URL used
        call_args = mock_get.call_args
        assert "api-sandbox.mercury.com" in call_args[0][0]

    @patch('httpx.get')
    def test_production_url(self, mock_get):
        """Test production environment uses correct URL."""
        from tools.get_accounts import GetAccountsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"accounts": []}
        mock_get.return_value = mock_response

        runtime = create_mock_runtime({
            "access_token": "test",
            "api_environment": "production"
        })
        tool = GetAccountsTool(runtime=runtime, session=create_mock_session())
        list(tool._invoke({}))

        # Check the URL used
        call_args = mock_get.call_args
        assert "api.mercury.com" in call_args[0][0]
        assert "sandbox" not in call_args[0][0]


class TestAPIEndpointPaths:
    """Tests to verify correct API endpoint paths are used."""

    @patch('httpx.get')
    def test_get_accounts_endpoint(self, mock_get):
        """Verify GET /api/v1/accounts endpoint."""
        from tools.get_accounts import GetAccountsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"accounts": []}
        mock_get.return_value = mock_response

        tool = GetAccountsTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({}))

        url = mock_get.call_args[0][0]
        assert url.endswith("/api/v1/accounts"), f"Expected /api/v1/accounts, got: {url}"

    @patch('httpx.get')
    def test_get_account_endpoint(self, mock_get):
        """Verify GET /api/v1/account/{id} endpoint."""
        from tools.get_account import GetAccountTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "acc_123", "name": "Test"}
        mock_get.return_value = mock_response

        tool = GetAccountTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({"account_id": "acc_123"}))

        url = mock_get.call_args[0][0]
        assert "/api/v1/account/acc_123" in url, f"Expected /api/v1/account/acc_123, got: {url}"

    @patch('httpx.get')
    def test_get_transactions_endpoint(self, mock_get):
        """Verify GET /api/v1/account/{id}/transactions endpoint."""
        from tools.get_transactions import GetTransactionsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"transactions": []}
        mock_get.return_value = mock_response

        tool = GetTransactionsTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({"account_id": "acc_123"}))

        url = mock_get.call_args[0][0]
        assert "/api/v1/account/acc_123/transactions" in url, f"Expected /api/v1/account/acc_123/transactions, got: {url}"

    @patch('httpx.get')
    def test_get_transaction_endpoint_with_account_id(self, mock_get):
        """Verify GET /api/v1/account/{id}/transaction/{txnId} endpoint when account_id is provided."""
        from tools.get_transaction import GetTransactionTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "txn_456"}
        mock_get.return_value = mock_response

        tool = GetTransactionTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({"account_id": "acc_123", "transaction_id": "txn_456"}))

        url = mock_get.call_args[0][0]
        assert "/api/v1/account/acc_123/transaction/txn_456" in url, f"Expected /api/v1/account/acc_123/transaction/txn_456, got: {url}"

    @patch('httpx.get')
    def test_get_transaction_endpoint_without_account_id(self, mock_get):
        """Verify GET /api/v1/transaction/{id} endpoint when account_id is not provided."""
        from tools.get_transaction import GetTransactionTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "txn_456", "accountId": "acc_123"}
        mock_get.return_value = mock_response

        tool = GetTransactionTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({"transaction_id": "txn_456"}))

        url = mock_get.call_args[0][0]
        assert "/api/v1/transaction/txn_456" in url, f"Expected /api/v1/transaction/txn_456, got: {url}"
        assert "/account/" not in url, f"Should not include /account/ when account_id not provided: {url}"

    @patch('httpx.patch')
    def test_update_transaction_endpoint(self, mock_patch):
        """Verify PATCH /api/v1/transaction/{id} endpoint."""
        from tools.update_transaction import UpdateTransactionTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "txn_123"}
        mock_patch.return_value = mock_response

        tool = UpdateTransactionTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({"transaction_id": "txn_123", "note": "test"}))

        url = mock_patch.call_args[0][0]
        assert "/api/v1/transaction/txn_123" in url, f"Expected /api/v1/transaction/txn_123, got: {url}"

    @patch('httpx.get')
    def test_get_recipients_endpoint(self, mock_get):
        """Verify GET /api/v1/recipients endpoint."""
        from tools.get_recipients import GetRecipientsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"recipients": []}
        mock_get.return_value = mock_response

        tool = GetRecipientsTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({}))

        url = mock_get.call_args[0][0]
        assert "/api/v1/recipients" in url, f"Expected /api/v1/recipients, got: {url}"

    @patch('httpx.get')
    def test_get_recipient_endpoint(self, mock_get):
        """Verify GET /api/v1/recipient/{id} endpoint."""
        from tools.get_recipient import GetRecipientTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "rcp_123", "name": "Test"}
        mock_get.return_value = mock_response

        tool = GetRecipientTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({"recipient_id": "rcp_123"}))

        url = mock_get.call_args[0][0]
        assert "/api/v1/recipient/rcp_123" in url, f"Expected /api/v1/recipient/rcp_123, got: {url}"

    @patch('httpx.post')
    def test_create_recipient_endpoint(self, mock_post):
        """Verify POST /api/v1/recipients endpoint."""
        from tools.create_recipient import CreateRecipientTool

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": "rcp_new"}
        mock_post.return_value = mock_response

        tool = CreateRecipientTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({
            "name": "Test",
            "payment_method": "ach",
            "account_number": "123456789",
            "routing_number": "021000021"
        }))

        url = mock_post.call_args[0][0]
        assert "/api/v1/recipients" in url, f"Expected /api/v1/recipients, got: {url}"

    @patch('httpx.patch')
    def test_edit_recipient_uses_patch(self, mock_patch):
        """Verify edit_recipient uses PATCH method (not POST)."""
        from tools.edit_recipient import EditRecipientTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "rcp_123", "name": "Updated"}
        mock_patch.return_value = mock_response

        tool = EditRecipientTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({"recipient_id": "rcp_123", "name": "Updated"}))

        # Verify PATCH was called, not POST
        assert mock_patch.called, "edit_recipient should use httpx.patch()"
        url = mock_patch.call_args[0][0]
        assert "/api/v1/recipient/rcp_123" in url, f"Expected /api/v1/recipient/rcp_123, got: {url}"

    @patch('httpx.get')
    def test_get_cards_endpoint(self, mock_get):
        """Verify GET /api/v1/account/{id}/cards endpoint."""
        from tools.get_cards import GetCardsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"cards": []}
        mock_get.return_value = mock_response

        tool = GetCardsTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({"account_id": "acc_123"}))

        url = mock_get.call_args[0][0]
        assert "/api/v1/account/acc_123/cards" in url, f"Expected /api/v1/account/acc_123/cards, got: {url}"

    @patch('httpx.get')
    def test_get_statements_endpoint(self, mock_get):
        """Verify GET /api/v1/account/{id}/statements endpoint."""
        from tools.get_statements import GetStatementsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"statements": []}
        mock_get.return_value = mock_response

        tool = GetStatementsTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({"account_id": "acc_123"}))

        url = mock_get.call_args[0][0]
        assert "/api/v1/account/acc_123/statements" in url, f"Expected /api/v1/account/acc_123/statements, got: {url}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
