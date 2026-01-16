from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class CreateChargeTool(Tool):
    """Tool to create payment charges in QuickBooks Payments."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the create_charge tool to process a payment.

        Args:
            tool_parameters: Dictionary containing charge parameters

        Returns:
            Charge details including status and transaction ID
        """
        # Get required parameters
        amount = tool_parameters.get("amount")
        token = tool_parameters.get("token")

        if not amount or not token:
            yield self.create_text_message("amount and token are required parameters")
            return

        # Get optional parameters
        currency = tool_parameters.get("currency", "USD")
        capture = tool_parameters.get("capture", "true") == "true"
        description = tool_parameters.get("description", "")
        customer_id = tool_parameters.get("customer_id")

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            yield self.create_text_message("QuickBooks Payments API Access Token is required.")
            return

        # Get API base URL
        environment = self.runtime.credentials.get("environment", "sandbox")
        if environment == "sandbox":
            api_base_url = "https://sandbox.api.intuit.com/quickbooks/v4/payments"
        else:
            api_base_url = "https://api.intuit.com/quickbooks/v4/payments"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Build request body
        request_body = {
            "amount": amount,
            "currency": currency,
            "token": token,
            "capture": capture,
            "context": {
                "mobile": False,
                "isEcommerce": True
            }
        }

        if description:
            request_body["description"] = description

        if customer_id:
            request_body["customer"] = {"id": customer_id}

        try:
            # Make API request
            response = httpx.post(
                f"{api_base_url}/charges",
                headers=headers,
                json=request_body,
                timeout=30
            )

            if response.status_code == 201:
                data = response.json()

                # Extract key information
                result = {
                    "id": data.get("id"),
                    "status": data.get("status"),
                    "amount": data.get("amount"),
                    "currency": data.get("currency"),
                    "created": data.get("created"),
                    "auth_code": data.get("authCode"),
                    "captured": capture
                }

                # Add card info if available
                if "card" in data:
                    card = data["card"]
                    result["card"] = {
                        "number": card.get("number"),
                        "card_type": card.get("cardType"),
                        "name": card.get("name")
                    }

                yield self.create_json_message(result)

            elif response.status_code == 400:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                yield self.create_text_message(f"Invalid request: {error_msg}")

            elif response.status_code == 401:
                yield self.create_text_message(
                    "Authentication failed. Please check your QuickBooks Payments API access token."
                )

            elif response.status_code == 402:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", "Payment declined")
                yield self.create_text_message(f"Payment declined: {error_msg}")

            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                yield self.create_text_message(
                    f"Failed to create charge: {response.status_code} - {error_msg}"
                )

        except httpx.HTTPError as e:
            yield self.create_text_message(f"Network error while creating charge: {str(e)}")
        except Exception as e:
            yield self.create_text_message(f"Unexpected error: {str(e)}")
