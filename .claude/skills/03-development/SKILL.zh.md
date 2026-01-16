# 插件开发阶段

插件开发的代码实现阶段，包括编码规范、实现模式和最佳实践。

## 何时使用此技能

- 编写插件代码
- 实现 Provider 和 Tools
- 遵循编码规范
- 处理错误和边缘情况

## ⭐ 官方插件参考 (最重要!)

开发前**必须**先获取官方插件仓库作为参考。这是最可靠的实现模式来源。

### 步骤 0: 获取官方插件仓库

```bash
# 首次克隆
cd /path/to/your/workspace
git clone https://github.com/langgenius/dify-official-plugins.git

# 开发前更新 (务必执行!)
cd dify-official-plugins
git pull origin main
```

### 仓库结构

```
dify-official-plugins/
├── tools/                    # Tool 插件
│   ├── google/               # Google 搜索
│   ├── github/               # GitHub 集成
│   ├── slack/                # Slack 集成
│   ├── arxiv/                # 学术论文搜索
│   ├── wikipedia/            # 维基百科
│   └── ...
├── extensions/               # Extension 插件
│   └── ...
├── models/                   # Model 插件
│   ├── openai/
│   ├── anthropic/
│   ├── azure_openai/
│   └── ...
└── agent-strategies/         # Agent Strategy 插件
    └── ...
```

### 如何查找参考示例

根据你的插件类型查找类似的官方实现：

| 需求类型 | 推荐参考 | 路径 |
|----------|----------|------|
| 简单 API 集成 | arxiv, wikipedia | `tools/arxiv/`, `tools/wikipedia/` |
| OAuth API 集成 | github, slack, google | `tools/github/`, `tools/slack/` |
| 金融/支付 | stripe (如有) | `tools/stripe/` |
| Webhook/Trigger | github, slack | 查找 `_trigger` 后缀 |
| 搜索功能 | google, bing, tavily | `tools/google/`, `tools/tavily/` |

### 参考开发流程

```bash
# 1. 更新官方仓库
cd /path/to/dify-official-plugins
git pull

# 2. 查找类似插件
ls tools/  # 查看可用的 tool 插件

# 3. 研究其结构
tree tools/github -L 2

# 4. 复制作为模板
cp -r tools/github /path/to/my_project/my_plugin

# 5. 修改为你的实现
```

### 必须参考的关键文件

对于每个参考插件，重点关注：

```bash
# 1. manifest.yaml - 插件元数据格式
cat tools/github/manifest.yaml

# 2. provider/*.yaml - 认证配置
cat tools/github/provider/github.yaml

# 3. provider/*.py - Provider 实现 (特别是 OAuth)
cat tools/github/provider/github.py

# 4. tools/*.py - Tool 实现模式
cat tools/github/tools/github_repositories.py
```

### 常见场景参考

#### OAuth 2.0 认证
```bash
# 参考 GitHub 的 OAuth 实现
cat tools/github/provider/github.py
# 关注: _oauth_get_authorization_url, _oauth_get_credentials
```

#### API Key 认证
```bash
# 参考 arxiv 的简单认证
cat tools/arxiv/provider/arxiv.py
```

#### Webhook/Trigger
```bash
# 查找 trigger 类型插件
find . -name "*trigger*" -type d
```

### 开发参考检查清单

- [ ] 已用 `git pull` 更新官方仓库
- [ ] 找到了类似的官方插件
- [ ] 研究了其 manifest.yaml 格式
- [ ] 研究了其 provider 认证实现
- [ ] 研究了其 tools 实现模式
- [ ] 对比了错误处理方式

## 插件目录结构

```
my_plugin/
├── _assets/
│   └── icon.svg           # 插件图标 (必需)
├── provider/
│   ├── my_provider.yaml   # Provider 配置
│   └── my_provider.py     # Provider 实现
├── tools/                 # Tool 插件
│   ├── get_data.yaml
│   └── get_data.py
├── events/                # Trigger 插件
│   ├── webhook.yaml
│   └── webhook.py
├── manifest.yaml          # 插件元数据
├── main.py                # 入口点
└── requirements.txt       # 依赖
```

## 最佳实践

### ✅ 应该做:

1. **返回结构化数据**
   ```python
   # Tools 应返回干净的 JSON
   yield self.create_json_message({
       "id": "123",
       "status": "success",
       "amount": 100.00
   })
   ```

2. **优雅处理错误**
   ```python
   if response.status_code == 401:
       yield self.create_text_message(
           "认证失败。请检查您的 API token。"
       )
   elif response.status_code == 404:
       yield self.create_text_message(
           f"资源 '{resource_id}' 未找到。"
       )
   ```

3. **支持多环境**
   ```python
   def _get_base_url(self, environment: str) -> str:
       urls = {
           "sandbox": "https://api-sandbox.example.com",
           "production": "https://api.example.com"
       }
       return urls.get(environment, urls["sandbox"])
   ```

4. **设置合理超时**
   ```python
   response = httpx.get(url, timeout=30)
   ```

5. **使用类型提示**
   ```python
   def _invoke(
       self, 
       tool_parameters: dict[str, Any]
   ) -> Generator[ToolInvokeMessage, None, None]:
   ```

### ❌ 不应该做:

1. **在工具中使用 LLM 进行简单格式化**
   ```python
   # ❌ 错误
   yield self.create_text_message(
       self.session.model.summary.invoke(...)
   )
   
   # ✅ 正确
   yield self.create_json_message(data)
   ```

2. **使用错误的异常类型**
   ```python
   # ❌ 错误 - httpx.RequestException 不存在
   except httpx.RequestException as e:
   
   # ✅ 正确
   except httpx.HTTPError as e:
   ```

3. **硬编码 URL**
   ```python
   # ❌ 错误
   url = "https://api.example.com/v1/data"
   
   # ✅ 正确
   url = f"{self._get_base_url(environment)}/data"
   ```

4. **使用无效标签**
   ```yaml
   # ❌ 错误
   tags:
     - banking      # 无效
     - payments     # 无效
   
   # ✅ 正确 - 使用 19 个有效标签之一
   tags:
     - finance
     - utilities
   ```

## 有效标签 (19 个有效标签)

```yaml
- search        # 搜索工具和服务
- image         # 图像生成、编辑、分析
- videos        # 视频处理、创建
- weather       # 天气信息服务
- finance       # 金融服务、银行、会计
- design        # 设计工具和服务
- travel        # 旅行和预订服务
- social        # 社交媒体集成
- news          # 新闻和 RSS 订阅
- medical       # 医疗保健服务
- productivity  # 生产力和工作流工具
- education     # 教育工具和内容
- business      # 业务运营和 CRM
- entertainment # 娱乐和游戏
- utilities     # 通用工具
- agent         # Agent 相关功能
- rag           # RAG 和知识库工具
- trigger       # 触发器/事件插件
- other         # 其他
```

## 代码审查检查清单

- [ ] 工具中没有不必要的 LLM 调用
- [ ] 使用 `httpx.HTTPError` (不是 `RequestException`)
- [ ] 环境选择正确工作
- [ ] 没有硬编码的 URL 或凭据
- [ ] 错误消息对用户友好
- [ ] 超时值合理 (推荐 30s)
- [ ] 使用有效的标签
- [ ] 类型提示完整

## 相关技能

- **01-design**: 设计阶段
- **02-api-reference**: API 文档参考
- **04-testing**: 测试验证
- **05-packaging**: 打包发布
- **dify-plugin**: 完整开发指南

## 参考资料

### 官方资源 (必读!)

- **官方插件仓库**: https://github.com/langgenius/dify-official-plugins
  - 开发前务必 `git pull` 获取最新版本
  - 包含 Tools, Models, Extensions 等各类插件示例
  
- **推荐参考插件**:
  | 场景 | 插件 | 路径 |
  |------|------|------|
  | 简单 API | arxiv | `tools/arxiv/` |
  | OAuth 认证 | github | `tools/github/` |
  | 搜索功能 | google | `tools/google/` |
  | 复杂工作流 | slack | `tools/slack/` |

### 本地资源

- `dify-plugin` skill: 完整的 Dify 插件开发指南
- `dify-plugin/references/tool-plugin.md`: Tool 插件详细参考
- `dify-plugin/references/trigger-plugin.md`: Trigger 插件详细参考
