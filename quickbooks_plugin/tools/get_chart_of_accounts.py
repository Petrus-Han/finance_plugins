import urllib.parse
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GetChartOfAccountsTool(Tool):
    """Tool to retrieve chart of accounts from QuickBooks Online."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_chart_of_accounts tool to fetch QuickBooks accounts.

        Args:
            tool_parameters: Dictionary containing query parameters

        Returns:
            List of accounts with their details
        """
        # Get optional parameters
        account_type = tool_parameters.get("account_type")

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        realm_id = self.runtime.credentials.get("realm_id")

        if not access_token or not realm_id:
            raise ToolProviderCredentialValidationError("QuickBooks API Access Token and Realm ID are required.")

        # Get API base URL
        environment = self.runtime.credentials.get("environment", "sandbox")
        if environment == "sandbox":
            api_base_url = "https://sandbox-quickbooks.api.intuit.com/v3"
        else:
            api_base_url = "https://quickbooks.api.intuit.com/v3"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

        # Build query
        query = "select * from Account"
        if account_type:
            query += f" where AccountType = '{account_type}'"

        encoded_query = urllib.parse.quote(query)
        url = f"{api_base_url}/company/{realm_id}/query?query={encoded_query}&minorversion=65"

        try:
            # Make API request
            response = httpx.get(
                url,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                accounts = data.get("QueryResponse", {}).get("Account", [])

                if not accounts:
                    yield self.create_json_message({
                        "accounts": [],
                        "count": 0,
                        "message": "No accounts found."
                    })
                    return

                # Format accounts for output
                output = []
                for acc in accounts:
                    account_info = {
                        "id": acc.get("Id"),
                        "name": acc.get("Name"),
                        "type": acc.get("AccountType"),
                        "sub_type": acc.get("AccountSubType"),
                        "active": acc.get("Active"),
                        "current_balance": acc.get("CurrentBalance", 0),
                        "classification": acc.get("Classification"),
                        "fully_qualified_name": acc.get("FullyQualifiedName")
                    }
                    output.append(account_info)

                yield self.create_json_message({
                    "accounts": output,
                    "count": len(output)
                })

            elif response.status_code == 400:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
                raise ValueError(f"Invalid request: {error_msg}")

            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your QuickBooks API access token."
                )

            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
                raise Exception(
                    f"Failed to retrieve accounts: {response.status_code} - {error_msg}"
                )

        except httpx.HTTPError as e:
            raise Exception(f"Network error while fetching accounts: {str(e)}") from e
