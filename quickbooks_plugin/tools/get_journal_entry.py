import urllib.parse
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GetJournalEntryTool(Tool):
    """Tool to retrieve journal entries from QuickBooks."""

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

        journal_entry_id = tool_parameters.get("journal_entry_id")
        query_string = tool_parameters.get("query_string")

        try:
            if journal_entry_id:
                # Get single journal entry by ID
                yield from self._get_by_id(api_base_url, realm_id, headers, journal_entry_id)
            else:
                # Query journal entries
                yield from self._query(api_base_url, realm_id, headers, query_string)

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _get_by_id(self, api_base_url: str, realm_id: str, headers: dict, je_id: str) -> Generator[ToolInvokeMessage, None, None]:
        url = f"{api_base_url}/company/{realm_id}/journalentry/{je_id}?minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            je = data.get("JournalEntry", {})
            yield self.create_json_message({
                "journal_entry": self._format(je),
                "count": 1
            })
        elif response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed.")
        elif response.status_code == 404:
            raise ValueError(f"Journal entry with ID '{je_id}' not found.")
        else:
            error_detail = response.json() if response.content else {}
            error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
            raise Exception(f"Failed to get journal entry: {response.status_code} - {error_msg}")

    def _query(self, api_base_url: str, realm_id: str, headers: dict, query_string: str | None) -> Generator[ToolInvokeMessage, None, None]:
        query = "SELECT * FROM JournalEntry"
        if query_string:
            query += f" WHERE {query_string}"

        encoded_query = urllib.parse.quote(query)
        url = f"{api_base_url}/company/{realm_id}/query?query={encoded_query}&minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            items = data.get("QueryResponse", {}).get("JournalEntry", [])
            yield self.create_json_message({
                "journal_entries": [self._format(item) for item in items],
                "count": len(items)
            })
        elif response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed.")
        else:
            error_detail = response.json() if response.content else {}
            error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
            raise Exception(f"Failed to query journal entries: {response.status_code} - {error_msg}")

    def _format(self, item: dict) -> dict:
        return {
            "id": item.get("Id"),
            "sync_token": item.get("SyncToken"),
            "doc_number": item.get("DocNumber"),
            "txn_date": item.get("TxnDate"),
            "private_note": item.get("PrivateNote"),
            "adjustment": item.get("Adjustment"),
            "lines": item.get("Line", []),
            "total_amount": item.get("TotalAmt"),
        }
