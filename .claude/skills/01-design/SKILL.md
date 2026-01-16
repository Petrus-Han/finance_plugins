---
name: plugin-design
description: Guide for Dify plugin design phase - requirements analysis, scope definition, and planning. Use when starting a new plugin project, defining features, or planning implementation.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Plugin Design Phase

Design phase for plugin development, including requirements analysis, scope definition, and planning.

## When to Use This Skill

- Starting a new plugin project
- Analyzing user requirements and feature scope
- Creating development plans and task breakdowns
- Evaluating technical feasibility

## Phase 0: Pre-Planning 🔍

### 0.1 Determine Plugin Type

| Type               | Purpose                        | Use Cases                                          |
| ------------------ | ------------------------------ | -------------------------------------------------- |
| **Tool**           | Add capabilities to workflows  | Integrate external APIs (search, database, SaaS)   |
| **Trigger**        | Start workflows from events    | Receive webhooks (GitHub, Slack, custom)           |
| **Extension**      | Custom HTTP endpoints          | Build APIs, OAuth callbacks                        |
| **Model**          | New AI model providers         | Add LLM/embedding providers                        |
| **Datasource**     | External data connections      | Connect to databases, knowledge bases              |
| **Agent Strategy** | Custom agent logic             | Implement specialized reasoning                    |

### 0.2 Research Target API

- Read official API documentation thoroughly
- Understand authentication methods (API Key / OAuth2)
- Note API rate limits and restrictions
- Check for sandbox/test environments

### 0.3 Review Official Examples (⭐ Critical Step!)

**First, clone/update the official plugins repository:**

```bash
# Initial clone
git clone https://github.com/langgenius/dify-official-plugins.git

# Update before each development (always do this!)
cd dify-official-plugins && git pull
```

**Then find similar plugins:**

```bash
# List all available tool plugins
ls dify-official-plugins/tools/

# Find similar functionality:
# Finance: stripe, plaid
# Search: google, arxiv, wikipedia
# Social: slack, github
# OAuth: github, google, slack
```

**Key points to review:**
- Search for similar integrations in the repository
- Study implementation patterns and code structure
- Identify reusable authentication and error handling patterns
- Note manifest.yaml and provider configuration patterns

## Phase 1: Requirements Analysis ✅

### 1.1 Define User Needs

Answer these questions:
- What problem does this plugin solve?
- What workflows will it enable?
- Who is the target user?

### 1.2 Clarify Integration Goals

- Which service are you integrating?
- What specific features are needed?
- Is it one-way or two-way integration?

### 1.3 Confirm Authentication Method

| Auth Type | Use Case | Complexity |
|-----------|----------|------------|
| API Key | Simple services | Low |
| API Token | Enterprise services | Medium |
| OAuth 2.0 | User authorization | High |

### 1.4 Confirm Data Flow

- [ ] Read-only queries?
- [ ] Write operations?
- [ ] Event-driven triggers?
- [ ] Bidirectional sync?

## Phase 2: Scope Definition 📋

### 2.1 List All Tools

Define 3-7 tools for MVP with clear naming:

```yaml
# Example: Mercury bank integration
tools:
  - get_accounts      # Get account list
  - get_account       # Get account details
  - get_transactions  # Get transaction records
  - create_payment    # Create payment (optional)
```

### 2.2 Set Priorities

| Priority | Label | Description |
|----------|-------|-------------|
| P0 | Must Have | Required for MVP |
| P1 | Should Have | Important but can defer |
| P2 | Nice to Have | Enhancement |

### 2.3 Map Dependencies

```
get_accounts ─────┐
                  ├──> get_transactions (needs account_id)
get_account ──────┘
                  
create_token ────> create_charge (needs token)
```

### 2.4 Evaluate Complexity

| Complexity | Characteristics | Estimated Time |
|------------|-----------------|----------------|
| Simple | Single API call, basic parameters | 1-2 hours |
| Medium | Multiple calls, data transformation | 2-4 hours |
| Complex | OAuth flow, webhook verification, state management | 4-8 hours |

### 2.5 Document Limitations

```yaml
limitations:
  rate_limits: "100 requests/minute"
  geographic: "US only"
  environment: "Webhooks not available in sandbox"
  authentication: "OAuth requires HTTPS callback URL"
```

## Phase 3: Planning & Approval 📝

### 3.1 Create Task List

Use `TodoWrite` tool to track progress with concrete tasks:

```
[ ] 1. Create plugin skeleton structure
[ ] 2. Implement Provider (authentication)
[ ] 3. Implement get_accounts tool
[ ] 4. Implement get_transactions tool
[ ] 5. Local testing
[ ] 6. Package and release
```

### 3.2 Document Key Files

```
my_plugin/
├── manifest.yaml       # Plugin metadata
├── main.py             # Entry point
├── requirements.txt    # Dependencies
├── provider/
│   ├── provider.yaml   # Auth configuration
│   └── provider.py     # OAuth/validation logic
└── tools/
    ├── get_accounts.yaml  # Tool definition
    └── get_accounts.py    # Tool implementation
```

### 3.3 Identify Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Complex OAuth flow | High | Reference official examples |
| Undocumented API behavior | Medium | Write diagnostic scripts |
| Missing test environment | Medium | Carefully test with production |

### 3.4 Get User Confirmation

Before starting development, present to user:
- Feature scope
- Task list
- Time estimate
- Potential risks

Use `AskUserQuestion` to confirm before proceeding.

## Design Document Template

```markdown
# [Plugin Name] Design Document

## Overview
Brief description of plugin purpose and goals.

## Functional Requirements
1. Feature A - Description
2. Feature B - Description

## Technical Approach
- Plugin Type: Tool / Trigger / Extension
- Authentication: API Key / OAuth 2.0
- Target API: [API documentation link]

## Tool List
| Tool Name | Function | Priority |
|-----------|----------|----------|
| get_xxx | Get xxx | P0 |
| create_xxx | Create xxx | P1 |

## Dependencies
[Dependency diagram]

## Risk Assessment
| Risk | Impact | Mitigation |
|------|--------|------------|

## Time Estimate
- Phase 1: X hours
- Phase 2: X hours
- Total: X hours
```

## Related Skills

- **02-api-reference**: API documentation collection
- **03-development**: Development implementation
- **04-testing**: Testing and validation
- **05-packaging**: Packaging and release

## Reference

- `dify-plugin` skill: Complete Dify plugin development guide
- `archive/solution-design.md`: Existing solution design documents
