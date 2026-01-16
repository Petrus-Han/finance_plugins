from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class CreatePurchaseTool(Tool):
    """Tool to create a purchase (expense) in QuickBooks Online."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the create_purchase tool to create a purchase/expense transaction.

        Args:
            tool_parameters: Dictionary containing purchase parameters

        Returns:
            Purchase details including ID and transaction information
        """
        # Get required parameters
        bank_account_id = tool_parameters.get("bank_account_id")
        amount = tool_parameters.get("amount")
        expense_account_id = tool_parameters.get("expense_account_id")

        if not all([bank_account_id, amount, expense_account_id]):
            yield self.create_text_message("bank_account_id, amount, and expense_account_id are required parameters")
            return

        # Get optional parameters
        payment_type = tool_parameters.get("payment_type", "CreditCard")
        txn_date = tool_parameters.get("txn_date")
        description = tool_parameters.get("description", "")
        note = tool_parameters.get("note", "")
        vendor_id = tool_parameters.get("vendor_id")

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
            "AccountRef": {
                "value": bank_account_id
            },
            "PaymentType": payment_type,
            "Line": [
                {
                    "Amount": abs(float(amount)),
                    "DetailType": "AccountBasedExpenseLineDetail",
                    "Description": description,
                    "AccountBasedExpenseLineDetail": {
                        "AccountRef": {
                            "value": expense_account_id
                        }
                    }
                }
            ]
        }

        if txn_date:
            payload["TxnDate"] = txn_date

        if note:
            payload["PrivateNote"] = note

        if vendor_id:
            payload["EntityRef"] = {
                "value": vendor_id,
                "type": "Vendor"
            }

        try:
            # Make API request
            response = httpx.post(
                f"{api_base_url}/company/{realm_id}/purchase?minorversion=65",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                purchase = data.get("Purchase", {})

                # Extract key information
                result = {
                    "id": purchase.get("Id"),
                    "txn_date": purchase.get("TxnDate"),
                    "total_amount": purchase.get("TotalAmt"),
                    "payment_type": purchase.get("PaymentType"),
                    "account": purchase.get("AccountRef", {}).get("name"),
                    "private_note": purchase.get("PrivateNote", ""),
                    "sync_token": purchase.get("SyncToken"),
                    "meta_data": purchase.get("MetaData", {})
                }

                # Add entity/vendor info if available
                if "EntityRef" in purchase:
                    result["entity"] = {
                        "name": purchase["EntityRef"].get("name"),
                        "type": purchase["EntityRef"].get("type")
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
                    f"Failed to create purchase: {response.status_code} - {error_msg}"
                )

        except httpx.HTTPError as e:
            yield self.create_text_message(f"Network error while creating purchase: {str(e)}")
        except Exception as e:
            yield self.create_text_message(f"Unexpected error: {str(e)}")
