import json
import logging
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin.config.logger_format import plugin_logger_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(plugin_logger_handler)


class EditRecipientTool(Tool):
    """Tool to update an existing recipient."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        logger.info("=== EditRecipientTool._invoke called ===")

        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        api_environment = self.runtime.credentials.get("api_environment", "production")
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        recipient_id = tool_parameters.get("recipient_id")
        if not recipient_id:
            raise ValueError("recipient_id is required")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }

        # Build payload with only provided fields
        payload: dict[str, Any] = {}

        if tool_parameters.get("name"):
            payload["name"] = tool_parameters["name"]
        if tool_parameters.get("nickname"):
            payload["nickname"] = tool_parameters["nickname"]
        if tool_parameters.get("contact_email"):
            payload["contactEmail"] = tool_parameters["contact_email"]

        if tool_parameters.get("emails_json"):
            try:
                payload["emails"] = json.loads(tool_parameters["emails_json"])
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid emails_json: {e}")

        # Build electronic routing info if account details provided
        account_number = tool_parameters.get("account_number")
        routing_number = tool_parameters.get("routing_number")
        if account_number and routing_number:
            payload["electronicRoutingInfo"] = {
                "accountNumber": account_number,
                "routingNumber": routing_number,
                "accountType": tool_parameters.get("account_type", "checking"),
            }

        if not payload:
            raise ValueError("At least one field must be provided for update")

        try:
            url = f"{api_base_url}/recipient/{recipient_id}"
            logger.info(f"Making request to: {url}")

            response = httpx.post(url, headers=headers, json=payload, timeout=15)
            logger.info(f"Response status: {response.status_code}")

            if response.status_code == 200:
                recipient = response.json()
                result = {
                    "success": True,
                    "recipient": {
                        "id": recipient.get("id", ""),
                        "name": recipient.get("name", ""),
                        "nickname": recipient.get("nickname"),
                        "status": recipient.get("status", ""),
                        "emails": recipient.get("emails", []),
                        "contact_email": recipient.get("contactEmail"),
                        "default_payment_method": recipient.get("defaultPaymentMethod"),
                        "date_last_paid": recipient.get("dateLastPaid"),
                    },
                    "message": "Recipient updated successfully"
                }

                # Yield each field as a separate variable for direct access
                for key, value in result.items():
                    yield self.create_variable_message(key, value)

                # Also yield the full JSON for convenience
                yield self.create_json_message(result)
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError("Authentication failed. Check your API token.")
            elif response.status_code == 404:
                raise ValueError(f"Recipient not found: {recipient_id}")
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to update recipient: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e
