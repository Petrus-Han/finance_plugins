from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GetRecipientTool(Tool):
    """Tool to retrieve details for a specific Mercury recipient."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_recipient tool to fetch recipient details.

        Args:
            tool_parameters: Dictionary containing:
                - recipient_id: The recipient ID (required)

        Returns:
            Detailed recipient information
        """
        # Get parameters
        recipient_id = tool_parameters.get("recipient_id", "")
        if not recipient_id:
            raise ValueError("Recipient ID is required.")

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

        try:
            response = httpx.get(
                f"{api_base_url}/recipient/{recipient_id}",
                headers=headers,
                timeout=15
            )

            if response.status_code == 200:
                rcp = response.json()

                # Build comprehensive output
                recipient_info = {
                    "id": rcp.get("id", ""),
                    "name": rcp.get("name", ""),
                    "status": rcp.get("status", ""),
                    "emails": rcp.get("emails", []),
                    "payment_method": rcp.get("paymentMethod", ""),
                    "created_at": rcp.get("createdAt", ""),
                }

                # Include routing info
                routing_info = rcp.get("electronicRoutingInfo", {})
                if routing_info:
                    recipient_info["electronic_routing_info"] = {
                        "account_number": routing_info.get("accountNumber", ""),
                        "routing_number": routing_info.get("routingNumber", ""),
                        "bank_name": routing_info.get("bankName", ""),
                        "account_type": routing_info.get("accountType", ""),
                    }

                # Include address
                address = rcp.get("address", {})
                if address:
                    recipient_info["address"] = {
                        "address1": address.get("address1", ""),
                        "address2": address.get("address2", ""),
                        "city": address.get("city", ""),
                        "region": address.get("region", ""),
                        "postal_code": address.get("postalCode", ""),
                        "country": address.get("country", ""),
                    }

                # Include attachments
                attachments = rcp.get("attachments", [])
                if attachments:
                    recipient_info["attachments"] = [
                        {
                            "id": att.get("id", ""),
                            "file_name": att.get("fileName", ""),
                            "tax_form_type": att.get("taxFormType", ""),
                            "uploaded_at": att.get("uploadedAt", ""),
                        }
                        for att in attachments
                    ]

                yield self.create_json_message(recipient_info)

            elif response.status_code == 404:
                raise ValueError(f"Recipient with ID '{recipient_id}' not found.")
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your Mercury API access token."
                )
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to retrieve recipient: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while fetching recipient: {str(e)}") from e
