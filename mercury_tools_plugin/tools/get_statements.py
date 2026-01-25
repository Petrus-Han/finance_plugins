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
    """Tool to retrieve monthly statements for Mercury bank accounts."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_statements tool to fetch statements.

        Args:
            tool_parameters: Optional 'account_id'. If not provided, fetches statements for all accounts.

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

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
        }

        # Get optional account_id parameter
        account_id = tool_parameters.get("account_id")

        try:
            if account_id:
                # Fetch statements for specific account
                account_ids = [account_id]
            else:
                # Fetch all accounts first
                logger.info("No account_id provided, fetching all accounts...")
                account_ids = self._get_all_account_ids(api_base_url, headers)
                if not account_ids:
                    yield self.create_text_message("No accounts found.")
                    return

            # Fetch statements for each account
            all_statements = []
            for acc_id in account_ids:
                statements = self._get_statements_for_account(api_base_url, headers, acc_id)
                all_statements.extend(statements)

            logger.info(f"Found {len(all_statements)} statements total")

            if not all_statements:
                yield self.create_text_message("No statements found.")
                return

            # Yield as variables for direct access
            yield self.create_variable_message("statements", all_statements)
            yield self.create_variable_message("total_count", len(all_statements))

            # Also yield the full JSON for convenience
            yield self.create_json_message({
                "statements": all_statements,
                "total_count": len(all_statements)
            })

        except httpx.HTTPError as e:
            raise Exception(f"Network error while fetching statements: {str(e)}") from e

    def _get_all_account_ids(self, api_base_url: str, headers: dict) -> list[str]:
        """Fetch all account IDs."""
        response = httpx.get(f"{api_base_url}/accounts", headers=headers, timeout=15)

        if response.status_code == 200:
            data = response.json()
            accounts = data.get("accounts", [])
            return [acc.get("id") for acc in accounts if acc.get("id")]
        elif response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed. Check your API token.")
        else:
            raise Exception(f"Failed to fetch accounts: {response.status_code}")

    def _get_statements_for_account(self, api_base_url: str, headers: dict, account_id: str) -> list[dict]:
        """Fetch statements for a specific account."""
        url = f"{api_base_url}/account/{account_id}/statements"
        logger.info(f"Fetching statements from: {url}")

        response = httpx.get(url, headers=headers, timeout=15)

        if response.status_code == 200:
            data = response.json()
            statements_list = data.get("statements", [])

            # Format statements for output
            output = []
            for stmt in statements_list:
                transactions = stmt.get("transactions", [])
                statement_info = {
                    "account_id": account_id,
                    "id": stmt.get("id", ""),
                    "start_date": stmt.get("startDate", ""),
                    "end_date": stmt.get("endDate", ""),
                    "ending_balance": stmt.get("endingBalance", 0),
                    "company_legal_name": stmt.get("companyLegalName", ""),
                    "download_url": stmt.get("downloadUrl", ""),
                    "transaction_count": len(transactions) if isinstance(transactions, list) else 0,
                }
                output.append(statement_info)

            return output

        elif response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed. Check your API token.")
        elif response.status_code == 404:
            logger.warning(f"Account not found: {account_id}")
            return []
        else:
            logger.warning(f"Failed to fetch statements for account {account_id}: {response.status_code}")
            return []
