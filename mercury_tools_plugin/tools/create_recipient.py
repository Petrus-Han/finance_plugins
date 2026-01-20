from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class CreateRecipientTool(Tool):
    """Tool to create a new payment recipient in Mercury."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the create_recipient tool to add a new recipient.

        Args:
            tool_parameters: Dictionary containing:
                - name: Recipient name (required)
                - payment_method: ach, wire, or check (required)
                - account_number: Bank account number (for ACH/wire)
                - routing_number: ABA routing number (for ACH/wire)
                - account_type: checking or savings
                - email: Contact email
                - address1, city, region, postal_code, country: Address fields

        Returns:
            Created recipient details including ID
        """
        # Get required parameters
        name = tool_parameters.get("name", "").strip()
        if not name:
            raise ValueError("Recipient name is required.")

        payment_method = tool_parameters.get("payment_method", "ach")

        # Validate payment method requirements
        if payment_method in ("ach", "wire"):
            account_number = tool_parameters.get("account_number", "").strip()
            routing_number = tool_parameters.get("routing_number", "").strip()
            if not account_number or not routing_number:
                raise ValueError(
                    f"Account number and routing number are required for {payment_method.upper()} payments."
                )

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
            "Content-Type": "application/json;charset=utf-8",
        }

        # Build request body
        recipient_data: dict[str, Any] = {
            "name": name,
            "paymentMethod": payment_method,
        }

        # Add email if provided
        email = tool_parameters.get("email", "").strip()
        if email:
            recipient_data["emails"] = [email]

        # Add electronic routing info for ACH/wire
        if payment_method in ("ach", "wire"):
            recipient_data["electronicRoutingInfo"] = {
                "accountNumber": tool_parameters.get("account_number", ""),
                "routingNumber": tool_parameters.get("routing_number", ""),
                "accountType": tool_parameters.get("account_type", "checking"),
            }

        # Add address if provided (required for check)
        address1 = tool_parameters.get("address1", "").strip()
        city = tool_parameters.get("city", "").strip()
        region = tool_parameters.get("region", "").strip()
        postal_code = tool_parameters.get("postal_code", "").strip()
        country = tool_parameters.get("country", "US").strip()

        if address1 and city:
            recipient_data["address"] = {
                "address1": address1,
                "city": city,
                "region": region,
                "postalCode": postal_code,
                "country": country,
            }
        elif payment_method == "check":
            raise ValueError("Address (address1 and city) is required for check payments.")

        try:
            response = httpx.post(
                f"{api_base_url}/recipients",
                headers=headers,
                json=recipient_data,
                timeout=15
            )

            if response.status_code in (200, 201):
                rcp = response.json()

                result = {
                    "success": True,
                    "id": rcp.get("id", ""),
                    "name": rcp.get("name", ""),
                    "status": rcp.get("status", ""),
                    "payment_method": rcp.get("paymentMethod", ""),
                    "created_at": rcp.get("createdAt", ""),
                    "message": f"Successfully created recipient '{name}'"
                }

                yield self.create_json_message(result)

            elif response.status_code == 400:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", "Invalid request")
                raise Exception(f"Failed to create recipient: {error_msg}")
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your Mercury API access token."
                )
            elif response.status_code == 403:
                raise Exception(
                    "Permission denied. Your API token may not have permission to create recipients."
                )
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to create recipient: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while creating recipient: {str(e)}") from e
