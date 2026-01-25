from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GetAccountTool(Tool):
    """Tool to retrieve details for a specific Mercury bank account."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_account tool to fetch a specific Mercury account.

        Args:
            tool_parameters: Dictionary containing:
                - account_id: The Mercury account ID to retrieve

        Returns:
            Account details including id, name, type, balances, etc.
        """
        # Get parameters
        account_id = tool_parameters.get("account_id", "")
        if not account_id:
            raise ValueError("Account ID is required.")

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        # Prepare request
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
            # Make API request
            response = httpx.get(
                f"{api_base_url}/account/{account_id}",
                headers=headers,
                timeout=15
            )

            if response.status_code == 200:
                account = response.json()

                # Create structured output
                account_info = {
                    "id": account.get("id", ""),
                    "name": account.get("name", ""),
                    "type": account.get("type", ""),
                    "status": account.get("status", ""),
                    "current_balance": account.get("currentBalance", 0),
                    "available_balance": account.get("availableBalance", 0),
                    "currency": account.get("currency", "USD"),
                    "routing_number": account.get("routingNumber", ""),
                    "account_number": account.get("accountNumber", ""),
                    "created_at": account.get("createdAt", ""),
                    "legal_business_name": account.get("legalBusinessName", ""),
                }

                # Yield each field as a separate variable for direct access
                for key, value in account_info.items():
                    yield self.create_variable_message(key, value)

                # Also yield the full JSON for convenience
                yield self.create_json_message(account_info)

            elif response.status_code == 404:
                raise ValueError(f"Account with ID '{account_id}' not found.")
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your Mercury API access token."
                )
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to retrieve account: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while fetching account: {str(e)}") from e
