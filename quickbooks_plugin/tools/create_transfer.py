from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class CreateTransferTool(Tool):
    """Tool to create a transfer between QuickBooks bank accounts."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the create_transfer tool to move money between accounts.

        Args:
            tool_parameters: Dictionary containing transfer parameters

        Returns:
            Transfer details including ID and transaction information
        """
        # Get required parameters
        from_account_id = tool_parameters.get("from_account_id")
        to_account_id = tool_parameters.get("to_account_id")
        amount = tool_parameters.get("amount")

        if not all([from_account_id, to_account_id, amount]):
            yield self.create_text_message("from_account_id, to_account_id, and amount are required parameters")
            return

        # Get optional parameters
        txn_date = tool_parameters.get("txn_date")
        note = tool_parameters.get("note", "")

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        realm_id = self.runtime.credentials.get("realm_id")

        if not access_token or not realm_id:
            yield self.create_text_message("QuickBooks API Access Token and Realm ID are required.")
            return

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
            "FromAccountRef": {
                "value": from_account_id
            },
            "ToAccountRef": {
                "value": to_account_id
            },
            "Amount": abs(float(amount))
        }

        if txn_date:
            payload["TxnDate"] = txn_date

        if note:
            payload["PrivateNote"] = note

        try:
            # Make API request
            response = httpx.post(
                f"{api_base_url}/company/{realm_id}/transfer?minorversion=65",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                transfer = data.get("Transfer", {})

                # Extract key information
                result = {
                    "id": transfer.get("Id"),
                    "txn_date": transfer.get("TxnDate"),
                    "amount": transfer.get("Amount"),
                    "from_account": {
                        "id": transfer.get("FromAccountRef", {}).get("value"),
                        "name": transfer.get("FromAccountRef", {}).get("name")
                    },
                    "to_account": {
                        "id": transfer.get("ToAccountRef", {}).get("value"),
                        "name": transfer.get("ToAccountRef", {}).get("name")
                    },
                    "private_note": transfer.get("PrivateNote", ""),
                    "sync_token": transfer.get("SyncToken"),
                    "meta_data": transfer.get("MetaData", {})
                }

                yield self.create_json_message(result)

            elif response.status_code == 400:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
                yield self.create_text_message(f"Invalid request: {error_msg}")

            elif response.status_code == 401:
                yield self.create_text_message(
                    "Authentication failed. Please check your QuickBooks API access token."
                )

            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
                yield self.create_text_message(
                    f"Failed to create transfer: {response.status_code} - {error_msg}"
                )

        except httpx.HTTPError as e:
            yield self.create_text_message(f"Network error while creating transfer: {str(e)}")
        except Exception as e:
            yield self.create_text_message(f"Unexpected error: {str(e)}")
