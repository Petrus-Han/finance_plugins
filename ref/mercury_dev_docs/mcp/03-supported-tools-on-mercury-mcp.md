# Supported tools on Mercury MCP

Learn what you can do with Mercury MCP tools.

Now that you've logged into your Mercury MCP, let's explore how AI assistants can use Mercury MCP tools to understand your balance, track your spend patterns, and let you dig into your cards and recipient data.

These tools work seamlessly together through prompts, where you can ask natural language questions like `What's my balance today?` and `Graph my last 6 months of transactions`, then the Mercury MCP will accurately and quickly return your Mercury data.

## Available Tools

| Name | Description | Sample Prompt |
|------|-------------|---------------|
| `getAccount` | Get account by id - Retrieve details of a specific Mercury account using its account ID | "What's the balance in my checking account?" or "Show me details for account abc123-xyz" |
| `getAccountCards` | Get cards for account - Retrieve all debit and credit cards associated with a specific account | "What cards are linked to my main account?" or "Show me all debit cards for account abc123" |
| `getAccountStatements` | Get account statements - Retrieve monthly statements for a specific account. Supports date range filtering | "Get my account statements from January through March" or "Show me last quarter's statements" |
| `getTransaction` | Get transaction by id - Retrieve details of a specific transaction using account ID and transaction ID | "Get more details about transaction txn789" or "Why was I charged $150 on transaction xyz?" |
| `getAccounts` | Get all accounts - Retrieve a list of all Mercury accounts for the organization | "What cards are linked to my checking account?" or "Show all my active cards" |
| `listCategories` | List all categories - Retrieve a list of all available custom expense categories for the organization. These are custom categories different from Mercury's built-in categories | "What expense categories do I have set up?" or "Show me my custom spending categories" |
| `listCredit` | List all credit accounts - Retrieve a list of all credit accounts for the organization | "How much credit do I have available?" or "Show me my credit card accounts" |
| `getOrganization` | Get organization info - Retrieve organization information | "What's my company's EIN?" or "Show me my business information" |
| `getRecipient` | Get recipient by id - Retrieve details of a specific recipient by ID | "What are the payment details for Acme Corp?" or "Show me recipient rec456" |
| `getRecipients` | Get all recipients - Retrieve a list of all recipients | "List all my payment recipients" or "Find recipient named Acme Corp" |
| `listTransactions` | List all transactions - Retrieve transactions with advanced filtering by date ranges, status, categories, and cursor-based pagination. Automatically handles pagination for complete results | "Graph my last 6 months of transactions" or "Show pending transactions from last week" |
| `getTreasury` | Get all treasury accounts - Retrieve all treasury accounts associated with the authenticated organization | "How much do I have in treasury?" or "Show me my treasury accounts and balances" |
| `getTreasuryTransactions` | Get treasury transactions - Retrieve paginated treasury transactions for a specific treasury account | "Show me recent treasury account activity" or "What are my treasury transactions this month?" |

---

We'd love your feedback. If there are more tools or data you'd love to see in Mercury's MCP, email us at api@mercury.com

---

## Navigation

- Previous: [Connecting Mercury MCP](./02-connecting-mercury-mcp.md)
- Next: [Security best practices](./04-security-best-practices.md)
