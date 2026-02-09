import json
import logging
import secrets
import time
import urllib.parse
from collections.abc import Mapping
from typing import Any

import gspread
import httpx
from dify_plugin import ToolProvider
from dify_plugin.entities.oauth import ToolOAuthCredentials
from dify_plugin.errors.tool import ToolProviderCredentialValidationError, ToolProviderOAuthError
from google.oauth2.credentials import Credentials as OAuthCredentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from werkzeug import Request

logger = logging.getLogger(__name__)

# Google OAuth endpoints
_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
_TOKEN_URL = "https://oauth2.googleapis.com/token"
_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# Scopes needed for Sheets access
_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
]

_REQUEST_TIMEOUT = 30

# Sheet definitions for auto-initialization
ROSTER_HEADERS = [
    "full_name", "email", "source", "source_id", "source_department",
    "job_title", "employment_type", "finance_department", "status", "notes", "last_synced",
]
DEPARTMENT_MAPPING_HEADERS = [
    "source_department", "finance_department", "source",
]
SYNC_LOG_HEADERS = [
    "timestamp", "source", "records_added", "records_updated", "records_skipped",
]


def get_gspread_client(credentials: Mapping[str, Any]) -> gspread.Client:
    """Build a gspread client from either OAuth token or Service Account JSON.

    Priority:
    1. OAuth access_token (from user authorization)
    2. service_account_json (from provider credentials)
    """
    access_token = credentials.get("access_token")
    sa_json = credentials.get("service_account_json")

    if access_token:
        creds = OAuthCredentials(
            token=access_token,
            scopes=_SCOPES,
        )
        return gspread.authorize(creds)

    if sa_json:
        try:
            sa_info = json.loads(sa_json) if isinstance(sa_json, str) else sa_json
        except (json.JSONDecodeError, TypeError) as e:
            raise ToolProviderCredentialValidationError(
                "Invalid Service Account JSON format."
            ) from e
        creds = ServiceAccountCredentials.from_service_account_info(sa_info, scopes=_SCOPES)
        return gspread.authorize(creds)

    raise ToolProviderCredentialValidationError(
        "No authentication credentials provided. "
        "Please configure OAuth2 authorization or provide a Service Account JSON."
    )


def ensure_sheets_initialized(spreadsheet: gspread.Spreadsheet) -> None:
    """Ensure all required sheets and headers exist in the spreadsheet.

    Creates missing sheets and sets header rows if they don't exist.
    """
    sheet_definitions = {
        "Roster": ROSTER_HEADERS,
        "Department_Mapping": DEPARTMENT_MAPPING_HEADERS,
        "Sync_Log": SYNC_LOG_HEADERS,
    }

    existing_titles = [ws.title for ws in spreadsheet.worksheets()]

    for sheet_name, headers in sheet_definitions.items():
        if sheet_name not in existing_titles:
            logger.info(f"Creating sheet: {sheet_name}")
            ws = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(headers))
            ws.update([headers], "A1")
        else:
            ws = spreadsheet.worksheet(sheet_name)
            # Check if header row exists (first row should match)
            try:
                first_row = ws.row_values(1)
            except Exception:
                first_row = []
            if first_row != headers:
                ws.update([headers], "A1")


class EmployeeRosterProvider(ToolProvider):
    """Provider for Employee Roster plugin with Google Sheets backend."""

    def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
        """Generate Google OAuth2 authorization URL."""
        params = {
            "client_id": system_credentials["client_id"],
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": " ".join(_SCOPES),
            "access_type": "offline",
            "prompt": "consent",
            "state": secrets.token_urlsafe(16),
        }
        return f"{_AUTH_URL}?{urllib.parse.urlencode(params)}"

    def _oauth_get_credentials(
        self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request
    ) -> ToolOAuthCredentials:
        """Exchange authorization code for access and refresh tokens."""
        code = request.args.get("code")
        if not code:
            raise ToolProviderOAuthError("No authorization code provided")

        data = {
            "code": code,
            "client_id": system_credentials["client_id"],
            "client_secret": system_credentials["client_secret"],
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }

        try:
            response = httpx.post(
                _TOKEN_URL,
                data=data,
                headers={"Accept": "application/json"},
                timeout=_REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            token_data = response.json()

            access_token = token_data.get("access_token")
            refresh_token = token_data.get("refresh_token")
            expires_in = token_data.get("expires_in", 3600)

            if not access_token:
                raise ToolProviderOAuthError(f"No access_token in response: {token_data}")

            expires_at = int(time.time()) + expires_in
            cred_dict = {"access_token": access_token}
            if refresh_token:
                cred_dict["refresh_token"] = refresh_token

            return ToolOAuthCredentials(credentials=cred_dict, expires_at=expires_at)

        except httpx.HTTPStatusError as e:
            raise ToolProviderOAuthError(f"Failed to exchange code for token: {e}") from e
        except ToolProviderOAuthError:
            raise
        except Exception as e:
            raise ToolProviderOAuthError(f"OAuth error: {e}") from e

    def _oauth_refresh_credentials(
        self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]
    ) -> ToolOAuthCredentials:
        """Refresh the access token using the refresh token."""
        refresh_token = credentials.get("refresh_token")
        if not refresh_token:
            raise ToolProviderOAuthError("No refresh token available. Please re-authorize Google Sheets.")

        data = {
            "refresh_token": refresh_token,
            "client_id": system_credentials.get("client_id") or credentials.get("client_id"),
            "client_secret": system_credentials.get("client_secret") or credentials.get("client_secret"),
            "grant_type": "refresh_token",
        }

        try:
            response = httpx.post(
                _TOKEN_URL,
                data=data,
                headers={"Accept": "application/json"},
                timeout=_REQUEST_TIMEOUT,
            )

            if response.status_code == 400:  # noqa: PLR2004
                try:
                    error_json = response.json()
                except Exception:
                    error_json = {}
                if error_json.get("error") == "invalid_grant":
                    raise ToolProviderOAuthError(
                        "Google refresh token has expired or been revoked. Please re-authorize."
                    )
                raise ToolProviderOAuthError(
                    f"Token refresh failed: {error_json.get('error_description', response.text)}"
                )

            response.raise_for_status()
            token_data = response.json()

            new_access_token = token_data.get("access_token")
            if not new_access_token:
                raise ToolProviderOAuthError(f"No access_token in refresh response: {token_data}")

            expires_in = token_data.get("expires_in", 3600)
            expires_at = int(time.time()) + expires_in

            # Google does NOT rotate refresh tokens by default
            new_creds = {
                "access_token": new_access_token,
                "refresh_token": refresh_token,
            }

            return ToolOAuthCredentials(credentials=new_creds, expires_at=expires_at)

        except ToolProviderOAuthError:
            raise
        except httpx.HTTPStatusError as e:
            raise ToolProviderOAuthError(f"Failed to refresh token: {e}") from e
        except Exception as e:
            raise ToolProviderOAuthError(f"Token refresh error: {e}") from e

    def _validate_credentials(self, credentials: Mapping[str, Any]) -> None:
        """Validate that the credentials can access the target spreadsheet."""
        spreadsheet_id = credentials.get("spreadsheet_id")
        if not spreadsheet_id:
            raise ToolProviderCredentialValidationError("Google Spreadsheet ID is required.")

        try:
            client = get_gspread_client(credentials)
            spreadsheet = client.open_by_key(spreadsheet_id)
            ensure_sheets_initialized(spreadsheet)
        except ToolProviderCredentialValidationError:
            raise
        except gspread.exceptions.SpreadsheetNotFound as e:
            raise ToolProviderCredentialValidationError(
                "Spreadsheet not found. Check the ID and ensure the account has access."
            ) from e
        except gspread.exceptions.APIError as e:
            status = getattr(e, "code", None) or (e.response.status_code if hasattr(e, "response") else "")
            if status == 403:  # noqa: PLR2004
                raise ToolProviderCredentialValidationError(
                    "Access denied. Share the spreadsheet with the authenticated account."
                ) from e
            if status == 401:  # noqa: PLR2004
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Token may be expired — please re-authorize."
                ) from e
            raise ToolProviderCredentialValidationError(f"Google Sheets API error: {e}") from e
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"Failed to validate credentials: {e}"
            ) from e
