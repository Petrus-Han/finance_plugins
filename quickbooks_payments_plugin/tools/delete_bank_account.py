from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class DeleteBankAccountTool(Tool):
    """Tool to delete bank accounts from QuickBooks Payments."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """Invoke the delete_bank_account tool."""
        customer_id = tool_parameters.get("customer_id")
        bank_account_id = tool_parameters.get("bank_account_id")

        if not customer_id or not bank_account_id:
            yield self.create_text_message("customer_id and bank_account_id are required")
            return

        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            yield self.create_text_message("QuickBooks Payments API Access Token is required.")
            return

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
                yield self.create_json_message({"success": True, "message": "Bank account deleted successfully"})
            elif response.status_code == 404:
                yield self.create_text_message(f"Customer or bank account not found.")
            elif response.status_code == 401:
                yield self.create_text_message("Authentication failed.")
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                yield self.create_text_message(f"Failed: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            yield self.create_text_message(f"Network error: {str(e)}")
        except Exception as e:
            yield self.create_text_message(f"Unexpected error: {str(e)}")
