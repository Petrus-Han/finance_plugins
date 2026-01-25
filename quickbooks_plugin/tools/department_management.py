import urllib.parse
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class DepartmentManagementTool(Tool):
    """Tool to manage departments in QuickBooks for tracking physical locations."""

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
            if operation == "create":
                yield from self._create(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "read":
                yield from self._read(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "update":
                yield from self._update(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "query":
                yield from self._query(api_base_url, realm_id, headers, tool_parameters)
            else:
                raise ValueError(f"Unknown operation: {operation}")
        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _create(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        name = params.get("name")
        if not name:
            raise ValueError("name is required for create")

        payload: dict[str, Any] = {"Name": name}

        if params.get("parent_id"):
            payload["ParentRef"] = {"value": params["parent_id"]}

        url = f"{api_base_url}/company/{realm_id}/department?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            yield self.create_json_message({
                "success": True,
                "operation": "create",
                "department": self._format(data.get("Department", {})),
                "message": "Department created successfully"
            })
        else:
            self._handle_error(response)

    def _read(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        department_id = params.get("department_id")
        if not department_id:
            raise ValueError("department_id is required for read")

        url = f"{api_base_url}/company/{realm_id}/department/{department_id}?minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            yield self.create_json_message({
                "success": True,
                "operation": "read",
                "department": self._format(data.get("Department", {})),
                "message": "Department retrieved successfully"
            })
        else:
            self._handle_error(response)

    def _update(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        department_id = params.get("department_id")
        sync_token = params.get("sync_token")

        if not department_id or not sync_token:
            raise ValueError("department_id and sync_token are required for update")

        # First read the existing department
        read_url = f"{api_base_url}/company/{realm_id}/department/{department_id}?minorversion=65"
        read_response = httpx.get(read_url, headers=headers, timeout=30)

        if read_response.status_code != 200:
            self._handle_error(read_response)

        payload = read_response.json().get("Department", {})
        payload["SyncToken"] = sync_token

        if params.get("name"):
            payload["Name"] = params["name"]
        if params.get("active") is not None:
            payload["Active"] = params["active"]

        url = f"{api_base_url}/company/{realm_id}/department?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            yield self.create_json_message({
                "success": True,
                "operation": "update",
                "department": self._format(data.get("Department", {})),
                "message": "Department updated successfully"
            })
        else:
            self._handle_error(response)

    def _query(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        query_string = params.get("query_string", "")
        query = "SELECT * FROM Department"
        if query_string:
            query += f" WHERE {query_string}"

        encoded_query = urllib.parse.quote(query)
        url = f"{api_base_url}/company/{realm_id}/query?query={encoded_query}&minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            items = data.get("QueryResponse", {}).get("Department", [])
            yield self.create_json_message({
                "success": True,
                "operation": "query",
                "departments": [self._format(item) for item in items],
                "count": len(items),
                "message": f"Found {len(items)} departments"
            })
        else:
            self._handle_error(response)

    def _format(self, item: dict) -> dict:
        return {
            "id": item.get("Id"),
            "sync_token": item.get("SyncToken"),
            "name": item.get("Name"),
            "fully_qualified_name": item.get("FullyQualifiedName"),
            "active": item.get("Active"),
            "sub_department": item.get("SubDepartment"),
            "parent_id": item.get("ParentRef", {}).get("value") if item.get("ParentRef") else None,
        }

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed.")
        error_detail = response.json() if response.content else {}
        error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
