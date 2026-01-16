import secrets
import urllib.parse
from collections.abc import Mapping
from typing import Any

import httpx
from werkzeug import Request

from dify_plugin import ToolProvider
from dify_plugin.entities.oauth import ToolOAuthCredentials
from dify_plugin.errors.tool import ToolProviderCredentialValidationError, ToolProviderOAuthError


class MercuryToolsProvider(ToolProvider):
    """Provider for Mercury Banking API tools."""

    _API_BASE_URL = "https://api.mercury.com/api/v1"
    _AUTH_URL = "https://app.mercury.com/oauth/authorize"
    _TOKEN_URL = "https://oauth2.mercury.com/oauth2/token"
    _REQUEST_TIMEOUT = 15

    def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
        """
        Generate the authorization URL for the Mercury OAuth.

        Args:
            redirect_uri: The callback URL where Mercury will redirect after authorization
            system_credentials: System-level credentials containing client_id and client_secret

        Returns:
            The full authorization URL
        """
        state = secrets.token_urlsafe(16)
        params = {
            "client_id": system_credentials["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "read:accounts read:transactions offline_access",
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
            "client_id": system_credentials["client_id"],
            "client_secret": system_credentials["client_secret"],
            "code": code,
            "redirect_uri": redirect_uri,
        }

        try:
            response = httpx.post(
                self._TOKEN_URL,
                data=data,
                headers={"Accept": "application/json"},
                timeout=self._REQUEST_TIMEOUT
            )
            response.raise_for_status()
            response_json = response.json()

            access_token = response_json.get("access_token")
            refresh_token = response_json.get("refresh_token")
            expires_in = response_json.get("expires_in", 3600)  # Default 1 hour

            if not access_token:
                raise ToolProviderOAuthError(f"Error in Mercury OAuth: {response_json}")

            # Calculate expiration timestamp (current time + expires_in seconds)
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
            "client_id": system_credentials["client_id"],
            "client_secret": system_credentials["client_secret"],
            "refresh_token": refresh_token,
        }

        try:
            response = httpx.post(
                self._TOKEN_URL,
                data=data,
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
        """Validate Mercury API access token by attempting to fetch accounts."""
        try:
            access_token = credentials.get("access_token")

            if not access_token:
                raise ToolProviderCredentialValidationError(
                    "Mercury API Access Token is required."
                )

            # Get API environment from credentials
            api_environment = credentials.get("api_environment", "production")

            # Determine API base URL based on environment
            if api_environment == "sandbox":
                api_base_url = "https://api-sandbox.mercury.com/api/v1"
            else:
                api_base_url = "https://api.mercury.com/api/v1"

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json;charset=utf-8",
            }

            # Validate token by fetching accounts
            response = httpx.get(
                f"{api_base_url}/accounts",
                headers=headers,
                timeout=self._REQUEST_TIMEOUT
            )

            if response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Invalid or expired Mercury API access token."
                )

            if response.status_code >= 400:
                try:
                    error_detail = response.json()
                    error_msg = error_detail.get("message", response.text)
                except Exception:
                    error_msg = response.text

                raise ToolProviderCredentialValidationError(
                    f"Mercury API validation failed: {error_msg}"
                )

        except ToolProviderCredentialValidationError:
            raise
        except httpx.HTTPError as exc:
            raise ToolProviderCredentialValidationError(
                f"Network error while validating credentials: {exc}"
            ) from exc
        except Exception as exc:
            raise ToolProviderCredentialValidationError(
                f"Unexpected error: {exc}"
            ) from exc
