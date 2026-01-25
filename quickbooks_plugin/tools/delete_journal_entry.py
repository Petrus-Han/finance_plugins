from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class DeleteJournalEntryTool(Tool):
    """Tool to delete journal entries in QuickBooks."""

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

        if not je_id:
            raise ValueError("journal_entry_id is required")
        if not sync_token:
            raise ValueError("sync_token is required. Get it from reading the journal entry first.")

        try:
            payload = {"Id": je_id, "SyncToken": sync_token}
            url = f"{api_base_url}/company/{realm_id}/journalentry?operation=delete&minorversion=65"
            response = httpx.post(url, headers=headers, json=payload, timeout=30)

            if response.status_code == 200:
                result = {
                    "success": True,
                    "deleted_id": je_id,
                    "message": f"Journal entry {je_id} deleted successfully"
                }
                for key, value in result.items():
                    yield self.create_variable_message(key, value)
                yield self.create_json_message(result)
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError("Authentication failed. Please check your QuickBooks credentials.")
            elif response.status_code == 404:
                raise ValueError(f"Journal entry with ID '{je_id}' not found.")
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
                raise Exception(f"Failed to delete journal entry: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e
