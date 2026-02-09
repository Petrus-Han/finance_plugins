import csv
import io
import logging
from collections.abc import Generator
from datetime import UTC, datetime
from typing import Any

import gspread
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from provider.employee_roster import ROSTER_HEADERS, ensure_sheets_initialized, get_gspread_client

logger = logging.getLogger(__name__)

# Column mapping: source CSV header -> our canonical field
# Feishu uses Chinese headers, Deel uses English headers
_COLUMN_MAPS: dict[str, dict[str, str]] = {
    "feishu": {
        "姓名": "full_name",
        "名字": "full_name",
        "邮箱": "email",
        "工作邮箱": "email",
        "邮件": "email",
        "工号": "source_id",
        "员工工号": "source_id",
        "部门": "source_department",
        "职位": "job_title",
        "职务": "job_title",
        "雇佣类型": "employment_type",
        "员工类型": "employment_type",
        "状态": "status",
        "员工状态": "status",
        # English fallbacks in case Feishu exports English headers
        "name": "full_name",
        "full_name": "full_name",
        "email": "email",
        "employee_id": "source_id",
        "department": "source_department",
        "job_title": "job_title",
        "employment_type": "employment_type",
        "status": "status",
    },
    "deel": {
        "name": "full_name",
        "full_name": "full_name",
        "full name": "full_name",
        "email": "email",
        "work email": "email",
        "id": "source_id",
        "employee_id": "source_id",
        "employee id": "source_id",
        "contract_id": "source_id",
        "department": "source_department",
        "team": "source_department",
        "job_title": "job_title",
        "job title": "job_title",
        "title": "job_title",
        "role": "job_title",
        "contract_type": "employment_type",
        "contract type": "employment_type",
        "type": "employment_type",
        "status": "status",
    },
}

# Fields that can be updated from CSV (finance_department and notes are preserved)
_UPDATABLE_FIELDS = ("full_name", "email", "source_department", "job_title", "employment_type", "status")


def _map_csv_row(row: dict[str, str], source: str) -> dict[str, str]:
    """Map a raw CSV row to our canonical roster fields using the column map."""
    col_map = _COLUMN_MAPS.get(source, _COLUMN_MAPS["deel"])
    mapped: dict[str, str] = {}
    for csv_header, value in row.items():
        canonical = col_map.get(csv_header.strip().lower())
        if canonical and canonical not in mapped:
            mapped[canonical] = value.strip()
    return mapped


def _build_index(records: list[dict[str, str]]) -> tuple[dict[str, int], dict[str, int]]:
    """Build lookup indexes from existing roster records.

    Returns:
        (source_index, email_index) where values are 0-based row indices.
    """
    source_index: dict[str, int] = {}
    email_index: dict[str, int] = {}
    for idx, rec in enumerate(records):
        src = rec.get("source", "")
        sid = rec.get("source_id", "")
        email = rec.get("email", "").lower()
        if src and sid:
            source_index[f"{src}:{sid}"] = idx
        if email:
            email_index[email] = idx
    return source_index, email_index


def _find_existing_idx(
    mapped: dict[str, str], source: str, source_index: dict[str, int], email_index: dict[str, int]
) -> int | None:
    """Find the index of an existing record matching by (source, source_id) then email."""
    sid = mapped.get("source_id", "")
    if sid:
        idx = source_index.get(f"{source}:{sid}")
        if idx is not None:
            return idx
    email_val = mapped.get("email", "").lower()
    if email_val:
        return email_index.get(email_val)
    return None


def _compute_changes(
    mapped: dict[str, str], existing: dict[str, str], source: str, now_ts: str
) -> dict[str, str]:
    """Compute field-level changes, preserving finance_department and notes."""
    changes: dict[str, str] = {}
    for field in _UPDATABLE_FIELDS:
        new_val = mapped.get(field, "")
        if new_val and new_val != str(existing.get(field, "")):
            changes[field] = new_val
    sid = mapped.get("source_id", "")
    if source != str(existing.get("source", "")):
        changes["source"] = source
    if sid and sid != str(existing.get("source_id", "")):
        changes["source_id"] = sid
    changes["last_synced"] = now_ts
    return changes


def _build_new_row(mapped: dict[str, str], source: str, now_ts: str) -> list[str]:
    """Build a new roster row from mapped CSV data."""
    new_row = {h: "" for h in ROSTER_HEADERS}
    new_row["source"] = source
    new_row["last_synced"] = now_ts
    for field, value in mapped.items():
        if field in new_row:
            new_row[field] = value
    return [new_row[h] for h in ROSTER_HEADERS]


def _apply_writes(  # noqa: PLR0913
    ws: gspread.Worksheet,
    spreadsheet: gspread.Spreadsheet,
    cells_to_update: list[tuple[int, dict[str, str]]],
    rows_to_append: list[list[str]],
    now_ts: str,
    source: str,
    added: int,
    updated: int,
    skipped: int,
) -> None:
    """Write updates, appends, and sync log to the spreadsheet."""
    if cells_to_update:
        batch_updates: list[dict[str, Any]] = []
        for row_num, changes in cells_to_update:
            for field, value in changes.items():
                if field in ROSTER_HEADERS:
                    col_idx = ROSTER_HEADERS.index(field) + 1
                    cell_ref = gspread.utils.rowcol_to_a1(row_num, col_idx)
                    batch_updates.append({"range": cell_ref, "values": [[value]]})
        if batch_updates:
            ws.batch_update(batch_updates)

    if rows_to_append:
        ws.append_rows(rows_to_append, value_input_option="RAW")

    try:
        sync_ws = spreadsheet.worksheet("Sync_Log")
        log_row = [now_ts, source, str(added), str(updated), str(skipped)]
        sync_ws.append_row(log_row, value_input_option="RAW")
    except Exception as e:
        logger.warning(f"Failed to write sync log: {e}")


class ImportRosterCsvTool(Tool):
    """Import employee records from Feishu or Deel CSV export."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:  # noqa: PLR0912, PLR0915
        csv_content = tool_parameters.get("csv_content", "")
        source = tool_parameters.get("source", "")
        dry_run = tool_parameters.get("dry_run", False)

        if not csv_content:
            raise ValueError("csv_content is required")
        if source not in ("feishu", "deel"):
            raise ValueError("source must be 'feishu' or 'deel'")

        credentials = self.runtime.credentials
        spreadsheet_id = credentials.get("spreadsheet_id")
        if not spreadsheet_id:
            raise ToolProviderCredentialValidationError("Google Spreadsheet ID is required.")

        try:
            client = get_gspread_client(credentials)
            spreadsheet = client.open_by_key(spreadsheet_id)
            ensure_sheets_initialized(spreadsheet)
        except gspread.exceptions.APIError as e:
            raise Exception(f"Google Sheets API error: {e}") from e

        csv_rows = list(csv.DictReader(io.StringIO(csv_content)))
        if not csv_rows:
            raise ValueError("CSV content is empty or has no data rows")

        ws = spreadsheet.worksheet("Roster")
        existing_records = ws.get_all_records(expected_headers=ROSTER_HEADERS)
        source_index, email_index = _build_index(existing_records)

        now_ts = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        added, updated, skipped = 0, 0, 0
        errors: list[str] = []
        rows_to_append: list[list[str]] = []
        cells_to_update: list[tuple[int, dict[str, str]]] = []

        for i, raw_row in enumerate(csv_rows, start=1):
            try:
                mapped = _map_csv_row(raw_row, source)
                if not mapped.get("full_name") and not mapped.get("email"):
                    errors.append(f"Row {i}: missing both name and email, skipped")
                    continue

                existing_idx = _find_existing_idx(mapped, source, source_index, email_index)

                if existing_idx is not None:
                    changes = _compute_changes(mapped, existing_records[existing_idx], source, now_ts)
                    if len(changes) > 1:  # more than just last_synced
                        cells_to_update.append((existing_idx + 2, changes))  # +2: header + 0-index
                        updated += 1
                    else:
                        skipped += 1
                else:
                    rows_to_append.append(_build_new_row(mapped, source, now_ts))
                    # Update indexes to prevent duplicate inserts within the same batch
                    new_idx = len(existing_records) + len(rows_to_append) - 1
                    sid = mapped.get("source_id", "")
                    if sid:
                        source_index[f"{source}:{sid}"] = new_idx
                    email_val = mapped.get("email", "").lower()
                    if email_val:
                        email_index[email_val] = new_idx
                    added += 1
            except Exception as e:
                errors.append(f"Row {i}: {e}")

        if not dry_run:
            _apply_writes(ws, spreadsheet, cells_to_update, rows_to_append, now_ts, source, added, updated, skipped)

        result = {"added": added, "updated": updated, "skipped": skipped, "errors": errors, "dry_run": dry_run}

        yield self.create_variable_message("added", added)
        yield self.create_variable_message("updated", updated)
        yield self.create_variable_message("skipped", skipped)
        yield self.create_json_message(result)
