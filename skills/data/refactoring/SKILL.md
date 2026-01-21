---
name: refactoring
description: 执行代码重构（识别坏味道→选择手法→小步修改→运行测试），在保持外部行为不变前提下改进内部结构。当TDD进入REFACTOR阶段、发现代码坏味道、需要消除重复代码、优化代码结构时使用。支持提取方法、类、参数对象等重构手法。
stage: EXECSPEC_FULFILL
level_supported: [L1-STREAMLINED, L2-BALANCED, L3-RIGOROUS]
---

# Refactoring Skill

> **Scope**: EXECSPEC_FULFILL — Fulfill ExecSpec（落实 ExecSpec）
>
> **版本**: 0.1.0（占位）| **创建日期**: 2025-11-27

---

## 概述

Refactoring 是在不改变外部行为的前提下改进代码内部结构：

```
┌─────────────────────────────────────────────────────┐
│              🔧 Refactoring Cycle                   │
├─────────────────────────────────────────────────────┤
│  识别坏味道 → 选择手法 → 小步修改 → 运行测试       │
│  (Smell)     (Technique) (Small Step) (Verify)    │
│       ↑                                   │        │
│       └───────────────────────────────────┘        │
└─────────────────────────────────────────────────────┘
```

**核心原则**：
- 小步前进，每步都可验证
- 测试必须始终通过
- 行为不变，结构改进

---

## 代码坏味道

### 常见坏味道

| 坏味道 | 信号 | 重构方向 |
|--------|------|----------|
| **重复代码** | 相似代码块 > 2 处 | Extract Method |
| **过长函数** | > 20 行 | Extract Method |
| **过大类** | > 300 行 | Extract Class |
| **过长参数** | > 4 个参数 | Introduce Parameter Object |
| **特性依恋** | 方法更多使用其他类数据 | Move Method |
| **数据泥团** | 相同数据组合多处出现 | Extract Class |
| **基本类型偏执** | 过度使用基本类型 | Replace with Object |
| **Switch 语句** | 多处相同 switch | Replace with Polymorphism |

---

## 重构手法

### 提取类手法

```
Extract Method      → 提取函数
Extract Class       → 提取类
Extract Interface   → 提取接口
Extract Variable    → 提取变量
```

### 移动类手法

```
Move Method         → 移动方法
Move Field          → 移动字段
Move Class          → 移动类
```

### 简化类手法

```
Inline Method       → 内联方法
Inline Class        → 内联类
Remove Parameter    → 移除参数
Rename              → 重命名
```

---

## L1-STREAMLINED 检查清单

- [ ] 重构前测试全绿
- [ ] 每步修改后运行测试
- [ ] 无新功能添加
- [ ] 代码可读性提升

### 通过标准

- 4 项全部通过（100%）

---

## 重构流程

### 1. 准备阶段

```
□ 确保测试覆盖充分
□ 理解现有代码行为
□ 识别要重构的坏味道
```

### 2. 执行阶段

```
□ 选择合适的重构手法
□ 小步修改（每步 < 5 分钟）
□ 每步后运行测试
□ 提交小步变更
```

### 3. 验证阶段

```
□ 所有测试通过
□ 代码结构改善
□ 无行为变化
```

---

## >> 命令

```
>>smell_detect       # 检测代码坏味道
>>refactor_suggest   # 建议重构手法
>>refactor_verify    # 验证重构结果
```

---

## 相关 Skills

- **前置**: tdd-cycle（GREEN 后进入 REFACTOR）
- **并行**: code-quality（质量检查）
- **原则**: principle-dry, principle-kiss, principle-solid

---

**TODO**: 待细化各重构手法的详细步骤和示例
