"""
Unit tests for Mercury Trigger webhook security.

These tests ensure that critical security validations are never accidentally removed.
"""

import hashlib
import hmac
import json
import time
from unittest.mock import MagicMock, patch

import pytest

# We need to mock dify_plugin modules before importing MercuryTrigger
# since they may not be available in the test environment


@pytest.fixture(autouse=True)
def mock_dify_plugin():
    """Mock dify_plugin modules for testing."""
    # Create mock classes
    class MockSubscription:
        def __init__(self, properties=None, endpoint="", parameters=None):
            self.properties = properties or {}
            self.endpoint = endpoint
            self.parameters = parameters or {}

    class MockEventDispatch:
        def __init__(self, events=None, response=None):
            self.events = events or []
            self.response = response

    class MockTriggerValidationError(Exception):
        pass

    class MockTrigger:
        pass

    # Create mock modules
    mock_entities_trigger = MagicMock()
    mock_entities_trigger.Subscription = MockSubscription
    mock_entities_trigger.EventDispatch = MockEventDispatch

    mock_errors_trigger = MagicMock()
    mock_errors_trigger.TriggerValidationError = MockTriggerValidationError

    mock_interfaces_trigger = MagicMock()
    mock_interfaces_trigger.Trigger = MockTrigger

    with patch.dict('sys.modules', {
        'dify_plugin': MagicMock(),
        'dify_plugin.entities': MagicMock(),
        'dify_plugin.entities.oauth': MagicMock(),
        'dify_plugin.entities.provider_config': MagicMock(),
        'dify_plugin.entities.trigger': mock_entities_trigger,
        'dify_plugin.errors': MagicMock(),
        'dify_plugin.errors.trigger': mock_errors_trigger,
        'dify_plugin.interfaces': MagicMock(),
        'dify_plugin.interfaces.trigger': mock_interfaces_trigger,
    }):
        # Store references for use in tests
        pytest.MockSubscription = MockSubscription
        pytest.MockTriggerValidationError = MockTriggerValidationError
        yield


class TestMercuryTriggerWebhookSecurity:
    """Test suite for Mercury webhook security validations.

    CRITICAL: These tests protect against accidental removal of security checks.
    """

    def test_dispatch_event_raises_error_when_webhook_secret_missing(self, mock_dify_plugin):
        """
        SECURITY TEST: Verify that _dispatch_event raises TriggerValidationError
        when webhook_secret is not configured.

        This test ensures that:
        1. Requests cannot be processed without signature verification
        2. The security check is not accidentally removed in future changes
        """
        # Import after mocking
        import sys
        sys.path.insert(0, '/home/ubuntu/playground/finance_plugins/mercury_trigger_plugin')

        from provider.mercury import MercuryTrigger

        # Create trigger instance
        trigger = MercuryTrigger()

        # Create subscription WITHOUT webhook_secret
        subscription = pytest.MockSubscription(
            properties={},  # No webhook_secret
            endpoint="https://example.com/webhook"
        )

        # Create mock request
        mock_request = MagicMock()
        mock_request.get_data.return_value = b'{"resourceType": "transaction"}'
        mock_request.get_json.return_value = {"resourceType": "transaction"}
        mock_request.headers = {}

        # Verify that TriggerValidationError is raised
        with pytest.raises(pytest.MockTriggerValidationError) as exc_info:
            trigger._dispatch_event(subscription, mock_request)

        # Verify error message mentions authentication/security
        error_message = str(exc_info.value)
        assert "secret" in error_message.lower() or "authenticity" in error_message.lower()

    def test_dispatch_event_raises_error_when_webhook_secret_is_none(self, mock_dify_plugin):
        """
        SECURITY TEST: Verify behavior when webhook_secret is explicitly None.
        """
        import sys
        sys.path.insert(0, '/home/ubuntu/playground/finance_plugins/mercury_trigger_plugin')

        from provider.mercury import MercuryTrigger

        trigger = MercuryTrigger()

        subscription = pytest.MockSubscription(
            properties={"webhook_secret": None},
            endpoint="https://example.com/webhook"
        )

        mock_request = MagicMock()
        mock_request.get_data.return_value = b'{"resourceType": "transaction"}'
        mock_request.headers = {}

        with pytest.raises(pytest.MockTriggerValidationError):
            trigger._dispatch_event(subscription, mock_request)

    def test_dispatch_event_raises_error_when_webhook_secret_is_empty_string(self, mock_dify_plugin):
        """
        SECURITY TEST: Verify behavior when webhook_secret is empty string.
        """
        import sys
        sys.path.insert(0, '/home/ubuntu/playground/finance_plugins/mercury_trigger_plugin')

        from provider.mercury import MercuryTrigger

        trigger = MercuryTrigger()

        subscription = pytest.MockSubscription(
            properties={"webhook_secret": ""},
            endpoint="https://example.com/webhook"
        )

        mock_request = MagicMock()
        mock_request.get_data.return_value = b'{"resourceType": "transaction"}'
        mock_request.headers = {}

        with pytest.raises(pytest.MockTriggerValidationError):
            trigger._dispatch_event(subscription, mock_request)

    def test_dispatch_event_validates_signature_when_secret_present(self, mock_dify_plugin):
        """
        SECURITY TEST: Verify that signature validation is called when secret is present.
        """
        import sys
        sys.path.insert(0, '/home/ubuntu/playground/finance_plugins/mercury_trigger_plugin')

        from provider.mercury import MercuryTrigger

        trigger = MercuryTrigger()

        # Create subscription WITH webhook_secret
        webhook_secret = "test_secret_123"
        subscription = pytest.MockSubscription(
            properties={"webhook_secret": webhook_secret},
            endpoint="https://example.com/webhook"
        )

        # Create mock request WITHOUT signature (should fail signature validation)
        mock_request = MagicMock()
        mock_request.get_data.return_value = b'{"resourceType": "transaction"}'
        mock_headers = MagicMock()
        mock_headers.get.return_value = None  # Missing Mercury-Signature header
        mock_request.headers = mock_headers

        # Should raise error due to missing signature header
        with pytest.raises(pytest.MockTriggerValidationError) as exc_info:
            trigger._dispatch_event(subscription, mock_request)

        # Error should be about missing signature, not missing secret
        error_message = str(exc_info.value)
        assert "signature" in error_message.lower() or "Mercury-Signature" in error_message

    def test_dispatch_event_rejects_invalid_signature(self, mock_dify_plugin):
        """
        SECURITY TEST: Verify that invalid signatures are rejected.
        """
        import sys
        sys.path.insert(0, '/home/ubuntu/playground/finance_plugins/mercury_trigger_plugin')

        from provider.mercury import MercuryTrigger

        trigger = MercuryTrigger()

        webhook_secret = "test_secret_123"
        subscription = pytest.MockSubscription(
            properties={"webhook_secret": webhook_secret},
            endpoint="https://example.com/webhook"
        )

        # Create request with invalid signature
        timestamp = str(int(time.time()))
        mock_request = MagicMock()
        mock_request.get_data.return_value = b'{"resourceType": "transaction"}'
        mock_headers = MagicMock()
        mock_headers.get.return_value = f"t={timestamp},v1=invalid_signature"
        mock_request.headers = mock_headers

        with pytest.raises(pytest.MockTriggerValidationError):
            trigger._dispatch_event(subscription, mock_request)

    def test_dispatch_event_rejects_expired_timestamp(self, mock_dify_plugin):
        """
        SECURITY TEST: Verify that requests with expired timestamps are rejected
        to prevent replay attacks.
        """
        import sys
        sys.path.insert(0, '/home/ubuntu/playground/finance_plugins/mercury_trigger_plugin')

        from provider.mercury import MercuryTrigger

        trigger = MercuryTrigger()

        webhook_secret = "test_secret_123"
        subscription = pytest.MockSubscription(
            properties={"webhook_secret": webhook_secret},
            endpoint="https://example.com/webhook"
        )

        # Create request with expired timestamp (10 minutes ago)
        expired_timestamp = str(int(time.time()) - 600)
        body = '{"resourceType": "transaction"}'
        signed_payload = f"{expired_timestamp}.{body}"
        signature = hmac.new(
            webhook_secret.encode(),
            signed_payload.encode(),
            hashlib.sha256
        ).hexdigest()

        mock_request = MagicMock()
        # get_data(as_text=True) returns string, get_data() returns bytes
        mock_request.get_data.return_value = body
        mock_headers = MagicMock()
        mock_headers.get.return_value = f"t={expired_timestamp},v1={signature}"
        mock_request.headers = mock_headers

        with pytest.raises(pytest.MockTriggerValidationError) as exc_info:
            trigger._dispatch_event(subscription, mock_request)

        error_message = str(exc_info.value)
        assert "timestamp" in error_message.lower() or "expired" in error_message.lower()

    def test_dispatch_event_accepts_valid_signature(self, mock_dify_plugin):
        """
        SECURITY TEST: Verify that valid signatures are accepted and processed.
        """
        import sys
        sys.path.insert(0, '/home/ubuntu/playground/finance_plugins/mercury_trigger_plugin')

        from provider.mercury import MercuryTrigger

        trigger = MercuryTrigger()

        webhook_secret = "test_secret_123"
        subscription = pytest.MockSubscription(
            properties={"webhook_secret": webhook_secret},
            endpoint="https://example.com/webhook"
        )

        # Create request with valid signature
        timestamp = str(int(time.time()))
        body = '{"resourceType": "transaction"}'
        signed_payload = f"{timestamp}.{body}"
        signature = hmac.new(
            webhook_secret.encode(),
            signed_payload.encode(),
            hashlib.sha256
        ).hexdigest()

        mock_request = MagicMock()
        # get_data(as_text=True) returns string
        mock_request.get_data.return_value = body
        mock_request.get_json.return_value = {"resourceType": "transaction"}
        mock_headers = MagicMock()
        mock_headers.get.return_value = f"t={timestamp},v1={signature}"
        mock_request.headers = mock_headers

        # Should not raise - valid signature should be accepted
        result = trigger._dispatch_event(subscription, mock_request)

        # Verify the result
        assert result is not None
        assert hasattr(result, 'events')
        assert "transaction" in result.events
