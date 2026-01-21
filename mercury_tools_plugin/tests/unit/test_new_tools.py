#!/usr/bin/env python3
"""
Unit tests for Mercury Tools Plugin - New Tools

Tests all new tool implementations with mocked HTTP responses.
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
    return MagicMock()


def get_message_text(result) -> str:
    """Extract text from ToolInvokeMessage."""
    if hasattr(result, 'message'):
        msg = result.message
        if hasattr(msg, 'text'):
            return msg.text
        return str(msg)
    return str(result)


def get_json_data(result) -> dict:
    """Extract JSON data from ToolInvokeMessage."""
    if hasattr(result, 'message'):
        msg = result.message
        if hasattr(msg, 'json_object'):
            return msg.json_object
        if isinstance(msg, dict):
            return msg
    return {}


# =============================================================================
# GetCardsTool Tests
# =============================================================================
class TestGetCardsTool:
    """Tests for GetCardsTool."""

    @patch('httpx.get')
    def test_get_cards_success(self, mock_get):
        """Test successful cards retrieval."""
        from tools.get_cards import GetCardsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "cards": [
                {
                    "cardId": "card_123",
                    "lastFourDigits": "4242",
                    "nameOnCard": "John Doe",
                    "network": "visa",
                    "status": "active",
                    "physicalCardStatus": "shipped",
                    "createdAt": "2024-01-01T00:00:00Z"
                }
            ]
        }
        mock_get.return_value = mock_response

        tool = GetCardsTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"account_id": "acc_123"}))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert "cards" in data
        assert len(data["cards"]) == 1
        assert data["cards"][0]["card_id"] == "card_123"
        assert data["cards"][0]["last_four_digits"] == "4242"

    @patch('httpx.get')
    def test_get_cards_empty(self, mock_get):
        """Test empty cards list."""
        from tools.get_cards import GetCardsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"cards": []}
        mock_get.return_value = mock_response

        tool = GetCardsTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"account_id": "acc_123"}))

        assert len(results) == 1
        assert "No cards found" in get_message_text(results[0])

    def test_get_cards_missing_account_id(self):
        """Test error when account_id is missing."""
        from tools.get_cards import GetCardsTool

        tool = GetCardsTool(runtime=create_mock_runtime(), session=create_mock_session())
        with pytest.raises(ValueError, match="account_id is required"):
            list(tool._invoke({}))

    def test_get_cards_missing_token(self):
        """Test error when token is missing."""
        from tools.get_cards import GetCardsTool

        runtime = create_mock_runtime({"api_environment": "sandbox"})
        tool = GetCardsTool(runtime=runtime, session=create_mock_session())
        with pytest.raises(ValueError, match="Access Token is required"):
            list(tool._invoke({"account_id": "acc_123"}))


# =============================================================================
# GetStatementsTool Tests
# =============================================================================
class TestGetStatementsTool:
    """Tests for GetStatementsTool."""

    @patch('httpx.get')
    def test_get_statements_success(self, mock_get):
        """Test successful statements retrieval."""
        from tools.get_statements import GetStatementsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "statements": [
                {
                    "id": "stmt_123",
                    "period": "2024-01",
                    "startDate": "2024-01-01",
                    "endDate": "2024-01-31",
                    "status": "available"
                }
            ]
        }
        mock_get.return_value = mock_response

        tool = GetStatementsTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"account_id": "acc_123"}))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert "statements" in data
        assert len(data["statements"]) == 1

    def test_get_statements_missing_account_id(self):
        """Test error when account_id is missing."""
        from tools.get_statements import GetStatementsTool

        tool = GetStatementsTool(runtime=create_mock_runtime(), session=create_mock_session())
        with pytest.raises(ValueError, match="account_id is required"):
            list(tool._invoke({}))


# =============================================================================
# DownloadStatementTool Tests
# =============================================================================
class TestDownloadStatementTool:
    """Tests for DownloadStatementTool."""

    @patch('httpx.get')
    def test_download_statement_success(self, mock_get):
        """Test successful statement download."""
        from tools.download_statement import DownloadStatementTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"%PDF-1.4 fake pdf content"
        mock_response.headers = {"content-type": "application/pdf"}
        mock_get.return_value = mock_response

        tool = DownloadStatementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"statement_id": "stmt_123"}))

        # Tool returns 2 messages: blob + json
        assert len(results) == 2

    def test_download_statement_missing_id(self):
        """Test error when statement_id is missing."""
        from tools.download_statement import DownloadStatementTool

        tool = DownloadStatementTool(runtime=create_mock_runtime(), session=create_mock_session())
        with pytest.raises(ValueError, match="statement_id is required"):
            list(tool._invoke({}))


# =============================================================================
# CustomerManagementTool Tests
# =============================================================================
class TestCustomerManagementTool:
    """Tests for CustomerManagementTool (AR)."""

    @patch('httpx.get')
    def test_list_customers_success(self, mock_get):
        """Test successful customer listing."""
        from tools.customer_management import CustomerManagementTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "customers": [
                {"id": "cust_1", "name": "Acme Corp", "email": "billing@acme.com"}
            ]
        }
        mock_get.return_value = mock_response

        tool = CustomerManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"operation": "list"}))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True
        assert data["operation"] == "list"
        assert len(data["customers"]) == 1

    @patch('httpx.get')
    def test_get_customer_success(self, mock_get):
        """Test successful customer retrieval."""
        from tools.customer_management import CustomerManagementTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "cust_1", "name": "Acme Corp", "email": "billing@acme.com"
        }
        mock_get.return_value = mock_response

        tool = CustomerManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"operation": "get", "customer_id": "cust_1"}))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True
        assert data["operation"] == "get"

    @patch('httpx.post')
    def test_create_customer_success(self, mock_post):
        """Test successful customer creation."""
        from tools.customer_management import CustomerManagementTool

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "cust_new", "name": "New Customer", "email": "new@example.com"
        }
        mock_post.return_value = mock_response

        tool = CustomerManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "operation": "create",
            "name": "New Customer",
            "email": "new@example.com"
        }))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True
        assert data["operation"] == "create"

    def test_create_customer_missing_fields(self):
        """Test error when required fields missing."""
        from tools.customer_management import CustomerManagementTool

        tool = CustomerManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        with pytest.raises(ValueError, match="name and email are required"):
            list(tool._invoke({"operation": "create", "name": "Test"}))

    @patch('httpx.delete')
    def test_delete_customer_success(self, mock_delete):
        """Test successful customer deletion."""
        from tools.customer_management import CustomerManagementTool

        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        tool = CustomerManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"operation": "delete", "customer_id": "cust_1"}))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True
        assert data["operation"] == "delete"

    def test_missing_operation(self):
        """Test error when operation is missing."""
        from tools.customer_management import CustomerManagementTool

        tool = CustomerManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        with pytest.raises(ValueError, match="operation is required"):
            list(tool._invoke({}))


# =============================================================================
# InvoiceManagementTool Tests
# =============================================================================
class TestInvoiceManagementTool:
    """Tests for InvoiceManagementTool (AR)."""

    @patch('httpx.get')
    def test_list_invoices_success(self, mock_get):
        """Test successful invoice listing."""
        from tools.invoice_management import InvoiceManagementTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "invoices": [
                {"id": "inv_1", "status": "open", "amount": 1000}
            ]
        }
        mock_get.return_value = mock_response

        tool = InvoiceManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"operation": "list"}))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True
        assert len(data["invoices"]) == 1

    @patch('httpx.post')
    def test_create_invoice_success(self, mock_post):
        """Test successful invoice creation."""
        from tools.invoice_management import InvoiceManagementTool

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": "inv_new", "status": "open", "amount": 500
        }
        mock_post.return_value = mock_response

        tool = InvoiceManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "operation": "create",
            "customer_id": "cust_1",
            "destination_account_id": "acc_1",
            "invoice_date": "2024-01-15",
            "due_date": "2024-02-15",
            "line_items_json": '[{"description": "Service", "amount": 500}]'
        }))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True
        assert data["operation"] == "create"

    def test_create_invoice_missing_fields(self):
        """Test error when required fields missing."""
        from tools.invoice_management import InvoiceManagementTool

        tool = InvoiceManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        with pytest.raises(ValueError, match="customer_id.*required"):
            list(tool._invoke({"operation": "create"}))

    def test_create_invoice_invalid_json(self):
        """Test error when line_items_json is invalid."""
        from tools.invoice_management import InvoiceManagementTool

        tool = InvoiceManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        with pytest.raises(ValueError, match="Invalid line_items_json"):
            list(tool._invoke({
                "operation": "create",
                "customer_id": "cust_1",
                "destination_account_id": "acc_1",
                "invoice_date": "2024-01-15",
                "due_date": "2024-02-15",
                "line_items_json": "not valid json"
            }))

    @patch('httpx.post')
    def test_cancel_invoice_success(self, mock_post):
        """Test successful invoice cancellation."""
        from tools.invoice_management import InvoiceManagementTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        tool = InvoiceManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"operation": "cancel", "invoice_id": "inv_1"}))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True
        assert data["operation"] == "cancel"


# =============================================================================
# GetInvoicePdfTool Tests
# =============================================================================
class TestGetInvoicePdfTool:
    """Tests for GetInvoicePdfTool."""

    @patch('httpx.get')
    def test_get_invoice_pdf_success(self, mock_get):
        """Test successful invoice PDF download."""
        from tools.get_invoice_pdf import GetInvoicePdfTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"%PDF-1.4 invoice content"
        mock_response.headers = {"content-type": "application/pdf"}
        mock_get.return_value = mock_response

        tool = GetInvoicePdfTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"invoice_id": "inv_123"}))

        # Tool returns 2 messages: blob + json
        assert len(results) == 2

    def test_get_invoice_pdf_missing_id(self):
        """Test error when invoice_id is missing."""
        from tools.get_invoice_pdf import GetInvoicePdfTool

        tool = GetInvoicePdfTool(runtime=create_mock_runtime(), session=create_mock_session())
        with pytest.raises(ValueError, match="invoice_id is required"):
            list(tool._invoke({}))


# =============================================================================
# EditRecipientTool Tests
# =============================================================================
class TestEditRecipientTool:
    """Tests for EditRecipientTool."""

    @patch('httpx.post')
    def test_edit_recipient_success(self, mock_post):
        """Test successful recipient edit."""
        from tools.edit_recipient import EditRecipientTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "rcpt_123",
            "name": "Updated Vendor",
            "status": "active"
        }
        mock_post.return_value = mock_response

        tool = EditRecipientTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "recipient_id": "rcpt_123",
            "name": "Updated Vendor"
        }))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True

    def test_edit_recipient_missing_id(self):
        """Test error when recipient_id is missing."""
        from tools.edit_recipient import EditRecipientTool

        tool = EditRecipientTool(runtime=create_mock_runtime(), session=create_mock_session())
        with pytest.raises(ValueError, match="recipient_id is required"):
            list(tool._invoke({"name": "Test"}))


# =============================================================================
# GetEventsTool Tests
# =============================================================================
class TestGetEventsTool:
    """Tests for GetEventsTool."""

    @patch('httpx.get')
    def test_list_events_success(self, mock_get):
        """Test successful events listing."""
        from tools.get_events import GetEventsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "events": [
                {
                    "id": "evt_1",
                    "type": "transaction.created",
                    "resourceType": "transaction",
                    "resourceId": "txn_123",
                    "createdAt": "2024-01-15T10:00:00Z"
                }
            ],
            "hasMore": False
        }
        mock_get.return_value = mock_response

        tool = GetEventsTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({}))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True
        assert data["count"] == 1
        assert data["has_more"] is False

    @patch('httpx.get')
    def test_list_events_with_pagination(self, mock_get):
        """Test events listing with pagination info."""
        from tools.get_events import GetEventsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "events": [{"id": "evt_1"}, {"id": "evt_2"}],
            "hasMore": True,
            "nextCursor": "cursor_abc"
        }
        mock_get.return_value = mock_response

        tool = GetEventsTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"limit": 2}))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["has_more"] is True
        assert data["next_cursor"] == "cursor_abc"

    @patch('httpx.get')
    def test_get_single_event_success(self, mock_get):
        """Test single event retrieval."""
        from tools.get_events import GetEventsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "evt_123",
            "type": "transaction.updated",
            "resourceType": "transaction"
        }
        mock_get.return_value = mock_response

        tool = GetEventsTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"event_id": "evt_123"}))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True
        assert "event" in data

    @patch('httpx.get')
    def test_list_events_with_filters(self, mock_get):
        """Test events listing with filters."""
        from tools.get_events import GetEventsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"events": [], "hasMore": False}
        mock_get.return_value = mock_response

        tool = GetEventsTool(runtime=create_mock_runtime(), session=create_mock_session())
        list(tool._invoke({
            "resource_type": "transaction",
            "event_type": "transaction.created",
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2024-01-31T23:59:59Z"
        }))

        # Verify the request was made with correct params
        call_args = mock_get.call_args
        params = call_args[1].get("params", {})
        assert params.get("resourceType") == "transaction"
        assert params.get("eventType") == "transaction.created"


# =============================================================================
# UploadTransactionAttachmentTool Tests
# =============================================================================
class TestUploadTransactionAttachmentTool:
    """Tests for UploadTransactionAttachmentTool."""

    @patch('httpx.post')
    def test_upload_attachment_success(self, mock_post):
        """Test successful attachment upload."""
        from tools.upload_transaction_attachment import UploadTransactionAttachmentTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "attach_123",
            "fileName": "receipt.pdf",
            "url": "https://mercury.com/attachments/attach_123"
        }
        mock_post.return_value = mock_response

        tool = UploadTransactionAttachmentTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "transaction_id": "txn_123",
            "file": {
                "data": b"fake pdf content",
                "filename": "receipt.pdf",
                "mime_type": "application/pdf"
            }
        }))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True

    def test_upload_attachment_missing_fields(self):
        """Test error when required fields missing."""
        from tools.upload_transaction_attachment import UploadTransactionAttachmentTool

        tool = UploadTransactionAttachmentTool(runtime=create_mock_runtime(), session=create_mock_session())
        with pytest.raises(ValueError, match="file is required"):
            list(tool._invoke({"transaction_id": "txn_123"}))


# =============================================================================
# UploadRecipientAttachmentTool Tests
# =============================================================================
class TestUploadRecipientAttachmentTool:
    """Tests for UploadRecipientAttachmentTool."""

    @patch('httpx.post')
    def test_upload_attachment_success(self, mock_post):
        """Test successful attachment upload."""
        from tools.upload_recipient_attachment import UploadRecipientAttachmentTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "attach_456",
            "fileName": "w9.pdf",
            "url": "https://mercury.com/attachments/attach_456"
        }
        mock_post.return_value = mock_response

        tool = UploadRecipientAttachmentTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "recipient_id": "rcpt_123",
            "file": {
                "data": b"fake w9 content",
                "filename": "w9.pdf",
                "mime_type": "application/pdf"
            }
        }))

        assert len(results) == 1
        data = get_json_data(results[0])
        assert data["success"] is True


# =============================================================================
# API Environment Tests
# =============================================================================
class TestAPIEnvironment:
    """Tests for API environment URL selection."""

    @patch('httpx.get')
    def test_sandbox_url(self, mock_get):
        """Test sandbox environment uses correct URL."""
        from tools.get_cards import GetCardsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"cards": []}
        mock_get.return_value = mock_response

        runtime = create_mock_runtime({
            "access_token": "test",
            "api_environment": "sandbox"
        })
        tool = GetCardsTool(runtime=runtime, session=create_mock_session())
        list(tool._invoke({"account_id": "acc_123"}))

        call_args = mock_get.call_args
        assert "api-sandbox.mercury.com" in call_args[0][0]

    @patch('httpx.get')
    def test_production_url(self, mock_get):
        """Test production environment uses correct URL."""
        from tools.get_cards import GetCardsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"cards": []}
        mock_get.return_value = mock_response

        runtime = create_mock_runtime({
            "access_token": "test",
            "api_environment": "production"
        })
        tool = GetCardsTool(runtime=runtime, session=create_mock_session())
        list(tool._invoke({"account_id": "acc_123"}))

        call_args = mock_get.call_args
        assert "api.mercury.com" in call_args[0][0]
        assert "sandbox" not in call_args[0][0]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
