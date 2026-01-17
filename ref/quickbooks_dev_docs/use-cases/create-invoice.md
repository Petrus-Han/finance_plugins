# Create Basic Invoices

> QuickBooks Online API - Invoice Creation Workflow

Invoicing is a fundamental accounting task for most businesses. Small businesses use invoices when they sell products and services, but expect customers to pay for them later on.

The **invoice** entity is a critical part of our API. Creating, sending, and managing invoices involves many other API entities including Customer, Item, sales tax, and payment processing.

---

## Overview

**Required Entities:**
- [Invoice](../api-reference/invoice.md) - The invoice itself
- [Item](../api-reference/item.md) - Products and services being sold
- [Customer](../api-reference/customer.md) - Who you're selling to

**Related Entities:**
- [Payment](../api-reference/payment.md) - Customer payments
- [TaxCode](../api-reference/taxcode.md) - Sales tax handling

---

## Step 1: Understand Invoice Structure

Every invoice requires two components:
1. **A line item** - The product or service being sold
2. **A customer** - The person or business you're selling to

### Basic Invoice Payload

```json
{
  "Line": [
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 100.0,
      "SalesItemLineDetail": {
        "ItemRef": {
          "name": "Concrete",
          "value": "3"
        }
      }
    }
  ],
  "CustomerRef": {
    "value": "1"
  }
}
```

### Understanding the Payload

| Field | Description |
|-------|-------------|
| `Line[]` | Array of line items on the invoice |
| `DetailType` | Type of line (SalesItemLineDetail, GroupLineDetail, etc.) |
| `Amount` | Cost of the item |
| `ItemRef.value` | ID of the item being sold |
| `ItemRef.name` | Name of the item |
| `CustomerRef.value` | ID of the customer |

**Key Constraint:** Only **one** `CustomerRef` object per invoice.

---

## Step 2: Create a Basic Invoice

### API Request

```http
POST /v3/company/{realmId}/invoice
Content-Type: application/json
Authorization: Bearer {access_token}
```

### Request Body

```json
{
  "Line": [
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 100.0,
      "SalesItemLineDetail": {
        "ItemRef": {
          "value": "1",
          "name": "Services"
        }
      }
    }
  ],
  "CustomerRef": {
    "value": "1"
  }
}
```

### Python Example

```python
def create_invoice(client, customer_id, items):
    """
    Create an invoice in QuickBooks.
    
    Args:
        client: QuickBooks API client
        customer_id: ID of the customer
        items: List of (item_id, item_name, amount) tuples
    """
    lines = []
    for item_id, item_name, amount in items:
        lines.append({
            "DetailType": "SalesItemLineDetail",
            "Amount": amount,
            "SalesItemLineDetail": {
                "ItemRef": {
                    "value": item_id,
                    "name": item_name
                }
            }
        })
    
    invoice = {
        "Line": lines,
        "CustomerRef": {
            "value": customer_id
        }
    }
    
    return client.create_invoice(invoice)
```

---

## Step 3: Add Multiple Items

Each unique item gets its own line with name, description, quantity, and cost.

```json
{
  "Line": [
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 100.0,
      "SalesItemLineDetail": {
        "ItemRef": {"value": "1", "name": "Services"}
      }
    },
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 50.0,
      "SalesItemLineDetail": {
        "ItemRef": {"value": "8", "name": "Lighting"}
      }
    },
    {
      "DetailType": "SalesItemLineDetail",
      "Amount": 75.0,
      "SalesItemLineDetail": {
        "ItemRef": {"value": "7", "name": "Installation"}
      }
    }
  ],
  "CustomerRef": {
    "value": "1"
  }
}
```

---

## Step 4: Add Bundles, Descriptions, and Discounts

### Line Detail Types

| DetailType | Purpose |
|------------|---------|
| `SalesItemLineDetail` | Standard item sale |
| `GroupLineDetail` | Bundle of items |
| `DescriptionOnly` | Text description line |
| `DiscountLineDetail` | Discount line |
| `SubTotalLineDetail` | Subtotal line |

### Invoice with Bundle and Discount

```json
{
  "Line": [
    {
      "DetailType": "GroupLineDetail",
      "GroupLineDetail": {
        "GroupItemRef": {
          "value": "19",
          "name": "Bundle One"
        },
        "Quantity": 2
      }
    },
    {
      "Description": "Additional info here",
      "DetailType": "DescriptionOnly"
    },
    {
      "DetailType": "DiscountLineDetail",
      "DiscountLineDetail": {
        "PercentBased": true,
        "DiscountPercent": 10
      }
    }
  ],
  "CustomerRef": {
    "value": "1"
  }
}
```

---

## Step 5: Handle Sales Tax

### US-Based Companies (Automated Sales Tax)

Since November 2017, US QuickBooks Online companies use **Automated Sales Tax (AST)**. Tax is automatically calculated based on:
- Shipping address
- Company location

No manual tax configuration needed - QuickBooks handles it.

### Non-US Companies (Manual Tax)

Non-US companies use manual tax codes and tax services. Use:
- `TaxCodeRef` to specify tax treatment
- `TxnTaxDetail` for tax details

---

## Step 6: Add Custom Fields

Query the **Preferences** entity to check if the user has custom fields:

```sql
SELECT * FROM Preferences
```

Add custom fields to invoice:

```json
{
  "CustomField": [
    {
      "DefinitionId": "1",
      "Name": "PO Number",
      "Type": "StringType",
      "StringValue": "PO-12345"
    }
  ]
}
```

---

## Step 7: Link Invoices to Payments

Payments received for an invoice appear in the `LinkedTxn` attribute:

```json
{
  "LinkedTxn": [
    {
      "TxnId": "123",
      "TxnType": "Payment"
    }
  ]
}
```

See [Manage Linked Transactions](./manage-linked-transactions.md) for details.

---

## Common Errors

### Invalid Reference ID (Error 2500)

```json
{
  "Fault": {
    "Error": [{
      "Message": "Invalid Reference Id",
      "Detail": "Something you're trying to use has been made inactive. Check the fields with accounts, customers, items, vendors or employees.",
      "code": "2500"
    }],
    "type": "ValidationFault"
  }
}
```

**Solution:** Verify the referenced Item or Customer exists and is active.

---

## Query Items and Customers

### Find Items

```sql
SELECT * FROM Item WHERE Active = true
```

### Find Customers

```sql
SELECT * FROM Customer WHERE Active = true
```

### Find Specific Item

```sql
SELECT * FROM Item WHERE Id = '3'
```

---

## SDK Examples

- [Java Invoice Example](https://github.com/IntuitDeveloper/QBOConceptsTutorial-Java/blob/master/src/main/java/com/intuit/developer/tutorials/controller/InvoiceController.java)
- [.NET Invoice Example](https://github.com/IntuitDeveloper/QBOConceptsTutorial-DotNet/blob/master/MvcCodeFlowClientManual/Controllers/InvoicingController.cs)
- [PHP Invoice Example](https://github.com/IntuitDeveloper/QBOConceptsTutorial-PHP/blob/master/InvoiceAndBilling.php)

---

## Related Documentation

- [Invoice Entity Reference](../api-reference/invoice.md)
- [Customer Entity Reference](../api-reference/customer.md)
- [Item Entity Reference](../api-reference/item.md)
- [Manage Linked Transactions](./manage-linked-transactions.md)
- [Calculate Sales Tax](./calculate-sales-tax.md)
