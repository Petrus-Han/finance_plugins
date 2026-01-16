---
name: plugin-development
description: Guide for Dify plugin development phase - coding, implementation patterns, and best practices. Use when writing plugin code, implementing tools, or following coding standards.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Plugin Development Phase

Code implementation phase for plugin development, including coding standards, implementation patterns, and best practices.

## When to Use This Skill

- Writing plugin code
- Implementing Provider and Tools
- Following coding standards
- Handling errors and edge cases

## ⭐ Official Plugin Reference (Most Important!)

Before development, you **MUST** get the official plugin repository as reference. This is the most reliable source for implementation patterns.

### Step 0: Get Official Plugin Repository

```bash
# Initial clone
cd /path/to/your/workspace
git clone https://github.com/langgenius/dify-official-plugins.git

# Update before development (always do this!)
cd dify-official-plugins
git pull origin main
```

### Repository Structure

```
dify-official-plugins/
├── tools/                    # Tool plugins
│   ├── google/               # Google Search
│   ├── github/               # GitHub integration
│   ├── slack/                # Slack integration
│   ├── arxiv/                # Academic paper search
│   ├── wikipedia/            # Wikipedia
│   └── ...
├── extensions/               # Extension plugins
│   └── ...
├── models/                   # Model plugins
│   ├── openai/
│   ├── anthropic/
│   ├── azure_openai/
│   └── ...
└── agent-strategies/         # Agent Strategy plugins
    └── ...
```

### How to Find Reference Examples

Find similar official implementations based on your plugin type:

| Requirement | Recommended Reference | Path |
|-------------|----------------------|------|
| Simple API integration | arxiv, wikipedia | `tools/arxiv/`, `tools/wikipedia/` |
| OAuth API integration | github, slack, google | `tools/github/`, `tools/slack/` |
| Finance/Payments | stripe (if available) | `tools/stripe/` |
| Webhook/Trigger | github, slack | Look for `_trigger` suffix |
| Search functionality | google, bing, tavily | `tools/google/`, `tools/tavily/` |

### Reference Development Flow

```bash
# 1. Update official repository
cd /path/to/dify-official-plugins
git pull

# 2. Find similar plugin
ls tools/  # View available tool plugins

# 3. Study its structure
tree tools/github -L 2

# 4. Copy as template
cp -r tools/github /path/to/my_project/my_plugin

# 5. Modify for your implementation
```

### Key Files to Reference

For each reference plugin, focus on:

```bash
# 1. manifest.yaml - Plugin metadata format
cat tools/github/manifest.yaml

# 2. provider/*.yaml - Authentication configuration
cat tools/github/provider/github.yaml

# 3. provider/*.py - Provider implementation (especially OAuth)
cat tools/github/provider/github.py

# 4. tools/*.py - Tool implementation patterns
cat tools/github/tools/github_repositories.py
```

### Common Scenario References

#### OAuth 2.0 Authentication
```bash
# Reference GitHub's OAuth implementation
cat tools/github/provider/github.py
# Focus on: _oauth_get_authorization_url, _oauth_get_credentials
```

#### API Key Authentication
```bash
# Reference arxiv's simple authentication
cat tools/arxiv/provider/arxiv.py
```

#### Webhook/Trigger
```bash
# Find trigger-type plugins
find . -name "*trigger*" -type d
```

### Development Reference Checklist

- [ ] Updated official repository with `git pull`
- [ ] Found similar official plugin
- [ ] Studied its manifest.yaml format
- [ ] Studied its provider authentication implementation
- [ ] Studied its tools implementation patterns
- [ ] Compared error handling approaches

## Plugin Directory Structure

```
my_plugin/
├── _assets/
│   └── icon.svg           # Plugin icon (required)
├── provider/
│   ├── my_provider.yaml   # Provider configuration
│   └── my_provider.py     # Provider implementation
├── tools/                 # Tool plugins
│   ├── get_data.yaml
│   └── get_data.py
├── events/                # Trigger plugins
│   ├── webhook.yaml
│   └── webhook.py
├── manifest.yaml          # Plugin metadata
├── main.py                # Entry point
└── requirements.txt       # Dependencies
```

## Implementation Order

### Step 1: Create Skeleton

```bash
mkdir -p my_plugin/{_assets,provider,tools}
touch my_plugin/{manifest.yaml,main.py,requirements.txt}
touch my_plugin/provider/my_provider.{yaml,py}
```

### Step 2: Implement manifest.yaml

```yaml
version: 0.1.0
type: plugin
author: your-name
name: my-plugin
created_at: "2025-01-16T00:00:00Z"
label:
  en_US: My Plugin
  zh_Hans: My Plugin
icon: icon.svg
description:
  en_US: Plugin description
  zh_Hans: Plugin description

resource:
  memory: 134217728
  permission:
    tool:
      enabled: true

plugins:
  tools:
    - provider/my_provider.yaml

tags:
  - finance    # Use valid tags
  - utilities

meta:
  version: 0.1.0
  arch: [amd64, arm64]
  runner:
    language: python
    version: "3.12"
    entrypoint: main
```

### Step 3: Implement main.py

```python
from dify_plugin import DifyPluginEnv, Plugin

plugin = Plugin(DifyPluginEnv())

if __name__ == "__main__":
    plugin.run()
```

### Step 4: Implement Provider

**provider/my_provider.yaml:**
```yaml
identity:
  name: my_provider
  author: your-name
  label:
    en_US: My Provider

credentials_schema:
  - name: api_key
    type: secret-input
    label:
      en_US: API Key
    required: true
    placeholder:
      en_US: Enter your API key
      
  - name: environment
    type: select
    label:
      en_US: Environment
    required: true
    options:
      - value: sandbox
        label:
          en_US: Sandbox
      - value: production
        label:
          en_US: Production
    default: sandbox

tools:
  - tools/get_data.yaml
```

**provider/my_provider.py:**
```python
import httpx
from dify_plugin import ToolProvider
from dify_plugin.errors import ToolProviderCredentialValidationError

class MyProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict) -> None:
        """Validate API credentials."""
        api_key = credentials.get("api_key")
        environment = credentials.get("environment", "sandbox")
        
        base_url = self._get_base_url(environment)
        
        try:
            response = httpx.get(
                f"{base_url}/ping",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=30
            )
            if response.status_code != 200:
                raise ToolProviderCredentialValidationError(
                    f"Invalid credentials: {response.status_code}"
                )
        except httpx.HTTPError as e:
            raise ToolProviderCredentialValidationError(str(e))
    
    def _get_base_url(self, environment: str) -> str:
        """Get API base URL for environment."""
        urls = {
            "sandbox": "https://api-sandbox.example.com",
            "production": "https://api.example.com"
        }
        return urls.get(environment, urls["sandbox"])
```

### Step 5: Implement Tools

**tools/get_data.yaml:**
```yaml
identity:
  name: get_data
  author: your-name
  label:
    en_US: Get Data

description:
  human:
    en_US: Get data from the API
  llm: Retrieves data from the external service. Use when you need to fetch information.

parameters:
  - name: resource_id
    type: string
    required: true
    label:
      en_US: Resource ID
    human_description:
      en_US: The ID of the resource to fetch
    llm_description: The unique identifier of the resource
    
  - name: include_details
    type: boolean
    required: false
    default: false
    label:
      en_US: Include Details
    human_description:
      en_US: Whether to include detailed information
```

**tools/get_data.py:**
```python
from typing import Any, Generator
import httpx
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage

class GetDataTool(Tool):
    def _invoke(
        self, 
        tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        """Invoke the get_data tool."""
        
        # Get parameters
        resource_id = tool_parameters.get("resource_id")
        include_details = tool_parameters.get("include_details", False)
        
        # Get credentials
        api_key = self.runtime.credentials.get("api_key")
        environment = self.runtime.credentials.get("environment", "sandbox")
        
        # Build URL
        base_url = self._get_base_url(environment)
        url = f"{base_url}/resources/{resource_id}"
        if include_details:
            url += "?include=details"
        
        # Make request
        try:
            response = httpx.get(
                url,
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=30
            )
            
            if response.status_code == 200:
                yield self.create_json_message(response.json())
            elif response.status_code == 404:
                yield self.create_text_message(
                    f"Resource '{resource_id}' not found."
                )
            else:
                yield self.create_text_message(
                    f"API error: {response.status_code}"
                )
                
        except httpx.HTTPError as e:
            yield self.create_text_message(f"Network error: {e}")
    
    def _get_base_url(self, environment: str) -> str:
        """Get API base URL for environment."""
        urls = {
            "sandbox": "https://api-sandbox.example.com",
            "production": "https://api.example.com"
        }
        return urls.get(environment, urls["sandbox"])
```

## Best Practices

### ✅ DO:

1. **Return structured data**
   ```python
   # Tools should return clean JSON
   yield self.create_json_message({
       "id": "123",
       "status": "success",
       "amount": 100.00
   })
   ```

2. **Handle errors gracefully**
   ```python
   if response.status_code == 401:
       yield self.create_text_message(
           "Authentication failed. Please check your API token."
       )
   elif response.status_code == 404:
       yield self.create_text_message(
           f"Resource '{resource_id}' not found."
       )
   ```

3. **Support multiple environments**
   ```python
   def _get_base_url(self, environment: str) -> str:
       urls = {
           "sandbox": "https://api-sandbox.example.com",
           "production": "https://api.example.com"
       }
       return urls.get(environment, urls["sandbox"])
   ```

4. **Set reasonable timeouts**
   ```python
   response = httpx.get(url, timeout=30)
   ```

5. **Use type hints**
   ```python
   def _invoke(
       self, 
       tool_parameters: dict[str, Any]
   ) -> Generator[ToolInvokeMessage, None, None]:
   ```

### ❌ DON'T:

1. **Use LLM in tools for simple formatting**
   ```python
   # ❌ BAD
   yield self.create_text_message(
       self.session.model.summary.invoke(...)
   )
   
   # ✅ GOOD
   yield self.create_json_message(data)
   ```

2. **Use wrong exception types**
   ```python
   # ❌ BAD - httpx.RequestException doesn't exist
   except httpx.RequestException as e:
   
   # ✅ GOOD
   except httpx.HTTPError as e:
   ```

3. **Hardcode URLs**
   ```python
   # ❌ BAD
   url = "https://api.example.com/v1/data"
   
   # ✅ GOOD
   url = f"{self._get_base_url(environment)}/data"
   ```

4. **Use invalid tags**
   ```yaml
   # ❌ BAD
   tags:
     - banking      # Invalid
     - payments     # Invalid
   
   # ✅ GOOD - Use one of 19 valid tags
   tags:
     - finance
     - utilities
   ```

## Valid Tags (19 Valid Tags)

```yaml
- search        # Search tools and services
- image         # Image generation, editing, analysis
- videos        # Video processing, creation
- weather       # Weather information services
- finance       # Financial services, banking, accounting
- design        # Design tools and services
- travel        # Travel and booking services
- social        # Social media integrations
- news          # News and RSS feeds
- medical       # Healthcare and medical services
- productivity  # Productivity and workflow tools
- education     # Educational tools and content
- business      # Business operations and CRM
- entertainment # Entertainment and gaming
- utilities     # General utility tools
- agent         # Agent-related functionality
- rag           # RAG and knowledge base tools
- trigger       # Trigger/event plugins
- other         # Miscellaneous
```

## Code Review Checklist

- [ ] No unnecessary LLM calls in tools
- [ ] Using `httpx.HTTPError` (not `RequestException`)
- [ ] Environment selection works correctly
- [ ] No hardcoded URLs or credentials
- [ ] User-friendly error messages
- [ ] Reasonable timeout values (recommended 30s)
- [ ] Using valid tags
- [ ] Complete type hints

## Related Skills

- **01-design**: Design phase
- **02-api-reference**: API documentation reference
- **04-testing**: Testing and validation
- **05-packaging**: Packaging and release
- **dify-plugin**: Complete development guide

## Reference

### Official Resources (Must Read!)

- **Official Plugin Repository**: https://github.com/langgenius/dify-official-plugins
  - Always `git pull` before development to get latest version
  - Contains Tools, Models, Extensions and other plugin examples
  
- **Recommended Reference Plugins**:
  | Scenario | Plugin | Path |
  |----------|--------|------|
  | Simple API | arxiv | `tools/arxiv/` |
  | OAuth Auth | github | `tools/github/` |
  | Search | google | `tools/google/` |
  | Complex Workflow | slack | `tools/slack/` |

### Local Resources

- `dify-plugin` skill: Complete Dify plugin development guide
- `dify-plugin/references/tool-plugin.md`: Tool plugin detailed reference
- `dify-plugin/references/trigger-plugin.md`: Trigger plugin detailed reference
