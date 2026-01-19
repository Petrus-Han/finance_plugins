from __future__ import annotations

import logging
import sys
from typing import Any, Mapping, Optional

from werkzeug import Request

from dify_plugin.entities.trigger import Variables
from dify_plugin.errors.trigger import TriggerDispatchError
from dify_plugin.interfaces.trigger import Event

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


def log_info(msg: str):
    """Log info message."""
    print(f"[TRANSACTION_EVENT] INFO: {msg}", flush=True)
    logger.info(msg)


class TransactionEvent(Event):
    """Mercury transaction event handler.

    Processes incoming transaction webhooks and normalizes the payload
    for downstream workflow consumption.
    """

    def _on_event(
        self,
        request: Request,
        parameters: Mapping[str, Any],
        payload: Mapping[str, Any]
    ) -> Optional[Variables]:
        """Process transaction event and return normalized variables.

        Args:
            request: The incoming webhook request
            parameters: Event-level parameters (includes operation_filter)
            payload: The webhook payload (may be empty, use request.get_json())

        Expected payload format (from Mercury):
        {
            "id": "evt_xxx",
            "resourceType": "transaction",
            "operationType": "created" | "updated",
            "resourceId": "txn_xxx",
            "mergePatch": {
                "accountId": "acc_xxx",
                "amount": -150.00,
                "status": "posted",
                "postedAt": "2025-12-19T10:30:00Z",
                "counterpartyName": "Staples",
                "bankDescription": "DEBIT CARD PURCHASE",
                "note": "",
                "category": "",
                "type": "debit"
            }
        }

        Returns:
            Variables with normalized transaction data, or None if filtered out
        """
        log_info("=== TransactionEvent._on_event called ===")

        # Get the raw payload from request
        raw_payload = request.get_json(force=True) or {}
        log_info(f"Raw payload keys: {list(raw_payload.keys())}")

        # Get operation type from payload
        operation_type = raw_payload.get("operationType", "")
        log_info(f"Operation type: {operation_type}")

        # Check operation_filter parameter
        operation_filter = parameters.get("operation_filter", "all")
        log_info(f"Operation filter: {operation_filter}")

        # Apply operation filter
        if operation_filter != "all":
            if operation_filter == "created" and operation_type != "created":
                log_info(f"Skipping event: filter is 'created' but operation is '{operation_type}'")
                # Return empty variables to skip this event
                return Variables(variables={
                    "_filtered": True,
                    "_filter_reason": f"Operation filter is 'created' but event is '{operation_type}'"
                })
            elif operation_filter == "updated" and operation_type != "updated":
                log_info(f"Skipping event: filter is 'updated' but operation is '{operation_type}'")
                return Variables(variables={
                    "_filtered": True,
                    "_filter_reason": f"Operation filter is 'updated' but event is '{operation_type}'"
                })

        # Extract fields from Mercury's JSON Merge Patch format
        merge_patch = raw_payload.get("mergePatch", {})
        log_info(f"MergePatch keys: {list(merge_patch.keys())}")

        # Build normalized variables
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

        log_info(f"Returning variables: event_id={variables['event_id']}, "
                 f"transaction_id={variables['transaction_id']}, "
                 f"amount={variables['amount']}")

        return Variables(variables=variables)
