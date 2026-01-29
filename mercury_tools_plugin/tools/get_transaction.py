from collections.abc import Generator
from typing import Any

import httpx

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GetTransactionTool(Tool):
    """Tool to retrieve details for a specific Mercury transaction."""

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the get_transaction tool to fetch transaction details.

        Args:
            tool_parameters: Dictionary containing:
                - transaction_id: The transaction ID (required)

        Returns:
            Detailed transaction information
        """
        # Get parameters
        account_id = tool_parameters.get("account_id", "")
        transaction_id = tool_parameters.get("transaction_id", "")
        if not transaction_id:
            raise ValueError("Transaction ID is required.")

        # Get credentials
        access_token = self.runtime.credentials.get("access_token")
        if not access_token:
            raise ValueError("Mercury API Access Token is required.")

        # Get API environment
        api_environment = self.runtime.credentials.get("api_environment", "production")

        # Determine API base URL based on environment
        if api_environment == "sandbox":
            api_base_url = "https://api-sandbox.mercury.com/api/v1"
        else:
            api_base_url = "https://api.mercury.com/api/v1"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json;charset=utf-8",
        }

        try:
            # Use different endpoint based on whether account_id is provided
            if account_id:
                url = f"{api_base_url}/account/{account_id}/transaction/{transaction_id}"
            else:
                url = f"{api_base_url}/transaction/{transaction_id}"

            response = httpx.get(url, headers=headers, timeout=15)

            if response.status_code == 200:
                txn = response.json()

                # Build comprehensive output with all Mercury API fields
                transaction_info = {
                    # Core identification
                    "id": txn.get("id", ""),
                    "account_id": txn.get("accountId", ""),

                    # Status: pending | sent | cancelled | failed | reversed | blocked
                    "status": txn.get("status", ""),

                    # Financial data
                    "amount": txn.get("amount", 0),
                    "kind": txn.get("kind", ""),  # externalTransfer, internalTransfer, etc.

                    # Counterparty info
                    "counterparty_id": txn.get("counterpartyId", ""),
                    "counterparty_name": txn.get("counterpartyName", ""),
                    "counterparty_nickname": txn.get("counterpartyNickname", ""),

                    # Descriptions and notes
                    "bank_description": txn.get("bankDescription", ""),
                    "note": txn.get("note", ""),
                    "external_memo": txn.get("externalMemo", ""),

                    # Timestamps
                    "created_at": txn.get("createdAt", ""),
                    "posted_at": txn.get("postedAt", ""),
                    "estimated_delivery_date": txn.get("estimatedDeliveryDate", ""),
                    "failed_at": txn.get("failedAt", ""),

                    # Tracking and reference
                    "tracking_number": txn.get("trackingNumber", ""),
                    "check_number": txn.get("checkNumber", ""),
                    "fee_id": txn.get("feeId", ""),

                    # Category data
                    "category_id": txn.get("categoryData", {}).get("id", "") if txn.get("categoryData") else "",
                    "category_name": txn.get("categoryData", {}).get("name", "") if txn.get("categoryData") else "",

                    # Compliance and metadata
                    "compliant_with_receipt_policy": txn.get("compliantWithReceiptPolicy", False),
                    "dashboard_link": txn.get("dashboardLink", ""),
                    "credit_account_period_id": txn.get("creditAccountPeriodId", ""),
                }

                # Include currency exchange info if present
                currency_exchange = txn.get("currencyExchangeInfo", {})
                if currency_exchange:
                    transaction_info["currency_exchange"] = {
                        "converted_amount": currency_exchange.get("convertedAmount", 0),
                        "exchange_rate": currency_exchange.get("exchangeRate", 0),
                        "from_currency": currency_exchange.get("fromCurrency", ""),
                        "to_currency": currency_exchange.get("toCurrency", ""),
                        "fee": currency_exchange.get("fee", 0),
                    }

                # Include details (routing info, card info, etc.)
                details = txn.get("details", {})
                if details:
                    # Electronic routing (ACH)
                    routing_info = details.get("electronicRoutingInfo", {})
                    if routing_info:
                        transaction_info["routing_details"] = {
                            "account_number": routing_info.get("accountNumber", ""),
                            "routing_number": routing_info.get("routingNumber", ""),
                            "bank_name": routing_info.get("bankName", ""),
                            "account_type": routing_info.get("accountType", ""),
                        }

                    # Domestic wire routing
                    domestic_wire = details.get("domesticWireRoutingInfo", {})
                    if domestic_wire:
                        transaction_info["domestic_wire_details"] = {
                            "account_number": domestic_wire.get("accountNumber", ""),
                            "routing_number": domestic_wire.get("routingNumber", ""),
                            "address": domestic_wire.get("address", {}),
                        }

                    # International wire routing
                    intl_wire = details.get("internationalWireRoutingInfo", {})
                    if intl_wire:
                        transaction_info["international_wire_details"] = {
                            "swift_code": intl_wire.get("swiftCode", ""),
                            "iban": intl_wire.get("iban", ""),
                            "bank_name": intl_wire.get("bankName", ""),
                            "country": intl_wire.get("country", ""),
                        }

                    # Extract credit card info (for credit card transactions)
                    credit_card_info = details.get("creditCardInfo", {})
                    if credit_card_info:
                        transaction_info["credit_card_id"] = credit_card_info.get("id", "")
                        transaction_info["credit_card_email"] = credit_card_info.get("email", "")
                        transaction_info["credit_card_payment_method"] = credit_card_info.get("paymentMethod", "")
                        transaction_info["credit_card_last_four"] = credit_card_info.get("lastFour", "")

                    # Extract debit card info (for debit card transactions)
                    debit_card_info = details.get("debitCardInfo", {})
                    if debit_card_info:
                        transaction_info["debit_card_id"] = debit_card_info.get("id", "")
                        transaction_info["debit_card_last_four"] = debit_card_info.get("lastFour", "")

                # Include attachments with full details
                attachments = txn.get("attachments", [])
                if attachments:
                    transaction_info["attachments"] = [
                        {
                            "id": att.get("id", ""),
                            "file_name": att.get("fileName", ""),
                            "url": att.get("url", ""),
                            "attachment_type": att.get("attachmentType", ""),  # checkImage | receipt | other
                        }
                        for att in attachments
                    ]

                # Yield scalar fields as variables for direct access
                for key, value in transaction_info.items():
                    if not isinstance(value, (list, dict)):
                        yield self.create_variable_message(key, value)

                # Yield full JSON for complete data including nested structures
                yield self.create_json_message(transaction_info)

            elif response.status_code == 404:
                raise ValueError(f"Transaction with ID '{transaction_id}' not found.")
            elif response.status_code == 401:
                raise ToolProviderCredentialValidationError(
                    "Authentication failed. Please check your Mercury API access token."
                )
            else:
                error_detail = response.json() if response.content else {}
                error_msg = error_detail.get("message", response.text)
                raise Exception(f"Failed to retrieve transaction: {response.status_code} - {error_msg}")

        except httpx.HTTPError as e:
            raise Exception(f"Network error while fetching transaction: {str(e)}") from e
