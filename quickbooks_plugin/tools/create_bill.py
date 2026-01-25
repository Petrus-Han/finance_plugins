from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class CreateBillTool(Tool):
    """Tool to create a bill (accounts payable) in QuickBooks Online."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the create_bill tool to create a new bill from a vendor.

        Args:
            tool_parameters: Dictionary containing:
                - vendor_id: Vendor ID (required)
                - line_items: JSON array of line items (required)
                - txn_date: Transaction date YYYY-MM-DD (optional)
                - due_date: Due date YYYY-MM-DD (optional)
                - doc_number: Bill reference number (optional)
                - private_note: Internal note (optional)
                - ap_account_id: Accounts Payable account ID (optional)

        Returns:
            Created bill details including ID and total amount
        """
        # Get required parameters
        vendor_id = tool_parameters.get("vendor_id", "").strip()
        line_items_str = tool_parameters.get("line_items", "")

        if not vendor_id:
            raise ValueError("vendor_id is required.")

        if not line_items_str:
            raise ValueError("line_items is required. Provide a JSON array of line items.")

        # Parse line items
        import json
        try:
            if isinstance(line_items_str, str):
                line_items = json.loads(line_items_str)
            else:
                line_items = line_items_str
        except json.JSONDecodeError:
            raise ValueError("line_items must be a valid JSON array.")

        if not isinstance(line_items, list) or len(line_items) == 0:
            raise ValueError("line_items must be a non-empty array.")

        # Get optional parameters
        txn_date = tool_parameters.get("txn_date", "").strip()
        due_date = tool_parameters.get("due_date", "").strip()
        doc_number = tool_parameters.get("doc_number", "").strip()
        private_note = tool_parameters.get("private_note", "").strip()
        ap_account_id = tool_parameters.get("ap_account_id", "").strip()

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        realm_id = self.runtime.credentials.get("realm_id")

        if not access_token or not realm_id:
            raise ToolProviderCredentialValidationError("QuickBooks API Access Token and Realm ID are required.")

        # Get API base URL
        environment = self.runtime.credentials.get("environment", "sandbox")
        if environment == "sandbox":
            api_base_url = "https://sandbox-quickbooks.api.intuit.com/v3"
        else:
            api_base_url = "https://quickbooks.api.intuit.com/v3"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Build line items for QuickBooks Bill format
        qb_lines = []
        for item in line_items:
            line: dict[str, Any] = {
                "Amount": float(item.get("amount", 0)),
                "DetailType": "AccountBasedExpenseLineDetail",
            }

            if item.get("description"):
                line["Description"] = item["description"]

            expense_detail: dict[str, Any] = {}
            if item.get("account_id"):
                expense_detail["AccountRef"] = {"value": str(item["account_id"])}

            if item.get("customer_id"):
                expense_detail["CustomerRef"] = {"value": str(item["customer_id"])}
                expense_detail["BillableStatus"] = item.get("billable_status", "NotBillable")

            if expense_detail:
                line["AccountBasedExpenseLineDetail"] = expense_detail

            qb_lines.append(line)

        # Build request payload
        payload: dict[str, Any] = {
            "VendorRef": {
                "value": vendor_id
            },
            "Line": qb_lines
        }

        if txn_date:
            payload["TxnDate"] = txn_date

        if due_date:
            payload["DueDate"] = due_date

        if doc_number:
            payload["DocNumber"] = doc_number

        if private_note:
            payload["PrivateNote"] = private_note

        if ap_account_id:
            payload["APAccountRef"] = {"value": ap_account_id}

        try:
            response = httpx.post(
                f"{api_base_url}/company/{realm_id}/bill?minorversion=65",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                bill = data.get("Bill", {})

                result = {
                    "success": True,
                    "id": bill.get("Id"),
                    "doc_number": bill.get("DocNumber"),
                    "txn_date": bill.get("TxnDate"),
                    "due_date": bill.get("DueDate"),
                    "total_amount": bill.get("TotalAmt"),
                    "balance": bill.get("Balance"),
                    "vendor": bill.get("VendorRef", {}).get("name"),
                    "ap_account": bill.get("APAccountRef", {}).get("name"),
                    "sync_token": bill.get("SyncToken"),
                    "message": f"Bill #{bill.get('DocNumber', bill.get('Id'))} created successfully"
                }

                for key, value in result.items():
                    yield self.create_variable_message(key, value)
                yield self.create_json_message(result)

            elif response.status_code == 400:
                error_detail = response.json() if response.content else {}
                errors = error_detail.get("Fault", {}).get("Error", [])
                error_msg = errors[0].get("Message", response.text) if errors else response.text
                raise ValueError(f"Invalid request: {error_msg}")

            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your QuickBooks API access token."
                )

            else:
                error_detail = response.json() if response.content else {}
                errors = error_detail.get("Fault", {}).get("Error", [])
                error_msg = errors[0].get("Message", response.text) if errors else response.text
                raise Exception(
                    f"Failed to create bill: {response.status_code} - {error_msg}"
                )

        except httpx.HTTPError as e:
            raise Exception(f"Network error while creating bill: {str(e)}") from e
