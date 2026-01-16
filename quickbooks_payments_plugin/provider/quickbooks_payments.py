import secrets
import urllib.parse
from collections.abc import Mapping
from typing import Any

import httpx
from werkzeug import Request

from dify_plugin import ToolProvider
from dify_plugin.entities.oauth import ToolOAuthCredentials
from dify_plugin.errors.tool import ToolProviderCredentialValidationError, ToolProviderOAuthError


class QuickBooksPaymentsProvider(ToolProvider):
    """Provider for QuickBooks Payments API."""

    _AUTH_URL = "https://appcenter.intuit.com/connect/oauth2"
    _TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    _API_BASE_URLS = {
        "production": "https://api.intuit.com/quickbooks/v4/payments",
        "sandbox": "https://sandbox.api.intuit.com/quickbooks/v4/payments"
    }
    _REQUEST_TIMEOUT = 30

    def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
        """
        Generate the authorization URL for QuickBooks Payments OAuth.

        Args:
            redirect_uri: The callback URL where QuickBooks will redirect after authorization
            system_credentials: System-level credentials containing client_id, client_secret, and environment

        Returns:
            The full authorization URL
        """
        state = secrets.token_urlsafe(16)
        params = {
            "client_id": system_credentials["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "com.intuit.quickbooks.payment",
            "state": state,
        }
        return f"{self._AUTH_URL}?{urllib.parse.urlencode(params)}"

    def _oauth_get_credentials(
        self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    ) -> ToolOAuthCredentials:
        """
        Exchange authorization code for access token.

        Args:
            redirect_uri: The callback URL
            system_credentials: System-level credentials containing client_id and client_secret
            request: The HTTP request containing the authorization code

        Returns:
            ToolOAuthCredentials containing the access token and expiration time
        """
        code = request.args.get("code")
        if not code:
            raise ToolProviderOAuthError("No authorization code provided")

        # Exchange code for access token
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }

        # Use HTTP Basic Auth for client credentials
        auth = (system_credentials["client_id"], system_credentials["client_secret"])

        try:
            response = httpx.post(
                self._TOKEN_URL,
                data=data,
                auth=auth,
                headers={"Accept": "application/json"},
                timeout=self._REQUEST_TIMEOUT
            )
            response.raise_for_status()
            response_json = response.json()

            access_token = response_json.get("access_token")
            refresh_token = response_json.get("refresh_token")
            expires_in = response_json.get("expires_in", 3600)  # Default 1 hour

            if not access_token:
                raise ToolProviderOAuthError(f"Error in QuickBooks OAuth: {response_json}")

            # Calculate expiration timestamp
            import time
            expires_at = int(time.time()) + expires_in

            credentials = {"access_token": access_token}
            if refresh_token:
                credentials["refresh_token"] = refresh_token

            return ToolOAuthCredentials(credentials=credentials, expires_at=expires_at)

        except httpx.HTTPStatusError as e:
            raise ToolProviderOAuthError(f"Failed to exchange code for token: {e}") from e
        except Exception as e:
            raise ToolProviderOAuthError(f"OAuth error: {e}") from e

    def _oauth_refresh_credentials(
        self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    ) -> ToolOAuthCredentials:
        """
        Refresh the access token using the refresh token.

        Args:
            redirect_uri: The callback URL
            system_credentials: System-level credentials containing client_id and client_secret
            credentials: Current credentials containing the refresh_token

        Returns:
            ToolOAuthCredentials containing the new access token and expiration time
        """
        refresh_token = credentials.get("refresh_token")
        if not refresh_token:
            raise ToolProviderOAuthError("No refresh token available")

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        # Use HTTP Basic Auth for client credentials
        auth = (system_credentials["client_id"], system_credentials["client_secret"])

        try:
            response = httpx.post(
                self._TOKEN_URL,
                data=data,
                auth=auth,
                headers={"Accept": "application/json"},
                timeout=self._REQUEST_TIMEOUT
            )
            response.raise_for_status()
            response_json = response.json()

            access_token = response_json.get("access_token")
            new_refresh_token = response_json.get("refresh_token", refresh_token)
            expires_in = response_json.get("expires_in", 3600)

            if not access_token:
                raise ToolProviderOAuthError(f"Error refreshing token: {response_json}")

            import time
            expires_at = int(time.time()) + expires_in

            new_credentials = {
                "access_token": access_token,
                "refresh_token": new_refresh_token
            }

            return ToolOAuthCredentials(credentials=new_credentials, expires_at=expires_at)

        except httpx.HTTPStatusError as e:
            raise ToolProviderOAuthError(f"Failed to refresh token: {e}") from e
        except Exception as e:
            raise ToolProviderOAuthError(f"Token refresh error: {e}") from e

    def _validate_credentials(self, credentials: Mapping[str, Any]) -> None:
        """
        Validate QuickBooks Payments API access token.

        Note: Since there's no simple validation endpoint, we just check if the token exists.
        Actual validation will happen when making API calls.
        """
        try:
            access_token = credentials.get("access_token")

            if not access_token:
                raise ToolProviderCredentialValidationError(
                    "QuickBooks Payments API Access Token is required."
                )

            # Token format validation (basic check)
            if len(access_token) < 20:
                raise ToolProviderCredentialValidationError(
                    "Invalid QuickBooks Payments API access token format."
                )

        except ToolProviderCredentialValidationError:
            raise
        except Exception as exc:
            raise ToolProviderCredentialValidationError(
                f"Unexpected error: {exc}"
            ) from exc

    def get_api_base_url(self, credentials: Mapping[str, Any]) -> str:
        """
        Get the API base URL based on environment.

        Args:
            credentials: Credentials containing environment selection

        Returns:
            API base URL
        """
        environment = credentials.get("environment", "sandbox")
        return self._API_BASE_URLS.get(environment, self._API_BASE_URLS["sandbox"])
