---
name: changelog-writer
description: 变更日志编写技能。当用户需要编写 CHANGELOG、版本发布说明、更新记录，或需要整理 Git 提交历史生成变更日志时使用此技能。
---

# Changelog Writer

生成规范、清晰的变更日志，帮助用户了解版本更新内容。

## 格式规范 (Keep a Changelog)

```markdown
# Changelog

## [Unreleased]

## [1.2.0] - 2024-01-15

### Added
- 新增用户导出功能
- 支持 OAuth2.0 登录

### Changed
- 优化首页加载速度
- 更新依赖版本

### Deprecated
- 废弃旧版API v1

### Removed
- 移除过时的配置项

### Fixed
- 修复登录超时问题
- 修复数据导出乱码

### Security
- 修复 XSS 漏洞
```

## 变更类型说明

| 类型 | 说明 |
|------|------|
| Added | 新增功能 |
| Changed | 功能变更 |
| Deprecated | 即将废弃 |
| Removed | 已移除功能 |
| Fixed | Bug 修复 |
| Security | 安全修复 |

## 版本号规范 (SemVer)

```
MAJOR.MINOR.PATCH

1.0.0 → 1.0.1# PATCH: 向后兼容的Bug 修复
1.0.1 → 1.1.0  # MINOR: 向后兼容的新功能
1.1.0 → 2.0.0  # MAJOR: 不兼容的 API 变更
```

## 编写原则

1. **面向用户**：描述对用户的影响，而非技术细节
2. **简洁明了**：每条记录一行，清晰描述变更
3. **按时间倒序**：最新版本在最上方
4. **关联Issue**：重要变更关联 Issue 编号

## 示例条目

```markdown
### Added
- 新增批量导入用户功能 (#123)
- 支持深色模式切换

### Fixed
- 修复大文件上传失败的问题 (#456)
- 修复移动端布局错位
```
