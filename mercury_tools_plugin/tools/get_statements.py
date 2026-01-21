import logging
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin.config.logger_format import plugin_logger_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(plugin_logger_handler)


class GetStatementsTool(Tool):
    """Tool to retrieve monthly statements for a Mercury bank account."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_statements tool to fetch all statements for a Mercury account.

        Args:
            tool_parameters: Must include 'account_id'

        Returns:
            List of statements with their details (id, period, balance, etc.)
        """
        logger.info("=== GetStatementsTool._invoke called ===")

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        # Get API environment
        api_environment = self.runtime.credentials.get("api_environment", "production")
        logger.info(f"API environment: {api_environment}")

        # Determine API base URL based on environment
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        # Get required parameter
        account_id = tool_parameters.get("account_id")
        if not account_id:
            raise ValueError("account_id is required")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
        }

        try:
            url = f"{api_base_url}/account/{account_id}/statements"
            logger.info(f"Making request to: {url}")

            response = httpx.get(url, headers=headers, timeout=15)
            logger.info(f"Response status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                statements_list = data.get("statements", [])
                logger.info(f"Found {len(statements_list)} statements")

                if not statements_list:
                    yield self.create_text_message("No statements found for this account.")
                    return

                # Format statements for output
                output = []
                for stmt in statements_list:
                    transactions = stmt.get("transactions", [])
                    statement_info = {
                        "id": stmt.get("id", ""),
                        "start_date": stmt.get("startDate", ""),
                        "end_date": stmt.get("endDate", ""),
                        "ending_balance": stmt.get("endingBalance", 0),
                        "company_legal_name": stmt.get("companyLegalName", ""),
                        "download_url": stmt.get("downloadUrl", ""),
                        "transaction_count": len(transactions) if isinstance(transactions, list) else 0,
                    }
                    output.append(statement_info)

                yield self.create_json_message({"statements": output})

            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    f"Authentication failed. Please check your Mercury API access token and ensure it's for the '{api_environment}' environment."
                )
            elif response.status_code == 404:
                raise ValueError(f"Account not found: {account_id}")
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to retrieve statements: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while fetching statements: {str(e)}") from e
