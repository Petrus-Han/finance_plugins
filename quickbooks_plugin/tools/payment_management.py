import urllib.parse
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class PaymentManagementTool(Tool):
    """Tool to manage customer payments in QuickBooks."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        access_token = self.runtime.credentials.get("access_token")
        realm_id = self.runtime.credentials.get("realm_id")

        if not access_token or not realm_id:
            raise ToolProviderCredentialValidationError("QuickBooks credentials required.")

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

        operation = tool_parameters.get("operation")
        if not operation:
            raise ValueError("operation is required")

        try:
            if operation == "create":
                yield from self._create_payment(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "read":
                yield from self._read_payment(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "update":
                yield from self._update_payment(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "delete":
                yield from self._delete_payment(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "void":
                yield from self._void_payment(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "query":
                yield from self._query_payments(api_base_url, realm_id, headers, tool_parameters)
            else:
                raise ValueError(f"Unknown operation: {operation}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _create_payment(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        customer_id = params.get("customer_id")
        total_amount = params.get("total_amount")

        if not customer_id or total_amount is None:
            raise ValueError("customer_id and total_amount are required for create")

        payload: dict[str, Any] = {
            "CustomerRef": {"value": customer_id},
            "TotalAmt": total_amount
        }

        if params.get("txn_date"):
            payload["TxnDate"] = params["txn_date"]
        if params.get("deposit_to_account_id"):
            payload["DepositToAccountRef"] = {"value": params["deposit_to_account_id"]}
        if params.get("payment_method_id"):
            payload["PaymentMethodRef"] = {"value": params["payment_method_id"]}
        if params.get("private_note"):
            payload["PrivateNote"] = params["private_note"]

        if params.get("invoice_id"):
            payload["Line"] = [{
                "Amount": total_amount,
                "LinkedTxn": [{"TxnId": params["invoice_id"], "TxnType": "Invoice"}]
            }]

        url = f"{api_base_url}/company/{realm_id}/payment?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            payment = data.get("Payment", {})
            result = {
                "success": True,
                "operation": "create",
                "payment": self._format_payment(payment),
                "message": "Payment created successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _read_payment(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        payment_id = params.get("payment_id")
        if not payment_id:
            raise ValueError("payment_id is required for read")

        url = f"{api_base_url}/company/{realm_id}/payment/{payment_id}?minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            payment = data.get("Payment", {})
            result = {
                "success": True,
                "operation": "read",
                "payment": self._format_payment(payment),
                "message": "Payment retrieved successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        elif response.status_code == 404:
            raise ValueError(f"Payment not found: {payment_id}")
        else:
            self._handle_error(response)

    def _update_payment(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        payment_id = params.get("payment_id")
        sync_token = params.get("sync_token")
        customer_id = params.get("customer_id")
        total_amount = params.get("total_amount")

        if not all([payment_id, sync_token, customer_id]) or total_amount is None:
            raise ValueError("payment_id, sync_token, customer_id, and total_amount are required for update")

        payload: dict[str, Any] = {
            "Id": payment_id,
            "SyncToken": sync_token,
            "CustomerRef": {"value": customer_id},
            "TotalAmt": total_amount
        }

        if params.get("txn_date"):
            payload["TxnDate"] = params["txn_date"]
        if params.get("private_note"):
            payload["PrivateNote"] = params["private_note"]

        url = f"{api_base_url}/company/{realm_id}/payment?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            payment = data.get("Payment", {})
            result = {
                "success": True,
                "operation": "update",
                "payment": self._format_payment(payment),
                "message": "Payment updated successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _delete_payment(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        payment_id = params.get("payment_id")
        sync_token = params.get("sync_token")

        if not payment_id or not sync_token:
            raise ValueError("payment_id and sync_token are required for delete")

        payload = {"Id": payment_id, "SyncToken": sync_token}
        url = f"{api_base_url}/company/{realm_id}/payment?operation=delete&minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = {
                "success": True,
                "operation": "delete",
                "message": f"Payment {payment_id} deleted successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _void_payment(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        payment_id = params.get("payment_id")
        sync_token = params.get("sync_token")

        if not payment_id or not sync_token:
            raise ValueError("payment_id and sync_token are required for void")

        payload = {"Id": payment_id, "SyncToken": sync_token}
        url = f"{api_base_url}/company/{realm_id}/payment?operation=void&minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = {
                "success": True,
                "operation": "void",
                "message": f"Payment {payment_id} voided successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _query_payments(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        query_string = params.get("query_string", "")
        query = f"SELECT * FROM Payment"
        if query_string:
            query += f" WHERE {query_string}"

        encoded_query = urllib.parse.quote(query)
        url = f"{api_base_url}/company/{realm_id}/query?query={encoded_query}&minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            payments = data.get("QueryResponse", {}).get("Payment", [])
            result = {
                "success": True,
                "operation": "query",
                "payments": [self._format_payment(p) for p in payments],
                "count": len(payments),
                "message": f"Found {len(payments)} payments"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _format_payment(self, payment: dict) -> dict:
        return {
            "id": payment.get("Id"),
            "sync_token": payment.get("SyncToken"),
            "customer_id": payment.get("CustomerRef", {}).get("value"),
            "customer_name": payment.get("CustomerRef", {}).get("name"),
            "total_amount": payment.get("TotalAmt"),
            "unapplied_amount": payment.get("UnappliedAmt"),
            "txn_date": payment.get("TxnDate"),
            "private_note": payment.get("PrivateNote"),
            "deposit_to_account_id": payment.get("DepositToAccountRef", {}).get("value") if payment.get("DepositToAccountRef") else None,
            "payment_method_id": payment.get("PaymentMethodRef", {}).get("value") if payment.get("PaymentMethodRef") else None,
            "lines": payment.get("Line", []),
            "created_at": payment.get("MetaData", {}).get("CreateTime"),
            "updated_at": payment.get("MetaData", {}).get("LastUpdatedTime"),
        }

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed.")
        error_detail = response.json() if response.content else {}
        error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
