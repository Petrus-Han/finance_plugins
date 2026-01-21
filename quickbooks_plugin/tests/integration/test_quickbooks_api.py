#!/usr/bin/env python3
"""
Integration tests for QuickBooks Tools Plugin

These tests make real API calls to the QuickBooks sandbox environment.
They require valid sandbox credentials in the .credentials file.

Run with: pytest tests/integration/test_quickbooks_api.py -v -s
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

    if not creds.get("access_token"):
        pytest.skip("access_token not found in .credentials - complete OAuth first")

    if not creds.get("realm_id"):
        pytest.skip("realm_id not found in .credentials")

    return creds


def create_runtime(creds: dict) -> MagicMock:
    """Create a mock runtime with real credentials."""
    runtime = MagicMock()
    runtime.credentials = {
        "access_token": creds["access_token"],
        "realm_id": creds["realm_id"],
        "environment": creds.get("environment", "sandbox")
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


# =============================================================================
# CustomerManagementTool Tests
# =============================================================================
class TestCustomerManagementIntegration:
    """Integration tests for CustomerManagementTool."""

    def test_list_customers(self, runtime, session):
        """Test listing customers."""
        from tools.customer_management import CustomerManagementTool

        tool = CustomerManagementTool(runtime=runtime, session=session)
        results = list(tool._invoke({"action": "list"}))

        assert len(results) >= 1
        data = get_json_data(results[0])

        assert "customers" in data
        customers = data["customers"]
        print(f"\nFound {data['count']} customer(s)")
        for cust in customers[:5]:
            print(f"  - {cust.get('display_name', 'N/A')} (ID: {cust.get('id')})")


# =============================================================================
# VendorManagementTool Tests
# =============================================================================
class TestVendorManagementIntegration:
    """Integration tests for VendorManagementTool."""

    def test_list_vendors(self, runtime, session):
        """Test listing vendors."""
        from tools.vendor_management import VendorManagementTool

        tool = VendorManagementTool(runtime=runtime, session=session)
        results = list(tool._invoke({"action": "list"}))

        assert len(results) >= 1
        data = get_json_data(results[0])

        assert "vendors" in data
        vendors = data["vendors"]
        print(f"\nFound {data['count']} vendor(s)")
        for v in vendors[:5]:
            print(f"  - {v.get('display_name', 'N/A')} (ID: {v.get('id')})")


# =============================================================================
# GetChartOfAccountsTool Tests
# =============================================================================
class TestChartOfAccountsIntegration:
    """Integration tests for GetChartOfAccountsTool."""

    def test_get_chart_of_accounts(self, runtime, session):
        """Test retrieving chart of accounts."""
        from tools.get_chart_of_accounts import GetChartOfAccountsTool

        tool = GetChartOfAccountsTool(runtime=runtime, session=session)
        results = list(tool._invoke({}))

        assert len(results) >= 1
        data = get_json_data(results[0])

        assert "accounts" in data
        accounts = data["accounts"]
        print(f"\nFound {len(accounts)} account(s) in chart of accounts")
        for acc in accounts[:10]:
            print(f"  - {acc.get('name', 'N/A')} ({acc.get('account_type', 'N/A')}) - ID: {acc.get('id')}")


# =============================================================================
# ItemManagementTool Tests
# =============================================================================
class TestItemManagementIntegration:
    """Integration tests for ItemManagementTool."""

    def test_list_items(self, runtime, session):
        """Test listing items."""
        from tools.item_management import ItemManagementTool

        tool = ItemManagementTool(runtime=runtime, session=session)
        results = list(tool._invoke({"operation": "list"}))

        assert len(results) >= 1
        data = get_json_data(results[0])

        if data.get("success"):
            items = data.get("items", [])
            print(f"\nFound {len(items)} item(s)")
            for item in items[:5]:
                print(f"  - {item.get('name', 'N/A')} ({item.get('type', 'N/A')}) - ${item.get('unit_price', 0)}")
        else:
            print(f"\n{data.get('message', 'No items')}")


# =============================================================================
# EmployeeManagementTool Tests
# =============================================================================
class TestEmployeeManagementIntegration:
    """Integration tests for EmployeeManagementTool."""

    def test_list_employees(self, runtime, session):
        """Test listing employees."""
        from tools.employee_management import EmployeeManagementTool

        tool = EmployeeManagementTool(runtime=runtime, session=session)
        results = list(tool._invoke({"operation": "list"}))

        assert len(results) >= 1
        data = get_json_data(results[0])

        if data.get("success"):
            employees = data.get("employees", [])
            print(f"\nFound {len(employees)} employee(s)")
            for emp in employees[:5]:
                print(f"  - {emp.get('display_name', 'N/A')} (ID: {emp.get('id')})")
        else:
            print(f"\n{data.get('message', 'No employees')}")


# =============================================================================
# ClassManagementTool Tests
# =============================================================================
class TestClassManagementIntegration:
    """Integration tests for ClassManagementTool."""

    def test_list_classes(self, runtime, session):
        """Test listing classes."""
        from tools.class_management import ClassManagementTool

        tool = ClassManagementTool(runtime=runtime, session=session)
        results = list(tool._invoke({"operation": "list"}))

        assert len(results) >= 1
        data = get_json_data(results[0])

        if data.get("success"):
            classes = data.get("classes", [])
            print(f"\nFound {len(classes)} class(es)")
            for cls in classes[:5]:
                print(f"  - {cls.get('name', 'N/A')} (ID: {cls.get('id')})")
        else:
            print(f"\n{data.get('message', 'No classes')}")


# =============================================================================
# DepartmentManagementTool Tests
# =============================================================================
class TestDepartmentManagementIntegration:
    """Integration tests for DepartmentManagementTool."""

    def test_list_departments(self, runtime, session):
        """Test listing departments."""
        from tools.department_management import DepartmentManagementTool

        tool = DepartmentManagementTool(runtime=runtime, session=session)
        results = list(tool._invoke({"operation": "list"}))

        assert len(results) >= 1
        data = get_json_data(results[0])

        if data.get("success"):
            departments = data.get("departments", [])
            print(f"\nFound {len(departments)} department(s)")
            for dept in departments[:5]:
                print(f"  - {dept.get('name', 'N/A')} (ID: {dept.get('id')})")
        else:
            print(f"\n{data.get('message', 'No departments')}")


# =============================================================================
# QueryEntitiesTool Tests
# =============================================================================
class TestQueryEntitiesIntegration:
    """Integration tests for QueryEntitiesTool."""

    def test_query_invoices(self, runtime, session):
        """Test querying invoices."""
        from tools.query_entities import QueryEntitiesTool

        tool = QueryEntitiesTool(runtime=runtime, session=session)
        results = list(tool._invoke({
            "entity_type": "Invoice",
            "max_results": 10
        }))

        assert len(results) >= 1
        data = get_json_data(results[0])

        if data.get("success"):
            entities = data.get("entities", [])
            print(f"\nFound {data.get('count', 0)} invoice(s)")
            for inv in entities[:5]:
                print(f"  - Invoice #{inv.get('DocNumber', 'N/A')} - ${inv.get('TotalAmt', 0)}")
        else:
            print(f"\n{data.get('message', 'No invoices')}")

    def test_query_bills(self, runtime, session):
        """Test querying bills."""
        from tools.query_entities import QueryEntitiesTool

        tool = QueryEntitiesTool(runtime=runtime, session=session)
        results = list(tool._invoke({
            "entity_type": "Bill",
            "max_results": 10
        }))

        assert len(results) >= 1
        data = get_json_data(results[0])

        if data.get("success"):
            entities = data.get("entities", [])
            print(f"\nFound {data.get('count', 0)} bill(s)")
            for bill in entities[:5]:
                vendor_ref = bill.get('VendorRef', {})
                print(f"  - Bill for {vendor_ref.get('name', 'N/A')} - ${bill.get('TotalAmt', 0)}")
        else:
            print(f"\n{data.get('message', 'No bills')}")

    def test_query_with_custom_sql(self, runtime, session):
        """Test querying with custom SQL."""
        from tools.query_entities import QueryEntitiesTool

        tool = QueryEntitiesTool(runtime=runtime, session=session)
        results = list(tool._invoke({
            "entity_type": "Customer",
            "custom_query": "SELECT * FROM Customer WHERE Active = true MAXRESULTS 5"
        }))

        assert len(results) >= 1
        data = get_json_data(results[0])

        if data.get("success"):
            print(f"\nCustom query returned {data.get('count', 0)} customer(s)")


# =============================================================================
# PaymentManagementTool Tests
# =============================================================================
class TestPaymentManagementIntegration:
    """Integration tests for PaymentManagementTool."""

    def test_list_payments(self, runtime, session):
        """Test listing payments."""
        from tools.payment_management import PaymentManagementTool

        tool = PaymentManagementTool(runtime=runtime, session=session)
        results = list(tool._invoke({"operation": "list"}))

        assert len(results) >= 1
        data = get_json_data(results[0])

        if data.get("success"):
            payments = data.get("payments", [])
            print(f"\nFound {len(payments)} payment(s)")
            for pmt in payments[:5]:
                print(f"  - Payment #{pmt.get('id', 'N/A')} - ${pmt.get('total_amount', 0)}")
        else:
            print(f"\n{data.get('message', 'No payments')}")


# =============================================================================
# EstimateManagementTool Tests
# =============================================================================
class TestEstimateManagementIntegration:
    """Integration tests for EstimateManagementTool."""

    def test_list_estimates(self, runtime, session):
        """Test listing estimates."""
        from tools.estimate_management import EstimateManagementTool

        tool = EstimateManagementTool(runtime=runtime, session=session)
        results = list(tool._invoke({"operation": "list"}))

        assert len(results) >= 1
        data = get_json_data(results[0])

        if data.get("success"):
            estimates = data.get("estimates", [])
            print(f"\nFound {len(estimates)} estimate(s)")
            for est in estimates[:5]:
                print(f"  - Estimate #{est.get('doc_number', 'N/A')} - ${est.get('total_amount', 0)}")
        else:
            print(f"\n{data.get('message', 'No estimates')}")


# =============================================================================
# SalesReceiptManagementTool Tests
# =============================================================================
class TestSalesReceiptManagementIntegration:
    """Integration tests for SalesReceiptManagementTool."""

    def test_list_sales_receipts(self, runtime, session):
        """Test listing sales receipts."""
        from tools.sales_receipt_management import SalesReceiptManagementTool

        tool = SalesReceiptManagementTool(runtime=runtime, session=session)
        results = list(tool._invoke({"operation": "list"}))

        assert len(results) >= 1
        data = get_json_data(results[0])

        if data.get("success"):
            receipts = data.get("sales_receipts", [])
            print(f"\nFound {len(receipts)} sales receipt(s)")
            for sr in receipts[:5]:
                print(f"  - Receipt #{sr.get('doc_number', 'N/A')} - ${sr.get('total_amount', 0)}")
        else:
            print(f"\n{data.get('message', 'No sales receipts')}")


# =============================================================================
# Error Handling Tests
# =============================================================================
class TestErrorHandling:
    """Test error handling with invalid inputs."""

    def test_missing_required_action(self, runtime, session):
        """Test error handling when required action is invalid."""
        from tools.customer_management import CustomerManagementTool

        tool = CustomerManagementTool(runtime=runtime, session=session)

        with pytest.raises(ValueError, match="Unknown action"):
            list(tool._invoke({"action": "invalid_action"}))

    def test_search_without_name(self, runtime, session):
        """Test error when searching without display_name."""
        from tools.customer_management import CustomerManagementTool

        tool = CustomerManagementTool(runtime=runtime, session=session)

        with pytest.raises(ValueError, match="display_name is required"):
            list(tool._invoke({"action": "search"}))


# =============================================================================
# Full Workflow Test
# =============================================================================
class TestFullWorkflow:
    """Test a complete workflow using multiple tools."""

    def test_financial_overview_workflow(self, runtime, session):
        """Test a workflow that gets financial overview."""
        from tools.get_chart_of_accounts import GetChartOfAccountsTool
        from tools.customer_management import CustomerManagementTool
        from tools.vendor_management import VendorManagementTool

        print("\n=== Financial Overview Workflow ===")

        # Step 1: Get chart of accounts
        accounts_tool = GetChartOfAccountsTool(runtime=runtime, session=session)
        account_results = list(accounts_tool._invoke({}))

        account_data = get_json_data(account_results[0])
        accounts = account_data.get("accounts", [])
        print(f"\n1. Chart of Accounts: {len(accounts)} accounts")

        # Count by type
        account_types = {}
        for acc in accounts:
            acc_type = acc.get("account_type", "Other")
            account_types[acc_type] = account_types.get(acc_type, 0) + 1

        for acc_type, count in sorted(account_types.items()):
            print(f"   - {acc_type}: {count}")

        # Step 2: Get customers
        customer_tool = CustomerManagementTool(runtime=runtime, session=session)
        customer_results = list(customer_tool._invoke({"action": "list"}))

        customer_data = get_json_data(customer_results[0])
        customers = customer_data.get("customers", [])
        print(f"\n2. Customers: {len(customers)}")

        # Step 3: Get vendors
        vendor_tool = VendorManagementTool(runtime=runtime, session=session)
        vendor_results = list(vendor_tool._invoke({"action": "list"}))

        vendor_data = get_json_data(vendor_results[0])
        vendors = vendor_data.get("vendors", [])
        print(f"\n3. Vendors: {len(vendors)}")

        print("\n=== Summary ===")
        print(f"Total Accounts: {len(accounts)}")
        print(f"Total Customers: {len(customers)}")
        print(f"Total Vendors: {len(vendors)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
