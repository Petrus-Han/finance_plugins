# Dify 插件开发完整指南

## 目录
1. [概述](#概述)
2. [插件系统架构](#插件系统架构)
3. [插件类型](#插件类型)
4. [开发环境搭建](#开发环境搭建)
5. [插件开发流程](#插件开发流程)
6. [配置文件格式](#配置文件格式)
7. [认证和授权机制](#认证和授权机制)
8. [部署方式](#部署方式)
9. [调试和测试](#调试和测试)
10. [数据传递方法](#数据传递方法)
11. [代码示例](#代码示例)
12. [资源链接](#资源链接)

---

## 概述

Dify 是一个易用的 LLMOps 平台，从 v1.0.0 版本（2025年2月）开始，引入了完整的插件生态系统。插件系统采用解耦架构，每个插件作为独立包运行，可以独立开发、部署和维护。

### 核心特点

- **标准化开发协议**：提供完整的工具链，包括远程调试、代码示例和 API 文档
- **五种插件类型**：Models、Tools、Agent Strategies、Extensions、Bundles
- **多种部署模式**：支持本地、远程、Serverless 部署
- **语义版本控制**：通过 `meta.version` 实现向后兼容，`meta.minimum_dify_version` 实现向前兼容

---

## 插件系统架构

### 架构设计原则

Dify 插件系统采用解耦架构，核心设计特点：

1. **独立包设计**：每个插件作为独立包，可单独安装、配置和使用
2. **统一框架**：所有工具和模型通过统一框架解耦
3. **开放接口**：提供开放接口与外部系统集成
4. **可插拔设计**：RAG 相关功能（文档解析器、OCR）均已插件化

### 运行时架构

#### 本地部署模式
- 插件作为子进程运行，由父进程管理生命周期
- 通过标准输入输出管道（STDIN/STDOUT）通信
- 父进程负责安装依赖和控制插件生命周期

#### SaaS/Serverless 模式
- 采用 Serverless 架构，可根据使用情况弹性扩展
- AWS Lambda 作为高并发、资源利用率和可用性的解决方案
- 通过 HTTP 协议调用插件

#### 远程调试模式
- 监听端口等待调试插件连接
- 基于 TCP 的全双工通信
- 支持主流 IDE，可连接到 Dify SaaS 服务进行本地测试

### 通信架构

插件系统通过自定义端点和 API 建立无缝连接：

- **事件驱动集成**：支持基于特定事件或条件自动执行逻辑
- **双向通信**：插件端点支持外部服务与 Dify 核心功能之间的双向通信
- **标准化接口**：所有插件遵循标准化开发协议

---

## 插件类型

### 1. Model Plugin（模型插件）

**功能**：将 AI 模型集成到 Dify 平台

**特点**：
- 支持 LLM、文本嵌入、语音转文本、文本转语音等多种模型类型
- 可配置、更新和在聊天机器人、Agent、工作流中使用
- 支持预定义模型和自定义模型两种类型

**典型示例**：
- OpenAI 插件（支持 GPT-4、GPT-4o、Whisper、TTS 等）
- Anthropic 插件（支持 Claude 系列模型）
- Bedrock/SageMaker 模型提供商

### 2. Tool Plugin（工具插件）

**功能**：为 Dify 应用添加专业能力

**特点**：
- 可被 Chatflow/Workflow/Agent 类型应用调用
- 提供完整的第三方服务 API 实现能力
- 支持在线搜索、图像生成、自定义集成等

**典型应用场景**：
- 数据分析工具
- 内容翻译服务
- 自定义业务集成
- 外部 API 调用

### 3. Agent Strategy Plugin（Agent 策略插件）

**功能**：为 Agent 节点提供推理策略

**特点**：
- 支持自主工具选择和执行
- 实现多步推理能力
- 可用于 Chatflow 和 Workflow 中的 Agent 节点

### 4. Extension Plugin（扩展插件）

**功能**：将业务逻辑封装为插件并提供 API 端点

**特点**：
- 相当于托管在 Dify 平台内的 API 服务
- 类似于在 Dify 内运行 HTTP 服务器
- 当用户激活 Endpoint 时，Dify 生成随机 URL
- 行为类似 Serverless 函数

**应用场景**：
- 自定义 Web 界面
- OpenAI 兼容 API
- 异步事件触发器
- 自定义业务逻辑封装

### 5. Bundle（插件包）

**功能**：将多个插件打包成一个包，实现批量安装

**三种类型**：

1. **Marketplace 类型**
   - 存储插件 ID 和版本信息
   - 导入时通过 Dify Marketplace 下载特定插件包

2. **GitHub 类型**
   - 存储 GitHub 仓库地址、版本号和资源文件名
   - 导入时从 GitHub 仓库下载插件包

3. **Package 类型**
   - 插件包直接存储在 Bundle 中
   - 不存储引用源，但可能导致 Bundle 包体积较大

---

## 开发环境搭建

### 前置要求

- **Python 版本**：3.11 或更高版本（推荐 3.12+）
- **操作系统**：macOS、Linux（Windows 需要额外适配）
- **依赖管理工具**：uv（需要手动安装）

### 安装 Dify CLI 工具

#### 方法 1：使用 Homebrew（macOS）

```bash
brew tap langgenius/dify
brew install dify
```

#### 方法 2：手动下载

1. 访问 [Dify Plugin CLI Releases](https://github.com/langgenius/dify-plugin-daemon/releases)
2. 下载适合您操作系统的版本
3. 对于 macOS M 系列芯片，下载 `dify-plugin-darwin-arm64`
4. 授予执行权限：

```bash
chmod +x dify-plugin-darwin-arm64
mv dify-plugin-darwin-arm64 /usr/local/bin/dify
```

### 验证安装

```bash
dify version
```

### 安装 uv 依赖管理工具

Dify daemon 使用 uv 管理插件依赖：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 安装 Python SDK

```bash
pip install dify_plugin
```

或使用 uv：

```bash
uv pip install dify_plugin
```

---

## 插件开发流程

### 步骤 1：初始化插件项目

```bash
dify plugin init
```

交互式提示：
- **开发语言**：选择 `python`
- **插件类型**：选择 `tool`、`model`、`extension` 或 `bundle`
- **插件名称**：输入您的插件名称

成功后将生成插件项目结构。

### 步骤 2：项目结构

典型的工具插件项目结构：

```
my-plugin/
├── manifest.yaml           # 插件清单文件
├── _assets/               # 资源文件（图标等）
│   └── icon.svg
├── provider/              # 提供商配置
│   └── my_provider.yaml
├── tools/                 # 工具定义
│   ├── tool1.yaml
│   └── tool1.py
├── main.py               # 入口文件
├── requirements.txt      # Python 依赖
└── .env.example         # 环境变量示例
```

### 步骤 3：配置插件清单（manifest.yaml）

```yaml
version: 0.0.1
type: "plugin"
author: "Your Name"
name: "my_plugin"
label:
  en_US: "My Plugin"
  zh_Hans: "我的插件"
created_at: "2025-01-15T00:00:00Z"
icon: "icon.svg"

# 资源限制
resource:
  memory: 1048576  # 1MB

# 权限配置
permission:
  tool:
    enabled: true
  model:
    enabled: false
  endpoint:
    enabled: false
  app:
    enabled: true
  storage:
    enabled: true
    size: 1048576

# 插件扩展列表
plugins:
  tools:
    - "provider/my_provider.yaml"

# 元数据
meta:
  version: 0.0.1
  arch:
    - "amd64"
    - "arm64"

# 运行时配置
runner:
  language: "python"
  version: "3.11"
  entrypoint: "main"

# 隐私政策（可选）
privacy: "./privacy.md"
```

### 步骤 4：开发插件核心逻辑

#### 工具插件示例（Google Search）

**provider/google.yaml**：

```yaml
identity:
  name: google
  author: Dify
  label:
    en_US: Google
    zh_Hans: 谷歌
  description:
    en_US: Google Search
    zh_Hans: 谷歌搜索
  icon: icon.svg

# 凭据配置
credentials_for_provider:
  api_key:
    type: secret-input
    required: true
    label:
      en_US: API Key
      zh_Hans: API 密钥
    placeholder:
      en_US: Please input your API Key
      zh_Hans: 请输入您的 API 密钥
```

**tools/google_search.yaml**：

```yaml
identity:
  name: google_search
  author: Dify
  label:
    en_US: Google Search
    zh_Hans: 谷歌搜索

parameters:
  - name: query
    type: string
    required: true
    label:
      en_US: Search Query
      zh_Hans: 搜索查询
    human_description:
      en_US: The search query string
      zh_Hans: 搜索查询字符串

  - name: result_type
    type: select
    required: false
    options:
      - value: text
        label:
          en_US: Text
          zh_Hans: 文本
      - value: link
        label:
          en_US: Link
          zh_Hans: 链接
    default: text
```

**tools/google_search.py**：

```python
from dify_plugin import Tool
from typing import Any, Generator

class GoogleSearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[str, None, None]:
        """
        工具调用方法
        """
        query = tool_parameters.get('query', '')
        result_type = tool_parameters.get('result_type', 'text')

        # 获取凭据
        api_key = self.runtime.credentials.get('api_key')

        # 实现搜索逻辑
        results = self._perform_search(query, api_key)

        # 返回结果
        if result_type == 'text':
            yield self.create_text_message(text=results)
        else:
            yield self.create_link_message(link=results)

    def _perform_search(self, query: str, api_key: str) -> str:
        # 实际搜索实现
        pass
```

#### 模型插件示例（Anthropic）

**providers/anthropic.py**：

```python
from dify_plugin.provider_kits import ModelProvider
from typing import Any

class AnthropicProvider(ModelProvider):
    def validate_provider_credentials(self, credentials: dict[str, Any]) -> None:
        """
        验证提供商凭据
        """
        api_key = credentials.get('api_key')

        if not api_key:
            raise ValueError('API Key is required')

        # 执行验证逻辑
        self._test_credentials(api_key)

    def _test_credentials(self, api_key: str) -> None:
        # 测试 API Key 是否有效
        pass
```

**models/llm/claude-3-opus.yaml**：

```yaml
model: claude-3-opus-20240229
label:
  en_US: Claude 3 Opus
model_type: llm
features:
  - agent-thought
  - vision
model_properties:
  mode: chat
  context_size: 200000
parameter_rules:
  - name: temperature
    use_template: temperature
  - name: top_p
    use_template: top_p
  - name: max_tokens
    use_template: max_tokens
    default: 4096
    min: 1
    max: 4096
pricing:
  input: '15'
  output: '75'
  unit: '0.000001'
  currency: USD
```

**models/llm/llm.py**：

```python
from dify_plugin.provider_kits.llm import LargeLanguageModel
from typing import Any, Generator

class ClaudeModel(LargeLanguageModel):
    def _invoke(
        self,
        model: str,
        credentials: dict[str, Any],
        prompt_messages: list,
        model_parameters: dict[str, Any],
        tools: list | None = None,
        stop: list[str] | None = None,
        stream: bool = True,
        user: str | None = None
    ) -> Generator:
        """
        调用 LLM 模型
        """
        # 实现模型调用逻辑
        pass

    def validate_credentials(
        self,
        model: str,
        credentials: dict[str, Any]
    ) -> None:
        """
        验证模型凭据
        """
        pass
```

#### Extension 插件示例

**main.py**：

```python
from dify_plugin import Endpoint
from flask import request, jsonify

class CustomEndpoint(Endpoint):
    def _invoke(self):
        """
        处理 HTTP 请求
        """
        # 获取请求数据
        data = request.get_json()

        # 处理业务逻辑
        result = self.process_data(data)

        # 返回响应
        return jsonify(result)

    def process_data(self, data):
        # 自定义业务逻辑
        return {"status": "success", "data": data}
```

### 步骤 5：本地调试

#### 配置调试环境

1. 复制 `.env.example` 为 `.env`
2. 填写远程服务器地址和调试密钥

**.env**：

```
DIFY_REMOTE_URL=https://your-dify-instance.com
DIFY_DEBUG_KEY=your-debug-key
```

#### 获取调试密钥

1. 登录 Dify 控制台
2. 进入"插件"页面
3. 点击"远程调试"
4. 复制调试密钥和远程 URL

#### 启动调试

```bash
dify plugin run
```

这将：
- 建立与 Dify 实例的长连接
- 将用户请求转发到本地插件
- 支持实时代码修改（所见即所得）
- 支持 IDE 断点调试

### 步骤 6：打包插件

完成开发后，打包插件：

```bash
cd /path/to/parent/directory
dify plugin package ./my-plugin
```

生成的文件：
- **工具/模型/Extension 插件**：`my-plugin.difypkg`
- **Bundle 插件**：`bundle.difybndl`

### 步骤 7：发布插件

#### 发布到 Dify Marketplace

1. 登录 Dify 控制台
2. 进入"插件"页面
3. 点击"上传插件"
4. 选择打包好的 `.difypkg` 或 `.difybndl` 文件
5. 填写插件描述、版本说明等信息
6. 提交审核

#### 发布到个人 GitHub 仓库

1. 创建 GitHub 仓库
2. 上传插件包到 Releases
3. 在 Dify 中添加 GitHub 插件源
4. 使用 URL 安装：`https://github.com/username/repo/releases/download/v1.0.0/plugin.difypkg`

---

## 配置文件格式

### Manifest.yaml 详解

#### 必填字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `version` | string | 插件版本号，格式：major.minor.patch |
| `type` | string | 插件类型，当前仅支持 "plugin" |
| `author` | string | 插件作者 |
| `name` | string | 插件名称（唯一标识符） |
| `label` | object | 多语言显示名称 |
| `created_at` | string | 创建时间（ISO 8601 格式） |
| `icon` | string | 图标文件路径 |

#### 权限配置（permission）

```yaml
permission:
  tool:
    enabled: true           # 是否启用工具功能
  model:
    enabled: true           # 是否启用模型功能
    llm: true              # 是否支持 LLM
    text_embedding: false  # 是否支持文本嵌入
    rerank: false          # 是否支持重排序
    tts: false             # 是否支持 TTS
    speech2text: false     # 是否支持语音转文本
    moderation: false      # 是否支持内容审核
  endpoint:
    enabled: true          # 是否启用端点
  app:
    enabled: true          # 是否启用应用集成
  storage:
    enabled: true          # 是否启用存储
    size: 1048576         # 存储大小限制（字节）
```

#### 资源限制（resource）

```yaml
resource:
  memory: 1048576  # 内存限制（字节）
  cpu: 1000        # CPU 限制（可选）
```

#### 插件扩展列表（plugins）

```yaml
plugins:
  tools:
    - "provider/google.yaml"
    - "provider/wikipedia.yaml"
  models:
    - "providers/openai.yaml"
  endpoints:
    - "provider/custom_api.yaml"
```

#### 运行时配置（runner）

```yaml
runner:
  language: "python"  # 编程语言
  version: "3.11"     # 语言版本
  entrypoint: "main"  # 入口文件（不含扩展名）
```

#### 元数据（meta）

```yaml
meta:
  version: 0.0.1           # SDK 版本
  minimum_dify_version: 1.7.1  # 最低 Dify 版本要求
  arch:
    - "amd64"
    - "arm64"
```

### 重要约束

1. **互斥性约束**：
   - 不允许同时扩展工具和模型
   - 不允许同时扩展模型和端点
   - 不允许没有任何扩展

2. **版本格式**：
   - 必须使用语义化版本号（major.minor.patch）
   - 错误格式会导致自动更新失败

3. **提供商限制**：
   - 当前每种扩展类型仅支持一个提供商

### Provider 配置文件

#### 工具提供商（provider/xxx.yaml）

```yaml
identity:
  name: my_tool_provider
  author: Your Name
  label:
    en_US: My Tool Provider
    zh_Hans: 我的工具提供商
  description:
    en_US: Description of the provider
    zh_Hans: 提供商描述
  icon: icon.svg

# 凭据配置（API Key 认证）
credentials_for_provider:
  api_key:
    type: secret-input
    required: true
    label:
      en_US: API Key
    placeholder:
      en_US: Please input your API Key

# OAuth 认证配置（可选）
oauth_schema:
  auth_url: https://oauth.example.com/authorize
  token_url: https://oauth.example.com/token
  scopes:
    - read
    - write
  client_id: ${CLIENT_ID}
  client_secret: ${CLIENT_SECRET}
```

#### 工具定义（tools/xxx.yaml）

```yaml
identity:
  name: my_tool
  author: Your Name
  label:
    en_US: My Tool
    zh_Hans: 我的工具

# 参数定义
parameters:
  - name: input_text
    type: string
    required: true
    label:
      en_US: Input Text
    human_description:
      en_US: The text to process
    llm_description: Text input for processing
    form: llm  # 表单类型：llm 或 form

  - name: option
    type: select
    required: false
    options:
      - value: option1
        label:
          en_US: Option 1
      - value: option2
        label:
          en_US: Option 2
    default: option1

  - name: number_param
    type: number
    required: false
    default: 10
    min: 1
    max: 100
```

### 通用数据结构

在插件开发中，有一些数据结构在工具、模型和端点之间通用。

#### I18nObject（国际化对象）

符合 IETF BCP 47 标准的国际化结构，支持四种语言：

| 字段 | 类型 | 说明 |
|------|------|------|
| `en_US` | string | 英语（美国）**必填** |
| `zh_Hans` | string | 简体中文 |
| `ja_JP` | string | 日语 |
| `pt_BR` | string | 葡萄牙语（巴西） |

**示例**：

```yaml
label:
  en_US: My Tool
  zh_Hans: 我的工具
  ja_JP: 私のツール
  pt_BR: Minha Ferramenta
```

#### ProviderConfig（提供商配置）

通用的提供商表单结构，适用于 Tool 和 Endpoint：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 表单项名称（变量名） |
| `label` | I18nObject | 是 | 显示标签 |
| `type` | ConfigType | 是 | 表单字段类型 |
| `scope` | string | 否 | 作用域，根据 type 值变化 |
| `required` | boolean | 否 | 是否必填 |
| `default` | any | 否 | 默认值（仅支持基本类型） |
| `options` | array | 否 | 选项列表（type 为 select 时使用） |
| `multiple` | boolean | 否 | 是否允许多选 |
| `help` | I18nObject | 否 | 帮助文本 |
| `url` | string | 否 | 帮助文档链接 |
| `placeholder` | I18nObject | 否 | 占位符文本 |

#### ConfigType（配置类型）

表单字段类型枚举：

| 类型 | 说明 |
|------|------|
| `secret-input` | 加密输入（如 API Key） |
| `text-input` | 纯文本输入 |
| `select` | 下拉选择 |
| `boolean` | 开关控件 |
| `model-selector` | 模型选择器 |
| `app-selector` | 应用选择器 |
| `array[tools]` | 工具列表选择器 |
| `any` | 任意类型 |

#### ConfigScope（配置作用域）

根据 `type` 的值，`scope` 有不同的可选值：

**当 type 为 `model-selector` 时**：

| 值 | 说明 |
|----|------|
| `llm` | 大语言模型 |
| `text-embedding` | 文本嵌入模型 |
| `rerank` | 重排序模型 |
| `tts` | 文本转语音模型 |
| `speech2text` | 语音转文本模型 |
| `moderation` | 内容审核模型 |
| `vision` | 视觉模型 |
| `document` | 文档处理模型 |
| `tool-call` | 支持工具调用的模型 |

**当 type 为 `app-selector` 时**：

| 值 | 说明 |
|----|------|
| `all` | 所有应用类型 |
| `chat` | 聊天应用 |
| `workflow` | 工作流应用 |
| `completion` | 补全应用 |

**当 type 为 `array[tools]` 时**：

| 值 | 说明 |
|----|------|
| `all` | 所有工具类型 |
| `plugin` | 插件工具 |
| `api` | API 工具 |
| `workflow` | 工作流工具 |

#### ConfigOption（配置选项）

用于 `select` 类型的选项定义：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `value` | string | 是 | 选项值 |
| `label` | I18nObject | 是 | 选项显示标签 |

**示例**：

```yaml
options:
  - value: option1
    label:
      en_US: Option 1
      zh_Hans: 选项一
  - value: option2
    label:
      en_US: Option 2
      zh_Hans: 选项二
```

#### ModelConfig（模型配置）

模型选择器返回的配置结构：

| 字段 | 类型 | 说明 |
|------|------|------|
| `provider` | string | 模型提供商（格式：`plugin_id/provider_name`） |
| `model` | string | 具体模型名称 |
| `model_type` | enum | 模型类型（llm, text-embedding 等） |

#### ToolSelector（工具选择器）

工具选择器返回的配置结构：

| 字段 | 类型 | 说明 |
|------|------|------|
| `provider_id` | string | 工具提供商名称 |
| `tool_name` | string | 工具名称 |
| `tool_description` | string | 工具描述 |
| `tool_configuration` | dict | 工具配置信息 |
| `tool_parameters` | dict | 需要 LLM 推理的参数 |

#### NodeResponse（节点响应）

工作流节点的响应结构：

| 字段 | 类型 | 说明 |
|------|------|------|
| `inputs` | dict | 最终输入到节点的变量 |
| `outputs` | dict | 节点的输出结果 |
| `process_data` | dict | 节点执行过程中产生的数据 |

---

## 认证和授权机制

### 1. API Key 认证

#### 配置方式

在 `provider.yaml` 中定义：

```yaml
credentials_for_provider:
  api_key:
    type: secret-input
    required: true
    label:
      en_US: API Key
      zh_Hans: API 密钥
    placeholder:
      en_US: Please input your API Key
      zh_Hans: 请输入您的 API 密钥
```

#### 代码中使用

```python
from dify_plugin import Tool

class MyTool(Tool):
    def _invoke(self, tool_parameters):
        # 获取 API Key
        api_key = self.runtime.credentials.get('api_key')

        # 使用 API Key 调用外部服务
        result = self.call_external_api(api_key, tool_parameters)

        return result
```

### 2. OAuth 2.0 认证

Dify v1.7.0+ 支持 OAuth 2.0 认证，无需手动管理 API 密钥。

#### 前置要求

在 `manifest.yaml` 中设置最低版本：

```yaml
meta:
  minimum_dify_version: 1.7.1
```

#### OAuth Schema 配置

```yaml
oauth_schema:
  # 授权 URL
  auth_url: https://oauth.example.com/authorize

  # 令牌 URL
  token_url: https://oauth.example.com/token

  # 权限范围
  scopes:
    - read
    - write
    - user_info

  # 客户端 ID（通常从环境变量获取）
  client_id: ${OAUTH_CLIENT_ID}

  # 客户端密钥
  client_secret: ${OAUTH_CLIENT_SECRET}

  # 重定向 URI 模板（Dify 自动生成）
  # 格式：https://{your-dify-domain}/console/api/oauth/plugin/{plugin-id}/{provider-name}/{tool-name}/callback
```

#### 支持双认证模式

同时支持 OAuth 和 API Key：

```yaml
# 既定义 oauth_schema 也定义 credentials_for_provider
oauth_schema:
  # OAuth 配置...

credentials_for_provider:
  api_key:
    # API Key 配置...
```

#### 代码中区分认证类型

```python
from dify_plugin import Tool

class MyTool(Tool):
    def _invoke(self, tool_parameters):
        # 检查认证类型
        auth_type = self.runtime.credential_type

        if auth_type == 'oauth':
            # OAuth 认证
            access_token = self.runtime.credentials.get('access_token')
            refresh_token = self.runtime.credentials.get('refresh_token')

            # Dify 自动处理 token 刷新
            result = self.call_api_with_oauth(access_token)

        elif auth_type == 'api_key':
            # API Key 认证
            api_key = self.runtime.credentials.get('api_key')
            result = self.call_api_with_key(api_key)

        return result
```

#### OAuth 特性

1. **自动刷新令牌**：Dify 自动处理访问令牌刷新
2. **安全存储**：令牌安全存储，不暴露给用户
3. **长期会话**：支持刷新令牌维持长期认证会话

#### Redirect URI 格式

- **自托管 Dify**：`https://{your-dify-domain}/console/api/oauth/plugin/{plugin-id}/{provider-name}/{tool-name}/callback`
- **SaaS Dify**：由平台自动配置

注意：`your-dify-domain` 应与 `CONSOLE_WEB_URL` 环境变量一致。

### 3. 自定义认证

对于 Extension 插件，可以实现自定义认证逻辑：

```python
from dify_plugin import Endpoint
from flask import request, jsonify

class CustomEndpoint(Endpoint):
    def _invoke(self):
        # 获取请求头中的认证信息
        auth_header = request.headers.get('Authorization')

        # 验证认证
        if not self.validate_auth(auth_header):
            return jsonify({"error": "Unauthorized"}), 401

        # 处理请求
        return jsonify({"status": "success"})

    def validate_auth(self, auth_header):
        # 自定义验证逻辑
        return auth_header == "Bearer valid-token"
```

---

## 部署方式

### 1. 本地部署

**适用场景**：
- 小团队和个人开发者
- 部署需求较低
- 注重高可用性而非大规模使用

**特点**：
- **一键部署**：强调开箱即用
- **子进程运行**：插件作为守护进程的子进程运行
- **管道通信**：通过 STDIN/STDOUT 与主进程通信
- **生命周期管理**：守护进程控制插件的启动、停止和依赖安装

**部署步骤**：

1. 安装 Dify 和插件守护进程：
   ```bash
   docker-compose up -d
   ```

2. 上传插件包到 Dify 实例

3. 在 Dify 控制台安装插件

4. 插件自动作为子进程启动

### 2. 远程/调试运行时

**适用场景**：
- 开发和调试阶段
- 需要本地 IDE 支持
- 连接到远程 Dify 实例进行测试

**特点**：
- **TCP 通信**：基于 TCP 的全双工通信
- **端口监听**：守护进程监听端口等待插件连接
- **IDE 集成**：支持主流 IDE（VS Code、PyCharm 等）
- **实时调试**：代码修改即时生效，无需重新安装

**部署步骤**：

1. 获取调试密钥：
   - 登录 Dify 控制台
   - 进入"插件"页面
   - 点击"远程调试"
   - 复制调试密钥和远程 URL

2. 配置本地环境（`.env`）：
   ```
   DIFY_REMOTE_URL=https://your-dify-instance.com
   DIFY_DEBUG_KEY=your-debug-key-here
   ```

3. 启动本地调试：
   ```bash
   dify plugin run
   ```

4. 在 Dify 中使用插件，请求会转发到本地

### 3. Serverless 运行时

**适用场景**：
- SaaS 版本
- 大规模用户
- 需要弹性扩展

**特点**：
- **弹性扩展**：根据使用情况自动扩展
- **高并发**：支持大规模并发请求
- **资源优化**：按需分配资源，提高利用率
- **高可用性**：多区域部署，故障自动转移

**技术架构**：
- **AWS Lambda**：主要 Serverless 解决方案
- **HTTP 协议**：通过 HTTP 调用插件
- **打包部署**：插件打包到 Lambda 函数

**部署步骤**：

1. 打包插件为 Serverless 格式：
   ```bash
   dify plugin package --serverless ./my-plugin
   ```

2. 上传到 AWS Lambda：
   ```bash
   aws lambda create-function \
     --function-name my-dify-plugin \
     --runtime python3.11 \
     --handler main.handler \
     --zip-file fileb://my-plugin.zip
   ```

3. 配置 API Gateway 触发器

4. 在 Dify 中配置 Serverless 端点

### 4. 企业版部署

**适用场景**：
- 企业私有化部署
- 高度可控性要求
- 严格的隐私保护需求

**特点**：
- **私有部署**：完全部署在企业内部
- **高可控性**：企业完全控制插件运行环境
- **数据隐私**：数据不离开企业网络
- **混合架构**：结合本地和 Serverless 优势

**部署架构**：
- 类似 SaaS 版本，但部署在企业内部
- 可使用企业自有的 Kubernetes 集群
- 支持自定义资源限制和安全策略

### 5. 混合部署

**推荐架构**：

```
┌─────────────────────────────────────────┐
│           Dify 主应用                    │
└─────────────────┬───────────────────────┘
                  │
        ┌─────────┴──────────┐
        │                    │
        ▼                    ▼
┌───────────────┐    ┌──────────────────┐
│   本地插件    │    │  Serverless 插件  │
│   (开发/测试) │    │   (生产环境)      │
└───────────────┘    └──────────────────┘
```

**优势**：
- 开发时使用本地/远程调试
- 生产环境使用 Serverless 自动扩展
- 关键插件可本地部署确保可控性

### 部署对比表

| 特性 | 本地部署 | 远程调试 | Serverless | 企业版 |
|------|---------|---------|-----------|--------|
| 易用性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| 扩展性 | ⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 调试便利性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ |
| 成本 | 低 | 低 | 按使用付费 | 高 |
| 适用场景 | 小团队 | 开发调试 | 大规模生产 | 企业私有化 |

---

## 调试和测试

### 1. 远程调试

Dify 提供了强大的远程调试功能，满足"所见即所得"和"本地调试"两大需求。

#### 配置远程调试

**步骤 1：获取调试凭据**

1. 登录 Dify 控制台
2. 导航至"插件"页面
3. 点击"远程调试"按钮
4. 复制显示的：
   - 远程服务器地址
   - 调试密钥

**步骤 2：配置本地环境**

复制 `.env.example` 为 `.env` 并填写：

```
DIFY_REMOTE_URL=https://cloud.dify.ai
DIFY_DEBUG_KEY=sk-xxxxxxxxxxxxxxxxxxxxxx
```

**步骤 3：启动调试会话**

```bash
dify plugin run
```

输出示例：
```
✓ Connected to Dify remote debugging server
✓ Plugin registered: my_plugin
✓ Waiting for requests...
```

#### 调试特性

1. **实时代码修改**：修改代码后无需重启，立即生效
2. **断点调试**：支持 IDE 断点调试（VS Code、PyCharm）
3. **长连接**：建立持久 TCP 连接，请求实时转发
4. **日志输出**：实时查看插件日志

#### IDE 集成

**VS Code 配置（launch.json）**：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Dify Plugin",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/main.py",
      "console": "integratedTerminal",
      "env": {
        "DIFY_REMOTE_URL": "https://cloud.dify.ai",
        "DIFY_DEBUG_KEY": "your-debug-key"
      }
    }
  ]
}
```

**PyCharm 配置**：

1. Run → Edit Configurations
2. 添加新的 Python 配置
3. Script path: `main.py`
4. Environment variables: 添加 `DIFY_REMOTE_URL` 和 `DIFY_DEBUG_KEY`
5. 设置断点并启动调试

### 2. 日志输出

#### 使用内置日志功能

```python
from dify_plugin import Tool

class MyTool(Tool):
    def _invoke(self, tool_parameters):
        # 输出调试日志
        self.logger.debug("Debug message")

        # 输出信息日志
        self.logger.info(f"Processing: {tool_parameters}")

        # 输出警告日志
        self.logger.warning("Warning message")

        # 输出错误日志
        self.logger.error("Error message")

        return result
```

#### 日志级别

- **DEBUG**：详细的调试信息
- **INFO**：一般信息
- **WARNING**：警告信息
- **ERROR**：错误信息
- **CRITICAL**：严重错误

#### 查看日志

**远程调试模式**：日志实时输出到终端

**生产环境**：在 Dify 控制台查看插件日志

### 3. 单元测试

#### 测试工具类插件

```python
import unittest
from tools.my_tool import MyTool

class TestMyTool(unittest.TestCase):
    def setUp(self):
        # 模拟运行时环境
        self.tool = MyTool()
        self.tool.runtime = MockRuntime()

    def test_basic_invoke(self):
        # 测试基本调用
        parameters = {"query": "test"}
        result = self.tool._invoke(parameters)

        self.assertIsNotNone(result)
        self.assertIn("data", result)

    def test_with_credentials(self):
        # 测试带凭据的调用
        self.tool.runtime.credentials = {"api_key": "test-key"}
        parameters = {"query": "test"}

        result = self.tool._invoke(parameters)
        self.assertTrue(result)

class MockRuntime:
    def __init__(self):
        self.credentials = {}
        self.credential_type = "api_key"

if __name__ == '__main__':
    unittest.run()
```

#### 运行测试

```bash
python -m unittest tests/test_my_tool.py
```

### 4. 工作流节点调试

Dify 1.5.0+ 提供了强大的工作流调试功能。

#### 单步运行

**特点**：
- 独立测试特定节点
- 无需执行整个工作流
- 验证新节点功能
- 排查单个节点错误

**使用方法**：
1. 在工作流画布中选择节点
2. 点击"单步运行"按钮
3. 提供测试输入
4. 查看节点输出

#### 逐步执行

**特点**：
- 按顺序执行节点
- 节点输出变量缓存到变量检查器
- 可编辑上游变量测试下游节点
- 实时查看所有变量内容

**使用方法**：
1. 点击工作流的"逐步执行"按钮
2. 执行每一步
3. 在变量检查器中查看和编辑变量
4. 继续下一步或重新执行

#### 变量检查器

**Dify 1.5.0 新特性**：

- **全局控制中心**：显示整个工作流的所有变量
- **实时跟踪**：实时显示变量内容
- **历史保存**：保存节点产生的内容
- **即时测试**：无需昂贵的重新运行即可测试单个步骤

### 5. 错误处理最佳实践

#### 定义错误处理

```python
from dify_plugin import Tool
from dify_plugin.exceptions import ToolException

class MyTool(Tool):
    def _invoke(self, tool_parameters):
        try:
            result = self.process(tool_parameters)
            return result

        except ValueError as e:
            # 抛出工具异常，提供明确的错误信息
            raise ToolException(f"Invalid parameter: {str(e)}")

        except ConnectionError as e:
            # 网络错误，可能需要重试
            raise ToolException(
                message=f"Connection failed: {str(e)}",
                retry=True  # 标记为可重试
            )
```

#### 配置节点重试

在 Dify 工作流中：
1. 选择节点
2. 启用"失败时重试"功能
3. 设置最大重试次数
4. 设置重试间隔

#### 预定义错误消息

在工具定义 YAML 中：

```yaml
error_messages:
  invalid_api_key:
    en_US: "The API key is invalid. Please check your credentials."
    zh_Hans: "API 密钥无效，请检查您的凭据。"
  rate_limit_exceeded:
    en_US: "Rate limit exceeded. Please try again later."
    zh_Hans: "超过速率限制，请稍后重试。"
```

### 6. 性能测试

#### 压力测试脚本

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

async def stress_test(tool, parameters, num_requests=100):
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(tool._invoke, parameters)
            for _ in range(num_requests)
        ]

        results = [f.result() for f in futures]

    end_time = time.time()

    print(f"Total requests: {num_requests}")
    print(f"Total time: {end_time - start_time:.2f}s")
    print(f"Average time per request: {(end_time - start_time) / num_requests:.3f}s")

    return results
```

---

## 数据传递方法

### 1. 工作流节点间数据传递

Dify 工作流通过变量系统实现节点间数据传递。

#### 基本变量传递

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│  Start   │─────▶│  Tool 1  │─────▶│  Tool 2  │
│  Node    │      │          │      │          │
└──────────┘      └──────────┘      └──────────┘
     │                 │                 │
     └─ query          └─ result_1       └─ final_result
```

**示例配置**：

**开始节点**：定义输入变量
```yaml
variables:
  - name: user_query
    type: string
    required: true
```

**工具 1 节点**：使用开始节点的变量
```yaml
inputs:
  query: "{{#start.user_query#}}"
```

**工具 2 节点**：使用工具 1 的输出
```yaml
inputs:
  previous_result: "{{#tool1.result#}}"
  original_query: "{{#start.user_query#}}"
```

#### 变量语法

- **引用变量**：`{{#node_name.variable_name#}}`
- **系统变量**：`{{#sys.user_id#}}`、`{{#sys.timestamp#}}`
- **环境变量**：`{{#env.API_KEY#}}`

### 2. Variable Assigner 节点

**用途**：重塑和重新分配变量，实现复杂数据转换

**示例**：

```yaml
# Variable Assigner 节点配置
assignments:
  - variable_name: formatted_data
    type: object
    value:
      title: "{{#tool1.title#}}"
      content: "{{#tool1.content#}}"
      metadata:
        source: "{{#tool1.source#}}"
        timestamp: "{{#sys.timestamp#}}"
```

**代码中访问**：

```python
from dify_plugin import Tool

class ProcessDataTool(Tool):
    def _invoke(self, tool_parameters):
        # 获取上游节点传递的数据
        formatted_data = tool_parameters.get('formatted_data', {})

        title = formatted_data.get('title')
        content = formatted_data.get('content')

        # 处理数据
        result = self.process(title, content)

        # 返回结果供下游节点使用
        return {
            "processed_title": result.title,
            "processed_content": result.content
        }
```

### 3. Template 节点

**用途**：使用模板语法转换数据格式

**示例**：

```jinja2
# Template 节点内容
{
  "summary": "{{#llm.response#}}",
  "keywords": [
    {% for keyword in tool1.keywords %}
    "{{ keyword }}"{% if not loop.last %},{% endif %}
    {% endfor %}
  ],
  "metadata": {
    "user": "{{#sys.user_id#}}",
    "timestamp": "{{#sys.timestamp#}}"
  }
}
```

### 4. 插件间数据传递的挑战与解决方案

#### 问题：插件无法直接访问工作流起始节点参数

**当前限制**：
- 插件难以直接获取工作流起始节点定义的用户参数
- 参数需要显式传递到插件节点

**解决方案 1：显式参数传递**

在工作流中连接节点时，显式传递参数：

```yaml
# 插件节点配置
inputs:
  user_defined_param: "{{#start.user_defined_param#}}"
```

**解决方案 2：事件订阅（社区建议）**

插件订阅工作流初始化事件：

```python
from dify_plugin import Extension

class MyExtension(Extension):
    def __init__(self):
        super().__init__()
        # 订阅工作流初始化事件
        self.subscribe('workflow.initialized', self.on_workflow_init)

    def on_workflow_init(self, event):
        # 获取工作流起始参数
        start_params = event.get('start_node_params', {})
        self.user_params = start_params

    def _invoke(self):
        # 使用获取到的参数
        param_value = self.user_params.get('param_name')
        return self.process(param_value)
```

注意：这是社区建议的方法，可能需要 Dify 未来版本支持。

### 5. 插件内部数据传递

#### 在工具类中共享数据

```python
from dify_plugin import Tool

class DataProcessingTool(Tool):
    def __init__(self):
        super().__init__()
        # 初始化共享数据存储
        self.cache = {}

    def _invoke(self, tool_parameters):
        step = tool_parameters.get('step')

        if step == 'fetch':
            # 第一步：获取数据
            data = self.fetch_data()
            self.cache['fetched_data'] = data
            return {"status": "fetched", "count": len(data)}

        elif step == 'process':
            # 第二步：处理数据
            data = self.cache.get('fetched_data', [])
            result = self.process_data(data)
            self.cache['processed_result'] = result
            return {"status": "processed", "result": result}

        elif step == 'finalize':
            # 第三步：完成处理
            result = self.cache.get('processed_result')
            final = self.finalize(result)
            return {"status": "completed", "final": final}
```

#### 使用存储 API

Dify 插件提供存储 API 用于持久化数据：

```python
from dify_plugin import Tool

class StatefulTool(Tool):
    def _invoke(self, tool_parameters):
        # 从存储读取数据
        previous_state = self.storage.get('state', {})

        # 更新状态
        new_state = self.update_state(previous_state, tool_parameters)

        # 保存到存储
        self.storage.set('state', new_state)

        return {"state": new_state}
```

### 6. Extension 插件的双向通信

Extension 插件支持与外部服务的双向通信。

#### Endpoint 接收外部数据

```python
from dify_plugin import Endpoint
from flask import request, jsonify

class WebhookEndpoint(Endpoint):
    def _invoke(self):
        # 接收外部 webhook 数据
        webhook_data = request.get_json()

        # 处理数据
        result = self.process_webhook(webhook_data)

        # 触发 Dify 工作流（可选）
        self.trigger_workflow('workflow_id', {
            'webhook_data': webhook_data,
            'processed_result': result
        })

        # 返回响应给外部服务
        return jsonify({"status": "received", "result": result})

    def trigger_workflow(self, workflow_id, inputs):
        # 调用 Dify API 触发工作流
        self.dify_client.workflows.run(
            workflow_id=workflow_id,
            inputs=inputs
        )
```

### 7. 跨插件数据共享

#### 使用工作流变量作为中介

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│ Plugin A │─────▶│ Variable │─────▶│ Plugin B │
│          │      │ Assigner │      │          │
└──────────┘      └──────────┘      └──────────┘
     │                 │                 │
     └─ output_a       └─ shared_data    └─ uses shared_data
```

**Plugin A 输出**：
```python
return {
    "data_for_b": processed_data,
    "metadata": metadata
}
```

**Variable Assigner 配置**：
```yaml
assignments:
  - variable_name: shared_data
    value:
      from_a: "{{#plugin_a.data_for_b#}}"
      metadata: "{{#plugin_a.metadata#}}"
```

**Plugin B 输入**：
```python
def _invoke(self, tool_parameters):
    shared_data = tool_parameters.get('shared_data', {})
    from_a = shared_data.get('from_a')

    # 使用 Plugin A 的数据
    result = self.process(from_a)
    return result
```

### 8. 最佳实践

1. **明确数据流**：设计清晰的数据流向，避免循环依赖
2. **使用类型化参数**：在 YAML 中明确定义参数类型
3. **验证输入**：始终验证接收到的参数
4. **错误处理**：处理缺失或无效的输入数据
5. **文档化接口**：清晰文档化插件的输入输出格式
6. **使用 Variable Assigner**：对于复杂数据转换，使用专门的节点
7. **避免过度耦合**：插件应独立工作，不依赖其他插件的内部实现

---

## 代码示例

### 示例 1：Google Search 工具插件

#### 文件结构

```
google_search/
├── manifest.yaml
├── _assets/
│   └── icon.svg
├── provider/
│   └── google.yaml
├── tools/
│   ├── google_search.yaml
│   └── google_search.py
├── main.py
└── requirements.txt
```

#### manifest.yaml

```yaml
version: 0.0.1
type: "plugin"
author: "Dify"
name: "google_search"
label:
  en_US: "Google Search"
  zh_Hans: "谷歌搜索"
created_at: "2025-01-15T00:00:00Z"
icon: "icon.svg"

resource:
  memory: 2097152  # 2MB

permission:
  tool:
    enabled: true
  model:
    enabled: false
  endpoint:
    enabled: false

plugins:
  tools:
    - "provider/google.yaml"

meta:
  version: 0.0.1
  arch:
    - "amd64"
    - "arm64"

runner:
  language: "python"
  version: "3.11"
  entrypoint: "main"
```

#### provider/google.yaml

```yaml
identity:
  name: google
  author: Dify
  label:
    en_US: Google
    zh_Hans: 谷歌
  description:
    en_US: Google Search Engine
    zh_Hans: 谷歌搜索引擎
  icon: icon.svg

credentials_for_provider:
  api_key:
    type: secret-input
    required: true
    label:
      en_US: API Key
      zh_Hans: API 密钥
    placeholder:
      en_US: Please input your Google API Key
      zh_Hans: 请输入您的 Google API 密钥

  search_engine_id:
    type: text-input
    required: true
    label:
      en_US: Search Engine ID
      zh_Hans: 搜索引擎 ID
    placeholder:
      en_US: Custom Search Engine ID
      zh_Hans: 自定义搜索引擎 ID
```

#### tools/google_search.yaml

```yaml
identity:
  name: google_search
  author: Dify
  label:
    en_US: Google Search
    zh_Hans: 谷歌搜索
  icon: icon.svg

description:
  human:
    en_US: Search Google for relevant results
    zh_Hans: 在谷歌上搜索相关结果
  llm: A tool for searching Google to find relevant web results for a query

parameters:
  - name: query
    type: string
    required: true
    label:
      en_US: Search Query
      zh_Hans: 搜索查询
    human_description:
      en_US: The search query string
      zh_Hans: 搜索查询字符串
    llm_description: The query to search for on Google
    form: llm

  - name: num_results
    type: number
    required: false
    default: 10
    min: 1
    max: 50
    label:
      en_US: Number of Results
      zh_Hans: 结果数量
    human_description:
      en_US: Maximum number of search results to return
      zh_Hans: 返回的最大搜索结果数

  - name: result_type
    type: select
    required: false
    default: snippets
    options:
      - value: snippets
        label:
          en_US: Text Snippets
          zh_Hans: 文本摘要
      - value: links
        label:
          en_US: Links Only
          zh_Hans: 仅链接
      - value: full
        label:
          en_US: Full Results
          zh_Hans: 完整结果
    label:
      en_US: Result Type
      zh_Hans: 结果类型
```

#### tools/google_search.py

```python
from dify_plugin import Tool
from typing import Any, Generator
import requests
import json

class GoogleSearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[str, None, None]:
        """
        Execute Google Search
        """
        # 获取参数
        query = tool_parameters.get('query', '')
        num_results = tool_parameters.get('num_results', 10)
        result_type = tool_parameters.get('result_type', 'snippets')

        # 获取凭据
        api_key = self.runtime.credentials.get('api_key')
        search_engine_id = self.runtime.credentials.get('search_engine_id')

        # 验证参数
        if not query:
            yield self.create_text_message("Please provide a search query")
            return

        if not api_key or not search_engine_id:
            yield self.create_text_message("API credentials not configured")
            return

        try:
            # 执行搜索
            results = self._perform_search(
                query=query,
                api_key=api_key,
                search_engine_id=search_engine_id,
                num_results=num_results
            )

            # 格式化输出
            if result_type == 'snippets':
                output = self._format_snippets(results)
            elif result_type == 'links':
                output = self._format_links(results)
            else:
                output = self._format_full_results(results)

            # 返回结果
            yield self.create_text_message(text=output)

        except Exception as e:
            self.logger.error(f"Search failed: {str(e)}")
            yield self.create_text_message(f"Error: {str(e)}")

    def _perform_search(
        self,
        query: str,
        api_key: str,
        search_engine_id: str,
        num_results: int
    ) -> list:
        """
        Call Google Custom Search API
        """
        url = "https://www.googleapis.com/customsearch/v1"

        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': query,
            'num': min(num_results, 10)  # API 限制单次最多 10 条
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        data = response.json()
        return data.get('items', [])

    def _format_snippets(self, results: list) -> str:
        """
        Format results as text snippets
        """
        output = []
        for i, item in enumerate(results, 1):
            title = item.get('title', 'No title')
            snippet = item.get('snippet', 'No description')
            output.append(f"{i}. {title}\n   {snippet}")

        return "\n\n".join(output)

    def _format_links(self, results: list) -> str:
        """
        Format results as links only
        """
        links = [item.get('link', '') for item in results]
        return "\n".join(links)

    def _format_full_results(self, results: list) -> str:
        """
        Format full results with all details
        """
        output = []
        for i, item in enumerate(results, 1):
            title = item.get('title', 'No title')
            link = item.get('link', '')
            snippet = item.get('snippet', 'No description')

            result_text = f"{i}. {title}\n   URL: {link}\n   {snippet}"
            output.append(result_text)

        return "\n\n".join(output)
```

#### main.py

```python
from dify_plugin import Plugin
from tools.google_search import GoogleSearchTool

# 初始化插件
plugin = Plugin()

# 注册工具
plugin.register_tool('google_search', GoogleSearchTool)

# 启动插件
if __name__ == '__main__':
    plugin.run()
```

#### requirements.txt

```
dify_plugin>=0.0.1
requests>=2.31.0
```

---

### 示例 2：Anthropic 模型插件

#### 文件结构

```
anthropic_provider/
├── manifest.yaml
├── _assets/
│   └── icon.svg
├── providers/
│   └── anthropic.yaml
├── models/
│   └── llm/
│       ├── claude-3-opus.yaml
│       ├── claude-3-sonnet.yaml
│       └── llm.py
├── main.py
└── requirements.txt
```

#### manifest.yaml

```yaml
version: 0.0.1
type: "plugin"
author: "Dify"
name: "anthropic_provider"
label:
  en_US: "Anthropic"
  zh_Hans: "Anthropic"
created_at: "2025-01-15T00:00:00Z"
icon: "icon.svg"

resource:
  memory: 5242880  # 5MB

permission:
  tool:
    enabled: false
  model:
    enabled: true
    llm: true
    text_embedding: false

plugins:
  models:
    - "providers/anthropic.yaml"

meta:
  version: 0.0.1
  arch:
    - "amd64"
    - "arm64"

runner:
  language: "python"
  version: "3.11"
  entrypoint: "main"
```

#### providers/anthropic.yaml

```yaml
identity:
  name: anthropic
  author: Dify
  label:
    en_US: Anthropic
    zh_Hans: Anthropic
  description:
    en_US: Anthropic Claude Models
    zh_Hans: Anthropic Claude 模型
  icon: icon.svg

supported_model_types:
  - llm

credentials_for_provider:
  api_key:
    type: secret-input
    required: true
    label:
      en_US: API Key
      zh_Hans: API 密钥
    placeholder:
      en_US: Enter your Anthropic API key
      zh_Hans: 输入您的 Anthropic API 密钥
```

#### models/llm/claude-3-opus.yaml

```yaml
model: claude-3-opus-20240229
label:
  en_US: Claude 3 Opus
  zh_Hans: Claude 3 Opus
model_type: llm

features:
  - agent-thought
  - vision
  - stream-tool-call

model_properties:
  mode: chat
  context_size: 200000
  max_chunks: 1

parameter_rules:
  - name: temperature
    use_template: temperature
    default: 1
    min: 0
    max: 1

  - name: top_p
    use_template: top_p
    default: 1
    min: 0
    max: 1

  - name: top_k
    type: int
    default: 5
    min: 1
    max: 100
    label:
      en_US: Top K

  - name: max_tokens
    use_template: max_tokens
    default: 4096
    min: 1
    max: 4096

pricing:
  input: '15'
  output: '75'
  unit: '0.000001'
  currency: USD
```

#### models/llm/llm.py

```python
from dify_plugin.provider_kits.llm import LargeLanguageModel
from typing import Any, Generator, Optional
import anthropic
from anthropic.types import MessageStreamEvent

class AnthropicLLM(LargeLanguageModel):
    def _invoke(
        self,
        model: str,
        credentials: dict[str, Any],
        prompt_messages: list,
        model_parameters: dict[str, Any],
        tools: Optional[list] = None,
        stop: Optional[list[str]] = None,
        stream: bool = True,
        user: Optional[str] = None
    ) -> Generator:
        """
        Invoke Anthropic LLM
        """
        # 获取 API Key
        api_key = credentials.get('api_key')

        # 初始化客户端
        client = anthropic.Anthropic(api_key=api_key)

        # 转换消息格式
        messages = self._convert_messages(prompt_messages)

        # 提取系统消息
        system_message = self._extract_system_message(messages)

        # 构建请求参数
        params = {
            'model': model,
            'messages': messages,
            'max_tokens': model_parameters.get('max_tokens', 4096),
            'temperature': model_parameters.get('temperature', 1.0),
            'top_p': model_parameters.get('top_p', 1.0),
            'top_k': model_parameters.get('top_k', 5),
        }

        if system_message:
            params['system'] = system_message

        if stop:
            params['stop_sequences'] = stop

        if tools:
            params['tools'] = self._convert_tools(tools)

        # 流式或非流式调用
        if stream:
            return self._stream_invoke(client, params)
        else:
            return self._sync_invoke(client, params)

    def _stream_invoke(self, client, params) -> Generator:
        """
        Streaming invocation
        """
        with client.messages.stream(**params) as stream:
            for event in stream:
                if isinstance(event, MessageStreamEvent):
                    if event.type == 'content_block_delta':
                        delta = event.delta
                        if hasattr(delta, 'text'):
                            yield self.create_text_chunk(text=delta.text)

                    elif event.type == 'message_stop':
                        # 消息结束
                        usage = stream.current_message.usage
                        yield self.create_final_chunk(
                            prompt_tokens=usage.input_tokens,
                            completion_tokens=usage.output_tokens
                        )

    def _sync_invoke(self, client, params) -> Generator:
        """
        Synchronous invocation
        """
        response = client.messages.create(**params)

        # 提取文本内容
        text = ''.join([
            block.text for block in response.content
            if hasattr(block, 'text')
        ])

        yield self.create_text_message(
            text=text,
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens
        )

    def _convert_messages(self, prompt_messages: list) -> list:
        """
        Convert Dify message format to Anthropic format
        """
        messages = []
        for msg in prompt_messages:
            if msg['role'] == 'system':
                continue  # 系统消息单独处理

            messages.append({
                'role': msg['role'],
                'content': msg['content']
            })

        return messages

    def _extract_system_message(self, messages: list) -> Optional[str]:
        """
        Extract system message
        """
        for msg in messages:
            if msg.get('role') == 'system':
                return msg.get('content')
        return None

    def _convert_tools(self, tools: list) -> list:
        """
        Convert Dify tools to Anthropic format
        """
        anthropic_tools = []
        for tool in tools:
            anthropic_tools.append({
                'name': tool['name'],
                'description': tool['description'],
                'input_schema': tool['parameters']
            })
        return anthropic_tools

    def validate_credentials(self, model: str, credentials: dict[str, Any]) -> None:
        """
        Validate credentials
        """
        api_key = credentials.get('api_key')

        if not api_key:
            raise ValueError("API Key is required")

        # 测试 API Key
        try:
            client = anthropic.Anthropic(api_key=api_key)
            client.messages.create(
                model='claude-3-haiku-20240307',  # 使用最小模型测试
                max_tokens=10,
                messages=[{'role': 'user', 'content': 'Hi'}]
            )
        except Exception as e:
            raise ValueError(f"Invalid API Key: {str(e)}")
```

#### main.py

```python
from dify_plugin import Plugin
from models.llm.llm import AnthropicLLM

# 初始化插件
plugin = Plugin()

# 注册模型
plugin.register_model('anthropic', AnthropicLLM)

# 启动插件
if __name__ == '__main__':
    plugin.run()
```

#### requirements.txt

```
dify_plugin>=0.0.1
anthropic>=0.39.0
```

---

### 示例 3：Extension 插件 - Webhook 处理器

#### 文件结构

```
webhook_handler/
├── manifest.yaml
├── _assets/
│   └── icon.svg
├── provider/
│   └── webhook.yaml
├── endpoints/
│   └── webhook_receiver.py
├── main.py
└── requirements.txt
```

#### manifest.yaml

```yaml
version: 0.0.1
type: "plugin"
author: "YourName"
name: "webhook_handler"
label:
  en_US: "Webhook Handler"
  zh_Hans: "Webhook 处理器"
created_at: "2025-01-15T00:00:00Z"
icon: "icon.svg"

resource:
  memory: 2097152

permission:
  tool:
    enabled: false
  model:
    enabled: false
  endpoint:
    enabled: true
  app:
    enabled: true
  storage:
    enabled: true
    size: 10485760  # 10MB

plugins:
  endpoints:
    - "provider/webhook.yaml"

meta:
  version: 0.0.1
  arch:
    - "amd64"
    - "arm64"

runner:
  language: "python"
  version: "3.11"
  entrypoint: "main"
```

#### provider/webhook.yaml

```yaml
identity:
  name: webhook_handler
  author: YourName
  label:
    en_US: Webhook Handler
    zh_Hans: Webhook 处理器
  description:
    en_US: Receive and process webhooks from external services
    zh_Hans: 接收和处理来自外部服务的 webhook
  icon: icon.svg

settings:
  - name: secret_token
    type: secret-input
    required: true
    label:
      en_US: Secret Token
      zh_Hans: 密钥令牌
    description:
      en_US: Token for webhook authentication
      zh_Hans: 用于 webhook 认证的令牌
```

#### endpoints/webhook_receiver.py

```python
from dify_plugin import Endpoint
from flask import request, jsonify
import hmac
import hashlib
import json

class WebhookReceiver(Endpoint):
    def _invoke(self):
        """
        Handle incoming webhook requests
        """
        # 获取请求方法
        method = request.method

        if method == 'GET':
            # 健康检查
            return self._health_check()

        elif method == 'POST':
            # 处理 webhook 数据
            return self._handle_webhook()

        else:
            return jsonify({"error": "Method not allowed"}), 405

    def _health_check(self):
        """
        Health check endpoint
        """
        return jsonify({
            "status": "healthy",
            "service": "webhook_handler"
        })

    def _handle_webhook(self):
        """
        Process webhook payload
        """
        try:
            # 获取请求数据
            payload = request.get_json()

            # 验证签名
            if not self._verify_signature(request):
                self.logger.warning("Invalid webhook signature")
                return jsonify({"error": "Invalid signature"}), 401

            # 记录日志
            self.logger.info(f"Received webhook: {payload.get('event_type')}")

            # 处理不同类型的事件
            event_type = payload.get('event_type')

            if event_type == 'user.created':
                result = self._handle_user_created(payload)

            elif event_type == 'order.completed':
                result = self._handle_order_completed(payload)

            elif event_type == 'data.updated':
                result = self._handle_data_updated(payload)

            else:
                result = self._handle_generic_event(payload)

            # 存储事件到持久化存储
            self._store_event(payload)

            # 可选：触发 Dify 工作流
            if payload.get('trigger_workflow'):
                self._trigger_dify_workflow(payload)

            return jsonify({
                "status": "processed",
                "event_type": event_type,
                "result": result
            })

        except Exception as e:
            self.logger.error(f"Error processing webhook: {str(e)}")
            return jsonify({"error": str(e)}), 500

    def _verify_signature(self, request) -> bool:
        """
        Verify webhook signature for security
        """
        # 获取密钥
        secret_token = self.runtime.settings.get('secret_token', '')

        # 获取签名头
        signature_header = request.headers.get('X-Webhook-Signature', '')

        # 计算预期签名
        payload_bytes = request.get_data()
        expected_signature = hmac.new(
            secret_token.encode(),
            payload_bytes,
            hashlib.sha256
        ).hexdigest()

        # 比较签名
        return hmac.compare_digest(signature_header, expected_signature)

    def _handle_user_created(self, payload: dict) -> dict:
        """
        Handle user.created event
        """
        user_data = payload.get('data', {})
        user_id = user_data.get('id')
        user_email = user_data.get('email')

        self.logger.info(f"New user created: {user_id} ({user_email})")

        # 执行业务逻辑
        # 例如：发送欢迎邮件、创建用户配置等

        return {
            "action": "user_created",
            "user_id": user_id,
            "processed": True
        }

    def _handle_order_completed(self, payload: dict) -> dict:
        """
        Handle order.completed event
        """
        order_data = payload.get('data', {})
        order_id = order_data.get('id')
        amount = order_data.get('amount')

        self.logger.info(f"Order completed: {order_id}, Amount: {amount}")

        # 执行业务逻辑
        # 例如：更新库存、发送确认邮件等

        return {
            "action": "order_completed",
            "order_id": order_id,
            "processed": True
        }

    def _handle_data_updated(self, payload: dict) -> dict:
        """
        Handle data.updated event
        """
        data = payload.get('data', {})
        entity_type = data.get('entity_type')
        entity_id = data.get('entity_id')

        self.logger.info(f"Data updated: {entity_type}/{entity_id}")

        # 执行业务逻辑

        return {
            "action": "data_updated",
            "entity": f"{entity_type}/{entity_id}",
            "processed": True
        }

    def _handle_generic_event(self, payload: dict) -> dict:
        """
        Handle generic events
        """
        event_type = payload.get('event_type', 'unknown')

        self.logger.info(f"Generic event: {event_type}")

        return {
            "action": "generic_event",
            "event_type": event_type,
            "processed": True
        }

    def _store_event(self, payload: dict):
        """
        Store event to persistent storage
        """
        event_id = payload.get('id', 'unknown')

        # 使用插件存储 API
        events = self.storage.get('events', [])
        events.append({
            'id': event_id,
            'event_type': payload.get('event_type'),
            'timestamp': payload.get('timestamp'),
            'processed': True
        })

        # 限制存储的事件数量（保留最近 1000 条）
        if len(events) > 1000:
            events = events[-1000:]

        self.storage.set('events', events)

    def _trigger_dify_workflow(self, payload: dict):
        """
        Trigger Dify workflow based on webhook event
        """
        workflow_id = payload.get('workflow_id')

        if workflow_id:
            # 调用 Dify API 触发工作流
            # 注意：这需要 Dify API 客户端支持
            self.logger.info(f"Triggering workflow: {workflow_id}")

            # 示例代码（需要实际实现）
            # self.dify_client.workflows.run(
            #     workflow_id=workflow_id,
            #     inputs=payload.get('data', {})
            # )
```

#### main.py

```python
from dify_plugin import Plugin
from endpoints.webhook_receiver import WebhookReceiver

# 初始化插件
plugin = Plugin()

# 注册端点
plugin.register_endpoint('webhook', WebhookReceiver)

# 启动插件
if __name__ == '__main__':
    plugin.run()
```

#### requirements.txt

```
dify_plugin>=0.0.1
flask>=3.0.0
```

---

### 示例 4：Bundle 插件包

#### 创建 Bundle

```bash
# 创建 Bundle 目录
mkdir my_bundle
cd my_bundle

# 初始化 Bundle
dify plugin init --type bundle
```

#### bundle_manifest.yaml

```yaml
version: 1.0.0
type: "bundle"
name: "ai_toolkit"
author: "YourName"
label:
  en_US: "AI Toolkit Bundle"
  zh_Hans: "AI 工具包"
description:
  en_US: "A comprehensive bundle of AI tools and models"
  zh_Hans: "全面的 AI 工具和模型集合"
icon: "icon.svg"

# Marketplace 类型 Bundle
plugins:
  - id: "google_search"
    version: "0.0.1"
    source: "marketplace"

  - id: "anthropic_provider"
    version: "0.0.1"
    source: "marketplace"

  - id: "webhook_handler"
    version: "0.0.1"
    source: "marketplace"

# GitHub 类型 Bundle
# plugins:
#   - name: "custom_tool"
#     source: "github"
#     repository: "username/repo"
#     release: "v1.0.0"
#     asset: "custom_tool.difypkg"

# Package 类型 Bundle
# plugins:
#   - name: "embedded_plugin"
#     source: "package"
#     path: "./plugins/embedded_plugin.difypkg"
```

#### 打包 Bundle

```bash
# 打包 Bundle
dify plugin bundle package ./my_bundle

# 生成 my_bundle.difybndl 文件
```

---

## 资源链接

### 官方文档

- [Dify 插件开发文档（英文）](https://docs.dify.ai/plugin-dev-en/0111-getting-started-dify-plugin)
- [Dify 插件开发文档（中文）](https://docs.dify.ai/zh-hans/plugins/quick-start/develop-plugins)
- [Dify 插件介绍](https://docs.dify.ai/plugins/introduction)
- [Manifest 配置文档](https://docs.dify.ai/plugin-dev-en/0411-plugin-info-by-manifest)
- [Schema 文档](https://langgenius.github.io/dify-plugin-sdks/schema/)

### GitHub 仓库

- [Dify 主仓库](https://github.com/langgenius/dify)
- [Dify 插件示例](https://github.com/langgenius/dify-plugins)
- [Dify 官方插件](https://github.com/langgenius/dify-official-plugins)
- [Dify 插件 SDK](https://github.com/langgenius/dify-plugin-sdks)
- [Dify 插件守护进程](https://github.com/langgenius/dify-plugin-daemon)
- [AWS Dify 工具](https://github.com/aws-samples/dify-aws-tool)

### PyPI 包

- [dify_plugin](https://pypi.org/project/dify_plugin/)

### 博客文章

- [Introducing Dify Plugins](https://dify.ai/blog/introducing-dify-plugins)
- [Dify v1.0.0: Building a Vibrant Plugin Ecosystem](https://dify.ai/blog/dify-v1-0-building-a-vibrant-plugin-ecosystem)
- [Dify Plugin System: Design and Implementation](https://dify.ai/blog/dify-plugin-system-design-and-implementation)
- [Extension Plugin Endpoint: Bringing Serverless Flexibility to Dify](https://dify.ai/blog/extension-plugin-endpoint-bringing-serverless-flexibility-to-dify)
- [Add OAuth Support to Your Tool Plugin](https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-oauth)
- [Dify 1.5.0: Real-Time Workflow Debugging](https://dify.ai/blog/dify-1-5-0-real-time-workflow-debugging-that-actually-works)

### 工具和资源

- [Dify Plugin Development Cheatsheet](https://docs.dify.ai/plugin-dev-en/0131-cheatsheet)
- [Debug Plugin 文档](https://docs.dify.ai/en/plugins/quick-start/debug-plugin)
- [发布插件指南](https://docs.dify.ai/plugins/publish-plugins)
- [GitHub 个人仓库发布](https://docs.dify.ai/en/plugins/publish-plugins/publish-plugin-on-personal-github-repo)

### 社区资源

- [Dify Plugins GitHub Topic](https://github.com/topics/dify-plugins)
- [CSDN: Dify Tool 插件开发流程](https://blog.csdn.net/wjj_fire/article/details/147686814)
- [知乎: Dify v1.0.0 插件系统](https://zhuanlan.zhihu.com/p/27357379692)

---

## 总结

Dify 插件系统为开发者提供了强大而灵活的扩展能力：

1. **五种插件类型**满足不同场景需求
2. **标准化开发流程**降低学习成本
3. **多种部署方式**适应不同规模应用
4. **完善的调试工具**提升开发效率
5. **活跃的社区生态**提供丰富的示例和支持

通过本指南，您应该能够：
- 理解 Dify 插件系统的核心架构
- 搭建完整的开发环境
- 开发各类型的插件
- 掌握调试和部署技巧
- 实现插件间的数据传递

祝您开发愉快！

---

**文档版本**: 1.0.0
**最后更新**: 2025-01-15
**作者**: Based on official Dify documentation and community resources
