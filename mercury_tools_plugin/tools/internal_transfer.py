from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class InternalTransferTool(Tool):
    """Tool to create an internal transfer between Mercury accounts."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the internal_transfer tool to move funds between accounts.

        Args:
            tool_parameters: Dictionary containing:
                - from_account_id: Source account ID (required)
                - to_account_id: Destination account ID (required)
                - amount: Amount to transfer (required, positive number)
                - idempotency_key: Unique key for deduplication (optional)
                - note: Internal note (optional)

        Returns:
            Transfer details including transaction ID
        """
        # Get required parameters
        from_account_id = tool_parameters.get("from_account_id", "").strip()
        to_account_id = tool_parameters.get("to_account_id", "").strip()
        amount = tool_parameters.get("amount")

        if not from_account_id:
            raise ValueError("from_account_id is required.")

        if not to_account_id:
            raise ValueError("to_account_id is required.")

        if from_account_id == to_account_id:
            raise ValueError("Source and destination accounts must be different.")

        if not amount or float(amount) <= 0:
            raise ValueError("amount must be a positive number.")

        # Get optional parameters
        idempotency_key = tool_parameters.get("idempotency_key", "").strip()
        note = tool_parameters.get("note", "").strip()

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
        transfer_data: dict[str, Any] = {
            "fromAccountId": from_account_id,
            "toAccountId": to_account_id,
            "amount": float(amount),
        }

        if note:
            transfer_data["note"] = note

        try:
            response = httpx.post(
                f"{api_base_url}/transfer",
                headers=headers,
                json=transfer_data,
                timeout=30
            )

            if response.status_code in (200, 201):
                data = response.json()

                result = {
                    "success": True,
                    "transaction_id": data.get("id", ""),
                    "status": data.get("status", ""),
                    "amount": data.get("amount"),
                    "from_account_id": data.get("fromAccountId", from_account_id),
                    "to_account_id": data.get("toAccountId", to_account_id),
                    "created_at": data.get("createdAt", ""),
                    "message": f"Successfully transferred ${amount}"
                }

                yield self.create_json_message(result)

            elif response.status_code == 400:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", "Invalid request")
                raise Exception(f"Failed to create transfer: {error_msg}")

            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your Mercury API access token."
                )

            elif response.status_code == 403:
                raise Exception(
                    "Permission denied. Your API token may not have permission to create transfers."
                )

            elif response.status_code == 404:
                raise ValueError("Account not found. Please verify the account IDs.")

            elif response.status_code == 422:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", "Validation error - possibly insufficient funds")
                raise Exception(f"Transfer failed: {error_msg}")

            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to create transfer: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while creating transfer: {str(e)}") from e
