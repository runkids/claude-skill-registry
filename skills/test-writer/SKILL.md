---
name: test-writer
description: 测试用例编写技能。当用户需要编写单元测试、集成测试、E2E 测试，或需要提高测试覆盖率、设计测试策略时使用此技能。
---

# Test Writer

编写高质量、可维护的测试用例，确保代码可靠性。

## 测试金字塔

```/\
       /E2E\        少量端到端测试
      /------\
     /集成测试\      适量集成测试
    /----------\
   /  单元测试  \    大量单元测试
  /--------------\
```

## 测试命名规范

```
test_[被测方法]_[场景]_[预期结果]

# 示例
test_login_withValidCredentials_returnsToken
test_divide_byZero_throwsException
test_createUser_duplicateEmail_returns409
```

## 单元测试结构 (AAA 模式)

```python
def test_calculate_discount():
    # Arrange - 准备测试数据
    price = 100
    discount_rate = 0.2
    
    # Act - 执行被测方法
    result = calculate_discount(price, discount_rate)
    
    # Assert - 验证结果
    assert result == 80
```

## 测试用例设计

### 边界值分析
- 最小值、最大值
- 边界值±1
- 空值、零值

### 等价类划分
- 有效等价类
- 无效等价类

### 必测场景
- ✅ 正常流程 (Happy Path)
- ❌ 异常流程 (Error Path)
- 🔲 边界条件 (Edge Cases)
- 🔒 权限验证 (Security)

## Mock 使用原则

```python
# 何时 Mock
- 外部服务（API、数据库）
- 不确定性因素（时间、随机数）
- 耗时操作

# 何时不 Mock
- 被测试的核心逻辑
- 简单的工具函数
```

## 测试质量检查

- [ ] 测试独立性：每个测试可单独运行
- [ ] 测试可重复：多次运行结果一致
- [ ] 测试快速：单元测试 < 100ms
- [ ] 断言明确：每个测试有清晰断言
- [ ] 覆盖充分：核心逻辑 > 80% 覆盖率