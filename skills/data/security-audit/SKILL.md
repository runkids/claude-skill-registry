---
name: security-audit
description: 代码安全审计指南。当用户需要检查代码安全漏洞、实施安全最佳实践、进行安全代码审查或修复安全问题时使用此技能。
---

# Security Audit

帮助开发者识别和修复代码中的安全漏洞，实施安全编码最佳实践。

## 核心检查清单

### 1. 输入验证

- [ ] 所有用户输入都经过验证和清理
- [ ] 使用白名单而非黑名单验证
- [ ] 限制输入长度和格式
- [ ] 对特殊字符进行转义

### 2. 认证与授权

- [ ] 密码使用强哈希算法（bcrypt/argon2）
- [ ] 实施多因素认证
- [ ] Session 管理安全
- [ ] 权限检查在服务端执行

### 3. 数据保护

- [ ] 敏感数据加密存储
- [ ] 使用 HTTPS 传输
- [ ] API Key 不硬编码
- [ ] 日志不包含敏感信息

## 常见漏洞与修复

### SQL 注入

```javascript
// ❌ 危险：字符串拼接
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ 安全：参数化查询
const query ='SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

### XSS 跨站脚本

```javascript
// ❌ 危险：直接插入 HTML
element.innerHTML = userInput;

// ✅ 安全：使用 textContent 或转义
element.textContent = userInput;
// 或使用 DOMPurify
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 敏感信息泄露

```javascript
// ❌ 危险：硬编码密钥
const API_KEY = 'sk-1234567890';

// ✅ 安全：使用环境变量
const API_KEY = process.env.API_KEY;
```

## 安全扫描工具

| 工具 | 用途 | 命令 |
|------|------|------|
| npm audit | Node.js 依赖漏洞 | `npm audit` |
| Snyk | 多语言依赖扫描 | `snyk test` |
| ESLint Security | JS 代码安全规则 | `eslint --plugin security` |
| Bandit | Python 安全扫描 | `bandit -r ./src` |
| Trivy | 容器镜像扫描 | `trivy image myapp` |

## 安全 Headers配置

```javascript
// Express.js 使用 helmet
const helmet = require('helmet');
app.use(helmet());

// 或手动配置
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  next();
});
```

## 审计流程

1. **依赖检查**：扫描第三方库漏洞
2. **代码审查**：检查常见漏洞模式
3. **配置审计**：检查安全配置
4. **渗透测试**：模拟攻击测试
5. **修复验证**：确认漏洞已修复

## 参考资源

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE 常见漏洞: https://cwe.mitre.org/