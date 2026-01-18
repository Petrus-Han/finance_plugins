# Obtain the tokens

The access code can be used to call Mercury API. For security reasons, the access token expires in one hour. If you want to maintain access to the Mercury API without user interaction, your client should include the `offline_access` scope in its configuration. This scope also should be included when starting the flow.

## Exchange authorization code

After receiving the authorization code with redirect, your client should exchange it for the access code. This step is slightly different for the clients that use the flow with PKCE. See the POST example that corresponds to your client type.

## Refreshing tokens

To refresh a token, use the same endpoint that you used for exchanging the authorization code. A refresh token can only be used once. On successful grant, the server returns a new access token and a new refresh token.

A refresh token expires in 720 hours. You can preemptively refresh your access tokens or wait for a request with an expired token to fail. Once a refresh token has expired, your client would need user interaction to grant the access again.

## Key Points

| Token Type | Expiration | Notes |
|------------|------------|-------|
| Access Token | 1 hour | Used for API calls |
| Refresh Token | 720 hours (30 days) | Can only be used once |

---

## Navigation

- Previous: [Start OAuth2 web flow](./02-start-oauth2-flow.md)
- Next: [Using the access token](./04-using-the-access-token.md)
