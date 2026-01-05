---
name: database-schema
description: Use when working with database models or migrations. Contains schema documentation and relationship patterns.
---

# Database Schema Skill

## Quick Reference
See [references/schema.md](references/schema.md) for the complete schema.

## Model Conventions
- All models inherit from BaseModel
- Use UUID for primary keys
- Include created_at and updated_at timestamps
- Soft delete via is_active flag

## Relationship Pattern
```python
class Pet(BaseModel):
    shelter_id = Column(UUID, ForeignKey('shelters.id'))
    shelter = relationship('Shelter', back_populates='pets')
```

When creating new models, always check references/schema.md first.
