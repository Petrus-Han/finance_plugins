# Learn About GraphQL

> **Source**: https://developer.intuit.com/app/developer/qbo/docs/learn/learn-about-graphql

## Overview

GraphQL is an API query language that simplifies client-side requests. Apps can do a lot of work with just a single query, such as:

- Query multiple resources and entities
- Request data in a specific format
- Get the server to perform several operations

With GraphQL, all queries go to a **single endpoint** on the server. The server parses queries and returns only the requested data in the requested format.

---

## Related Topics

- [Learn about the advantages of using GraphQL query language](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-about-graphql/graphql-advantages)
- [Learn about the differences between REST and GraphQL](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-about-graphql/graphql-rest-vs-gql)
- [Learn the basics of how to program using GraphQL](https://developer.intuit.com/app/developer/qbo/docs/learn/learn-about-graphql/graphql-basics)

---

## Mercury Integration Notes

For the Mercury-QuickBooks sync plugin:

The Mercury sync plugin uses the **REST API** for QuickBooks Online, not GraphQL. The REST API is well-suited for:
- Creating transactions (Purchases, Deposits)
- Managing vendors
- Querying accounts

GraphQL may be useful if you need to:
- Fetch multiple related entities in a single request
- Reduce over-fetching of data
- Build more complex queries with specific field selection
