---
name: git-commit-helper
description: 分析 Git diff 并生成符合规范的提交信息
allowed-tools:
  - Bash
---

# Git 提交助手

帮助生成规范的 Git 提交信息。

## 工作流程

1. **检查 Git 仓库**
   - 确认当前目录是 Git 仓库
   - 检查是否有未提交的更改

2. **分析变更**
   - 运行 `git diff` 查看修改
   - 识别变更的类型和范围

3. **生成提交信息**
   - 遵循提交信息规范
   - 包含类型、范围和描述

4. **确认并提交**
   - 展示生成的提交信息
   - 询问是否确认
   - 如果确认，执行提交

## 提交信息规范

生成的提交信息遵循以下格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type（类型）

- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档变更
- `style`: 代码格式（不影响功能）
- `refactor`: 重构（既不是新功能也不是修复）
- `perf`: 性能优化
- `test`: 添加测试
- `chore`: 构建或辅助工具的变更

### Scope（范围）

变更影响的模块或组件，例如：

- `api`: API 相关
- `ui`: 用户界面
- `auth`: 认证相关
- `config`: 配置文件

### Subject（描述）

- 使用现在时态（"add" 而不是 "added"）
- 首字母小写
- 不要以句号结尾

## 输出格式

生成的提交信息应该：

```markdown
# 建议的提交信息

```

feat(api): add user authentication endpoint

- Add POST /api/auth/login endpoint
- Implement JWT token generation
- Add input validation for credentials

Closes #123

```

## 分析结果

**变更文件**：
- [文件列表]

**变更类型**：feat/fix/docs/etc
**影响范围**：api/ui/etc
**变更摘要**：[简短描述]

---

是否确认使用这个提交信息？或者你想修改它？
```

## 使用示例

查看 [examples.md](examples.md) 了解更多使用示例。

## 注意事项

- 如果没有未提交的更改，提示用户
- 如果是首次提交，特殊处理
- 提供修改提交信息的机会
- 执行前再次确认

---

开始分析当前的 Git 变更吧！
