---
name: plugin-testing
description: Guide for Dify plugin testing phase - credential testing, local testing, and integration testing. Use when validating credentials, testing tools locally, or performing end-to-end testing.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Plugin Testing Phase

Testing phase for plugin development, including credential testing, local testing, and integration testing.

## When to Use This Skill

- Validating API credentials
- Testing tools locally
- End-to-end integration testing
- Debugging plugin issues

## Phase 1: Credential Testing 🔑

### 1.1 Setup Test Environment

1. Register developer account
2. Create test application
3. Choose sandbox environment (if available)

### 1.2 Collect Credentials

Request test credentials from user or guide them to obtain:

```python
# Required credentials
credentials = {
    "api_key": "test_xxx",           # API Key
    "access_token": "xxx",           # OAuth Token
    "environment": "sandbox",        # Environment selection
    "realm_id": "xxx"               # Required by some APIs
}
```

### 1.3 Write Diagnostic Script

```python
# test_api_key.py - Test API connectivity
import httpx

API_KEY = "your_test_api_key"
BASE_URL = "https://api-sandbox.example.com/v1"

def test_connection():
    """Test basic API connectivity."""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = httpx.get(
            f"{BASE_URL}/ping",
            headers=headers,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
        if response.status_code == 200:
            print("✅ API connection successful!")
            return True
        else:
            print(f"❌ API returned error: {response.status_code}")
            return False
            
    except httpx.HTTPError as e:
        print(f"❌ Network error: {e}")
        return False

if __name__ == "__main__":
    test_connection()
```

### 1.4 Test Provider Validation

```python
# test_provider.py - Test Provider validation
import sys
sys.path.insert(0, "my_plugin")

from provider.my_provider import MyProvider

def test_provider_validation():
    provider = MyProvider()
    
    credentials = {
        "api_key": "test_key",
        "environment": "sandbox"
    }
    
    try:
        provider._validate_credentials(credentials)
        print("✅ Provider validation passed")
    except Exception as e:
        print(f"❌ Validation failed: {e}")

if __name__ == "__main__":
    test_provider_validation()
```

## Phase 2: Local Testing 🧪

### 2.1 Mock Runtime Testing

```python
# test_local.py - Local tool testing
import sys
sys.path.insert(0, "my_plugin")

from tools.get_data import GetDataTool

class MockRuntime:
    """Mock Dify runtime for local testing."""
    def __init__(self, credentials: dict):
        self.credentials = credentials

class MockSession:
    """Mock Dify session."""
    pass

def test_get_data_tool():
    """Test GetDataTool locally."""
    
    # Setup mock
    runtime = MockRuntime({
        "api_key": "your_test_key",
        "environment": "sandbox"
    })
    session = MockSession()
    
    # Create tool instance
    tool = GetDataTool(runtime=runtime, session=session)
    
    # Test with parameters
    parameters = {
        "resource_id": "test_123",
        "include_details": True
    }
    
    # Invoke and collect results
    results = list(tool._invoke(parameters))
    
    print(f"Got {len(results)} messages:")
    for result in results:
        print(f"  Type: {type(result).__name__}")
        print(f"  Content: {result}")
        print()

if __name__ == "__main__":
    test_get_data_tool()
```

### 2.2 Test Multiple Scenarios

```python
def test_scenarios():
    """Test multiple scenarios."""
    
    test_cases = [
        # Normal case
        {
            "name": "Valid resource",
            "params": {"resource_id": "valid_123"},
            "expected": "success"
        },
        # Error case
        {
            "name": "Invalid resource",
            "params": {"resource_id": "invalid_999"},
            "expected": "not_found"
        },
        # Edge case
        {
            "name": "Empty ID",
            "params": {"resource_id": ""},
            "expected": "error"
        }
    ]
    
    for tc in test_cases:
        print(f"\n--- Testing: {tc['name']} ---")
        results = list(tool._invoke(tc["params"]))
        
        # Check results
        if tc["expected"] == "success":
            assert len(results) > 0
            print("✅ Passed")
        elif tc["expected"] == "not_found":
            assert "not found" in str(results[0]).lower()
            print("✅ Passed")
        else:
            print(f"Result: {results}")
```

## Phase 3: Package Testing 📦

### 3.1 Validate Packaging

```bash
cd /path/to/finance_plugins

# Package plugin
dify plugin package ./my_plugin -o ./dist/my_plugin.difypkg

# Check packaging result
ls -la dist/my_plugin.difypkg

# Verify checksum
dify plugin checksum ./dist/my_plugin.difypkg
```

### 3.2 Inspect Package Contents

```bash
# Unzip to view contents (difypkg is zip format)
unzip -l ./dist/my_plugin.difypkg
```

## Phase 4: Integration Testing 🔄

### 4.1 Upload and Configure

1. Upload `.difypkg` to Dify
2. Configure credentials in UI
3. Test OAuth flow (if applicable)

### 4.2 Tool Testing Checklist

Systematically test each tool:

| Test Type | Description | Expected Result |
|-----------|-------------|-----------------|
| ✅ Normal case | Valid inputs, successful response | Returns correct data |
| ❌ Error case | Invalid inputs, API errors | Friendly error message |
| 🔍 Edge case | Empty results, rate limits | Graceful handling |

### 4.3 Integration Testing

1. Create test workflow in Dify
2. Chain multiple tools together
3. Verify data passes correctly between tools
4. Test error handling in workflow

## Debugging Guide 🐛

### Common Errors and Solutions

#### Error: "permission denied, you need to enable llm access"

**Cause**: Tool is calling `self.session.model.summary.invoke()` but manifest doesn't have model permission.

**Solution**: Remove LLM calls from tools, return JSON directly.

```python
# ❌ BAD
yield self.create_text_message(
    self.session.model.summary.invoke(...)
)

# ✅ GOOD
yield self.create_json_message(data)
```

#### Error: "AttributeError: module 'httpx' has no attribute 'RequestException'"

**Cause**: Using non-existent exception type.

**Solution**: Change to `httpx.HTTPError`:

```python
# ❌ BAD
except httpx.RequestException as e:

# ✅ GOOD
except httpx.HTTPError as e:
```

#### Error: "401 Unauthorized" in production

**Cause**: Using sandbox credentials in production environment.

**Solution**: Add environment selection and use correct credentials for each environment.

#### Error: "404 Not Found" on API calls

**Cause**: Wrong API base URL.

**Solution**: Verify URL construction and environment selection logic.

#### Tool returns empty data

**Cause**: API response structure changed or credentials lack permissions.

**Solution**:
1. Write diagnostic script to test API directly
2. Check API response structure
3. Verify credential scopes/permissions

#### Error: "Field validation for 'Tags[X]' failed"

**Cause**: Using invalid tag.

**Solution**: Use only 19 valid tags.

### Remote Debugging

```bash
# 1. Get debug key from Dify console
# Plugins → Remote Debugging

# 2. Create .env file
cat > .env << EOF
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=https://your-dify.com
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=your-debug-key
EOF

# 3. Run plugin
uv run python -m main
```

## Test Script Template

```python
#!/usr/bin/env python3
"""
Plugin Test Suite
Usage: python test_plugin.py
"""

import sys
sys.path.insert(0, "my_plugin")

from provider.my_provider import MyProvider
from tools.get_data import GetDataTool

# Test credentials (from environment or config)
CREDENTIALS = {
    "api_key": "your_test_key",
    "environment": "sandbox"
}

class MockRuntime:
    def __init__(self, credentials):
        self.credentials = credentials

class MockSession:
    pass

def test_provider():
    """Test provider validation."""
    print("\n=== Testing Provider ===")
    provider = MyProvider()
    try:
        provider._validate_credentials(CREDENTIALS)
        print("✅ Provider validation passed")
        return True
    except Exception as e:
        print(f"❌ Provider validation failed: {e}")
        return False

def test_get_data():
    """Test get_data tool."""
    print("\n=== Testing GetDataTool ===")
    
    runtime = MockRuntime(CREDENTIALS)
    session = MockSession()
    tool = GetDataTool(runtime=runtime, session=session)
    
    # Test cases
    test_cases = [
        {"resource_id": "valid_123", "expected": "success"},
        {"resource_id": "invalid_999", "expected": "not_found"},
    ]
    
    all_passed = True
    for tc in test_cases:
        print(f"\n  Testing resource_id={tc['resource_id']}")
        try:
            results = list(tool._invoke({"resource_id": tc["resource_id"]}))
            print(f"  Result: {results[0] if results else 'No results'}")
            print(f"  ✅ Completed")
        except Exception as e:
            print(f"  ❌ Error: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests."""
    print("=" * 50)
    print("Plugin Test Suite")
    print("=" * 50)
    
    results = {
        "Provider": test_provider(),
        "GetDataTool": test_get_data(),
    }
    
    print("\n" + "=" * 50)
    print("Summary:")
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name}: {status}")
    
    all_passed = all(results.values())
    print("\n" + ("All tests passed!" if all_passed else "Some tests failed!"))
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
```

## Related Skills

- **01-design**: Design phase
- **02-api-reference**: API documentation reference
- **03-development**: Development implementation
- **05-packaging**: Packaging and release
- **dify-plugin/references/debugging.md**: Detailed debugging guide
