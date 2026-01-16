---
name: plugin-packaging
description: Guide for Dify plugin packaging and release phase - building, versioning, and distribution. Use when packaging plugins, managing versions, or preparing for release.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Plugin Packaging & Release Phase

Packaging and release phase for plugin development, including building, version management, and distribution.

## When to Use This Skill

- Packaging plugins as .difypkg files
- Managing version numbers
- Preparing for release
- Maintenance and iteration

## Output Directory Convention

**Important**: All `.difypkg` files should be output to the `dist/` directory in the project root.

```
finance_plugins/
├── dist/                           # All packaged plugin files
│   ├── quickbooks_plugin.difypkg
│   ├── quickbooks_payments_plugin.difypkg
│   ├── mercury_tools_plugin.difypkg
│   └── mercury_trigger_plugin.difypkg
├── quickbooks_plugin/              # Plugin source code
├── quickbooks_payments_plugin/
├── mercury_tools_plugin/
├── mercury_trigger_plugin/
└── archive/                        # Documentation and archives
```

## Packaging Commands

### Single Plugin Packaging

```bash
# Go to project root directory
cd /path/to/finance_plugins

# Package single plugin to dist/ directory
dify plugin package ./mercury_tools_plugin -o ./dist/mercury_tools_plugin.difypkg

# Verify packaging result
ls -la ./dist/mercury_tools_plugin.difypkg
```

### Batch Packaging Script

```bash
#!/bin/bash
# build_all.sh - Batch package all plugins to dist/ directory

set -e

PROJECT_ROOT="/path/to/finance_plugins"
DIST_DIR="${PROJECT_ROOT}/dist"

# Ensure dist directory exists
mkdir -p "$DIST_DIR"

cd "$PROJECT_ROOT"

# Iterate all *_plugin directories
for plugin_dir in *_plugin/; do
    plugin_name="${plugin_dir%/}"
    output_file="${DIST_DIR}/${plugin_name}.difypkg"
    
    echo "📦 Packaging ${plugin_name}..."
    
    # Package
    if dify plugin package "./${plugin_dir}" -o "$output_file"; then
        echo "   ✅ Created: ${output_file}"
    else
        echo "   ❌ Failed to package ${plugin_name}"
        exit 1
    fi
done

echo ""
echo "🎉 All plugins packaged successfully!"
echo ""
echo "Output files:"
ls -la "$DIST_DIR"/*.difypkg
```

### Verify Packaging

```bash
# Verify checksum
dify plugin checksum ./dist/mercury_tools_plugin.difypkg

# View package contents (difypkg is zip format)
unzip -l ./dist/mercury_tools_plugin.difypkg
```

## Version Management

### Semantic Versioning

```yaml
# Semantic Versioning: major.minor.patch
version: 0.1.0  # Initial release
version: 0.2.0  # New feature (backward compatible)
version: 0.2.1  # Bug fix
version: 1.0.0  # Breaking change
```

### Version Upgrade Rules

| Change Type | Version Part | Example |
|-------------|--------------|---------|
| Bug fix | patch | 0.1.0 → 0.1.1 |
| New feature (compatible) | minor | 0.1.1 → 0.2.0 |
| Breaking change | major | 0.2.0 → 1.0.0 |

### Update Version Number

Update version in `manifest.yaml`:

```yaml
version: 0.2.0  # Update here

# ... other configuration ...

meta:
  version: 0.2.0  # Sync update here
```

## Quality Checklist

### Pre-Release Checklist

```yaml
pre_release_checklist:
  code_quality:
    - [ ] No hardcoded credentials
    - [ ] No sensitive data
    - [ ] Clear code comments
    - [ ] User-friendly error messages
    
  functionality:
    - [ ] All tools tested
    - [ ] Provider validation works
    - [ ] Error handling complete
    - [ ] Multi-environment support
    
  configuration:
    - [ ] .gitignore configured correctly
    - [ ] manifest.yaml complete
    - [ ] Version number updated
    - [ ] Using valid tags
    
  documentation:
    - [ ] README.md exists
    - [ ] Usage instructions clear
    - [ ] Authentication setup documented
```

### Sensitive Data Check

```bash
# Check for hardcoded credentials
grep -r "api_key\|secret\|password\|token" ./my_plugin --include="*.py" | grep -v "def\|#\|credentials"

# Check .gitignore
cat .gitignore
```

## Documentation

### README Template

```markdown
# [Plugin Name]

## Overview
Brief description of plugin purpose.

## Features
- Feature 1
- Feature 2
- Feature 3

## Installation
1. Download `plugin_name.difypkg`
2. Upload plugin in Dify console
3. Configure credentials

## Configuration

### Credentials
| Field | Description | Required |
|-------|-------------|----------|
| API Key | Your API key | Yes |
| Environment | sandbox/production | Yes |

### Getting API Key
1. Visit [Developer Portal](https://...)
2. Create application
3. Copy API Key

## Available Tools

### get_data
Retrieve data from the service.

**Parameters:**
- `resource_id` (string, required): Resource ID

**Example:**
```json
{
  "resource_id": "123"
}
```

## Testing
See `test_plugin.py`

## Version History
- 0.1.0: Initial release
- 0.2.0: Added xxx feature
```

## Maintenance & Iteration

### 8.1 Monitor Issues

- Track user feedback
- Log common errors
- Identify improvement areas

### 8.2 Add Features

```bash
# 1. Update code
# 2. Update minor version
# manifest.yaml: version: 0.1.0 → 0.2.0

# 3. Re-package
dify plugin package ./my_plugin -o ./dist/my_plugin.difypkg

# 4. Test
# 5. Release
```

### 8.3 Fix Bugs

```bash
# 1. Fix code
# 2. Update patch version
# manifest.yaml: version: 0.1.0 → 0.1.1

# 3. Re-package
dify plugin package ./my_plugin -o ./dist/my_plugin.difypkg

# 4. Verify fix
# 5. Release
```

## CI/CD Integration (Optional)

### GitHub Actions Example

```yaml
# .github/workflows/build.yml
name: Build Plugin

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Dify CLI
        run: |
          # Install dify CLI
          
      - name: Package Plugins
        run: |
          mkdir -p dist
          for dir in *_plugin/; do
            name="${dir%/}"
            dify plugin package "./$dir" -o "./dist/${name}.difypkg"
          done
          
      - name: Upload Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: plugins
          path: dist/*.difypkg
```

## Distribution

### Distribution Methods

1. **Direct Sharing**
   - Send `.difypkg` file
   - User manually uploads to Dify

2. **Internal Repository**
   - Store on internal file server
   - Provide download link

3. **Dify Plugin Marketplace** (if available)
   - Submit to official marketplace
   - Wider distribution

### Release Checklist

```bash
# Final checks
echo "=== Final Release Checklist ==="

# 1. Version number
grep "version:" ./my_plugin/manifest.yaml

# 2. Package size
ls -lh ./dist/my_plugin.difypkg

# 3. Checksum
dify plugin checksum ./dist/my_plugin.difypkg

echo "=== Ready for release! ==="
```

## Related Skills

- **01-design**: Design phase
- **02-api-reference**: API documentation reference
- **03-development**: Development implementation
- **04-testing**: Testing and validation
- **dify-plugin**: Complete development guide
