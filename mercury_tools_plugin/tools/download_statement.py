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


class DownloadStatementTool(Tool):
    """Tool to download a Mercury bank account statement as PDF."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the download_statement tool to fetch a statement PDF.

        Args:
            tool_parameters: Must include 'statement_id'

        Returns:
            PDF file as blob message
        """
        logger.info("=== DownloadStatementTool._invoke called ===")

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        # Get API environment
        api_environment = self.runtime.credentials.get("api_environment", "production")
        logger.info(f"API environment: {api_environment}")

        # Determine API base URL based on environment
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        # Get required parameter
        statement_id = tool_parameters.get("statement_id")
        if not statement_id:
            raise ValueError("statement_id is required")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/pdf",
        }

        try:
            url = f"{api_base_url}/statement/{statement_id}/pdf"
            logger.info(f"Making request to: {url}")

            response = httpx.get(url, headers=headers, timeout=30)
            logger.info(f"Response status: {response.status_code}")

            if response.status_code == 200:
                # Get content type to verify it's a PDF
                content_type = response.headers.get("content-type", "")
                logger.info(f"Content-Type: {content_type}")

                if "application/pdf" in content_type or response.content[:4] == b"%PDF":
                    # Generate filename
                    filename = f"mercury_statement_{statement_id}.pdf"

                    # Return as blob message
                    yield self.create_blob_message(
                        blob=response.content,
                        meta={"mime_type": "application/pdf", "filename": filename}
                    )
                    yield self.create_json_message({
                        "success": True,
                        "filename": filename,
                        "message": f"Statement PDF downloaded successfully ({len(response.content)} bytes)"
                    })
                else:
                    raise Exception(f"Unexpected content type: {content_type}")

            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    f"Authentication failed. Please check your Mercury API access token and ensure it's for the '{api_environment}' environment."
                )
            elif response.status_code == 404:
                raise ValueError(f"Statement not found: {statement_id}")
            else:
                error_detail = response.text
                raise Exception(f"Failed to download statement: {response.status_code} - {error_detail}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while downloading statement: {str(e)}") from e
