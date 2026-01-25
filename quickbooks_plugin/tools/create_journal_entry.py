from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class CreateJournalEntryTool(Tool):
    """Tool to create journal entries in QuickBooks."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        access_token = self.runtime.credentials.get("access_token")
        realm_id = self.runtime.credentials.get("realm_id")

        if not access_token or not realm_id:
            raise ToolProviderCredentialValidationError("QuickBooks credentials required.")

        environment = self.runtime.credentials.get("environment", "sandbox")
        api_base_url = f"https://{'sandbox-' if environment == 'sandbox' else ''}quickbooks.api.intuit.com/v3"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # Build lines from individual parameters
        lines = []
        for i in range(1, 5):  # Support up to 4 lines
            line_type = tool_parameters.get(f"line{i}_type")
            account_id = tool_parameters.get(f"line{i}_account_id")
            amount = tool_parameters.get(f"line{i}_amount")
            description = tool_parameters.get(f"line{i}_description")

            # Skip if essential fields are missing
            if not line_type or not account_id or amount is None:
                continue

            line = {
                "DetailType": "JournalEntryLineDetail",
                "Amount": float(amount),
                "JournalEntryLineDetail": {
                    "PostingType": line_type,
                    "AccountRef": {"value": str(account_id)}
                }
            }
            if description:
                line["Description"] = description
            lines.append(line)

        if len(lines) < 2:
            raise ValueError("At least 2 lines are required for a journal entry (one debit, one credit).")

        # Validate debit = credit
        total_debit = sum(l["Amount"] for l in lines if l["JournalEntryLineDetail"]["PostingType"] == "Debit")
        total_credit = sum(l["Amount"] for l in lines if l["JournalEntryLineDetail"]["PostingType"] == "Credit")

        if abs(total_debit - total_credit) > 0.01:  # Allow small rounding difference
            raise ValueError(f"Total debits ({total_debit}) must equal total credits ({total_credit}).")

        payload: dict[str, Any] = {"Line": lines}

        if tool_parameters.get("txn_date"):
            payload["TxnDate"] = tool_parameters["txn_date"]
        if tool_parameters.get("doc_number"):
            payload["DocNumber"] = tool_parameters["doc_number"]
        if tool_parameters.get("private_note"):
            payload["PrivateNote"] = tool_parameters["private_note"]

        try:
            url = f"{api_base_url}/company/{realm_id}/journalentry?minorversion=65"
            response = httpx.post(url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                data = response.json()
                je = data.get("JournalEntry", {})
                result = {
                    "id": je.get("Id"),
                    "sync_token": je.get("SyncToken"),
                    "doc_number": je.get("DocNumber"),
                    "txn_date": je.get("TxnDate"),
                    "private_note": je.get("PrivateNote"),
                    "total_amount": je.get("TotalAmt"),
                    "lines": je.get("Line", []),
                }
                for key, value in result.items():
                    yield self.create_variable_message(key, value)
                yield self.create_json_message(result)
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError("Authentication failed. Please check your QuickBooks credentials.")
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
                raise Exception(f"Failed to create journal entry: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e
