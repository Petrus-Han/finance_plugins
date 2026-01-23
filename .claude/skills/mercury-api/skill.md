---
name: mercury-api
description: Mercury Bank API reference. Use when working with Mercury API integration.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Mercury API Reference

## API Documentation

- Official Docs: https://docs.mercury.com/reference
- Sandbox Guide: https://docs.mercury.com/docs/using-mercury-sandbox

## Environments

| Environment | Base URL |
|-------------|----------|
| Production | `https://api.mercury.com` |
| Sandbox | `https://api-sandbox.mercury.com` |

## Authentication

```python
headers = {
    "Authorization": f"Bearer {api_token}",
    "Accept": "application/json;charset=utf-8"
}
```

## Local Reference

- Full docs: `mercury_tools_plugin/docs/Mercury_MCP_API_Reference.md`
