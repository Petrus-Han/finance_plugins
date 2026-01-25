from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class CreateRefundTool(Tool):
    """Tool to create refunds in QuickBooks Payments."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """Invoke the create_refund tool to refund a charge."""
        charge_id = tool_parameters.get("charge_id")
        if not charge_id:
            raise ValueError("charge_id is required")

        amount = tool_parameters.get("amount")
        description = tool_parameters.get("description", "")

        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ToolProviderCredentialValidationError("QuickBooks Payments API Access Token is required.")

        environment = self.runtime.credentials.get("environment", "sandbox")
        api_base_url = "https://sandbox.api.intuit.com/quickbooks/v4/payments" if environment == "sandbox" else "https://api.intuit.com/quickbooks/v4/payments"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        request_body = {}
        if amount:
            request_body["amount"] = amount
        if description:
            request_body["description"] = description

        try:
            response = httpx.post(
                f"{api_base_url}/charges/{charge_id}/refunds",
                headers=headers,
                json=request_body,
                timeout=30
            )

            if response.status_code == 201:
                data = response.json()
                for key, value in data.items():
                    yield self.create_variable_message(key, value)
                yield self.create_json_message(data)
            elif response.status_code == 404:
                raise ValueError(f"Charge with ID '{charge_id}' not found.")
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError("Authentication failed. Please check your access token.")
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to create refund: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e
