import urllib.parse
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class ItemManagementTool(Tool):
    """Tool to manage items (products, services, inventory) in QuickBooks."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        access_token = self.runtime.credentials.get("access_token")
        realm_id = self.runtime.credentials.get("realm_id")

        if not access_token or not realm_id:
            raise ToolProviderCredentialValidationError("QuickBooks credentials required.")

        environment = self.runtime.credentials.get("environment", "sandbox")
        api_base_url = f"https://{'sandbox-' if environment == 'sandbox' else ''}quickbooks.api.intuit.com/v3"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        operation = tool_parameters.get("operation")
        if not operation:
            raise ValueError("operation is required")

        try:
            if operation == "create":
                yield from self._create(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "read":
                yield from self._read(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "update":
                yield from self._update(api_base_url, realm_id, headers, tool_parameters)
            elif operation == "query":
                yield from self._query(api_base_url, realm_id, headers, tool_parameters)
            else:
                raise ValueError(f"Unknown operation: {operation}")
        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _create(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        name = params.get("name")
        item_type = params.get("item_type")

        if not name or not item_type:
            raise ValueError("name and item_type are required for create")

        payload: dict[str, Any] = {
            "Name": name,
            "Type": item_type
        }

        if params.get("income_account_id"):
            payload["IncomeAccountRef"] = {"value": params["income_account_id"]}
        if params.get("expense_account_id"):
            payload["ExpenseAccountRef"] = {"value": params["expense_account_id"]}
        if params.get("asset_account_id"):
            payload["AssetAccountRef"] = {"value": params["asset_account_id"]}
        if params.get("unit_price") is not None:
            payload["UnitPrice"] = params["unit_price"]
        if params.get("purchase_cost") is not None:
            payload["PurchaseCost"] = params["purchase_cost"]
        if params.get("description"):
            payload["Description"] = params["description"]
        if params.get("sku"):
            payload["Sku"] = params["sku"]
        if params.get("taxable"):
            payload["Taxable"] = params["taxable"]

        # Inventory-specific fields
        if item_type == "Inventory":
            payload["TrackQtyOnHand"] = True
            if params.get("qty_on_hand") is not None:
                payload["QtyOnHand"] = params["qty_on_hand"]
            else:
                payload["QtyOnHand"] = 0
            # InvStartDate defaults to today if not specified
            from datetime import date
            payload["InvStartDate"] = date.today().isoformat()

        url = f"{api_base_url}/company/{realm_id}/item?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            yield self.create_json_message({
                "success": True,
                "operation": "create",
                "item": self._format(data.get("Item", {})),
                "message": "Item created successfully"
            })
        else:
            self._handle_error(response)

    def _read(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        item_id = params.get("item_id")
        if not item_id:
            raise ValueError("item_id is required for read")

        url = f"{api_base_url}/company/{realm_id}/item/{item_id}?minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            yield self.create_json_message({
                "success": True,
                "operation": "read",
                "item": self._format(data.get("Item", {})),
                "message": "Item retrieved successfully"
            })
        else:
            self._handle_error(response)

    def _update(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        item_id = params.get("item_id")
        sync_token = params.get("sync_token")
        name = params.get("name")
        item_type = params.get("item_type")

        if not all([item_id, sync_token, name, item_type]):
            raise ValueError("item_id, sync_token, name, and item_type are required for update")

        payload: dict[str, Any] = {
            "Id": item_id,
            "SyncToken": sync_token,
            "Name": name,
            "Type": item_type
        }

        if params.get("income_account_id"):
            payload["IncomeAccountRef"] = {"value": params["income_account_id"]}
        if params.get("expense_account_id"):
            payload["ExpenseAccountRef"] = {"value": params["expense_account_id"]}
        if params.get("unit_price") is not None:
            payload["UnitPrice"] = params["unit_price"]
        if params.get("purchase_cost") is not None:
            payload["PurchaseCost"] = params["purchase_cost"]
        if params.get("description"):
            payload["Description"] = params["description"]
        if params.get("sku"):
            payload["Sku"] = params["sku"]
        if params.get("taxable") is not None:
            payload["Taxable"] = params["taxable"]

        url = f"{api_base_url}/company/{realm_id}/item?minorversion=65"
        response = httpx.post(url, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            yield self.create_json_message({
                "success": True,
                "operation": "update",
                "item": self._format(data.get("Item", {})),
                "message": "Item updated successfully"
            })
        else:
            self._handle_error(response)

    def _query(self, api_base_url: str, realm_id: str, headers: dict, params: dict) -> Generator[ToolInvokeMessage, None, None]:
        query_string = params.get("query_string", "")
        query = "SELECT * FROM Item"
        if query_string:
            query += f" WHERE {query_string}"

        encoded_query = urllib.parse.quote(query)
        url = f"{api_base_url}/company/{realm_id}/query?query={encoded_query}&minorversion=65"
        response = httpx.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            data = response.json()
            items = data.get("QueryResponse", {}).get("Item", [])
            yield self.create_json_message({
                "success": True,
                "operation": "query",
                "items": [self._format(item) for item in items],
                "count": len(items),
                "message": f"Found {len(items)} items"
            })
        else:
            self._handle_error(response)

    def _format(self, item: dict) -> dict:
        return {
            "id": item.get("Id"),
            "sync_token": item.get("SyncToken"),
            "name": item.get("Name"),
            "type": item.get("Type"),
            "description": item.get("Description"),
            "sku": item.get("Sku"),
            "unit_price": item.get("UnitPrice"),
            "purchase_cost": item.get("PurchaseCost"),
            "qty_on_hand": item.get("QtyOnHand"),
            "taxable": item.get("Taxable"),
            "active": item.get("Active"),
            "income_account_id": item.get("IncomeAccountRef", {}).get("value") if item.get("IncomeAccountRef") else None,
            "expense_account_id": item.get("ExpenseAccountRef", {}).get("value") if item.get("ExpenseAccountRef") else None,
            "asset_account_id": item.get("AssetAccountRef", {}).get("value") if item.get("AssetAccountRef") else None,
        }

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed.")
        error_detail = response.json() if response.content else {}
        error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
