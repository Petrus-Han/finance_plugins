# API 参考文档收集

收集和整理 API 文档，为插件开发做准备。

## 何时使用此技能

- 研究目标 API 的认证方式
- 整理 API 端点和参数
- 记录 API 限制和注意事项
- 创建 API 文档参考

## API 文档结构

### 标准 API 文档模板

```markdown
# [服务名称] API 文档

## 概述
- 基础 URL: `https://api.example.com/v1`
- 认证方式: OAuth 2.0 / API Key
- 速率限制: 100 请求/分钟

## 认证

### OAuth 2.0 流程
1. 授权 URL: `https://auth.example.com/authorize`
2. Token URL: `https://auth.example.com/token`
3. Scopes: `read`, `write`

### 请求头
```http
Authorization: Bearer {access_token}
Content-Type: application/json
Accept: application/json
```

## 端点

### 获取资源
```http
GET /resources
```

**参数:**
| 名称 | 类型 | 必需 | 描述 |
|------|------|------|------|
| limit | integer | 否 | 最大结果数 (默认: 50) |
| offset | integer | 否 | 分页偏移量 |

**响应:**
```json
{
  "data": [...],
  "meta": {"total": 100}
}
```

## 错误码
| 状态码 | 含义 | 处理方式 |
|--------|------|----------|
| 400 | 请求错误 | 检查参数 |
| 401 | 未授权 | 刷新 token |
| 429 | 速率限制 | 退避重试 |
```

## 现有 API 参考

本项目中可用的 API 文档：

### Mercury Bank API
- 位置: `archive/Mercury_API_Documentation.md`
- 用于: `mercury_tools_plugin`, `mercury_trigger_plugin`

### QuickBooks Online API
- 位置: `archive/QuickBooks_API_Documentation.md`
- 用于: `quickbooks_plugin`

### QuickBooks Payments API
- 位置: `QuickBooks_Payments_API_Documentation.md`
- 用于: `quickbooks_payments_plugin`

## 如何研究新 API

### 步骤 1: 获取官方文档

1. 访问服务商开发者门户
2. 注册开发者账号
3. 创建应用获取凭据
4. 下载或阅读 API 文档

### 步骤 2: 识别关键信息

```yaml
api_research_checklist:
  authentication:
    - type: "OAuth 2.0 / API Key / Token"
    - authorization_url: ""
    - token_url: ""
    - scopes: []
    
  base_urls:
    sandbox: ""
    production: ""
    
  rate_limits:
    requests_per_minute: 100
    requests_per_day: 10000
    
  required_headers:
    - "Authorization"
    - "Content-Type"
    
  common_endpoints:
    - "GET /resources"
    - "POST /resources"
    - "GET /resources/{id}"
```

### 步骤 3: 编写诊断脚本

```python
# test_api.py - 测试 API 连接
import httpx

API_KEY = "your_api_key"
BASE_URL = "https://api.example.com/v1"

def test_connection():
    """测试基本 API 连接。"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = httpx.get(f"{BASE_URL}/ping", headers=headers)
    print(f"状态: {response.status_code}")
    print(f"响应: {response.text}")
    
    if response.status_code == 200:
        print("✅ API 连接成功!")
    else:
        print("❌ API 连接失败!")

if __name__ == "__main__":
    test_connection()
```

### 步骤 4: 记录端点详情

为每个需要的端点记录：

```yaml
endpoint:
  name: "获取账户"
  method: GET
  path: "/accounts"
  
  request:
    headers:
      Authorization: "Bearer {token}"
    query_params:
      - name: limit
        type: integer
        required: false
        default: 50
        
  response:
    success:
      status: 200
      body:
        accounts:
          - id: "string"
            name: "string"
            balance: "number"
    errors:
      - status: 401
        meaning: "未授权"
      - status: 404
        meaning: "未找到"
```

## API 认证模式

### 模式 1: API Key

```python
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
```

### 模式 2: OAuth 2.0

```python
class OAuthProvider(ToolProvider):
    def _oauth_get_authorization_url(self, system_credentials):
        return {
            "url": f"{AUTH_URL}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}"
        }
    
    def _oauth_get_credentials(self, system_credentials, code):
        # 用授权码换取 token
        response = httpx.post(TOKEN_URL, data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret
        })
        return response.json()
    
    def _oauth_refresh_credentials(self, system_credentials, credentials):
        # 刷新过期的 token
        response = httpx.post(TOKEN_URL, data={
            "grant_type": "refresh_token",
            "refresh_token": credentials["refresh_token"],
            "client_id": client_id,
            "client_secret": client_secret
        })
        return response.json()
```

### 模式 3: 签名验证 (Webhook)

```python
import hmac
import hashlib

def verify_signature(payload, signature, secret):
    """验证 webhook 签名。"""
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

## 常见 API 约定

### RESTful 端点

```
GET    /resources          # 列出所有
GET    /resources/{id}     # 获取单个
POST   /resources          # 创建
PUT    /resources/{id}     # 更新
DELETE /resources/{id}     # 删除
```

### 分页

```python
# 偏移量分页
GET /resources?offset=0&limit=50

# 游标分页
GET /resources?cursor=abc123&limit=50
```

### 日期格式

```python
# ISO 8601
"2025-01-16T12:00:00Z"

# Unix 时间戳
1705406400
```

### 错误响应格式

```json
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "请求无效",
    "details": [
      {"field": "amount", "issue": "必须为正数"}
    ]
  }
}
```

## 相关技能

- **01-design**: 设计阶段
- **03-development**: 开发实现 (使用这些 API)
- **04-testing**: 测试 API 调用
- **05-packaging**: 打包发布

## 快速参考

### 常见 HTTP 状态码

| 状态码 | 含义 | 插件处理方式 |
|--------|------|--------------|
| 200 | 成功 | 返回数据 |
| 201 | 已创建 | 返回创建的资源 |
| 400 | 请求错误 | 返回验证错误 |
| 401 | 未授权 | 刷新 token / 重新认证 |
| 403 | 禁止访问 | 检查权限 |
| 404 | 未找到 | 返回未找到消息 |
| 429 | 速率限制 | 退避重试 |
| 500 | 服务器错误 | 重试或优雅失败 |

### httpx 最佳实践

```python
import httpx

# 推荐配置
client = httpx.Client(
    timeout=30.0,
    headers={"User-Agent": "DifyPlugin/1.0"}
)

# 错误处理
try:
    response = client.get(url)
    response.raise_for_status()
except httpx.HTTPError as e:
    # 处理错误
    pass
```
