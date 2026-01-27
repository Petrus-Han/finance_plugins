#!/usr/bin/env python3
"""
Webhook Receiver - Simulates Dify Plugin Webhook Endpoint

WARNING: This script is for development only. Do not use in production.

This server receives webhook events and validates them exactly like
the mercury_trigger_plugin does. Use this for debugging the full flow.

Features:
1. Receives POST webhooks at any path
2. Validates Mercury-Signature header (HMAC-SHA256)
3. Parses and displays the event payload
4. Shows all headers for debugging

Usage:
    python scripts/webhook_receiver.py

    # Server runs on http://localhost:8766
    # All POST requests will be received and logged

    # Specify a webhook secret for signature validation:
    WEBHOOK_SECRET="your_base64_secret" python scripts/webhook_receiver.py

Endpoints:
    POST /*         Receive any webhook
    GET  /          Status page with recent webhooks
    GET  /webhooks  List all received webhooks
    GET  /clear     Clear webhook history

Environment Variables:
    WEBHOOK_PORT    - Server port (default: 8766)
    WEBHOOK_SECRET  - Webhook secret for signature validation (optional)
"""

import base64
import hashlib
import hmac
import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional

# Configuration
PORT = int(os.environ.get("WEBHOOK_PORT", "8766"))
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")

# Storage for received webhooks
received_webhooks: list[dict] = []


def validate_signature(body: str, sig_header: str, secret: str) -> dict:
    """Validate Mercury-style webhook signature.

    Returns a dict with validation result and debug info.
    """
    result = {
        "valid": False,
        "sig_header": sig_header,
        "timestamp": None,
        "received_sig": None,
        "expected_sig": None,
        "error": None
    }

    if not sig_header:
        result["error"] = "Missing Mercury-Signature header"
        return result

    try:
        # Parse signature header: t=timestamp,v1=signature
        parts = dict(p.split("=", 1) for p in sig_header.split(","))
        timestamp = parts.get("t")
        signature = parts.get("v1")

        result["timestamp"] = timestamp
        result["received_sig"] = signature

        if not timestamp or not signature:
            result["error"] = "Invalid signature format (missing t or v1)"
            return result

        # Decode the secret (base64)
        try:
            secret_bytes = base64.b64decode(secret)
        except Exception:
            secret_bytes = secret.encode()

        # Calculate expected signature
        signed_payload = f"{timestamp}.{body}"
        expected = hmac.new(
            secret_bytes,
            signed_payload.encode(),
            hashlib.sha256
        ).hexdigest()

        result["expected_sig"] = expected
        result["valid"] = hmac.compare_digest(signature, expected)

        if not result["valid"]:
            result["error"] = "Signature mismatch"

        return result

    except Exception as e:
        result["error"] = f"Validation error: {e}"
        return result


class WebhookReceiverHandler(BaseHTTPRequestHandler):
    """HTTP handler for receiving webhooks."""

    def log_message(self, format, *args):
        """Custom log format."""
        pass  # Suppress default logging, we do our own

    def _send_response(self, data: dict, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())

    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/":
            self._send_response({
                "service": "Webhook Receiver",
                "status": "running",
                "received_count": len(received_webhooks),
                "recent_webhooks": received_webhooks[-5:],
                "signature_validation": "enabled" if WEBHOOK_SECRET else "disabled"
            })
        elif self.path == "/webhooks":
            self._send_response({
                "webhooks": received_webhooks,
                "count": len(received_webhooks)
            })
        elif self.path == "/clear":
            received_webhooks.clear()
            self._send_response({"message": "Cleared all webhooks"})
        else:
            self._send_response({"status": "ok"})

    def do_POST(self):
        """Handle POST requests (webhooks)."""
        timestamp = datetime.now()

        # Read body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode() if content_length > 0 else ""

        # Parse payload
        try:
            payload = json.loads(body) if body else {}
        except json.JSONDecodeError:
            payload = {"_raw": body}

        # Extract important headers
        sig_header = self.headers.get("Mercury-Signature", "")
        headers = {
            "Mercury-Signature": sig_header,
            "Content-Type": self.headers.get("Content-Type"),
            "User-Agent": self.headers.get("User-Agent"),
            "X-Mercury-Event-Id": self.headers.get("X-Mercury-Event-Id"),
            "X-Mercury-Webhook-Id": self.headers.get("X-Mercury-Webhook-Id"),
        }

        # Validate signature if secret is configured
        sig_validation = None
        if WEBHOOK_SECRET:
            sig_validation = validate_signature(body, sig_header, WEBHOOK_SECRET)

        # Store webhook data
        webhook_data = {
            "timestamp": timestamp.isoformat(),
            "path": self.path,
            "headers": headers,
            "payload": payload,
            "signature_validation": sig_validation,
            "body_length": len(body)
        }
        received_webhooks.append(webhook_data)

        # Print detailed information
        print("\n" + "=" * 70)
        print(f"  WEBHOOK RECEIVED [{timestamp.strftime('%H:%M:%S')}]")
        print("=" * 70)

        print(f"\n  Path: {self.path}")
        print(f"  Body Length: {len(body)} bytes")

        print(f"\n  Headers:")
        for key, value in headers.items():
            if value:
                # Truncate long values
                display_value = value[:60] + "..." if len(str(value)) > 60 else value
                print(f"    {key}: {display_value}")

        # Signature validation result
        if sig_validation:
            print(f"\n  Signature Validation:")
            if sig_validation["valid"]:
                print(f"    Status: VALID")
            else:
                print(f"    Status: INVALID")
                print(f"    Error: {sig_validation['error']}")
            print(f"    Timestamp: {sig_validation['timestamp']}")
            if sig_validation["received_sig"]:
                print(f"    Received: {sig_validation['received_sig'][:32]}...")
            if sig_validation["expected_sig"]:
                print(f"    Expected: {sig_validation['expected_sig'][:32]}...")

        # Payload summary
        print(f"\n  Payload:")
        if isinstance(payload, dict):
            # Mercury-style event
            if "resourceType" in payload:
                print(f"    Event ID: {payload.get('id', 'N/A')}")
                print(f"    Resource Type: {payload.get('resourceType', 'N/A')}")
                print(f"    Operation: {payload.get('operationType', 'N/A')}")
                print(f"    Resource ID: {payload.get('resourceId', 'N/A')}")

                # Transaction details from mergePatch
                merge_patch = payload.get("mergePatch", {})
                if merge_patch:
                    print(f"\n    Transaction Details:")
                    print(f"      Amount: {merge_patch.get('amount', 'N/A')}")
                    print(f"      Status: {merge_patch.get('status', 'N/A')}")
                    print(f"      Counterparty: {merge_patch.get('counterpartyName', 'N/A')}")
                    print(f"      Account ID: {merge_patch.get('accountId', 'N/A')}")
                    print(f"      Kind: {merge_patch.get('kind', 'N/A')}")
            else:
                # Generic payload
                print(f"    Keys: {list(payload.keys())}")
                payload_str = json.dumps(payload, indent=6)
                if len(payload_str) > 500:
                    print(f"    Data: {payload_str[:500]}...")
                else:
                    print(f"    Data: {payload_str}")
        else:
            print(f"    {payload}")

        print("\n" + "=" * 70)

        # Return success response (like Dify plugin would)
        self._send_response({"status": "ok", "received": True})


def print_banner():
    """Print startup banner."""
    print("\n" + "=" * 70)
    print("  Webhook Receiver - For Testing Mercury Webhooks")
    print("=" * 70)
    print(f"""
  Server Address: http://localhost:{PORT}

  Endpoints:
    POST /*         Receive any webhook (will be logged)
    GET  /          Status page
    GET  /webhooks  List all received webhooks
    GET  /clear     Clear webhook history

  Signature Validation: {"ENABLED" if WEBHOOK_SECRET else "DISABLED"}
""")
    if WEBHOOK_SECRET:
        print(f"  Webhook Secret configured: True")
    else:
        print("""  To enable signature validation, set the WEBHOOK_SECRET env var:
    WEBHOOK_SECRET="your_base64_secret" python scripts/webhook_receiver.py
""")
    print("  Waiting for webhooks...")
    print("=" * 70 + "\n")


def main():
    """Start the webhook receiver."""
    server = HTTPServer(("0.0.0.0", PORT), WebhookReceiverHandler)
    print_banner()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down receiver...")
        server.shutdown()
        print("Receiver stopped.")


if __name__ == "__main__":
    main()
