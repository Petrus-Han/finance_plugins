#!/usr/bin/env python3
"""
Unit tests for QuickBooks Tools Plugin

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
        "realm_id": "1234567890",
        "environment": "sandbox"
    }
    return runtime


def create_mock_session():
    """Create a mock session object."""
    session = MagicMock()
    return session


class TestGetChartOfAccountsTool:
    """Tests for GetChartOfAccountsTool."""

    @patch('httpx.get')
    def test_get_accounts_success(self, mock_get):
        """Test successful accounts retrieval."""
        from tools.get_chart_of_accounts import GetChartOfAccountsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "QueryResponse": {
                "Account": [
                    {
                        "Id": "1",
                        "Name": "Checking",
                        "AccountType": "Bank",
                        "AccountSubType": "Checking",
                        "CurrentBalance": 10000.00,
                        "Active": True
                    },
                    {
                        "Id": "2",
                        "Name": "Office Expenses",
                        "AccountType": "Expense",
                        "AccountSubType": "OfficeExpenses",
                        "Active": True
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        tool = GetChartOfAccountsTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({}))

        assert len(results) == 1
        assert results[0].json_object["count"] == 2

    @patch('httpx.get')
    def test_get_accounts_filter_by_type(self, mock_get):
        """Test filtering accounts by type."""
        from tools.get_chart_of_accounts import GetChartOfAccountsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "QueryResponse": {
                "Account": [
                    {
                        "Id": "1",
                        "Name": "Checking",
                        "AccountType": "Bank",
                        "Active": True
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        tool = GetChartOfAccountsTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"account_type": "Bank"}))

        # Verify the query was made with type filter
        call_args = mock_get.call_args
        assert "Bank" in str(call_args)

    def test_missing_credentials(self):
        """Test error when credentials are missing."""
        from tools.get_chart_of_accounts import GetChartOfAccountsTool

        runtime = create_mock_runtime({"environment": "sandbox"})
        tool = GetChartOfAccountsTool(runtime=runtime, session=create_mock_session())
        results = list(tool._invoke({}))

        assert len(results) == 1
        assert "required" in results[0].message.lower()


class TestVendorManagementTool:
    """Tests for VendorManagementTool."""

    @patch('httpx.get')
    def test_list_vendors_success(self, mock_get):
        """Test successful vendor listing."""
        from tools.vendor_management import VendorManagementTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "QueryResponse": {
                "Vendor": [
                    {
                        "Id": "1",
                        "DisplayName": "Acme Corp",
                        "CompanyName": "Acme Corporation",
                        "Active": True,
                        "Balance": 500.00
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        tool = VendorManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"action": "list"}))

        assert len(results) == 1
        assert results[0].json_object["count"] == 1
        assert results[0].json_object["vendors"][0]["display_name"] == "Acme Corp"

    @patch('httpx.post')
    def test_create_vendor_success(self, mock_post):
        """Test successful vendor creation."""
        from tools.vendor_management import VendorManagementTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Vendor": {
                "Id": "new_vendor",
                "DisplayName": "New Vendor",
                "SyncToken": "0"
            }
        }
        mock_post.return_value = mock_response

        tool = VendorManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "action": "create",
            "display_name": "New Vendor"
        }))

        assert len(results) == 1
        assert results[0].json_object["id"] == "new_vendor"


class TestCustomerManagementTool:
    """Tests for CustomerManagementTool."""

    @patch('httpx.get')
    def test_list_customers_success(self, mock_get):
        """Test successful customer listing."""
        from tools.customer_management import CustomerManagementTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "QueryResponse": {
                "Customer": [
                    {
                        "Id": "1",
                        "DisplayName": "John Doe",
                        "CompanyName": "",
                        "PrimaryEmailAddr": {"Address": "john@example.com"},
                        "Balance": 0,
                        "Active": True
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        tool = CustomerManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"action": "list"}))

        assert len(results) == 1
        assert results[0].json_object["count"] == 1

    @patch('httpx.post')
    def test_create_customer_success(self, mock_post):
        """Test successful customer creation."""
        from tools.customer_management import CustomerManagementTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Customer": {
                "Id": "new_customer",
                "DisplayName": "Jane Doe",
                "SyncToken": "0"
            }
        }
        mock_post.return_value = mock_response

        tool = CustomerManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "action": "create",
            "display_name": "Jane Doe",
            "email": "jane@example.com"
        }))

        assert len(results) == 1
        assert results[0].json_object["id"] == "new_customer"

    def test_create_customer_missing_name(self):
        """Test error when display_name is missing."""
        from tools.customer_management import CustomerManagementTool

        tool = CustomerManagementTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({"action": "create"}))

        assert len(results) == 1
        assert "required" in results[0].message.lower()


class TestCreatePurchaseTool:
    """Tests for CreatePurchaseTool."""

    @patch('httpx.post')
    def test_create_purchase_success(self, mock_post):
        """Test successful purchase creation."""
        from tools.create_purchase import CreatePurchaseTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Purchase": {
                "Id": "purchase_123",
                "TxnDate": "2024-01-15",
                "TotalAmt": 500.00,
                "PaymentType": "CreditCard",
                "AccountRef": {"name": "Checking"},
                "SyncToken": "0"
            }
        }
        mock_post.return_value = mock_response

        tool = CreatePurchaseTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "bank_account_id": "1",
            "amount": 500.00,
            "expense_account_id": "2",
            "payment_type": "CreditCard"
        }))

        assert len(results) == 1
        assert results[0].json_object["id"] == "purchase_123"
        assert results[0].json_object["total_amount"] == 500.00

    def test_create_purchase_missing_required(self):
        """Test error when required fields are missing."""
        from tools.create_purchase import CreatePurchaseTool

        tool = CreatePurchaseTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "bank_account_id": "1"
            # Missing amount and expense_account_id
        }))

        assert len(results) == 1
        assert "required" in results[0].message.lower()


class TestCreateDepositTool:
    """Tests for CreateDepositTool."""

    @patch('httpx.post')
    def test_create_deposit_success(self, mock_post):
        """Test successful deposit creation."""
        from tools.create_deposit import CreateDepositTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Deposit": {
                "Id": "deposit_123",
                "TxnDate": "2024-01-15",
                "TotalAmt": 1000.00,
                "DepositToAccountRef": {"name": "Checking"},
                "SyncToken": "0"
            }
        }
        mock_post.return_value = mock_response

        tool = CreateDepositTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "bank_account_id": "1",
            "amount": 1000.00,
            "income_account_id": "3"
        }))

        assert len(results) == 1
        assert results[0].json_object["id"] == "deposit_123"


class TestCreateTransferTool:
    """Tests for CreateTransferTool."""

    @patch('httpx.post')
    def test_create_transfer_success(self, mock_post):
        """Test successful transfer creation."""
        from tools.create_transfer import CreateTransferTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Transfer": {
                "Id": "transfer_123",
                "TxnDate": "2024-01-15",
                "Amount": 2000.00,
                "FromAccountRef": {"value": "1", "name": "Checking"},
                "ToAccountRef": {"value": "2", "name": "Savings"},
                "SyncToken": "0"
            }
        }
        mock_post.return_value = mock_response

        tool = CreateTransferTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "from_account_id": "1",
            "to_account_id": "2",
            "amount": 2000.00
        }))

        assert len(results) == 1
        assert results[0].json_object["id"] == "transfer_123"
        assert results[0].json_object["from_account"]["name"] == "Checking"
        assert results[0].json_object["to_account"]["name"] == "Savings"

    def test_create_transfer_missing_required(self):
        """Test error when required fields are missing."""
        from tools.create_transfer import CreateTransferTool

        tool = CreateTransferTool(runtime=create_mock_runtime(), session=create_mock_session())
        results = list(tool._invoke({
            "from_account_id": "1"
            # Missing to_account_id and amount
        }))

        assert len(results) == 1
        assert "required" in results[0].message.lower()


class TestAPIEnvironment:
    """Tests for API environment URL selection."""

    @patch('httpx.get')
    def test_sandbox_url(self, mock_get):
        """Test sandbox environment uses correct URL."""
        from tools.get_chart_of_accounts import GetChartOfAccountsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"QueryResponse": {"Account": []}}
        mock_get.return_value = mock_response

        runtime = create_mock_runtime({
            "access_token": "test",
            "realm_id": "123",
            "environment": "sandbox"
        })
        tool = GetChartOfAccountsTool(runtime=runtime, session=create_mock_session())
        list(tool._invoke({}))

        call_args = mock_get.call_args
        assert "sandbox-quickbooks" in call_args[0][0]

    @patch('httpx.get')
    def test_production_url(self, mock_get):
        """Test production environment uses correct URL."""
        from tools.get_chart_of_accounts import GetChartOfAccountsTool

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"QueryResponse": {"Account": []}}
        mock_get.return_value = mock_response

        runtime = create_mock_runtime({
            "access_token": "test",
            "realm_id": "123",
            "environment": "production"
        })
        tool = GetChartOfAccountsTool(runtime=runtime, session=create_mock_session())
        list(tool._invoke({}))

        call_args = mock_get.call_args
        assert "quickbooks.api.intuit.com" in call_args[0][0]
        assert "sandbox" not in call_args[0][0]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
