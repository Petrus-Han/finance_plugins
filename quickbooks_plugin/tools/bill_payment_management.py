import urllib.parse
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class BillPaymentManagementTool(Tool):
    """Tool to manage bill payments (payments to vendors) in QuickBooks."""

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
            elif operation == "void":
                yield from self._void(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "query":
                yield from self._query(api_base_url, realm_id, headers, tool_parameters)
            else:
                raise ValueError(f"Unknown operation: {operation}")
        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _create(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        vendor_id = params.get("vendor_id")
        total_amount = params.get("total_amount")
        pay_type = params.get("pay_type")

        if not all([vendor_id, pay_type]) or total_amount is None:
            raise ValueError("vendor_id, total_amount, and pay_type are required for create")

        payload: dict[str, Any] = {
            "VendorRef": {"value": vendor_id},
            "TotalAmt": total_amount,
            "PayType": pay_type,
            "Line": []
        }

        if params.get("bill_id"):
            payload["Line"].append({
                "Amount": total_amount,
                "LinkedTxn": [{"TxnId": params["bill_id"], "TxnType": "Bill"}]
            })

        if pay_type == "Check":
            bank_account_id = params.get("bank_account_id")
            if not bank_account_id:
                raise ValueError("bank_account_id is required for Check payments")
            payload["CheckPayment"] = {"BankAccountRef": {"value": bank_account_id}}
        elif pay_type == "CreditCard":
            cc_account_id = params.get("credit_card_account_id")
            if not cc_account_id:
                raise ValueError("credit_card_account_id is required for CreditCard payments")
            payload["CreditCardPayment"] = {"CCAccountRef": {"value": cc_account_id}}

        if params.get("txn_date"):
            payload["TxnDate"] = params["txn_date"]
        if params.get("private_note"):
            payload["PrivateNote"] = params["private_note"]

        url = f"{api_base_url}/company/{realm_id}/billpayment?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            result = {
                "success": True,
                "operation": "create",
                "bill_payment": self._format(data.get("BillPayment", {})),
                "message": "Bill payment created successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _read(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        bill_payment_id = params.get("bill_payment_id")
        if not bill_payment_id:
            raise ValueError("bill_payment_id is required for read")

        url = f"{api_base_url}/company/{realm_id}/billpayment/{bill_payment_id}?minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            result = {
                "success": True,
                "operation": "read",
                "bill_payment": self._format(data.get("BillPayment", {})),
                "message": "Bill payment retrieved successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _delete(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        bill_payment_id = params.get("bill_payment_id")
        sync_token = params.get("sync_token")

        if not bill_payment_id or not sync_token:
            raise ValueError("bill_payment_id and sync_token are required for delete")

        payload = {"Id": bill_payment_id, "SyncToken": sync_token}
        url = f"{api_base_url}/company/{realm_id}/billpayment?operation=delete&minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = {
                "success": True,
                "operation": "delete",
                "message": f"Bill payment {bill_payment_id} deleted successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _void(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        bill_payment_id = params.get("bill_payment_id")
        sync_token = params.get("sync_token")

        if not bill_payment_id or not sync_token:
            raise ValueError("bill_payment_id and sync_token are required for void")

        payload = {"Id": bill_payment_id, "SyncToken": sync_token, "sparse": True}
        url = f"{api_base_url}/company/{realm_id}/billpayment?operation=update&include=void&minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = {
                "success": True,
                "operation": "void",
                "message": f"Bill payment {bill_payment_id} voided successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _query(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        query_string = params.get("query_string", "")
        query = "SELECT * FROM BillPayment"
        if query_string:
            query += f" WHERE {query_string}"

        encoded_query = urllib.parse.quote(query)
        url = f"{api_base_url}/company/{realm_id}/query?query={encoded_query}&minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            items = data.get("QueryResponse", {}).get("BillPayment", [])
            result = {
                "success": True,
                "operation": "query",
                "bill_payments": [self._format(item) for item in items],
                "count": len(items),
                "message": f"Found {len(items)} bill payments"
            }
            # Only create variable messages for scalar values
            yield self.create_variable_message("success", True)
            yield self.create_variable_message("operation", "query")
            yield self.create_variable_message("count", len(items))
            yield self.create_variable_message("message", f"Found {len(items)} bill payments")
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _format(self, item: dict) -> dict:
        return {
            "id": item.get("Id"),
            "sync_token": item.get("SyncToken"),
            "vendor_id": item.get("VendorRef", {}).get("value"),
            "vendor_name": item.get("VendorRef", {}).get("name"),
            "total_amount": item.get("TotalAmt"),
            "pay_type": item.get("PayType"),
            "txn_date": item.get("TxnDate"),
            "private_note": item.get("PrivateNote"),
            "lines": item.get("Line", []),
        }

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed.")
        error_detail = response.json() if response.content else {}
        error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
