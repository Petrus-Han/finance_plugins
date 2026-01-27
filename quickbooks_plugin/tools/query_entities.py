import re
import urllib.parse
from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class QueryEntitiesTool(Tool):
    """Tool to run custom SQL-like queries against any QuickBooks entity."""

    SUPPORTED_ENTITIES = [
        "Account", "Bill", "BillPayment", "Budget", "Class", "CompanyInfo",
        "CreditMemo", "Customer", "Department", "Deposit", "Employee",
        "Estimate", "Invoice", "Item", "JournalEntry", "Payment",
        "PaymentMethod", "Preferences", "Purchase", "PurchaseOrder",
        "RefundReceipt", "SalesReceipt", "TaxCode", "TaxRate", "Term",
        "TimeActivity", "Transfer", "Vendor", "VendorCredit"
    ]

    # Dangerous SQL keywords that could indicate injection attempts
    _DANGEROUS_KEYWORDS = [
        "DELETE", "UPDATE", "INSERT", "DROP", "ALTER", "TRUNCATE",
        "CREATE", "EXEC", "EXECUTE", "UNION", "INTO", "--", "/*", "*/"
    ]

    def _validate_custom_query(self, query: str) -> None:
        """Validate custom query to prevent injection attacks.

        Ensures the query:
        - Starts with SELECT
        - Does not contain dangerous keywords
        - References only supported entity types
        """
        if not query or not query.strip():
            raise ValueError("Custom query cannot be empty")

        normalized = query.strip().upper()

        # Must start with SELECT
        if not normalized.startswith("SELECT"):
            raise ValueError(
                "Custom query must start with SELECT. "
                "Only read operations are allowed."
            )

        # Check for dangerous keywords
        for keyword in self._DANGEROUS_KEYWORDS:
            # Use word boundary matching for SQL keywords, literal match for comment markers
            if keyword.startswith("-") or keyword.startswith("/") or keyword.startswith("*"):
                if keyword in normalized:
                    raise ValueError(
                        f"Custom query contains forbidden pattern: {keyword}. "
                        "Only SELECT queries are allowed."
                    )
            else:
                # Word boundary check for SQL keywords
                pattern = rf"\b{keyword}\b"
                if re.search(pattern, normalized):
                    raise ValueError(
                        f"Custom query contains forbidden keyword: {keyword}. "
                        "Only SELECT queries are allowed."
                    )

        # Validate FROM clause references a supported entity
        from_match = re.search(r"\bFROM\s+(\w+)", normalized)
        if from_match:
            entity = from_match.group(1)
            # Check against supported entities (case-insensitive)
            entity_upper_list = [e.upper() for e in self.SUPPORTED_ENTITIES]
            if entity not in entity_upper_list:
                raise ValueError(
                    f"Unsupported entity type in query: {entity}. "
                    f"Supported entities: {', '.join(self.SUPPORTED_ENTITIES)}"
                )

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

        entity_type = tool_parameters.get("entity_type")
        query_string = tool_parameters.get("query_string", "")
        custom_query = tool_parameters.get("custom_query", "")
        max_results = tool_parameters.get("max_results", 100)

        try:
            if custom_query:
                # Validate custom query for injection protection
                self._validate_custom_query(custom_query)
                query = custom_query
            elif entity_type:
                if entity_type not in self.SUPPORTED_ENTITIES:
                    raise ValueError(f"Unsupported entity type: {entity_type}. Supported: {', '.join(self.SUPPORTED_ENTITIES)}")

                query = f"SELECT * FROM {entity_type}"
                if query_string:
                    query += f" WHERE {query_string}"
                if max_results:
                    query += f" MAXRESULTS {max_results}"
            else:
                raise ValueError("Either entity_type or custom_query is required")

            encoded_query = urllib.parse.quote(query)
            url = f"{api_base_url}/company/{realm_id}/query?query={encoded_query}&minorversion=65"
            response = httpx.get(url, headers=headers, timeout=30)

            if response.status_code == 200:
                data = response.json()
                query_response = data.get("QueryResponse", {})

                # Find the entity key in response
                result_key = None
                results = []
                for key in query_response:
                    if key not in ["startPosition", "maxResults", "totalCount"]:
                        result_key = key
                        results = query_response[key]
                        break

                result = {
                    "success": True,
                    "entity_type": result_key or entity_type,
                    "results": results,
                    "count": len(results),
                    "total_count": query_response.get("totalCount"),
                    "query": query,
                    "message": f"Query executed successfully, found {len(results)} results"
                }
                for key, value in result.items():
                    yield self.create_variable_message(key, value)
                yield self.create_json_message(result)
            else:
                self._handle_error(response)

        except httpx.HTTPError as e:
            raise Exception(f"Network error: {str(e)}") from e

    def _handle_error(self, response: httpx.Response) -> None:
        if response.status_code == 401:
            raise ToolProviderCredentialValidationError("Authentication failed.")
        error_detail = response.json() if response.content else {}
        error_msg = error_detail.get("Fault", {}).get("Error", [{}])[0].get("Message", response.text)
        raise Exception(f"API error {response.status_code}: {error_msg}")
