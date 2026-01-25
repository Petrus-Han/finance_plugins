import json
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class UpdateJournalEntryTool(Tool):
    """Tool to update journal entries in QuickBooks."""

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

        je_id = tool_parameters.get("journal_entry_id")
        sync_token = tool_parameters.get("sync_token")
        lines_json = tool_parameters.get("lines_json")

        if not je_id:
            raise ValueError("journal_entry_id is required")
        if not sync_token:
            raise ValueError("sync_token is required. Get it from reading the journal entry first.")
        if not lines_json:
            raise ValueError("lines_json is required")

        try:
            lines_data = json.loads(lines_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid lines_json format: {e}")

        # Format lines for QuickBooks API
        formatted_lines = []
        for line in lines_data:
            formatted_line = {
                "DetailType": "JournalEntryLineDetail",
                "Amount": line.get("Amount"),
                "JournalEntryLineDetail": {
                    "PostingType": line.get("PostingType"),
                    "AccountRef": line.get("AccountRef")
                }
            }
            if line.get("Description"):
                formatted_line["Description"] = line["Description"]
            formatted_lines.append(formatted_line)

        payload: dict[str, Any] = {
            "Id": je_id,
            "SyncToken": sync_token,
            "Line": formatted_lines
        }

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
                raise Exception(f"Failed to update journal entry: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e
