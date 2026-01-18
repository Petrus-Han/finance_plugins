# Learn QuickBooks Online API

> Concepts, basics, and API features for building integrations

## Overview

This section covers the foundational concepts needed to understand QuickBooks Online and its API. Start here to learn about bookkeeping basics, API features, and how different components work together.

---

## Pages in This Section

### API Fundamentals

| Page | Description | Mercury Relevance |
|------|-------------|-------------------|
| [Explore the QuickBooks Online API](explore-the-quickbooks-online-api.md) | Overview of what the API can do | Understanding API capabilities |
| [REST API Features](rest-api-features.md) | Schema, data formats, rate limits, error handling | **★ Essential** - Core API patterns for all calls |
| [Basic Field Definitions](learn-basic-field-definitions.md) | Common IDs: realmID, entityID, requestID | **★ Essential** - Understanding ID relationships |
| [Scopes](scopes.md) | OAuth scopes for API access permissions | **★ Essential** - Required scope configuration |

### QuickBooks Concepts

| Page | Description | Mercury Relevance |
|------|-------------|-------------------|
| [QuickBooks Online Basics](learn-quickbooks-online-basics.md) | Company files, settings, chart of accounts, lists | Understanding QBO structure for mapping |
| [Basic Bookkeeping](learn-basic-bookkeeping.md) | Double-entry accounting, debits/credits, workflows | **★ Essential** - Correct transaction recording |
| [GraphQL](learn-about-graphql.md) | GraphQL API overview (alternative to REST) | Optional - REST preferred for this project |

### Advanced API Features

Located in `explore-the-quickbooks-online-api/` subdirectory:

| Page | Description | Mercury Relevance |
|------|-------------|-------------------|
| [Minor Versions](explore-the-quickbooks-online-api/minor-versions.md) | API versioning and feature flags | Ensuring compatibility |
| [Data Queries](explore-the-quickbooks-online-api/data-queries.md) | SQL-like query language for filtering entities | **★ Essential** - Efficient data retrieval |
| [Batch Operations](explore-the-quickbooks-online-api/batch.md) | Multiple operations in a single request | Performance optimization |
| [Change Data Capture](explore-the-quickbooks-online-api/change-data-capture.md) | Detecting changes since last sync | **★ Essential** - Sync optimization |

---

## Recommended Reading Order

For the Mercury-QuickBooks sync plugin, read in this order:

1. **[REST API Features](rest-api-features.md)** - Understand request/response formats
2. **[Basic Field Definitions](learn-basic-field-definitions.md)** - Learn ID concepts
3. **[Basic Bookkeeping](learn-basic-bookkeeping.md)** - Understand accounting fundamentals
4. **[Data Queries](explore-the-quickbooks-online-api/data-queries.md)** - Learn to query entities
5. **[Change Data Capture](explore-the-quickbooks-online-api/change-data-capture.md)** - Optimize sync operations
6. **[Scopes](scopes.md)** - Configure OAuth permissions

---

## Key Concepts for Mercury Integration

### IDs You'll Work With

| ID | Description | Usage |
|----|-------------|-------|
| **realmId** | Company identifier (unique per QBO company) | Every API call |
| **entityId** | Entity record ID (Vendor, Customer, Account, etc.) | References in transactions |
| **requestId** | Unique request identifier for idempotency | Preventing duplicates |

### Accounting Fundamentals

Understanding these is critical for correct transaction mapping:

- **Double-entry**: Every transaction affects at least 2 accounts
- **Debits/Credits**: Bank account debits = money out, credits = money in
- **Account Types**: Asset, Liability, Equity, Income, Expense

### Mercury Transaction Mapping

| Mercury Transaction | QBO Accounting Entry |
|---------------------|---------------------|
| Outgoing payment | Debit: Expense account, Credit: Bank account |
| Incoming deposit | Debit: Bank account, Credit: Income account |
| Internal transfer | Debit: To-account, Credit: From-account |

---

## Related Sections

- **[Get Started](../get-started/)** - Setting up your developer account
- **[Develop](../develop/)** - OAuth, webhooks, and SDK guides
- **[API Reference](../api-reference/)** - Entity documentation
- **[Use Cases](../use-cases/)** - Workflow examples

---

*Last updated: 2025-01-17*
