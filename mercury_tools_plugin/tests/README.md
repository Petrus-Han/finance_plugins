# Mercury Tools Plugin 测试目录

## 目录结构

```
tests/
├── api/                    # API 测试 - 直接调用 Mercury API
│   ├── test_mercury_api.py         # 基础 API 连通性测试
│   ├── test_mercury_apikey.py      # API Key 详细诊断工具
│   └── test_mercury_tools.py       # Mercury Tools API 功能测试
├── unit/                   # 单元测试 - 使用 Mock 测试插件组件
│   └── test_mercury_tools_local.py # 本地插件工具测试
├── integration/            # 集成测试 - 端到端测试
│   └── (待添加)
└── README.md
```

## 测试类型说明

### API 测试 (`api/`)

直接通过 HTTP 调用 Mercury API，用于验证：
- API Key 是否有效
- API 端点是否可访问
- API 响应格式是否正确

运行示例：
```bash
# 测试 API Key
python tests/api/test_mercury_api.py <API_TOKEN> [sandbox|production]

# 详细 API Key 诊断
python tests/api/test_mercury_apikey.py <API_KEY> [environment]

# 测试 Mercury Tools API
python tests/api/test_mercury_tools.py <API_TOKEN>
```

### 单元测试 (`unit/`)

使用 Mock 对象测试插件组件，不需要真实的网络连接（但目前仍需有效 API Key）：
- Provider 验证逻辑
- Tool 实现逻辑

运行示例：
```bash
python tests/unit/test_mercury_tools_local.py
```

### 集成测试 (`integration/`)

端到端测试，模拟完整的 Dify 插件运行环境：
- 完整工作流测试
- 多工具协作测试

## 环境配置

推荐使用环境变量存储敏感信息：

```bash
export MERCURY_API_KEY="your_api_key"
export MERCURY_ENVIRONMENT="sandbox"  # 或 "production"
```
