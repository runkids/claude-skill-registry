---
name: dependency-audit
description: Comprehensive dependency security and license audit
disable-model-invocation: true
---

# Dependency Security & License Audit

I'll perform comprehensive security and license audits of your project dependencies, identifying vulnerabilities, license issues, and outdated packages.

Arguments: `$ARGUMENTS` - specific packages, severity level, or audit focus

## Audit Philosophy

- **Security First**: Identify all vulnerabilities
- **License Compliance**: Ensure legal compatibility
- **Supply Chain Security**: Verify package integrity
- **Update Strategy**: Safe upgrade paths

**Token Optimization:**
- Uses package manager commands (minimal tokens)
- Grep for specific patterns (100 tokens)
- Expected: 500-1,000 tokens

## Phase 1: Dependency Detection

First, let me detect your package managers and dependencies:

```bash
#!/bin/bash
# Detect package managers and dependency files

detect_package_managers() {
    echo "=== Package Manager Detection ==="
    echo ""

    MANAGERS=()

    # Node.js / npm/yarn/pnpm
    if [ -f "package.json" ]; then
        echo "✓ Node.js project detected"
        if [ -f "package-lock.json" ]; then
            MANAGERS+=("npm")
        elif [ -f "yarn.lock" ]; then
            MANAGERS+=("yarn")
        elif [ -f "pnpm-lock.yaml" ]; then
            MANAGERS+=("pnpm")
        else
            MANAGERS+=("npm")
        fi
    fi

    # Python / pip/poetry/pipenv
    if [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
        echo "✓ Python project detected"
        if [ -f "poetry.lock" ]; then
            MANAGERS+=("poetry")
        elif [ -f "Pipfile" ]; then
            MANAGERS+=("pipenv")
        else
            MANAGERS+=("pip")
        fi
    fi

    # Ruby / bundler
    if [ -f "Gemfile" ]; then
        echo "✓ Ruby project detected"
        MANAGERS+=("bundler")
    fi

    # Go / go modules
    if [ -f "go.mod" ]; then
        echo "✓ Go project detected"
        MANAGERS+=("go")
    fi

    # Rust / cargo
    if [ -f "Cargo.toml" ]; then
        echo "✓ Rust project detected"
        MANAGERS+=("cargo")
    fi

    # PHP / composer
    if [ -f "composer.json" ]; then
        echo "✓ PHP project detected"
        MANAGERS+=("composer")
    fi

    echo ""
    echo "Package managers: ${MANAGERS[@]}"
    echo ""
}

detect_package_managers
```

## Phase 2: Security Vulnerability Audit

Scan for known security vulnerabilities:

### npm/yarn/pnpm Audit

```bash
#!/bin/bash
# Security audit for Node.js projects

npm_security_audit() {
    echo "=== npm Security Audit ==="
    echo ""

    # Run npm audit
    echo "Running npm audit..."
    npm audit --json > .audit-report.json 2>/dev/null

    # Parse results
    CRITICAL=$(cat .audit-report.json | grep -o '"critical":[0-9]*' | grep -o '[0-9]*')
    HIGH=$(cat .audit-report.json | grep -o '"high":[0-9]*' | grep -o '[0-9]*')
    MODERATE=$(cat .audit-report.json | grep -o '"moderate":[0-9]*' | grep -o '[0-9]*')
    LOW=$(cat .audit-report.json | grep -o '"low":[0-9]*' | grep -o '[0-9]*')

    echo "Vulnerability Summary:"
    echo "  Critical: ${CRITICAL:-0}"
    echo "  High:     ${HIGH:-0}"
    echo "  Moderate: ${MODERATE:-0}"
    echo "  Low:      ${LOW:-0}"
    echo ""

    # Check if any critical or high vulnerabilities
    if [ "${CRITICAL:-0}" -gt 0 ] || [ "${HIGH:-0}" -gt 0 ]; then
        echo "❌ CRITICAL/HIGH vulnerabilities found!"
        echo ""
        echo "Detailed report:"
        npm audit

        echo ""
        echo "Fix suggestions:"
        echo "  1. Run: npm audit fix"
        echo "  2. For breaking changes: npm audit fix --force"
        echo "  3. Manual review: npm audit"
    else
        echo "✓ No critical or high severity vulnerabilities"
    fi

    # Check for outdated packages
    echo ""
    echo "Outdated packages:"
    npm outdated

    rm -f .audit-report.json
}

npm_security_audit
```

### Python pip-audit

```bash
#!/bin/bash
# Security audit for Python projects

python_security_audit() {
    echo "=== Python Security Audit ==="
    echo ""

    # Install pip-audit if not available
    if ! command -v pip-audit &> /dev/null; then
        echo "Installing pip-audit..."
        pip install pip-audit
    fi

    # Run audit
    echo "Running pip-audit..."
    pip-audit --format=json > .pip-audit.json 2>/dev/null

    # Parse results
    VULN_COUNT=$(cat .pip-audit.json | grep -c '"id":' || echo 0)

    if [ "$VULN_COUNT" -gt 0 ]; then
        echo "❌ $VULN_COUNT vulnerabilities found!"
        echo ""
        pip-audit

        echo ""
        echo "Fix suggestions:"
        echo "  1. Update packages: pip install --upgrade <package>"
        echo "  2. Review: pip-audit --desc"
    else
        echo "✓ No vulnerabilities detected"
    fi

    # Check outdated packages
    echo ""
    echo "Outdated packages:"
    pip list --outdated

    rm -f .pip-audit.json
}

python_security_audit
```

### Comprehensive Multi-Language Audit

```bash
#!/bin/bash
# Universal security audit script

comprehensive_security_audit() {
    echo "=== Comprehensive Security Audit ==="
    echo ""

    # Create audit report
    AUDIT_REPORT="SECURITY_AUDIT_$(date +%Y%m%d_%H%M%S).md"

    cat > "$AUDIT_REPORT" << EOF
# Security Audit Report

**Date**: $(date +%Y-%m-%d)
**Project**: $(basename $(pwd))

## Executive Summary

EOF

    # Node.js
    if [ -f "package.json" ]; then
        echo "## Node.js Dependencies" >> "$AUDIT_REPORT"
        echo "" >> "$AUDIT_REPORT"
        echo "Running npm audit..." >> "$AUDIT_REPORT"
        echo '```' >> "$AUDIT_REPORT"
        npm audit >> "$AUDIT_REPORT" 2>&1 || true
        echo '```' >> "$AUDIT_REPORT"
        echo "" >> "$AUDIT_REPORT"
    fi

    # Python
    if [ -f "requirements.txt" ]; then
        echo "## Python Dependencies" >> "$AUDIT_REPORT"
        echo "" >> "$AUDIT_REPORT"
        if command -v pip-audit &> /dev/null; then
            echo "Running pip-audit..." >> "$AUDIT_REPORT"
            echo '```' >> "$AUDIT_REPORT"
            pip-audit >> "$AUDIT_REPORT" 2>&1 || true
            echo '```' >> "$AUDIT_REPORT"
        else
            echo "pip-audit not installed. Run: pip install pip-audit" >> "$AUDIT_REPORT"
        fi
        echo "" >> "$AUDIT_REPORT"
    fi

    # Ruby
    if [ -f "Gemfile" ]; then
        echo "## Ruby Dependencies" >> "$AUDIT_REPORT"
        echo "" >> "$AUDIT_REPORT"
        echo "Running bundle audit..." >> "$AUDIT_REPORT"
        echo '```' >> "$AUDIT_REPORT"
        bundle audit >> "$AUDIT_REPORT" 2>&1 || true
        echo '```' >> "$AUDIT_REPORT"
        echo "" >> "$AUDIT_REPORT"
    fi

    # Go
    if [ -f "go.mod" ]; then
        echo "## Go Dependencies" >> "$AUDIT_REPORT"
        echo "" >> "$AUDIT_REPORT"
        echo "Running govulncheck..." >> "$AUDIT_REPORT"
        echo '```' >> "$AUDIT_REPORT"
        go list -json -m all | govulncheck >> "$AUDIT_REPORT" 2>&1 || true
        echo '```' >> "$AUDIT_REPORT"
        echo "" >> "$AUDIT_REPORT"
    fi

    echo "✓ Audit report generated: $AUDIT_REPORT"
}

comprehensive_security_audit
```

## Phase 3: License Compliance Audit

Check for license compatibility issues:

```bash
#!/bin/bash
# License compliance audit

license_audit() {
    echo "=== License Compliance Audit ==="
    echo ""

    # Problematic licenses for commercial use
    COPYLEFT_LICENSES=("GPL" "AGPL" "LGPL")
    RESTRICTED_LICENSES=("CC-BY-NC" "Commons Clause")

    # Node.js license check
    if [ -f "package.json" ]; then
        echo "Checking Node.js package licenses..."

        # Install license-checker if not available
        if ! command -v license-checker &> /dev/null; then
            npm install -g license-checker
        fi

        # Generate license report
        license-checker --json > .licenses.json

        # Check for problematic licenses
        for license in "${COPYLEFT_LICENSES[@]}"; do
            if grep -q "\"licenses\":.*\"$license" .licenses.json; then
                echo "⚠️  WARNING: Copyleft license found: $license"
                grep -B 2 "\"licenses\":.*\"$license" .licenses.json | grep -o '"[^"]*@[^"]*":' | sed 's/"//g' | sed 's/://g'
            fi
        done

        # Generate summary
        echo ""
        echo "License Summary:"
        cat .licenses.json | grep -o '"licenses":"[^"]*"' | sort | uniq -c | sort -rn

        rm -f .licenses.json
    fi

    # Python license check
    if [ -f "requirements.txt" ]; then
        echo ""
        echo "Checking Python package licenses..."

        pip-licenses --format=json > .pip-licenses.json 2>/dev/null

        # Check for problematic licenses
        for license in "${COPYLEFT_LICENSES[@]}"; do
            if grep -q "$license" .pip-licenses.json; then
                echo "⚠️  WARNING: Copyleft license found: $license"
                grep -B 1 "$license" .pip-licenses.json | grep "Name" | sed 's/"Name": "//g' | sed 's/",//g'
            fi
        done

        echo ""
        echo "License Summary:"
        cat .pip-licenses.json | grep -o '"License":"[^"]*"' | sort | uniq -c | sort -rn

        rm -f .pip-licenses.json
    fi
}

license_audit
```

**Detailed License Report:**

```bash
#!/bin/bash
# Generate detailed license report

generate_license_report() {
    REPORT="LICENSE_AUDIT_$(date +%Y%m%d).md"

    cat > "$REPORT" << EOF
# License Compliance Report

**Date**: $(date +%Y-%m-%d)
**Project**: $(basename $(pwd))

## License Classification

### Permissive Licenses (✅ Safe for commercial use)
- MIT
- Apache-2.0
- BSD-2-Clause, BSD-3-Clause
- ISC

### Weak Copyleft (⚠️ Review required)
- LGPL (requires dynamic linking)
- MPL-2.0

### Strong Copyleft (❌ Avoid for proprietary software)
- GPL-2.0, GPL-3.0
- AGPL-3.0

### Unknown/Custom (⚠️ Manual review required)
- Custom licenses
- Unlicensed packages

## Dependencies by License

EOF

    if [ -f "package.json" ]; then
        echo "### Node.js Dependencies" >> "$REPORT"
        echo "" >> "$REPORT"
        license-checker --markdown >> "$REPORT" 2>/dev/null || echo "Install: npm install -g license-checker" >> "$REPORT"
        echo "" >> "$REPORT"
    fi

    if [ -f "requirements.txt" ]; then
        echo "### Python Dependencies" >> "$REPORT"
        echo "" >> "$REPORT"
        pip-licenses --format=markdown >> "$REPORT" 2>/dev/null || echo "Install: pip install pip-licenses" >> "$REPORT"
        echo "" >> "$REPORT"
    fi

    cat >> "$REPORT" << EOF

## Recommendations

1. **Review all GPL/AGPL licenses** - May require source disclosure
2. **Document all dependencies** - Maintain in THIRD_PARTY_LICENSES
3. **Update policy** - Define acceptable licenses for the project
4. **Regular audits** - Run quarterly license audits

## Compliance Checklist

- [ ] All dependencies documented
- [ ] License files included in distribution
- [ ] Attribution requirements met
- [ ] No incompatible licenses
- [ ] Legal review completed
EOF

    echo "✓ License report generated: $REPORT"
}

generate_license_report
```

## Phase 4: Supply Chain Security

Verify package integrity and authenticity:

```bash
#!/bin/bash
# Supply chain security checks

supply_chain_audit() {
    echo "=== Supply Chain Security Audit ==="
    echo ""

    # Check for known malicious packages
    echo "Checking for known malicious packages..."

    # Node.js
    if [ -f "package.json" ]; then
        # Check package integrity
        echo "Verifying npm package integrity..."
        npm audit signatures 2>&1 || echo "Note: Signature verification requires npm 8.15.0+"

        # Check for suspicious dependencies
        echo ""
        echo "Checking for suspicious patterns..."

        # Look for packages with no repository
        npx npm-check -u --json | grep '"repository": null' && {
            echo "⚠️  WARNING: Packages without repository found"
        }

        # Check for deprecated packages
        echo ""
        echo "Checking for deprecated packages..."
        npm ls --depth=0 2>&1 | grep -i "deprecated" || echo "No deprecated packages"
    fi

    # Check for typosquatting
    echo ""
    echo "Checking for potential typosquatting..."
    check_typosquatting
}

check_typosquatting() {
    # Common typosquatting patterns
    POPULAR_PACKAGES=("react" "express" "lodash" "axios" "webpack")

    if [ -f "package.json" ]; then
        for pkg in "${POPULAR_PACKAGES[@]}"; do
            # Look for similar package names
            grep -i "$pkg" package.json | grep -v "\"$pkg\":" && {
                echo "⚠️  Potential typosquatting: Check packages similar to $pkg"
            }
        done
    fi
}

supply_chain_audit
```

## Phase 5: Outdated Package Analysis

Identify and prioritize package updates:

```bash
#!/bin/bash
# Analyze outdated packages and create update plan

analyze_outdated_packages() {
    echo "=== Outdated Package Analysis ==="
    echo ""

    UPDATE_PLAN="UPDATE_PLAN_$(date +%Y%m%d).md"

    cat > "$UPDATE_PLAN" << EOF
# Dependency Update Plan

**Date**: $(date +%Y-%m-%d)

## Priority 1: Security Updates (Immediate)

EOF

    if [ -f "package.json" ]; then
        echo "### Node.js Dependencies" >> "$UPDATE_PLAN"
        echo "" >> "$UPDATE_PLAN"

        # Get outdated with security flag
        npm outdated --json > .outdated.json 2>/dev/null

        echo "| Package | Current | Latest | Type |" >> "$UPDATE_PLAN"
        echo "|---------|---------|--------|------|" >> "$UPDATE_PLAN"

        # Parse outdated packages
        cat .outdated.json | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    for pkg, info in data.items():
        current = info.get('current', 'N/A')
        latest = info.get('latest', 'N/A')
        pkg_type = info.get('type', 'N/A')
        print(f'| {pkg} | {current} | {latest} | {pkg_type} |')
except:
    pass
" >> "$UPDATE_PLAN" 2>/dev/null

        echo "" >> "$UPDATE_PLAN"

        rm -f .outdated.json
    fi

    cat >> "$UPDATE_PLAN" << EOF

## Priority 2: Major Version Updates (Review Required)

## Priority 3: Minor/Patch Updates (Low Risk)

## Update Strategy

1. **Test in staging** - All updates must pass tests in staging
2. **One at a time** - Update major versions individually
3. **Review changelogs** - Check breaking changes
4. **Monitor** - Watch for issues after deployment

## Automated Update Commands

\`\`\`bash
# Update all patch and minor versions (safe)
npm update

# Update specific package
npm install <package>@latest

# Update all (including major versions - review first!)
npx npm-check-updates -u
npm install
\`\`\`
EOF

    echo "✓ Update plan generated: $UPDATE_PLAN"
}

analyze_outdated_packages
```

## Phase 6: Continuous Monitoring

Set up automated dependency monitoring:

```bash
#!/bin/bash
# Set up continuous dependency monitoring

setup_monitoring() {
    echo "=== Setting up Dependency Monitoring ==="
    echo ""

    # GitHub Dependabot
    if [ -d ".github" ]; then
        echo "Creating Dependabot configuration..."
        mkdir -p .github

        cat > .github/dependabot.yml << EOF
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
EOF

        echo "✓ Dependabot configured"
    fi

    # Pre-commit hook for audit
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit dependency audit

echo "Running dependency audit..."
if [ -f "package.json" ]; then
    npm audit --audit-level=high || {
        echo "❌ High/Critical vulnerabilities detected!"
        echo "Run: npm audit fix"
        exit 1
    }
fi

echo "✓ Dependency audit passed"
EOF

    chmod +x .git/hooks/pre-commit
    echo "✓ Pre-commit hook installed"
}

setup_monitoring
```

## Practical Examples

**Full Audit:**
```bash
/dependency-audit              # Complete audit
/dependency-audit --critical   # Only critical issues
/dependency-audit --licenses   # License audit only
```

**Specific Focus:**
```bash
/dependency-audit security     # Security vulnerabilities
/dependency-audit outdated     # Outdated packages
/dependency-audit supply-chain # Supply chain risks
```

**Generate Reports:**
```bash
/dependency-audit --report     # Generate full report
/dependency-audit --export     # Export to JSON/CSV
```

## Best Practices

**Regular Audits:**
- ✅ Run audits before releases
- ✅ Weekly automated scans
- ✅ Review before adding new dependencies
- ✅ Monitor security advisories

**Update Strategy:**
- ✅ Patch updates: Apply immediately
- ✅ Minor updates: Weekly review
- ✅ Major updates: Quarterly planning
- ✅ Breaking changes: Dedicated sprint

## What I'll Actually Do

1. **Detect dependencies** - Find all package managers
2. **Security scan** - Check for vulnerabilities
3. **License audit** - Verify compliance
4. **Supply chain check** - Validate integrity
5. **Update analysis** - Prioritize upgrades
6. **Generate reports** - Comprehensive documentation

**Important:** I will NEVER:
- Auto-update without confirmation
- Skip vulnerability disclosure
- Ignore license incompatibilities
- Add AI attribution

All audits will be thorough, well-documented, and actionable.

**Credits:** Based on industry-standard dependency audit tools: npm audit, pip-audit, bundler-audit, and OWASP dependency-check.
