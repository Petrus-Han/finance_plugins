# 插件测试阶段

插件开发的测试阶段，包括凭据测试、本地测试和集成测试。

## 何时使用此技能

- 验证 API 凭据
- 本地测试工具
- 端到端集成测试
- 调试插件问题

## 阶段 1: 凭据测试 🔑

### 1.1 设置测试环境

1. 注册开发者账号
2. 创建测试应用
3. 选择沙箱环境 (如果可用)

### 1.2 收集凭据

向用户请求测试凭据或引导他们获取：

```python
# 需要的凭据
credentials = {
    "api_key": "test_xxx",           # API Key
    "access_token": "xxx",           # OAuth Token
    "environment": "sandbox",        # 环境选择
    "realm_id": "xxx"               # 某些 API 需要
}
```

### 1.3 编写诊断脚本

```python
# test_api_key.py - 测试 API 连接
import httpx

API_KEY = "your_test_api_key"
BASE_URL = "https://api-sandbox.example.com/v1"

def test_connection():
    """测试基本 API 连接。"""
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
        
        print(f"状态: {response.status_code}")
        print(f"响应: {response.text[:500]}")
        
        if response.status_code == 200:
            print("✅ API 连接成功!")
            return True
        else:
            print(f"❌ API 返回错误: {response.status_code}")
            return False
            
    except httpx.HTTPError as e:
        print(f"❌ 网络错误: {e}")
        return False

if __name__ == "__main__":
    test_connection()
```

### 1.4 测试 Provider 验证

```python
# test_provider.py - 测试 Provider 验证
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
        print("✅ Provider 验证通过")
    except Exception as e:
        print(f"❌ 验证失败: {e}")

if __name__ == "__main__":
    test_provider_validation()
```

## 阶段 2: 本地测试 🧪

### 2.1 Mock Runtime 测试

```python
# test_local.py - 本地工具测试
import sys
sys.path.insert(0, "my_plugin")

from tools.get_data import GetDataTool

class MockRuntime:
    """用于本地测试的 Mock Dify runtime。"""
    def __init__(self, credentials: dict):
        self.credentials = credentials

class MockSession:
    """Mock Dify session。"""
    pass

def test_get_data_tool():
    """本地测试 GetDataTool。"""
    
    # 设置 mock
    runtime = MockRuntime({
        "api_key": "your_test_key",
        "environment": "sandbox"
    })
    session = MockSession()
    
    # 创建工具实例
    tool = GetDataTool(runtime=runtime, session=session)
    
    # 使用参数测试
    parameters = {
        "resource_id": "test_123",
        "include_details": True
    }
    
    # 调用并收集结果
    results = list(tool._invoke(parameters))
    
    print(f"获得 {len(results)} 条消息:")
    for result in results:
        print(f"  类型: {type(result).__name__}")
        print(f"  内容: {result}")
        print()

if __name__ == "__main__":
    test_get_data_tool()
```

### 2.2 测试多个场景

```python
def test_scenarios():
    """测试多个场景。"""
    
    test_cases = [
        # 正常情况
        {
            "name": "有效资源",
            "params": {"resource_id": "valid_123"},
            "expected": "success"
        },
        # 错误情况
        {
            "name": "无效资源",
            "params": {"resource_id": "invalid_999"},
            "expected": "not_found"
        },
        # 边缘情况
        {
            "name": "空 ID",
            "params": {"resource_id": ""},
            "expected": "error"
        }
    ]
    
    for tc in test_cases:
        print(f"\n--- 测试: {tc['name']} ---")
        results = list(tool._invoke(tc["params"]))
        
        # 检查结果
        if tc["expected"] == "success":
            assert len(results) > 0
            print("✅ 通过")
        elif tc["expected"] == "not_found":
            assert "not found" in str(results[0]).lower()
            print("✅ 通过")
        else:
            print(f"结果: {results}")
```

## 阶段 3: 打包测试 📦

### 3.1 验证打包

```bash
cd /path/to/finance_plugins

# 打包插件
dify plugin package ./my_plugin -o ./dist/my_plugin.difypkg

# 检查打包结果
ls -la dist/my_plugin.difypkg

# 验证校验和
dify plugin checksum ./dist/my_plugin.difypkg
```

### 3.2 检查包内容

```bash
# 解压查看内容 (difypkg 是 zip 格式)
unzip -l ./dist/my_plugin.difypkg
```

## 阶段 4: 集成测试 🔄

### 4.1 上传并配置

1. 上传 `.difypkg` 到 Dify
2. 在 UI 中配置凭据
3. 测试 OAuth 流程 (如适用)

### 4.2 工具测试清单

系统地测试每个工具：

| 测试类型 | 描述 | 预期结果 |
|----------|------|----------|
| ✅ 正常情况 | 有效输入，成功响应 | 返回正确数据 |
| ❌ 错误情况 | 无效输入，API 错误 | 友好的错误消息 |
| 🔍 边缘情况 | 空结果，速率限制 | 优雅处理 |

### 4.3 集成测试

1. 在 Dify 中创建测试工作流
2. 串联多个工具
3. 验证数据在工具之间正确传递
4. 测试工作流中的错误处理

## 调试指南 🐛

### 常见错误及解决方案

#### 错误: "permission denied, you need to enable llm access"

**原因**: 工具调用了 `self.session.model.summary.invoke()` 但 manifest 没有 model 权限。

**解决**: 从工具中移除 LLM 调用，直接返回 JSON。

```python
# ❌ 错误
yield self.create_text_message(
    self.session.model.summary.invoke(...)
)

# ✅ 正确
yield self.create_json_message(data)
```

#### 错误: "AttributeError: module 'httpx' has no attribute 'RequestException'"

**原因**: 使用了不存在的异常类型。

**解决**: 改用 `httpx.HTTPError`:

```python
# ❌ 错误
except httpx.RequestException as e:

# ✅ 正确
except httpx.HTTPError as e:
```

#### 错误: 生产环境 "401 Unauthorized"

**原因**: 在生产环境使用了沙箱凭据。

**解决**: 添加环境选择并为每个环境使用正确的凭据。

#### 错误: API 调用 "404 Not Found"

**原因**: 错误的 API base URL。

**解决**: 验证 URL 构建和环境选择逻辑。

#### 工具返回空数据

**原因**: API 响应结构变化或凭据缺少权限。

**解决**:
1. 编写诊断脚本直接测试 API
2. 检查 API 响应结构
3. 验证凭据范围/权限

#### 错误: "Field validation for 'Tags[X]' failed"

**原因**: 使用了无效的标签。

**解决**: 只使用 19 个有效标签。

### 远程调试

```bash
# 1. 从 Dify 控制台获取调试密钥
# Plugins → Remote Debugging

# 2. 创建 .env 文件
cat > .env << EOF
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=https://your-dify.com
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=your-debug-key
EOF

# 3. 运行插件
uv run python -m main
```

## 测试脚本模板

```python
#!/usr/bin/env python3
"""
插件测试套件
用法: python test_plugin.py
"""

import sys
sys.path.insert(0, "my_plugin")

from provider.my_provider import MyProvider
from tools.get_data import GetDataTool

# 测试凭据 (从环境变量或配置获取)
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
    """测试 provider 验证。"""
    print("\n=== 测试 Provider ===")
    provider = MyProvider()
    try:
        provider._validate_credentials(CREDENTIALS)
        print("✅ Provider 验证通过")
        return True
    except Exception as e:
        print(f"❌ Provider 验证失败: {e}")
        return False

def test_get_data():
    """测试 get_data 工具。"""
    print("\n=== 测试 GetDataTool ===")
    
    runtime = MockRuntime(CREDENTIALS)
    session = MockSession()
    tool = GetDataTool(runtime=runtime, session=session)
    
    # 测试用例
    test_cases = [
        {"resource_id": "valid_123", "expected": "success"},
        {"resource_id": "invalid_999", "expected": "not_found"},
    ]
    
    all_passed = True
    for tc in test_cases:
        print(f"\n  测试 resource_id={tc['resource_id']}")
        try:
            results = list(tool._invoke({"resource_id": tc["resource_id"]}))
            print(f"  结果: {results[0] if results else '无结果'}")
            print(f"  ✅ 完成")
        except Exception as e:
            print(f"  ❌ 错误: {e}")
            all_passed = False
    
    return all_passed

def main():
    """运行所有测试。"""
    print("=" * 50)
    print("插件测试套件")
    print("=" * 50)
    
    results = {
        "Provider": test_provider(),
        "GetDataTool": test_get_data(),
    }
    
    print("\n" + "=" * 50)
    print("总结:")
    for name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"  {name}: {status}")
    
    all_passed = all(results.values())
    print("\n" + ("所有测试通过!" if all_passed else "部分测试失败!"))
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
```

## 相关技能

- **01-design**: 设计阶段
- **02-api-reference**: API 文档参考
- **03-development**: 开发实现
- **05-packaging**: 打包发布
- **dify-plugin/references/debugging.md**: 详细调试指南
