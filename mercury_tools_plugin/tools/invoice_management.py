import json
import logging
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin.config.logger_format import plugin_logger_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(plugin_logger_handler)


class InvoiceManagementTool(Tool):
    """Tool to manage AR invoices - CRUD + cancel operations."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        logger.info("=== InvoiceManagementTool._invoke called ===")

        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        api_environment = self.runtime.credentials.get("api_environment", "production")
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }

        operation = tool_parameters.get("operation")
        if not operation:
            raise ValueError("operation is required")

        try:
            if operation == "list":
                yield from self._list_invoices(api_base_url, headers)
            elif operation == "get":
                invoice_id = tool_parameters.get("invoice_id")
                if not invoice_id:
                    raise ValueError("invoice_id is required for get operation")
                yield from self._get_invoice(api_base_url, headers, invoice_id)
            elif operation == "create":
                yield from self._create_invoice(api_base_url, headers, tool_parameters)
            elif operation == "update":
                invoice_id = tool_parameters.get("invoice_id")
                if not invoice_id:
                    raise ValueError("invoice_id is required for update operation")
                yield from self._update_invoice(api_base_url, headers, invoice_id, tool_parameters)
            elif operation == "cancel":
                invoice_id = tool_parameters.get("invoice_id")
                if not invoice_id:
                    raise ValueError("invoice_id is required for cancel operation")
                yield from self._cancel_invoice(api_base_url, headers, invoice_id)
            else:
                raise ValueError(f"Unknown operation: {operation}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _list_invoices(self, api_base_url: str, headers: dict) -> Generator[ToolInvokeMessage, None, None]:
        response = httpx.get(f"{api_base_url}/ar/invoices", headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            invoices = [self._format_invoice(inv) for inv in data.get("invoices", [])]
            yield self.create_json_message({
                "success": True,
                "operation": "list",
                "invoices": invoices,
                "message": f"Found {len(invoices)} invoices"
            })
        else:
            self._handle_error(response)

    def _get_invoice(self, api_base_url: str, headers: dict, invoice_id: str) -> Generator[ToolInvokeMessage, None, None]:
        response = httpx.get(f"{api_base_url}/ar/invoices/{invoice_id}", headers=headers, timeout=15)
        if response.status_code == 200:
            invoice = self._format_invoice(response.json())
            yield self.create_json_message({
                "success": True,
                "operation": "get",
                "invoice": invoice,
                "message": "Invoice retrieved successfully"
            })
        elif response.status_code == 404:
            raise ValueError(f"Invoice not found: {invoice_id}")
        else:
            self._handle_error(response)

    def _create_invoice(self, api_base_url: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        customer_id = params.get("customer_id")
        destination_account_id = params.get("destination_account_id")
        invoice_date = params.get("invoice_date")
        due_date = params.get("due_date")
        line_items_json = params.get("line_items_json")

        if not all([customer_id, destination_account_id, invoice_date, due_date, line_items_json]):
            raise ValueError("customer_id, destination_account_id, invoice_date, due_date, and line_items_json are required")

        try:
            line_items = json.loads(line_items_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid line_items_json: {e}")

        payload: dict[str, Any] = {
            "customerId": customer_id,
            "destinationAccountId": destination_account_id,
            "invoiceDate": invoice_date,
            "dueDate": due_date,
            "lineItems": line_items,
            "creditCardEnabled": params.get("credit_card_enabled", True),
            "achDebitEnabled": params.get("ach_debit_enabled", True),
        }

        if params.get("invoice_number"):
            payload["invoiceNumber"] = params["invoice_number"]
        if params.get("po_number"):
            payload["poNumber"] = params["po_number"]
        if params.get("payer_memo"):
            payload["payerMemo"] = params["payer_memo"]
        if params.get("internal_note"):
            payload["internalNote"] = params["internal_note"]

        response = httpx.post(f"{api_base_url}/ar/invoices", headers=headers, json=payload, timeout=15)
        if response.status_code in (200, 201):
            invoice = self._format_invoice(response.json())
            yield self.create_json_message({
                "success": True,
                "operation": "create",
                "invoice": invoice,
                "message": "Invoice created successfully"
            })
        else:
            self._handle_error(response)

    def _update_invoice(self, api_base_url: str, headers: dict, invoice_id: str, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        payload: dict[str, Any] = {}

        if params.get("due_date"):
            payload["dueDate"] = params["due_date"]
        if params.get("invoice_date"):
            payload["invoiceDate"] = params["invoice_date"]
        if params.get("invoice_number"):
            payload["invoiceNumber"] = params["invoice_number"]
        if params.get("po_number"):
            payload["poNumber"] = params["po_number"]
        if params.get("payer_memo"):
            payload["payerMemo"] = params["payer_memo"]
        if params.get("internal_note"):
            payload["internalNote"] = params["internal_note"]
        if params.get("line_items_json"):
            try:
                payload["lineItems"] = json.loads(params["line_items_json"])
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid line_items_json: {e}")
        if "credit_card_enabled" in params:
            payload["creditCardEnabled"] = params["credit_card_enabled"]
        if "ach_debit_enabled" in params:
            payload["achDebitEnabled"] = params["ach_debit_enabled"]

        if not payload:
            raise ValueError("No fields to update")

        response = httpx.post(f"{api_base_url}/ar/invoices/{invoice_id}", headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            invoice = self._format_invoice(response.json())
            yield self.create_json_message({
                "success": True,
                "operation": "update",
                "invoice": invoice,
                "message": "Invoice updated successfully"
            })
        elif response.status_code == 404:
            raise ValueError(f"Invoice not found: {invoice_id}")
        else:
            self._handle_error(response)

    def _cancel_invoice(self, api_base_url: str, headers: dict, invoice_id: str) -> Generator[ToolInvokeMessage, None, None]:
        response = httpx.post(f"{api_base_url}/ar/invoices/{invoice_id}/cancel", headers=headers, timeout=15)
        if response.status_code in (200, 204):
            yield self.create_json_message({
                "success": True,
                "operation": "cancel",
                "message": f"Invoice {invoice_id} cancelled successfully"
            })
        elif response.status_code == 404:
            raise ValueError(f"Invoice not found: {invoice_id}")
        else:
            self._handle_error(response)

    def _format_invoice(self, invoice: dict) -> dict:
        return {
            "id": invoice.get("id", ""),
            "status": invoice.get("status", ""),
            "amount": invoice.get("amount", 0),
            "invoice_number": invoice.get("invoiceNumber"),
            "po_number": invoice.get("poNumber"),
            "invoice_date": invoice.get("invoiceDate"),
            "due_date": invoice.get("dueDate"),
            "customer_id": invoice.get("customerId"),
            "destination_account_id": invoice.get("destinationAccountId"),
            "slug": invoice.get("slug"),
            "payer_memo": invoice.get("payerMemo"),
            "internal_note": invoice.get("internalNote"),
            "credit_card_enabled": invoice.get("creditCardEnabled"),
            "ach_debit_enabled": invoice.get("achDebitEnabled"),
            "created_at": invoice.get("createdAt"),
            "updated_at": invoice.get("updatedAt"),
            "canceled_at": invoice.get("canceledAt"),
            "line_items": invoice.get("lineItems", []),
        }

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed. Check your API token.")

        error_detail = response.json() if response.content else {}

        # Check for AR subscription error
        if response.status_code == 403:
            errors = error_detail.get("errors", {})
            if "subscriptions" in errors:
                raise Exception(
                    "This feature requires a Mercury AR (Accounts Receivable) subscription. "
                    "Please subscribe to AR in your Mercury Dashboard under Plan & Billing. "
                    "Learn more: https://mercury.com/pricing"
                )

        error_msg = error_detail.get("message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
