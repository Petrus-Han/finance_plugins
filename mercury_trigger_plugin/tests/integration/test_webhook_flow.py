#!/usr/bin/env python3
"""
Integration tests for Mercury Trigger Plugin

Tests the complete webhook flow with the mock Mercury server:
1. API key validation
2. Webhook subscription creation
3. Event dispatch handling
4. Subscription deletion

Requirements:
- Mock Mercury Server running at http://localhost:8765
- Or use pytest fixtures to start/stop servers
"""

import json
import os
import sys
import time
from typing import Any, Dict, Optional
from unittest.mock import MagicMock, patch

import httpx
import pytest

# Configuration
MOCK_SERVER_URL = os.environ.get("MOCK_MERCURY_URL", "http://localhost:8765")
MOCK_TOKEN = os.environ.get("MOCK_MERCURY_TOKEN", "mock_token_12345")


def is_mock_server_running() -> bool:
    """Check if mock Mercury server is running."""
    try:
        resp = httpx.get(f"{MOCK_SERVER_URL}/", timeout=2)
        return resp.status_code == 200
    except Exception:
        return False


@pytest.fixture(scope="module")
def mock_server_check():
    """Skip tests if mock server is not running."""
    if not is_mock_server_running():
        pytest.skip(
            f"Mock Mercury server not running at {MOCK_SERVER_URL}. "
            "Start it with: python scripts/mock_mercury_server.py"
        )


@pytest.fixture
def credentials() -> Dict[str, Any]:
    """Test credentials for mock server."""
    return {
        "access_token": MOCK_TOKEN,
        "api_environment": "sandbox"  # Will be ignored by mock but needed for plugin
    }


@pytest.fixture
def mock_credentials() -> Dict[str, Any]:
    """Credentials configured to use mock server."""
    return {
        "access_token": MOCK_TOKEN,
        "api_environment": "sandbox"
    }


class TestAPIKeyValidation:
    """Tests for API key validation against mock server."""

    def test_valid_api_key(self, mock_server_check, credentials):
        """Test that valid API key passes validation."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Accept": "application/json"
        }

        resp = httpx.get(f"{MOCK_SERVER_URL}/api/v1/accounts", headers=headers)

        assert resp.status_code == 200
        data = resp.json()
        assert "accounts" in data
        assert len(data["accounts"]) > 0

    def test_invalid_api_key(self, mock_server_check):
        """Test that invalid API key is rejected."""
        headers = {
            "Authorization": "Bearer invalid_token",
            "Accept": "application/json"
        }

        resp = httpx.get(f"{MOCK_SERVER_URL}/api/v1/accounts", headers=headers)

        assert resp.status_code == 401


class TestWebhookSubscription:
    """Tests for webhook subscription management."""

    def test_create_webhook(self, mock_server_check, credentials):
        """Test creating a webhook subscription."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        webhook_data = {
            "url": "http://localhost:8766/webhook/test",
            "eventTypes": ["transaction.created", "transaction.updated"]
        }

        resp = httpx.post(
            f"{MOCK_SERVER_URL}/api/v1/webhooks",
            headers=headers,
            json=webhook_data
        )

        assert resp.status_code == 201
        data = resp.json()

        assert "id" in data
        assert "secret" in data
        assert data["url"] == webhook_data["url"]
        assert data["eventTypes"] == webhook_data["eventTypes"]
        assert data["status"] == "active"

        # Store webhook_id for cleanup
        webhook_id = data["id"]

        # Clean up - delete the webhook
        delete_resp = httpx.delete(
            f"{MOCK_SERVER_URL}/api/v1/webhook/{webhook_id}",
            headers=headers
        )
        assert delete_resp.status_code == 204

    def test_list_webhooks(self, mock_server_check, credentials):
        """Test listing webhook subscriptions."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Accept": "application/json"
        }

        resp = httpx.get(f"{MOCK_SERVER_URL}/api/v1/webhooks", headers=headers)

        assert resp.status_code == 200
        data = resp.json()
        assert "webhooks" in data

    def test_get_webhook_details(self, mock_server_check, credentials):
        """Test getting webhook details."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # First create a webhook
        webhook_data = {
            "url": "http://localhost:8766/webhook/details-test",
            "eventTypes": ["transaction.created"]
        }

        create_resp = httpx.post(
            f"{MOCK_SERVER_URL}/api/v1/webhooks",
            headers=headers,
            json=webhook_data
        )
        assert create_resp.status_code == 201
        webhook_id = create_resp.json()["id"]

        # Get webhook details
        get_resp = httpx.get(
            f"{MOCK_SERVER_URL}/api/v1/webhook/{webhook_id}",
            headers=headers
        )

        assert get_resp.status_code == 200
        data = get_resp.json()
        assert data["id"] == webhook_id
        # Secret should NOT be returned on GET
        assert "secret" not in data

        # Cleanup
        httpx.delete(f"{MOCK_SERVER_URL}/api/v1/webhook/{webhook_id}", headers=headers)

    def test_delete_webhook(self, mock_server_check, credentials):
        """Test deleting a webhook subscription."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Create a webhook
        webhook_data = {
            "url": "http://localhost:8766/webhook/delete-test",
            "eventTypes": ["transaction.created"]
        }

        create_resp = httpx.post(
            f"{MOCK_SERVER_URL}/api/v1/webhooks",
            headers=headers,
            json=webhook_data
        )
        webhook_id = create_resp.json()["id"]

        # Delete the webhook
        delete_resp = httpx.delete(
            f"{MOCK_SERVER_URL}/api/v1/webhook/{webhook_id}",
            headers=headers
        )

        assert delete_resp.status_code == 204

        # Verify it's deleted
        get_resp = httpx.get(
            f"{MOCK_SERVER_URL}/api/v1/webhook/{webhook_id}",
            headers=headers
        )
        assert get_resp.status_code == 404

    def test_delete_nonexistent_webhook(self, mock_server_check, credentials):
        """Test deleting a webhook that doesn't exist."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Accept": "application/json"
        }

        resp = httpx.delete(
            f"{MOCK_SERVER_URL}/api/v1/webhook/nonexistent_id",
            headers=headers
        )

        assert resp.status_code == 404


class TestEventSimulation:
    """Tests for event simulation with mock server."""

    def test_simulate_transaction_created(self, mock_server_check, credentials):
        """Test simulating a transaction.created event."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Content-Type": "application/json"
        }

        # First create a webhook (events need a destination)
        webhook_resp = httpx.post(
            f"{MOCK_SERVER_URL}/api/v1/webhooks",
            headers=headers,
            json={
                "url": "http://localhost:8766/webhook/sim-test",
                "eventTypes": ["transaction.created"]
            }
        )
        webhook_id = webhook_resp.json()["id"]

        # Simulate transaction event
        sim_resp = httpx.post(
            f"{MOCK_SERVER_URL}/simulate/transaction",
            json={
                "amount": -250.00,
                "counterparty": "Integration Test Vendor"
            }
        )

        assert sim_resp.status_code == 200
        data = sim_resp.json()

        assert "event_id" in data
        assert "transaction_id" in data
        assert "payload" in data
        assert data["payload"]["resourceType"] == "transaction"
        assert data["payload"]["operationType"] == "created"

        # Cleanup
        httpx.delete(f"{MOCK_SERVER_URL}/api/v1/webhook/{webhook_id}", headers=headers)

    def test_simulate_transaction_updated(self, mock_server_check, credentials):
        """Test simulating a transaction.updated event."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Content-Type": "application/json"
        }

        # Create webhook
        webhook_resp = httpx.post(
            f"{MOCK_SERVER_URL}/api/v1/webhooks",
            headers=headers,
            json={
                "url": "http://localhost:8766/webhook/update-test",
                "eventTypes": ["transaction.updated"]
            }
        )
        webhook_id = webhook_resp.json()["id"]

        # Simulate update event
        sim_resp = httpx.post(
            f"{MOCK_SERVER_URL}/simulate/transaction/update",
            json={
                "amount": -300.00,
                "status": "sent"
            }
        )

        assert sim_resp.status_code == 200
        data = sim_resp.json()

        assert data["payload"]["operationType"] == "updated"
        assert data["payload"]["mergePatch"]["status"] == "sent"

        # Cleanup
        httpx.delete(f"{MOCK_SERVER_URL}/api/v1/webhook/{webhook_id}", headers=headers)


class TestMercuryAPIEndpoints:
    """Tests for Mercury API endpoints on mock server."""

    def test_get_accounts(self, mock_server_check, credentials):
        """Test getting accounts list."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Accept": "application/json"
        }

        resp = httpx.get(f"{MOCK_SERVER_URL}/api/v1/accounts", headers=headers)

        assert resp.status_code == 200
        data = resp.json()
        assert "accounts" in data
        assert len(data["accounts"]) >= 1

        # Verify account structure
        account = data["accounts"][0]
        assert "id" in account
        assert "name" in account
        assert "currentBalance" in account

    def test_get_account_details(self, mock_server_check, credentials):
        """Test getting single account details."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Accept": "application/json"
        }

        # First get accounts list to get an ID
        accounts_resp = httpx.get(f"{MOCK_SERVER_URL}/api/v1/accounts", headers=headers)
        account_id = accounts_resp.json()["accounts"][0]["id"]

        # Get account details
        resp = httpx.get(f"{MOCK_SERVER_URL}/api/v1/account/{account_id}", headers=headers)

        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == account_id

    def test_get_account_transactions(self, mock_server_check, credentials):
        """Test getting account transactions."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Accept": "application/json"
        }

        # Get an account ID
        accounts_resp = httpx.get(f"{MOCK_SERVER_URL}/api/v1/accounts", headers=headers)
        account_id = accounts_resp.json()["accounts"][0]["id"]

        # Get transactions
        resp = httpx.get(
            f"{MOCK_SERVER_URL}/api/v1/account/{account_id}/transactions",
            headers=headers
        )

        assert resp.status_code == 200
        data = resp.json()
        assert "transactions" in data

    def test_get_recipients(self, mock_server_check, credentials):
        """Test getting recipients list."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Accept": "application/json"
        }

        resp = httpx.get(f"{MOCK_SERVER_URL}/api/v1/recipients", headers=headers)

        assert resp.status_code == 200
        data = resp.json()
        assert "recipients" in data

    def test_get_categories(self, mock_server_check, credentials):
        """Test getting categories list."""
        headers = {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Accept": "application/json"
        }

        resp = httpx.get(f"{MOCK_SERVER_URL}/api/v1/categories", headers=headers)

        assert resp.status_code == 200
        data = resp.json()
        assert "categories" in data


def main():
    """Run integration tests."""
    print("=" * 70)
    print("Mercury Trigger Plugin - Integration Tests")
    print("=" * 70)
    print(f"\nMock Server URL: {MOCK_SERVER_URL}")
    print(f"Mock Token: {MOCK_TOKEN}")
    print()

    if not is_mock_server_running():
        print("ERROR: Mock Mercury server is not running!")
        print("Start it with: python scripts/mock_mercury_server.py")
        return 1

    print("Mock server is running. Starting tests...\n")

    # Run pytest
    pytest.main([__file__, "-v", "--tb=short"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
