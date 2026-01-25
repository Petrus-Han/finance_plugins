from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class CreateTokenTool(Tool):
    """Tool to create payment tokens for QuickBooks Payments."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the create_token tool to tokenize payment information.

        Args:
            tool_parameters: Dictionary containing payment information

        Returns:
            Payment token that can be used for charges
        """
        # Get payment type
        payment_type = tool_parameters.get("payment_type")
        if not payment_type or payment_type not in ["card", "bank_account"]:
            raise ValueError("payment_type is required and must be 'card' or 'bank_account'")

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ToolProviderCredentialValidationError("QuickBooks Payments API Access Token is required.")

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

        # Build request body based on payment type
        if payment_type == "card":
            # Validate card parameters
            card_number = tool_parameters.get("card_number")
            card_exp_month = tool_parameters.get("card_exp_month")
            card_exp_year = tool_parameters.get("card_exp_year")
            card_cvc = tool_parameters.get("card_cvc")
            card_name = tool_parameters.get("card_name")

            if not all([card_number, card_exp_month, card_exp_year, card_cvc, card_name]):
                raise ValueError(
                    "For card payments, all fields are required: card_number, card_exp_month, "
                    "card_exp_year, card_cvc, card_name"
                )

            request_body = {
                "card": {
                    "number": card_number,
                    "expMonth": card_exp_month,
                    "expYear": card_exp_year,
                    "cvc": card_cvc,
                    "name": card_name
                }
            }

        else:  # bank_account
            # Validate bank account parameters
            routing_number = tool_parameters.get("bank_routing_number")
            account_number = tool_parameters.get("bank_account_number")
            account_type = tool_parameters.get("bank_account_type")
            account_name = tool_parameters.get("bank_account_name")

            if not all([routing_number, account_number, account_type, account_name]):
                raise ValueError(
                    "For bank account payments, all fields are required: bank_routing_number, "
                    "bank_account_number, bank_account_type, bank_account_name"
                )

            request_body = {
                "bankAccount": {
                    "routingNumber": routing_number,
                    "accountNumber": account_number,
                    "accountType": account_type,
                    "name": account_name
                }
            }

        try:
            # Make API request
            response = httpx.post(
                f"{api_base_url}/tokens",
                headers=headers,
                json=request_body,
                timeout=30
            )

            if response.status_code == 201:
                data = response.json()
                token_value = data.get("value")
                created_at = data.get("createdAt")

                result = {
                    "token": token_value,
                    "created_at": created_at,
                    "payment_type": payment_type,
                    "note": "This token is single-use and expires after 15 minutes"
                }

                for key, value in result.items():
                    yield self.create_variable_message(key, value)
                yield self.create_json_message(result)

            elif response.status_code == 400:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise ValueError(f"Invalid request: {error_msg}")

            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your QuickBooks Payments API access token."
                )

            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to create token: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while creating token: {str(e)}") from e
