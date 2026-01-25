from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class CreateDepositTool(Tool):
    """Tool to create a deposit in QuickBooks Online."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the create_deposit tool to create a deposit transaction.

        Args:
            tool_parameters: Dictionary containing deposit parameters

        Returns:
            Deposit details including ID and transaction information
        """
        # Get required parameters
        bank_account_id = tool_parameters.get("bank_account_id")
        amount = tool_parameters.get("amount")
        income_account_id = tool_parameters.get("income_account_id")

        if not all([bank_account_id, amount, income_account_id]):
            raise ValueError("bank_account_id, amount, and income_account_id are required parameters")

        # Get optional parameters
        txn_date = tool_parameters.get("txn_date")
        description = tool_parameters.get("description", "")
        note = tool_parameters.get("note", "")

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
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Build request payload
        payload = {
            "DepositToAccountRef": {
                "value": bank_account_id
            },
            "Line": [
                {
                    "Amount": amount,
                    "DetailType": "DepositLineDetail",
                    "Description": description,
                    "DepositLineDetail": {
                        "AccountRef": {
                            "value": income_account_id
                        }
                    }
                }
            ]
        }

        if txn_date:
            payload["TxnDate"] = txn_date

        if note:
            payload["PrivateNote"] = note

        try:
            # Make API request
            response = httpx.post(
                f"{api_base_url}/company/{realm_id}/deposit?minorversion=65",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                deposit = data.get("Deposit", {})

                # Extract key information
                result = {
                    "id": deposit.get("Id"),
                    "txn_date": deposit.get("TxnDate"),
                    "total_amount": deposit.get("TotalAmt"),
                    "deposit_to_account": deposit.get("DepositToAccountRef", {}).get("name"),
                    "private_note": deposit.get("PrivateNote", ""),
                    "sync_token": deposit.get("SyncToken"),
                    "meta_data": deposit.get("MetaData", {})
                }

                for key, value in result.items():
                    yield self.create_variable_message(key, value)
                yield self.create_json_message(result)

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
                    f"Failed to create deposit: {response.status_code} - {error_msg}"
                )

        except httpx.HTTPError as e:
            raise Exception(f"Network error while creating deposit: {str(e)}") from e
