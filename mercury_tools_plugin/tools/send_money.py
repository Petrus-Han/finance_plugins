from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class SendMoneyTool(Tool):
    """Tool to request sending money from a Mercury account."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the send_money tool to request a payment.

        Note: This creates a send money request that may require approval
        depending on your Mercury account settings.

        Args:
            tool_parameters: Dictionary containing:
                - account_id: Source account ID (required)
                - recipient_id: Recipient ID (required)
                - amount: Amount to send (required, positive number)
                - payment_method: ach, wire, or check (default: ach)
                - idempotency_key: Unique key for deduplication (optional)
                - note: Internal note (optional)
                - external_memo: External memo visible to recipient (optional)

        Returns:
            Send money request details including status
        """
        # Get required parameters
        account_id = tool_parameters.get("account_id", "").strip()
        recipient_id = tool_parameters.get("recipient_id", "").strip()
        amount = tool_parameters.get("amount")

        if not account_id:
            raise ValueError("account_id is required.")

        if not recipient_id:
            raise ValueError("recipient_id is required.")

        if not amount or float(amount) <= 0:
            raise ValueError("amount must be a positive number.")

        # Get optional parameters
        payment_method = tool_parameters.get("payment_method", "ach")
        idempotency_key = tool_parameters.get("idempotency_key", "").strip()
        note = tool_parameters.get("note", "").strip()
        external_memo = tool_parameters.get("external_memo", "").strip()

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        # Get API environment
        api_environment = self.runtime.credentials.get("api_environment", "production")

        # Determine API base URL based on environment
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json;charset=utf-8",
        }

        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key

        # Build request body
        request_data: dict[str, Any] = {
            "recipientId": recipient_id,
            "amount": float(amount),
            "paymentMethod": payment_method,
        }

        if note:
            request_data["note"] = note

        if external_memo:
            request_data["externalMemo"] = external_memo

        try:
            response = httpx.post(
                f"{api_base_url}/account/{account_id}/request-send-money",
                headers=headers,
                json=request_data,
                timeout=30
            )

            if response.status_code in (200, 201, 202):
                data = response.json()

                result = {
                    "success": True,
                    "request_id": data.get("id", ""),
                    "status": data.get("status", ""),
                    "amount": data.get("amount"),
                    "recipient_id": data.get("recipientId", ""),
                    "payment_method": data.get("paymentMethod", ""),
                    "created_at": data.get("createdAt", ""),
                    "message": f"Send money request created for ${amount}"
                }

                # Add transaction ID if payment was immediately processed
                if data.get("transactionId"):
                    result["transaction_id"] = data.get("transactionId")

                # Yield each field as a separate variable for direct access
                for key, value in result.items():
                    yield self.create_variable_message(key, value)

                # Also yield the full JSON for convenience
                yield self.create_json_message(result)

            elif response.status_code == 400:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", "Invalid request")
                raise Exception(f"Failed to send money: {error_msg}")

            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your Mercury API access token."
                )

            elif response.status_code == 403:
                raise Exception(
                    "Permission denied. Your API token may not have permission to send money."
                )

            elif response.status_code == 404:
                raise ValueError("Account or recipient not found. Please verify the IDs.")

            elif response.status_code == 422:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", "Validation error")
                raise Exception(f"Validation error: {error_msg}")

            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to send money: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while sending money: {str(e)}") from e
