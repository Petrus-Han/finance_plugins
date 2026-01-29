import urllib.parse
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class VendorManagementTool(Tool):
    """Tool to search for or create vendors in QuickBooks Online."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the vendor_management tool to search or create vendors.

        Args:
            tool_parameters: Dictionary containing action and vendor parameters

        Returns:
            Vendor information or search results
        """
        # Get required parameters
        action = tool_parameters.get("action")
        name = tool_parameters.get("name")

        if not action or not name:
            raise ValueError("action and name are required parameters")

        if action not in ["search", "create"]:
            raise ValueError("action must be 'search' or 'create'")

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
            if action == "search":
                # Search for vendors by name
                name_escaped = name.replace("'", "''")
                query = f"select * from Vendor where DisplayName like '%{name_escaped}%'"
                encoded_query = urllib.parse.quote(query)
                url = f"{api_base_url}/company/{realm_id}/query?query={encoded_query}&minorversion=65"

                response = httpx.get(
                    url,
                    headers=headers,
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    vendors = data.get("QueryResponse", {}).get("Vendor", [])

                    if not vendors:
                        raise ValueError(f"No vendors found matching '{name}'")

                    # Format vendors for output
                    output = []
                    for vendor in vendors:
                        vendor_info = {
                            "id": vendor.get("Id"),
                            "display_name": vendor.get("DisplayName"),
                            "company_name": vendor.get("CompanyName"),
                            "active": vendor.get("Active"),
                            "balance": vendor.get("Balance", 0),
                            "print_on_check_name": vendor.get("PrintOnCheckName"),
                            "sync_token": vendor.get("SyncToken")
                        }
                        output.append(vendor_info)

                    result = {
                        "vendors": output,
                        "count": len(output)
                    }
                    # Only create variable message for scalar values
                    yield self.create_variable_message("count", len(output))
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
                        f"Failed to search vendors: {response.status_code} - {error_msg}"
                    )

            elif action == "create":
                # Create a new vendor
                url = f"{api_base_url}/company/{realm_id}/vendor?minorversion=65"
                payload = {
                    "DisplayName": name,
                    "CompanyName": name
                }

                response = httpx.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:
                    data = response.json()
                    vendor = data.get("Vendor", {})

                    result = {
                        "id": vendor.get("Id"),
                        "display_name": vendor.get("DisplayName"),
                        "company_name": vendor.get("CompanyName"),
                        "active": vendor.get("Active"),
                        "balance": vendor.get("Balance", 0),
                        "sync_token": vendor.get("SyncToken"),
                        "meta_data": vendor.get("MetaData", {})
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
                        f"Failed to create vendor: {response.status_code} - {error_msg}"
                    )

        except httpx.HTTPError as e:
            raise Exception(f"Network error while managing vendors: {str(e)}") from e
