# Connecting Mercury MCP

Learn how to get started and plug Mercury into your AI tool.

This guide walks you through connecting your AI tool to Mercury using the Model Context Protocol (MCP).

## Log in to your AI tool

Mercury MCP is available anywhere you can use MCPs, but the easiest way to set this up:

### Step 1: Open Connectors Settings

- Open **[Add Connectors](https://claude.ai/settings/connectors?modal=add-custom-connector)** in Claude
- Or **[Apps & Connectors](https://chatgpt.com/#settings/Connectors)** in ChatGPT

### Step 2: Create a new custom connection

1. Add Mercury as a new MCP and use the URL `https://mcp.mercury.com/mcp` in the MCP server URL field
2. Adding this MCP does not give the LLM access to your Mercury data until you login (next step)

### Step 3: Login to Mercury MCP

1. After you start a chat asking about Mercury data, it should prompt login via OAuth
2. Sessions will remain active for 3 days on the same chat thread, so you may need to authenticate after that.

## Notes

- Mercury's hosted MCP has been scoped to read-only access to certain types of information to prevent unintended actions on your behalf, however you are responsible for deciding if you should connect Mercury's data with a third party.
- Mercury does **not** offer a non-hosted MCP at this time.

---

## Navigation

- Previous: [What is Mercury MCP?](./01-what-is-mercury-mcp.md)
- Next: [Supported tools on Mercury MCP](./03-supported-tools-on-mercury-mcp.md)
