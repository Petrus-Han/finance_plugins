import logging
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin.config.logger_format import plugin_logger_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(plugin_logger_handler)


class CustomerManagementTool(Tool):
    """Tool to manage AR customers - CRUD operations."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        logger.info("=== CustomerManagementTool._invoke called ===")

        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        api_environment = self.runtime.credentials.get("api_environment", "production")
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
            "Content-Type": "application/json",
        }

        operation = tool_parameters.get("operation")
        if not operation:
            raise ValueError("operation is required")

        try:
            if operation == "list":
                yield from self._list_customers(api_base_url, headers)
            elif operation == "get":
                customer_id = tool_parameters.get("customer_id")
                if not customer_id:
                    raise ValueError("customer_id is required for get operation")
                yield from self._get_customer(api_base_url, headers, customer_id)
            elif operation == "create":
                yield from self._create_customer(api_base_url, headers, tool_parameters)
            elif operation == "update":
                customer_id = tool_parameters.get("customer_id")
                if not customer_id:
                    raise ValueError("customer_id is required for update operation")
                yield from self._update_customer(api_base_url, headers, customer_id, tool_parameters)
            elif operation == "delete":
                customer_id = tool_parameters.get("customer_id")
                if not customer_id:
                    raise ValueError("customer_id is required for delete operation")
                yield from self._delete_customer(api_base_url, headers, customer_id)
            else:
                raise ValueError(f"Unknown operation: {operation}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _list_customers(self, api_base_url: str, headers: dict) -> Generator[ToolInvokeMessage, None, None]:
        response = httpx.get(f"{api_base_url}/ar/customers", headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            customers = [self._format_customer(c) for c in data.get("customers", [])]
            yield self.create_json_message({
                "success": True,
                "operation": "list",
                "customers": customers,
                "message": f"Found {len(customers)} customers"
            })
        else:
            self._handle_error(response)

    def _get_customer(self, api_base_url: str, headers: dict, customer_id: str) -> Generator[ToolInvokeMessage, None, None]:
        response = httpx.get(f"{api_base_url}/ar/customers/{customer_id}", headers=headers, timeout=15)
        if response.status_code == 200:
            customer = self._format_customer(response.json())
            yield self.create_json_message({
                "success": True,
                "operation": "get",
                "customer": customer,
                "message": "Customer retrieved successfully"
            })
        elif response.status_code == 404:
            raise ValueError(f"Customer not found: {customer_id}")
        else:
            self._handle_error(response)

    def _create_customer(self, api_base_url: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        name = params.get("name")
        email = params.get("email")
        if not name or not email:
            raise ValueError("name and email are required for create operation")

        payload: dict[str, Any] = {"name": name, "email": email}
        address = self._build_address(params)
        if address:
            payload["address"] = address

        response = httpx.post(f"{api_base_url}/ar/customers", headers=headers, json=payload, timeout=15)
        if response.status_code in (200, 201):
            customer = self._format_customer(response.json())
            yield self.create_json_message({
                "success": True,
                "operation": "create",
                "customer": customer,
                "message": "Customer created successfully"
            })
        else:
            self._handle_error(response)

    def _update_customer(self, api_base_url: str, headers: dict, customer_id: str, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        name = params.get("name")
        email = params.get("email")
        if not name or not email:
            raise ValueError("name and email are required for update operation")

        payload: dict[str, Any] = {
            "name": name,
            "email": email,
            "resendOpenInvoices": params.get("resend_open_invoices", False)
        }
        address = self._build_address(params)
        if address:
            payload["address"] = address

        response = httpx.post(f"{api_base_url}/ar/customers/{customer_id}", headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            customer = self._format_customer(response.json())
            yield self.create_json_message({
                "success": True,
                "operation": "update",
                "customer": customer,
                "message": "Customer updated successfully"
            })
        elif response.status_code == 404:
            raise ValueError(f"Customer not found: {customer_id}")
        else:
            self._handle_error(response)

    def _delete_customer(self, api_base_url: str, headers: dict, customer_id: str) -> Generator[ToolInvokeMessage, None, None]:
        response = httpx.delete(f"{api_base_url}/ar/customers/{customer_id}", headers=headers, timeout=15)
        if response.status_code in (200, 204):
            yield self.create_json_message({
                "success": True,
                "operation": "delete",
                "message": f"Customer {customer_id} deleted successfully"
            })
        elif response.status_code == 404:
            raise ValueError(f"Customer not found: {customer_id}")
        else:
            self._handle_error(response)

    def _build_address(self, params: dict) -> dict | None:
        address1 = params.get("address1")
        if not address1:
            return None
        return {
            "address1": address1,
            "address2": params.get("address2"),
            "city": params.get("city", ""),
            "region": params.get("region", ""),
            "postalCode": params.get("postal_code", ""),
            "country": params.get("country", "US"),
        }

    def _format_customer(self, customer: dict) -> dict:
        address = customer.get("address") or {}
        return {
            "id": customer.get("id", ""),
            "name": customer.get("name", ""),
            "email": customer.get("email", ""),
            "address": {
                "address1": address.get("address1", ""),
                "address2": address.get("address2"),
                "city": address.get("city", ""),
                "region": address.get("region", ""),
                "postal_code": address.get("postalCode", ""),
                "country": address.get("country", ""),
            } if address else None,
            "deleted_at": customer.get("deletedAt"),
        }

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed. Check your API token.")

        error_detail = response.json() if response.content else {}

        # Check for AR subscription error
        if response.status_code == 403:
            errors = error_detail.get("errors", {})
            if "subscriptions" in errors:
                raise Exception(
                    "This feature requires a Mercury AR (Accounts Receivable) subscription. "
                    "Please subscribe to AR in your Mercury Dashboard under Plan & Billing. "
                    "Learn more: https://mercury.com/pricing"
                )

        error_msg = error_detail.get("message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
