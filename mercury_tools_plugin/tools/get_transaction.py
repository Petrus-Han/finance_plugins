from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GetTransactionTool(Tool):
    """Tool to retrieve details for a specific Mercury transaction."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_transaction tool to fetch transaction details.

        Args:
            tool_parameters: Dictionary containing:
                - transaction_id: The transaction ID (required)

        Returns:
            Detailed transaction information
        """
        # Get parameters
        account_id = tool_parameters.get("account_id", "")
        transaction_id = tool_parameters.get("transaction_id", "")
        if not transaction_id:
            raise ValueError("Transaction ID is required.")

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
        }

        try:
            # Use different endpoint based on whether account_id is provided
            if account_id:
                url = f"{api_base_url}/account/{account_id}/transaction/{transaction_id}"
            else:
                url = f"{api_base_url}/transaction/{transaction_id}"

            response = httpx.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                txn = response.json()

                # Build comprehensive output
                transaction_info = {
                    "id": txn.get("id", ""),
                    "account_id": txn.get("accountId", ""),
                    "amount": txn.get("amount", 0),
                    "status": txn.get("status", ""),
                    "counterparty_name": txn.get("counterpartyName", ""),
                    "counterparty_id": txn.get("counterpartyId", ""),
                    "note": txn.get("note", ""),
                    "external_memo": txn.get("externalMemo", ""),
                    "posted_at": txn.get("postedAt", ""),
                    "created_at": txn.get("createdAt", ""),
                    "kind": txn.get("kind", ""),
                    "tracking_number": txn.get("trackingNumber", ""),
                }

                # Include details (routing info, etc.)
                details = txn.get("details", {})
                if details:
                    routing_info = details.get("electronicRoutingInfo", {})
                    if routing_info:
                        transaction_info["routing_details"] = {
                            "account_number": routing_info.get("accountNumber", ""),
                            "routing_number": routing_info.get("routingNumber", ""),
                            "bank_name": routing_info.get("bankName", ""),
                        }

                # Include attachments
                attachments = txn.get("attachments", [])
                if attachments:
                    transaction_info["attachments"] = [
                        {
                            "id": att.get("id", ""),
                            "file_name": att.get("fileName", ""),
                        }
                        for att in attachments
                    ]

                # Yield each field as a separate variable for direct access
                for key, value in transaction_info.items():
                    yield self.create_variable_message(key, value)

                # Also yield the full JSON for convenience
                yield self.create_json_message(transaction_info)

            elif response.status_code == 404:
                raise ValueError(f"Transaction with ID '{transaction_id}' not found.")
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your Mercury API access token."
                )
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to retrieve transaction: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while fetching transaction: {str(e)}") from e
