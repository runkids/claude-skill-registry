---
name: Python Best Practices
description: Type hints, dataclasses, async patterns, testing with pytest, and modern Python tooling
keywords:
  - python
  - type-hints
  - async
  - pytest
  - dataclasses
  - pydantic
---

# Python Best Practices

## When to Use

**Perfect for:**
- Data processing and analysis (pandas, numpy)
- Web backends and APIs (FastAPI, Django)
- Automation and scripting
- Machine learning and AI workflows
- DevOps and infrastructure tooling

**Not ideal for:**
- Hard real-time systems (use Rust/C++ instead)
- Mobile app development (use Swift/Kotlin)
- GUI applications (consider Qt, but weigh alternatives)

## Quick Reference

### Type Hints
```python
from typing import Optional, List, Dict, Union, Callable, TypeVar, Generic
from collections.abc import Sequence, Mapping

# Function type hints
def process_items(items: List[str], count: int = 10) -> Dict[str, int]:
    """Process items and return counts."""
    return {item: len(item) for item in items[:count]}

# Optional parameters
def get_user(user_id: int, default: Optional[str] = None) -> Optional[str]:
    return default

# Union types (Python 3.10+ use |)
def handle_value(value: str | int | float) -> str:
    return str(value)

# Callable types
def register_handler(callback: Callable[[int], str]) -> None:
    result = callback(42)

# TypeVar for generics
T = TypeVar('T')

def get_first(items: List[T]) -> T:
    return items[0]

# Type aliases
UserID = int
UserName = str
UserData = Dict[UserID, UserName]
```

### Dataclasses
```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    """User with type hints and validation."""
    id: int
    name: str
    email: str
    age: int = 0
    tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate after initialization."""
        if self.age < 0:
            raise ValueError("Age cannot be negative")

# Usage
user = User(id=1, name="Alice", email="alice@example.com", age=30)
print(user)  # User(id=1, name='Alice', email='alice@example.com', age=30, tags=[])
```

### Pydantic Models
```python
from pydantic import BaseModel, Field, field_validator

class User(BaseModel):
    """User model with validation."""
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(default=0, ge=0, le=150)
    tags: list[str] = Field(default_factory=list)

    @field_validator('name')
    def name_must_be_titlecase(cls, v):
        if not v.istitle():
            raise ValueError('Name must be title case')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "age": 30,
                "tags": ["admin", "user"]
            }
        }

# Usage with validation
try:
    user = User(id=1, name="Alice Smith", email="alice@example.com")
except ValueError as e:
    print(f"Validation error: {e}")

# JSON schema
print(User.model_json_schema())
```

### Async/Await Patterns
```python
import asyncio
from typing import Coroutine

# Basic async function
async def fetch_data(url: str) -> str:
    """Simulate async data fetch."""
    await asyncio.sleep(1)
    return f"Data from {url}"

# Concurrent execution
async def fetch_multiple(urls: list[str]) -> list[str]:
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)

# Async context manager
class Database:
    async def __aenter__(self):
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await asyncio.sleep(0.1)

async def use_db():
    async with Database() as db:
        # Use database
        pass

# Run async code
# asyncio.run(fetch_multiple(['url1', 'url2', 'url3']))
```

### Error Handling
```python
from contextlib import contextmanager
from typing import Generator

# Custom exceptions
class ValidationError(Exception):
    """Raised when validation fails."""
    pass

class DatabaseError(Exception):
    """Raised when database operation fails."""
    pass

# Try/except pattern
def process_data(data: dict) -> str:
    try:
        value = data['key']
        if not isinstance(value, str):
            raise ValidationError("Key must be string")
        return value
    except KeyError:
        raise ValidationError("Missing required key") from None
    except ValidationError:
        raise  # Re-raise validation errors
    except Exception as e:
        raise DatabaseError(f"Unexpected error: {e}") from e

# Context manager for resources
@contextmanager
def managed_resource() -> Generator:
    """Context manager example."""
    resource = None
    try:
        resource = "initialized"
        yield resource
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        print("Cleanup")
```

### Testing with Pytest
```python
import pytest
from unittest.mock import Mock, patch

# Simple test
def test_add():
    assert 2 + 2 == 4

# Parametrized tests
@pytest.mark.parametrize("input,expected", [
    ([1, 2, 3], 6),
    ([0], 0),
    ([-1, 1], 0),
])
def test_sum(input, expected):
    assert sum(input) == expected

# Fixtures
@pytest.fixture
def sample_user():
    return {"id": 1, "name": "Alice"}

def test_user_name(sample_user):
    assert sample_user["name"] == "Alice"

# Async tests
@pytest.mark.asyncio
async def test_async_fetch():
    result = await fetch_data("url")
    assert "url" in result

# Mocking
@patch('requests.get')
def test_with_mock(mock_get):
    mock_get.return_value.text = "mocked"
    result = fetch_url("url")
    assert result == "mocked"

# Exception testing
def test_raises():
    with pytest.raises(ValidationError, match="Invalid"):
        process_data({})
```

## Deep Dive

### Advanced Type Hints
```python
from typing import Protocol, TypedDict, Literal, Final
from abc import ABC, abstractmethod

# Protocol for structural typing
class Drawable(Protocol):
    def draw(self) -> None: ...

# TypedDict for dictionaries with specific structure
class UserDict(TypedDict):
    id: int
    name: str
    email: str

# Literal types for specific values
def set_log_level(level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]) -> None:
    pass

# Final for constants
MAX_RETRIES: Final = 3
MAX_TIMEOUT: Final[int] = 30

# Abstract base classes
class DataSource(ABC):
    @abstractmethod
    def fetch(self, query: str) -> str:
        pass

class APIDataSource(DataSource):
    def fetch(self, query: str) -> str:
        return f"API result: {query}"
```

### Modern Project Structure
```
my_project/
├── pyproject.toml          # Project metadata and dependencies (uv)
├── README.md
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── main.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── conftest.py         # Pytest configuration
│   ├── unit/
│   │   └── test_main.py
│   └── integration/
│       └── test_api.py
└── .gitignore
```

### pyproject.toml Example
```toml
[build-system]
requires = ["setuptools>=68.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "My awesome package"
requires-python = ">=3.9"
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.5.0",
    "ruff>=0.1.0",
]

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.ruff]
line-length = 100
target-version = "py39"
```

### Async Context Managers
```python
class AsyncResource:
    """Async context manager for managing resources."""

    def __init__(self, name: str):
        self.name = name

    async def __aenter__(self):
        print(f"Opening {self.name}")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print(f"Closing {self.name}")
        await asyncio.sleep(0.1)
        if exc_type:
            print(f"Error: {exc_type.__name__}: {exc}")
        return False  # Don't suppress exceptions

async def main():
    async with AsyncResource("MyResource") as resource:
        print(f"Using {resource.name}")
```

### Dependency Injection Pattern
```python
from typing import Protocol
from abc import ABC, abstractmethod

# Define interfaces
class Logger(Protocol):
    def log(self, message: str) -> None: ...

class Repository(ABC):
    @abstractmethod
    async def get(self, id: int) -> dict:
        pass

# Implementations
class ConsoleLogger:
    def log(self, message: str) -> None:
        print(message)

class DatabaseRepository(Repository):
    async def get(self, id: int) -> dict:
        return {"id": id, "name": "Item"}

# Service with dependency injection
class UserService:
    def __init__(self, logger: Logger, repository: Repository):
        self.logger = logger
        self.repository = repository

    async def get_user(self, user_id: int) -> dict:
        self.logger.log(f"Fetching user {user_id}")
        return await self.repository.get(user_id)

# Usage
logger = ConsoleLogger()
repo = DatabaseRepository()
service = UserService(logger, repo)
```

## Anti-Patterns

### DON'T: Skip Type Hints
```python
# Bad - no type information
def process(items, count=10):
    return {item: len(item) for item in items[:count]}

# Good - clear types
def process(items: list[str], count: int = 10) -> dict[str, int]:
    return {item: len(item) for item in items[:count]}
```

### DON'T: Use Bare Except
```python
# Bad - catches all exceptions including KeyboardInterrupt
try:
    do_something()
except:
    pass

# Good - specific exception handling
try:
    do_something()
except ValueError as e:
    print(f"Invalid value: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### DON'T: Modify Loop Variables
```python
# Bad - confusing and error-prone
items = [1, 2, 3]
for i, item in enumerate(items):
    items[i] = item * 2  # Modifying while iterating

# Good - use list comprehension or copy
items = [item * 2 for item in items]
```

### DON'T: Use Mutable Default Arguments
```python
# Bad - default list shared across calls
def append_item(item, items=[]):
    items.append(item)
    return items

# Good - use None and create new list
def append_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### DON'T: Mix Sync and Async Without Care
```python
# Bad - mixing sync and async
async def mixed():
    sync_result = slow_sync_operation()  # Blocks event loop
    await async_operation()

# Good - keep async clean
async def async_only():
    result = await async_fetch()
    processed = await async_process(result)
```

### DON'T: Hardcode Configuration
```python
# Bad - hardcoded values
DATABASE_URL = "postgresql://localhost/mydb"
API_KEY = "sk_live_xxxxx"

# Good - use environment variables
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/mydb")
API_KEY = os.getenv("API_KEY")  # Fail if not set
```
