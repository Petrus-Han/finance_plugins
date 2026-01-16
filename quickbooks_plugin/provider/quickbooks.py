import secrets
import urllib.parse
from collections.abc import Mapping
from typing import Any

import httpx
from werkzeug import Request

from dify_plugin import ToolProvider
from dify_plugin.entities.oauth import ToolOAuthCredentials
from dify_plugin.errors.tool import ToolProviderCredentialValidationError, ToolProviderOAuthError


class QuickBooksProvider(ToolProvider):
    """Provider for QuickBooks Online Accounting API."""

    _AUTH_URL = "https://appcenter.intuit.com/connect/oauth2"
    _TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
    _API_BASE_URLS = {
        "production": "https://quickbooks.api.intuit.com/v3",
        "sandbox": "https://sandbox-quickbooks.api.intuit.com/v3"
    }
    _REQUEST_TIMEOUT = 30

    def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
        """
        Generate the authorization URL for QuickBooks OAuth.

        Args:
            redirect_uri: The callback URL where QuickBooks will redirect after authorization
            system_credentials: System-level credentials containing client_id and client_secret

        Returns:
            The full authorization URL
        """
        state = secrets.token_urlsafe(16)
        params = {
            "client_id": system_credentials["client_id"],
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "com.intuit.quickbooks.accounting",
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
            request: The HTTP request containing the authorization code and realm_id

        Returns:
            ToolOAuthCredentials containing the access token and expiration time
        """
        code = request.args.get("code")
        realm_id = request.args.get("realmId")  # QuickBooks returns this in callback

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
            if realm_id:
                credentials["realm_id"] = realm_id

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

            # Preserve realm_id and other credentials
            new_credentials = {
                "access_token": access_token,
                "refresh_token": new_refresh_token
            }

            # Preserve realm_id if it exists
            if "realm_id" in credentials:
                new_credentials["realm_id"] = credentials["realm_id"]

            return ToolOAuthCredentials(credentials=new_credentials, expires_at=expires_at)

        except httpx.HTTPStatusError as e:
            raise ToolProviderOAuthError(f"Failed to refresh token: {e}") from e
        except Exception as e:
            raise ToolProviderOAuthError(f"Token refresh error: {e}") from e

    def _validate_credentials(self, credentials: Mapping[str, Any]) -> None:
        """
        Validate QuickBooks API access token by querying CompanyInfo.

        Args:
            credentials: Credentials containing access_token and realm_id
        """
        try:
            access_token = credentials.get("access_token")
            realm_id = credentials.get("realm_id")

            if not access_token:
                raise ToolProviderCredentialValidationError(
                    "QuickBooks API Access Token is required."
                )

            if not realm_id:
                raise ToolProviderCredentialValidationError(
                    "QuickBooks Realm ID (Company ID) is required."
                )

            # Get environment
            environment = credentials.get("environment", "sandbox")
            api_base_url = self._API_BASE_URLS.get(environment, self._API_BASE_URLS["sandbox"])

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json"
            }

            # Validate by querying CompanyInfo
            response = httpx.get(
                f"{api_base_url}/company/{realm_id}/companyinfo/{realm_id}",
                headers=headers,
                timeout=self._REQUEST_TIMEOUT
            )

            if response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Invalid or expired QuickBooks API access token."
                )

            if response.status_code == 403:
                raise ToolProviderCredentialValidationError(
                    "Access forbidden. Please check your QuickBooks permissions."
                )

            if response.status_code >= 400:
                try:
                    error_detail = response.json()
                    error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
                except Exception:
                    error_msg = response.text

                raise ToolProviderCredentialValidationError(
                    f"QuickBooks API validation failed: {error_msg}"
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

    def get_api_base_url(self, credentials: Mapping[str, Any]) -> str:
        """
        Get the API base URL based on environment.

        Args:
            credentials: Credentials containing environment selection

        Returns:
            API base URL for the selected environment
        """
        environment = credentials.get("environment", "sandbox")
        return self._API_BASE_URLS.get(environment, self._API_BASE_URLS["sandbox"])
