from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class CreateInvoiceTool(Tool):
    """Tool to create an invoice in QuickBooks Online."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the create_invoice tool to create a new invoice.

        Args:
            tool_parameters: Dictionary containing:
                - customer_id: Customer ID (required)
                - line_items: JSON array of line items (required)
                - txn_date: Transaction date YYYY-MM-DD (optional)
                - due_date: Due date YYYY-MM-DD (optional)
                - doc_number: Invoice number (optional, auto-generated if not provided)
                - customer_memo: Message to customer (optional)
                - private_note: Internal note (optional)
                - bill_email: Email to send invoice to (optional)

        Returns:
            Created invoice details including ID and total amount
        """
        # Get required parameters
        customer_id = tool_parameters.get("customer_id", "").strip()
        line_items_str = tool_parameters.get("line_items", "")

        if not customer_id:
            raise ValueError("customer_id is required.")

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
        customer_memo = tool_parameters.get("customer_memo", "").strip()
        private_note = tool_parameters.get("private_note", "").strip()
        bill_email = tool_parameters.get("bill_email", "").strip()

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

        # Build line items for QuickBooks format
        qb_lines = []
        for idx, item in enumerate(line_items):
            line = {
                "Amount": float(item.get("amount", 0)),
                "DetailType": "SalesItemLineDetail",
            }

            if item.get("description"):
                line["Description"] = item["description"]

            sales_detail = {}
            if item.get("item_id"):
                sales_detail["ItemRef"] = {"value": str(item["item_id"])}
            if item.get("quantity"):
                sales_detail["Qty"] = float(item["quantity"])
            if item.get("unit_price"):
                sales_detail["UnitPrice"] = float(item["unit_price"])

            if sales_detail:
                line["SalesItemLineDetail"] = sales_detail

            qb_lines.append(line)

        # Build request payload
        payload: dict[str, Any] = {
            "CustomerRef": {
                "value": customer_id
            },
            "Line": qb_lines
        }

        if txn_date:
            payload["TxnDate"] = txn_date

        if due_date:
            payload["DueDate"] = due_date

        if doc_number:
            payload["DocNumber"] = doc_number

        if customer_memo:
            payload["CustomerMemo"] = {"value": customer_memo}

        if private_note:
            payload["PrivateNote"] = private_note

        if bill_email:
            payload["BillEmail"] = {"Address": bill_email}

        try:
            response = httpx.post(
                f"{api_base_url}/company/{realm_id}/invoice?minorversion=65",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                invoice = data.get("Invoice", {})

                result = {
                    "success": True,
                    "id": invoice.get("Id"),
                    "doc_number": invoice.get("DocNumber"),
                    "txn_date": invoice.get("TxnDate"),
                    "due_date": invoice.get("DueDate"),
                    "total_amount": invoice.get("TotalAmt"),
                    "balance": invoice.get("Balance"),
                    "customer": invoice.get("CustomerRef", {}).get("name"),
                    "email_status": invoice.get("EmailStatus"),
                    "sync_token": invoice.get("SyncToken"),
                    "message": f"Invoice #{invoice.get('DocNumber', invoice.get('Id'))} created successfully"
                }

                if invoice.get("InvoiceLink"):
                    result["invoice_link"] = invoice.get("InvoiceLink")

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
                    f"Failed to create invoice: {response.status_code} - {error_msg}"
                )

        except httpx.HTTPError as e:
            raise Exception(f"Network error while creating invoice: {str(e)}") from e
