---
name: data-architecture
description: Design data architectures with modeling, pipelines, and governance
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 06-data-architecture
bond_type: PRIMARY_BOND
last_updated: "2025-01"
---

# Data Architecture Skill

## Purpose
Design data architectures including data models, pipeline designs, governance frameworks, and quality management for operational and analytical systems.

---

## Parameters

| Parameter | Type | Required | Validation | Default |
|-----------|------|----------|------------|---------|
| `data_domain` | string | ✅ | min: 20 chars | - |
| `design_type` | enum | ⚪ | model\|pipeline\|governance\|quality | `model` |
| `data_type` | enum | ⚪ | operational\|analytical\|streaming | `operational` |
| `volume_tier` | enum | ⚪ | small\|medium\|large\|massive | `medium` |
| `output_format` | enum | ⚪ | erd\|yaml\|json | `erd` |

---

## Execution Flow

```
┌──────────────────────────────────────────────────────────┐
│ 1. VALIDATE: Check data domain and requirements          │
│ 2. DISCOVER: Identify data sources and entities          │
│ 3. MODEL: Create conceptual/logical/physical model       │
│ 4. DESIGN: Pipeline or governance framework              │
│ 5. QUALITY: Define data quality rules                    │
│ 6. VALIDATE: Check model consistency                     │
│ 7. DOCUMENT: Return data architecture                    │
└──────────────────────────────────────────────────────────┘
```

---

## Retry Logic

| Error | Retry | Backoff | Max Attempts |
|-------|-------|---------|--------------|
| `VALIDATION_ERROR` | No | - | 1 |
| `MODEL_GENERATION_ERROR` | Yes | 1s | 2 |
| `FORMAT_ERROR` | Yes | 500ms | 3 |

---

## Logging & Observability

```yaml
log_points:
  - event: design_started
    level: info
    data: [design_type, data_type]
  - event: entities_identified
    level: info
    data: [entity_count, relationship_count]
  - event: quality_rules_defined
    level: info
    data: [rule_count, dimensions_covered]

metrics:
  - name: models_created
    type: counter
    labels: [design_type]
  - name: design_time_ms
    type: histogram
  - name: entity_count
    type: gauge
```

---

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `E401` | Missing data domain | Request domain description |
| `E402` | Invalid relationships | Highlight circular/missing refs |
| `E403` | Schema validation failed | Show validation errors |
| `E404` | Unsupported volume tier | Suggest architectural changes |

---

## Unit Test Template

```yaml
test_cases:
  - name: "E-commerce data model"
    input:
      data_domain: "E-commerce order management"
      design_type: "model"
      output_format: "erd"
    expected:
      has_entities: true
      entities_include: ["Customer", "Order", "Product"]
      has_relationships: true
      valid_erd: true

  - name: "Analytics pipeline"
    input:
      data_domain: "Customer analytics"
      design_type: "pipeline"
      data_type: "analytical"
    expected:
      has_ingestion: true
      has_transformation: true
      has_serving: true

  - name: "Data quality rules"
    input:
      data_domain: "User profiles"
      design_type: "quality"
    expected:
      has_dimensions: true
      dimensions_include: ["completeness", "accuracy"]
      has_rules: true
```

---

## Troubleshooting

### Common Issues

| Symptom | Root Cause | Resolution |
|---------|------------|------------|
| Missing relationships | Incomplete domain | Add missing entities |
| Invalid ERD syntax | Format error | Validate Mermaid ERD |
| Missing quality rules | Dimensions not specified | Add quality dimensions |

### Debug Checklist
```
□ Is data domain clearly defined?
□ Are all entities identified?
□ Are relationships correctly typed?
□ Is output format valid?
□ Are quality dimensions covered?
```

---

## Data Quality Dimensions

| Dimension | Example Rule |
|-----------|--------------|
| Completeness | NOT NULL checks |
| Accuracy | Regex validation |
| Consistency | Referential integrity |
| Timeliness | SLA monitoring |
| Uniqueness | Primary key constraints |

---

## Integration

| Component | Trigger | Data Flow |
|-----------|---------|-----------|
| Agent 06 | Design request | Receives domain, returns model |
| Agent 04 | Cloud data services | Cloud data platform |

---

## Quality Standards

- **Normalized:** 3NF for operational, denormalized for analytical
- **Documented:** All entities and relationships described
- **Quality-first:** DQ rules for all critical fields

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01 | Production-grade: ERD, pipelines, DQ framework |
| 1.0.0 | 2024-12 | Initial release |
