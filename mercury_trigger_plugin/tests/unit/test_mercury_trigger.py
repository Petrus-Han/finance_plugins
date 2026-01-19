#!/usr/bin/env python3
"""
Unit tests for Mercury Trigger Plugin

Tests the core functionality of:
- MercuryTrigger (event dispatch)
- MercurySubscriptionConstructor (webhook management)
- TransactionEvent (event processing)
"""

import base64
import hashlib
import hmac
import json
import time
from io import BytesIO
from typing import Any
from unittest.mock import MagicMock, patch

import pytest


# Mock werkzeug Request for testing
class MockRequest:
    """Mock werkzeug Request object."""

    def __init__(self, data: dict, headers: dict = None, raw_body: str = None):
        # If raw_body is provided, use it directly (for signature validation tests)
        # Otherwise, serialize the dict
        if raw_body is not None:
            self._data = raw_body
        else:
            self._data = json.dumps(data)
        self.headers = headers or {}
        self.method = "POST"

    def get_data(self, as_text=False):
        if as_text:
            return self._data
        return self._data.encode()

    def get_json(self, force=False):
        return json.loads(self._data)


def generate_signature(secret: str, timestamp: int, body: str) -> str:
    """Generate Mercury-style webhook signature."""
    try:
        secret_bytes = base64.b64decode(secret)
    except Exception:
        secret_bytes = secret.encode()

    signed_payload = f"{timestamp}.{body}"
    signature = hmac.new(
        secret_bytes,
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature


def create_mock_runtime():
    """Create a mock runtime object for testing."""
    runtime = MagicMock()
    runtime.credentials = {}
    return runtime


class TestTransactionEvent:
    """Tests for TransactionEvent handler."""

    def test_on_event_basic(self):
        """Test basic event processing."""
        from events.transaction import TransactionEvent

        # Create mock event with runtime
        mock_runtime = create_mock_runtime()
        event = TransactionEvent(runtime=mock_runtime)

        # Create test payload
        payload = {
            "id": "evt_test_001",
            "resourceType": "transaction",
            "operationType": "created",
            "resourceId": "txn_test_001",
            "mergePatch": {
                "accountId": "acc_test_001",
                "amount": -150.00,
                "status": "pending",
                "postedAt": "2026-01-15T10:30:00Z",
                "counterpartyName": "Test Vendor",
                "bankDescription": "TEST PAYMENT",
                "note": "Test note",
                "category": "software",
                "type": "externalTransfer"
            }
        }

        request = MockRequest(payload)
        parameters = {}

        # Process event
        result = event._on_event(request, parameters, payload)

        # Verify result
        assert result is not None
        assert result.variables["event_id"] == "evt_test_001"
        assert result.variables["transaction_id"] == "txn_test_001"
        assert result.variables["operation_type"] == "created"
        assert result.variables["account_id"] == "acc_test_001"
        assert result.variables["amount"] == -150.00
        assert result.variables["status"] == "pending"
        assert result.variables["counterparty_name"] == "Test Vendor"
        assert result.variables["bank_description"] == "TEST PAYMENT"
        assert result.variables["note"] == "Test note"

    def test_on_event_with_operation_filter_created(self):
        """Test event filtering - only created events."""
        from events.transaction import TransactionEvent

        mock_runtime = create_mock_runtime()
        event = TransactionEvent(runtime=mock_runtime)

        # Test created event with 'created' filter - should pass
        payload = {
            "id": "evt_test_002",
            "resourceType": "transaction",
            "operationType": "created",
            "resourceId": "txn_test_002",
            "mergePatch": {"accountId": "acc_001", "amount": -100}
        }

        request = MockRequest(payload)
        parameters = {"operation_filter": "created"}

        result = event._on_event(request, parameters, payload)
        assert result.variables.get("_filtered") is None
        assert result.variables["operation_type"] == "created"

        # Test updated event with 'created' filter - should be filtered
        payload["operationType"] = "updated"
        request = MockRequest(payload)

        result = event._on_event(request, parameters, payload)
        assert result.variables.get("_filtered") is True

    def test_on_event_with_operation_filter_updated(self):
        """Test event filtering - only updated events."""
        from events.transaction import TransactionEvent

        mock_runtime = create_mock_runtime()
        event = TransactionEvent(runtime=mock_runtime)

        # Test updated event with 'updated' filter - should pass
        payload = {
            "id": "evt_test_003",
            "resourceType": "transaction",
            "operationType": "updated",
            "resourceId": "txn_test_003",
            "mergePatch": {"accountId": "acc_001", "amount": -100, "status": "posted"}
        }

        request = MockRequest(payload)
        parameters = {"operation_filter": "updated"}

        result = event._on_event(request, parameters, payload)
        assert result.variables.get("_filtered") is None

        # Test created event with 'updated' filter - should be filtered
        payload["operationType"] = "created"
        request = MockRequest(payload)

        result = event._on_event(request, parameters, payload)
        assert result.variables.get("_filtered") is True

    def test_on_event_with_operation_filter_all(self):
        """Test event filtering - all events."""
        from events.transaction import TransactionEvent

        mock_runtime = create_mock_runtime()
        event = TransactionEvent(runtime=mock_runtime)

        for op_type in ["created", "updated"]:
            payload = {
                "id": f"evt_test_{op_type}",
                "resourceType": "transaction",
                "operationType": op_type,
                "resourceId": f"txn_test_{op_type}",
                "mergePatch": {"accountId": "acc_001", "amount": -100}
            }

            request = MockRequest(payload)
            parameters = {"operation_filter": "all"}

            result = event._on_event(request, parameters, payload)
            assert result.variables.get("_filtered") is None
            assert result.variables["operation_type"] == op_type

    def test_on_event_empty_merge_patch(self):
        """Test handling of events with empty mergePatch."""
        from events.transaction import TransactionEvent

        mock_runtime = create_mock_runtime()
        event = TransactionEvent(runtime=mock_runtime)

        payload = {
            "id": "evt_test_empty",
            "resourceType": "transaction",
            "operationType": "created",
            "resourceId": "txn_test_empty",
            "mergePatch": {}
        }

        request = MockRequest(payload)
        parameters = {}

        result = event._on_event(request, parameters, payload)

        assert result.variables["event_id"] == "evt_test_empty"
        assert result.variables["transaction_id"] == "txn_test_empty"
        assert result.variables["account_id"] == ""
        assert result.variables["amount"] is None


class TestSignatureValidation:
    """Tests for webhook signature validation."""

    def test_valid_signature(self):
        """Test that valid signatures are accepted."""
        from provider.mercury import MercuryTrigger

        mock_runtime = create_mock_runtime()
        trigger = MercuryTrigger(runtime=mock_runtime)

        # Create test data - use raw_body to ensure exact match
        secret = base64.b64encode(b"test_secret_key_32bytes_long!!!!").decode()
        body = '{"id":"evt_001","resourceType":"transaction"}'
        timestamp = int(time.time())
        signature = generate_signature(secret, timestamp, body)

        # Use raw_body parameter to ensure the exact string is used for signature verification
        request = MockRequest(
            data={},  # Not used when raw_body is provided
            headers={
                "Mercury-Signature": f"t={timestamp},v1={signature}"
            },
            raw_body=body  # Use exact body string for signature match
        )

        # Should not raise exception
        trigger._validate_signature(request, secret)

    def test_invalid_signature(self):
        """Test that invalid signatures are rejected."""
        from provider.mercury import MercuryTrigger
        from dify_plugin.errors.trigger import TriggerValidationError

        mock_runtime = create_mock_runtime()
        trigger = MercuryTrigger(runtime=mock_runtime)

        secret = base64.b64encode(b"test_secret_key_32bytes_long!!!!").decode()
        body = '{"id":"evt_001","resourceType":"transaction"}'
        timestamp = int(time.time())

        request = MockRequest(
            json.loads(body),
            headers={
                "Mercury-Signature": f"t={timestamp},v1=invalid_signature"
            }
        )

        with pytest.raises(TriggerValidationError) as exc_info:
            trigger._validate_signature(request, secret)

        assert "Invalid webhook signature" in str(exc_info.value)

    def test_missing_signature_header(self):
        """Test that missing signature header is rejected."""
        from provider.mercury import MercuryTrigger
        from dify_plugin.errors.trigger import TriggerValidationError

        mock_runtime = create_mock_runtime()
        trigger = MercuryTrigger(runtime=mock_runtime)

        request = MockRequest(
            {"id": "evt_001"},
            headers={}
        )

        with pytest.raises(TriggerValidationError) as exc_info:
            trigger._validate_signature(request, "secret")

        assert "Missing Mercury-Signature header" in str(exc_info.value)


class TestPayloadParsing:
    """Tests for webhook payload parsing."""

    def test_parse_valid_payload(self):
        """Test parsing valid JSON payload."""
        from provider.mercury import MercuryTrigger

        mock_runtime = create_mock_runtime()
        trigger = MercuryTrigger(runtime=mock_runtime)

        payload = {
            "id": "evt_001",
            "resourceType": "transaction",
            "operationType": "created"
        }

        request = MockRequest(payload)
        result = trigger._parse_payload(request)

        assert result["id"] == "evt_001"
        assert result["resourceType"] == "transaction"

    def test_parse_empty_payload(self):
        """Test parsing empty payload raises error."""
        from provider.mercury import MercuryTrigger
        from dify_plugin.errors.trigger import TriggerDispatchError

        mock_runtime = create_mock_runtime()
        trigger = MercuryTrigger(runtime=mock_runtime)

        request = MockRequest({})

        with pytest.raises(TriggerDispatchError) as exc_info:
            trigger._parse_payload(request)

        assert "Empty or invalid JSON payload" in str(exc_info.value)


class TestEventTypeResolution:
    """Tests for event type resolution."""

    def test_resolve_transaction_event(self):
        """Test resolving transaction event type."""
        from provider.mercury import MercuryTrigger

        mock_runtime = create_mock_runtime()
        trigger = MercuryTrigger(runtime=mock_runtime)

        payload = {
            "resourceType": "transaction",
            "operationType": "created"
        }

        result = trigger._resolve_event_types(payload)
        assert "transaction" in result

    def test_resolve_unknown_resource_type(self):
        """Test resolving unknown resource type defaults to transaction."""
        from provider.mercury import MercuryTrigger

        mock_runtime = create_mock_runtime()
        trigger = MercuryTrigger(runtime=mock_runtime)

        payload = {
            "resourceType": "unknown",
            "operationType": "created"
        }

        result = trigger._resolve_event_types(payload)
        # Default to transaction for now
        assert "transaction" in result


class TestSubscriptionConstructor:
    """Tests for MercurySubscriptionConstructor."""

    def test_get_api_base_url_production(self):
        """Test production API URL selection."""
        from provider.mercury import MercurySubscriptionConstructor

        mock_runtime = create_mock_runtime()
        constructor = MercurySubscriptionConstructor(runtime=mock_runtime)

        credentials = {"api_environment": "production"}
        url = constructor._get_api_base_url(credentials)

        assert url == "https://api.mercury.com/api/v1"

    def test_get_api_base_url_sandbox(self):
        """Test sandbox API URL selection."""
        from provider.mercury import MercurySubscriptionConstructor

        mock_runtime = create_mock_runtime()
        constructor = MercurySubscriptionConstructor(runtime=mock_runtime)

        credentials = {"api_environment": "sandbox"}
        url = constructor._get_api_base_url(credentials)

        assert url == "https://api-sandbox.mercury.com/api/v1"

    def test_get_api_base_url_default(self):
        """Test default API URL is sandbox."""
        from provider.mercury import MercurySubscriptionConstructor

        mock_runtime = create_mock_runtime()
        constructor = MercurySubscriptionConstructor(runtime=mock_runtime)

        credentials = {}
        url = constructor._get_api_base_url(credentials)

        assert url == "https://api-sandbox.mercury.com/api/v1"

    def test_get_api_base_url_mock(self):
        """Test mock API URL selection."""
        from provider.mercury import MercurySubscriptionConstructor

        mock_runtime = create_mock_runtime()
        constructor = MercurySubscriptionConstructor(runtime=mock_runtime)

        credentials = {
            "api_environment": "mock",
            "mock_server_url": "http://192.168.1.100:8765"
        }
        url = constructor._get_api_base_url(credentials)

        assert url == "http://192.168.1.100:8765/api/v1"

    def test_get_api_base_url_mock_with_trailing_slash(self):
        """Test mock API URL with trailing slash."""
        from provider.mercury import MercurySubscriptionConstructor

        mock_runtime = create_mock_runtime()
        constructor = MercurySubscriptionConstructor(runtime=mock_runtime)

        credentials = {
            "api_environment": "mock",
            "mock_server_url": "http://192.168.1.100:8765/"
        }
        url = constructor._get_api_base_url(credentials)

        assert url == "http://192.168.1.100:8765/api/v1"

    def test_get_api_base_url_mock_missing_url(self):
        """Test mock environment without URL raises error."""
        from provider.mercury import MercurySubscriptionConstructor
        from dify_plugin.errors.trigger import TriggerProviderCredentialValidationError

        mock_runtime = create_mock_runtime()
        constructor = MercurySubscriptionConstructor(runtime=mock_runtime)

        credentials = {"api_environment": "mock"}

        with pytest.raises(TriggerProviderCredentialValidationError):
            constructor._get_api_base_url(credentials)


def main():
    """Run tests."""
    import sys
    import os

    # Add plugin directory to path
    plugin_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    sys.path.insert(0, plugin_dir)

    print("=" * 70)
    print("Mercury Trigger Plugin - Unit Tests")
    print("=" * 70)

    # Run pytest
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    main()
