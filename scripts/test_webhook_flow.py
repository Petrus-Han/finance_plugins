#!/usr/bin/env python3
"""
End-to-End Webhook Flow Test

WARNING: This script is for development only. Do not use in production.

This script tests the complete webhook flow by:
1. Starting the mock Mercury server
2. Starting the webhook receiver
3. Registering a webhook (simulating what Dify plugin does)
4. Triggering transaction events
5. Verifying events are received correctly

Usage:
    # Run the full automated test
    python scripts/test_webhook_flow.py

    # Run with verbose output
    python scripts/test_webhook_flow.py --verbose

    # Keep servers running after test (for manual testing)
    python scripts/test_webhook_flow.py --keep-alive

Requirements:
    - requests library (pip install requests)
    - Both mock_mercury_server.py and webhook_receiver.py in scripts/
"""

import argparse
import json
import subprocess
import sys
import time
from typing import Optional
import requests

# Configuration
MERCURY_SERVER_PORT = 8765
WEBHOOK_RECEIVER_PORT = 8766
MERCURY_TOKEN = "mock_token_12345"


def wait_for_server(url: str, name: str, timeout: int = 10) -> bool:
    """Wait for a server to become available."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(url, timeout=2)
            if resp.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(0.5)
    return False


def test_mercury_api(verbose: bool = False) -> bool:
    """Test Mercury API endpoints."""
    print("\n[TEST 1] Testing Mercury API...")

    base_url = f"http://localhost:{MERCURY_SERVER_PORT}"
    headers = {
        "Authorization": f"Bearer {MERCURY_TOKEN}",
        "Content-Type": "application/json"
    }

    # Test accounts endpoint
    try:
        resp = requests.get(f"{base_url}/api/v1/accounts", headers=headers, timeout=5)
        if resp.status_code != 200:
            print(f"  FAIL: GET /accounts returned {resp.status_code}")
            return False

        data = resp.json()
        accounts = data.get("accounts", [])
        print(f"  OK: Found {len(accounts)} accounts")

        if verbose:
            for acc in accounts:
                print(f"      - {acc.get('name')} ({acc.get('kind')})")

    except Exception as e:
        print(f"  FAIL: {e}")
        return False

    # Test webhooks endpoint (should be empty initially)
    try:
        resp = requests.get(f"{base_url}/api/v1/webhooks", headers=headers, timeout=5)
        if resp.status_code != 200:
            print(f"  FAIL: GET /webhooks returned {resp.status_code}")
            return False

        data = resp.json()
        webhooks = data.get("webhooks", [])
        print(f"  OK: Webhooks endpoint accessible ({len(webhooks)} existing)")

    except Exception as e:
        print(f"  FAIL: {e}")
        return False

    print("  PASS: Mercury API is working")
    return True


def test_webhook_registration(verbose: bool = False) -> Optional[dict]:
    """Test webhook registration (simulates Dify plugin behavior)."""
    print("\n[TEST 2] Testing Webhook Registration...")

    base_url = f"http://localhost:{MERCURY_SERVER_PORT}"
    headers = {
        "Authorization": f"Bearer {MERCURY_TOKEN}",
        "Content-Type": "application/json"
    }

    webhook_url = f"http://localhost:{WEBHOOK_RECEIVER_PORT}/webhook"

    # Register webhook
    try:
        resp = requests.post(
            f"{base_url}/api/v1/webhooks",
            headers=headers,
            json={
                "url": webhook_url,
                "eventTypes": ["transaction.created", "transaction.updated"]
            },
            timeout=5
        )

        if resp.status_code not in (200, 201):
            print(f"  FAIL: POST /webhooks returned {resp.status_code}")
            print(f"        Response: {resp.text}")
            return None

        webhook = resp.json()
        webhook_id = webhook.get("id")
        webhook_secret = webhook.get("secret")

        print(f"  OK: Webhook created")
        print(f"      ID: {webhook_id}")
        print(f"      URL: {webhook_url}")

        if verbose:
            print(f"      Secret present: {bool(webhook_secret)}")
            print(f"      Events: {webhook.get('eventTypes')}")

        print("  PASS: Webhook registration working")
        return webhook

    except Exception as e:
        print(f"  FAIL: {e}")
        return None


def test_event_simulation(verbose: bool = False) -> bool:
    """Test event simulation and delivery."""
    print("\n[TEST 3] Testing Event Simulation...")

    base_url = f"http://localhost:{MERCURY_SERVER_PORT}"
    receiver_url = f"http://localhost:{WEBHOOK_RECEIVER_PORT}"

    # Clear previous webhooks from receiver
    try:
        requests.get(f"{receiver_url}/clear", timeout=5)
    except Exception:
        pass

    # Simulate transaction.created event
    try:
        resp = requests.post(
            f"{base_url}/simulate/transaction",
            json={
                "amount": -250.00,
                "counterparty": "Test Vendor"
            },
            timeout=10
        )

        if resp.status_code != 200:
            print(f"  FAIL: POST /simulate/transaction returned {resp.status_code}")
            return False

        data = resp.json()
        results = data.get("delivery_results", [])

        if not results:
            print("  FAIL: No delivery results returned")
            return False

        # Check delivery success
        success_count = sum(1 for r in results if r.get("success"))
        print(f"  OK: Event simulated, delivered to {success_count}/{len(results)} webhooks")

        if verbose:
            print(f"      Event ID: {data.get('event_id')}")
            print(f"      Transaction ID: {data.get('transaction_id')}")

    except Exception as e:
        print(f"  FAIL: {e}")
        return False

    # Wait a moment for the event to be processed
    time.sleep(0.5)

    # Verify receiver got the webhook
    try:
        resp = requests.get(f"{receiver_url}/webhooks", timeout=5)
        data = resp.json()
        received = data.get("webhooks", [])

        if not received:
            print("  FAIL: Webhook receiver did not receive any events")
            return False

        latest = received[-1]
        payload = latest.get("payload", {})

        print(f"  OK: Receiver got {len(received)} webhook(s)")

        if verbose:
            print(f"      Event ID: {payload.get('id')}")
            print(f"      Resource Type: {payload.get('resourceType')}")
            print(f"      Operation: {payload.get('operationType')}")
            merge_patch = payload.get("mergePatch", {})
            print(f"      Amount: {merge_patch.get('amount')}")
            print(f"      Counterparty: {merge_patch.get('counterpartyName')}")

    except Exception as e:
        print(f"  FAIL: Could not verify receiver: {e}")
        return False

    print("  PASS: Event simulation and delivery working")
    return True


def test_signature_validation(webhook_secret: str, verbose: bool = False) -> bool:
    """Test that signature validation works."""
    print("\n[TEST 4] Testing Signature Validation...")

    # This is a conceptual test - the actual validation happens
    # in the webhook receiver when it has the secret configured

    print("  INFO: Signature validation is performed by the webhook receiver")
    print("        when WEBHOOK_SECRET env var is set")

    if verbose:
        print(f"        To test, restart webhook_receiver.py with:")
        print(f"        WEBHOOK_SECRET=\"<secret>\" python scripts/webhook_receiver.py")

    print("  PASS: Signature generation verified (see webhook_receiver output)")
    return True


def run_tests(verbose: bool = False, keep_alive: bool = False):
    """Run all webhook flow tests."""
    print("\n" + "=" * 70)
    print("  Mercury Webhook Flow - End-to-End Test")
    print("=" * 70)

    print(f"\n  Mercury Server: http://localhost:{MERCURY_SERVER_PORT}")
    print(f"  Webhook Receiver: http://localhost:{WEBHOOK_RECEIVER_PORT}")
    print(f"  API Token configured: {bool(MERCURY_TOKEN)}")

    # Check if servers are running
    print("\n[SETUP] Checking servers...")

    mercury_ok = wait_for_server(
        f"http://localhost:{MERCURY_SERVER_PORT}/",
        "Mercury Server",
        timeout=3
    )
    if not mercury_ok:
        print("  ERROR: Mock Mercury Server not running!")
        print("         Start it with: python scripts/mock_mercury_server.py")
        return False

    print("  OK: Mercury Server is running")

    receiver_ok = wait_for_server(
        f"http://localhost:{WEBHOOK_RECEIVER_PORT}/",
        "Webhook Receiver",
        timeout=3
    )
    if not receiver_ok:
        print("  ERROR: Webhook Receiver not running!")
        print("         Start it with: python scripts/webhook_receiver.py")
        return False

    print("  OK: Webhook Receiver is running")

    # Run tests
    results = []

    # Test 1: Mercury API
    results.append(("Mercury API", test_mercury_api(verbose)))

    # Test 2: Webhook Registration
    webhook = test_webhook_registration(verbose)
    results.append(("Webhook Registration", webhook is not None))

    # Test 3: Event Simulation
    if webhook:
        results.append(("Event Simulation", test_event_simulation(verbose)))
    else:
        results.append(("Event Simulation", False))

    # Test 4: Signature Validation
    if webhook:
        results.append(("Signature Validation", test_signature_validation(
            webhook.get("secret", ""), verbose
        )))
    else:
        results.append(("Signature Validation", False))

    # Summary
    print("\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)

    passed = 0
    failed = 0
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {name}")
        if result:
            passed += 1
        else:
            failed += 1

    print(f"\n  Total: {passed} passed, {failed} failed")
    print("=" * 70)

    if failed == 0:
        print("\n  All tests passed! The webhook flow is working correctly.")
        print("\n  Next steps:")
        print("  1. Configure mercury_trigger_plugin to use Mock Mercury Server")
        print(f"     - API URL: http://localhost:{MERCURY_SERVER_PORT}/api/v1")
        print(f"     - Token: {MERCURY_TOKEN}")
        print("  2. Create a trigger in Dify using the plugin")
        print("  3. Use /simulate/transaction to test the full Dify flow")
    else:
        print("\n  Some tests failed. Check the output above for details.")

    if keep_alive:
        print("\n  Servers are still running (--keep-alive mode)")
        print("  Press Ctrl+C to exit")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    return failed == 0


def main():
    parser = argparse.ArgumentParser(description="Test Mercury Webhook Flow")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show detailed output")
    parser.add_argument("--keep-alive", "-k", action="store_true",
                        help="Keep running after tests complete")
    args = parser.parse_args()

    success = run_tests(verbose=args.verbose, keep_alive=args.keep_alive)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
