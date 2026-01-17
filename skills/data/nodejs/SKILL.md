---
name: nodejs
description: Node.js and Express development patterns and best practices
license: MIT
compatibility: opencode
---

# Node.js Skill

Comprehensive patterns and best practices for Node.js and Express development.

## What I Know

### Project Structure

```
src/
├── controllers/       # Request handlers
├── services/          # Business logic
├── repositories/      # Data access layer
├── middleware/        # Express middleware
├── routes/            # Route definitions
├── models/            # Data models
├── utils/             # Helper functions
├── config/            # Configuration
├── types/             # TypeScript types
└── index.ts           # Application entry
```

### Express Server Setup

**TypeScript Setup**
```ts
// src/index.ts
import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import compression from 'compression'
import { json } from 'body-parser'
import { morganMiddleware } from './utils/logger'
import { errorHandler } from './middleware/errorHandler'
import { apiRouter } from './routes'

const app = express()

// Security middleware
app.use(helmet())
app.use(cors())
app.use(compression())

// Body parsing
app.use(json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true }))

// Logging
app.use(morganMiddleware)

// Routes
app.use('/api', apiRouter)

// Error handling (must be last)
app.use(errorHandler)

const PORT = process.env.PORT || 3000
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`)
})
```

### Controllers

**Controller Pattern**
```ts
// src/controllers/user.controller.ts
import { Request, Response, NextFunction } from 'express'
import { UserService } from '../services/user.service'
import { CreateUserDto, UpdateUserDto } from '../dto/user.dto'

export class UserController {
  constructor(private userService: UserService) {}

  async findAll(req: Request, res: Response, next: NextFunction) {
    try {
      const users = await this.userService.findAll({
        page: Number(req.query.page) || 1,
        limit: Number(req.query.limit) || 20,
      })
      res.json(users)
    } catch (error) {
      next(error)
    }
  }

  async findOne(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await this.userService.findOne(Number(req.params.id))
      res.json(user)
    } catch (error) {
      next(error)
    }
  }

  async create(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await this.userService.create(req.body as CreateUserDto)
      res.status(201).json(user)
    } catch (error) {
      next(error)
    }
  }

  async update(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await this.userService.update(
        Number(req.params.id),
        req.body as UpdateUserDto
      )
      res.json(user)
    } catch (error) {
      next(error)
    }
  }

  async delete(req: Request, res: Response, next: NextFunction) {
    try {
      await this.userService.delete(Number(req.params.id))
      res.status(204).send()
    } catch (error) {
      next(error)
    }
  }
}
```

### Services (Business Logic)

```ts
// src/services/user.service.ts
import { UserRepository } from '../repositories/user.repository'
import { User } from '../models/user.model'
import { CreateUserDto, UpdateUserDto } from '../dto/user.dto'
import { ConflictException, NotFoundException } from '../exceptions'

export class UserService {
  constructor(private userRepository: UserRepository) {}

  async findAll(options: { page: number; limit: number }) {
    const { page, limit } = options
    const [data, total] = await Promise.all([
      this.userRepository.findMany({ skip: (page - 1) * limit, take: limit }),
      this.userRepository.count()
    ])

    return {
      data,
      meta: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit)
      }
    }
  }

  async findOne(id: number): Promise<User> {
    const user = await this.userRepository.findOne(id)
    if (!user) {
      throw new NotFoundException('User not found')
    }
    return user
  }

  async create(dto: CreateUserDto): Promise<User> {
    const existing = await this.userRepository.findByEmail(dto.email)
    if (existing) {
      throw new ConflictException('Email already exists')
    }
    return this.userRepository.create(dto)
  }

  async update(id: number, dto: UpdateUserDto): Promise<User> {
    const user = await this.findOne(id)
    return this.userRepository.update(id, dto)
  }

  async delete(id: number): Promise<void> {
    await this.findOne(id)
    await this.userRepository.delete(id)
  }
}
```

### Repositories (Data Access)

```ts
// src/repositories/user.repository.ts
import { PrismaClient, User } from '@prisma/client'
import { CreateUserDto, UpdateUserDto } from '../dto/user.dto'

export class UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findMany(options: { skip?: number; take?: number }) {
    return this.prisma.user.findMany({
      skip: options.skip,
      take: options.take,
      select: {
        id: true,
        email: true,
        name: true,
        createdAt: true,
        password: false,
      },
    })
  }

  async findOne(id: number) {
    return this.prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        email: true,
        name: true,
        createdAt: true,
        password: false,
      },
    })
  }

  async findByEmail(email: string) {
    return this.prisma.user.findUnique({
      where: { email },
    })
  }

  async create(dto: CreateUserDto) {
    return this.prisma.user.create({
      data: {
        email: dto.email,
        name: dto.name,
        password: await this.hashPassword(dto.password),
      },
    })
  }

  async update(id: number, dto: UpdateUserDto) {
    return this.prisma.user.update({
      where: { id },
      data: dto,
    })
  }

  async delete(id: number) {
    return this.prisma.user.delete({
      where: { id },
    })
  }

  async count() {
    return this.prisma.user.count()
  }

  private async hashPassword(password: string): Promise<string> {
    const bcrypt = await import('bcrypt')
    return bcrypt.hash(password, 10)
  }
}
```

### Routes

```ts
// src/routes/index.ts
import { Router } from 'express'
import { UserController } from '../controllers/user.controller'
import { authMiddleware } from '../middleware/auth.middleware'
import { validateMiddleware } from '../middleware/validate.middleware'
import { createUserSchema, updateUserSchema } from '../validators/user.validator'

const router = Router()
const controller = new UserController(/* inject dependencies */)

router.get('/users', controller.findAll.bind(controller))
router.get('/users/:id', controller.findOne.bind(controller))
router.post('/users', validateMiddleware(createUserSchema), controller.create.bind(controller))
router.patch('/users/:id', validateMiddleware(updateUserSchema), controller.update.bind(controller))
router.delete('/users/:id', controller.delete.bind(controller))

export function apiRouter(): Router {
  return router
}
```

### Middleware

**Authentication**
```ts
// src/middleware/auth.middleware.ts
import { Request, Response, NextFunction } from 'express'
import jwt from 'jsonwebtoken'

export interface AuthRequest extends Request {
  userId?: number
}

export function authMiddleware(req: AuthRequest, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization

  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Unauthorized' })
  }

  const token = authHeader.split(' ')[1]

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as { userId: number }
    req.userId = payload.userId
    next()
  } catch {
    return res.status(401).json({ error: 'Invalid token' })
  }
}
```

**Error Handler**
```ts
// src/middleware/errorHandler.ts
import { Request, Response, NextFunction } from 'express'
import { ZodError } from 'zod'
import { AppError } from '../exceptions/app.error'

export function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  console.error(err)

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: err.message,
      ...(err.errors && { errors: err.errors }),
    })
  }

  if (err instanceof ZodError) {
    return res.status(400).json({
      error: 'Validation error',
      errors: err.errors,
    })
  }

  res.status(500).json({ error: 'Internal server error' })
}
```

### Validation (Zod)

```ts
// src/validators/user.validator.ts
import { z } from 'zod'

export const createUserSchema = z.object({
  email: z.string().email('Invalid email format'),
  name: z.string().min(2).max(100),
  password: z.string().min(8).regex(/[A-Z]/).regex(/[0-9]/),
})

export const updateUserSchema = createUserSchema.partial()

export type CreateUserDto = z.infer<typeof createUserSchema>
export type UpdateUserDto = z.infer<typeof updateUserSchema>
```

### Dependency Injection

**DI Container (Simple)**
```ts
// src/container.ts
import { PrismaClient } from '@prisma/client'
import { UserRepository } from './repositories/user.repository'
import { UserService } from './services/user.service'
import { UserController } from './controllers/user.controller'

class DIContainer {
  private static instances = new Map()

  static register<T>(key: string, factory: () => T) {
    this.instances.set(key, factory())
  }

  static resolve<T>(key: string): T {
    const instance = this.instances.get(key)
    if (!instance) {
      throw new Error(`Dependency ${key} not found`)
    }
    return instance as T
  }
}

// Initialize
DIContainer.register('prisma', () => new PrismaClient())
DIContainer.register('userRepo', () => new UserRepository(DIContainer.resolve('prisma')))
DIContainer.register('userService', () => new UserService(DIContainer.resolve('userRepo')))
DIContainer.register('userController', () => new UserController(DIContainer.resolve('userService')))
```

### Async Patterns

**Promises & Async/Await**
```ts
// Parallel execution
async function getUserData(userId: number) {
  const [user, posts, settings] = await Promise.all([
    userRepository.findOne(userId),
    postRepository.findByUser(userId),
    settingsRepository.findByUser(userId),
  ])

  return { user, posts, settings }
}

// Error handling in async
async function safeExecute<T>(
  fn: () => Promise<T>
): Promise<{ data?: T; error?: Error }> {
  try {
    const data = await fn()
    return { data }
  } catch (error) {
    return { error: error as Error }
  }
}
```

### Environment Configuration

```ts
// src/config/index.ts
import { z } from 'zod'

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.string().transform(Number).default('3000'),
  DATABASE_URL: z.string(),
  JWT_SECRET: z.string(),
  REDIS_URL: z.string().optional(),
})

export const env = envSchema.parse(process.env)
```

### Testing

**Jest Setup**
```ts
// tests/unit/user.service.test.ts
import { describe, it, expect, beforeEach } from '@jest/globals'
import { UserService } from '../../src/services/user.service'
import { MockUserRepository } from '../mocks/user.repository.mock'

describe('UserService', () => {
  let service: UserService
  let mockRepo: MockUserRepository

  beforeEach(() => {
    mockRepo = new MockUserRepository()
    service = new UserService(mockRepo)
  })

  it('should return all users with pagination', async () => {
    mockRepo.mockFindMany([{ id: 1, email: 'test@example.com' }])
    mockRepo.mockCount(10)

    const result = await service.findAll({ page: 1, limit: 20 })

    expect(result.data).toHaveLength(1)
    expect(result.meta.total).toBe(10)
  })

  it('should throw NotFoundException when user not found', async () => {
    mockRepo.mockFindOne(null)

    await expect(service.findOne(999)).rejects.toThrow('User not found')
  })
})
```

### Common Pitfalls

1. **Callback hell** → Use async/await
2. **Mixing callbacks and promises** → Choose one approach
3. **Not handling errors** → Always use try/catch
4. **Blocking event loop** → Offload CPU-intensive work
5. **Memory leaks** → Clean up listeners and timers
6. **Ignoring TypeScript** → Use types for safety
7. **Secrets in code** → Use environment variables

### API Design Patterns

**RESTful Conventions**
```ts
// Use proper HTTP methods and status codes
export class UserController {
  // GET /users - List with pagination
  @Get()
  async findAll(@Req() req: Request) {
    const { page = 1, limit = 20, search } = req.query
    const result = await this.userService.findAll({ page, limit, search })
    res.json(result)
  }

  // GET /users/:id - Get single resource
  @Get(':id')
  async findOne(@Param('id') id: string) {
    const user = await this.userService.findOne(id)
    if (!user) throw new NotFoundException('User not found')
    res.json(user)
  }

  // POST /users - Create resource
  @Post()
  async create(@Body() dto: CreateUserDto) {
    const user = await this.userService.create(dto)
    res.status(201).json(user)
  }

  // PATCH /users/:id - Partial update
  @Patch(':id')
  async update(@Param('id') id: string, @Body() dto: UpdateUserDto) {
    const user = await this.userService.update(id, dto)
    res.json(user)
  }

  // DELETE /users/:id - Delete resource
  @Delete(':id')
  async delete(@Param('id') id: string) {
    await this.userService.delete(id)
    res.status(204).send()
  }
}
```

**Standardized API Response**
```ts
// src/utils/response.ts
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: {
    code: string
    message: string
    details?: unknown
  }
  meta?: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

export function successResponse<T>(
  data: T,
  meta?: ApiResponse<T>['meta']
): ApiResponse<T> {
  return { success: true, data, meta }
}

export function errorResponse(
  code: string,
  message: string,
  details?: unknown
): ApiResponse<never> {
  return { success: false, error: { code, message, details } }
}
```

**API Versioning**
```ts
// src/routes/v1/index.ts
const v1Router = Router()
v1Router.use('/users', userRoutes)

// src/routes/index.ts
import { Router } from 'express'

const apiRouter = Router()

apiRouter.use('/v1', v1Router)
// Future: apiRouter.use('/v2', v2Router)

export { apiRouter }
```

**Rate Limiting**
```ts
// src/middleware/rateLimit.ts
import rateLimit from 'express-rate-limit'

export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per window
  message: 'Too many requests from this IP',
  standardHeaders: true,
  legacyHeaders: false,
})

export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Stricter for auth endpoints
  skipSuccessfulRequests: true,
})
```

**Pagination Helper**
```ts
// src/utils/pagination.ts
export interface PaginationOptions {
  page: number
  limit: number
}

export interface PaginatedResult<T> {
  data: T[]
  meta: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

export function createPagination<T>(
  data: T[],
  total: number,
  options: PaginationOptions
): PaginatedResult<T> {
  const { page, limit } = options
  return {
    data,
    meta: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  }
}

export function getPaginationParams(query: any): PaginationOptions {
  const page = Math.max(1, Number(query.page) || 1)
  const limit = Math.min(100, Math.max(1, Number(query.limit) || 20))
  return { page, limit }
}
```

### Database Patterns

**Connection Pooling**
```ts
// src/config/database.ts
import { Pool } from 'pg'

export const pool = new Pool({
  host: process.env.DB_HOST,
  port: Number(process.env.DB_PORT),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20, // Maximum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
})

pool.on('error', (err) => {
  console.error('Unexpected database error', err)
})
```

**Transaction Pattern**
```ts
// src/repositories/base.repository.ts
export class BaseRepository {
  async transaction<T>(
    callback: (client: PoolClient) => Promise<T>
  ): Promise<T> {
    const client = await pool.connect()
    try {
      await client.query('BEGIN')
      const result = await callback(client)
      await client.query('COMMIT')
      return result
    } catch (error) {
      await client.query('ROLLBACK')
      throw error
    } finally {
      client.release()
    }
  }
}

// Usage
await userRepository.transaction(async (client) => {
  await createUser(client, userData)
  await createProfile(client, profileData)
})
```

**Query Builder Pattern**
```ts
// src/repositories/query-builder.ts
export class QueryBuilder {
  private query = ''
  private params: any[] = []
  private whereCount = 0

  select(columns: string): this {
    this.query = `SELECT ${columns}`
    return this
  }

  from(table: string): this {
    this.query += ` FROM ${table}`
    return this
  }

  where(column: string, value: any): this {
    this.whereCount++
    const param = `$${this.params.length + 1}`
    this.params.push(value)

    if (this.whereCount === 1) {
      this.query += ` WHERE ${column} = ${param}`
    } else {
      this.query += ` AND ${column} = ${param}`
    }
    return this
  }

  orderBy(column: string, direction: 'ASC' | 'DESC' = 'ASC'): this {
    this.query += ` ORDER BY ${column} ${direction}`
    return this
  }

  limit(count: number): this {
    this.query += ` LIMIT $${this.params.length + 1}`
    this.params.push(count)
    return this
  }

  build(): { query: string; params: any[] } {
    return { query: this.query, params: this.params }
  }
}
```

**Repository Pattern with Mongoose**
```ts
// src/repositories/user.repository.ts
import { Model, Document, FilterQuery } from 'mongoose'

export class BaseRepository<T extends Document> {
  constructor(private model: Model<T>) {}

  async findOne(id: string): Promise<T | null> {
    return this.model.findById(id).exec()
  }

  async findOneBy(filter: FilterQuery<T>): Promise<T | null> {
    return this.model.findOne(filter).exec()
  }

  async findMany(filter: FilterQuery<T> = {}): Promise<T[]> {
    return this.model.find(filter).exec()
  }

  async create(data: Partial<T>): Promise<T> {
    return this.model.create(data)
  }

  async update(id: string, data: Partial<T>): Promise<T | null> {
    return this.model.findByIdAndUpdate(id, data, { new: true }).exec()
  }

  async delete(id: string): Promise<T | null> {
    return this.model.findByIdAndDelete(id).exec()
  }

  async paginate(
    filter: FilterQuery<T> = {},
    options: { page: number; limit: number } = { page: 1, limit: 20 }
  ) {
    const { page, limit } = options
    const skip = (page - 1) * limit

    const [data, total] = await Promise.all([
      this.model.find(filter).skip(skip).limit(limit).exec(),
      this.model.countDocuments(filter),
    ])

    return { data, meta: { page, limit, total, totalPages: Math.ceil(total / limit) } }
  }
}
```

### Security Patterns

**Helmet (Security Headers)**
```ts
import helmet from 'helmet'

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
}))
```

**CORS Configuration**
```ts
import cors from 'cors'

const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(',') || ['http://localhost:3000']

app.use(cors({
  origin: (origin, callback) => {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true)
    } else {
      callback(new Error('Not allowed by CORS'))
    }
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
}))
```

**Input Sanitization**
```ts
// src/middleware/sanitize.ts
import { body, param, query, validationResult } from 'express-validator'

export const validate = (req: Request, res: Response, next: NextFunction) => {
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() })
  }
  next()
}

export const userValidation = {
  create: [
    body('email').isEmail().normalizeEmail(),
    body('name').trim().escape().isLength({ min: 2, max: 100 }),
    body('password').isStrongPassword(),
    validate,
  ],
  update: [
    param('id').isMongoId(),
    body('email').optional().isEmail().normalizeEmail(),
    body('name').optional().trim().escape().isLength({ min: 2, max: 100 }),
    validate,
  ],
}
```

**JWT Authentication**
```ts
// src/utils/jwt.ts
import jwt from 'jsonwebtoken'

export function generateToken(payload: { userId: string }): string {
  return jwt.sign(
    payload,
    process.env.JWT_SECRET!,
    { expiresIn: process.env.JWT_EXPIRES_IN || '1h' }
  )
}

export function verifyToken(token: string): { userId: string } {
  return jwt.verify(token, process.env.JWT_SECRET!) as { userId: string }
}

export function generateRefreshToken(payload: { userId: string }): string {
  return jwt.sign(
    payload,
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: '7d' }
  )
}
```

**Password Hashing**
```ts
// src/utils/password.ts
import bcrypt from 'bcrypt'

export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, 12)
}

export async function verifyPassword(
  password: string,
  hash: string
): Promise<boolean> {
  return bcrypt.compare(password, hash)
}
```

**XSS Protection**
```ts
// src/utils/sanitize.ts
import createDOMPurify from 'dompurify'
import { JSDOM } from 'jsdom'

const window = new JSDOM('').window
const DOMPurify = createDOMPurify(window)

export function sanitizeHtml(html: string): string {
  return DOMPurify.sanitize(html, { ALLOWED_TAGS: [] })
}

export function sanitizeUserInput(input: string): string {
  return input.trim().replace(/[<>]/g, '')
}
```

**SQL Injection Prevention**
```ts
// Use parameterized queries - NEVER concatenate user input
// BAD:
const query = `SELECT * FROM users WHERE id = '${userId}'`

// GOOD:
const query = 'SELECT * FROM users WHERE id = $1'
await pool.query(query, [userId])

// With Prisma/ORM:
await prisma.user.findUnique({ where: { id: userId } })
```

### Performance Patterns

**Response Compression**
```ts
import compression from 'compression'

app.use(compression({
  filter: (req, res) => {
    if (req.headers['x-no-compression']) return false
    return compression.filter(req, res)
  },
  threshold: 1024, // Only compress if payload > 1KB
}))
```

**Caching Strategy**
```ts
// src/cache/redis.ts
import { createClient } from 'redis'

const redis = createClient({
  url: process.env.REDIS_URL,
})

export class CacheService {
  async get<T>(key: string): Promise<T | null> {
    const data = await redis.get(key)
    return data ? JSON.parse(data) : null
  }

  async set(key: string, value: any, ttl: number = 3600): Promise<void> {
    await redis.setEx(key, ttl, JSON.stringify(value))
  }

  async delete(key: string): Promise<void> {
    await redis.del(key)
  }

  async invalidatePattern(pattern: string): Promise<void> {
    const keys = await redis.keys(pattern)
    if (keys.length) await redis.del(keys)
  }
}

// Caching middleware
export function cacheMiddleware(ttl: number = 300) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const key = `cache:${req.originalUrl}`
    const cached = await cacheService.get(key)

    if (cached) {
      return res.json(cached)
    }

    // Capture original json method
    const originalJson = res.json.bind(res)
    res.json = (data) => {
      cacheService.set(key, data, ttl)
      return originalJson(data)
    }

    next()
  }
}
```

**Database Query Optimization**
```ts
// Use connection pooling
// Select only needed columns
const users = await prisma.user.findMany({
  select: { id: true, name: true, email: true },
})

// Use pagination for large datasets
const users = await prisma.user.findMany({
  skip: (page - 1) * limit,
  take: limit,
})

// Use indexes in database
// Eager loading to prevent N+1 queries
const users = await prisma.user.findMany({
  include: { posts: true },
})

// Batch operations
await prisma.user.createMany({
  data: usersData,
})
```

**Worker Threads for CPU Intensive Tasks**
```ts
// src/workers/heavy-task.ts
import { Worker, isMainThread, parentPort, workerData } from 'worker_threads'

export function runHeavyTask(data: any): Promise<any> {
  return new Promise((resolve, reject) => {
    const worker = new Worker(__filename, {
      workerData: data,
    })

    worker.on('message', resolve)
    worker.on('error', reject)
    worker.on('exit', (code) => {
      if (code !== 0) reject(new Error(`Worker stopped with exit code ${code}`))
    })
  })
}

if (!isMainThread) {
  // CPU intensive work here
  const result = heavyComputation(workerData)
  parentPort?.postMessage(result)
}
```

**Lazy Loading Routes**
```ts
// src/app.ts
import express from 'express'

const app = express()

// Lazy load routes
app.use('/api/users', (req, res, next) => {
  import('./routes/user.routes').then((routes) => {
    routes.default(req, res, next)
  })
})
```

### Best Practices

1. **Use TypeScript** for type safety
2. **Use async/await** for cleaner code
3. **Validate input** with Zod or express-validator
4. **Centralize error handling** in middleware
5. **Use dependency injection** for testability
6. **Keep controllers thin** - move logic to services
7. **Use environment variables** for configuration
8. **Handle promises properly** - no floating promises
9. **Implement caching** for frequently accessed data
10. **Sanitize all user input** to prevent XSS and injection attacks
11. **Use parameterized queries** to prevent SQL injection
12. **Set up rate limiting** to prevent abuse
13. **Use connection pooling** for database connections
14. **Implement proper logging** for debugging and monitoring
15. **Use compression** to reduce response size

---

*Part of SuperAI GitHub - Centralized OpenCode Configuration*
