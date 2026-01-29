import logging
import os
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin.config.logger_format import plugin_logger_handler

logger = logging.getLogger(__name__)
logger.addHandler(plugin_logger_handler)

# Only enable debug logging when explicitly requested via environment variable
if os.environ.get("MERCURY_PLUGIN_DEBUG", "").lower() in ("true", "1", "yes"):
    logger.setLevel(logging.DEBUG)


class GetTransactionsTool(Tool):
    """Tool to retrieve transactions for Mercury bank accounts."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_transactions tool to fetch transactions.

        Args:
            tool_parameters: Dictionary containing:
                - account_id: The Mercury account ID (optional - fetches all if not provided)
                - start_date: Start date for filtering (ISO 8601, optional)
                - end_date: End date for filtering (ISO 8601, optional)
                - limit: Max number of results per account (optional, default 100)
                - offset: Pagination offset (optional, default 0)

        Returns:
            List of transactions with details
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

        # Get parameters
        account_id = tool_parameters.get("account_id")
        start_date = tool_parameters.get("start_date")
        end_date = tool_parameters.get("end_date")
        limit = tool_parameters.get("limit", 100)
        offset = tool_parameters.get("offset", 0)

        try:
            if account_id:
                # Fetch transactions for specific account
                account_ids = [account_id]
            else:
                # Fetch all accounts first
                account_ids = self._get_all_account_ids(api_base_url, headers)
                if not account_ids:
                    yield self.create_text_message("No accounts found.")
                    return

            # Fetch transactions for each account
            all_transactions = []
            for acc_id in account_ids:
                transactions = self._get_transactions_for_account(
                    api_base_url, headers, acc_id,
                    start_date, end_date, limit, offset
                )
                all_transactions.extend(transactions)

            if not all_transactions:
                yield self.create_text_message("No transactions found for the specified criteria.")
                return

            # Yield as variables for direct access
            yield self.create_variable_message("transactions", all_transactions)
            yield self.create_variable_message("total_count", len(all_transactions))
            yield self.create_variable_message("limit", limit)
            yield self.create_variable_message("offset", offset)

            # Also yield the full JSON for convenience
            yield self.create_json_message({
                "transactions": all_transactions,
                "total_count": len(all_transactions),
                "limit": limit,
                "offset": offset
            })

        except httpx.HTTPError as e:
            raise Exception(f"Network error while fetching transactions: {str(e)}") from e

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

    def _get_transactions_for_account(
        self, api_base_url: str, headers: dict, account_id: str,
        start_date: str = None, end_date: str = None,
        limit: int = 100, offset: int = 0
    ) -> list[dict]:
        """Fetch transactions for a specific account."""
        url = f"{api_base_url}/account/{account_id}/transactions"

        # Build query parameters
        params = {
            "limit": limit,
            "offset": offset,
        }
        if start_date:
            params["postedAtStart"] = start_date
        if end_date:
            params["postedAtEnd"] = end_date

        response = httpx.get(url, headers=headers, params=params, timeout=15)

        if response.status_code == 200:
            data = response.json()
            transactions = data.get("transactions", [])

            # Format transactions for output
            output = []
            for txn in transactions:
                transaction_info = {
                    "account_id": account_id,
                    "id": txn.get("id", ""),
                    "amount": txn.get("amount", 0),
                    "posted_at": txn.get("postedAt", ""),
                    "status": txn.get("status", ""),
                    "counterparty_name": txn.get("counterpartyName", ""),
                    "bank_description": txn.get("bankDescription", ""),
                    "note": txn.get("note", ""),
                    "category": txn.get("category", ""),
                    "type": txn.get("type", ""),
                }
                output.append(transaction_info)

            return output

        elif response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed. Check your API token.")
        elif response.status_code == 404:
            return []
        else:
            return []
