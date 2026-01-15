# CLAUDE.md

本文件为 Claude 提供 Dify 插件开发的上下文和参考指南。

## 项目概述

Mercury Plugin 是一个 Dify Trigger 插件项目，用于实现 Mercury 银行与 QuickBooks 的实时交易同步。

## Workspace 参考仓库

本 workspace 包含多个关联仓库，在开发插件时应参考：

### 1. 插件运行时 (dify-plugin-daemon)

**路径**: `/Users/petrus/Source/dify/ee/dify-plugin-daemon`

**用途**: 了解插件如何被执行和管理

**关键目录**:
- `cmd/commandline/plugin/templates/` - 插件模板文件
- `pkg/entities/plugin_entities/` - 插件实体定义（Go）
- `internal/core/plugin_manager/` - 插件管理器实现
- `internal/core/local_runtime/` - 本地运行时实现

**参考场景**:
- 理解插件生命周期
- 了解插件与 Dify 的通信协议
- 排查插件运行时问题

### 2. 官方插件示例 (dify-official-plugins)

**路径**: `/Users/petrus/Source/dify/ee/dify-official-plugins`

**用途**: 参考官方插件的实现模式和最佳实践

**关键目录**:
- `tools/` - 工具插件示例（如 Google、GitHub、Slack 等）
- `triggers/` - Trigger 插件示例 ⚠️ 重点参考
- `models/` - 模型插件示例
- `extensions/` - 扩展插件示例

**参考场景**:
- 实现新功能时先查找类似的官方插件
- 学习 YAML 配置文件的标准写法
- 参考 Python 代码结构和最佳实践

### 3. Dify 平台 (dify)

**路径**: `/Users/petrus/Source/dify/ee/dify`

**用途**: 了解平台侧如何调用和集成插件

**关键目录**:
- `api/core/plugin/` - 插件调用核心逻辑
- `api/core/trigger/` - Trigger 相关实现
- `api/core/tools/` - 工具调用实现
- `api/services/` - 服务层实现

**参考场景**:
- 理解插件 API 的调用方式
- 调试平台与插件的交互问题
- 了解 OAuth 集成的平台侧实现

## 本项目文档

### 核心文档

| 文档 | 用途 |
|------|------|
| `架构方案-优化版.md` | 项目整体架构设计，包含 Trigger Plugin 方案 |
| `Dify_Plugin_Development_Guide.md` | 插件开发完整指南 |
| `Dify_Trigger_Plugin_Guide.md` | Trigger 插件专项指南 |
| `solution-design.md` | 技术方案详细设计 |
| `dev-docs.md` | 开发参考链接汇总 |

### API 文档

| 文档 | 用途 |
|------|------|
| `Mercury_API_Documentation.md` | Mercury 银行 API 文档 |
| `QuickBooks_API_Documentation.md` | QuickBooks API 文档 |

## 插件开发规范

### 文件结构标准

```
plugin-name/
├── _assets/
│   └── icon.svg              # 插件图标
├── provider/
│   └── provider-name.yaml    # Provider 配置
├── triggers/                  # Trigger 插件
│   └── trigger-name/
│       ├── trigger-name.yaml # Trigger 配置
│       └── trigger-name.py   # Trigger 实现
├── tools/                     # Tool 插件
│   └── tool-name/
│       ├── tool-name.yaml
│       └── tool-name.py
├── manifest.yaml             # 插件清单
├── requirements.txt          # Python 依赖
└── README.md
```

### 代码风格

1. **Python**
   - 使用类型提示
   - 遵循 PEP 8 规范
   - 使用 `dify_plugin` SDK 提供的基类

2. **YAML 配置**
   - 参考 `dify-official-plugins` 中的格式
   - 确保 `en_US` 和 `zh_Hans` 标签完整

### Trigger 插件开发要点

1. **继承 `Trigger` 基类**
2. **实现 `_run` 方法** - 返回 Generator 
3. **实现 `_schedule` 方法** - 用于定时任务
4. **使用 `self.session.create_message()` 触发 Workflow**

### OAuth 集成要点

1. 在 provider YAML 中配置 `credentials_schema`
2. 使用 `credentials_for_provider` 属性获取认证信息
3. 参考 `dify-official-plugins/tools/` 中的 OAuth 示例

## 开发命令

```bash
# 初始化插件项目
dify plugin init

# 打包插件
dify plugin package ./plugin-folder

# 本地调试（需要先配置 .env）
dify run ./plugin-folder
```

## 调试技巧

### 连接远程调试

1. 在 Dify 平台启用远程调试
2. 获取调试密钥
3. 配置 `.env` 文件
4. 运行 `dify run ./plugin-folder`

### 查看日志

- 插件运行日志通过 STDOUT 输出
- 使用 `logging` 模块记录调试信息

## 搜索策略

当需要查找实现参考时，按以下顺序搜索：

1. **先搜官方插件** (`dify-official-plugins/triggers/` 或 `tools/`)
2. **再查插件运行时** (`dify-plugin-daemon/`) 了解底层实现
3. **最后查平台代码** (`dify/api/`) 了解调用方

## 注意事项

- **不要自动运行测试**：除非用户明确要求
- **优先参考官方插件**：不要凭空实现，先找类似示例
- **保持代码简洁**：不要过度设计，遵循 KISS 原则




