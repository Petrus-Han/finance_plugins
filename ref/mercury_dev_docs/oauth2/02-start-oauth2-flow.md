# Start OAuth2 web flow

The web flow starts when your client redirects a user to the Mercury OAuth2 server that will verify client identity and let them confirm the authorization request.

The query parameters of the authorization URL are:

- `client_id` - uniquely identifies your client.
- `redirect_url` - should match the registered client URL. It is also known as the Authorization callback URL.
- `scope` - specifies what type of access you need.
- `state` - random value that should be at least eight characters long.

## Scopes

The `scope` parameter contains a space-separated list of scopes that your client requests. Mercury supports two scopes:

- **"read"** — access the accounts and transactions.
- **"offline_access"** — required for refresh tokens.

> **Note:** An access token has a short lifespan. A refresh token lets a client request a new access token without any user interaction. Add this scope if a client needs to maintain continuous access to the Mercury account.

## State Parameter

Generate a random string for the query parameter `state` and store it. It's used to protect against cross-site request forgery. The client should verify its value when Mercury sends a user back.

## PKCE (Proof Key for Code Exchange)

If your client has PKCE, do the following as well:

1. Generate a cryptographic random string that satisfies [these requirements](https://tools.ietf.org/html/rfc7636#section-4.1) and store it. It's going to be used as `code_verifier` when obtaining a token.
2. Calculate its SHA256 hash and convert it to base64. This is the value of the `code_challenge` query parameter.

---

## Navigation

- Previous: [Integrations with OAuth2](./01-integrations-with-oauth2.md)
- Next: [Obtain the tokens](./03-obtain-the-tokens.md)
