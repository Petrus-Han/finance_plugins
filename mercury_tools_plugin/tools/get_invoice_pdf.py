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


class GetInvoicePdfTool(Tool):
    """Tool to download an AR invoice as PDF."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        logger.info("=== GetInvoicePdfTool._invoke called ===")

        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        api_environment = self.runtime.credentials.get("api_environment", "production")
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        invoice_id = tool_parameters.get("invoice_id")
        if not invoice_id:
            raise ValueError("invoice_id is required")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/pdf",
        }

        try:
            url = f"{api_base_url}/ar/invoices/{invoice_id}/pdf"
            logger.info(f"Making request to: {url}")

            response = httpx.get(url, headers=headers, timeout=30)
            logger.info(f"Response status: {response.status_code}")

            if response.status_code == 200:
                content_type = response.headers.get("content-type", "")
                if "application/pdf" in content_type or response.content[:4] == b"%PDF":
                    filename = f"mercury_invoice_{invoice_id}.pdf"
                    yield self.create_blob_message(
                        blob=response.content,
                        meta={"mime_type": "application/pdf", "filename": filename}
                    )
                    yield self.create_json_message({
                        "success": True,
                        "filename": filename,
                        "message": f"Invoice PDF downloaded successfully ({len(response.content)} bytes)"
                    })
                else:
                    raise Exception(f"Unexpected content type: {content_type}")
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError("Authentication failed. Check your API token.")
            elif response.status_code == 403:
                # Check for AR subscription error
                try:
                    error_detail = response.json()
                    errors = error_detail.get("errors", {})
                    if "subscriptions" in errors:
                        raise Exception(
                            "此功能需要 Mercury AR (Accounts Receivable) 订阅。"
                            "请在 Mercury Dashboard 的 Plan & Billing 中订阅 AR 服务。"
                            "了解更多: https://mercury.com/pricing"
                        )
                except:
                    pass
                raise Exception(f"Access denied: {response.status_code} - {response.text}")
            elif response.status_code == 404:
                raise ValueError(f"Invoice not found: {invoice_id}")
            else:
                raise Exception(f"Failed to download invoice PDF: {response.status_code} - {response.text}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e
