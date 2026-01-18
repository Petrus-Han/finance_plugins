# Item

An item is a thing that your company buys, sells, or re-sells, such as products and services. An item is shown as a line on an invoice or other sales form. The Item.Type attribute, which specifies how the item is used, has one of the following values:

## Item Types

| Type | Description |
|------|-------------|
| **Inventory** | Used in transactions to track merchandise that your company buys, stocks, and re-sells as inventory. QuickBooks tracks the current number of items in inventory and the monetary value of that inventory, based on the method of accounting called FIFO (First-In-First-Out). As inventory items are sold, QuickBooks reduces the quantity on hand. If you track inventory of an item, you must include IncomeAccountRef, ExpenseAccountRef, AssetAccountRef, InvStartDate, Type, Name, and QtyOnHand. |
| **Service** | Used in transactions for services you charge on the purchase and/or items you sell. For example, specialized labor, consulting hours, and professional fees. |
| **NonInventory** | Used in transactions for non-inventory items. These are goods you buy or sell that are not tracked for inventory purposes. Examples include office supplies. |
| **Category** | Used to organize groups of items. Categories can be nested up to 4 levels deep. |

## Business Rules

- For UK, different coexistence rules apply per edition type. Click [here](https://developer.intuit.com/app/developer/qbo/docs/develop/tutorials-and-guides/manage-items) for more information.
- For inventory items:
  - The AssetAccountRef, InvStartDate, QtyOnHand, ExpenseAccountRef, and IncomeAccountRef attributes are required for Inventory item types.
  - After creating an item, you cannot change its type from Inventory to another type.
- For Canada and UK companies, IncomeAccountRef and ExpenseAccountRef must be populated even if you don't subscribe to Plus or Essentials.

## The Item Object

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String, read only, filterable, sortable | Unique identifier for this object. Sort order is ASC by default. *Required for update* |
| **Name** | String (max 100 chars), filterable, sortable | Name of the item. This value must be unique. *Required* |
| **Type** | ItemTypeEnum, filterable, sortable | Classification that specifies the use of this item. Possible values: Inventory, Service, NonInventory. *Required* |
| **SyncToken** | String, read only | Version number of the object. It is used to lock an object for use by one app at a time. *Required for update* |
| **InvStartDate** | Date | Date of opening balance for the inventory transaction. *Conditionally required for Inventory items* |
| **QtyOnHand** | Decimal | Current quantity of the inventory items available for sale. Not used for Service or NonInventory item types. *Conditionally required for Inventory items* |
| **AssetAccountRef** | ReferenceType | Reference to the Inventory Asset account that tracks the current value of the inventory. Must be an account with Account.AccountType set to Other Current Asset. *Conditionally required for Inventory items* |
| **IncomeAccountRef** | ReferenceType | Reference to the posting account (that records the proceeds from the sale of this item). Must be an account with account type of Sales of Product Income. *Conditionally required for Inventory and Service items* |
| **ExpenseAccountRef** | ReferenceType | Reference to the expense account used to pay the vendor for this item. Must be an account with account type of Cost of Goods Sold. *Conditionally required for Inventory, NonInventory, and Service items* |
| **Sku** | String (max 100 chars) | The stock keeping unit (SKU) for this item. |
| **Description** | String (max 4000 chars) | Description of the item. |
| **PurchaseDesc** | String (max 1000 chars) | Purchase description for the item. |
| **UnitPrice** | Decimal, sortable (max 99999999999) | Price/Rate column value - unit price, discount, or tax rate. |
| **PurchaseCost** | Decimal, sortable (max 99999999999) | Amount paid when buying or ordering the item. |
| **Taxable** | Boolean, filterable | If true, transactions for this item are taxable. |
| **Active** | Boolean, filterable | If true, the object is currently enabled for use by QuickBooks. Default is true. |
| **ReorderPoint** | Decimal | The minimum quantity of this item that you want to keep in stock. |
| **Level** | Integer, read only | Specifies the level of the hierarchy in which the entity is located. Limited to 5 levels. |
| **FullyQualifiedName** | String, read only, filterable | Fully qualified name prepending topmost parent. Takes the form of Item:SubItem. Limited to 5 levels. |
| **SubItem** | Boolean, filterable | If true, this is a sub-item. If false, it's a top-level item. Default is false. *Conditionally required for sub-items* |
| **ParentRef** | ReferenceType | Reference to the parent item in hierarchy. Required if SubItem is true. |
| **AbatementRate** | Decimal | Sales tax abatement rate (India locales only). |
| **ReverseChargeRate** | Decimal | Sales tax reverse charge rate (India locales only). |
| **ServiceType** | String | Sales tax service type (India locales only). |
| **ItemCategoryType** | String | Item type: Product, Service. (India locales only). |
| **PrefVendorRef** | ReferenceType | Reference to the preferred vendor for this item. |
| **ClassRef** | ReferenceType | Reference to the Class associated with the item. *minorVersion: 41* |
| **Source** | String, read only | Originating source of the Item. Valid values include: QBCommerce. *minorVersion: 59* |
| **TaxClassificationRef** | ReferenceType | Tax classification for the item. *minorVersion: 34* |
| **MetaData** | ModificationMetaData | Descriptive information about the entity. Read only. |

### Sample Object

```json
{
  "Item": {
    "FullyQualifiedName": "Rock Fountain",
    "domain": "QBO",
    "Id": "5",
    "Name": "Rock Fountain",
    "TrackQtyOnHand": true,
    "Type": "Inventory",
    "PurchaseCost": 125,
    "QtyOnHand": 2,
    "IncomeAccountRef": {
      "name": "Sales of Product Income",
      "value": "79"
    },
    "AssetAccountRef": {
      "name": "Inventory Asset",
      "value": "81"
    },
    "Taxable": true,
    "MetaData": {
      "CreateTime": "2014-09-16T10:42:19-07:00",
      "LastUpdatedTime": "2014-09-19T13:16:17-07:00"
    },
    "sparse": false,
    "Active": true,
    "SyncToken": "2",
    "InvStartDate": "2014-09-19",
    "UnitPrice": 275,
    "ExpenseAccountRef": {
      "name": "Cost of Goods Sold",
      "value": "80"
    },
    "PurchaseDesc": "Rock Fountain",
    "Description": "Rock Fountain"
  },
  "time": "2014-09-19T13:16:17.413-07:00"
}
```

## Create an Item

### Request

```
POST /v3/company/<realmID>/item
Content-Type: application/json
```

**Production Base URL:** `https://quickbooks.api.intuit.com`
**Sandbox Base URL:** `https://sandbox-quickbooks.api.intuit.com`

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **Name** | String | Name of the item (must be unique). *Required* |
| **Type** | String | Classification: Inventory, Service, NonInventory. *Required* |
| **IncomeAccountRef** | ReferenceType | Reference to the sales account. *Conditionally required for Inventory and Service* |
| **ExpenseAccountRef** | ReferenceType | Reference to the expense account. *Conditionally required for Inventory, NonInventory, and Service* |
| **AssetAccountRef** | ReferenceType | Reference to the inventory asset account. *Conditionally required for Inventory* |
| **InvStartDate** | Date | Date of opening balance. *Conditionally required for Inventory* |
| **QtyOnHand** | Decimal | Initial quantity on hand. *Conditionally required for Inventory* |

### Sample Request Body (Service Item)

```json
{
  "Name": "Garden Design",
  "Type": "Service",
  "IncomeAccountRef": {
    "value": "1"
  }
}
```

### Sample Request Body (Inventory Item)

```json
{
  "Name": "Widget A",
  "Type": "Inventory",
  "TrackQtyOnHand": true,
  "QtyOnHand": 100,
  "InvStartDate": "2023-01-01",
  "IncomeAccountRef": {
    "value": "79"
  },
  "ExpenseAccountRef": {
    "value": "80"
  },
  "AssetAccountRef": {
    "value": "81"
  }
}
```

### Sample Response

```json
{
  "Item": {
    "FullyQualifiedName": "Garden Design",
    "domain": "QBO",
    "Name": "Garden Design",
    "SyncToken": "0",
    "sparse": false,
    "Active": true,
    "Type": "Service",
    "Id": "10",
    "MetaData": {
      "CreateTime": "2015-07-24T11:10:18-07:00",
      "LastUpdatedTime": "2015-07-24T11:10:18-07:00"
    },
    "IncomeAccountRef": {
      "name": "Sales of Product Income",
      "value": "1"
    }
  },
  "time": "2015-07-24T11:10:18.596-07:00"
}
```

## Create a Category

### Request

```
POST /v3/company/<realmID>/item?minorversion=4
Content-Type: application/json
```

### Sample Request Body

```json
{
  "Name": "Flowers and Trees",
  "Type": "Category"
}
```

### Sample Response

```json
{
  "Item": {
    "FullyQualifiedName": "Flowers and Trees",
    "domain": "QBO",
    "Name": "Flowers and Trees",
    "SyncToken": "0",
    "sparse": false,
    "Active": true,
    "Type": "Category",
    "Id": "28",
    "MetaData": {
      "CreateTime": "2015-10-06T08:50:34-07:00",
      "LastUpdatedTime": "2015-10-06T08:50:34-07:00"
    }
  },
  "time": "2015-10-06T08:50:34.654-07:00"
}
```

## Query an Item

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: application/text
```

### Sample Query

```sql
select * from Item where Name = 'Rock Fountain'
```

## Query a Bundle

### Sample Query

```sql
select * from Item where Type='Bundle'
```

## Query a Category

### Sample Query

```sql
select * from Item where Type='Category'
```

## Read an Item

### Request

```
GET /v3/company/<realmID>/item/<itemId>
```

## Read a Bundle

### Request

```
GET /v3/company/<realmID>/item/<bundleId>
```

## Read a Category

### Request

```
GET /v3/company/<realmID>/item/<categoryId>?minorversion=4
```

## Full Update an Item

Use this operation to update any of the writable fields of an existing item object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL.

### Request

```
POST /v3/company/<realmID>/item
Content-Type: application/json
```

### Required Fields

| Attribute | Type | Description |
|-----------|------|-------------|
| **Id** | String | Unique identifier. *Required for update* |
| **SyncToken** | String | Version number. *Required for update* |
| **Name** | String | Name of the item. *Required* |
| **Type** | String | Item type. *Required* |

### Sample Request Body

```json
{
  "FullyQualifiedName": "Rock Fountain",
  "domain": "QBO",
  "Id": "5",
  "Name": "Rock Fountain",
  "TrackQtyOnHand": true,
  "Type": "Inventory",
  "PurchaseCost": 125,
  "QtyOnHand": 2,
  "IncomeAccountRef": {
    "name": "Sales of Product Income",
    "value": "79"
  },
  "AssetAccountRef": {
    "name": "Inventory Asset",
    "value": "81"
  },
  "Taxable": true,
  "MetaData": {
    "CreateTime": "2014-09-16T10:42:19-07:00",
    "LastUpdatedTime": "2014-09-19T13:16:17-07:00"
  },
  "sparse": false,
  "Active": true,
  "SyncToken": "2",
  "InvStartDate": "2014-09-19",
  "UnitPrice": 275,
  "ExpenseAccountRef": {
    "name": "Cost of Goods Sold",
    "value": "80"
  },
  "PurchaseDesc": "Rock Fountain",
  "Description": "New, updated description for Rock Fountain"
}
```

### Sample Response

```json
{
  "Item": {
    "FullyQualifiedName": "Rock Fountain",
    "domain": "QBO",
    "Id": "5",
    "Name": "Rock Fountain",
    "TrackQtyOnHand": true,
    "Type": "Inventory",
    "PurchaseCost": 125,
    "QtyOnHand": 2,
    "IncomeAccountRef": {
      "name": "Sales of Product Income",
      "value": "79"
    },
    "AssetAccountRef": {
      "name": "Inventory Asset",
      "value": "81"
    },
    "Taxable": true,
    "MetaData": {
      "CreateTime": "2014-09-16T10:42:19-07:00",
      "LastUpdatedTime": "2015-04-22T11:10:18-07:00"
    },
    "sparse": false,
    "Active": true,
    "SyncToken": "3",
    "InvStartDate": "2014-09-19",
    "UnitPrice": 275,
    "ExpenseAccountRef": {
      "name": "Cost of Goods Sold",
      "value": "80"
    },
    "PurchaseDesc": "Rock Fountain",
    "Description": "New, updated description for Rock Fountain"
  },
  "time": "2015-04-22T11:08:31.596-07:00"
}
```

## Update a Category

### Request

```
POST /v3/company/<realmID>/item?minorversion=4
Content-Type: application/json
```

### Sample Request Body

```json
{
  "SyncToken": "1",
  "domain": "QBO",
  "Name": "Organic Trees",
  "sparse": false,
  "Type": "Category",
  "Id": "29"
}
```

### Sample Response

```json
{
  "Item": {
    "FullyQualifiedName": "Organic Trees",
    "domain": "QBO",
    "Name": "Organic Trees",
    "SyncToken": "2",
    "sparse": false,
    "Active": true,
    "Type": "Category",
    "Id": "29",
    "MetaData": {
      "CreateTime": "2015-10-06T08:50:34-07:00",
      "LastUpdatedTime": "2015-10-07T12:38:03-07:00"
    }
  },
  "time": "2015-10-07T12:40:29.199-07:00"
}
```
