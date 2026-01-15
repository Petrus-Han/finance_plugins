# Mercury-QuickBooks Sync Plugin

Dify Trigger plugin for syncing Mercury banking transactions to QuickBooks in real-time.

## Project Structure

```
mercury_plugin/
├── .venv/                          # Python virtual environment (auto-created)
├── mercury-trigger/                # Mercury Trigger plugin (to be created)
├── quickbooks-plugin/              # QuickBooks Tool plugin (to be created)
├── docs/                           # Documentation
│   ├── Mercury_API_Documentation.md
│   ├── QuickBooks_API_Documentation.md
│   ├── Dify_Trigger_Plugin_Guide.md
│   └── ...
└── .claude/                        # Claude Code configuration
    └── skills/                     # Custom skills
```

## Prerequisites

- Python 3.12+
- Dify CLI v0.4.1+
- uv package manager

## Development Setup

### 1. Always Use Virtual Environment

**IMPORTANT**: Always activate the virtual environment before running any Python commands:

```bash
# Activate virtual environment
source .venv/bin/activate

# Verify you're in the venv (should show .venv/bin/python)
which python

# When done, deactivate
deactivate
```

### 2. Install Dependencies (when needed)

```bash
# Activate venv first!
source .venv/bin/activate

# Install Dify plugin SDK
uv pip install "dify-plugin>=0.6.0,<0.7.0"

# Install other dependencies
uv pip install requests python-dotenv
```

### 3. Create Plugin Projects

```bash
# Initialize Mercury Trigger plugin
dify plugin init mercury-trigger --template=tool

# Initialize QuickBooks Tool plugin
dify plugin init quickbooks-plugin --template=tool
```

## Quick Start

1. **Activate virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

2. **Develop plugins** (see development plan in `开发计划.md`)

3. **Debug locally**:
   ```bash
   cd mercury-trigger
   dify plugin debug
   ```

4. **Package for distribution**:
   ```bash
   dify plugin package ./mercury-trigger
   ```

## Documentation

- **Development Plan**: `开发计划.md` (Chinese)
- **Architecture**: `架构方案-优化版.md` (Chinese)
- **API References**:
  - Mercury API: `Mercury_API_Documentation.md`
  - QuickBooks API: `QuickBooks_API_Documentation.md`
  - Dify Trigger Plugin: `Dify_Trigger_Plugin_Guide.md`
- **Project Context**: `CLAUDE.md` (for AI assistants)

## Reference Repositories

See `CLAUDE.md` for local workspace references:
- `dify-official-plugins/` - Official plugin examples
- `dify-plugin-daemon/` - Plugin runtime
- `dify/` - Platform code

## Environment Variables

Create `.env` file for local development (not committed to git):

```bash
# Mercury API
MERCURY_CLIENT_ID=your_client_id
MERCURY_CLIENT_SECRET=your_client_secret

# QuickBooks API
QUICKBOOKS_CLIENT_ID=your_client_id
QUICKBOOKS_CLIENT_SECRET=your_client_secret

# Dify Debug
DIFY_DEBUG_KEY=your_debug_key
```

## Development Workflow

1. **Plan** → See `开发计划.md` for phases
2. **Reference** → Check official plugins first
3. **Implement** → Follow Dify plugin patterns
4. **Test** → Use remote debugging
5. **Package** → Create .difypkg files
6. **Deploy** → Upload to Dify marketplace

## Support

- Dify Plugin Docs: https://docs.dify.ai/en/develop-plugin
- Mercury API: https://docs.mercury.com
- QuickBooks API: https://developer.intuit.com

---

**Remember**: Always use virtual environment! `source .venv/bin/activate`
