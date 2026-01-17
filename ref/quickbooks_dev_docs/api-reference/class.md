# Class

Class objects provide a way to track different segments of the business so they're not tied to a particular client or project. For example, you can define classes to break down the income and expenses for each business segment. Classes are available to the entire transaction or to individual detail lines of a transaction.

## The Class Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **Id** | String, filterable, sortable | Required for update | Unique identifier for this object. Sort order is ASC by default. Read only, system defined. |
| **Name** | String (max 100 chars) | Required | User recognizable name for the Class. |
| **SyncToken** | String | Required for update | Version number of the object. It is used to lock an object for use by one app at a time. As soon as an application modifies an object, its SyncToken is incremented. Attempts to modify an object specifying an older SyncToken fails. Only the latest version of the object is maintained by QuickBooks Online. Read only, system defined. |
| **ParentRef** | ReferenceType | Conditionally required | The immediate parent of the SubClass. Required if this object is a subclass. |
| **SubClass** | Boolean | Optional | Specifies whether this object is a subclass. true--this object represents a subclass. false or null--this object represents a top-level class. System defined. |
| **Active** | Boolean, filterable, sortable | Optional | If true, this entity is currently enabled for use by QuickBooks. |
| **MetaData** | ModificationMetaData, filterable, sortable | Optional | Descriptive information about the object. The MetaData values are set by Data Services and are read only for all applications. |
| **FullyQualifiedName** | String, filterable, sortable | Read only | Fully qualified name of the entity. The fully qualified name prepends the topmost parent, followed by each sub class separated by colons. Takes the form of Parent:Class1:SubClass1:SubClass2. Limited to 5 levels. System defined. |

### Sample Object

```json
{
  "Class": {
    "FullyQualifiedName": "France",
    "domain": "QBO",
    "Name": "France",
    "SyncToken": "0",
    "SubClass": false,
    "sparse": false,
    "Active": true,
    "Id": "5000000000000007280",
    "MetaData": {
      "CreateTime": "2015-07-22T13:57:27-07:00",
      "LastUpdatedTime": "2015-07-22T13:57:27-07:00"
    }
  },
  "time": "2015-07-22T13:57:27.84-07:00"
}
```

## Create a Class

### Request

```
POST /v3/company/<realmID>/class
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Minimum Required Elements

- **Name**: User recognizable name for the Class

### Request Body

```json
{
  "Name": "France"
}
```

### Creating a SubClass

To create a subclass, include the ParentRef:

```json
{
  "Name": "InternalParts",
  "ParentRef": {
    "value": "5000000000000005251"
  }
}
```

### Response

```json
{
  "Class": {
    "FullyQualifiedName": "France",
    "domain": "QBO",
    "Name": "France",
    "SyncToken": "0",
    "SubClass": false,
    "sparse": false,
    "Active": true,
    "Id": "5000000000000007280",
    "MetaData": {
      "CreateTime": "2015-07-22T13:57:27-07:00",
      "LastUpdatedTime": "2015-07-22T13:57:27-07:00"
    }
  },
  "time": "2015-07-22T13:57:27.84-07:00"
}
```

## Read a Class

Retrieves the details of a class object that has been previously created.

### Request

```
GET /v3/company/<realmID>/class/<classId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "FullyQualifiedName": "France",
  "domain": "QBO",
  "Name": "France",
  "SyncToken": "0",
  "SubClass": false,
  "sparse": false,
  "Active": true,
  "Id": "5000000000000007280",
  "MetaData": {
    "CreateTime": "2015-07-22T13:57:27-07:00",
    "LastUpdatedTime": "2015-07-22T13:57:27-07:00"
  }
}
```

## Query a Class

### Request

```
GET /v3/company/<realmID>/query?query=<selectStatement>
Content-Type: text/plain
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Sample Query

```sql
select * from Class
```

### Response

```json
{
  "QueryResponse": {
    "startPosition": 1,
    "totalCount": 5,
    "Class": [
      {
        "FullyQualifiedName": "Europe",
        "domain": "QBO",
        "Name": "Europe",
        "SyncToken": "0",
        "SubClass": false,
        "sparse": false,
        "Active": true,
        "Id": "5000000000000007195",
        "MetaData": {
          "CreateTime": "2015-07-14T14:25:49-07:00",
          "LastUpdatedTime": "2015-07-14T14:25:49-07:00"
        }
      },
      {
        "FullyQualifiedName": "InternalCafe",
        "domain": "QBO",
        "Name": "InternalCafe",
        "SyncToken": "2",
        "SubClass": false,
        "sparse": false,
        "Active": true,
        "Id": "5000000000000005251",
        "MetaData": {
          "CreateTime": "2015-06-30T15:38:56-07:00",
          "LastUpdatedTime": "2015-06-30T15:51:07-07:00"
        }
      },
      {
        "FullyQualifiedName": "InternalCafe:InternalParts",
        "domain": "QBO",
        "Name": "InternalParts",
        "SyncToken": "0",
        "sparse": false,
        "SubClass": true,
        "ParentRef": {
          "value": "5000000000000005251"
        },
        "Active": true,
        "Id": "5000000000000005252",
        "MetaData": {
          "CreateTime": "2015-06-30T15:41:51-07:00",
          "LastUpdatedTime": "2015-06-30T15:51:07-07:00"
        }
      },
      {
        "FullyQualifiedName": "North America",
        "domain": "QBO",
        "Name": "North America",
        "SyncToken": "0",
        "SubClass": false,
        "sparse": false,
        "Active": true,
        "Id": "5000000000000007194",
        "MetaData": {
          "CreateTime": "2015-07-14T14:24:49-07:00",
          "LastUpdatedTime": "2015-07-14T14:24:49-07:00"
        }
      },
      {
        "FullyQualifiedName": "Sales Dept",
        "domain": "QBO",
        "Name": "Sales Dept",
        "SyncToken": "0",
        "SubClass": false,
        "sparse": false,
        "Active": true,
        "Id": "5000000000000005250",
        "MetaData": {
          "CreateTime": "2015-06-30T15:37:54-07:00",
          "LastUpdatedTime": "2015-06-30T15:37:54-07:00"
        }
      }
    ],
    "maxResults": 5
  },
  "time": "2015-07-22T13:55:26.286-07:00"
}
```

## Full Update a Class

Use this operation to update any of the writable fields of an existing class object. The request body must include all writable fields of the existing object as returned in a read response. Writable fields omitted from the request body are set to NULL. The ID of the object to update is specified in the request body.

### Request

```
POST /v3/company/<realmID>/class
Content-Type: application/json
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Request Body

```json
{
  "FullyQualifiedName": "France",
  "domain": "QBO",
  "Name": "France",
  "SyncToken": "1",
  "SubClass": false,
  "sparse": false,
  "Active": true,
  "Id": "5000000000000007280",
  "MetaData": {
    "CreateTime": "2015-07-22T13:57:27-07:00",
    "LastUpdatedTime": "2015-07-22T13:57:27-07:00"
  }
}
```

### Response

```json
{
  "Class": {
    "FullyQualifiedName": "France",
    "domain": "QBO",
    "Name": "France",
    "SyncToken": "2",
    "SubClass": false,
    "sparse": false,
    "Active": true,
    "Id": "5000000000000007280",
    "MetaData": {
      "CreateTime": "2015-07-22T13:57:27-07:00",
      "LastUpdatedTime": "2015-07-22T15:13:03-07:00"
    }
  },
  "time": "2015-07-22T15:13:03.963-07:00"
}
```

## Class Hierarchy

Classes support up to 5 levels of hierarchy:
- Parent
- Class1
- SubClass1
- SubClass2
- SubClass3

The FullyQualifiedName shows the complete hierarchy path, e.g., `Parent:Class1:SubClass1:SubClass2`.
