---
name: migration-planning
description: Plan ETL/ELT pipelines, data migrations, change data capture, and rollback strategies.
allowed-tools: Read, Write, Glob, Grep, Task
---

# Migration Planning

## When to Use This Skill

Use this skill when:

- **Migration Planning tasks** - Working on plan etl/elt pipelines, data migrations, change data capture, and rollback strategies
- **Planning or design** - Need guidance on Migration Planning approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Migration planning defines how data moves between systems, including initial loads, incremental updates, transformations, and recovery strategies.

## ETL vs ELT

### Pattern Comparison

| Aspect | ETL | ELT |
|--------|-----|-----|
| Transform Location | Staging server | Target database |
| Best For | Limited target capacity | Cloud data warehouses |
| Data Volume | Small to medium | Large scale |
| Latency | Higher | Lower |
| Flexibility | Defined upfront | Schema-on-read |
| Examples | SSIS, Informatica | dbt, Snowflake, Databricks |

### Architecture Patterns

```text
ETL PATTERN
┌─────────┐    ┌──────────────────┐    ┌──────────┐
│ Source  │───►│   ETL Server     │───►│  Target  │
│ Systems │    │ Extract→Transform│    │    DW    │
└─────────┘    │ →Load            │    └──────────┘
               └──────────────────┘

ELT PATTERN
┌─────────┐    ┌──────────┐    ┌────────────────────┐
│ Source  │───►│  Staging │───►│    Target DW       │
│ Systems │    │  (Raw)   │    │ Transform in place │
└─────────┘    └──────────┘    └────────────────────┘
```

## Load Strategies

### Full vs Incremental

| Strategy | Description | Use Case |
|----------|-------------|----------|
| Full Load | Complete refresh | Small tables, dimension tables |
| Incremental | Only changes | Large tables, transaction data |
| CDC | Real-time changes | Near real-time requirements |
| Snapshot | Point-in-time | Audit, historical comparison |

### Incremental Load Approaches

| Approach | Detection Method | Pros | Cons |
|----------|------------------|------|------|
| Timestamp | modified_at column | Simple | Clock skew, deletes missed |
| Rowversion | Database version | Accurate | SQL Server specific |
| Trigger-based | Audit tables | All changes | Performance overhead |
| Log-based CDC | Transaction log | Real-time | Complex setup |
| Hash comparison | Row hash | Database agnostic | Processing overhead |

## Migration Plan Template

```markdown
# Data Migration Plan: CRM to Data Warehouse

## Executive Summary
- Source: Salesforce CRM
- Target: Azure Synapse Analytics
- Data Volume: 50M records initial, 100K daily incremental
- Timeline: 6 weeks

## Scope

### In Scope
| Object | Records | Load Type | Priority |
|--------|---------|-----------|----------|
| Accounts | 5M | Full then CDC | P1 |
| Contacts | 20M | Full then CDC | P1 |
| Opportunities | 15M | Full then Incremental | P1 |
| Activities | 10M | Incremental only | P2 |

### Out of Scope
- Attachments/Files
- Custom objects (phase 2)

## Migration Approach

### Phase 1: Initial Load
1. Extract full data to Azure Data Lake (Parquet)
2. Apply transformations via Synapse Spark pools
3. Load to staging tables
4. Validate record counts and checksums
5. Promote to production tables

### Phase 2: Incremental Sync
1. Enable CDC on source
2. Stream changes via Azure Data Factory
3. Apply upsert logic to target
4. Run hourly (can reduce to 15 min)

## Data Mapping
See Appendix A for full source-to-target mapping

## Validation Strategy
- Record count comparison
- Checksum validation on key columns
- Business rule validation queries
- Sample record verification

## Rollback Plan
1. Preserve backup of target tables before migration
2. Maintain ability to revert to backup for 7 days
3. If issues found, truncate and restore from backup
```

## Change Data Capture (CDC)

### CDC Implementation Options

| Option | Technology | Latency | Complexity |
|--------|------------|---------|------------|
| SQL Server CDC | Built-in feature | Seconds | Low |
| Debezium | Kafka Connect | Sub-second | Medium |
| AWS DMS | Managed service | Seconds | Low |
| Azure Data Factory | Managed service | Minutes | Low |

### SQL Server CDC Setup

```sql
-- Enable CDC on database
EXEC sys.sp_cdc_enable_db;

-- Enable CDC on table
EXEC sys.sp_cdc_enable_table
    @source_schema = N'dbo',
    @source_name = N'Customers',
    @role_name = NULL,
    @supports_net_changes = 1;

-- Query changes
DECLARE @from_lsn binary(10) = sys.fn_cdc_get_min_lsn('dbo_Customers');
DECLARE @to_lsn binary(10) = sys.fn_cdc_get_max_lsn();

SELECT
    __$operation,  -- 1=Delete, 2=Insert, 3=Before Update, 4=After Update
    customer_id,
    customer_name,
    email,
    __$start_lsn
FROM cdc.fn_cdc_get_net_changes_dbo_Customers(@from_lsn, @to_lsn, 'all')
ORDER BY __$start_lsn;
```

### C# CDC Consumer

```csharp
public class CdcProcessor
{
    private readonly IDbConnection _connection;
    private readonly IMessagePublisher _publisher;

    public async Task ProcessChanges(
        string captureInstance,
        byte[] fromLsn,
        CancellationToken ct)
    {
        var toLsn = await GetMaxLsn(ct);

        var changes = await GetNetChanges(captureInstance, fromLsn, toLsn, ct);

        foreach (var change in changes)
        {
            var operation = change.__$operation switch
            {
                1 => ChangeOperation.Delete,
                2 => ChangeOperation.Insert,
                4 => ChangeOperation.Update,
                _ => ChangeOperation.Unknown
            };

            await _publisher.PublishAsync(new ChangeEvent
            {
                Operation = operation,
                EntityType = captureInstance,
                EntityId = change.customer_id,
                Data = change,
                Timestamp = DateTime.UtcNow
            }, ct);
        }

        await SaveCheckpoint(captureInstance, toLsn, ct);
    }
}
```

## Bulk Load Patterns

### SQL Server Bulk Insert

```csharp
public class BulkLoader
{
    public async Task BulkInsert<T>(
        IEnumerable<T> records,
        string tableName,
        SqlConnection connection,
        CancellationToken ct)
    {
        using var bulkCopy = new SqlBulkCopy(connection)
        {
            DestinationTableName = tableName,
            BatchSize = 10000,
            BulkCopyTimeout = 600
        };

        // Map properties to columns
        var properties = typeof(T).GetProperties();
        foreach (var prop in properties)
        {
            bulkCopy.ColumnMappings.Add(prop.Name, prop.Name);
        }

        using var reader = new ObjectDataReader<T>(records);
        await bulkCopy.WriteToServerAsync(reader, ct);
    }
}

// Using with EF Core Bulk Extensions
await _context.BulkInsertAsync(customers, options =>
{
    options.BatchSize = 10000;
    options.SetOutputIdentity = true;
    options.UseTempDB = true;
});
```

## Pipeline Orchestration

### Pipeline Definition Template

```markdown
# Pipeline: Daily Customer Sync

## Schedule
- Frequency: Daily at 02:00 UTC
- Timeout: 2 hours
- Retry: 3 attempts with exponential backoff

## Steps

### Step 1: Extract
- Source: CRM API
- Method: Incremental (last 24 hours)
- Output: customers_extract_{date}.parquet

### Step 2: Validate Extract
- Check record count > 0
- Validate schema matches expected
- Log statistics

### Step 3: Transform
- Apply data quality rules
- Standardize address format
- Lookup reference data

### Step 4: Stage
- Load to staging.stg_customers
- Truncate and reload

### Step 5: Merge
- Upsert to dbo.dim_customer (SCD Type 2)
- Track new, updated, unchanged counts

### Step 6: Validate Load
- Compare source vs target counts
- Run quality checks
- Alert if discrepancies

## Dependencies
- Ref data pipeline (must complete first)
- DW infrastructure available

## Notifications
- Success: Slack #data-ops
- Failure: PagerDuty, Email to data-team@
```

### Azure Data Factory Pipeline

```json
{
  "name": "CustomerSync",
  "properties": {
    "activities": [
      {
        "name": "ExtractFromCRM",
        "type": "Copy",
        "inputs": [{ "referenceName": "CRM_Customer", "type": "DatasetReference" }],
        "outputs": [{ "referenceName": "ADLS_CustomerRaw", "type": "DatasetReference" }]
      },
      {
        "name": "TransformWithDataFlow",
        "type": "ExecuteDataFlow",
        "dependsOn": [{ "activity": "ExtractFromCRM", "dependencyConditions": ["Succeeded"] }],
        "dataFlow": { "referenceName": "CustomerTransform", "type": "DataFlowReference" }
      },
      {
        "name": "LoadToSynapse",
        "type": "Copy",
        "dependsOn": [{ "activity": "TransformWithDataFlow", "dependencyConditions": ["Succeeded"] }],
        "inputs": [{ "referenceName": "ADLS_CustomerClean", "type": "DatasetReference" }],
        "outputs": [{ "referenceName": "Synapse_DimCustomer", "type": "DatasetReference" }]
      }
    ]
  }
}
```

## Rollback Strategies

### Rollback Approaches

| Strategy | Recovery Time | Data Loss Risk | Complexity |
|----------|---------------|----------------|------------|
| Backup/Restore | Hours | Low | Low |
| Point-in-time | Minutes | None | Medium |
| Dual-write | Seconds | None | High |
| Temporal tables | Immediate | None | Medium |

### Rollback Implementation

```sql
-- Pre-migration backup
SELECT * INTO dbo.Customers_Backup_20241220
FROM dbo.Customers;

-- Create temporal table for automatic history
ALTER TABLE dbo.Customers
ADD
    ValidFrom DATETIME2 GENERATED ALWAYS AS ROW START DEFAULT SYSUTCDATETIME(),
    ValidTo DATETIME2 GENERATED ALWAYS AS ROW END DEFAULT CAST('9999-12-31 23:59:59' AS DATETIME2),
    PERIOD FOR SYSTEM_TIME (ValidFrom, ValidTo);

ALTER TABLE dbo.Customers
SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE = dbo.Customers_History));

-- Rollback to point in time
SELECT * FROM dbo.Customers
FOR SYSTEM_TIME AS OF '2024-12-20 01:00:00';
```

## Validation Framework

### Validation Checks

```csharp
public class MigrationValidator
{
    public async Task<ValidationResult> Validate(MigrationContext context, CancellationToken ct)
    {
        var results = new List<ValidationCheck>();

        // Row count comparison
        var sourceCount = await context.Source.CountAsync(ct);
        var targetCount = await context.Target.CountAsync(ct);
        results.Add(new ValidationCheck
        {
            Name = "RowCount",
            Passed = sourceCount == targetCount,
            SourceValue = sourceCount.ToString(),
            TargetValue = targetCount.ToString()
        });

        // Checksum validation
        var sourceChecksum = await CalculateChecksum(context.Source, context.KeyColumns, ct);
        var targetChecksum = await CalculateChecksum(context.Target, context.KeyColumns, ct);
        results.Add(new ValidationCheck
        {
            Name = "Checksum",
            Passed = sourceChecksum == targetChecksum,
            SourceValue = sourceChecksum,
            TargetValue = targetChecksum
        });

        // Sample record validation
        var sampleResults = await ValidateSampleRecords(context, 100, ct);
        results.AddRange(sampleResults);

        return new ValidationResult
        {
            AllPassed = results.All(r => r.Passed),
            Checks = results
        };
    }
}
```

## Validation Checklist

- [ ] Source and target systems identified
- [ ] Data volumes estimated
- [ ] Load strategy selected (full, incremental, CDC)
- [ ] Source-to-target mappings documented
- [ ] Transformation rules defined
- [ ] Validation approach planned
- [ ] Rollback strategy defined
- [ ] Performance testing planned
- [ ] Cutover plan documented

## Integration Points

**Inputs from**:

- `er-modeling` skill → Source schema
- `schema-design` skill → Target schema
- `data-lineage` skill → Transformation specs

**Outputs to**:

- ETL/ELT tools → Pipeline configurations
- `data-quality-planning` skill → Validation rules
- Operations → Monitoring and alerting
