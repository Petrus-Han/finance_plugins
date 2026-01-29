import logging
import os
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin.config.logger_format import plugin_logger_handler

# Set up logging with Dify's plugin logger handler
logger = logging.getLogger(__name__)
logger.addHandler(plugin_logger_handler)

# Only enable debug logging when explicitly requested via environment variable
if os.environ.get("MERCURY_PLUGIN_DEBUG", "").lower() in ("true", "1", "yes"):
    logger.setLevel(logging.DEBUG)


class GetAccountsTool(Tool):
    """Tool to retrieve all Mercury bank accounts."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_accounts tool to fetch all Mercury accounts.

        Returns:
            List of accounts with their details (id, name, type, balances, etc.)
        """
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
            # Make API request
            response = httpx.get(
                f"{api_base_url}/accounts",
                headers=headers,
                timeout=15
            )

            if response.status_code == 200:
                accounts_data = response.json()

                # Format accounts for output
                accounts_list = accounts_data.get("accounts", [])

                if not accounts_list:
                    yield self.create_text_message("No accounts found.")
                    return

                # Create structured output
                output = []
                for account in accounts_list:
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
                    }
                    output.append(account_info)

                # Yield as variable for direct access
                yield self.create_variable_message("accounts", output)
                yield self.create_variable_message("count", len(output))

                # Also yield the full JSON for convenience
                yield self.create_json_message({"accounts": output, "count": len(output)})

            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    f"Authentication failed. Please check your Mercury API access token and ensure it's for the '{api_environment}' environment."
                )
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to retrieve accounts: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while fetching accounts: {str(e)}") from e
