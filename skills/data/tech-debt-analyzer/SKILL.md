# 💳 Tech Debt Analyzer Skill

---
name: tech-debt-analyzer
description: Identify, measure, and prioritize technical debt for strategic remediation
---

## 🎯 Purpose

วิเคราะห์ technical debt ใน codebase เพื่อวางแผนการแก้ไขอย่างมีกลยุทธ์

## 📋 When to Use

- Sprint planning
- Refactoring decisions
- Code quality audits
- Resource allocation
- Risk assessment

## 🔧 Debt Categories

| Category | Examples | Impact |
|----------|----------|--------|
| **Code** | Duplication, complexity | Maintainability |
| **Architecture** | Tight coupling, monolith | Scalability |
| **Testing** | Low coverage | Reliability |
| **Dependencies** | Outdated packages | Security |
| **Documentation** | Missing docs | Onboarding |
| **Infrastructure** | Manual processes | Efficiency |

## 📊 Debt Metrics

### Code Quality
```bash
# Complexity (ESLint)
npx eslint --ext .ts,.tsx src/ --format json

# Duplication
npx jscpd src/

# Test coverage
npm run test -- --coverage
```

### Scoring
| Metric | Good | Moderate | High Debt |
|--------|------|----------|-----------|
| Coverage | >80% | 50-80% | <50% |
| Complexity | <10 | 10-20 | >20 |
| Duplication | <3% | 3-5% | >5% |

## 📝 Debt Analysis Template

```markdown
## 💳 Tech Debt Report

### Summary
- **Total Items**: 23
- **High Priority**: 5
- **Estimated Effort**: 40 hours

### By Category
| Category | Count | Priority |
|----------|-------|----------|
| Code | 10 | Medium |
| Testing | 8 | High |
| Deps | 5 | High |

### Top Items

#### 1. Low Test Coverage in Auth Module
- **Impact**: High (security critical)
- **Effort**: 8 hours
- **Risk**: Bugs in production

#### 2. Outdated React Version
- **Impact**: Medium (missing features)
- **Effort**: 16 hours
- **Risk**: Security vulnerabilities
```

## 🔄 Remediation Process

```
1. IDENTIFY debt
2. MEASURE impact
3. PRIORITIZE by ROI
4. ALLOCATE (20% sprint capacity)
5. TRACK progress
```

## ✅ Debt Prevention

- [ ] Code reviews
- [ ] Test requirements
- [ ] Dependency updates
- [ ] Documentation standards
- [ ] Refactoring time

## 🔗 Related Skills

- `code-review` - Prevent debt
- `refactoring` - Pay down debt
- `testing` - Reduce test debt
