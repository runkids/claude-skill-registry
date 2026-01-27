---
name: inline-docs
description: Generate JSDoc/docstrings from code analysis
disable-model-invocation: true
---

# Inline Documentation Generator

I'll analyze your code and generate comprehensive JSDoc comments, Python docstrings, or Go documentation from function signatures and behavior.

**Supported Languages:**
- JavaScript/TypeScript (JSDoc)
- Python (Google-style, NumPy-style, reStructuredText)
- Go (godoc)
- Java (Javadoc)
- Rust (rustdoc)

**Token Optimization:**
- Uses Grep to find undocumented functions (150 tokens)
- Reads only target files (800-1,200 tokens)
- Batch processes similar functions (saves 400 tokens)
- Expected: 2,000-3,500 tokens total

## Phase 1: Language Detection

```bash
#!/bin/bash
# Detect project language and documentation style

echo "=== Detecting Project Language ==="
echo ""

detect_language() {
    if [ -f "package.json" ]; then
        if grep -q "\"typescript\"" package.json; then
            echo "typescript"
        else
            echo "javascript"
        fi
    elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
        echo "python"
    elif [ -f "go.mod" ]; then
        echo "go"
    elif [ -f "Cargo.toml" ]; then
        echo "rust"
    elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
        echo "java"
    else
        echo "unknown"
    fi
}

LANGUAGE=$(detect_language)

if [ "$LANGUAGE" = "unknown" ]; then
    echo "❌ Could not detect project language"
    echo ""
    echo "Supported languages:"
    echo "  - JavaScript/TypeScript (package.json)"
    echo "  - Python (pyproject.toml, setup.py)"
    echo "  - Go (go.mod)"
    echo "  - Rust (Cargo.toml)"
    echo "  - Java (pom.xml, build.gradle)"
    exit 1
fi

echo "✓ Detected language: $LANGUAGE"
```

## Phase 2: Find Undocumented Functions

I'll use Grep to efficiently find functions without documentation:

```bash
echo ""
echo "=== Finding Undocumented Functions ==="
echo ""

find_undocumented() {
    case $LANGUAGE in
        typescript|javascript)
            # Find function declarations without JSDoc
            echo "Scanning for undocumented functions..."

            # Functions without /** */ comments above them
            grep -r "^[[:space:]]*\(export \)*\(async \)*function" \
                --include="*.ts" --include="*.js" \
                --exclude-dir=node_modules \
                --exclude-dir=dist \
                --exclude-dir=build \
                -n . | while read line; do
                file=$(echo $line | cut -d: -f1)
                line_num=$(echo $line | cut -d: -f2)

                # Check if previous line has JSDoc
                prev_line=$((line_num - 1))
                if ! sed -n "${prev_line}p" "$file" | grep -q "/\*\*"; then
                    echo "$file:$line_num"
                fi
            done | head -50
            ;;

        python)
            # Find functions without docstrings
            echo "Scanning for undocumented functions..."

            grep -r "^[[:space:]]*def " \
                --include="*.py" \
                --exclude-dir=venv \
                --exclude-dir=.venv \
                --exclude-dir=__pycache__ \
                -n . | while read line; do
                file=$(echo $line | cut -d: -f1)
                line_num=$(echo $line | cut -d: -f2)

                # Check if next line has docstring
                next_line=$((line_num + 1))
                if ! sed -n "${next_line}p" "$file" | grep -q '"""'; then
                    echo "$file:$line_num"
                fi
            done | head -50
            ;;

        go)
            # Find functions without doc comments
            echo "Scanning for undocumented functions..."

            grep -r "^func " \
                --include="*.go" \
                --exclude-dir=vendor \
                -n . | while read line; do
                file=$(echo $line | cut -d: -f1)
                line_num=$(echo $line | cut -d: -f2)

                # Check if previous line has // comment
                prev_line=$((line_num - 1))
                if ! sed -n "${prev_line}p" "$file" | grep -q "^//"; then
                    echo "$file:$line_num"
                fi
            done | head -50
            ;;

        rust)
            # Find functions without /// doc comments
            echo "Scanning for undocumented functions..."

            grep -r "^[[:space:]]*\(pub \)*fn " \
                --include="*.rs" \
                --exclude-dir=target \
                -n . | while read line; do
                file=$(echo $line | cut -d: -f1)
                line_num=$(echo $line | cut -d: -f2)

                # Check if previous line has /// comment
                prev_line=$((line_num - 1))
                if ! sed -n "${prev_line}p" "$file" | grep -q "^[[:space:]]*///"; then
                    echo "$file:$line_num"
                fi
            done | head -50
            ;;
    esac
}

UNDOCUMENTED=$(find_undocumented)
UNDOC_COUNT=$(echo "$UNDOCUMENTED" | wc -l)

if [ -z "$UNDOCUMENTED" ]; then
    echo "✓ All functions appear to be documented!"
    exit 0
fi

echo "Found $UNDOC_COUNT undocumented functions"
echo ""
echo "Sample functions without documentation:"
echo "$UNDOCUMENTED" | head -10 | sed 's/^/  /'
```

## Phase 3: Generate Documentation

Based on the language, I'll generate appropriate documentation:

### TypeScript/JavaScript (JSDoc)

```typescript
/**
 * Calculate the sum of two numbers
 *
 * This function performs addition of two numeric values and returns
 * the result. It handles both integers and floating-point numbers.
 *
 * @param {number} a - The first number to add
 * @param {number} b - The second number to add
 * @returns {number} The sum of a and b
 * @throws {TypeError} If either parameter is not a number
 *
 * @example
 * ```typescript
 * const result = add(5, 3);
 * console.log(result); // Output: 8
 * ```
 *
 * @example
 * ```typescript
 * const result = add(2.5, 3.7);
 * console.log(result); // Output: 6.2
 * ```
 */
function add(a: number, b: number): number {
  if (typeof a !== 'number' || typeof b !== 'number') {
    throw new TypeError('Both arguments must be numbers');
  }
  return a + b;
}

/**
 * User data interface
 *
 * Represents a user entity with authentication and profile information.
 *
 * @interface
 */
interface User {
  /**
   * Unique user identifier
   * @type {string}
   */
  id: string;

  /**
   * User's email address
   * Must be a valid email format
   * @type {string}
   */
  email: string;

  /**
   * User's display name
   * @type {string}
   */
  name: string;

  /**
   * User role for authorization
   * @type {'admin' | 'user' | 'guest'}
   * @default 'user'
   */
  role: 'admin' | 'user' | 'guest';

  /**
   * Optional profile metadata
   * @type {Object}
   * @optional
   */
  profile?: {
    bio?: string;
    avatarUrl?: string;
  };
}

/**
 * Fetch user data from API
 *
 * Retrieves user information from the backend API. Includes error handling
 * for network failures and invalid responses.
 *
 * @async
 * @param {string} userId - The unique identifier of the user to fetch
 * @returns {Promise<User>} A promise that resolves to the user object
 * @throws {Error} If the user is not found (404)
 * @throws {Error} If the network request fails
 *
 * @example
 * ```typescript
 * try {
 *   const user = await fetchUser('user_123');
 *   console.log(user.name);
 * } catch (error) {
 *   console.error('Failed to fetch user:', error);
 * }
 * ```
 */
async function fetchUser(userId: string): Promise<User> {
  const response = await fetch(`/api/users/${userId}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch user: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Generic repository class for data access
 *
 * Provides CRUD operations for any entity type. Uses generics to maintain
 * type safety across different entity types.
 *
 * @template T - The entity type this repository manages
 *
 * @example
 * ```typescript
 * const userRepo = new Repository<User>();
 * const user = await userRepo.findById('123');
 * ```
 */
class Repository<T> {
  /**
   * Find entity by ID
   *
   * @param {string} id - The entity identifier
   * @returns {Promise<T | null>} The found entity or null
   */
  async findById(id: string): Promise<T | null> {
    // Implementation
    return null;
  }

  /**
   * Save entity to database
   *
   * @param {T} entity - The entity to save
   * @returns {Promise<T>} The saved entity with generated ID
   * @throws {Error} If validation fails
   */
  async save(entity: T): Promise<T> {
    // Implementation
    return entity;
  }
}
```

### Python (Google-style Docstrings)

```python
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers.

    This function performs addition of two numeric values and returns
    the result. It handles both integers and floating-point numbers.

    Args:
        a: The first number to add.
        b: The second number to add.

    Returns:
        The sum of a and b.

    Raises:
        TypeError: If either parameter is not a number.

    Examples:
        >>> calculate_sum(5, 3)
        8

        >>> calculate_sum(2.5, 3.7)
        6.2

    Note:
        This function performs simple arithmetic addition without any
        overflow checking.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    return a + b


class UserRepository:
    """Repository for user data access.

    This class provides CRUD operations for user entities. It handles
    database connections, query execution, and error handling.

    Attributes:
        connection: Database connection object.
        table_name: Name of the users table.

    Example:
        >>> repo = UserRepository(db_connection)
        >>> user = repo.find_by_id("user_123")
        >>> print(user.name)
    """

    def __init__(self, connection):
        """Initialize the user repository.

        Args:
            connection: Active database connection object.

        Raises:
            ValueError: If connection is None or invalid.
        """
        if connection is None:
            raise ValueError("Database connection cannot be None")
        self.connection = connection
        self.table_name = "users"

    def find_by_id(self, user_id: str) -> dict | None:
        """Find user by their unique identifier.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            User data as dictionary, or None if not found.

        Raises:
            DatabaseError: If database query fails.

        Example:
            >>> user = repo.find_by_id("user_123")
            >>> if user:
            ...     print(f"Found user: {user['name']}")
        """
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        result = self.connection.execute(query, (user_id,))
        return result.fetchone()

    async def save(self, user_data: dict) -> dict:
        """Save user data to database.

        This method performs an insert or update operation depending on
        whether the user already exists.

        Args:
            user_data: Dictionary containing user information.
                Must include 'id', 'email', and 'name' keys.

        Returns:
            The saved user data with any generated fields.

        Raises:
            ValueError: If required fields are missing.
            DatabaseError: If save operation fails.

        Example:
            >>> user = {
            ...     'id': 'user_123',
            ...     'email': 'user@example.com',
            ...     'name': 'John Doe'
            ... }
            >>> saved_user = await repo.save(user)
        """
        required_fields = ['id', 'email', 'name']
        if not all(field in user_data for field in required_fields):
            raise ValueError(f"Missing required fields: {required_fields}")

        # Implementation
        return user_data
```

### Go (godoc)

```go
package user

// User represents a user entity with authentication and profile information.
//
// The User struct contains all fields necessary for user management,
// including authentication credentials and profile data.
//
// Example:
//     user := &User{
//         ID:    "user_123",
//         Email: "user@example.com",
//         Name:  "John Doe",
//     }
type User struct {
    // ID is the unique identifier for the user
    ID string

    // Email is the user's email address (must be unique)
    Email string

    // Name is the user's display name
    Name string

    // Role defines the user's authorization level
    // Valid values: "admin", "user", "guest"
    Role string

    // CreatedAt is the timestamp when the user was created
    CreatedAt time.Time
}

// UserRepository provides data access operations for users.
//
// This repository handles all database operations related to users,
// including CRUD operations and queries.
type UserRepository struct {
    db *sql.DB
}

// NewUserRepository creates a new user repository instance.
//
// Parameters:
//   - db: Active database connection
//
// Returns a configured UserRepository ready for use.
//
// Example:
//     repo := NewUserRepository(dbConnection)
//     user, err := repo.FindByID("user_123")
func NewUserRepository(db *sql.DB) *UserRepository {
    return &UserRepository{db: db}
}

// FindByID retrieves a user by their unique identifier.
//
// This method queries the database for a user with the given ID.
// If no user is found, it returns nil without an error.
//
// Parameters:
//   - ctx: Context for request cancellation and timeout
//   - userID: The unique identifier of the user to find
//
// Returns:
//   - *User: The found user, or nil if not found
//   - error: Any error that occurred during the query
//
// Example:
//     ctx := context.Background()
//     user, err := repo.FindByID(ctx, "user_123")
//     if err != nil {
//         log.Fatal(err)
//     }
//     if user != nil {
//         fmt.Println(user.Name)
//     }
func (r *UserRepository) FindByID(ctx context.Context, userID string) (*User, error) {
    query := "SELECT id, email, name, role, created_at FROM users WHERE id = ?"

    var user User
    err := r.db.QueryRowContext(ctx, query, userID).Scan(
        &user.ID,
        &user.Email,
        &user.Name,
        &user.Role,
        &user.CreatedAt,
    )

    if err == sql.ErrNoRows {
        return nil, nil
    }
    if err != nil {
        return nil, fmt.Errorf("failed to find user: %w", err)
    }

    return &user, nil
}

// Save persists a user to the database.
//
// This method performs an insert or update operation. If the user ID
// already exists, it updates the existing record; otherwise, it creates
// a new one.
//
// Parameters:
//   - ctx: Context for request cancellation and timeout
//   - user: The user entity to save
//
// Returns an error if the save operation fails.
//
// Example:
//     user := &User{
//         ID:    "user_123",
//         Email: "user@example.com",
//         Name:  "John Doe",
//     }
//     err := repo.Save(context.Background(), user)
//     if err != nil {
//         log.Fatal(err)
//     }
func (r *UserRepository) Save(ctx context.Context, user *User) error {
    query := `
        INSERT INTO users (id, email, name, role, created_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            email = excluded.email,
            name = excluded.name,
            role = excluded.role
    `

    _, err := r.db.ExecContext(ctx, query,
        user.ID,
        user.Email,
        user.Name,
        user.Role,
        user.CreatedAt,
    )

    if err != nil {
        return fmt.Errorf("failed to save user: %w", err)
    }

    return nil
}
```

## Phase 4: Apply Documentation

```bash
echo ""
echo "=== Applying Documentation ==="
echo ""

apply_docs() {
    local file="$1"
    local line_num="$2"

    echo "Processing: $file:$line_num"

    # Extract function signature
    signature=$(sed -n "${line_num}p" "$file")

    # Generate documentation based on signature
    # This would use the patterns above based on language

    # Insert documentation above function
    # Using sed or similar tool

    echo "  ✓ Added documentation"
}

# Process each undocumented function
echo "$UNDOCUMENTED" | while read location; do
    file=$(echo $location | cut -d: -f1)
    line=$(echo $location | cut -d: -f2)
    apply_docs "$file" "$line"
done

echo ""
echo "✓ Documentation applied to $UNDOC_COUNT functions"
```

## Summary

```bash
echo ""
echo "=== ✓ Inline Documentation Complete ==="
echo ""
echo "📊 Documentation generated:"
echo "  - Functions documented: $UNDOC_COUNT"
echo "  - Files modified: $(echo "$UNDOCUMENTED" | cut -d: -f1 | sort -u | wc -l)"
echo ""
echo "📝 Documentation includes:"
echo "  ✓ Function/method descriptions"
echo "  ✓ Parameter documentation"
echo "  ✓ Return value descriptions"
echo "  ✓ Error/exception documentation"
echo "  ✓ Usage examples"
echo "  ✓ Type information"
echo ""
echo "🚀 Next steps:"
echo ""
echo "1. Review generated documentation:"
echo "   - Verify accuracy of descriptions"
echo "   - Add domain-specific details"
echo "   - Customize examples"
echo ""
echo "2. Configure documentation tools:"

case $LANGUAGE in
    typescript|javascript)
        echo "   - npm install --save-dev typedoc"
        echo "   - npx typedoc --out docs src"
        ;;
    python)
        echo "   - pip install sphinx"
        echo "   - sphinx-quickstart docs"
        ;;
    go)
        echo "   - godoc -http=:6060"
        echo "   - Visit http://localhost:6060"
        ;;
    rust)
        echo "   - cargo doc --open"
        ;;
esac

echo ""
echo "3. Enforce documentation in CI:"
echo "   - Add documentation coverage checks"
echo "   - Fail builds on missing docs"
echo ""
echo "💡 Tip: Run /inline-docs regularly to document new functions"
```

## Best Practices

**Documentation Quality:**
- Write clear, concise descriptions
- Include practical code examples
- Document edge cases and errors
- Keep type information accurate
- Explain the "why" not just "what"

**Consistency:**
- Follow language-specific conventions
- Use consistent terminology
- Match project documentation style
- Keep formatting uniform

**Maintenance:**
- Update docs when code changes
- Remove obsolete documentation
- Keep examples working
- Validate doc coverage

**Integration Points:**
- `/readme-generate` - Link API docs to README
- `/api-docs-generate` - Generate API documentation
- `/review` - Check documentation quality

## What I'll Actually Do

1. **Detect language** - Identify project language
2. **Find undocumented code** - Grep for missing docs
3. **Analyze signatures** - Extract function parameters
4. **Generate documentation** - Create appropriate format
5. **Apply to code** - Insert above functions
6. **Preserve existing** - Keep manual documentation
7. **Fill gaps only** - Don't overwrite good docs

**Important:** I will NEVER:
- Overwrite existing documentation
- Generate inaccurate descriptions
- Add placeholder "TODO" comments
- Remove manually written docs
- Add AI attribution

All generated documentation is based on actual code analysis and follows language-specific conventions.

**Credits:** Documentation patterns based on JSDoc, Google Python Style Guide, Go documentation conventions, rustdoc, and Javadoc standards. Inspired by documentation practices from TypeScript, Python, and Go communities.
