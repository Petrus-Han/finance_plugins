import urllib.parse
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class AttachableManagementTool(Tool):
    """Tool to manage attachments and notes in QuickBooks."""

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

        operation = tool_parameters.get("operation")
        if not operation:
            raise ValueError("operation is required")

        try:
            if operation == "create_note":
                yield from self._create_note(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "read":
                yield from self._read(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "update":
                yield from self._update(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "delete":
                yield from self._delete(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "download":
                yield from self._download(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "query":
                yield from self._query(api_base_url, realm_id, headers, tool_parameters)
            else:
                raise ValueError(f"Unknown operation: {operation}")
        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _create_note(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        note = params.get("note")
        if not note:
            raise ValueError("note is required for create_note")

        payload: dict[str, Any] = {"Note": note}

        entity_type = params.get("entity_type")
        entity_id = params.get("entity_id")
        if entity_type and entity_id:
            payload["AttachableRef"] = [{
                "EntityRef": {"type": entity_type, "value": entity_id},
                "IncludeOnSend": params.get("include_on_send", False)
            }]

        url = f"{api_base_url}/company/{realm_id}/attachable?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            result = {
                "success": True,
                "operation": "create_note",
                "attachable": self._format(data.get("Attachable", {})),
                "message": "Note attachment created successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _read(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        attachable_id = params.get("attachable_id")
        if not attachable_id:
            raise ValueError("attachable_id is required for read")

        url = f"{api_base_url}/company/{realm_id}/attachable/{attachable_id}?minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            result = {
                "success": True,
                "operation": "read",
                "attachable": self._format(data.get("Attachable", {})),
                "message": "Attachable retrieved successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _update(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        attachable_id = params.get("attachable_id")
        sync_token = params.get("sync_token")

        if not attachable_id or not sync_token:
            raise ValueError("attachable_id and sync_token are required for update")

        payload: dict[str, Any] = {
            "Id": attachable_id,
            "SyncToken": sync_token
        }

        if params.get("note"):
            payload["Note"] = params["note"]

        entity_type = params.get("entity_type")
        entity_id = params.get("entity_id")
        if entity_type and entity_id:
            payload["AttachableRef"] = [{
                "EntityRef": {"type": entity_type, "value": entity_id},
                "IncludeOnSend": params.get("include_on_send", False)
            }]

        url = f"{api_base_url}/company/{realm_id}/attachable?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            result = {
                "success": True,
                "operation": "update",
                "attachable": self._format(data.get("Attachable", {})),
                "message": "Attachable updated successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _delete(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        attachable_id = params.get("attachable_id")
        sync_token = params.get("sync_token")

        if not attachable_id or not sync_token:
            raise ValueError("attachable_id and sync_token are required for delete")

        # Need to read first to get full payload
        read_url = f"{api_base_url}/company/{realm_id}/attachable/{attachable_id}?minorversion=65"
        read_response = httpx.get(read_url, headers=headers, timeout=30)

        if read_response.status_code != 200:
            self._handle_error(read_response)

        payload = read_response.json().get("Attachable", {})
        payload["SyncToken"] = sync_token

        url = f"{api_base_url}/company/{realm_id}/attachable?operation=delete&minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            result = {
                "success": True,
                "operation": "delete",
                "message": f"Attachable {attachable_id} deleted successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _download(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        attachable_id = params.get("attachable_id")
        if not attachable_id:
            raise ValueError("attachable_id is required for download")

        # Use text/plain for download endpoint
        download_headers = {**headers, "Accept": "text/plain"}
        url = f"{api_base_url}/company/{realm_id}/download/{attachable_id}?minorversion=65"
        response = httpx.get(url, headers=download_headers, timeout=30)

        if response.status_code == 200:
            download_url = response.text.strip().strip('"')
            result = {
                "success": True,
                "operation": "download",
                "download_url": download_url,
                "message": "Download URL retrieved (expires in 15 minutes)"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _query(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        query_string = params.get("query_string", "")
        query = "SELECT * FROM Attachable"
        if query_string:
            query += f" WHERE {query_string}"

        encoded_query = urllib.parse.quote(query)
        url = f"{api_base_url}/company/{realm_id}/query?query={encoded_query}&minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            items = data.get("QueryResponse", {}).get("Attachable", [])
            result = {
                "success": True,
                "operation": "query",
                "attachables": [self._format(item) for item in items],
                "count": len(items),
                "message": f"Found {len(items)} attachables"
            }
            # Only create variable messages for scalar values
            yield self.create_variable_message("success", True)
            yield self.create_variable_message("operation", "query")
            yield self.create_variable_message("count", len(items))
            yield self.create_variable_message("message", f"Found {len(items)} attachables")
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _format(self, item: dict) -> dict:
        refs = item.get("AttachableRef", [])
        return {
            "id": item.get("Id"),
            "sync_token": item.get("SyncToken"),
            "file_name": item.get("FileName"),
            "note": item.get("Note"),
            "content_type": item.get("ContentType"),
            "size": item.get("Size"),
            "category": item.get("Category"),
            "temp_download_uri": item.get("TempDownloadUri"),
            "attachable_refs": [
                {
                    "entity_type": ref.get("EntityRef", {}).get("type"),
                    "entity_id": ref.get("EntityRef", {}).get("value"),
                    "include_on_send": ref.get("IncludeOnSend")
                }
                for ref in refs
            ] if refs else [],
        }

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed.")
        error_detail = response.json() if response.content else {}
        error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
