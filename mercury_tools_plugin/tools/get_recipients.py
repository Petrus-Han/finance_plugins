from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GetRecipientsTool(Tool):
    """Tool to retrieve all payment recipients from Mercury."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_recipients tool to fetch all recipients.

        Args:
            tool_parameters: Dictionary containing:
                - limit: Maximum number of results (optional, default 50)

        Returns:
            List of recipients with their details
        """
        # Get parameters
        limit = tool_parameters.get("limit", 50)

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        # Get API environment
        api_environment = self.runtime.credentials.get("api_environment", "production")

        # Determine API base URL based on environment
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
        }

        params = {"limit": limit}

        try:
            response = httpx.get(
                f"{api_base_url}/recipients",
                headers=headers,
                params=params,
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()
                recipients = data.get("recipients", [])

                if not recipients:
                    yield self.create_text_message("No recipients found.")
                    return

                # Format recipients for output
                output = []
                for rcp in recipients:
                    recipient_info = {
                        "id": rcp.get("id", ""),
                        "name": rcp.get("name", ""),
                        "status": rcp.get("status", ""),
                        "emails": rcp.get("emails", []),
                        "payment_method": rcp.get("paymentMethod", ""),
                        "created_at": rcp.get("createdAt", ""),
                    }

                    # Include routing info if available
                    routing_info = rcp.get("electronicRoutingInfo", {})
                    if routing_info:
                        recipient_info["bank_name"] = routing_info.get("bankName", "")
                        recipient_info["account_number_masked"] = routing_info.get("accountNumber", "")

                    # Include address if available
                    address = rcp.get("address", {})
                    if address:
                        recipient_info["address"] = {
                            "city": address.get("city", ""),
                            "region": address.get("region", ""),
                            "country": address.get("country", ""),
                        }

                    output.append(recipient_info)

                # Yield as variables for direct access
                yield self.create_variable_message("recipients", output)
                yield self.create_variable_message("count", len(recipients))
                yield self.create_variable_message("has_more", data.get("hasMore", False))

                # Also yield the full JSON for convenience
                yield self.create_json_message({
                    "recipients": output,
                    "count": len(recipients),
                    "has_more": data.get("hasMore", False)
                })

            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your Mercury API access token."
                )
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to retrieve recipients: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while fetching recipients: {str(e)}") from e
