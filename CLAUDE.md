# CLAUDE.md

This file provides Claude with context and development guidelines for the Finance Plugins project.

## Project Overview

Finance Plugins is a collection of Dify plugins for Mercury Bank and QuickBooks integration:

- `mercury_tools_plugin` - Mercury Bank API tools (accounts, transactions, recipients, etc.)
- `mercury_trigger_plugin` - Mercury Webhook trigger (transaction event sync)

## Project Documentation

| Document | Purpose |
|----------|---------|
| `Mercury_API_Documentation.md` | Mercury Bank API documentation |
| `QuickBooks_API_Documentation.md` | QuickBooks API documentation |
| `solution-design.md` | Technical solution design |

## Financial Security Compliance Requirements

This project handles bank accounts and financial data. The following compliance requirements must be followed:

### 1. Data Classification and Protection

**Sensitive Data Types**:
- Bank account numbers, routing numbers
- API credentials (Access Token, Refresh Token, API Key)
- OAuth Client Secret
- Transaction amounts and details
- Personal identifiable information (name, address, tax ID, etc.)

**Protection Measures**:
- Sensitive data must be encrypted in transit (TLS 1.2+)
- Sensitive data must not be stored in plaintext in code, config files, or logs
- Follow the principle of least privilege, only request data necessary for business

### 2. Authentication and Authorization

- All API calls must be authenticated
- OAuth Tokens must have reasonable expiration times
- Refresh Tokens must be stored securely, never exposed to clients
- Implement automatic token refresh to avoid service interruption
- Webhook requests must verify signatures to prevent forgery

### 3. Logging and Audit

**Must Log**:
- Timestamps (UTC) for all financial operations
- Operation type and result (success/failure)
- Masked business identifiers
- Error codes and non-sensitive error messages

**Must NOT Log**:
- Full account numbers (only last 4 digits allowed)
- Access Token, Refresh Token, API Key
- Full transaction amount details
- Personal identifiable information

### 4. Data Masking Rules

- Bank account numbers: show only last 4 digits, e.g., `****1234`
- Routing numbers: show only last 4 digits
- API Tokens: only log existence (true/false)
- Amounts: allowed in audit logs, forbidden in debug logs

### 5. Error Handling

- Error messages must not contain internal system paths
- Error messages must not contain database queries or raw API responses
- Error messages must not contain credential information
- Distinguish between user-visible errors and internal log errors

### 6. Transport Security

- All external API calls must use HTTPS
- Never disable SSL/TLS certificate verification
- Set reasonable request timeouts (recommended 15-30 seconds)
- Use exponential backoff for request retries

### 7. Input Validation

- Validate format and range of all external inputs
- Account IDs and Transaction IDs must be format-validated
- Amounts must be validated as positive and within reasonable range
- Dates must be validated for format and validity
- Prevent injection attacks (SQL, command, SSRF)

### 8. Idempotency and Consistency

- Financial operations must be idempotent
- Use unique business identifiers for deduplication
- Avoid duplicate processing of the same transaction
- Ensure state consistency when operations fail

### 9. Rate Limiting

- Comply with third-party API rate limits
- Implement client-side throttling to avoid exceeding limits
- Monitor API quota usage

### 10. Code Review Checklist

- [ ] No hardcoded credentials or secrets
- [ ] No sensitive data in logs
- [ ] All external inputs validated
- [ ] Error messages don't expose internal details
- [ ] API calls use HTTPS
- [ ] Request timeouts are set
- [ ] Webhook signatures are verified
- [ ] Financial operations are idempotent

### 11. Prohibited Actions

- Writing real credentials in code, comments, or config
- Committing any credentials to version control
- Disabling SSL/TLS certificate verification
- Logging full credentials or account information
- Implementing backdoors that bypass authentication/authorization
- Passing sensitive information in URL parameters
- Storing personal data beyond business requirements

## Git Workflow

- **Never commit directly to main branch**: Always create a feature branch for the current task
- **Branch naming convention**: `feature/<feature-name>`, `fix/<issue-description>`, `chore/<maintenance-task>`
- **Before creating PR**: Ensure all unit tests and integration tests pass
- **PR merge strategy**: Always use **Rebase and merge** to keep commit history clean and linear. Never create merge commits.
- **Never auto-merge PRs**: Claude must never execute `gh pr merge` or any PR merge operations. User must manually merge PRs on GitHub.
- **Delete feature branch after PR is merged**

## Best Practices

- **Reference official plugins first**: Don't implement from scratch, find similar examples first
- **Keep code simple**: Follow the KISS principle, avoid over-engineering
- **Strict security compliance**: The above security requirements are mandatory and non-negotiable
