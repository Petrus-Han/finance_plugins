from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GetTransactionsTool(Tool):
    """Tool to retrieve transactions for a Mercury bank account."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_transactions tool to fetch transactions for a Mercury account.

        Args:
            tool_parameters: Dictionary containing:
                - account_id: The Mercury account ID (required)
                - start_date: Start date for filtering (ISO 8601, optional)
                - end_date: End date for filtering (ISO 8601, optional)
                - limit: Max number of results (optional, default 100)
                - offset: Pagination offset (optional, default 0)

        Returns:
            List of transactions with details
        """
        # Get parameters
        account_id = tool_parameters.get("account_id", "")
        if not account_id:
            raise ValueError("Account ID is required.")

        start_date = tool_parameters.get("start_date")
        end_date = tool_parameters.get("end_date")
        limit = tool_parameters.get("limit", 100)
        offset = tool_parameters.get("offset", 0)

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

        # Build query parameters
        params = {
            "limit": limit,
            "offset": offset,
        }

        if start_date:
            params["postedAtStart"] = start_date
        if end_date:
            params["postedAtEnd"] = end_date

        try:
            # Make API request
            response = httpx.get(
                f"{api_base_url}/account/{account_id}/transactions",
                headers=headers,
                params=params,
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                transactions = data.get("transactions", [])

                if not transactions:
                    yield self.create_text_message("No transactions found for the specified criteria.")
                    return

                # Format transactions for output
                output = []
                for txn in transactions:
                    transaction_info = {
                        "id": txn.get("id", ""),
                        "amount": txn.get("amount", 0),
                        "posted_at": txn.get("postedAt", ""),
                        "status": txn.get("status", ""),
                        "counterparty_name": txn.get("counterpartyName", ""),
                        "bank_description": txn.get("bankDescription", ""),
                        "note": txn.get("note", ""),
                        "category": txn.get("category", ""),
                        "type": txn.get("type", ""),
                        "account_id": txn.get("accountId", ""),
                    }
                    output.append(transaction_info)

                # Return JSON data with metadata
                total_count = data.get("total", len(transactions))
                yield self.create_json_message({
                    "transactions": output,
                    "count": len(transactions),
                    "total": total_count,
                    "offset": offset,
                    "limit": limit
                })

            elif response.status_code == 404:
                raise ValueError(f"Account with ID '{account_id}' not found.")
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your Mercury API access token."
                )
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to retrieve transactions: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while fetching transactions: {str(e)}") from e
