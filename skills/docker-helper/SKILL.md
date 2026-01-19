---
name: docker-helper
description: Docker容器化开发指南。当用户需要编写 Dockerfile、配置 docker-compose、优化镜像大小、调试容器问题或实施容器化最佳实践时使用此技能。
---

# Docker Helper

帮助开发者高效地进行容器化开发，编写优化的 Dockerfile 和 docker-compose 配置。

## 核心能力

- Dockerfile 编写与优化
- docker-compose 多服务编排
- 镜像体积优化
- 多阶段构建
- 容器调试与问题排查

## Dockerfile 最佳实践

### 基础模板

```dockerfile
# 使用官方基础镜像，指定具体版本
FROM node:20-alpine AS base

# 设置工作目录
WORKDIR /app

# 先复制依赖文件（利用缓存）
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production

# 复制源代码
COPY . .

# 非root 用户运行
USER node

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["node", "server.js"]
```

### 多阶段构建（推荐）

```dockerfile
# 构建阶段
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 生产阶段
FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

##镜像优化指南

### 1. 选择合适的基础镜像

|镜像 | 大小 | 适用场景 |
|------|------|----------|
| `alpine` | ~5MB | 生产环境首选 |
| `slim` | ~80MB | 需要更多系统工具 |
| `bookworm` | ~120MB | 完整 Debian 环境 |

### 2. 减少层数和大小

```dockerfile
# ❌ 不推荐：多个RUN 指令
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get clean

# ✅ 推荐：合并 RUN 指令
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### 3. 使用 .dockerignore

```
node_modules
.git
.env
*.log
dist
coverage
.DS_Store
```

## docker-compose 模板

### 开发环境

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "3000:3000"
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

## 常用命令速查

```bash
# 构建镜像
docker build -t myapp:latest .

# 查看镜像大小
docker images myapp

# 分析镜像层
docker history myapp:latest

# 进入运行中的容器
docker exec -it<container_id> sh

# 查看容器日志
docker logs -f <container_id>

# 清理未使用资源
docker system prune -a

# 导出镜像
docker save myapp:latest | gzip > myapp.tar.gz
```

## 调试技巧

### 1. 构建失败调试

```bash
# 使用 --progress=plain 查看详细输出
docker build --progress=plain -t myapp .

# 从特定阶段开始构建
docker build --target builder -t myapp:builder .
```

### 2. 容器运行调试

```bash
# 覆盖入口点进入 shell
docker run -it --entrypoint sh myapp

# 检查容器文件系统
docker run --rm -it myapp ls -la /app
```

## 安全建议

1. **不使用 root 用户**：始终使用 `USER` 指令
2. **扫描漏洞**：使用 `docker scout` 或 `trivy`
3. **固定版本**：避免使用 `latest` 标签
4. **最小权限**：只安装必要的包
5. **敏感信息**：使用 secrets，不要硬编码

## 参考资源

- Docker 官方文档：https://docs.docker.com
- Dockerfile 最佳实践：https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- Docker Compose 规范：https://docs.docker.com/compose/compose-file/