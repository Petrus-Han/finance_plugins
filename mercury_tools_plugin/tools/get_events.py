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


class GetEventsTool(Tool):
    """Tool to retrieve audit events tracking resource changes."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        logger.info("=== GetEventsTool._invoke called ===")

        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        api_environment = self.runtime.credentials.get("api_environment", "production")
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
        }

        event_id = tool_parameters.get("event_id")

        try:
            if event_id:
                # Get specific event
                url = f"{api_base_url}/event/{event_id}"
                logger.info(f"Making request to: {url}")
                response = httpx.get(url, headers=headers, timeout=15)

                if response.status_code == 200:
                    event = self._format_event(response.json())
                    yield self.create_json_message({
                        "success": True,
                        "event": event,
                        "message": "Event retrieved successfully"
                    })
                elif response.status_code == 404:
                    raise ValueError(f"Event not found: {event_id}")
                else:
                    self._handle_error(response)
            else:
                # List all events
                url = f"{api_base_url}/events"
                params: dict[str, Any] = {}

                if tool_parameters.get("resource_type"):
                    params["resourceType"] = tool_parameters["resource_type"]
                if tool_parameters.get("limit"):
                    params["limit"] = int(tool_parameters["limit"])

                logger.info(f"Making request to: {url} with params: {params}")
                response = httpx.get(url, headers=headers, params=params, timeout=15)

                if response.status_code == 200:
                    data = response.json()
                    events = [self._format_event(e) for e in data.get("events", [])]
                    yield self.create_json_message({
                        "success": True,
                        "events": events,
                        "message": f"Found {len(events)} events"
                    })
                else:
                    self._handle_error(response)

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _format_event(self, event: dict) -> dict:
        return {
            "id": event.get("id", ""),
            "resource_type": event.get("resourceType", ""),
            "resource_id": event.get("resourceId", ""),
            "operation_type": event.get("operationType", ""),
            "resource_version": event.get("resourceVersion"),
            "occurred_at": event.get("occurredAt", ""),
            "changed_paths": event.get("changedPaths", []),
            "merge_patch": event.get("mergePatch", {}),
            "previous_values": event.get("previousValues"),
        }

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed. Check your API token.")
        error_detail = response.json() if response.content else {}
        error_msg = error_detail.get("message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
