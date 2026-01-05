---
name: database-design
description: Expert database design and data modeling. Use when designing schemas, normalizing data, creating ER diagrams, or making architectural database decisions.
allowed-tools: Bash, Read, Grep
---

# Database Design Skill

Comprehensive knowledge for designing robust, scalable, and maintainable database schemas for SQL Server.

## Database Design Principles

### 1. Understand the Domain

Before designing:
- Identify all entities (nouns in requirements)
- Identify relationships between entities
- Understand business rules and constraints
- Consider access patterns and query requirements
- Plan for future growth and scalability

### 2. Normalization

Apply normalization to eliminate redundancy and ensure data integrity.

**First Normal Form (1NF)**
- ❌ Violates 1NF: `Products(Id, Name, Tags VARCHAR)` where Tags = "laptop, computer, electronics"
- ✓ Conforms to 1NF: Separate `ProductTags` table with one tag per row

**Second Normal Form (2NF)**
- ❌ Violates 2NF: `OrderItems(OrderId, ProductId, CustomerName)` - CustomerName depends on OrderId, not the composite key
- ✓ Conforms to 2NF: Move CustomerName to Orders table

**Third Normal Form (3NF)**
- ❌ Violates 3NF: `Employees(Id, DepartmentId, DepartmentName)` - DepartmentName depends on DepartmentId (transitive dependency)
- ✓ Conforms to 3NF: Create Departments table with DepartmentName

**Boyce-Codd Normal Form (BCNF)**
- Stricter version of 3NF
- Every determinant must be a candidate key
- Usually achieved when 3NF is properly implemented

### When to Denormalize

Sometimes denormalization is acceptable for:
- **Performance**: Avoid complex joins for frequently accessed data
- **Read-heavy workloads**: Optimize for reads at expense of writes
- **Reporting databases**: Data warehouses often denormalize
- **Caching computed values**: Store aggregates to avoid recalculation

Examples:
- Store CustomerName in Orders for faster order display
- Maintain OrderCount on Customers table
- Store denormalized product details in OrderItems for historical accuracy

## Common Design Patterns

### 1. One-to-Many Relationship

**Example**: Customers → Orders

```sql
CREATE TABLE Customers (
    CustomerId INT IDENTITY(1,1) PRIMARY KEY,
    CustomerName NVARCHAR(100) NOT NULL,
    Email NVARCHAR(255) NOT NULL UNIQUE,
    CreatedAt DATETIME2 DEFAULT GETUTCDATE()
);

CREATE TABLE Orders (
    OrderId INT IDENTITY(1,1) PRIMARY KEY,
    CustomerId INT NOT NULL,
    OrderDate DATETIME2 DEFAULT GETUTCDATE(),
    TotalAmount DECIMAL(10,2) NOT NULL,

    CONSTRAINT FK_Orders_Customers
        FOREIGN KEY (CustomerId)
        REFERENCES Customers(CustomerId)
);

CREATE NONCLUSTERED INDEX IX_Orders_CustomerId
    ON Orders(CustomerId);
```

### 2. Many-to-Many Relationship

**Example**: Students ↔ Courses

```sql
CREATE TABLE Students (
    StudentId INT IDENTITY(1,1) PRIMARY KEY,
    StudentName NVARCHAR(100) NOT NULL
);

CREATE TABLE Courses (
    CourseId INT IDENTITY(1,1) PRIMARY KEY,
    CourseName NVARCHAR(100) NOT NULL
);

-- Junction/Bridge table
CREATE TABLE Enrollments (
    StudentId INT NOT NULL,
    CourseId INT NOT NULL,
    EnrollmentDate DATETIME2 DEFAULT GETUTCDATE(),
    Grade CHAR(2),

    PRIMARY KEY (StudentId, CourseId),

    CONSTRAINT FK_Enrollments_Students
        FOREIGN KEY (StudentId)
        REFERENCES Students(StudentId),

    CONSTRAINT FK_Enrollments_Courses
        FOREIGN KEY (CourseId)
        REFERENCES Courses(CourseId)
);
```

### 3. One-to-One Relationship

**Example**: Users → UserProfiles

```sql
CREATE TABLE Users (
    UserId INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) NOT NULL UNIQUE,
    Email NVARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE UserProfiles (
    UserId INT PRIMARY KEY,  -- PK and FK combined
    Bio NVARCHAR(MAX),
    ProfilePictureUrl NVARCHAR(500),
    DateOfBirth DATE,

    CONSTRAINT FK_UserProfiles_Users
        FOREIGN KEY (UserId)
        REFERENCES Users(UserId)
        ON DELETE CASCADE
);
```

### 4. Self-Referencing Relationship

**Example**: Employees (manager hierarchy)

```sql
CREATE TABLE Employees (
    EmployeeId INT IDENTITY(1,1) PRIMARY KEY,
    EmployeeName NVARCHAR(100) NOT NULL,
    ManagerId INT NULL,  -- References another Employee

    CONSTRAINT FK_Employees_Manager
        FOREIGN KEY (ManagerId)
        REFERENCES Employees(EmployeeId)
);
```

**Example**: Categories (tree structure)

```sql
CREATE TABLE Categories (
    CategoryId INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName NVARCHAR(100) NOT NULL,
    ParentCategoryId INT NULL,

    CONSTRAINT FK_Categories_Parent
        FOREIGN KEY (ParentCategoryId)
        REFERENCES Categories(CategoryId)
);
```

### 5. Polymorphic Associations (Use with Caution)

**Problem**: Multiple entity types sharing a relationship

**Approach 1: Separate Foreign Keys** (Preferred)
```sql
CREATE TABLE Comments (
    CommentId INT IDENTITY(1,1) PRIMARY KEY,
    CommentText NVARCHAR(MAX),
    PostId INT NULL,
    PhotoId INT NULL,

    CONSTRAINT FK_Comments_Posts
        FOREIGN KEY (PostId) REFERENCES Posts(PostId),
    CONSTRAINT FK_Comments_Photos
        FOREIGN KEY (PhotoId) REFERENCES Photos(PhotoId),

    CONSTRAINT CK_Comments_OneParent
        CHECK (
            (PostId IS NOT NULL AND PhotoId IS NULL) OR
            (PostId IS NULL AND PhotoId IS NOT NULL)
        )
);
```

**Approach 2: Supertype/Subtype** (Preferred for similar entities)
```sql
CREATE TABLE Media (
    MediaId INT IDENTITY(1,1) PRIMARY KEY,
    MediaType NVARCHAR(20) NOT NULL,  -- 'Post' or 'Photo'
    CreatedAt DATETIME2 DEFAULT GETUTCDATE()
);

CREATE TABLE Posts (
    MediaId INT PRIMARY KEY,
    Title NVARCHAR(200),
    Content NVARCHAR(MAX),

    CONSTRAINT FK_Posts_Media
        FOREIGN KEY (MediaId) REFERENCES Media(MediaId)
);

CREATE TABLE Photos (
    MediaId INT PRIMARY KEY,
    Url NVARCHAR(500),
    Caption NVARCHAR(500),

    CONSTRAINT FK_Photos_Media
        FOREIGN KEY (MediaId) REFERENCES Media(MediaId)
);

CREATE TABLE Comments (
    CommentId INT IDENTITY(1,1) PRIMARY KEY,
    MediaId INT NOT NULL,
    CommentText NVARCHAR(MAX),

    CONSTRAINT FK_Comments_Media
        FOREIGN KEY (MediaId) REFERENCES Media(MediaId)
);
```

### 6. Audit Pattern

Track who created/modified records and when:

```sql
CREATE TABLE Products (
    ProductId INT IDENTITY(1,1) PRIMARY KEY,
    ProductName NVARCHAR(100) NOT NULL,
    Price DECIMAL(10,2) NOT NULL,

    -- Audit columns
    CreatedAt DATETIME2 DEFAULT GETUTCDATE() NOT NULL,
    CreatedBy INT NOT NULL,
    UpdatedAt DATETIME2,
    UpdatedBy INT,
    IsDeleted BIT DEFAULT 0 NOT NULL,
    DeletedAt DATETIME2,
    DeletedBy INT,

    CONSTRAINT FK_Products_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Users(UserId),
    CONSTRAINT FK_Products_UpdatedBy
        FOREIGN KEY (UpdatedBy) REFERENCES Users(UserId),
    CONSTRAINT FK_Products_DeletedBy
        FOREIGN KEY (DeletedBy) REFERENCES Users(UserId)
);
```

### 7. Temporal Tables (SQL Server 2016+)

Automatic history tracking:

```sql
CREATE TABLE Products (
    ProductId INT PRIMARY KEY,
    ProductName NVARCHAR(100),
    Price DECIMAL(10,2),

    -- System-versioning columns (required)
    ValidFrom DATETIME2 GENERATED ALWAYS AS ROW START NOT NULL,
    ValidTo DATETIME2 GENERATED ALWAYS AS ROW END NOT NULL,
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo)
)
WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.ProductsHistory));

-- Query historical data
SELECT * FROM Products
FOR SYSTEM_TIME AS OF '2024-01-01';

SELECT * FROM Products
FOR SYSTEM_TIME BETWEEN '2024-01-01' AND '2024-12-31';
```

### 8. Type Tables (Lookup Tables)

For enumeration values:

```sql
CREATE TABLE OrderStatuses (
    StatusId INT PRIMARY KEY,  -- Fixed values (1=Pending, 2=Processing, etc.)
    StatusName NVARCHAR(50) NOT NULL UNIQUE,
    DisplayOrder INT NOT NULL
);

INSERT INTO OrderStatuses VALUES
    (1, 'Pending', 1),
    (2, 'Processing', 2),
    (3, 'Shipped', 3),
    (4, 'Delivered', 4),
    (5, 'Cancelled', 5);

CREATE TABLE Orders (
    OrderId INT IDENTITY(1,1) PRIMARY KEY,
    StatusId INT NOT NULL DEFAULT 1,

    CONSTRAINT FK_Orders_Status
        FOREIGN KEY (StatusId)
        REFERENCES OrderStatuses(StatusId)
);
```

## Data Type Selection Guide

### Strings

| Type | Use When |
|------|----------|
| `NVARCHAR(n)` | Unicode text (names, addresses, international content) |
| `VARCHAR(n)` | ASCII-only text (codes, slugs) |
| `NVARCHAR(MAX)` | Large text (descriptions, content) - up to 2GB |
| `CHAR(n)` | Fixed-length codes (country codes: 'US', 'UK') |

**Examples**:
```sql
Email NVARCHAR(255)
CountryCode CHAR(2)
ProductDescription NVARCHAR(MAX)
SKU VARCHAR(50)
```

### Numbers

| Type | Range | Use When |
|------|-------|----------|
| `TINYINT` | 0 to 255 | Small counts, flags (0-255) |
| `SMALLINT` | -32K to 32K | Small integers |
| `INT` | -2.1B to 2.1B | Standard integers (most common) |
| `BIGINT` | -9.2E18 to 9.2E18 | Large integers |
| `DECIMAL(p,s)` | Exact | Money, precise calculations |
| `FLOAT` | Approximate | Scientific data (avoid for money!) |

**Examples**:
```sql
Age TINYINT
Quantity SMALLINT
UserId INT
TransactionId BIGINT
Price DECIMAL(10,2)
TaxRate DECIMAL(5,4)  -- e.g., 0.0825 for 8.25%
```

### Dates and Times

| Type | Use When |
|------|----------|
| `DATE` | Date only (birthdate, event date) |
| `TIME` | Time only (opening hours) |
| `DATETIME2` | Date and time (preferred, higher precision) |
| `DATETIMEOFFSET` | Date/time with timezone |

**Examples**:
```sql
DateOfBirth DATE
OrderDate DATETIME2
CreatedAt DATETIME2 DEFAULT GETUTCDATE()
AppointmentTime TIME
EventStartTime DATETIMEOFFSET
```

### Other Types

```sql
-- Boolean
IsActive BIT DEFAULT 1

-- GUID
UniqueId UNIQUEIDENTIFIER DEFAULT NEWID()

-- Binary (files, images)
ProfilePicture VARBINARY(MAX)

-- JSON
Metadata NVARCHAR(MAX) CHECK (ISJSON(Metadata) = 1)

-- XML
Configuration XML
```

## Indexing Strategy

### Clustered Index (one per table)

Usually on:
- Primary key (default)
- Most common filter/sort column
- Narrow, unique, static column

```sql
-- Default: clustered on PK
CREATE TABLE Users (
    UserId INT IDENTITY(1,1) PRIMARY KEY CLUSTERED
);

-- Custom: clustered on different column
CREATE TABLE Logs (
    LogId BIGINT IDENTITY(1,1) PRIMARY KEY NONCLUSTERED,
    LogDate DATETIME2 NOT NULL,
    Message NVARCHAR(MAX)
);

CREATE CLUSTERED INDEX IX_Logs_LogDate ON Logs(LogDate);
```

### Non-Clustered Indexes

Create for:
- Foreign keys (JOIN columns)
- WHERE clause columns
- ORDER BY columns
- Frequently searched columns

```sql
-- Basic index
CREATE NONCLUSTERED INDEX IX_Orders_CustomerId
    ON Orders(CustomerId);

-- Composite index (order matters!)
CREATE NONCLUSTERED INDEX IX_Orders_CustomerId_OrderDate
    ON Orders(CustomerId, OrderDate DESC);

-- Covering index (includes extra columns)
CREATE NONCLUSTERED INDEX IX_Orders_CustomerId_Covering
    ON Orders(CustomerId)
    INCLUDE (OrderDate, TotalAmount);

-- Filtered index (partial index)
CREATE NONCLUSTERED INDEX IX_Orders_Active
    ON Orders(OrderDate)
    WHERE IsActive = 1 AND IsDeleted = 0;

-- Unique index
CREATE UNIQUE NONCLUSTERED INDEX IX_Users_Email
    ON Users(Email);
```

## Constraints

### Primary Key
```sql
-- Identity primary key
UserId INT IDENTITY(1,1) PRIMARY KEY

-- GUID primary key
UserId UNIQUEIDENTIFIER DEFAULT NEWID() PRIMARY KEY

-- Composite primary key
PRIMARY KEY (StudentId, CourseId)

-- Named constraint
CONSTRAINT PK_Users PRIMARY KEY (UserId)
```

### Foreign Key
```sql
CONSTRAINT FK_Orders_Customers
    FOREIGN KEY (CustomerId)
    REFERENCES Customers(CustomerId)
    ON DELETE CASCADE          -- Options: NO ACTION, CASCADE, SET NULL, SET DEFAULT
    ON UPDATE CASCADE
```

### Unique
```sql
CONSTRAINT UQ_Users_Email UNIQUE (Email)

-- Multi-column unique
CONSTRAINT UQ_Products_SKU_Supplier UNIQUE (SKU, SupplierId)
```

### Check
```sql
-- Range check
CONSTRAINT CK_Products_Price CHECK (Price >= 0)

-- Pattern check
CONSTRAINT CK_Users_Email CHECK (Email LIKE '%@%.%')

-- Multi-column check
CONSTRAINT CK_Events_Dates CHECK (EndDate >= StartDate)

-- Complex business rule
CONSTRAINT CK_Orders_Discount
    CHECK (DiscountPercent >= 0 AND DiscountPercent <= 100)
```

### Default
```sql
CreatedAt DATETIME2 DEFAULT GETUTCDATE()
IsActive BIT DEFAULT 1
Status NVARCHAR(20) DEFAULT 'Pending'
Quantity INT DEFAULT 0
```

## Schema Organization

### Use Schemas for Logical Grouping

```sql
-- Create schemas
CREATE SCHEMA Sales;
CREATE SCHEMA HR;
CREATE SCHEMA Reporting;

-- Create tables in schemas
CREATE TABLE Sales.Orders (...);
CREATE TABLE Sales.Customers (...);
CREATE TABLE HR.Employees (...);
CREATE TABLE Reporting.SalesSummary (...);

-- Query with schema
SELECT * FROM Sales.Orders;
```

Benefits:
- Logical organization
- Security (grant permissions per schema)
- Namespace management

## Common Anti-Patterns to Avoid

### 1. Entity-Attribute-Value (EAV)
```sql
-- ❌ Hard to query, poor performance
CREATE TABLE EntityAttributes (
    EntityId INT,
    AttributeName NVARCHAR(50),
    AttributeValue NVARCHAR(MAX)
);

-- ✓ Proper design with columns
CREATE TABLE Products (
    ProductId INT PRIMARY KEY,
    Name NVARCHAR(100),
    Price DECIMAL(10,2),
    Color NVARCHAR(50)
);
```

### 2. Comma-Separated Values
```sql
-- ❌ Violates 1NF, hard to query
CREATE TABLE Products (
    Tags NVARCHAR(500)  -- 'laptop,computer,electronics'
);

-- ✓ Separate table
CREATE TABLE ProductTags (
    ProductId INT,
    Tag NVARCHAR(50),
    PRIMARY KEY (ProductId, Tag)
);
```

### 3. Using Reserved Keywords
```sql
-- ❌ Avoid
CREATE TABLE User (...);  -- 'User' is reserved
CREATE TABLE [Order] (...);  -- Needs brackets

-- ✓ Better
CREATE TABLE Users (...);
CREATE TABLE Orders (...);
```

### 4. No Foreign Keys
```sql
-- ❌ No referential integrity
CREATE TABLE Orders (
    CustomerId INT  -- No FK constraint
);

-- ✓ With foreign key
CREATE TABLE Orders (
    CustomerId INT NOT NULL,
    CONSTRAINT FK_Orders_Customers
        FOREIGN KEY (CustomerId) REFERENCES Customers(CustomerId)
);
```

## Documentation

Always document your schema:

```sql
-- Table comments
EXEC sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Stores customer information',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'Customers';

-- Column comments
EXEC sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Unique customer identifier',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE',  @level1name = 'Customers',
    @level2type = N'COLUMN', @level2name = 'CustomerId';
```

## When to Use This Skill

Use this skill when:
- Designing a new database schema
- Normalizing existing tables
- Creating entity-relationship diagrams
- Choosing appropriate data types
- Defining relationships and constraints
- Planning indexes
- Making architectural database decisions

Simply mention database design, schema modeling, or data architecture, and this knowledge will be applied to help create robust, scalable database structures.
