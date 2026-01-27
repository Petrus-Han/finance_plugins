from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import logging
import re
import secrets
import time
import urllib.parse
from collections.abc import Mapping
from typing import Any
from urllib.parse import urlparse

import httpx
from werkzeug import Request, Response

from dify_plugin.entities.oauth import TriggerOAuthCredentials
from dify_plugin.entities.provider_config import CredentialType
from dify_plugin.entities.trigger import EventDispatch, Subscription, UnsubscribeResult
from dify_plugin.errors.trigger import (
    SubscriptionError,
    TriggerDispatchError,
    TriggerProviderCredentialValidationError,
    TriggerProviderOAuthError,
    TriggerValidationError,
    UnsubscribeError,
)
from dify_plugin.interfaces.trigger import Trigger, TriggerSubscriptionConstructor

logger = logging.getLogger(__name__)

# Webhook timestamp tolerance in seconds (5 minutes)
_WEBHOOK_TIMESTAMP_TOLERANCE = 300


class MercuryTrigger(Trigger):
    """Handle Mercury transaction webhook event dispatch."""

    def _dispatch_event(self, subscription: Subscription, request: Request) -> EventDispatch:
        webhook_secret = subscription.properties.get("webhook_secret")
        if webhook_secret:
            self._validate_signature(request, webhook_secret)
        else:
            logger.warning(
                "Webhook signature validation is disabled: webhook_secret not configured. "
                "This is a security risk - webhooks can be forged without signature verification."
            )

        payload = self._validate_payload(request)
        response = Response(response='{"status": "ok"}', status=200, mimetype="application/json")
        events = self._resolve_event_types(payload)

        return EventDispatch(events=events, response=response)

    def _validate_signature(self, request: Request, secret: str) -> None:
        """Verify Mercury webhook signature and timestamp."""
        sig_header = request.headers.get("Mercury-Signature")
        if not sig_header:
            raise TriggerValidationError("Missing Mercury-Signature header")

        try:
            parts = dict(p.split("=", 1) for p in sig_header.split(","))
            timestamp = parts.get("t")
            signature = parts.get("v1")

            if not timestamp or not signature:
                raise TriggerValidationError("Invalid Mercury-Signature format")

            # Validate timestamp to prevent replay attacks
            try:
                webhook_timestamp = int(timestamp)
                current_timestamp = int(time.time())
                time_diff = abs(current_timestamp - webhook_timestamp)
                if time_diff > _WEBHOOK_TIMESTAMP_TOLERANCE:
                    raise TriggerValidationError(
                        f"Webhook timestamp expired: request is {time_diff} seconds old "
                        f"(tolerance: {_WEBHOOK_TIMESTAMP_TOLERANCE} seconds)"
                    )
            except ValueError as e:
                raise TriggerValidationError(f"Invalid timestamp format: {timestamp}") from e

            body = request.get_data(as_text=True)
            signed_payload = f"{timestamp}.{body}"
            expected = hmac.new(secret.encode(), signed_payload.encode(), hashlib.sha256).hexdigest()

            if not hmac.compare_digest(signature, expected):
                raise TriggerValidationError("Invalid webhook signature")

        except TriggerValidationError:
            raise
        except Exception as exc:
            raise TriggerValidationError(f"Signature verification failed: {exc}") from exc

    def _validate_payload(self, request: Request) -> Mapping[str, Any]:
        """Parse and validate the webhook payload."""
        try:
            payload = request.get_json(force=True)
            if not payload:
                raise TriggerDispatchError("Empty request body")
            return payload
        except TriggerDispatchError:
            raise
        except Exception as exc:
            raise TriggerDispatchError(f"Failed to parse payload: {exc}") from exc

    def _resolve_event_types(self, payload: Mapping[str, Any]) -> list[str]:
        """Determine which event handlers to dispatch to based on payload content."""
        resource_type = payload.get("resourceType", "").lower()
        if resource_type == "transaction":
            return ["transaction"]
        return ["transaction"]


class MercurySubscriptionConstructor(TriggerSubscriptionConstructor):
    """Manage Mercury webhook subscriptions."""

    _API_BASE_URLS = {
        "production": "https://api.mercury.com/api/v1",
        "sandbox": "https://api-sandbox.mercury.com/api/v1",
    }
    _AUTH_URL = "https://app.mercury.com/oauth/authorize"
    _TOKEN_URL = "https://oauth2.mercury.com/oauth2/token"
    _REQUEST_TIMEOUT = 15
    _WEBHOOK_TTL = 30 * 24 * 60 * 60  # 30 days

    def _get_api_base_url(self, credentials: Mapping[str, Any]) -> str:
        """Get the API base URL based on environment setting."""
        api_environment = credentials.get("api_environment", "sandbox")

        if api_environment == "mock":
            mock_url = credentials.get("mock_server_url", "").strip()
            if not mock_url:
                raise TriggerProviderCredentialValidationError(
                    "Mock Server URL is required when using Mock environment"
                )

            # SSRF protection: validate mock_server_url
            self._validate_mock_url(mock_url)

            base_url = mock_url.rstrip("/")
            if not base_url.endswith("/api/v1"):
                base_url = f"{base_url}/api/v1"
            return base_url

        return self._API_BASE_URLS.get(api_environment, self._API_BASE_URLS["sandbox"])

    def _validate_mock_url(self, url: str) -> None:
        """Validate mock server URL to prevent SSRF attacks.

        Only allows localhost and 127.0.0.1 for mock/testing purposes.
        Rejects private IP ranges and other potentially dangerous URLs.
        """
        try:
            parsed = urlparse(url)

            # Must have http or https scheme
            if parsed.scheme not in ("http", "https"):
                raise TriggerProviderCredentialValidationError(
                    f"Invalid URL scheme: {parsed.scheme}. Only http or https are allowed."
                )

            hostname = parsed.hostname
            if not hostname:
                raise TriggerProviderCredentialValidationError("Invalid URL: missing hostname")

            # Allow only localhost for mock testing
            allowed_hosts = {"localhost", "127.0.0.1", "::1"}
            if hostname.lower() in allowed_hosts:
                return

            # Check if it's an IP address
            try:
                ip = ipaddress.ip_address(hostname)

                # Only allow loopback addresses
                if ip.is_loopback:
                    return

                # Block private, link-local, and reserved ranges
                if ip.is_private or ip.is_link_local or ip.is_reserved:
                    raise TriggerProviderCredentialValidationError(
                        f"Mock server URL cannot use private/internal IP address: {hostname}. "
                        "Only localhost (127.0.0.1) is allowed for security reasons."
                    )

                # Block any other IP address
                raise TriggerProviderCredentialValidationError(
                    f"Mock server URL cannot use IP address: {hostname}. "
                    "Only localhost (127.0.0.1) is allowed for security reasons."
                )

            except ValueError:
                # Not an IP address - it's a hostname
                # Block any hostname that's not localhost
                raise TriggerProviderCredentialValidationError(
                    f"Mock server URL hostname not allowed: {hostname}. "
                    "Only localhost (127.0.0.1) is allowed for mock testing."
                )

        except TriggerProviderCredentialValidationError:
            raise
        except Exception as e:
            raise TriggerProviderCredentialValidationError(f"Invalid mock server URL: {e}") from e

    def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
        state = secrets.token_urlsafe(16)
        params = {
            "client_id": system_credentials["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "read:accounts read:transactions webhooks:write offline_access",
            "state": state,
        }
        return f"{self._AUTH_URL}?{urllib.parse.urlencode(params)}"

    def _oauth_get_credentials(
        self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    ) -> TriggerOAuthCredentials:
        code = request.args.get("code")
        if not code:
            raise TriggerProviderOAuthError("No authorization code provided")

        if not system_credentials.get("client_id") or not system_credentials.get("client_secret"):
            raise TriggerProviderOAuthError("Client ID or Client Secret is required")

        data = {
            "grant_type": "authorization_code",
            "client_id": system_credentials["client_id"],
            "client_secret": system_credentials["client_secret"],
            "code": code,
            "redirect_uri": redirect_uri,
        }

        try:
            response = httpx.post(
                self._TOKEN_URL, data=data, headers={"Accept": "application/json"}, timeout=self._REQUEST_TIMEOUT
            )
            response.raise_for_status()
            response_json = response.json()

            access_token = response_json.get("access_token")
            if not access_token:
                raise TriggerProviderOAuthError(f"Error in Mercury OAuth: {response_json}")

            refresh_token = response_json.get("refresh_token")
            expires_in = response_json.get("expires_in", 3600)
            expires_at = int(time.time()) + expires_in

            credentials = {"access_token": access_token}
            if refresh_token:
                credentials["refresh_token"] = refresh_token

            return TriggerOAuthCredentials(credentials=credentials, expires_at=expires_at)

        except httpx.HTTPStatusError as e:
            raise TriggerProviderOAuthError(f"Failed to exchange code for token: {e}") from e
        except TriggerProviderOAuthError:
            raise
        except Exception as e:
            raise TriggerProviderOAuthError(f"OAuth error: {e}") from e

    def _oauth_refresh_credentials(
        self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    ) -> TriggerOAuthCredentials:
        refresh_token = credentials.get("refresh_token")
        if not refresh_token:
            raise TriggerProviderOAuthError("No refresh token available")

        data = {
            "grant_type": "refresh_token",
            "client_id": system_credentials["client_id"],
            "client_secret": system_credentials["client_secret"],
            "refresh_token": refresh_token,
        }

        try:
            response = httpx.post(
                self._TOKEN_URL, data=data, headers={"Accept": "application/json"}, timeout=self._REQUEST_TIMEOUT
            )
            response.raise_for_status()
            response_json = response.json()

            access_token = response_json.get("access_token")
            if not access_token:
                raise TriggerProviderOAuthError(f"Error refreshing token: {response_json}")

            new_refresh_token = response_json.get("refresh_token", refresh_token)
            expires_in = response_json.get("expires_in", 3600)
            expires_at = int(time.time()) + expires_in

            return TriggerOAuthCredentials(
                credentials={"access_token": access_token, "refresh_token": new_refresh_token}, expires_at=expires_at
            )

        except httpx.HTTPStatusError as e:
            raise TriggerProviderOAuthError(f"Failed to refresh token: {e}") from e
        except TriggerProviderOAuthError:
            raise
        except Exception as e:
            raise TriggerProviderOAuthError(f"Token refresh error: {e}") from e

    def _validate_api_key(self, credentials: Mapping[str, Any]) -> None:
        access_token = credentials.get("access_token")
        if not access_token:
            raise TriggerProviderCredentialValidationError("Mercury API Access Token is required.")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
        }

        api_base_url = self._get_api_base_url(credentials)
        url = f"{api_base_url}/accounts"

        try:
            response = httpx.get(url, headers=headers, timeout=self._REQUEST_TIMEOUT)
        except httpx.HTTPError as exc:
            raise TriggerProviderCredentialValidationError(f"Error while validating credentials: {exc}") from exc

        if response.status_code == 401:
            raise TriggerProviderCredentialValidationError("Invalid or expired Mercury API access token.")

        if response.status_code >= 400:
            try:
                details = response.json()
            except json.JSONDecodeError:
                details = {"message": response.text}
            raise TriggerProviderCredentialValidationError(
                f"Mercury API validation failed: {details.get('message', response.text)}"
            )

    def _create_subscription(
        self,
        endpoint: str,
        parameters: Mapping[str, Any],
        credentials: Mapping[str, Any],
        credential_type: CredentialType,
    ) -> Subscription:
        access_token = credentials.get("access_token")
        if not access_token:
            raise SubscriptionError("Mercury API access token is required.", error_code="MISSING_CREDENTIALS")

        event_types: list[str] = parameters.get("event_types", [])
        filter_paths_str: str = parameters.get("filter_paths", "")

        webhook_data: dict[str, Any] = {"url": endpoint}
        if event_types:
            webhook_data["eventTypes"] = event_types
        if filter_paths_str and filter_paths_str.strip():
            filter_paths = [p.strip() for p in filter_paths_str.split(",") if p.strip()]
            if filter_paths:
                webhook_data["filterPaths"] = filter_paths

        api_base_url = self._get_api_base_url(credentials)
        url = f"{api_base_url}/webhooks"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json;charset=utf-8",
        }

        try:
            response = httpx.post(url, json=webhook_data, headers=headers, timeout=self._REQUEST_TIMEOUT)
        except httpx.HTTPError as exc:
            raise SubscriptionError(f"Network error while creating webhook: {exc}", error_code="NETWORK_ERROR") from exc

        if response.status_code in (200, 201):
            webhook_response = response.json()
            return Subscription(
                expires_at=int(time.time()) + self._WEBHOOK_TTL,
                endpoint=endpoint,
                parameters=parameters,
                properties={
                    "external_id": webhook_response.get("id"),
                    "webhook_secret": webhook_response.get("secret"),
                    "status": webhook_response.get("status", "active"),
                },
            )

        response_data: dict[str, Any] = {}
        try:
            response_data = response.json() if response.content else {}
        except json.JSONDecodeError:
            response_data = {"message": response.text}

        raise SubscriptionError(
            f"Failed to create Mercury webhook: {response_data.get('message', json.dumps(response_data))}",
            error_code="WEBHOOK_CREATION_FAILED",
            external_response=response_data,
        )

    def _delete_subscription(
        self, subscription: Subscription, credentials: Mapping[str, Any], credential_type: CredentialType
    ) -> UnsubscribeResult:
        external_id = subscription.properties.get("external_id")
        if not external_id:
            raise UnsubscribeError(
                message="Missing webhook ID information", error_code="MISSING_PROPERTIES", external_response=None
            )

        access_token = credentials.get("access_token")
        if not access_token:
            raise UnsubscribeError(
                message="Mercury API access token is required.",
                error_code="MISSING_CREDENTIALS",
                external_response=None,
            )

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
        }

        api_base_url = self._get_api_base_url(credentials)
        url = f"{api_base_url}/webhook/{external_id}"

        try:
            response = httpx.delete(url, headers=headers, timeout=self._REQUEST_TIMEOUT)
        except httpx.HTTPError as exc:
            raise UnsubscribeError(
                message=f"Network error while deleting webhook: {exc}",
                error_code="NETWORK_ERROR",
                external_response=None,
            ) from exc

        if response.status_code in (200, 204):
            return UnsubscribeResult(success=True, message=f"Successfully removed webhook {external_id} from Mercury")

        if response.status_code == 404:
            return UnsubscribeResult(
                success=True, message=f"Webhook {external_id} not found in Mercury (already deleted)"
            )

        response_data = None
        try:
            response_data = response.json() if response.content else None
        except json.JSONDecodeError:
            pass

        raise UnsubscribeError(
            message=f"Failed to delete webhook: {response.text}",
            error_code="WEBHOOK_DELETION_FAILED",
            external_response=response_data,
        )

    def _refresh_subscription(
        self, subscription: Subscription, credentials: Mapping[str, Any], credential_type: CredentialType
    ) -> Subscription:
        external_id = subscription.properties.get("external_id")
        if not external_id:
            raise SubscriptionError("Missing webhook ID for refresh", error_code="MISSING_PROPERTIES")

        access_token = credentials.get("access_token")
        if not access_token:
            raise SubscriptionError("Mercury API access token is required.", error_code="MISSING_CREDENTIALS")

        api_base_url = self._get_api_base_url(credentials)
        url = f"{api_base_url}/webhook/{external_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
        }

        try:
            response = httpx.get(url, headers=headers, timeout=self._REQUEST_TIMEOUT)
        except httpx.HTTPError as exc:
            raise SubscriptionError(
                f"Network error while refreshing webhook: {exc}", error_code="NETWORK_ERROR"
            ) from exc

        if response.status_code == 200:
            webhook_data = response.json()
            updated_properties = dict(subscription.properties)
            updated_properties["status"] = webhook_data.get("status", "active")
            return Subscription(
                expires_at=int(time.time()) + self._WEBHOOK_TTL,
                endpoint=subscription.endpoint,
                parameters=subscription.parameters,
                properties=updated_properties,
            )

        if response.status_code == 404:
            raise SubscriptionError(
                f"Webhook {external_id} no longer exists on Mercury", error_code="WEBHOOK_NOT_FOUND"
            )

        raise SubscriptionError(f"Failed to refresh webhook: {response.text}", error_code="WEBHOOK_REFRESH_FAILED")
