# 插件设计阶段

插件开发的设计阶段，包括需求分析、范围定义和计划制定。

## 何时使用此技能

- 开始一个新的插件项目
- 分析用户需求和功能范围
- 制定开发计划和任务分解
- 评估技术可行性

## 阶段 0: 预规划 🔍

### 0.1 确定插件类型

| 类型               | 用途                       | 使用场景                                           |
| ------------------ | --------------------------- | -------------------------------------------------- |
| **Tool**           | 为工作流添加能力             | 集成外部 API (搜索、数据库、SaaS)                   |
| **Trigger**        | 从事件启动工作流             | 接收 Webhooks (GitHub, Slack, 自定义)               |
| **Extension**      | 自定义 HTTP 端点             | 构建 API、OAuth 回调                                |
| **Model**          | 新的 AI 模型提供者           | 添加 LLM/embedding 提供者                           |
| **Datasource**     | 外部数据连接                 | 连接数据库、知识库                                  |
| **Agent Strategy** | 自定义 Agent 逻辑            | 实现专门的推理逻辑                                  |

### 0.2 研究目标 API

- 仔细阅读官方 API 文档
- 了解认证方式 (API Key / OAuth2)
- 注意 API 速率限制和限制条件
- 检查是否有沙箱/测试环境

### 0.3 查阅官方示例 (⭐ 关键步骤!)

**首先克隆/更新官方插件仓库：**

```bash
# 首次克隆
git clone https://github.com/langgenius/dify-official-plugins.git

# 每次开发前更新 (务必执行!)
cd dify-official-plugins && git pull
```

**然后查找类似插件：**

```bash
# 列出所有可用的 tool 插件
ls dify-official-plugins/tools/

# 查找类似功能:
# 金融类: stripe, plaid
# 搜索类: google, arxiv, wikipedia
# 社交类: slack, github
# OAuth: github, google, slack
```

**参考要点：**
- 在仓库中搜索类似集成
- 研究实现模式和代码结构
- 识别可复用的认证和错误处理模式
- 注意 manifest.yaml 和 provider 的配置模式

## 阶段 1: 需求分析 ✅

### 1.1 定义用户需求

回答以下问题：
- 这个插件解决什么问题？
- 它将启用什么工作流？
- 目标用户是谁？

### 1.2 明确集成目标

- 集成哪个服务？
- 需要哪些具体功能？
- 是单向还是双向集成？

### 1.3 确认认证方式

| 认证类型 | 适用场景 | 复杂度 |
|----------|----------|--------|
| API Key | 简单服务 | 低 |
| API Token | 企业服务 | 中 |
| OAuth 2.0 | 用户授权 | 高 |

### 1.4 确认数据流向

- [ ] 只读查询？
- [ ] 写操作？
- [ ] 事件驱动触发器？
- [ ] 双向同步？

## 阶段 2: 范围定义 📋

### 2.1 列出所有工具

为 MVP 定义 3-7 个工具，清晰命名：

```yaml
# 示例：Mercury 银行集成
tools:
  - get_accounts      # 获取账户列表
  - get_account       # 获取账户详情
  - get_transactions  # 获取交易记录
  - create_payment    # 创建付款 (可选)
```

### 2.2 设置优先级

| 优先级 | 标签 | 说明 |
|--------|------|------|
| P0 | 必须有 | MVP 必需 |
| P1 | 应该有 | 重要但可延后 |
| P2 | 可以有 | 锦上添花 |

### 2.3 映射依赖关系

```
get_accounts ─────┐
                  ├──> get_transactions (需要 account_id)
get_account ──────┘
                  
create_token ────> create_charge (需要 token)
```

### 2.4 评估复杂度

| 复杂度 | 特征 | 预估时间 |
|--------|------|----------|
| 简单 | 单个 API 调用，基础参数 | 1-2 小时 |
| 中等 | 多次调用，数据转换 | 2-4 小时 |
| 复杂 | OAuth 流程，Webhook 验证，状态管理 | 4-8 小时 |

### 2.5 记录限制条件

```yaml
limitations:
  rate_limits: "100 requests/minute"
  geographic: "仅限美国"
  environment: "沙箱不支持 Webhooks"
  authentication: "OAuth 需要 HTTPS 回调 URL"
```

## 阶段 3: 计划与确认 📝

### 3.1 创建任务列表

使用 `TodoWrite` 工具跟踪进度，分解为具体任务：

```
[ ] 1. 创建插件骨架结构
[ ] 2. 实现 Provider (认证)
[ ] 3. 实现 get_accounts 工具
[ ] 4. 实现 get_transactions 工具
[ ] 5. 本地测试
[ ] 6. 打包发布
```

### 3.2 记录关键文件

```
my_plugin/
├── manifest.yaml       # 插件元数据
├── main.py             # 入口点
├── requirements.txt    # 依赖
├── provider/
│   ├── provider.yaml   # 认证配置
│   └── provider.py     # OAuth/验证逻辑
└── tools/
    ├── get_accounts.yaml  # 工具定义
    └── get_accounts.py    # 工具实现
```

### 3.3 识别风险

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| 复杂 OAuth 流程 | 高 | 参考官方示例 |
| 未文档化的 API 行为 | 中 | 编写诊断脚本 |
| 缺少测试环境 | 中 | 小心测试生产环境 |

### 3.4 获取用户确认

开始开发前，向用户展示：
- 功能范围
- 任务列表
- 时间估算
- 潜在风险

使用 `AskUserQuestion` 确认后再继续。

## 设计文档模板

```markdown
# [插件名称] 设计文档

## 概述
简要描述插件用途和目标。

## 功能需求
1. 功能 A - 描述
2. 功能 B - 描述

## 技术方案
- 插件类型: Tool / Trigger / Extension
- 认证方式: API Key / OAuth 2.0
- 目标 API: [API 文档链接]

## 工具列表
| 工具名称 | 功能 | 优先级 |
|----------|------|--------|
| get_xxx | 获取 xxx | P0 |
| create_xxx | 创建 xxx | P1 |

## 依赖关系
[依赖关系图]

## 风险评估
| 风险 | 影响 | 缓解措施 |
|------|------|----------|

## 时间估算
- 阶段 1: X 小时
- 阶段 2: X 小时
- 总计: X 小时
```

## 相关技能

- **02-api-reference**: API 文档收集
- **03-development**: 开发实现
- **04-testing**: 测试验证
- **05-packaging**: 打包发布

## 参考资料

- `dify-plugin` skill: 完整的 Dify 插件开发指南
- `archive/solution-design.md`: 现有解决方案设计文档
