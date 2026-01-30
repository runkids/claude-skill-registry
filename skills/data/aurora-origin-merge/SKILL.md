---
name: aurora-origin-merge
description: >
  Handles .origin.ts file merges after Aurora CLI regeneration. Provides
  step-by-step workflow to surgically merge new schema code into files with
  custom modifications, preserving all business logic.
  Trigger: After aurora load back module creates .origin files, or when merging
  regenerated code with custom modifications.
license: MIT
metadata:
  author: aurora
  version: '1.1'
  auto_invoke: 'origin file merge, .origin.ts, merge after regeneration'
  scope: back
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, Task
---

## When to Use

Use this skill when:

- Aurora CLI creates `.origin.ts` files after regeneration
- You need to merge new schema-generated code into files with custom
  modifications
- The CLI prompts "Do you want to manage origin files? (Y/n)"
- You find `.origin.ts` files in the codebase after running
  `aurora load back module`

**Always combine with:**

- `aurora-cli` skill (triggers the regeneration that creates .origin files)
- `aurora-cqrs` skill (understand editable zones vs generated zones)
- `prettier` skill (format after merge)

---

## Critical Concept: Why .origin Files Exist

Aurora tracks every generated file via SHA1 hash in `*-lock.json` files. When
you regenerate a module (`aurora load back module -n=bc/module -ft`), Aurora
compares each file's current hash against the stored hash.

```
File hash matches lock?
    │
    YES → Overwrite safely (no custom code)
    │
    NO  → File has custom modifications
         │
         └→ Create filename.origin.ts (new generated version)
            Keep filename.ts intact (your custom code)
```

The `.origin.ts` file contains what Aurora WOULD have generated. Your job is to
**surgically extract** only the new schema-related code from `.origin` and merge
it into the existing file.

---

## Step-by-Step Merge Workflow

### Step 0: Detect YAML Schema Delta (CRITICAL)

**Before touching any `.origin` file, you MUST determine what changed in the YAML
schema.** This tells you exactly what to merge and — equally important — what NOT
to merge (fields intentionally removed from certain files).

**Detect which workflow the developer followed:**

```bash
# Check if YAML has uncommitted changes
git diff HEAD -- cliter/<bc>/<module>.aurora.yaml
```

- **If diff exists** → Flujo A (YAML changed, not yet committed) → compare
  against `HEAD`
- **If no diff** → Flujo B (YAML already committed) → compare against previous
  commit

**Get the previous YAML version:**

```bash
# Flujo A: YAML not committed yet — HEAD has the old version
git show HEAD:cliter/<bc>/<module>.aurora.yaml > /tmp/old-schema.yaml

# Flujo B: YAML already committed — get the commit before the latest change
PREV_COMMIT=$(git log -2 --format="%H" -- cliter/<bc>/<module>.aurora.yaml | tail -1)
git show $PREV_COMMIT:cliter/<bc>/<module>.aurora.yaml > /tmp/old-schema.yaml
```

**Compare old vs current YAML to get the delta:**

```bash
diff /tmp/old-schema.yaml cliter/<bc>/<module>.aurora.yaml
```

**The delta tells you:**

| Delta | Action |
| --- | --- |
| New field in YAML | Merge from `.origin` into existing files |
| Removed field in YAML | Remove from existing files |
| Changed field type/properties | Update in existing files |
| No change for a field | DO NOT touch — even if missing from existing file |

**WHY this matters:** Without the YAML delta, you cannot distinguish between:

- A field that is **new** (must be merged from `.origin`)
- A field that was **intentionally removed** from a specific file (e.g., a
  back-calculated field removed from the creation DTO/Input)

If a field exists in the YAML but is NOT in the existing file, and the YAML delta
shows that field is NOT new → **it was intentionally removed. Do NOT add it.**

### Step 1: Find All .origin Files

```bash
fd ".origin.ts"
```

### Step 2: For EACH .origin File

Read BOTH files side by side:

1. **Existing file** (has custom code + old schema)
2. **Origin file** (has NO custom code + new schema)

### Step 3: Merge Using the YAML Delta

For each change identified in Step 0:

**New field added:**

1. Find the field in the `.origin` file
2. Copy the corresponding code (import, Value Object instantiation, response
   mapping, etc.) into the existing file
3. Respect the field order from the YAML

**Field removed:**

1. Remove the corresponding code from the existing file
2. Remove unused imports

**Field type/properties changed:**

1. Find the field in the `.origin` file
2. Replace the corresponding code in the existing file with the `.origin`
   version
3. Preserve any custom transformation logic around that field

**GOLDEN RULE: Only merge code related to fields that CHANGED in the YAML delta.
Never touch code for fields that didn't change — even if the `.origin` file has
them and the existing file doesn't.**

### Step 4: Preserve ALL Custom Code

While merging, ensure:

- Custom class properties remain untouched
- Custom logic in method bodies is preserved
- Custom helper methods are kept
- Custom imports are retained
- Intentionally removed fields stay removed

### Step 5: Delete the .origin File

```bash
rm path/to/file.origin.ts
```

### Step 6: Verify No .origin Files Remain

```bash
fd ".origin.ts"
# Should return empty
```

---

## Merge Rules by File Type

### Mapper Files (`*.mapper.ts`)

**Most common merge scenario.** Mappers have both generated and custom zones.

**Custom zones to PRESERVE:**

- Class-level properties
- Logic in public methods (`mapModelToAggregate`, `mapModelsToAggregates`,
  `mapAggregateToResponse`, `mapAggregatesToResponses`)
- Custom helper methods
- Constructor modifications

**Generated zones to UPDATE from .origin:**

- Imports (new Value Object imports)
- `makeAggregate()` method — new Value Object instantiations
- `makeResponse()` method — new `.value` property accesses
- Eager loading blocks (new related mappers)

**Example — Adding `observations` field:**

```typescript
// 1. ADD new import (from .origin)
import {
  // ... existing imports
  ProductionPlanningProductionOrderHeaderObservations, // ← NEW
  // ... existing imports
} from '@app/.../domain/value-objects';

// 2. ADD in makeAggregate() — after rowId, before next field
private makeAggregate(...) {
  return ProductionOrderHeader.register(
    new Id(model.id, { undefinable: true }),
    new RowId(model.rowId, { undefinable: true }),
    new Observations(model.observations, { undefinable: true }), // ← NEW
    new ProductionCenterId(model.productionCenterId, { undefinable: true }),
    // ...
  );
}

// 3. ADD in makeResponse() — same position as makeAggregate
private makeResponse(header) {
  return new Response(
    header.id.value,
    header.rowId.value,
    header.observations.value, // ← NEW
    header.productionCenterId.value,
    // ...
  );
}
```

**CRITICAL: Parameter order in `register()` and `Response()` MUST match the
field order defined in the `.aurora.yaml` file.**

---

### Command Handler Files (`*command-handler.ts`)

**Custom zones to PRESERVE:**

- Constructor injected dependencies
- ALL logic in `execute()` method body (validations, business rules, external
  calls, data denormalization, calculated fields)
- Custom helper methods
- Custom decorators

**Generated zones to UPDATE from .origin:**

- Command payload destructuring (new fields)
- Value Object instantiations in service call
- New imports for Value Objects

**Example — Handler with custom SAP integration:**

```typescript
// PRESERVE: All custom logic (validations, API calls, error handling)
async execute(command: CreateOrderCommand): Promise<void> {
  // ✅ PRESERVE: Custom validation
  const delivery = await this.httpService.get(sapUrl);
  if (!delivery) throw new BadRequestException('Not found');

  // ✅ PRESERVE: Custom business rules
  if (!account.scopes.includes('MANAGER')) {
    // ... complex permission checking
  }

  // UPDATE from .origin: New field in service call
  await this.service.main(
    {
      id: new OrderId(command.payload.id),
      observations: new OrderObservations(command.payload.observations), // ← NEW
      // ... rest of fields
    },
    command.cQMetadata,
  );
}
```

---

### Query Handler Files (`*query-handler.ts`)

Same pattern as Command Handlers. Preserve custom logic, update generated query
parameters.

---

### Aggregate Files (`*.aggregate.ts`)

**Normally fully generated — should NOT have custom code.**

If custom code exists (rare), preserve it and merge:

- New properties
- New parameters in `register()` static method
- New parameters in `constructor()`
- New fields in `created()`, `updated()`, `deleted()` event methods
- New fields in `toDTO()` and `toRepository()`

---

### Response Files (`*-response.ts`)

**Normally fully generated — should NOT have custom code.**

If custom code exists, merge new constructor parameters in correct position.

---

### Model Files (`*.model.ts`) — Sequelize

**Normally fully generated — should NOT have custom code.**

If custom code exists (custom hooks, virtual fields, scopes), preserve and merge:

- New `@Column` decorators
- New `@BelongsTo`, `@HasMany`, `@BelongsToMany` associations
- New lifecycle hooks

---

### Service Files (`*service.ts` in `@app/`)

**Normally fully generated — should NOT have custom code.**

Business logic belongs in handlers, NOT services. If custom code exists in
services, it's likely a custom service in `@api/` layer (not generated).

---

### API Handler Files (`*.handler.ts` in `@api/`)

**Can be heavily customized.** These are the primary location for:

- External API integrations (SAP, HESA, OData)
- Data denormalization
- Multi-step validation workflows
- Queue management
- Complex business orchestration

**Merge strategy:** These files can have 500+ lines of custom code. Be extremely
careful:

1. Read the ENTIRE existing file
2. Read the ENTIRE .origin file
3. Identify ONLY the schema-delta lines
4. Add them without touching any custom logic

---

### Resolver/Controller Files (`@api/`)

**Custom zones to PRESERVE:**

- Custom decorators (`@UseGuards`, `@UseInterceptors`)
- Custom parameter decorators
- Pre/post processing logic
- Custom error handling

**Generated zones to UPDATE from .origin:**

- New input/output type references
- New field mappings in payload construction

---

### DTO / Input Files

**Normally fully generated.** If custom validation decorators were added,
preserve them and merge new fields.

---

### Event Files (`*.event.ts`, `*event-handler.ts`)

**Normally fully generated.** Merge new event properties from .origin.

---

### Seeder Files (`*.seeder.ts`)

**Often customized** with specific seed data. Merge new field entries preserving
custom seed values.

---

## Handling Parameter Order

**CRITICAL:** Aurora generates parameters in the EXACT order defined in
`.aurora.yaml`. When merging, the new field MUST be inserted in the correct
position.

```yaml
# YAML field order:
aggregateProperties:
  - name: id          # position 0
  - name: rowId       # position 1
  - name: observations # position 2  ← NEW FIELD
  - name: code        # position 3
  - name: status      # position 4
```

This order MUST be reflected in:

1. `register()` parameters in Aggregate
2. `register()` arguments in Mapper's `makeAggregate()`
3. `Response` constructor parameters
4. `Response` constructor arguments in Mapper's `makeResponse()`
5. Command/Query payload fields
6. Event properties

**How to determine position:** Look at the `.origin` file — Aurora already
generated the correct order. Just match that order when inserting into the
existing file.

---

## Conflict Resolution

### Scenario: .origin restructures code that custom code also modified

**Example:** You customized `makeAggregate()` to add a conditional mapping, and
the .origin has a new field in `makeAggregate()`.

**Resolution:**

1. Identify the NEW lines in .origin (the schema delta)
2. Insert those lines into YOUR customized version
3. Keep your conditional logic intact

```typescript
// YOUR custom makeAggregate (existing)
private makeAggregate(model, cQMetadata) {
  // CUSTOM: conditional mapping based on status
  const status = model.status === 'LEGACY'
    ? ProductStatus.MIGRATED
    : model.status;

  return Product.register(
    new ProductId(model.id, { undefinable: true }),
    new ProductStatus(status, { undefinable: true }), // CUSTOM: uses transformed status
    // ...
  );
}

// .origin makeAggregate (new field: observations)
private makeAggregate(model, cQMetadata) {
  return Product.register(
    new ProductId(model.id, { undefinable: true }),
    new ProductObservations(model.observations, { undefinable: true }), // ← NEW
    new ProductStatus(model.status, { undefinable: true }),
    // ...
  );
}

// ✅ MERGED RESULT: custom logic preserved + new field added
private makeAggregate(model, cQMetadata) {
  // CUSTOM: conditional mapping based on status
  const status = model.status === 'LEGACY'
    ? ProductStatus.MIGRATED
    : model.status;

  return Product.register(
    new ProductId(model.id, { undefinable: true }),
    new ProductObservations(model.observations, { undefinable: true }), // ← NEW from .origin
    new ProductStatus(status, { undefinable: true }), // CUSTOM: preserved transformation
    // ...
  );
}
```

### Scenario: Field exists in .origin but NOT in existing file

**This is the most dangerous case.** Before adding anything, check the YAML
delta from Step 0:

- **Field IS in the YAML delta (new)** → Merge it from `.origin`
- **Field is NOT in the YAML delta (existed before)** → It was intentionally
  removed. **DO NOT add it.**

**Common case:** A field like `code` exists in the YAML (and in `.origin`) but
was removed from the creation DTO/Input because it's auto-generated by a
database trigger or calculated in the back-end. The YAML delta won't show `code`
as new → don't touch it.

### Scenario: Multiple .origin files from one regeneration

Process them ALL. Order doesn't matter since each .origin corresponds to exactly
one existing file.

### Scenario: .origin file for a file you don't recognize

Read both files. If the existing file has no meaningful custom code (just a stale
hash), you can safely replace it entirely with the .origin content.

---

## Post-Merge Checklist

After merging ALL .origin files:

- [ ] No `.origin.ts` files remain (`fd ".origin.ts"` returns empty)
- [ ] All new imports are added (no missing Value Objects)
- [ ] Parameter order matches `.aurora.yaml` field order
- [ ] All custom logic is preserved (no overwrites)
- [ ] Eager loading blocks include new relationships (if any)
- [ ] Run Prettier to format (`npx prettier --write <files>`)
- [ ] TypeScript compiles without errors (`npx tsc --noEmit`)

---

## Common Mistakes

| Mistake | Consequence | Prevention |
| --- | --- | --- |
| Skipping YAML delta detection (Step 0) | Re-adding intentionally removed fields | ALWAYS diff YAML before merging |
| Adding a field that exists in .origin but was intentionally removed | Breaks custom back-calculation logic | Check YAML delta — if field is NOT new, don't add it |
| Replacing existing file with .origin entirely | Custom code LOST | Always compare first |
| Forgetting to add new import | TypeScript compilation error | Check .origin imports section |
| Wrong parameter order in `register()` | Runtime mapping errors | Match YAML field order |
| Leaving .origin files in codebase | Confuses future regenerations | Always delete after merge |
| Missing field in `makeResponse()` but added in `makeAggregate()` | Response missing data | Update BOTH methods |
| Answering `n` to origin files prompt | .origin files not created, can't merge | Always answer `Y` |
| Not running Prettier after merge | Inconsistent formatting | Run prettier on modified files |

---

## Commands

```bash
# Find all .origin files
fd ".origin.ts"

# Compare files side by side (VS Code)
code -d path/to/file.ts path/to/file.origin.ts

# Delete all .origin files after merge
fd ".origin.ts" -x rm {}

# Verify no .origin files remain
fd ".origin.ts"

# Check TypeScript compiles
npx tsc --noEmit

# Format merged files
npx prettier --write "src/@app/production-planning/**/*.ts"
```

---

## Decision Tree: How Complex Is This Merge?

```
How many .origin files?
    │
    1 file ─────────────── Simple merge (5 min)
    │
    2-5 files ──────────── Medium merge (review each)
    │
    5+ files ───────────── Complex merge (plan first)

Does the existing file have custom logic?
    │
    NO (just stale hash) → Replace entirely with .origin content
    │
    YES, simple (property, one-liner) → Quick surgical merge
    │
    YES, complex (50+ lines custom) → Careful line-by-line merge
    │
    YES, very complex (external APIs, queues, 500+ lines) → Read ENTIRE file,
      identify ONLY the schema delta, merge minimally
```

---

## Related Skills

| Skill | When to Use Together |
| --- | --- |
| `aurora-cli` | Triggers regeneration that creates .origin files |
| `aurora-cqrs` | Understand editable zones vs generated zones |
| `aurora-schema` | Understanding YAML field order for parameter positioning |
| `prettier` | Format files after merge |
| `conventional-commits` | Commit after successful merge |
