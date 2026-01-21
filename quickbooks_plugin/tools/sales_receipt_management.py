import json
import urllib.parse
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class SalesReceiptManagementTool(Tool):
    """Tool to manage sales receipts in QuickBooks."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        access_token = self.runtime.credentials.get("access_token")
        realm_id = self.runtime.credentials.get("realm_id")

        if not access_token or not realm_id:
            raise ToolProviderCredentialValidationError("QuickBooks credentials required.")

        environment = self.runtime.credentials.get("environment", "sandbox")
        api_base_url = f"https://{'sandbox-' if environment == 'sandbox' else ''}quickbooks.api.intuit.com/v3"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        operation = tool_parameters.get("operation")
        if not operation:
            raise ValueError("operation is required")

        try:
            if operation == "create":
                yield from self._create(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "read":
                yield from self._read(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "delete":
                yield from self._delete(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "query":
                yield from self._query(api_base_url, realm_id, headers, tool_parameters)
            else:
                raise ValueError(f"Unknown operation: {operation}")
        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _create(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        lines_json = params.get("lines_json")
        if not lines_json:
            raise ValueError("lines_json is required for create")

        try:
            lines_data = json.loads(lines_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid lines_json: {e}")

        formatted_lines = []
        for line in lines_data:
            formatted_lines.append({
                "DetailType": "SalesItemLineDetail",
                "Amount": line.get("Amount"),
                "SalesItemLineDetail": {
                    "ItemRef": line.get("ItemRef"),
                    "Qty": line.get("Qty", 1),
                    "UnitPrice": line.get("UnitPrice")
                }
            })

        payload: dict[str, Any] = {"Line": formatted_lines}

        if params.get("customer_id"):
            payload["CustomerRef"] = {"value": params["customer_id"]}
        if params.get("deposit_to_account_id"):
            payload["DepositToAccountRef"] = {"value": params["deposit_to_account_id"]}
        if params.get("payment_method_id"):
            payload["PaymentMethodRef"] = {"value": params["payment_method_id"]}
        if params.get("txn_date"):
            payload["TxnDate"] = params["txn_date"]
        if params.get("private_note"):
            payload["PrivateNote"] = params["private_note"]

        url = f"{api_base_url}/company/{realm_id}/salesreceipt?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            yield self.create_json_message({
                "success": True,
                "operation": "create",
                "sales_receipt": self._format(data.get("SalesReceipt", {})),
                "message": "Sales receipt created successfully"
            })
        else:
            self._handle_error(response)

    def _read(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        sr_id = params.get("sales_receipt_id")
        if not sr_id:
            raise ValueError("sales_receipt_id is required for read")

        url = f"{api_base_url}/company/{realm_id}/salesreceipt/{sr_id}?minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            yield self.create_json_message({
                "success": True,
                "operation": "read",
                "sales_receipt": self._format(data.get("SalesReceipt", {})),
                "message": "Sales receipt retrieved successfully"
            })
        else:
            self._handle_error(response)

    def _delete(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        sr_id = params.get("sales_receipt_id")
        sync_token = params.get("sync_token")

        if not sr_id or not sync_token:
            raise ValueError("sales_receipt_id and sync_token are required for delete")

        payload = {"Id": sr_id, "SyncToken": sync_token}
        url = f"{api_base_url}/company/{realm_id}/salesreceipt?operation=delete&minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            yield self.create_json_message({
                "success": True,
                "operation": "delete",
                "message": f"Sales receipt {sr_id} deleted successfully"
            })
        else:
            self._handle_error(response)

    def _query(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        query_string = params.get("query_string", "")
        query = "SELECT * FROM SalesReceipt"
        if query_string:
            query += f" WHERE {query_string}"

        encoded_query = urllib.parse.quote(query)
        url = f"{api_base_url}/company/{realm_id}/query?query={encoded_query}&minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            items = data.get("QueryResponse", {}).get("SalesReceipt", [])
            yield self.create_json_message({
                "success": True,
                "operation": "query",
                "sales_receipts": [self._format(item) for item in items],
                "count": len(items),
                "message": f"Found {len(items)} sales receipts"
            })
        else:
            self._handle_error(response)

    def _format(self, item: dict) -> dict:
        return {
            "id": item.get("Id"),
            "sync_token": item.get("SyncToken"),
            "doc_number": item.get("DocNumber"),
            "customer_id": item.get("CustomerRef", {}).get("value") if item.get("CustomerRef") else None,
            "customer_name": item.get("CustomerRef", {}).get("name") if item.get("CustomerRef") else None,
            "txn_date": item.get("TxnDate"),
            "total_amount": item.get("TotalAmt"),
            "balance": item.get("Balance"),
            "lines": item.get("Line", []),
        }

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed.")
        error_detail = response.json() if response.content else {}
        error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
