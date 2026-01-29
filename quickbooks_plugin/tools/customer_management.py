from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class CustomerManagementTool(Tool):
    """Tool to manage customers in QuickBooks Online."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the customer_management tool to list, search, or create customers.

        Args:
            tool_parameters: Dictionary containing:
                - action: list, search, or create
                - display_name: Customer name (for create/search)
                - company_name: Company name (optional)
                - email: Email address (optional)
                - phone: Phone number (optional)

        Returns:
            Customer information based on the action
        """
        action = tool_parameters.get("action", "list")

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

        try:
            if action == "list":
                yield from self._list_customers(api_base_url, realm_id, headers)
            elif action == "search":
                display_name = tool_parameters.get("display_name", "")
                if not display_name:
                    raise ValueError("display_name is required for search")
                yield from self._search_customer(api_base_url, realm_id, headers, display_name)
            elif action == "create":
                display_name = tool_parameters.get("display_name", "")
                if not display_name:
                    raise ValueError("display_name is required for create")
                yield from self._create_customer(
                    api_base_url, realm_id, headers,
                    display_name,
                    tool_parameters.get("company_name"),
                    tool_parameters.get("email"),
                    tool_parameters.get("phone")
                )
            else:
                raise ValueError(f"Unknown action: {action}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _list_customers(self, api_base_url: str, realm_id: str, headers: dict) -> Generator[ToolInvokeMessage, None, None]:
        """List all active customers."""
        query = "SELECT * FROM Customer WHERE Active = true MAXRESULTS 100"

        response = httpx.get(
            f"{api_base_url}/company/{realm_id}/query",
            headers=headers,
            params={"query": query, "minorversion": "65"},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            customers = data.get("QueryResponse", {}).get("Customer", [])

            customers_list = []
            for cust in customers:
                customers_list.append({
                    "id": cust.get("Id"),
                    "display_name": cust.get("DisplayName"),
                    "company_name": cust.get("CompanyName", ""),
                    "email": cust.get("PrimaryEmailAddr", {}).get("Address", ""),
                    "phone": cust.get("PrimaryPhone", {}).get("FreeFormNumber", ""),
                    "balance": cust.get("Balance", 0),
                    "active": cust.get("Active", True)
                })

            result = {
                "customers": customers_list,
                "count": len(customers_list)
            }
            # Only create variable message for scalar values
            yield self.create_variable_message("count", len(customers_list))
            yield self.create_json_message(result)

        elif response.status_code == 401:
            raise ToolProviderCredentialValidationError(
                "Authentication failed. Please check your QuickBooks API access token."
            )

        else:
            error_detail = response.json() if response.content else {}
            error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
            raise Exception(f"Failed to list customers: {error_msg}")

    def _search_customer(self, api_base_url: str, realm_id: str, headers: dict, display_name: str) -> Generator[ToolInvokeMessage, None, None]:
        """Search for customer by name."""
        # Escape single quotes in the name
        safe_name = display_name.replace("'", "\\'")
        query = f"SELECT * FROM Customer WHERE DisplayName LIKE '%{safe_name}%'"

        response = httpx.get(
            f"{api_base_url}/company/{realm_id}/query",
            headers=headers,
            params={"query": query, "minorversion": "65"},
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            customers = data.get("QueryResponse", {}).get("Customer", [])

            if not customers:
                raise ValueError(f"No customers found matching '{display_name}'")

            customers_list = []
            for cust in customers:
                customers_list.append({
                    "id": cust.get("Id"),
                    "display_name": cust.get("DisplayName"),
                    "company_name": cust.get("CompanyName", ""),
                    "email": cust.get("PrimaryEmailAddr", {}).get("Address", ""),
                    "phone": cust.get("PrimaryPhone", {}).get("FreeFormNumber", ""),
                    "balance": cust.get("Balance", 0)
                })

            result = {
                "customers": customers_list,
                "count": len(customers_list)
            }
            # Only create variable message for scalar values
            yield self.create_variable_message("count", len(customers_list))
            yield self.create_json_message(result)

        elif response.status_code == 401:
            raise ToolProviderCredentialValidationError(
                "Authentication failed. Please check your QuickBooks API access token."
            )

        else:
            error_detail = response.json() if response.content else {}
            error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
            raise Exception(f"Failed to search customers: {error_msg}")

    def _create_customer(self, api_base_url: str, realm_id: str, headers: dict,
                        display_name: str, company_name: str = None,
                        email: str = None, phone: str = None) -> Generator[ToolInvokeMessage, None, None]:
        """Create a new customer."""
        payload: dict[str, Any] = {
            "DisplayName": display_name
        }

        if company_name:
            payload["CompanyName"] = company_name

        if email:
            payload["PrimaryEmailAddr"] = {"Address": email}

        if phone:
            payload["PrimaryPhone"] = {"FreeFormNumber": phone}

        response = httpx.post(
            f"{api_base_url}/company/{realm_id}/customer?minorversion=65",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            data = response.json()
            customer = data.get("Customer", {})

            result = {
                "id": customer.get("Id"),
                "display_name": customer.get("DisplayName"),
                "company_name": customer.get("CompanyName", ""),
                "sync_token": customer.get("SyncToken"),
                "message": f"Successfully created customer '{display_name}'"
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
                f"Failed to create customer: {response.status_code} - {error_msg}"
            )
