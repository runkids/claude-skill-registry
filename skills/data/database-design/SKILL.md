---
name: database-design
description: 数据库设计指南。当用户需要设计数据库 Schema、优化索引、规划表结构、处理数据关系或进行数据库性能优化时使用此技能。
---

# Database Design

帮助开发者设计高效、可扩展的数据库结构，遵循最佳实践。

## 设计流程

1. **需求分析**：理解业务实体和关系
2. **概念设计**：绘制 ER 图
3. **逻辑设计**：定义表结构和关系
4. **物理设计**：索引、分区策略
5. **优化迭代**：根据查询模式调整

## Schema 设计原则

### 命名规范

```sql
-- 表名：小写复数，下划线分隔
users, order_items, user_profiles

-- 字段名：小写，下划线分隔
created_at, user_id, is_active

-- 主键：id 或 表名单数_id
id, user_id

-- 外键：关联表单数_id
user_id, order_id
```

### 基础表模板

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 更新时间触发器
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## 索引策略

### 何时创建索引

| 场景 | 建议|
|------|------|
| WHERE 条件字段 | ✅ 创建索引 |
| JOIN 关联字段 | ✅ 创建索引 |
| ORDER BY 字段 | ✅ 考虑索引 |
|高频更新字段 | ⚠️ 谨慎索引 |
| 低基数字段 | ❌ 避免索引 |

### 索引类型选择

```sql
-- B-Tree：默认，适合等值和范围查询
CREATE INDEX idx_users_email ON users(email);

-- 复合索引：多字段查询
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- 部分索引：条件过滤
CREATE INDEX idx_active_users ON users(email) WHERE is_active = true;

-- 唯一索引：保证唯一性
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
```

## 关系设计

### 一对多

```sql
-- 用户有多个订单
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    total_amount DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### 多对多

```sql
-- 用户和角色的多对多关系
CREATE TABLE user_roles (
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    role_id BIGINT REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id)
);
```

## 常见反模式

| 反模式 | 问题 | 解决方案 |
|--------|------|----------|
| 过度规范化 | 查询复杂，性能差 | 适度反规范化 |
| 万能表 | 难维护，浪费空间 | 拆分为专用表 |
| 无索引外键 | JOIN 性能差 | 为外键添加索引 |
| 存储 JSON滥用 | 无法有效查询 | 结构化数据用列存储 |

## 性能优化

1. **EXPLAIN 分析**：检查查询计划
2. **避免 SELECT ***：只查询需要的字段
3. **分页优化**：使用游标分页替代 OFFSET
4. **连接池**：复用数据库连接
5. **读写分离**：主从架构分担负载

## 参考资源

- PostgreSQL 文档: https://www.postgresql.org/docs/
- MySQL 优化指南: https://dev.mysql.com/doc/refman/8.0/en/optimization.html