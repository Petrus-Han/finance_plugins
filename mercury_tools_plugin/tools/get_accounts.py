import logging
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin.config.logger_format import plugin_logger_handler

# Set up logging with Dify's plugin logger handler
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(plugin_logger_handler)


class GetAccountsTool(Tool):
    """Tool to retrieve all Mercury bank accounts."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_accounts tool to fetch all Mercury accounts.

        Returns:
            List of accounts with their details (id, name, type, balances, etc.)
        """
        logger.info("=== GetAccountsTool._invoke called ===")
        print("[GET_ACCOUNTS] Starting tool invocation", flush=True)

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        logger.info(f"Access token present: {bool(access_token)}")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        # Get API environment
        api_environment = self.runtime.credentials.get("api_environment", "production")
        logger.info(f"API environment: {api_environment}")
        print(f"[GET_ACCOUNTS] API environment: {api_environment}", flush=True)

        # Determine API base URL based on environment
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        logger.info(f"API base URL: {api_base_url}")
        print(f"[GET_ACCOUNTS] API base URL: {api_base_url}", flush=True)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
        }

        try:
            # Make API request
            logger.info(f"Making request to: {api_base_url}/accounts")
            print(f"[GET_ACCOUNTS] Making request to: {api_base_url}/accounts", flush=True)
            response = httpx.get(
                f"{api_base_url}/accounts",
                headers=headers,
                timeout=15
            )
            logger.info(f"Response status: {response.status_code}")
            print(f"[GET_ACCOUNTS] Response status: {response.status_code}", flush=True)

            if response.status_code == 200:
                accounts_data = response.json()
                logger.info(f"Response data keys: {accounts_data.keys() if isinstance(accounts_data, dict) else 'not a dict'}")
                print(f"[GET_ACCOUNTS] Response data: {accounts_data}", flush=True)

                # Format accounts for output
                accounts_list = accounts_data.get("accounts", [])
                logger.info(f"Found {len(accounts_list)} accounts")
                print(f"[GET_ACCOUNTS] Found {len(accounts_list)} accounts", flush=True)

                if not accounts_list:
                    logger.info("No accounts found, returning message")
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

                logger.info(f"Returning {len(output)} accounts")
                # Yield as variable for direct access
                yield self.create_variable_message("accounts", output)
                yield self.create_variable_message("count", len(output))

                # Also yield the full JSON for convenience
                yield self.create_json_message({"accounts": output, "count": len(output)})
                logger.info("Successfully yielded JSON message")

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
