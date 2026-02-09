import logging
from collections.abc import Generator
from typing import Any

import gspread
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from provider.employee_roster import ROSTER_HEADERS, ensure_sheets_initialized, get_gspread_client

logger = logging.getLogger(__name__)


class QueryRosterTool(Tool):
    """Search the employee roster by name or email (fuzzy match)."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        query = (tool_parameters.get("query") or "").strip()
        if not query:
            raise ValueError("query parameter is required")

        credentials = self.runtime.credentials
        spreadsheet_id = credentials.get("spreadsheet_id")
        if not spreadsheet_id:
            raise ToolProviderCredentialValidationError("Google Spreadsheet ID is required.")

        try:
            client = get_gspread_client(credentials)
            spreadsheet = client.open_by_key(spreadsheet_id)
            ensure_sheets_initialized(spreadsheet)

            ws = spreadsheet.worksheet("Roster")
            all_records = ws.get_all_records(expected_headers=ROSTER_HEADERS)
        except gspread.exceptions.APIError as e:
            raise Exception(f"Google Sheets API error: {e}") from e

        # Fuzzy match: case-insensitive substring search on full_name and email
        query_lower = query.lower()
        matches = []
        for row in all_records:
            name = str(row.get("full_name", "")).lower()
            email = str(row.get("email", "")).lower()
            if query_lower in name or query_lower in email:
                matches.append({
                    "full_name": row.get("full_name", ""),
                    "email": row.get("email", ""),
                    "source": row.get("source", ""),
                    "source_department": row.get("source_department", ""),
                    "job_title": row.get("job_title", ""),
                    "employment_type": row.get("employment_type", ""),
                    "finance_department": row.get("finance_department", ""),
                    "status": row.get("status", ""),
                    "notes": row.get("notes", ""),
                })

        result = {
            "employees": matches,
            "count": len(matches),
        }

        yield self.create_variable_message("count", len(matches))
        yield self.create_json_message(result)
