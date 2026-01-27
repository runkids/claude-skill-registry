---
name: boilerplate
description: Generate framework-specific boilerplate code
disable-model-invocation: true
---

# Framework Boilerplate Generator

I'll generate framework-specific boilerplate code following best practices and conventions for React, Vue, Next.js, Express, FastAPI, Django, and more.

Arguments: `$ARGUMENTS` - component/route/model name and type

**Supported Frameworks:**
- Frontend: React, Vue, Next.js, Angular, Svelte
- Backend: Express, Fastify, NestJS, FastAPI, Django
- Full-stack: Next.js, Remix, SvelteKit

**Token Optimization:**
- Framework detection via Grep (100 tokens)
- Template-based generation (500-800 tokens)
- Reads only config files (400 tokens)
- Expected: 2,500-4,000 tokens total

## Phase 1: Framework Detection

```bash
#!/bin/bash
# Detect project framework

echo "=== Detecting Framework ==="
echo ""

detect_framework() {
    if [ -f "package.json" ]; then
        if grep -q "\"react\"" package.json; then
            if grep -q "\"next\"" package.json; then
                echo "nextjs"
            else
                echo "react"
            fi
        elif grep -q "\"vue\"" package.json; then
            echo "vue"
        elif grep -q "\"@angular/core\"" package.json; then
            echo "angular"
        elif grep -q "\"svelte\"" package.json; then
            echo "svelte"
        elif grep -q "\"express\"" package.json; then
            echo "express"
        elif grep -q "\"fastify\"" package.json; then
            echo "fastify"
        elif grep -q "\"@nestjs/core\"" package.json; then
            echo "nestjs"
        fi
    elif [ -f "requirements.txt" ]; then
        if grep -q "fastapi" requirements.txt; then
            echo "fastapi"
        elif grep -q "django" requirements.txt; then
            echo "django"
        elif grep -q "flask" requirements.txt; then
            echo "flask"
        fi
    fi
}

FRAMEWORK=$(detect_framework)

if [ -z "$FRAMEWORK" ]; then
    echo "❌ No supported framework detected"
    echo ""
    echo "Supported frameworks:"
    echo "  Frontend: React, Vue, Next.js, Angular, Svelte"
    echo "  Backend: Express, Fastify, NestJS, FastAPI, Django, Flask"
    exit 1
fi

echo "✓ Detected framework: $FRAMEWORK"

# Parse arguments
COMPONENT_NAME="${1:-MyComponent}"
COMPONENT_TYPE="${2:-component}"

echo "  Name: $COMPONENT_NAME"
echo "  Type: $COMPONENT_TYPE"
```

## Phase 2: React Component Boilerplate

```typescript
// React component with TypeScript
import React, { useState, useEffect } from 'react';
import styles from './${COMPONENT_NAME}.module.css';

/**
 * Props for ${COMPONENT_NAME} component
 */
interface ${COMPONENT_NAME}Props {
  /**
   * Component title
   */
  title?: string;

  /**
   * Additional CSS classes
   */
  className?: string;

  /**
   * Event handler when component is clicked
   */
  onClick?: () => void;
}

/**
 * ${COMPONENT_NAME} component
 *
 * @example
 * ```tsx
 * <${COMPONENT_NAME} title="Hello" onClick={() => console.log('clicked')} />
 * ```
 */
export const ${COMPONENT_NAME}: React.FC<${COMPONENT_NAME}Props> = ({
  title = 'Default Title',
  className,
  onClick,
}) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    // Component mounted
    console.log('${COMPONENT_NAME} mounted');

    return () => {
      // Component unmounted
      console.log('${COMPONENT_NAME} unmounted');
    };
  }, []);

  const handleClick = () => {
    setCount((prev) => prev + 1);
    onClick?.();
  };

  return (
    <div className={`${styles.container} ${className || ''}`}>
      <h2>{title}</h2>
      <p>Count: {count}</p>
      <button onClick={handleClick}>Increment</button>
    </div>
  );
};

export default ${COMPONENT_NAME};
```

```css
/* ${COMPONENT_NAME}.module.css */
.container {
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.container h2 {
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
}

.container button {
  padding: 0.5rem 1rem;
  background-color: #0070f3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.container button:hover {
  background-color: #0051cc;
}
```

```typescript
// ${COMPONENT_NAME}.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ${COMPONENT_NAME} } from './${COMPONENT_NAME}';

describe('${COMPONENT_NAME}', () => {
  it('renders with default props', () => {
    render(<${COMPONENT_NAME} />);
    expect(screen.getByText('Default Title')).toBeInTheDocument();
  });

  it('renders with custom title', () => {
    render(<${COMPONENT_NAME} title="Custom Title" />);
    expect(screen.getByText('Custom Title')).toBeInTheDocument();
  });

  it('increments count on button click', () => {
    render(<${COMPONENT_NAME} />);
    const button = screen.getByRole('button', { name: /increment/i });

    expect(screen.getByText('Count: 0')).toBeInTheDocument();
    fireEvent.click(button);
    expect(screen.getByText('Count: 1')).toBeInTheDocument();
  });

  it('calls onClick handler when clicked', () => {
    const handleClick = jest.fn();
    render(<${COMPONENT_NAME} onClick={handleClick} />);

    const button = screen.getByRole('button', { name: /increment/i });
    fireEvent.click(button);

    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

## Phase 3: Next.js Page/Route Boilerplate

```typescript
// Next.js App Router page
import { Metadata } from 'next';
import { ${COMPONENT_NAME} } from '@/components/${COMPONENT_NAME}';

/**
 * Page metadata
 */
export const metadata: Metadata = {
  title: '${COMPONENT_NAME}',
  description: '${COMPONENT_NAME} page description',
};

/**
 * ${COMPONENT_NAME} page component
 */
export default async function ${COMPONENT_NAME}Page() {
  // Server-side data fetching
  const data = await fetchData();

  return (
    <div>
      <h1>${COMPONENT_NAME}</h1>
      <${COMPONENT_NAME} data={data} />
    </div>
  );
}

/**
 * Fetch data on the server
 */
async function fetchData() {
  // Fetch data from API or database
  const res = await fetch('https://api.example.com/data', {
    next: { revalidate: 3600 }, // Revalidate every hour
  });

  if (!res.ok) {
    throw new Error('Failed to fetch data');
  }

  return res.json();
}
```

```typescript
// Next.js API Route
import { NextRequest, NextResponse } from 'next/server';

/**
 * GET /api/${COMPONENT_NAME}
 */
export async function GET(request: NextRequest) {
  try {
    // Get query parameters
    const searchParams = request.nextUrl.searchParams;
    const id = searchParams.get('id');

    // Fetch data
    const data = await fetchData(id);

    return NextResponse.json({
      success: true,
      data,
    });
  } catch (error) {
    console.error('${COMPONENT_NAME} GET error:', error);
    return NextResponse.json(
      { success: false, error: 'Internal server error' },
      { status: 500 }
    );
  }
}

/**
 * POST /api/${COMPONENT_NAME}
 */
export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate request body
    if (!body.name) {
      return NextResponse.json(
        { success: false, error: 'Name is required' },
        { status: 400 }
      );
    }

    // Process data
    const result = await createData(body);

    return NextResponse.json({
      success: true,
      data: result,
    }, { status: 201 });
  } catch (error) {
    console.error('${COMPONENT_NAME} POST error:', error);
    return NextResponse.json(
      { success: false, error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## Phase 4: Express Route Boilerplate

```typescript
// Express route handler
import { Router, Request, Response, NextFunction } from 'express';
import { body, param, validationResult } from 'express-validator';

const router = Router();

/**
 * ${COMPONENT_NAME} interface
 */
interface ${COMPONENT_NAME} {
  id: string;
  name: string;
  createdAt: Date;
}

/**
 * GET /api/${COMPONENT_NAME}
 * List all ${COMPONENT_NAME}s
 */
router.get(
  '/',
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { page = 1, limit = 10, search } = req.query;

      // Fetch data from database
      const items = await db.${COMPONENT_NAME}.findMany({
        where: search ? { name: { contains: search as string } } : {},
        skip: (Number(page) - 1) * Number(limit),
        take: Number(limit),
      });

      const total = await db.${COMPONENT_NAME}.count();

      res.json({
        data: items,
        pagination: {
          page: Number(page),
          limit: Number(limit),
          total,
          totalPages: Math.ceil(total / Number(limit)),
        },
      });
    } catch (error) {
      next(error);
    }
  }
);

/**
 * GET /api/${COMPONENT_NAME}/:id
 * Get ${COMPONENT_NAME} by ID
 */
router.get(
  '/:id',
  param('id').isUUID(),
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const item = await db.${COMPONENT_NAME}.findUnique({
        where: { id: req.params.id },
      });

      if (!item) {
        return res.status(404).json({ error: '${COMPONENT_NAME} not found' });
      }

      res.json({ data: item });
    } catch (error) {
      next(error);
    }
  }
);

/**
 * POST /api/${COMPONENT_NAME}
 * Create new ${COMPONENT_NAME}
 */
router.post(
  '/',
  body('name').isString().trim().isLength({ min: 1, max: 255 }),
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const item = await db.${COMPONENT_NAME}.create({
        data: {
          name: req.body.name,
        },
      });

      res.status(201).json({ data: item });
    } catch (error) {
      next(error);
    }
  }
);

/**
 * PUT /api/${COMPONENT_NAME}/:id
 * Update ${COMPONENT_NAME}
 */
router.put(
  '/:id',
  param('id').isUUID(),
  body('name').isString().trim().isLength({ min: 1, max: 255 }),
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      const item = await db.${COMPONENT_NAME}.update({
        where: { id: req.params.id },
        data: { name: req.body.name },
      });

      res.json({ data: item });
    } catch (error) {
      next(error);
    }
  }
);

/**
 * DELETE /api/${COMPONENT_NAME}/:id
 * Delete ${COMPONENT_NAME}
 */
router.delete(
  '/:id',
  param('id').isUUID(),
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ errors: errors.array() });
      }

      await db.${COMPONENT_NAME}.delete({
        where: { id: req.params.id },
      });

      res.status(204).send();
    } catch (error) {
      next(error);
    }
  }
);

export default router;
```

## Phase 5: FastAPI Route Boilerplate

```python
# FastAPI route handler
from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/api/${COMPONENT_NAME}",
    tags=["${COMPONENT_NAME}"],
)

class ${COMPONENT_NAME}Base(BaseModel):
    """Base ${COMPONENT_NAME} schema"""
    name: str = Field(..., min_length=1, max_length=255)

class ${COMPONENT_NAME}Create(${COMPONENT_NAME}Base):
    """Schema for creating ${COMPONENT_NAME}"""
    pass

class ${COMPONENT_NAME}Update(${COMPONENT_NAME}Base):
    """Schema for updating ${COMPONENT_NAME}"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)

class ${COMPONENT_NAME}InDB(${COMPONENT_NAME}Base):
    """Schema for ${COMPONENT_NAME} in database"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    """Paginated response schema"""
    data: List[${COMPONENT_NAME}InDB]
    total: int
    page: int
    page_size: int
    total_pages: int

@router.get("/", response_model=PaginatedResponse)
async def list_${COMPONENT_NAME}s(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
):
    """
    List all ${COMPONENT_NAME}s with pagination

    Args:
        page: Page number (default: 1)
        page_size: Items per page (default: 10, max: 100)
        search: Optional search query

    Returns:
        Paginated list of ${COMPONENT_NAME}s
    """
    try:
        # Query database
        skip = (page - 1) * page_size
        query = db.query(${COMPONENT_NAME})

        if search:
            query = query.filter(${COMPONENT_NAME}.name.contains(search))

        total = query.count()
        items = query.offset(skip).limit(page_size).all()

        return PaginatedResponse(
            data=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=${COMPONENT_NAME}InDB)
async def get_${COMPONENT_NAME}(
    id: str = Path(..., description="${COMPONENT_NAME} ID"),
):
    """
    Get ${COMPONENT_NAME} by ID

    Args:
        id: ${COMPONENT_NAME} unique identifier

    Returns:
        ${COMPONENT_NAME} object

    Raises:
        HTTPException: 404 if ${COMPONENT_NAME} not found
    """
    item = db.query(${COMPONENT_NAME}).filter(${COMPONENT_NAME}.id == id).first()

    if not item:
        raise HTTPException(status_code=404, detail="${COMPONENT_NAME} not found")

    return item

@router.post("/", response_model=${COMPONENT_NAME}InDB, status_code=201)
async def create_${COMPONENT_NAME}(
    data: ${COMPONENT_NAME}Create,
):
    """
    Create new ${COMPONENT_NAME}

    Args:
        data: ${COMPONENT_NAME} creation data

    Returns:
        Created ${COMPONENT_NAME} object
    """
    try:
        item = ${COMPONENT_NAME}(
            id=str(uuid.uuid4()),
            name=data.name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}", response_model=${COMPONENT_NAME}InDB)
async def update_${COMPONENT_NAME}(
    id: str = Path(..., description="${COMPONENT_NAME} ID"),
    data: ${COMPONENT_NAME}Update = None,
):
    """
    Update ${COMPONENT_NAME}

    Args:
        id: ${COMPONENT_NAME} unique identifier
        data: Update data

    Returns:
        Updated ${COMPONENT_NAME} object

    Raises:
        HTTPException: 404 if ${COMPONENT_NAME} not found
    """
    item = db.query(${COMPONENT_NAME}).filter(${COMPONENT_NAME}.id == id).first()

    if not item:
        raise HTTPException(status_code=404, detail="${COMPONENT_NAME} not found")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    item.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{id}", status_code=204)
async def delete_${COMPONENT_NAME}(
    id: str = Path(..., description="${COMPONENT_NAME} ID"),
):
    """
    Delete ${COMPONENT_NAME}

    Args:
        id: ${COMPONENT_NAME} unique identifier

    Raises:
        HTTPException: 404 if ${COMPONENT_NAME} not found
    """
    item = db.query(${COMPONENT_NAME}).filter(${COMPONENT_NAME}.id == id).first()

    if not item:
        raise HTTPException(status_code=404, detail="${COMPONENT_NAME} not found")

    db.delete(item)
    db.commit()
    return None
```

## Summary

```bash
echo ""
echo "=== ✓ Boilerplate Generation Complete ==="
echo ""
echo "📁 Generated files for $FRAMEWORK:"

case $FRAMEWORK in
    react)
        echo "  - src/components/${COMPONENT_NAME}/${COMPONENT_NAME}.tsx"
        echo "  - src/components/${COMPONENT_NAME}/${COMPONENT_NAME}.module.css"
        echo "  - src/components/${COMPONENT_NAME}/${COMPONENT_NAME}.test.tsx"
        ;;
    nextjs)
        echo "  - app/${COMPONENT_NAME}/page.tsx"
        echo "  - app/api/${COMPONENT_NAME}/route.ts"
        ;;
    express)
        echo "  - src/routes/${COMPONENT_NAME}.routes.ts"
        echo "  - src/controllers/${COMPONENT_NAME}.controller.ts"
        ;;
    fastapi)
        echo "  - app/routes/${COMPONENT_NAME}.py"
        echo "  - app/schemas/${COMPONENT_NAME}.py"
        ;;
esac

echo ""
echo "✓ Includes:"
echo "  - TypeScript/type definitions"
echo "  - Input validation"
echo "  - Error handling"
echo "  - JSDoc/docstrings"
echo "  - Unit tests"
echo ""
echo "🚀 Next steps:"
echo "  1. Review and customize generated code"
echo "  2. Update business logic"
echo "  3. Add database integration"
echo "  4. Run tests: npm test"
```

## Best Practices

**Code Quality:**
- Follow framework conventions
- Include comprehensive types
- Add proper error handling
- Write meaningful documentation

**Integration Points:**
- `/test` - Generate tests for boilerplate
- `/scaffold` - Complete feature scaffolding
- `/inline-docs` - Add documentation

## What I'll Actually Do

1. **Detect framework** - Identify project type
2. **Parse arguments** - Component name and type
3. **Generate boilerplate** - Framework-specific code
4. **Include tests** - Unit/integration tests
5. **Add documentation** - JSDoc/docstrings
6. **Follow conventions** - Framework best practices

**Important:** I will NEVER add AI attribution.

**Credits:** Boilerplate patterns based on Create React App, Next.js, Express.js, FastAPI, and framework documentation best practices.
