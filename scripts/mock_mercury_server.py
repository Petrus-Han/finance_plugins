#!/usr/bin/env python3
"""
Mock Mercury Server - Complete Mercury API and Webhook Simulator

This server simulates the Mercury Banking API for local development and testing
of the mercury_trigger_plugin. It implements:

1. Mercury API Endpoints:
   - GET  /api/v1/accounts           - List accounts
   - GET  /api/v1/webhooks           - List webhooks
   - POST /api/v1/webhooks           - Create webhook (returns secret)
   - GET  /api/v1/webhooks/{id}      - Get webhook details
   - DELETE /api/v1/webhooks/{id}    - Delete webhook

2. Webhook Event Simulation:
   - POST /simulate/transaction      - Simulate transaction.created event
   - POST /simulate/transaction/update - Simulate transaction.updated event
   - POST /simulate/custom           - Simulate custom event with JSON body

3. Utility Endpoints:
   - GET  /                          - Status page with usage info
   - GET  /webhooks/list             - List all registered webhooks (no auth)
   - POST /webhooks/clear            - Clear all webhooks (for testing)

Usage:
    # Start the mock server
    python scripts/mock_mercury_server.py

    # Server runs on http://localhost:8765
    # Default API Token: mock_token_12345

    # Register webhook (from Dify plugin or manually)
    curl -X POST http://localhost:8765/api/v1/webhooks \\
      -H "Authorization: Bearer mock_token_12345" \\
      -H "Content-Type: application/json" \\
      -d '{"url": "http://localhost:8766/webhook", "eventTypes": ["transaction.created"]}'

    # Simulate transaction event
    curl -X POST http://localhost:8765/simulate/transaction

    # Simulate with custom amount
    curl -X POST http://localhost:8765/simulate/transaction \\
      -H "Content-Type: application/json" \\
      -d '{"amount": -500.00, "counterparty": "Amazon"}'

Environment Variables:
    MOCK_MERCURY_PORT - Server port (default: 8765)
    MOCK_MERCURY_TOKEN - API token (default: mock_token_12345)
"""

import base64
import hashlib
import hmac
import json
import secrets
import time
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Any, Optional
from urllib.parse import urlparse, parse_qs
import threading
import os

import requests

# Configuration
MOCK_TOKEN = os.environ.get("MOCK_MERCURY_TOKEN", "mock_token_12345")
PORT = int(os.environ.get("MOCK_MERCURY_PORT", "8765"))

# Mock data storage
registered_webhooks: dict[str, dict] = {}  # webhook_id -> webhook_data
mock_transactions: list[dict] = []  # simulated transactions

# Mock accounts (realistic Mercury account structure)
MOCK_ACCOUNTS = [
    {
        "id": "acc_mock_checking_001",
        "name": "Mercury Checking",
        "accountNumber": "****1234",
        "routingNumber": "084106768",
        "kind": "checking",
        "type": "mercury",
        "status": "active",
        "currentBalance": 50000.00,
        "availableBalance": 48000.00,
        "canReceiveTransactions": True,
        "createdAt": "2024-01-15T10:30:00Z"
    },
    {
        "id": "acc_mock_savings_002",
        "name": "Mercury Treasury",
        "accountNumber": "****5678",
        "routingNumber": "084106768",
        "kind": "savings",
        "type": "mercury",
        "status": "active",
        "currentBalance": 100000.00,
        "availableBalance": 100000.00,
        "canReceiveTransactions": True,
        "createdAt": "2024-01-15T10:30:00Z"
    }
]


def generate_webhook_secret() -> str:
    """Generate a webhook secret (base64 encoded, like Mercury does)."""
    raw_secret = secrets.token_bytes(32)
    return base64.b64encode(raw_secret).decode()


def generate_signature(secret: str, timestamp: int, body: str) -> str:
    """Generate Mercury-style webhook signature.

    Mercury uses HMAC-SHA256 with the secret base64-decoded.
    The signed payload is: "{timestamp}.{body}"
    """
    try:
        secret_bytes = base64.b64decode(secret)
    except Exception:
        # Fallback to raw encoding if not valid base64
        secret_bytes = secret.encode()

    signed_payload = f"{timestamp}.{body}"
    signature = hmac.new(
        secret_bytes,
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature


def send_webhook(webhook_url: str, secret: str, payload: dict) -> dict:
    """Send a webhook event to the registered URL with proper signature."""
    body = json.dumps(payload, separators=(',', ':'))  # Compact JSON
    timestamp = int(time.time())
    signature = generate_signature(secret, timestamp, body)

    headers = {
        "Content-Type": "application/json",
        "Mercury-Signature": f"t={timestamp},v1={signature}",
        "User-Agent": "Mercury-Webhook/1.0 (Mock)",
        "X-Mercury-Event-Id": payload.get("id", ""),
        "X-Mercury-Webhook-Id": "mock_webhook"
    }

    print(f"\n{'='*60}")
    print(f"[SEND] Webhook to: {webhook_url}")
    print(f"{'='*60}")
    print(f"  Timestamp: {timestamp}")
    print(f"  Signature: t={timestamp},v1={signature[:32]}...")
    print(f"  Payload keys: {list(payload.keys())}")
    print(f"  Event ID: {payload.get('id', 'N/A')}")
    print(f"  Resource Type: {payload.get('resourceType', 'N/A')}")
    print(f"  Operation: {payload.get('operationType', 'N/A')}")

    try:
        resp = requests.post(
            webhook_url,
            headers=headers,
            data=body,
            timeout=30
        )
        result = {
            "success": resp.status_code < 400,
            "status_code": resp.status_code,
            "response": resp.text[:500] if resp.text else ""
        }

        if result["success"]:
            print(f"  Result: SUCCESS ({resp.status_code})")
        else:
            print(f"  Result: FAILED ({resp.status_code})")
            print(f"  Response: {resp.text[:200]}")

        return result

    except requests.exceptions.Timeout:
        print(f"  Result: TIMEOUT")
        return {"success": False, "error": "Request timeout"}
    except requests.exceptions.ConnectionError as e:
        print(f"  Result: CONNECTION ERROR - {e}")
        return {"success": False, "error": f"Connection error: {e}"}
    except Exception as e:
        print(f"  Result: ERROR - {e}")
        return {"success": False, "error": str(e)}


def create_transaction_event(
    operation: str = "created",
    amount: Optional[float] = None,
    counterparty: Optional[str] = None,
    status: Optional[str] = None,
    account_id: Optional[str] = None,
    transaction_type: Optional[str] = None
) -> dict:
    """Create a realistic Mercury transaction webhook event payload."""
    txn_id = f"txn_{secrets.token_hex(12)}"
    event_id = f"evt_{secrets.token_hex(12)}"

    # Default values based on operation
    if amount is None:
        amount = -150.00 if operation == "created" else -150.00

    if counterparty is None:
        counterparty = "Acme Corp"

    if status is None:
        status = "pending" if operation == "created" else "sent"

    if account_id is None:
        account_id = MOCK_ACCOUNTS[0]["id"]

    if transaction_type is None:
        transaction_type = "externalTransfer" if amount < 0 else "internalTransfer"

    # Mercury's JSON Merge Patch format
    merge_patch = {
        "id": txn_id,
        "accountId": account_id,
        "amount": amount,
        "status": status,
        "postedAt": datetime.now(timezone.utc).isoformat(),
        "estimatedDeliveryDate": datetime.now(timezone.utc).isoformat()[:10],
        "counterpartyName": counterparty,
        "counterpartyId": f"cp_{secrets.token_hex(8)}",
        "bankDescription": f"Transfer to {counterparty}",
        "note": "Simulated transaction for testing",
        "mercuryCategory": "transfers",
        "externalMemo": "",
        "kind": "debit" if amount < 0 else "credit",
        "type": transaction_type,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    payload = {
        "id": event_id,
        "resourceType": "transaction",
        "operationType": operation,
        "resourceId": txn_id,
        "mergePatch": merge_patch,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }

    # Store for reference
    mock_transactions.append(payload)

    return payload


class MockMercuryHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Mock Mercury Server."""

    def log_message(self, format, *args):
        """Custom log format."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {args[0]}")

    def _send_json(self, data: dict, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("X-Request-Id", secrets.token_hex(16))
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def _check_auth(self) -> bool:
        """Verify Bearer token authentication."""
        auth = self.headers.get("Authorization", "")
        if auth != f"Bearer {MOCK_TOKEN}":
            self._send_json({
                "error": "unauthorized",
                "message": "Invalid or missing API token"
            }, 401)
            return False
        return True

    def _read_body(self) -> dict:
        """Read and parse JSON body."""
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length).decode()
        try:
            return json.loads(body) if body else {}
        except json.JSONDecodeError:
            return {}

    def do_GET(self):
        """Handle GET requests."""
        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)

        # Status page
        if path == "/" or path == "/status":
            self._send_json({
                "service": "Mock Mercury Server",
                "version": "1.1.0",
                "status": "running",
                "api_token": MOCK_TOKEN,
                "registered_webhooks": len(registered_webhooks),
                "simulated_transactions": len(mock_transactions),
                "endpoints": {
                    "Mercury API": {
                        "GET /api/v1/accounts": "List accounts",
                        "GET /api/v1/account/{id}": "Get account details",
                        "GET /api/v1/account/{id}/transactions": "Get account transactions",
                        "GET /api/v1/recipients": "List recipients",
                        "GET /api/v1/recipient/{id}": "Get recipient details",
                        "GET /api/v1/categories": "List categories",
                        "GET /api/v1/webhooks": "List webhooks",
                        "POST /api/v1/webhooks": "Create webhook",
                        "GET /api/v1/webhook/{id}": "Get webhook (singular)",
                        "DELETE /api/v1/webhook/{id}": "Delete webhook (singular)"
                    },
                    "Simulation": {
                        "POST /simulate/transaction": "Simulate transaction.created",
                        "POST /simulate/transaction/update": "Simulate transaction.updated",
                        "POST /simulate/custom": "Simulate custom event"
                    },
                    "Utility": {
                        "GET /webhooks/list": "List webhooks (no auth)",
                        "POST /webhooks/clear": "Clear all webhooks"
                    }
                }
            })
            return

        # GET /api/v1/accounts
        if path == "/api/v1/accounts":
            if not self._check_auth():
                return
            self._send_json({"accounts": MOCK_ACCOUNTS})
            return

        # GET /api/v1/webhooks
        if path == "/api/v1/webhooks":
            if not self._check_auth():
                return
            # Return webhooks without the secret (like real Mercury)
            webhooks = []
            for wh in registered_webhooks.values():
                wh_copy = dict(wh)
                wh_copy.pop("secret", None)  # Don't return secret on list
                webhooks.append(wh_copy)
            self._send_json({"webhooks": webhooks})
            return

        # GET /api/v1/webhook/{id} (singular - per Mercury spec)
        # Also support /api/v1/webhooks/{id} for backward compatibility
        if path.startswith("/api/v1/webhook/") or path.startswith("/api/v1/webhooks/"):
            if not self._check_auth():
                return
            webhook_id = path.split("/")[-1]
            if webhook_id in registered_webhooks:
                wh_copy = dict(registered_webhooks[webhook_id])
                wh_copy.pop("secret", None)  # Don't return secret
                self._send_json(wh_copy)
            else:
                self._send_json({"error": "not_found", "message": "Webhook not found"}, 404)
            return

        # GET /api/v1/account/{id} - Get single account details
        if path.startswith("/api/v1/account/") and "/transactions" not in path and "/cards" not in path:
            if not self._check_auth():
                return
            account_id = path.split("/")[-1]
            account = next((a for a in MOCK_ACCOUNTS if a["id"] == account_id), None)
            if account:
                self._send_json(account)
            else:
                self._send_json({"error": "not_found", "message": "Account not found"}, 404)
            return

        # GET /api/v1/account/{id}/transactions - Get account transactions
        if "/transactions" in path and path.startswith("/api/v1/account/"):
            if not self._check_auth():
                return
            parts = path.split("/")
            account_id = parts[4] if len(parts) > 4 else None

            # Generate mock transactions for the account
            transactions = [
                {
                    "id": f"txn_mock_{i:03d}",
                    "accountId": account_id,
                    "amount": -150.00 * (i + 1),
                    "status": "posted" if i % 2 == 0 else "pending",
                    "postedAt": f"2026-01-{15-i:02d}T10:30:00Z",
                    "counterpartyName": f"Vendor {i + 1}",
                    "bankDescription": f"Payment to Vendor {i + 1}",
                    "note": "",
                    "mercuryCategory": "transfers",
                    "kind": "debit",
                    "type": "externalTransfer",
                    "createdAt": f"2026-01-{15-i:02d}T10:30:00Z"
                }
                for i in range(5)
            ]
            self._send_json({"transactions": transactions, "total": len(transactions)})
            return

        # GET /api/v1/recipients - List recipients
        if path == "/api/v1/recipients":
            if not self._check_auth():
                return
            recipients = [
                {
                    "id": "rcp_mock_001",
                    "name": "Acme Corp",
                    "status": "active",
                    "paymentMethod": "ach",
                    "accountNumber": "****5678",
                    "routingNumber": "021000021",
                    "createdAt": "2024-06-01T10:00:00Z"
                },
                {
                    "id": "rcp_mock_002",
                    "name": "Test Vendor LLC",
                    "status": "active",
                    "paymentMethod": "wire",
                    "accountNumber": "****9012",
                    "routingNumber": "021000021",
                    "createdAt": "2024-07-15T14:30:00Z"
                }
            ]
            self._send_json({"recipients": recipients})
            return

        # GET /api/v1/recipient/{id} - Get recipient details
        if path.startswith("/api/v1/recipient/"):
            if not self._check_auth():
                return
            recipient_id = path.split("/")[-1]
            if recipient_id == "rcp_mock_001":
                self._send_json({
                    "id": "rcp_mock_001",
                    "name": "Acme Corp",
                    "status": "active",
                    "paymentMethod": "ach",
                    "accountNumber": "123456789",
                    "routingNumber": "021000021",
                    "address": {
                        "address1": "123 Main St",
                        "city": "New York",
                        "state": "NY",
                        "postalCode": "10001"
                    },
                    "createdAt": "2024-06-01T10:00:00Z"
                })
            else:
                self._send_json({"error": "not_found", "message": "Recipient not found"}, 404)
            return

        # GET /api/v1/categories - List categories
        if path == "/api/v1/categories":
            if not self._check_auth():
                return
            categories = [
                {"id": "cat_001", "name": "Software & SaaS", "color": "#3B82F6"},
                {"id": "cat_002", "name": "Marketing", "color": "#10B981"},
                {"id": "cat_003", "name": "Payroll", "color": "#F59E0B"},
                {"id": "cat_004", "name": "Office Supplies", "color": "#EF4444"},
                {"id": "cat_005", "name": "Travel", "color": "#8B5CF6"}
            ]
            self._send_json({"categories": categories})
            return

        # GET /webhooks/list (no auth, for debugging)
        if path == "/webhooks/list":
            self._send_json({
                "webhooks": list(registered_webhooks.values()),
                "count": len(registered_webhooks)
            })
            return

        # GET /transactions (debug)
        if path == "/transactions":
            self._send_json({
                "transactions": mock_transactions[-10:],
                "total": len(mock_transactions)
            })
            return

        self._send_json({"error": "not_found", "message": "Endpoint not found"}, 404)

    def do_POST(self):
        """Handle POST requests."""
        path = urlparse(self.path).path
        data = self._read_body()

        # POST /api/v1/recipients - Create recipient
        if path == "/api/v1/recipients":
            if not self._check_auth():
                return

            name = data.get("name")
            if not name:
                self._send_json({
                    "error": "validation_error",
                    "message": "name is required"
                }, 400)
                return

            recipient_id = f"rcp_{secrets.token_hex(12)}"
            recipient = {
                "id": recipient_id,
                "name": name,
                "status": "active",
                "paymentMethod": data.get("paymentMethod", "ach"),
                "accountNumber": data.get("accountNumber", ""),
                "routingNumber": data.get("routingNumber", ""),
                "address": data.get("address", {}),
                "createdAt": datetime.now(timezone.utc).isoformat()
            }

            print(f"\n{'='*60}")
            print(f"[CREATE] Recipient Created")
            print(f"{'='*60}")
            print(f"  ID: {recipient_id}")
            print(f"  Name: {name}")
            print(f"{'='*60}\n")

            self._send_json(recipient, 201)
            return

        # POST /api/v1/webhooks - Create webhook
        if path == "/api/v1/webhooks":
            if not self._check_auth():
                return

            url = data.get("url")
            if not url:
                self._send_json({
                    "error": "validation_error",
                    "message": "url is required"
                }, 400)
                return

            webhook_id = f"wh_{secrets.token_hex(12)}"
            webhook_secret = generate_webhook_secret()

            webhook = {
                "id": webhook_id,
                "url": url,
                "secret": webhook_secret,  # Only returned on creation!
                "status": "active",
                "eventTypes": data.get("eventTypes", ["transaction.created", "transaction.updated"]),
                "filterPaths": data.get("filterPaths", []),
                "createdAt": datetime.now(timezone.utc).isoformat()
            }
            registered_webhooks[webhook_id] = webhook

            print(f"\n{'='*60}")
            print(f"[CREATE] Webhook Registered")
            print(f"{'='*60}")
            print(f"  ID: {webhook_id}")
            print(f"  URL: {url}")
            print(f"  Events: {webhook['eventTypes']}")
            print(f"  Secret: {webhook_secret[:20]}... (base64)")
            print(f"{'='*60}\n")

            self._send_json(webhook, 201)
            return

        # POST /simulate/transaction - Simulate transaction.created
        if path == "/simulate/transaction":
            if not registered_webhooks:
                self._send_json({
                    "error": "no_webhooks",
                    "message": "No webhooks registered. Create a webhook first."
                }, 400)
                return

            payload = create_transaction_event(
                operation="created",
                amount=data.get("amount"),
                counterparty=data.get("counterparty"),
                status=data.get("status"),
                account_id=data.get("account_id")
            )

            results = []
            for wh in registered_webhooks.values():
                # Check event type filter
                if "transaction.created" not in wh.get("eventTypes", []):
                    continue
                result = send_webhook(wh["url"], wh["secret"], payload)
                results.append({
                    "webhook_id": wh["id"],
                    "webhook_url": wh["url"],
                    **result
                })

            self._send_json({
                "message": "Transaction created event sent",
                "event_id": payload["id"],
                "transaction_id": payload["resourceId"],
                "payload": payload,
                "delivery_results": results
            })
            return

        # POST /simulate/transaction/update - Simulate transaction.updated
        if path == "/simulate/transaction/update":
            if not registered_webhooks:
                self._send_json({
                    "error": "no_webhooks",
                    "message": "No webhooks registered. Create a webhook first."
                }, 400)
                return

            payload = create_transaction_event(
                operation="updated",
                amount=data.get("amount"),
                counterparty=data.get("counterparty"),
                status=data.get("status", "sent"),
                account_id=data.get("account_id")
            )

            results = []
            for wh in registered_webhooks.values():
                if "transaction.updated" not in wh.get("eventTypes", []):
                    continue
                result = send_webhook(wh["url"], wh["secret"], payload)
                results.append({
                    "webhook_id": wh["id"],
                    "webhook_url": wh["url"],
                    **result
                })

            self._send_json({
                "message": "Transaction updated event sent",
                "event_id": payload["id"],
                "transaction_id": payload["resourceId"],
                "payload": payload,
                "delivery_results": results
            })
            return

        # POST /simulate/custom - Send custom event
        if path == "/simulate/custom":
            if not registered_webhooks:
                self._send_json({
                    "error": "no_webhooks",
                    "message": "No webhooks registered."
                }, 400)
                return

            if not data:
                self._send_json({
                    "error": "validation_error",
                    "message": "Request body required with custom event payload"
                }, 400)
                return

            results = []
            for wh in registered_webhooks.values():
                result = send_webhook(wh["url"], wh["secret"], data)
                results.append({
                    "webhook_id": wh["id"],
                    "webhook_url": wh["url"],
                    **result
                })

            self._send_json({
                "message": "Custom event sent",
                "payload": data,
                "delivery_results": results
            })
            return

        # POST /webhooks/clear - Clear all webhooks
        if path == "/webhooks/clear":
            count = len(registered_webhooks)
            registered_webhooks.clear()
            mock_transactions.clear()
            self._send_json({
                "message": f"Cleared {count} webhooks and transaction history"
            })
            return

        # POST /api/v1/account/{id}/request-send-money - Request to send money
        if "/request-send-money" in path and path.startswith("/api/v1/account/"):
            if not self._check_auth():
                return

            parts = path.split("/")
            account_id = parts[4] if len(parts) > 4 else None

            recipient_id = data.get("recipientId")
            amount = data.get("amount")

            if not recipient_id or not amount:
                self._send_json({
                    "error": "validation_error",
                    "message": "recipientId and amount are required"
                }, 400)
                return

            request_id = f"smr_{secrets.token_hex(12)}"
            txn_id = f"txn_{secrets.token_hex(12)}"

            result = {
                "id": request_id,
                "transactionId": txn_id,
                "status": "pending_approval",
                "amount": float(amount),
                "recipientId": recipient_id,
                "accountId": account_id,
                "paymentMethod": data.get("paymentMethod", "ach"),
                "note": data.get("note", ""),
                "externalMemo": data.get("externalMemo", ""),
                "createdAt": datetime.now(timezone.utc).isoformat()
            }

            print(f"\n{'='*60}")
            print(f"[SEND MONEY] Request Created")
            print(f"{'='*60}")
            print(f"  Request ID: {request_id}")
            print(f"  Transaction ID: {txn_id}")
            print(f"  Amount: ${amount}")
            print(f"  Recipient: {recipient_id}")
            print(f"  Status: pending_approval")
            print(f"{'='*60}\n")

            self._send_json(result, 202)
            return

        # POST /api/v1/transfer - Create internal transfer
        if path == "/api/v1/transfer":
            if not self._check_auth():
                return

            from_account_id = data.get("fromAccountId")
            to_account_id = data.get("toAccountId")
            amount = data.get("amount")

            if not from_account_id or not to_account_id or not amount:
                self._send_json({
                    "error": "validation_error",
                    "message": "fromAccountId, toAccountId, and amount are required"
                }, 400)
                return

            if from_account_id == to_account_id:
                self._send_json({
                    "error": "validation_error",
                    "message": "Source and destination accounts must be different"
                }, 400)
                return

            txn_id = f"txn_{secrets.token_hex(12)}"

            result = {
                "id": txn_id,
                "status": "sent",
                "amount": float(amount),
                "fromAccountId": from_account_id,
                "toAccountId": to_account_id,
                "note": data.get("note", ""),
                "kind": "internalTransfer",
                "createdAt": datetime.now(timezone.utc).isoformat()
            }

            print(f"\n{'='*60}")
            print(f"[TRANSFER] Internal Transfer Created")
            print(f"{'='*60}")
            print(f"  Transaction ID: {txn_id}")
            print(f"  Amount: ${amount}")
            print(f"  From: {from_account_id}")
            print(f"  To: {to_account_id}")
            print(f"  Status: sent")
            print(f"{'='*60}\n")

            self._send_json(result, 201)
            return

        self._send_json({"error": "not_found", "message": "Endpoint not found"}, 404)

    def do_DELETE(self):
        """Handle DELETE requests."""
        path = urlparse(self.path).path

        # DELETE /api/v1/webhook/{id} (singular - per Mercury spec)
        # Also support /api/v1/webhooks/{id} for backward compatibility
        if path.startswith("/api/v1/webhook/") or path.startswith("/api/v1/webhooks/"):
            if not self._check_auth():
                return

            webhook_id = path.split("/")[-1]
            if webhook_id in registered_webhooks:
                del registered_webhooks[webhook_id]
                print(f"\n[DELETE] Webhook removed: {webhook_id}\n")
                self.send_response(204)
                self.end_headers()
            else:
                self._send_json({"error": "not_found", "message": "Webhook not found"}, 404)
            return

        # DELETE /api/v1/recipient/{id}
        if path.startswith("/api/v1/recipient/"):
            if not self._check_auth():
                return
            recipient_id = path.split("/")[-1]
            print(f"\n[DELETE] Recipient removed (mock): {recipient_id}\n")
            self.send_response(204)
            self.end_headers()
            return

        self._send_json({"error": "not_found", "message": "Endpoint not found"}, 404)


def print_banner():
    """Print server startup banner."""
    print("\n" + "=" * 70)
    print("  Mock Mercury Server - For Testing mercury_trigger_plugin")
    print("=" * 70)
    print(f"""
  Server Address: http://localhost:{PORT}
  API Token:      {MOCK_TOKEN}

  Mercury API Endpoints:
    Accounts:
      GET  /api/v1/accounts                    List all accounts
      GET  /api/v1/account/{{id}}                Get account details
      GET  /api/v1/account/{{id}}/transactions   Get account transactions

    Recipients:
      GET  /api/v1/recipients                  List all recipients
      GET  /api/v1/recipient/{{id}}              Get recipient details
      POST /api/v1/recipients                  Create recipient
      DELETE /api/v1/recipient/{{id}}            Delete recipient

    Categories:
      GET  /api/v1/categories                  List expense categories

    Webhooks:
      GET  /api/v1/webhooks                    List webhooks
      POST /api/v1/webhooks                    Create webhook (returns secret)
      GET  /api/v1/webhook/{{id}}                Get webhook details
      DELETE /api/v1/webhook/{{id}}              Delete webhook

  Simulation Endpoints:
    POST /simulate/transaction                 Send transaction.created event
    POST /simulate/transaction/update          Send transaction.updated event
    POST /simulate/custom                      Send custom event (JSON body)

  Quick Start:
    1. Start your Dify plugin or webhook receiver
    2. Register a webhook:
       curl -X POST http://localhost:{PORT}/api/v1/webhooks \\
         -H "Authorization: Bearer {MOCK_TOKEN}" \\
         -H "Content-Type: application/json" \\
         -d '{{"url": "http://localhost:8766/webhook"}}'

    3. Simulate an event:
       curl -X POST http://localhost:{PORT}/simulate/transaction

  Press Ctrl+C to stop
""")
    print("=" * 70 + "\n")


def main():
    """Start the mock server."""
    server = HTTPServer(("0.0.0.0", PORT), MockMercuryHandler)
    print_banner()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        server.shutdown()
        print("Server stopped.")


if __name__ == "__main__":
    main()
