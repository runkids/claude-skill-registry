---
name: license-check
description: License compliance checking and conflict detection
disable-model-invocation: true
---

# License Compliance Checker

I'll analyze your project dependencies for license compliance, detect conflicts, and ensure legal compatibility.

Arguments: `$ARGUMENTS` - focus area (commercial, gpl, conflicts) or specific packages

## License Compliance Philosophy

**Core Principles:**
- Identify all dependency licenses
- Detect incompatible license combinations
- Flag copyleft licenses for commercial projects
- Generate compliance documentation
- Track license changes

**Token Optimization:**
- Uses package manager commands (200 tokens)
- Grep for license patterns (100 tokens)
- Expected: 2,000-3,000 tokens

## Phase 1: License Detection

```bash
#!/bin/bash
# Detect project licenses and dependency managers

detect_license_info() {
    echo "=== License Detection ==="
    echo ""

    # Check project license
    if [ -f "LICENSE" ] || [ -f "LICENSE.md" ] || [ -f "LICENSE.txt" ]; then
        echo "✓ Project license file found"
        PROJECT_LICENSE=$(head -5 LICENSE* | grep -i -o "MIT\|Apache\|GPL\|BSD\|ISC" | head -1)
        if [ -n "$PROJECT_LICENSE" ]; then
            echo "  Project license: $PROJECT_LICENSE"
        fi
    else
        echo "⚠️  No project license file found"
    fi

    # Check package.json license field
    if [ -f "package.json" ]; then
        PKG_LICENSE=$(grep -o '"license"[[:space:]]*:[[:space:]]*"[^"]*"' package.json | cut -d'"' -f4)
        if [ -n "$PKG_LICENSE" ]; then
            echo "  package.json license: $PKG_LICENSE"
        fi
    fi

    echo ""

    # Detect package managers
    MANAGERS=()

    if [ -f "package.json" ]; then
        echo "✓ Node.js project detected"
        MANAGERS+=("npm")
    fi

    if [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
        echo "✓ Python project detected"
        MANAGERS+=("pip")
    fi

    if [ -f "Gemfile" ]; then
        echo "✓ Ruby project detected"
        MANAGERS+=("bundler")
    fi

    if [ -f "go.mod" ]; then
        echo "✓ Go project detected"
        MANAGERS+=("go")
    fi

    if [ -f "Cargo.toml" ]; then
        echo "✓ Rust project detected"
        MANAGERS+=("cargo")
    fi

    if [ -f "composer.json" ]; then
        echo "✓ PHP project detected"
        MANAGERS+=("composer")
    fi

    echo ""
}

detect_license_info
```

## Phase 2: Node.js License Analysis

```bash
#!/bin/bash
# Comprehensive Node.js license checking

check_npm_licenses() {
    echo "=== Node.js License Analysis ==="
    echo ""

    # Install license-checker if not available
    if ! command -v license-checker &> /dev/null; then
        echo "Installing license-checker..."
        npm install -g license-checker
    fi

    # Generate license report
    echo "Scanning dependencies..."
    license-checker --json --production > .licenses.json 2>/dev/null

    if [ ! -f ".licenses.json" ]; then
        echo "❌ Failed to generate license report"
        exit 1
    fi

    # License categories
    PERMISSIVE_LICENSES=("MIT" "Apache-2.0" "BSD-2-Clause" "BSD-3-Clause" "ISC" "0BSD")
    WEAK_COPYLEFT=("LGPL-2.1" "LGPL-3.0" "MPL-2.0")
    STRONG_COPYLEFT=("GPL-2.0" "GPL-3.0" "AGPL-3.0")
    PROBLEMATIC=("CC-BY-NC" "Commons Clause" "Unlicense" "WTFPL")

    echo ""
    echo "=== License Summary ==="
    echo ""

    # Count licenses
    total_packages=$(cat .licenses.json | grep -c '"licenses":')
    echo "Total packages: $total_packages"
    echo ""

    # Categorize licenses
    echo "License breakdown:"
    cat .licenses.json | grep -o '"licenses":"[^"]*"' | sort | uniq -c | sort -rn | while read count license; do
        license_name=$(echo "$license" | cut -d'"' -f4)
        printf "  %-30s %5d\n" "$license_name" "$count"
    done

    echo ""
}

check_npm_licenses
```

### Identify License Issues

```bash
#!/bin/bash
# Detect license compliance issues

detect_license_issues() {
    echo "=== License Compliance Issues ==="
    echo ""

    ISSUES_FOUND=false

    # Check for strong copyleft licenses
    echo "Checking for copyleft licenses..."
    COPYLEFT_PKGS=$(cat .licenses.json | grep -E "GPL-[23]\.0|AGPL" | grep -o '"[^"]*@[^"]*":')

    if [ -n "$COPYLEFT_PKGS" ]; then
        echo "❌ STRONG COPYLEFT licenses found (may require source disclosure):"
        echo "$COPYLEFT_PKGS" | sed 's/"//g' | sed 's/://g' | sed 's/^/  - /'
        echo ""
        echo "⚠️  WARNING: GPL/AGPL licenses may require:"
        echo "  - Source code disclosure"
        echo "  - Same license for derivative works"
        echo "  - Patent grants"
        echo ""
        ISSUES_FOUND=true
    else
        echo "✓ No strong copyleft licenses detected"
    fi

    echo ""

    # Check for weak copyleft licenses
    echo "Checking for weak copyleft licenses..."
    WEAK_COPYLEFT_PKGS=$(cat .licenses.json | grep -E "LGPL|MPL-2\.0" | grep -o '"[^"]*@[^"]*":')

    if [ -n "$WEAK_COPYLEFT_PKGS" ]; then
        echo "⚠️  WEAK COPYLEFT licenses found:"
        echo "$WEAK_COPYLEFT_PKGS" | sed 's/"//g' | sed 's/://g' | sed 's/^/  - /'
        echo ""
        echo "Note: LGPL allows usage if dynamically linked"
        echo "MPL-2.0 requires modified files to be open-sourced"
        echo ""
    else
        echo "✓ No weak copyleft licenses detected"
    fi

    echo ""

    # Check for custom/unknown licenses
    echo "Checking for custom/unknown licenses..."
    CUSTOM_LICENSES=$(cat .licenses.json | grep -o '"licenses":"[^"]*"' | grep -v -E "MIT|Apache|BSD|ISC|GPL|LGPL|MPL|CC0" | grep -v "UNKNOWN")

    if [ -n "$CUSTOM_LICENSES" ]; then
        echo "⚠️  Custom/uncommon licenses found (manual review needed):"
        echo "$CUSTOM_LICENSES" | sed 's/"licenses":"//g' | sed 's/"//g' | sort -u | sed 's/^/  - /'
        echo ""
        ISSUES_FOUND=true
    else
        echo "✓ All licenses are standard OSI-approved"
    fi

    echo ""

    # Check for packages without licenses
    echo "Checking for unlicensed packages..."
    UNLICENSED=$(cat .licenses.json | grep '"licenses":"UNKNOWN\|UNLICENSED"' | grep -o '"[^"]*@[^"]*":')

    if [ -n "$UNLICENSED" ]; then
        echo "❌ Packages without clear licenses:"
        echo "$UNLICENSED" | sed 's/"//g' | sed 's/://g' | sed 's/^/  - /'
        echo ""
        echo "Action: Contact package authors or find alternatives"
        echo ""
        ISSUES_FOUND=true
    else
        echo "✓ All packages have declared licenses"
    fi

    echo ""

    if [ "$ISSUES_FOUND" = true ]; then
        echo "⚠️  License compliance issues detected"
        echo "Review recommendations above"
    else
        echo "✓ No critical license issues found"
        echo "All dependencies use permissive licenses"
    fi

    echo ""
}

detect_license_issues
```

## Phase 3: Python License Analysis

```bash
#!/bin/bash
# Python license checking

check_python_licenses() {
    echo "=== Python License Analysis ==="
    echo ""

    # Install pip-licenses if not available
    if ! command -v pip-licenses &> /dev/null; then
        echo "Installing pip-licenses..."
        pip install pip-licenses
    fi

    # Generate license report
    echo "Scanning Python dependencies..."
    pip-licenses --format=json --with-urls > .pip-licenses.json 2>/dev/null

    if [ ! -f ".pip-licenses.json" ]; then
        echo "❌ Failed to generate license report"
        exit 1
    fi

    echo ""
    echo "=== License Summary ==="
    echo ""

    # Count packages
    total_packages=$(cat .pip-licenses.json | grep -c '"Name":')
    echo "Total packages: $total_packages"
    echo ""

    # License breakdown
    echo "License breakdown:"
    cat .pip-licenses.json | grep -o '"License":"[^"]*"' | sort | uniq -c | sort -rn | while read count license; do
        license_name=$(echo "$license" | cut -d'"' -f4)
        printf "  %-40s %5d\n" "$license_name" "$count"
    done

    echo ""

    # Check for problematic licenses
    echo "Checking for problematic licenses..."

    GPL_PKGS=$(cat .pip-licenses.json | grep -B 1 '"License":".*GPL' | grep '"Name":' | cut -d'"' -f4)

    if [ -n "$GPL_PKGS" ]; then
        echo "⚠️  GPL-licensed packages:"
        echo "$GPL_PKGS" | sed 's/^/  - /'
        echo ""
    else
        echo "✓ No GPL licenses found"
    fi

    rm -f .pip-licenses.json
    echo ""
}

check_python_licenses
```

## Phase 4: License Conflict Detection

```bash
#!/bin/bash
# Detect incompatible license combinations

check_license_conflicts() {
    echo "=== License Conflict Detection ==="
    echo ""

    PROJECT_LICENSE="${1:-MIT}"  # Default to MIT if not specified
    echo "Project license: $PROJECT_LICENSE"
    echo ""

    # Define compatibility rules
    check_compatibility() {
        local project_lic="$1"
        local dep_lic="$2"

        case "$project_lic" in
            MIT|Apache-2.0|BSD-*|ISC)
                # Permissive licenses are compatible with most licenses
                case "$dep_lic" in
                    *GPL*|*AGPL*)
                        echo "CONFLICT"
                        ;;
                    *)
                        echo "OK"
                        ;;
                esac
                ;;
            LGPL-*)
                # LGPL can use MIT/Apache but not GPL
                case "$dep_lic" in
                    GPL-*|AGPL-*)
                        echo "CONFLICT"
                        ;;
                    *)
                        echo "OK"
                        ;;
                esac
                ;;
            GPL-*|AGPL-*)
                # GPL can use anything except incompatible GPL versions
                echo "OK"
                ;;
            *)
                echo "UNKNOWN"
                ;;
        esac
    }

    CONFLICTS_FOUND=false

    # Check each dependency license
    if [ -f ".licenses.json" ]; then
        cat .licenses.json | grep -o '"[^"]*@[^"]*":[^}]*"licenses":"[^"]*"' | while IFS=: read package info; do
            pkg_name=$(echo "$package" | sed 's/"//g')
            dep_license=$(echo "$info" | grep -o '"licenses":"[^"]*"' | cut -d'"' -f4)

            compatibility=$(check_compatibility "$PROJECT_LICENSE" "$dep_license")

            if [ "$compatibility" = "CONFLICT" ]; then
                echo "❌ CONFLICT: $pkg_name ($dep_license)"
                CONFLICTS_FOUND=true
            fi
        done
    fi

    if [ "$CONFLICTS_FOUND" = false ]; then
        echo "✓ No license conflicts detected"
    fi

    echo ""
}

check_license_conflicts "$PROJECT_LICENSE"
```

## Phase 5: Generate Compliance Report

```bash
#!/bin/bash
# Generate comprehensive license compliance report

generate_compliance_report() {
    local output="${1:-LICENSE_COMPLIANCE_REPORT.md}"

    echo "=== Generating Compliance Report ==="
    echo ""

    cat > "$output" << EOF
# License Compliance Report

**Generated:** $(date +"%Y-%m-%d %H:%M:%S")
**Project:** $(basename $(pwd))

## Executive Summary

EOF

    # Add project license
    if [ -f "LICENSE" ]; then
        echo "**Project License:** $(head -5 LICENSE | grep -i -o "MIT\|Apache\|GPL\|BSD\|ISC" | head -1)" >> "$output"
    fi

    echo "" >> "$output"

    # Add statistics
    if [ -f ".licenses.json" ]; then
        total=$(cat .licenses.json | grep -c '"licenses":')
        echo "**Total Dependencies:** $total" >> "$output"
        echo "" >> "$output"

        # License breakdown
        echo "## License Distribution" >> "$output"
        echo "" >> "$output"
        echo "| License | Count |" >> "$output"
        echo "|---------|-------|" >> "$output"

        cat .licenses.json | grep -o '"licenses":"[^"]*"' | sort | uniq -c | sort -rn | while read count license; do
            license_name=$(echo "$license" | cut -d'"' -f4)
            echo "| $license_name | $count |" >> "$output"
        done

        echo "" >> "$output"
    fi

    # Add compliance status
    cat >> "$output" << EOF

## Compliance Status

### ✅ Permissive Licenses (Safe for Commercial Use)
- MIT
- Apache-2.0
- BSD (2-Clause, 3-Clause)
- ISC

### ⚠️  Weak Copyleft (Review Required)
- LGPL (requires dynamic linking)
- MPL-2.0 (modified files must be open-sourced)

### ❌ Strong Copyleft (Commercial Risk)
- GPL-2.0, GPL-3.0
- AGPL-3.0

EOF

    # Add detailed dependency list
    echo "## Detailed Dependency Licenses" >> "$output"
    echo "" >> "$output"

    if [ -f ".licenses.json" ]; then
        echo "| Package | License | Repository |" >> "$output"
        echo "|---------|---------|------------|" >> "$output"

        cat .licenses.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for pkg, info in sorted(data.items()):
    license = info.get('licenses', 'Unknown')
    repo = info.get('repository', 'N/A')
    print(f'| {pkg} | {license} | {repo} |')
" >> "$output" 2>/dev/null
    fi

    echo "" >> "$output"

    # Add recommendations
    cat >> "$output" << EOF

## Recommendations

1. **Document all dependencies** - Maintain THIRD_PARTY_LICENSES file
2. **Monitor license changes** - Run this check before releases
3. **Legal review** - Consult legal counsel for GPL/AGPL dependencies
4. **Update policy** - Define acceptable licenses for the project
5. **Regular audits** - Quarterly license compliance checks

## Action Items

- [ ] Review all copyleft licenses
- [ ] Replace problematic dependencies if necessary
- [ ] Update THIRD_PARTY_LICENSES file
- [ ] Add license checking to CI/CD pipeline
- [ ] Document license compliance policy

## Tools Used

- license-checker (Node.js)
- pip-licenses (Python)
- Manual LICENSE file analysis

## Notes

This report is for informational purposes. Consult legal counsel for
specific compliance questions.

EOF

    echo "✓ Compliance report generated: $output"
    echo ""
}

generate_compliance_report "$1"
```

## Phase 6: THIRD_PARTY_LICENSES Generation

```bash
#!/bin/bash
# Generate THIRD_PARTY_LICENSES file

generate_third_party_licenses() {
    local output="${1:-THIRD_PARTY_LICENSES.txt}"

    echo "=== Generating Third-Party Licenses ==="
    echo ""

    cat > "$output" << EOF
THIRD-PARTY SOFTWARE LICENSES

This file contains the licenses for third-party software used in this project.

Generated: $(date +"%Y-%m-%d")

================================================================================

EOF

    # Node.js dependencies
    if [ -f "package.json" ]; then
        echo "Node.js Dependencies" >> "$output"
        echo "===================" >> "$output"
        echo "" >> "$output"

        license-checker --plainVertical >> "$output" 2>/dev/null
        echo "" >> "$output"
    fi

    # Python dependencies
    if [ -f "requirements.txt" ]; then
        echo "Python Dependencies" >> "$output"
        echo "==================" >> "$output"
        echo "" >> "$output"

        pip-licenses --format=plain-vertical >> "$output" 2>/dev/null
        echo "" >> "$output"
    fi

    echo "✓ Third-party licenses file generated: $output"
    echo ""
}

generate_third_party_licenses "$1"
```

## Phase 7: CI/CD Integration

```bash
#!/bin/bash
# Add license checking to CI/CD

add_license_check_to_ci() {
    echo "=== Adding License Check to CI/CD ==="
    echo ""

    # GitHub Actions workflow
    if [ -d ".github/workflows" ]; then
        cat > .github/workflows/license-check.yml << 'EOF'
name: License Compliance Check

on:
  pull_request:
    branches: [main, master]
  push:
    branches: [main, master]
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  license-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install license-checker
        run: npm install -g license-checker

      - name: Check licenses
        run: |
          license-checker --production --failOn "GPL-2.0;GPL-3.0;AGPL-3.0"

      - name: Generate license report
        if: always()
        run: |
          license-checker --json --production > licenses.json

      - name: Upload license report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: license-report
          path: licenses.json
EOF

        echo "✓ GitHub Actions workflow created"
    fi

    # Pre-commit hook
    if [ -d ".git/hooks" ]; then
        cat > .git/hooks/pre-commit-license-check << 'EOF'
#!/bin/bash
# Pre-commit license compliance check

echo "Checking license compliance..."

if [ -f "package.json" ]; then
    license-checker --production --failOn "GPL-2.0;GPL-3.0;AGPL-3.0" || {
        echo ""
        echo "❌ License compliance check failed!"
        echo "Run: /license-check to review licenses"
        exit 1
    }
fi

echo "✓ License compliance check passed"
EOF

        chmod +x .git/hooks/pre-commit-license-check
        echo "✓ Pre-commit hook created"
    fi

    echo ""
}

add_license_check_to_ci
```

## Practical Examples

**Full compliance check:**
```bash
/license-check
/license-check --report
```

**Specific focus:**
```bash
/license-check --commercial      # Check for commercial compatibility
/license-check --gpl             # Find GPL licenses
/license-check --conflicts       # Detect conflicts
```

**Generate documentation:**
```bash
/license-check --generate-report
/license-check --third-party-licenses
```

## Best Practices

**License Management:**
- ✅ Check licenses before adding dependencies
- ✅ Document all third-party software
- ✅ Review licenses quarterly
- ✅ Update LICENSE file when dependencies change
- ✅ Automate checks in CI/CD

**Red Flags:**
- ❌ GPL/AGPL in proprietary software
- ❌ Unlicensed dependencies
- ❌ Custom licenses without review
- ❌ License changes in updates

## Integration Points

- `/dependency-audit` - Combined security and license audit
- `/ci-setup` - Add license checks to CI pipeline
- `/docs` - Generate compliance documentation

## What I'll Actually Do

1. **Detect licenses** - Scan all dependencies
2. **Categorize** - Group by license type
3. **Find conflicts** - Check compatibility
4. **Generate reports** - Create compliance documentation
5. **Provide guidance** - Actionable recommendations

**Important:** I will NEVER:
- Provide legal advice (consult a lawyer)
- Ignore license violations
- Auto-accept copyleft licenses
- Add AI attribution

All license analysis will be thorough, accurate, and well-documented. This is informational only - consult legal counsel for compliance decisions.

**Credits:** Based on license-checker, pip-licenses, and OSI license compatibility guidelines.
