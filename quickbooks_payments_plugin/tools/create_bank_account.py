from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class CreateBankAccountTool(Tool):
    """Tool to create bank accounts in QuickBooks Payments."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """Invoke the create_bank_account tool."""
        customer_id = tool_parameters.get("customer_id")
        routing_number = tool_parameters.get("routing_number")
        account_number = tool_parameters.get("account_number")
        account_type = tool_parameters.get("account_type")
        name = tool_parameters.get("name")

        if not all([customer_id, routing_number, account_number, account_type, name]):
            yield self.create_text_message("customer_id, routing_number, account_number, account_type, and name are required")
            return

        phone = tool_parameters.get("phone")

        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            yield self.create_text_message("QuickBooks Payments API Access Token is required.")
            return

        environment = self.runtime.credentials.get("environment", "sandbox")
        api_base_url = "https://sandbox.api.intuit.com/quickbooks/v4/payments" if environment == "sandbox" else "https://api.intuit.com/quickbooks/v4/payments"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        request_body = {
            "routingNumber": routing_number,
            "accountNumber": account_number,
            "accountType": account_type,
            "name": name
        }
        if phone:
            request_body["phone"] = phone

        try:
            response = httpx.post(
                f"{api_base_url}/customers/{customer_id}/bank-accounts",
                headers=headers,
                json=request_body,
                timeout=30
            )

            if response.status_code == 201:
                data = response.json()
                yield self.create_json_message(data)
            elif response.status_code == 404:
                yield self.create_text_message(f"Customer with ID '{customer_id}' not found.")
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
