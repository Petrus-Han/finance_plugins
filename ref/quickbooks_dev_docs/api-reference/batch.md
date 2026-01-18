# Batch

The batch operation enables an application to perform multiple operations in a single request. For example, in a single batch request an application can create a customer, update an invoice, and read an account. Compared to multiple requests, a single batch request can improve an application's performance by decreasing network roundtrips and increasing throughput. The individual operations within a batch request are called BatchItemRequest objects.

## Business Rules

- The maximum number of payloads in a single BatchItemRequest is **30**.
- The maximum number of requests to the batch endpoint per minute per realmID is **40**.
- Execution order of BatchItemRequest objects should not be assumed.
- BatchItemRequest objects are treated independently; a given object cannot depend on another one within the same batch operation. For example, a newly created customer is not available for a subsequent invoice create operation within the same batch operation. You would need to create the customer object first, either autonomously or via a batch request, and then create the invoice object in a subsequent batch request.
- A batch request is authenticated once. This single authentication applies to all BatchItemRequest objects in the request.
- The maximum number of objects that can be returned in a response is **1000**.

## The Batch Object

### Request Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **BatchItemRequest** | BatchItemRequest | Required | A wrapper around all request objects for this batch operation. |

### BatchItemRequest Child Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **bId** | String | Unique identifier for this batch item request. Used to correlate responses with requests. |
| **operation** | String | The operation to perform: "create", "update", "delete", or omit for query. |
| **Query** | String | SQL-like query string for read operations. |
| **[EntityName]** | Object | The entity object (Vendor, Invoice, SalesReceipt, etc.) to operate on. |

### Response Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **BatchItemResponse** | BatchItemResponse | Required | A wrapper around all response objects for this batch operation. |

### BatchItemResponse Child Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **bId** | String | Identifier correlating this response with the corresponding request. |
| **[EntityName]** | Object | The resulting entity object for successful operations. |
| **QueryResponse** | Object | Query results for query operations. |
| **Fault** | Object | Error information if the operation failed. |

## Sample Batch Request

### Request

```
POST /v3/company/<realmID>/batch
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

This example includes four BatchItemRequest objects:
1. Create a Vendor
2. Delete an Invoice
3. Update a SalesReceipt (sparse update)
4. Query SalesReceipts

```json
{
  "BatchItemRequest": [
    {
      "bId": "bid1",
      "Vendor": {
        "DisplayName": "Smith Family Store"
      },
      "operation": "create"
    },
    {
      "bId": "bid2",
      "operation": "delete",
      "Invoice": {
        "SyncToken": "0",
        "Id": "129"
      }
    },
    {
      "SalesReceipt": {
        "PrivateNote": "A private note.",
        "SyncToken": "0",
        "domain": "QBO",
        "Id": "11",
        "sparse": true
      },
      "bId": "bid3",
      "operation": "update"
    },
    {
      "Query": "select * from SalesReceipt where TotalAmt > '300.00'",
      "bId": "bid4"
    }
  ]
}
```

### Response

The response shows mixed results - some operations may succeed while others fail:

```json
{
  "BatchItemResponse": [
    {
      "Fault": {
        "type": "ValidationFault",
        "Error": [
          {
            "Message": "Duplicate Name Exists Error",
            "code": "6240",
            "Detail": "The name supplied already exists. : Another customer, vendor or employee is already using this name. Please use a different name.",
            "element": ""
          }
        ]
      },
      "bId": "bid1"
    },
    {
      "Fault": {
        "type": "ValidationFault",
        "Error": [
          {
            "Message": "Object Not Found",
            "code": "610",
            "Detail": "Object Not Found : Something you're trying to use has been made inactive. Check the fields with accounts, customers, items, vendors or employees.",
            "element": ""
          }
        ]
      },
      "bId": "bid2"
    },
    {
      "Fault": {
        "type": "ValidationFault",
        "Error": [
          {
            "Message": "Stale Object Error",
            "code": "5010",
            "Detail": "Stale Object Error : You and root were working on this at the same time. root finished before you did, so your work was not saved.",
            "element": ""
          }
        ]
      },
      "bId": "bid3"
    },
    {
      "bId": "bid4",
      "QueryResponse": {
        "SalesReceipt": [
          {
            "TxnDate": "2015-08-25",
            "domain": "QBO",
            "CurrencyRef": {
              "name": "United States Dollar",
              "value": "USD"
            },
            "PrintStatus": "NotSet",
            "PaymentRefNum": "10264",
            "TotalAmt": 337.5,
            "Line": [
              {
                "Description": "Custom Design",
                "DetailType": "SalesItemLineDetail",
                "SalesItemLineDetail": {
                  "TaxCodeRef": {
                    "value": "NON"
                  },
                  "Qty": 4.5,
                  "UnitPrice": 75,
                  "ItemRef": {
                    "name": "Design",
                    "value": "4"
                  }
                },
                "LineNum": 1,
                "Amount": 337.5,
                "Id": "1"
              },
              {
                "DetailType": "SubTotalLineDetail",
                "Amount": 337.5,
                "SubTotalLineDetail": {}
              }
            ],
            "ApplyTaxAfterDiscount": false,
            "DocNumber": "1003",
            "PrivateNote": "A private note.",
            "sparse": false,
            "DepositToAccountRef": {
              "name": "Checking",
              "value": "35"
            },
            "CustomerMemo": {
              "value": "Thank you for your business and have a great day!"
            },
            "Balance": 0,
            "CustomerRef": {
              "name": "Dylan Sollfrank",
              "value": "6"
            },
            "TxnTaxDetail": {
              "TotalTax": 0
            },
            "SyncToken": "1",
            "PaymentMethodRef": {
              "name": "Check",
              "value": "2"
            },
            "EmailStatus": "NotSet",
            "BillAddr": {
              "Lat": "INVALID",
              "Long": "INVALID",
              "Id": "49",
              "Line1": "Dylan Sollfrank"
            },
            "MetaData": {
              "CreateTime": "2015-08-27T14:59:48-07:00",
              "LastUpdatedTime": "2016-04-15T09:01:10-07:00"
            },
            "CustomField": [
              {
                "DefinitionId": "1",
                "Type": "StringType",
                "Name": "Crew #"
              }
            ],
            "Id": "11"
          }
        ],
        "startPosition": 1,
        "maxResults": 1
      }
    }
  ],
  "time": "2016-04-15T09:01:18.141-07:00"
}
```

## Supported Operations

| Operation | Description |
|-----------|-------------|
| **create** | Create a new entity |
| **update** | Update an existing entity (full or sparse) |
| **delete** | Delete an entity |
| **query** | Query entities (omit operation, use Query attribute) |

## Error Handling

Each BatchItemResponse may contain a `Fault` object if the operation failed. The Fault object includes:

| Field | Description |
|-------|-------------|
| **type** | The type of fault (e.g., "ValidationFault") |
| **Error** | Array of error objects with Message, code, Detail, and element fields |

Common error codes:
- **6240**: Duplicate Name Exists Error
- **610**: Object Not Found
- **5010**: Stale Object Error (concurrent modification)
