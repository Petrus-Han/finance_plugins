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
    """Tool to retrieve audit events tracking resource changes.

    Supports polling mode with cursor pagination and time-based filtering
    for incremental event synchronization.
    """

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
                yield from self._get_single_event(api_base_url, headers, event_id)
            else:
                yield from self._list_events(api_base_url, headers, tool_parameters)

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _get_single_event(self, api_base_url: str, headers: dict, event_id: str) -> Generator[ToolInvokeMessage, None, None]:
        """Get a specific event by ID."""
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

    def _list_events(self, api_base_url: str, headers: dict, tool_parameters: dict) -> Generator[ToolInvokeMessage, None, None]:
        """List events with filtering and pagination support."""
        url = f"{api_base_url}/events"
        params: dict[str, Any] = {}

        # Resource type filter
        if tool_parameters.get("resource_type"):
            params["resourceType"] = tool_parameters["resource_type"]

        # Event type filter (e.g., "transaction.created")
        if tool_parameters.get("event_type"):
            params["eventType"] = tool_parameters["event_type"]

        # Pagination
        if tool_parameters.get("limit"):
            params["limit"] = int(tool_parameters["limit"])
        if tool_parameters.get("start_after"):
            params["start_after"] = tool_parameters["start_after"]
        if tool_parameters.get("end_before"):
            params["end_before"] = tool_parameters["end_before"]

        # Time range filter (ISO 8601 format)
        if tool_parameters.get("start_time"):
            params["start"] = tool_parameters["start_time"]
        if tool_parameters.get("end_time"):
            params["end"] = tool_parameters["end_time"]

        logger.info(f"Making request to: {url} with params: {params}")
        response = httpx.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            events = [self._format_event(e) for e in data.get("events", [])]

            result = {
                "success": True,
                "events": events,
                "count": len(events),
                "message": f"Found {len(events)} events"
            }

            # Include pagination info for polling
            if data.get("hasMore"):
                result["has_more"] = True
                result["next_cursor"] = data.get("nextCursor")
            else:
                result["has_more"] = False

            yield self.create_json_message(result)
        else:
            self._handle_error(response)

    def _format_event(self, event: dict) -> dict:
        """Format event data for output."""
        # Extract data from different response formats
        data = event.get("data", event.get("mergePatch", {}))
        previous_data = event.get("previousData", event.get("previousValues"))

        return {
            "id": event.get("id", ""),
            "type": event.get("type", ""),  # e.g., "transaction.created"
            "resource_type": event.get("resourceType", ""),
            "resource_id": event.get("resourceId", ""),
            "operation_type": event.get("operationType", ""),
            "created_at": event.get("createdAt", event.get("occurredAt", "")),
            "resource_version": event.get("resourceVersion"),
            "changed_paths": event.get("changedPaths", []),
            "data": data,
            "previous_data": previous_data,
        }

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed. Check your API token.")
        error_detail = response.json() if response.content else {}
        error_msg = error_detail.get("message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
