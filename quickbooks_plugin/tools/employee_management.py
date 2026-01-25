import urllib.parse
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class EmployeeManagementTool(Tool):
    """Tool to manage employees in QuickBooks."""

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
        given_name = params.get("given_name")
        family_name = params.get("family_name")

        if not given_name and not family_name:
            raise ValueError("At least one of given_name or family_name is required for create")

        payload: dict[str, Any] = {}

        if given_name:
            payload["GivenName"] = given_name
        if family_name:
            payload["FamilyName"] = family_name
        if params.get("display_name"):
            payload["DisplayName"] = params["display_name"]
        if params.get("email"):
            payload["PrimaryEmailAddr"] = {"Address": params["email"]}
        if params.get("phone"):
            payload["PrimaryPhone"] = {"FreeFormNumber": params["phone"]}
        if params.get("mobile"):
            payload["Mobile"] = {"FreeFormNumber": params["mobile"]}

        # Address
        if params.get("address_line1"):
            payload["PrimaryAddr"] = {
                "Line1": params["address_line1"],
                "City": params.get("city", ""),
                "CountrySubDivisionCode": params.get("state", ""),
                "PostalCode": params.get("postal_code", "")
            }

        url = f"{api_base_url}/company/{realm_id}/employee?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            result = {
                "success": True,
                "operation": "create",
                "employee": self._format(data.get("Employee", {})),
                "message": "Employee created successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _read(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        employee_id = params.get("employee_id")
        if not employee_id:
            raise ValueError("employee_id is required for read")

        url = f"{api_base_url}/company/{realm_id}/employee/{employee_id}?minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            result = {
                "success": True,
                "operation": "read",
                "employee": self._format(data.get("Employee", {})),
                "message": "Employee retrieved successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _update(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        employee_id = params.get("employee_id")
        sync_token = params.get("sync_token")

        if not employee_id or not sync_token:
            raise ValueError("employee_id and sync_token are required for update")

        # First read the existing employee
        read_url = f"{api_base_url}/company/{realm_id}/employee/{employee_id}?minorversion=65"
        read_response = httpx.get(read_url, headers=headers, timeout=30)

        if read_response.status_code != 200:
            self._handle_error(read_response)

        payload = read_response.json().get("Employee", {})
        payload["SyncToken"] = sync_token

        # Update fields
        if params.get("given_name"):
            payload["GivenName"] = params["given_name"]
        if params.get("family_name"):
            payload["FamilyName"] = params["family_name"]
        if params.get("display_name"):
            payload["DisplayName"] = params["display_name"]
        if params.get("email"):
            payload["PrimaryEmailAddr"] = {"Address": params["email"]}
        if params.get("phone"):
            payload["PrimaryPhone"] = {"FreeFormNumber": params["phone"]}
        if params.get("active") is not None:
            payload["Active"] = params["active"]

        url = f"{api_base_url}/company/{realm_id}/employee?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            result = {
                "success": True,
                "operation": "update",
                "employee": self._format(data.get("Employee", {})),
                "message": "Employee updated successfully"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _query(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        query_string = params.get("query_string", "")
        query = "SELECT * FROM Employee"
        if query_string:
            query += f" WHERE {query_string}"

        encoded_query = urllib.parse.quote(query)
        url = f"{api_base_url}/company/{realm_id}/query?query={encoded_query}&minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            items = data.get("QueryResponse", {}).get("Employee", [])
            result = {
                "success": True,
                "operation": "query",
                "employees": [self._format(item) for item in items],
                "count": len(items),
                "message": f"Found {len(items)} employees"
            }
            for key, value in result.items():
                yield self.create_variable_message(key, value)
            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _format(self, item: dict) -> dict:
        return {
            "id": item.get("Id"),
            "sync_token": item.get("SyncToken"),
            "display_name": item.get("DisplayName"),
            "given_name": item.get("GivenName"),
            "family_name": item.get("FamilyName"),
            "email": item.get("PrimaryEmailAddr", {}).get("Address") if item.get("PrimaryEmailAddr") else None,
            "phone": item.get("PrimaryPhone", {}).get("FreeFormNumber") if item.get("PrimaryPhone") else None,
            "mobile": item.get("Mobile", {}).get("FreeFormNumber") if item.get("Mobile") else None,
            "active": item.get("Active"),
            "billable_time": item.get("BillableTime"),
        }

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed.")
        error_detail = response.json() if response.content else {}
        error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
