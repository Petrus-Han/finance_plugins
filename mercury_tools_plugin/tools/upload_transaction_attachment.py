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


class UploadTransactionAttachmentTool(Tool):
    """Tool to upload an attachment to a transaction."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        logger.info("=== UploadTransactionAttachmentTool._invoke called ===")

        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        api_environment = self.runtime.credentials.get("api_environment", "production")
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        transaction_id = tool_parameters.get("transaction_id")
        if not transaction_id:
            raise ValueError("transaction_id is required")

        file_data = tool_parameters.get("file")
        if not file_data:
            raise ValueError("file is required")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
        }

        try:
            url = f"{api_base_url}/transaction/{transaction_id}/attachment"
            logger.info(f"Making request to: {url}")

            # Handle file input from Dify
            if isinstance(file_data, dict):
                file_content = file_data.get("data", b"")
                file_name = file_data.get("filename", "attachment")
                mime_type = file_data.get("mime_type", "application/octet-stream")
            else:
                file_content = file_data
                file_name = "attachment"
                mime_type = "application/octet-stream"

            files = {
                "file": (file_name, file_content, mime_type)
            }

            response = httpx.post(url, headers=headers, files=files, timeout=60)
            logger.info(f"Response status: {response.status_code}")

            if response.status_code in (200, 201):
                data = response.json()
                yield self.create_json_message({
                    "success": True,
                    "attachment": {
                        "id": data.get("id", ""),
                        "filename": data.get("fileName", file_name),
                        "url": data.get("url", ""),
                    },
                    "message": "Attachment uploaded successfully"
                })
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError("Authentication failed. Check your API token.")
            elif response.status_code == 404:
                raise ValueError(f"Transaction not found: {transaction_id}")
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to upload attachment: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e
