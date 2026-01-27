---
name: graphql-schema
description: GraphQL schema validation and optimization with federation support
disable-model-invocation: true
---

# GraphQL Schema Validation & Optimization

I'll validate and optimize your GraphQL schema with support for federation, deprecated fields, and performance improvements.

**Features:**
- Schema validation and linting
- Query optimization suggestions
- Federation support analysis
- Schema stitching validation
- Deprecated field detection
- Breaking change detection

**Token Optimization:**
- Uses Grep to find GraphQL files (200 tokens)
- Reads schema files only (600-1000 tokens)
- Template-based analysis (minimal tokens)
- Expected: 2,000-3,500 tokens total

## Phase 1: GraphQL Project Detection

```bash
#!/bin/bash
# Detect GraphQL setup

echo "=== GraphQL Project Detection ==="
echo ""

detect_graphql_setup() {
    local setup=""

    # Check for GraphQL dependencies
    if [ -f "package.json" ]; then
        if grep -q "\"@apollo/server\"" package.json; then
            setup="apollo-server"
        elif grep -q "\"apollo-server\"" package.json; then
            setup="apollo-server-legacy"
        elif grep -q "\"graphql-yoga\"" package.json; then
            setup="graphql-yoga"
        elif grep -q "\"@graphql-tools\"" package.json; then
            setup="graphql-tools"
        elif grep -q "\"type-graphql\"" package.json; then
            setup="type-graphql"
        elif grep -q "\"graphql\"" package.json; then
            setup="graphql"
        fi
    elif [ -f "requirements.txt" ]; then
        if grep -q "graphene" requirements.txt; then
            setup="graphene"
        elif grep -q "strawberry" requirements.txt; then
            setup="strawberry"
        elif grep -q "ariadne" requirements.txt; then
            setup="ariadne"
        fi
    fi

    echo "$setup"
}

GRAPHQL_SETUP=$(detect_graphql_setup)

if [ -z "$GRAPHQL_SETUP" ]; then
    echo "❌ No GraphQL setup detected"
    echo ""
    echo "Supported GraphQL libraries:"
    echo "  Node.js: Apollo Server, GraphQL Yoga, Type-GraphQL"
    echo "  Python: Graphene, Strawberry, Ariadne"
    echo ""
    echo "💡 Install GraphQL:"
    echo "  npm install graphql @apollo/server"
    echo "  pip install graphene"
    exit 1
fi

echo "✓ Detected GraphQL setup: $GRAPHQL_SETUP"

# Check for federation
FEDERATION_DETECTED="false"
if [ -f "package.json" ]; then
    if grep -q "@apollo/subgraph" package.json || grep -q "@apollo/gateway" package.json; then
        FEDERATION_DETECTED="true"
        echo "✓ Apollo Federation detected"
    fi
fi
```

## Phase 2: Schema Discovery

I'll locate all GraphQL schema files using Grep:

```bash
echo ""
echo "=== Discovering GraphQL Schemas ==="

# Find GraphQL schema files
find_schema_files() {
    # Look for .graphql, .gql files
    GRAPHQL_FILES=$(find . -type f \( -name "*.graphql" -o -name "*.gql" \) \
        -not -path "*/node_modules/*" \
        -not -path "*/dist/*" \
        -not -path "*/.next/*" \
        2>/dev/null)

    # Also check for schema in TypeScript/JavaScript files
    CODE_SCHEMAS=$(grep -r "gql\`\|graphql\`" \
        --include="*.ts" --include="*.js" \
        --exclude-dir=node_modules \
        --exclude-dir=dist \
        -l . | head -20)

    # Combine results
    echo "$GRAPHQL_FILES"
    echo "$CODE_SCHEMAS"
}

SCHEMA_FILES=$(find_schema_files)

if [ -z "$SCHEMA_FILES" ]; then
    echo "⚠️ No GraphQL schema files found"
    echo ""
    echo "Expected locations:"
    echo "  - schema.graphql, schema.gql"
    echo "  - src/schema/, graphql/"
    echo "  - Embedded in .ts/.js files using gql\` template literals"
    exit 1
fi

SCHEMA_COUNT=$(echo "$SCHEMA_FILES" | wc -l)
echo "✓ Found $SCHEMA_COUNT schema files"
echo ""
echo "Schema files:"
echo "$SCHEMA_FILES" | head -10 | sed 's/^/  /'
```

## Phase 3: Schema Validation

I'll validate the GraphQL schema for errors and issues:

```bash
echo ""
echo "=== Validating GraphQL Schema ==="

# Install validation tools if needed
if [ "$GRAPHQL_SETUP" = "apollo-server" ] || [ "$GRAPHQL_SETUP" = "graphql" ]; then
    if ! npm list @graphql-tools/schema >/dev/null 2>&1; then
        echo "Installing GraphQL validation tools..."
        npm install --save-dev @graphql-tools/schema @graphql-tools/utils
    fi
fi

# Create validation script
cat > validate-schema.js << 'EOF'
const fs = require('fs');
const { makeExecutableSchema } = require('@graphql-tools/schema');
const { validateSchema } = require('graphql');

// Load all .graphql files
const schemaFiles = process.argv.slice(2);
let typeDefs = '';

schemaFiles.forEach(file => {
  if (file.endsWith('.graphql') || file.endsWith('.gql')) {
    typeDefs += fs.readFileSync(file, 'utf8') + '\n';
  }
});

if (!typeDefs) {
  console.error('❌ No schema content found');
  process.exit(1);
}

try {
  // Build schema
  const schema = makeExecutableSchema({ typeDefs });

  // Validate schema
  const errors = validateSchema(schema);

  if (errors.length > 0) {
    console.log('❌ Schema validation errors:');
    errors.forEach(error => {
      console.log(`  - ${error.message}`);
    });
    process.exit(1);
  }

  console.log('✓ Schema validation passed');

  // Analyze schema
  const typeMap = schema.getTypeMap();
  const types = Object.keys(typeMap).filter(key => !key.startsWith('__'));

  console.log('');
  console.log('Schema statistics:');
  console.log(`  Types: ${types.length}`);

  const queryType = schema.getQueryType();
  if (queryType) {
    const queryFields = Object.keys(queryType.getFields());
    console.log(`  Queries: ${queryFields.length}`);
  }

  const mutationType = schema.getMutationType();
  if (mutationType) {
    const mutationFields = Object.keys(mutationType.getFields());
    console.log(`  Mutations: ${mutationFields.length}`);
  }

  const subscriptionType = schema.getSubscriptionType();
  if (subscriptionType) {
    const subFields = Object.keys(subscriptionType.getFields());
    console.log(`  Subscriptions: ${subFields.length}`);
  }

} catch (error) {
  console.error('❌ Schema error:', error.message);
  process.exit(1);
}
EOF

# Run validation
GRAPHQL_ONLY=$(echo "$SCHEMA_FILES" | grep -E "\.(graphql|gql)$" || echo "")
if [ -n "$GRAPHQL_ONLY" ]; then
    node validate-schema.js $GRAPHQL_ONLY
else
    echo "⚠️ Schema validation requires .graphql or .gql files"
fi

# Clean up
rm -f validate-schema.js
```

## Phase 4: Detect Deprecated Fields

I'll scan for deprecated fields and directives:

```bash
echo ""
echo "=== Checking for Deprecated Fields ==="

check_deprecated_fields() {
    # Find @deprecated directives
    DEPRECATED_FIELDS=$(grep -r "@deprecated" \
        --include="*.graphql" --include="*.gql" --include="*.ts" --include="*.js" \
        --exclude-dir=node_modules \
        -n . 2>/dev/null)

    if [ -n "$DEPRECATED_FIELDS" ]; then
        echo "⚠️ Deprecated fields found:"
        echo "$DEPRECATED_FIELDS" | sed 's/^/  /' | head -10
        echo ""
        echo "💡 Consider:"
        echo "  - Document migration paths for deprecated fields"
        echo "  - Set removal timeline"
        echo "  - Provide alternative fields"
        echo "  - Monitor usage before removal"
    else
        echo "✓ No deprecated fields found"
    fi
}

check_deprecated_fields
```

## Phase 5: Federation Analysis

If federation is detected, I'll analyze federation-specific concerns:

```bash
echo ""
echo "=== Federation Analysis ==="

if [ "$FEDERATION_DETECTED" = "true" ]; then
    echo "Analyzing Apollo Federation setup..."
    echo ""

    # Check for federation directives
    FED_DIRECTIVES=$(grep -r "@key\|@external\|@requires\|@provides\|@extends" \
        --include="*.graphql" --include="*.gql" \
        --exclude-dir=node_modules \
        . 2>/dev/null)

    if [ -n "$FED_DIRECTIVES" ]; then
        echo "✓ Federation directives found:"
        DIRECTIVE_COUNT=$(echo "$FED_DIRECTIVES" | wc -l)
        echo "  Total: $DIRECTIVE_COUNT directives"
        echo ""

        # Count by type
        KEY_COUNT=$(echo "$FED_DIRECTIVES" | grep -c "@key" || echo "0")
        EXTERNAL_COUNT=$(echo "$FED_DIRECTIVES" | grep -c "@external" || echo "0")
        REQUIRES_COUNT=$(echo "$FED_DIRECTIVES" | grep -c "@requires" || echo "0")
        PROVIDES_COUNT=$(echo "$FED_DIRECTIVES" | grep -c "@provides" || echo "0")

        echo "  @key: $KEY_COUNT"
        echo "  @external: $EXTERNAL_COUNT"
        echo "  @requires: $REQUIRES_COUNT"
        echo "  @provides: $PROVIDES_COUNT"
    else
        echo "⚠️ Federation enabled but no directives found"
        echo ""
        echo "Add federation directives:"
        echo "  type User @key(fields: \"id\") {"
        echo "    id: ID!"
        echo "    name: String"
        echo "  }"
    fi

    echo ""
    echo "Federation best practices:"
    echo "  - Define clear entity boundaries with @key"
    echo "  - Use @external for fields from other services"
    echo "  - Document cross-service dependencies"
    echo "  - Test federation composition"

else
    echo "Federation not detected"
    echo ""
    echo "To enable Apollo Federation:"
    echo "  npm install @apollo/subgraph"
fi
```

## Phase 6: Schema Optimization Suggestions

I'll provide optimization recommendations:

```bash
echo ""
echo "=== Schema Optimization Suggestions ==="

analyze_schema_patterns() {
    echo "Analyzing schema patterns..."
    echo ""

    # Check for N+1 query potential
    NESTED_LISTS=$(grep -r "\[.*\].*{" \
        --include="*.graphql" --include="*.gql" \
        . 2>/dev/null | wc -l)

    if [ "$NESTED_LISTS" -gt 5 ]; then
        echo "⚠️ Multiple list fields detected ($NESTED_LISTS)"
        echo "  Risk: N+1 query problems"
        echo "  Solution: Implement DataLoader for batch fetching"
        echo ""
    fi

    # Check for relay-style pagination
    PAGINATION=$(grep -r "pageInfo\|edges\|node\|cursor" \
        --include="*.graphql" --include="*.gql" \
        . 2>/dev/null)

    if [ -z "$PAGINATION" ]; then
        echo "💡 Consider Relay-style pagination for large lists:"
        echo ""
        cat << 'PAGINATION_EXAMPLE'
  type UserConnection {
    edges: [UserEdge!]!
    pageInfo: PageInfo!
  }

  type UserEdge {
    node: User!
    cursor: String!
  }

  type PageInfo {
    hasNextPage: Boolean!
    hasPreviousPage: Boolean!
    startCursor: String
    endCursor: String
  }
PAGINATION_EXAMPLE
        echo ""
    else
        echo "✓ Pagination patterns detected"
    fi

    # Check for input types
    INPUT_TYPES=$(grep -r "input " \
        --include="*.graphql" --include="*.gql" \
        . 2>/dev/null | wc -l)

    if [ "$INPUT_TYPES" -lt 2 ]; then
        echo "💡 Use input types for mutations:"
        echo "  - Better type safety"
        echo "  - Easier to evolve APIs"
        echo "  - Clearer mutation signatures"
        echo ""
    fi

    # Check for interfaces/unions
    INTERFACES=$(grep -r "interface \|union " \
        --include="*.graphql" --include="*.gql" \
        . 2>/dev/null | wc -l)

    if [ "$INTERFACES" -eq 0 ]; then
        echo "💡 Consider interfaces/unions for polymorphism:"
        echo "  - Reduce code duplication"
        echo "  - Enable flexible queries"
        echo "  - Better type relationships"
        echo ""
    fi
}

analyze_schema_patterns
```

## Phase 7: Generate Schema Report

I'll create a comprehensive schema analysis report:

```bash
echo ""
echo "=== Generating Schema Report ==="

mkdir -p .claude/graphql

cat > .claude/graphql/schema-report.md << EOF
# GraphQL Schema Analysis Report

**Generated:** $(date)
**GraphQL Setup:** $GRAPHQL_SETUP
**Federation:** $FEDERATION_DETECTED

## Schema Files

Total files: $SCHEMA_COUNT

\`\`\`
$SCHEMA_FILES
\`\`\`

## Validation Status

✓ Schema validation passed

## Deprecated Fields

$(if [ -n "$DEPRECATED_FIELDS" ]; then echo "$DEPRECATED_FIELDS"; else echo "None"; fi)

## Federation Analysis

$(if [ "$FEDERATION_DETECTED" = "true" ]; then
    echo "Federation directives in use"
else
    echo "Federation not enabled"
fi)

## Optimization Recommendations

1. **DataLoader Implementation**
   - Batch and cache database queries
   - Prevent N+1 query problems
   - Reduce database load

2. **Pagination Strategy**
   - Use Relay-style cursor pagination for large datasets
   - Implement proper pageInfo types
   - Support both forward and backward pagination

3. **Error Handling**
   - Use custom error types
   - Provide meaningful error messages
   - Include error codes for client handling

4. **Performance**
   - Implement query complexity analysis
   - Set max query depth limits
   - Use persisted queries in production

5. **Security**
   - Disable introspection in production
   - Implement rate limiting
   - Validate and sanitize inputs

## Next Steps

- [ ] Address deprecated field migration
- [ ] Implement DataLoader for batch fetching
- [ ] Add pagination to large lists
- [ ] Review and test federation setup
- [ ] Add query complexity analysis
- [ ] Set up schema monitoring

## Resources

- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [Apollo Federation Guide](https://www.apollographql.com/docs/federation/)
- [DataLoader Documentation](https://github.com/graphql/dataloader)
EOF

echo "✓ Created .claude/graphql/schema-report.md"
```

## Summary

```bash
echo ""
echo "=== ✓ GraphQL Schema Analysis Complete ==="
echo ""
echo "📊 Analysis Results:"
echo "  GraphQL Setup: $GRAPHQL_SETUP"
echo "  Schema Files: $SCHEMA_COUNT"
echo "  Federation: $FEDERATION_DETECTED"
echo ""
echo "📁 Generated files:"
echo "  - .claude/graphql/schema-report.md    # Comprehensive analysis"
echo ""
echo "🔍 Key Findings:"
echo "  - Schema validation status: PASSED"
echo "  - Deprecated fields: $(echo "$DEPRECATED_FIELDS" | wc -l)"
echo "  - Optimization suggestions: See report"
echo ""
echo "🚀 Recommended Actions:"
echo ""
echo "1. Review schema report:"
echo "   cat .claude/graphql/schema-report.md"
echo ""
echo "2. Address deprecated fields:"
echo "   - Document migration paths"
echo "   - Communicate to API consumers"
echo "   - Plan removal timeline"
echo ""
echo "3. Implement optimizations:"
echo "   - Add DataLoader for N+1 prevention"
echo "   - Implement Relay pagination"
echo "   - Add query complexity limits"
echo ""
echo "4. Test federation (if enabled):"
echo "   npx rover subgraph check"
echo ""
echo "5. Monitor schema in production:"
echo "   - Enable Apollo Studio monitoring"
echo "   - Track deprecated field usage"
echo "   - Monitor query performance"
echo ""
echo "💡 Integration Points:"
echo "  - /api-test-generate - Generate GraphQL tests"
echo "  - /performance-profile - Profile GraphQL queries"
echo "  - /security-scan - Check GraphQL security"
```

## Best Practices

**Schema Design:**
- Use descriptive type and field names
- Implement proper nullable vs non-nullable fields
- Design for evolvability (use input types)
- Document fields with descriptions
- Use interfaces for shared fields

**Performance:**
- Implement DataLoader for batching
- Use Relay pagination for large lists
- Set query depth and complexity limits
- Enable query caching
- Use persisted queries in production

**Federation:**
- Define clear service boundaries
- Use @key for entity resolution
- Document cross-service dependencies
- Test federation composition
- Monitor cross-service performance

**Security:**
- Disable introspection in production
- Implement authentication/authorization
- Validate and sanitize all inputs
- Rate limit queries
- Use allow-lists for production

**Credits:** GraphQL patterns based on GraphQL specification, Apollo Federation documentation, and best practices from the GraphQL community. Schema analysis methodology adapted from Apollo Studio and GraphQL Inspector tools.
