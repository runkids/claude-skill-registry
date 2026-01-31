---
name: database-design
description: PostgreSQL models, SQLAlchemy, migrations, relationships, indexing
---

# Database Design — CEI-001

## Model Pattern

```python
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, JSON, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
import enum

from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="user", index=True)
    is_active = Column(Boolean, default=True, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    evaluations = relationship("Evaluation", back_populates="user", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
```

## Relationships

### One-to-Many
```python
class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(50), default="in_progress", index=True)
    score = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationship
    user = relationship("User", back_populates="evaluations")
    answers = relationship("Answer", back_populates="evaluation", cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    evaluation_id = Column(UUID(as_uuid=True), ForeignKey("evaluations.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    
    answer_value = Column(String(50), nullable=False)
    comment = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    evaluation = relationship("Evaluation", back_populates="answers")
```

### Many-to-Many
```python
from sqlalchemy import Table

document_category_association = Table(
    'document_category_association',
    Base.metadata,
    Column('document_id', UUID(as_uuid=True), ForeignKey('documents.id'), primary_key=True),
    Column('category_id', UUID(as_uuid=True), ForeignKey('categories.id'), primary_key=True)
)

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(255), nullable=False)
    source_filename = Column(String(255), nullable=False)
    status = Column(String(50), default="draft", index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Many-to-Many relationship
    categories = relationship("Category", secondary=document_category_association, back_populates="documents")

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), unique=True, nullable=False)
    
    # Back relationship
    documents = relationship("Document", secondary=document_category_association, back_populates="categories")
```

## Core Tables

### Chat System
```python
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    sources = Column(JSON, default=list)  # Array of {title, excerpt}
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    conversation = relationship("Conversation", back_populates="messages")
```

### Evaluation System
```python
class Question(Base):
    __tablename__ = "questions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    module_id = Column(String(50), nullable=False, index=True)
    
    text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # yesno, scale, multiple
    weight = Column(Integer, default=1)
    
    order = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Metadata
    __table_args__ = (
        Index('idx_questions_module', 'module_id', 'order'),
    )
```

### Documents/RAG
```python
class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    source_filename = Column(String(255), nullable=False)
    source_mimetype = Column(String(100), nullable=False)
    
    status = Column(String(50), default="draft", index=True)  # draft, processing, review, published, archived
    current_version = Column(Integer, default=1)
    
    # Metadata
    categories = Column(JSON, default=list)  # ['module1', 'module2']
    tags = Column(JSON, default=list)
    
    # Statistics
    chunk_count = Column(Integer, default=0)
    token_count = Column(Integer, default=0)
    rag_hit_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = Column(DateTime, nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    # Relationships
    versions = relationship("DocumentVersion", back_populates="document", cascade="all, delete-orphan")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    section_title = Column(String(255), nullable=True)
    
    # Weaviate reference
    weaviate_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship
    document = relationship("Document", back_populates="chunks")
    
    __table_args__ = (
        Index('idx_chunks_document_index', 'document_id', 'chunk_index'),
    )
```

## Migrations (Alembic)

```python
# alembic/versions/xxx_create_users_table.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_role'), 'users', ['role'])
    op.create_index(op.f('ix_users_is_active'), 'users', ['is_active'])

def downgrade():
    op.drop_index(op.f('ix_users_is_active'), table_name='users')
    op.drop_index(op.f('ix_users_role'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
```

## Indexes Strategy

```python
# Always index these:
- Primary keys (automatic)
- Foreign keys (for joins)
- Status columns (frequently filtered)
- Timestamps for range queries
- Email/unique identifiers

# Example:
class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(UUID(as_uuid=True), primary_key=True)  # Automatic index
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)  # Foreign key
    status = Column(String(50), index=True)  # Status filter
    
    # Composite index for common queries
    __table_args__ = (
        Index('idx_eval_user_status', 'user_id', 'status'),
    )
```

## Conventions

- Table names: lowercase_plural
- Column names: snake_case
- Primary keys: `id` with UUID
- Timestamps: ALWAYS `created_at` and `updated_at` with timezone
- Status: dedicated column with enum/string values
- Boolean: prefix with `is_` (is_active, is_deleted)
- Foreign keys: always indexed
- Relationships: use back_populates for bi-directional
- Cascading: use `cascade="all, delete-orphan"` for ownership
- Default values: use `server_default` for database-level defaults
