from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class DeleteBankAccountTool(Tool):
    """Tool to delete bank accounts from QuickBooks Payments."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """Invoke the delete_bank_account tool."""
        customer_id = tool_parameters.get("customer_id")
        bank_account_id = tool_parameters.get("bank_account_id")

        if not customer_id or not bank_account_id:
            raise ValueError("customer_id and bank_account_id are required")

        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ToolProviderCredentialValidationError("QuickBooks Payments API Access Token is required.")

        environment = self.runtime.credentials.get("environment", "sandbox")
        api_base_url = "https://sandbox.api.intuit.com/quickbooks/v4/payments" if environment == "sandbox" else "https://api.intuit.com/quickbooks/v4/payments"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

        try:
            response = httpx.delete(
                f"{api_base_url}/customers/{customer_id}/bank-accounts/{bank_account_id}",
                headers=headers,
                timeout=30
            )

            if response.status_code == 204:
                result = {"success": True, "message": "Bank account deleted successfully"}
                for key, value in result.items():
                    yield self.create_variable_message(key, value)
                yield self.create_json_message(result)
            elif response.status_code == 404:
                raise ValueError("Customer or bank account not found.")
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError("Authentication failed. Please check your access token.")
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e
