---
name: quality-gates
description: Type safety checks, test requirements, linting, code conventions, validation
---

# Quality Gates — CEI-001

## Pre-Commit Checklist

### Type Safety
- [ ] **No `any` type** in TypeScript/Python
- [ ] **All function parameters typed**
- [ ] **All function returns typed**
- [ ] **Strict tsconfig enabled** (all checks on)
- [ ] **mypy passing** for Python

```bash
# Run checks
npx tsc --noEmit
mypy app/ --ignore-missing-imports
```

### Testing (≥70% coverage)
- [ ] **Unit tests written** for new functions
- [ ] **Happy path tested**
- [ ] **Edge cases covered**
- [ ] **Error scenarios handled**
- [ ] **Coverage ≥70%**

```bash
# Backend
pytest tests/ --cov=app --cov-fail-under=70

# Frontend
npm test -- --coverage --watchAll=false
```

### Code Quality
- [ ] **No unused imports**
- [ ] **No console.log() in production code**
- [ ] **Linter passing** (ruff, eslint)
- [ ] **Code formatted** (black, prettier)

```bash
# Backend
ruff check app/
black app/
mypy app/

# Frontend
eslint src/
prettier --write src/
```

### Conventions
- [ ] **Route patterns** follow `/api/[resource]/[action]`
- [ ] **File naming** consistent (PascalCase components, snake_case functions)
- [ ] **Database** uses migrations (Alembic)
- [ ] **Relationships** use back_populates
- [ ] **Error messages** are helpful (not generic)
- [ ] **API responses** use status codes correctly

### Documentation
- [ ] **Docstrings present** on all public functions
- [ ] **Example included** in docstrings
- [ ] **Complex logic explained**
- [ ] **Comments only for "why", not "what"**

```python
# Good docstring
async def create_evaluation(eval_data: EvaluationCreate) -> Evaluation:
    """
    Create new evaluation session for user.
    
    Args:
        eval_data: Evaluation creation data
    
    Returns:
        Created evaluation with all fields
    
    Example:
        >>> eval = await create_evaluation(
        ...     EvaluationCreate(company_id="123", project_type="new")
        ... )
    """
    ...
```

## Test Requirements

### Backend (pytest)
```python
# tests/test_evaluation_service.py
import pytest
from app.services.evaluation_service import EvaluationService

@pytest.mark.asyncio
async def test_create_evaluation():
    """Test creating evaluation"""
    # Arrange
    service = EvaluationService(db)
    data = EvaluationCreate(company_id="123")
    
    # Act
    result = await service.create("user123", data)
    
    # Assert
    assert result.id is not None
    assert result.user_id == "user123"
    assert result.status == "in_progress"

@pytest.mark.asyncio
async def test_create_evaluation_missing_user():
    """Test error when user not found"""
    # Arrange
    service = EvaluationService(db)
    
    # Act & Assert
    with pytest.raises(ValueError, match="User not found"):
        await service.create("nonexistent", EvaluationCreate(...))
```

### Frontend (Jest)
```typescript
// src/__tests__/components/ChatWindow.test.tsx
import { render, screen } from '@testing-library/react';
import { ChatWindow } from '@/components/chat/ChatWindow';

describe('ChatWindow', () => {
  it('renders message input', () => {
    render(<ChatWindow />);
    const input = screen.getByPlaceholderText('Posez votre question...');
    expect(input).toBeInTheDocument();
  });

  it('sends message on submit', async () => {
    render(<ChatWindow />);
    const input = screen.getByPlaceholderText('Posez votre question...');
    const button = screen.getByText('Envoyer');
    
    // Type and submit
    await userEvent.type(input, 'Test message');
    await userEvent.click(button);
    
    // Assert
    expect(chatService.sendMessage).toHaveBeenCalledWith(
      expect.objectContaining({ content: 'Test message' })
    );
  });
});
```

## Common Issues & Fixes

| Issue | Fix | Prevention |
|-------|-----|-----------|
| `type: ignore` comments | Add proper types instead | Use strict mode |
| No tests | Write test before fix | Require tests in PR |
| Missing docstring | Add doc with example | Linter check |
| Hardcoded values | Move to config/constants | Code review |
| Circular imports | Reorganize imports | Linter check |
| Unused variables | Remove them | noUnusedLocals: true |
| Silent errors | Add explicit error handling | Type checking |
| `any` type used | Replace with specific type | No any rule |

## Auto-fix Commands

```bash
# Format all code
black app/
prettier --write src/

# Fix linter issues
ruff check --fix app/
eslint --fix src/

# Check compliance
npm run type-check
npm run lint
npm test -- --coverage
```

## CI/CD Pipeline

```yaml
# .github/workflows/quality.yml
name: Quality Gates
on: [pull_request]

jobs:
  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install
      - run: npx tsc --noEmit
      - run: pip install mypy
      - run: mypy app/

  tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install && npm test -- --coverage --watchAll=false
      - run: pip install pytest-cov && pytest --cov=app --cov-fail-under=70

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run lint
      - run: pip install ruff && ruff check app/
```

---

---
name: project-workflow
description: Workflows for new features, debugging, code review, migrations, RAG updates
---

# Project Workflows — CEI-001

## Workflow 1: New Feature (Full-stack)

### Input
```
Crée composant Chat pour le module d'évaluation
```

### Steps

#### 1. Design (5 min)
- [ ] Review requirements
- [ ] Sketch component structure
- [ ] Identify dependencies

#### 2. Database (10 min - if needed)
- [ ] Create model if needed
- [ ] Create migration
- [ ] Test migration locally

#### 3. Backend (15 min)
- [ ] Create/update endpoint
- [ ] Add validation schemas
- [ ] Add service methods
- [ ] Write endpoint docstring

#### 4. Frontend (15 min)
- [ ] Create component file
- [ ] Define prop interfaces
- [ ] Implement component
- [ ] Add custom hook if needed

#### 5. Testing (10 min)
- [ ] Write backend tests (pytest)
- [ ] Write component tests (jest)
- [ ] Run coverage check (≥70%)

#### 6. Validation (5 min)
```bash
# Type check
npm run type-check
mypy app/

# Lint
npm run lint
ruff check app/

# Test
npm test -- --coverage
pytest --cov=app
```

#### 7. Documentation (5 min)
- [ ] Add docstring with example
- [ ] Update README if public API
- [ ] Add component prop docs

#### 8. Ready
```
Valide contre quality-gates
```

---

## Workflow 2: Debug Error

### Input
```
Debug: POST /api/chat/message retourne 500 avec "token limit exceeded"
```

### Steps

#### 1. Identify Layer
- Backend error? → Check `app/api/routes/` logs
- Frontend error? → Check browser console
- Database error? → Check `docker-compose logs postgres`
- Weaviate error? → Check `docker-compose logs weaviate`

#### 2. Find Root Cause
```bash
# Check logs
docker-compose logs backend | grep error

# Check recent changes
git diff HEAD~1

# Test endpoint locally
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}'

# Check database state
docker-compose exec postgres psql
```

#### 3. Propose Fix
- Code change? Use fastapi-backend skill
- Query issue? Use database-design skill
- Frontend issue? Use react-frontend skill
- Weaviate? Use rag-weaviate skill

#### 4. Test Fix
```bash
# Unit test for fix
pytest tests/test_chat_service.py::test_token_limit

# Integration test
curl -X POST http://localhost:8000/api/chat/message ...

# Full test suite
npm test -- --coverage
pytest --cov=app
```

#### 5. Validate
```bash
# Type check
npm run type-check
mypy app/

# Lint
npm run lint

# Coverage
pytest --cov=app --cov-fail-under=70
```

---

## Workflow 3: Code Review

### Pre-PR Checklist
- [ ] Type safety (`tsc --noEmit`, `mypy`)
- [ ] Tests passing (≥70% coverage)
- [ ] Lint clean (eslint, ruff)
- [ ] No console.log in production
- [ ] Docstrings present
- [ ] Error messages helpful
- [ ] No `any` type
- [ ] No hardcoded values
- [ ] Conventions followed

### Review Checklist
- [ ] **Functionality** — Does it work as intended?
- [ ] **Performance** — Any N+1 queries? Unnecessary renders?
- [ ] **Security** — Authentication? Authorization? Input validation?
- [ ] **Maintainability** — Can others understand the code?
- [ ] **Testing** — Is coverage adequate? Edge cases covered?
- [ ] **Documentation** — Are docstrings clear?

### Common Comments
```
❌ "Type hints missing"
✅ "add: async def foo(bar: str) -> bool:"

❌ "No error handling"
✅ "add try/except with specific exception"

❌ "No tests"
✅ "add test_foo() with happy path + edge cases"

❌ "Hardcoded value"
✅ "move to config or constants"
```

---

## Workflow 4: Database Migration

### Input
```
Add column priority (int, nullable) to evaluations table
```

### Steps

#### 1. Update Model
```python
# app/models/evaluation.py
class Evaluation(Base):
    # ... existing columns ...
    priority = Column(Integer, nullable=True, index=True)
```

#### 2. Create Migration
```bash
alembic revision --autogenerate -m "Add priority to evaluations"
```

#### 3. Review Migration
```python
# alembic/versions/xxx_add_priority_to_evaluations.py
def upgrade():
    op.add_column('evaluations', sa.Column('priority', sa.Integer(), nullable=True))
    op.create_index('ix_evaluations_priority', 'evaluations', ['priority'])

def downgrade():
    op.drop_index('ix_evaluations_priority', table_name='evaluations')
    op.drop_column('evaluations', 'priority')
```

#### 4. Test Migration
```bash
# Apply
alembic upgrade head

# Verify
docker-compose exec postgres psql -c "\\d evaluations"

# Rollback
alembic downgrade -1

# Re-apply
alembic upgrade head
```

#### 5. Update ORM Queries
Update any service/route that uses evaluations to handle new column

#### 6. Test Full Suite
```bash
pytest --cov=app --cov-fail-under=70
npm test -- --coverage
```

---

## Workflow 5: Add Document to RAG

### Input
```
Upload Genius documentation PDF and index for RAG
```

### Steps

#### 1. Upload via Admin UI
- Go to `/admin/documents`
- Click "Upload Document"
- Select PDF file
- Fill metadata (title, categories, tags)
- Click "Upload"

#### 2. Configure Pipeline
- Select transformations:
  - [ ] Anonymize
  - [ ] Whitelabel
  - [ ] Normalize
  - [ ] Enrich Summary
  - [ ] Generate Q&A
  - [ ] Segment
- Click "Start Pipeline"

#### 3. Review & Approve
- Admin reviews before/after
- Edit if needed
- Click "Approve"

#### 4. Publish
- Click "Publish to RAG"
- Chunks are indexed in Weaviate

#### 5. Test
```bash
# Verify in Weaviate
curl http://localhost:8080/v1/objects

# Test RAG search
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": "test", "content": "How to implement ERP?"}'

# Should include document in sources
```

---

## Quick Command Reference

```bash
# Development
docker-compose up -d
docker-compose logs -f backend

# Migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1

# Testing
pytest tests/ --cov=app --cov-fail-under=70
npm test -- --coverage --watchAll=false

# Code Quality
black app/ && ruff check --fix app/
prettier --write src/ && eslint --fix src/

# Type Checking
mypy app/ --ignore-missing-imports
npm run type-check
```
