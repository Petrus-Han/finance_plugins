# TaxClassification

Tax classification segregates different items into different classifications and the tax classification is one of the key parameters to determine appropriate tax on transactions involving items. Tax classifications are sourced by either tax governing authorities as in India/Malaysia or externally like Exactor. 'Fuel', 'Garments' and 'Soft drinks' are a few examples of tax classification in layman terms. User can choose a specific tax classification for an item while creating it.

## The TaxClassification Object

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| **ParentRef** | ReferenceType | Required | Reference Type for parent. |
| **ApplicableTo** | ItemTypeEnum | Optional | List of item types the tax classification is applicable to. Includes Inventory, NonInventory, Bundle and Service. |
| **Code** | String | Optional | Code. |
| **Name** | String | Optional | Name of the tax classification. |
| **Description** | String | Optional | Description of the tax classification. |
| **Level** | String | read only, system defined | Tax classification level (Numeric value 1, or 2. 1 specifies parent tax classification). |

### Sample Object

```json
{
  "TaxClassification": {
    "applicableTo": [
      "Inventory",
      "Noninventory"
    ],
    "code": "EUC-01010101",
    "description": "Custom software (developed especially for purchaser) - Licensed (not sold), and delivered on a tangible format, such as on a CD or DVD.",
    "level": "2",
    "ParentRef": {
      "name": "Professional Services",
      "value": "V1-00100000"
    },
    "id": "EUC-01010101-V1-00100000",
    "name": "Tangible, custom software"
  }
}
```

## Read a TaxClassification by ID

Retrieves the details of a TaxClassification object that has been previously created.

### Returns

Returns the TaxClassification object.

### Request URL

```
GET /v3/company/<realmID>/taxclassification/<taxClassificationId>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "TaxClassification": {
    "applicableTo": [
      "Inventory",
      "Noninventory"
    ],
    "code": "EUC-01010101",
    "description": "Custom software (developed especially for purchaser) - Licensed (not sold), and delivered on a tangible format, such as on a CD or DVD.",
    "level": "2",
    "ParentRef": {
      "name": "Professional Services",
      "value": "V1-00100000"
    },
    "id": "EUC-01010101-V1-00100000",
    "name": "Tangible, custom software"
  }
}
```

## Read a TaxClassification by Parent ID

Retrieves the details of a TaxClassification object by parent ID.

### Returns

Returns the TaxClassification object by parent ID.

### Request URL

```
GET /v3/company/<realmID>/taxclassification/<parentid>/children
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "QueryResponse": {
    "TaxClassification": [
      {
        "applicableTo": [
          "Inventory",
          "Noninventory"
        ],
        "code": "EUC-01010101",
        "description": "Custom software (developed especially for purchaser) - Licensed (not sold), and delivered on a tangible format, such as on a CD or DVD.",
        "level": "2",
        "ParentRef": {
          "name": "Professional Services",
          "value": "V1-00100000"
        },
        "id": "EUC-01010101-V1-00100000",
        "name": "Tangible, custom software"
      },
      {
        "applicableTo": [
          "Inventory",
          "Noninventory"
        ],
        "code": "EUC-01010201",
        "description": "Canned software (off-the-shelf) - Licensed (not sold) which is delivered in a tangible format, such as on a CD or DVD.",
        "level": "2",
        "ParentRef": {
          "name": "Professional Services",
          "value": "V1-00100000"
        },
        "id": "EUC-01010201-V1-00100000",
        "name": "Tangible, canned software"
      }
    ]
  }
}
```

## Read All TaxClassifications

Retrieves the details of all TaxClassification objects that have been previously created.

### Returns

Returns all TaxClassification records.

### Request URL

```
GET /v3/company/<realmID>/taxclassification
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "QueryResponse": {
    "TaxClassification": [
      {
        "applicableTo": [
          "Inventory",
          "Noninventory"
        ],
        "code": "EUC-01010101",
        "description": "Custom software (developed especially for purchaser) - Licensed (not sold), and delivered on a tangible format, such as on a CD or DVD.",
        "level": "2",
        "ParentRef": {
          "name": "Professional Services",
          "value": "V1-00100000"
        },
        "id": "EUC-01010101-V1-00100000",
        "name": "Tangible, custom software"
      },
      {
        "applicableTo": [
          "Inventory",
          "Noninventory"
        ],
        "code": "EUC-01010201",
        "description": "Canned software (off-the-shelf) - Licensed (not sold) which is delivered in a tangible format, such as on a CD or DVD.",
        "level": "2",
        "ParentRef": {
          "name": "Professional Services",
          "value": "V1-00100000"
        },
        "id": "EUC-01010201-V1-00100000",
        "name": "Tangible, canned software"
      }
    ]
  }
}
```

## Read TaxClassifications by Level

Retrieves the details of a TaxClassification object that has been previously created by level.

### Returns

Returns the TaxClassification object based on level.

### Request URL

```
GET /v3/company/<realmID>/taxclassification?level=<level>
Production Base URL: https://quickbooks.api.intuit.com
Sandbox Base URL: https://sandbox-quickbooks.api.intuit.com
```

### Response

```json
{
  "QueryResponse": {
    "TaxClassification": [
      {
        "applicableTo": [
          "Inventory",
          "Noninventory"
        ],
        "code": "EUC-01010101",
        "description": "Custom software (developed especially for purchaser) - Licensed (not sold), and delivered on a tangible format, such as on a CD or DVD.",
        "level": "2",
        "ParentRef": {
          "name": "Professional Services",
          "value": "V1-00100000"
        },
        "id": "EUC-01010101-V1-00100000",
        "name": "Tangible, custom software"
      },
      {
        "applicableTo": [
          "Inventory",
          "Noninventory"
        ],
        "code": "EUC-01010201",
        "description": "Canned software (off-the-shelf) - Licensed (not sold) which is delivered in a tangible format, such as on a CD or DVD.",
        "level": "2",
        "ParentRef": {
          "name": "Professional Services",
          "value": "V1-00100000"
        },
        "id": "EUC-01010201-V1-00100000",
        "name": "Tangible, canned software"
      }
    ]
  }
}
```
