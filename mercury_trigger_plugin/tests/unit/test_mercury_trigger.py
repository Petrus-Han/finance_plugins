#!/usr/bin/env python3
"""Unit tests for Mercury Trigger Plugin."""

import hashlib
import hmac
import json
import time
from unittest.mock import MagicMock

import pytest


class MockRequest:
    """Mock werkzeug Request object."""

    def __init__(self, data: dict, headers: dict = None, raw_body: str = None):
        self._data = raw_body if raw_body is not None else json.dumps(data)
        self.headers = headers or {}
        self.method = "POST"

    def get_data(self, as_text=False):
        return self._data if as_text else self._data.encode()

    def get_json(self, force=False):
        return json.loads(self._data)


def generate_signature(secret: str, timestamp: int, body: str) -> str:
    """Generate Mercury-style webhook signature."""
    signed_payload = f"{timestamp}.{body}"
    return hmac.new(secret.encode(), signed_payload.encode(), hashlib.sha256).hexdigest()


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

        event = TransactionEvent(runtime=create_mock_runtime())
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
                "type": "externalTransfer",
            },
        }

        request = MockRequest(payload)
        result = event._on_event(request, {}, payload)

        assert result.variables["event_id"] == "evt_test_001"
        assert result.variables["transaction_id"] == "txn_test_001"
        assert result.variables["operation_type"] == "created"
        assert result.variables["account_id"] == "acc_test_001"
        assert result.variables["amount"] == -150.00
        assert result.variables["status"] == "pending"
        assert result.variables["counterparty_name"] == "Test Vendor"

    def test_on_event_filter_created_passes(self):
        """Test created filter passes created events."""
        from events.transaction import TransactionEvent

        event = TransactionEvent(runtime=create_mock_runtime())
        payload = {
            "id": "evt_test",
            "operationType": "created",
            "resourceId": "txn_test",
            "mergePatch": {"accountId": "acc_001", "amount": -100},
        }

        request = MockRequest(payload)
        result = event._on_event(request, {"operation_filter": "created"}, payload)
        assert result.variables["operation_type"] == "created"

    def test_on_event_filter_created_ignores_updated(self):
        """Test created filter ignores updated events."""
        from events.transaction import TransactionEvent
        from dify_plugin.errors.trigger import EventIgnoreError

        event = TransactionEvent(runtime=create_mock_runtime())
        payload = {
            "id": "evt_test",
            "operationType": "updated",
            "resourceId": "txn_test",
            "mergePatch": {"accountId": "acc_001", "amount": -100},
        }

        request = MockRequest(payload)
        with pytest.raises(EventIgnoreError):
            event._on_event(request, {"operation_filter": "created"}, payload)

    def test_on_event_filter_updated_ignores_created(self):
        """Test updated filter ignores created events."""
        from events.transaction import TransactionEvent
        from dify_plugin.errors.trigger import EventIgnoreError

        event = TransactionEvent(runtime=create_mock_runtime())
        payload = {
            "id": "evt_test",
            "operationType": "created",
            "resourceId": "txn_test",
            "mergePatch": {"accountId": "acc_001", "amount": -100},
        }

        request = MockRequest(payload)
        with pytest.raises(EventIgnoreError):
            event._on_event(request, {"operation_filter": "updated"}, payload)

    def test_on_event_filter_all_passes_both(self):
        """Test all filter passes both created and updated events."""
        from events.transaction import TransactionEvent

        event = TransactionEvent(runtime=create_mock_runtime())
        for op_type in ["created", "updated"]:
            payload = {
                "id": f"evt_{op_type}",
                "operationType": op_type,
                "resourceId": f"txn_{op_type}",
                "mergePatch": {"accountId": "acc_001", "amount": -100},
            }
            request = MockRequest(payload)
            result = event._on_event(request, {"operation_filter": "all"}, payload)
            assert result.variables["operation_type"] == op_type

    def test_on_event_empty_merge_patch(self):
        """Test handling of events with empty mergePatch."""
        from events.transaction import TransactionEvent

        event = TransactionEvent(runtime=create_mock_runtime())
        payload = {
            "id": "evt_empty",
            "operationType": "created",
            "resourceId": "txn_empty",
            "mergePatch": {},
        }

        request = MockRequest(payload)
        result = event._on_event(request, {}, payload)

        assert result.variables["event_id"] == "evt_empty"
        assert result.variables["account_id"] == ""
        assert result.variables["amount"] is None


class TestSignatureValidation:
    """Tests for webhook signature validation."""

    def test_valid_signature(self):
        """Test that valid signatures are accepted."""
        from provider.mercury import MercuryTrigger

        trigger = MercuryTrigger(runtime=create_mock_runtime())
        secret = "test_secret_key"
        body = '{"id":"evt_001","resourceType":"transaction"}'
        timestamp = int(time.time())
        signature = generate_signature(secret, timestamp, body)

        request = MockRequest(
            data={}, headers={"Mercury-Signature": f"t={timestamp},v1={signature}"}, raw_body=body
        )
        trigger._validate_signature(request, secret)  # Should not raise

    def test_invalid_signature(self):
        """Test that invalid signatures are rejected."""
        from provider.mercury import MercuryTrigger
        from dify_plugin.errors.trigger import TriggerValidationError

        trigger = MercuryTrigger(runtime=create_mock_runtime())
        timestamp = int(time.time())

        request = MockRequest(
            {"id": "evt_001"}, headers={"Mercury-Signature": f"t={timestamp},v1=invalid_signature"}
        )

        with pytest.raises(TriggerValidationError, match="Invalid webhook signature"):
            trigger._validate_signature(request, "secret")

    def test_missing_signature_header(self):
        """Test that missing signature header is rejected."""
        from provider.mercury import MercuryTrigger
        from dify_plugin.errors.trigger import TriggerValidationError

        trigger = MercuryTrigger(runtime=create_mock_runtime())
        request = MockRequest({"id": "evt_001"}, headers={})

        with pytest.raises(TriggerValidationError, match="Missing Mercury-Signature header"):
            trigger._validate_signature(request, "secret")


class TestPayloadParsing:
    """Tests for webhook payload parsing."""

    def test_parse_valid_payload(self):
        """Test parsing valid JSON payload."""
        from provider.mercury import MercuryTrigger

        trigger = MercuryTrigger(runtime=create_mock_runtime())
        payload = {"id": "evt_001", "resourceType": "transaction"}

        request = MockRequest(payload)
        result = trigger._validate_payload(request)

        assert result["id"] == "evt_001"
        assert result["resourceType"] == "transaction"

    def test_parse_empty_payload(self):
        """Test parsing empty payload raises error."""
        from provider.mercury import MercuryTrigger
        from dify_plugin.errors.trigger import TriggerDispatchError

        trigger = MercuryTrigger(runtime=create_mock_runtime())
        request = MockRequest({})

        with pytest.raises(TriggerDispatchError, match="Empty request body"):
            trigger._validate_payload(request)


class TestEventTypeResolution:
    """Tests for event type resolution."""

    def test_resolve_transaction_event(self):
        """Test resolving transaction event type."""
        from provider.mercury import MercuryTrigger

        trigger = MercuryTrigger(runtime=create_mock_runtime())
        result = trigger._resolve_event_types({"resourceType": "transaction"})
        assert "transaction" in result

    def test_resolve_unknown_resource_type(self):
        """Test resolving unknown resource type defaults to transaction."""
        from provider.mercury import MercuryTrigger

        trigger = MercuryTrigger(runtime=create_mock_runtime())
        result = trigger._resolve_event_types({"resourceType": "unknown"})
        assert "transaction" in result


class TestSubscriptionConstructor:
    """Tests for MercurySubscriptionConstructor."""

    def test_get_api_base_url_production(self):
        """Test production API URL selection."""
        from provider.mercury import MercurySubscriptionConstructor

        constructor = MercurySubscriptionConstructor(runtime=create_mock_runtime())
        url = constructor._get_api_base_url({"api_environment": "production"})
        assert url == "https://api.mercury.com/api/v1"

    def test_get_api_base_url_sandbox(self):
        """Test sandbox API URL selection."""
        from provider.mercury import MercurySubscriptionConstructor

        constructor = MercurySubscriptionConstructor(runtime=create_mock_runtime())
        url = constructor._get_api_base_url({"api_environment": "sandbox"})
        assert url == "https://api-sandbox.mercury.com/api/v1"

    def test_get_api_base_url_default(self):
        """Test default API URL is sandbox."""
        from provider.mercury import MercurySubscriptionConstructor

        constructor = MercurySubscriptionConstructor(runtime=create_mock_runtime())
        url = constructor._get_api_base_url({})
        assert url == "https://api-sandbox.mercury.com/api/v1"

    def test_get_api_base_url_mock(self):
        """Test mock API URL selection."""
        from provider.mercury import MercurySubscriptionConstructor

        constructor = MercurySubscriptionConstructor(runtime=create_mock_runtime())
        url = constructor._get_api_base_url(
            {"api_environment": "mock", "mock_server_url": "http://192.168.1.100:8765"}
        )
        assert url == "http://192.168.1.100:8765/api/v1"

    def test_get_api_base_url_mock_missing_url(self):
        """Test mock environment without URL raises error."""
        from provider.mercury import MercurySubscriptionConstructor
        from dify_plugin.errors.trigger import TriggerProviderCredentialValidationError

        constructor = MercurySubscriptionConstructor(runtime=create_mock_runtime())
        with pytest.raises(TriggerProviderCredentialValidationError):
            constructor._get_api_base_url({"api_environment": "mock"})


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
