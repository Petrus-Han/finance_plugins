from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class UpdateTransactionTool(Tool):
    """Tool to update metadata for a Mercury transaction."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the update_transaction tool to modify transaction metadata.

        Args:
            tool_parameters: Dictionary containing:
                - transaction_id: The transaction ID (required)
                - note: Internal note (optional)
                - category_id: Category ID (optional)

        Returns:
            Updated transaction information
        """
        # Get parameters
        transaction_id = tool_parameters.get("transaction_id", "")
        if not transaction_id:
            raise ValueError("Transaction ID is required.")

        note = tool_parameters.get("note")
        category_id = tool_parameters.get("category_id")

        # Check if there's anything to update
        if note is None and category_id is None:
            raise ValueError("At least one field (note or category_id) must be provided to update.")

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

        # Build update payload
        update_data: dict[str, Any] = {}
        if note is not None:
            update_data["note"] = note
        if category_id is not None:
            update_data["categoryId"] = category_id

        try:
            # Use PATCH to update transaction
            response = httpx.patch(
                f"{api_base_url}/transaction/{transaction_id}",
                headers=headers,
                json=update_data,
                timeout=15
            )

            if response.status_code == 200:
                txn = response.json()

                result = {
                    "success": True,
                    "id": txn.get("id", transaction_id),
                    "note": txn.get("note", ""),
                    "status": txn.get("status", ""),
                    "message": f"Successfully updated transaction '{transaction_id}'"
                }

                yield self.create_json_message(result)

            elif response.status_code == 404:
                raise ValueError(f"Transaction with ID '{transaction_id}' not found.")
            elif response.status_code == 400:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", "Invalid request")
                raise Exception(f"Failed to update transaction: {error_msg}")
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your Mercury API access token."
                )
            elif response.status_code == 403:
                raise Exception(
                    "Permission denied. Your API token may not have permission to update transactions."
                )
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to update transaction: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while updating transaction: {str(e)}") from e
