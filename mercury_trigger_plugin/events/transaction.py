from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from werkzeug import Request

from dify_plugin.entities.trigger import Variables
from dify_plugin.errors.trigger import EventIgnoreError
from dify_plugin.interfaces.trigger import Event


class TransactionEvent(Event):
    """Mercury transaction event handler."""

    def _on_event(
        self, request: Request, parameters: Mapping[str, Any], payload: Mapping[str, Any]
    ) -> Variables:
        raw_payload = request.get_json(force=True) or {}

        # Get and filter by operation type
        operation_type = raw_payload.get("operationType", "")
        operation_filter = parameters.get("operation_filter", "all")

        if operation_filter != "all":
            if operation_filter == "created" and operation_type != "created":
                raise EventIgnoreError()
            if operation_filter == "updated" and operation_type != "updated":
                raise EventIgnoreError()

        # Extract fields from Mercury's JSON Merge Patch format
        merge_patch = raw_payload.get("mergePatch", {})

        variables = {
            "event_id": raw_payload.get("id", ""),
            "transaction_id": raw_payload.get("resourceId", ""),
            "operation_type": operation_type,
            "account_id": merge_patch.get("accountId", ""),
            "amount": merge_patch.get("amount"),
            "status": merge_patch.get("status", ""),
            "posted_at": merge_patch.get("postedAt", ""),
            "counterparty_name": merge_patch.get("counterpartyName", ""),
            "bank_description": merge_patch.get("bankDescription", ""),
            "note": merge_patch.get("note", ""),
            "category": merge_patch.get("category", merge_patch.get("mercuryCategory", "")),
            "transaction_type": merge_patch.get("type", merge_patch.get("kind", "")),
        }

        return Variables(variables=variables)
