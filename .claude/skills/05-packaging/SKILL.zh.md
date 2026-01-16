# 插件打包与发布阶段

插件开发的打包和发布阶段，包括构建、版本管理和分发。

## 何时使用此技能

- 将插件打包为 .difypkg 文件
- 管理版本号
- 准备发布
- 维护和迭代

## 输出目录规范

**重要**: 所有 `.difypkg` 文件应统一输出到项目根目录的 `dist/` 目录。

```
finance_plugins/
├── dist/                           # 所有打包后的插件文件
│   ├── quickbooks_plugin.difypkg
│   ├── quickbooks_payments_plugin.difypkg
│   ├── mercury_tools_plugin.difypkg
│   └── mercury_trigger_plugin.difypkg
├── quickbooks_plugin/              # 插件源代码
├── quickbooks_payments_plugin/
├── mercury_tools_plugin/
├── mercury_trigger_plugin/
└── archive/                        # 文档和归档资料
```

## 打包命令

### 单个插件打包

```bash
# 进入项目根目录
cd /path/to/finance_plugins

# 打包单个插件到 dist/ 目录
dify plugin package ./mercury_tools_plugin -o ./dist/mercury_tools_plugin.difypkg

# 验证打包结果
ls -la ./dist/mercury_tools_plugin.difypkg
```

### 批量打包脚本

```bash
#!/bin/bash
# build_all.sh - 批量打包所有插件到 dist/ 目录

set -e

PROJECT_ROOT="/path/to/finance_plugins"
DIST_DIR="${PROJECT_ROOT}/dist"

# 确保 dist 目录存在
mkdir -p "$DIST_DIR"

cd "$PROJECT_ROOT"

# 遍历所有 *_plugin 目录
for plugin_dir in *_plugin/; do
    plugin_name="${plugin_dir%/}"
    output_file="${DIST_DIR}/${plugin_name}.difypkg"
    
    echo "📦 正在打包 ${plugin_name}..."
    
    # 打包
    if dify plugin package "./${plugin_dir}" -o "$output_file"; then
        echo "   ✅ 已创建: ${output_file}"
    else
        echo "   ❌ 打包失败 ${plugin_name}"
        exit 1
    fi
done

echo ""
echo "🎉 所有插件打包成功!"
echo ""
echo "输出文件:"
ls -la "$DIST_DIR"/*.difypkg
```

### 验证打包

```bash
# 验证校验和
dify plugin checksum ./dist/mercury_tools_plugin.difypkg

# 查看包内容 (difypkg 是 zip 格式)
unzip -l ./dist/mercury_tools_plugin.difypkg
```

## 版本管理

### 语义化版本

```yaml
# 语义化版本: major.minor.patch
version: 0.1.0  # 初始发布
version: 0.2.0  # 新功能 (向后兼容)
version: 0.2.1  # Bug 修复
version: 1.0.0  # 破坏性更改
```

### 版本升级规则

| 变更类型 | 版本部分 | 示例 |
|----------|----------|------|
| Bug 修复 | patch | 0.1.0 → 0.1.1 |
| 新功能 (兼容) | minor | 0.1.1 → 0.2.0 |
| 破坏性更改 | major | 0.2.0 → 1.0.0 |

### 更新版本号

在 `manifest.yaml` 中更新版本：

```yaml
version: 0.2.0  # 在此更新

# ... 其他配置 ...

meta:
  version: 0.2.0  # 同步更新此处
```

## 质量检查清单

### 发布前检查清单

```yaml
pre_release_checklist:
  code_quality:
    - [ ] 没有硬编码的凭据
    - [ ] 没有敏感数据
    - [ ] 代码注释清晰
    - [ ] 错误消息对用户友好
    
  functionality:
    - [ ] 所有工具已测试
    - [ ] Provider 验证正常
    - [ ] 错误处理完善
    - [ ] 支持多环境
    
  configuration:
    - [ ] .gitignore 配置正确
    - [ ] manifest.yaml 完整
    - [ ] 版本号已更新
    - [ ] 使用有效标签
    
  documentation:
    - [ ] README.md 存在
    - [ ] 使用说明清晰
    - [ ] 认证设置已文档化
```

### 敏感数据检查

```bash
# 检查硬编码的凭据
grep -r "api_key\|secret\|password\|token" ./my_plugin --include="*.py" | grep -v "def\|#\|credentials"

# 检查 .gitignore
cat .gitignore
```

## 文档

### README 模板

```markdown
# [插件名称]

## 概述
简要描述插件用途。

## 功能
- 功能 1
- 功能 2
- 功能 3

## 安装
1. 下载 `plugin_name.difypkg`
2. 在 Dify 控制台上传插件
3. 配置凭据

## 配置

### 凭据
| 字段 | 描述 | 必需 |
|------|------|------|
| API Key | 你的 API key | 是 |
| Environment | sandbox/production | 是 |

### 获取 API Key
1. 访问 [开发者门户](https://...)
2. 创建应用
3. 复制 API Key

## 可用工具

### get_data
从服务获取数据。

**参数:**
- `resource_id` (string, 必需): 资源 ID

**示例:**
```json
{
  "resource_id": "123"
}
```

## 测试
参见 `test_plugin.py`

## 版本历史
- 0.1.0: 初始发布
- 0.2.0: 添加 xxx 功能
```

## 维护与迭代

### 8.1 监控问题

- 跟踪用户反馈
- 记录常见错误
- 识别改进区域

### 8.2 添加功能

```bash
# 1. 更新代码
# 2. 更新 minor 版本
# manifest.yaml: version: 0.1.0 → 0.2.0

# 3. 重新打包
dify plugin package ./my_plugin -o ./dist/my_plugin.difypkg

# 4. 测试
# 5. 发布
```

### 8.3 修复 Bug

```bash
# 1. 修复代码
# 2. 更新 patch 版本
# manifest.yaml: version: 0.1.0 → 0.1.1

# 3. 重新打包
dify plugin package ./my_plugin -o ./dist/my_plugin.difypkg

# 4. 验证修复
# 5. 发布
```

## CI/CD 集成 (可选)

### GitHub Actions 示例

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
          # 安装 dify CLI
          
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

## 分发

### 分发方式

1. **直接分享**
   - 发送 `.difypkg` 文件
   - 用户手动上传到 Dify

2. **内部仓库**
   - 存储在内部文件服务器
   - 提供下载链接

3. **Dify 插件市场** (如可用)
   - 提交到官方市场
   - 更广泛的分发

### 发布检查

```bash
# 最终检查
echo "=== 最终发布检查清单 ==="

# 1. 版本号
grep "version:" ./my_plugin/manifest.yaml

# 2. 包大小
ls -lh ./dist/my_plugin.difypkg

# 3. 校验和
dify plugin checksum ./dist/my_plugin.difypkg

echo "=== 准备发布! ==="
```

## 相关技能

- **01-design**: 设计阶段
- **02-api-reference**: API 文档参考
- **03-development**: 开发实现
- **04-testing**: 测试验证
- **dify-plugin**: 完整开发指南
