# Mercury API Documentation

This directory contains offline documentation for the Mercury Bank API, scraped from [docs.mercury.com](https://docs.mercury.com).

## Directory Structure

```
mercury_dev_docs/
├── README.md                    # This file
├── CHANGELOG.md                 # API changelog and updates
├── guides/                      # Getting started guides
│   ├── 01-welcome.md
│   ├── 02-getting-started.md
│   ├── 03-api-token-security-policies.md
│   └── 04-using-mercury-sandbox.md
├── oauth2/                      # OAuth2 integration guides
│   ├── 01-integrations-with-oauth2.md
│   ├── 02-start-oauth2-flow.md
│   ├── 03-obtain-the-tokens.md
│   └── 04-using-the-access-token.md
├── mcp/                         # Model Context Protocol (Beta)
│   ├── 01-what-is-mercury-mcp.md
│   ├── 02-connecting-mercury-mcp.md
│   ├── 03-supported-tools-on-mercury-mcp.md
│   └── 04-security-best-practices.md
├── api-reference/               # API endpoint reference
│   ├── 00-overview.md           # Complete endpoint listing
│   ├── accounts/README.md       # Accounts API details
│   ├── transactions/README.md   # Transactions API details
│   ├── recipients/README.md     # Recipients API details
│   ├── webhooks/README.md       # Webhooks API details
│   ├── events/README.md         # Events API details
│   ├── accounts-receivable/README.md  # Invoicing API
│   ├── treasury/README.md       # Treasury API details
│   ├── users/README.md          # Users API details
│   ├── oauth2/README.md         # OAuth2 API details
│   └── misc/README.md           # Categories, Credit, Org, etc.
└── recipes/                     # Code examples and use cases
    └── README.md
```

## Quick Links

### Getting Started
- [Welcome](./guides/01-welcome.md) - Overview of Mercury API capabilities
- [Getting Started](./guides/02-getting-started.md) - Authentication and first API call
- [API Token Security](./guides/03-api-token-security-policies.md) - Token management best practices
- [Sandbox Testing](./guides/04-using-mercury-sandbox.md) - Using the test environment

### OAuth2 Integration
- [OAuth2 Overview](./oauth2/01-integrations-with-oauth2.md) - For building integrations
- [Start OAuth2 Flow](./oauth2/02-start-oauth2-flow.md) - Initiate authorization
- [Obtain Tokens](./oauth2/03-obtain-the-tokens.md) - Exchange code for tokens
- [Using Access Token](./oauth2/04-using-the-access-token.md) - Make authenticated requests

### MCP (Model Context Protocol)
- [What is Mercury MCP?](./mcp/01-what-is-mercury-mcp.md) - Connect AI tools to Mercury
- [Connecting MCP](./mcp/02-connecting-mercury-mcp.md) - Setup guide
- [Supported Tools](./mcp/03-supported-tools-on-mercury-mcp.md) - Available MCP tools
- [Security Best Practices](./mcp/04-security-best-practices.md) - Stay secure

### API Reference
- [API Overview](./api-reference/00-overview.md) - Complete endpoint listing
- [Accounts API](./api-reference/accounts/README.md) - Account management, cards, statements
- [Transactions API](./api-reference/transactions/README.md) - Transaction listing, filtering, attachments
- [Recipients API](./api-reference/recipients/README.md) - Payment recipients management
- [Webhooks API](./api-reference/webhooks/README.md) - Real-time notifications
- [Events API](./api-reference/events/README.md) - Event log for reconciliation
- [Accounts Receivable](./api-reference/accounts-receivable/README.md) - Invoicing and customers
- [Treasury API](./api-reference/treasury/README.md) - Treasury accounts
- [Users API](./api-reference/users/README.md) - User management
- [OAuth2 API](./api-reference/oauth2/README.md) - OAuth2 authentication flow
- [Misc APIs](./api-reference/misc/README.md) - Categories, Credit, Organization

### Examples
- [Recipes](./recipes/README.md) - Code examples and common use cases

## Base URLs

| Environment | API URL | OAuth2 URL |
|-------------|---------|------------|
| Production | `https://api.mercury.com/api/v1` | `https://oauth2.mercury.com` |
| Sandbox | `https://api-sandbox.mercury.com/api/v1` | `https://oauth2-sandbox.mercury.com` |

## Authentication Methods

### 1. API Token (Basic Auth)
```bash
curl --user <api_token>: https://api.mercury.com/api/v1/accounts
```

### 2. API Token (Bearer)
```bash
curl -H "Authorization: Bearer <api_token>" https://api.mercury.com/api/v1/accounts
```

### 3. OAuth2 Access Token
```bash
curl -H "Authorization: Bearer <access_token>" https://api.mercury.com/api/v1/accounts
```

## Token Permission Tiers

| Tier | Capabilities | IP Whitelist Required |
|------|--------------|----------------------|
| Read Only | Fetch account data, transactions, statements | No |
| Read and Write | All read + initiate transactions, manage recipients | Yes |
| Custom | Specific scopes only | Depends on scopes |

## Rate Limits

Mercury implements rate limiting to ensure API stability. If you receive a `429 Too Many Requests` response, wait before retrying.

## Support

- Email: api@mercury.com
- Documentation: [docs.mercury.com](https://docs.mercury.com)
- FAQ: [mercury.com/faq](https://mercury.com/faq)

---

*Last updated: January 2025*
*Source: [docs.mercury.com](https://docs.mercury.com)*
