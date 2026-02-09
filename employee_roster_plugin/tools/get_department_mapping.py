import logging
from collections.abc import Generator
from typing import Any

import gspread
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from provider.employee_roster import DEPARTMENT_MAPPING_HEADERS, ensure_sheets_initialized, get_gspread_client

logger = logging.getLogger(__name__)


class GetDepartmentMappingTool(Tool):
    """Get the department mapping table (source department -> finance department)."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        source_department_filter = (tool_parameters.get("source_department") or "").strip()

        credentials = self.runtime.credentials
        spreadsheet_id = credentials.get("spreadsheet_id")
        if not spreadsheet_id:
            raise ToolProviderCredentialValidationError("Google Spreadsheet ID is required.")

        try:
            client = get_gspread_client(credentials)
            spreadsheet = client.open_by_key(spreadsheet_id)
            ensure_sheets_initialized(spreadsheet)

            ws = spreadsheet.worksheet("Department_Mapping")
            all_records = ws.get_all_records(expected_headers=DEPARTMENT_MAPPING_HEADERS)
        except gspread.exceptions.APIError as e:
            raise Exception(f"Google Sheets API error: {e}") from e

        # Optionally filter by source department (fuzzy match)
        if source_department_filter:
            filter_lower = source_department_filter.lower()
            mappings = [
                {
                    "source_department": row.get("source_department", ""),
                    "finance_department": row.get("finance_department", ""),
                    "source": row.get("source", ""),
                }
                for row in all_records
                if filter_lower in str(row.get("source_department", "")).lower()
            ]
        else:
            mappings = [
                {
                    "source_department": row.get("source_department", ""),
                    "finance_department": row.get("finance_department", ""),
                    "source": row.get("source", ""),
                }
                for row in all_records
            ]

        result = {
            "mappings": mappings,
            "count": len(mappings),
        }

        yield self.create_variable_message("count", len(mappings))
        yield self.create_json_message(result)
