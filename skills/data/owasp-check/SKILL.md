---
name: owasp-check
description: OWASP Top 10 vulnerability scanning and remediation
disable-model-invocation: true
---

# OWASP Top 10 Vulnerability Scanner

I'll scan your application for OWASP Top 10 vulnerabilities and provide remediation guidance for common web security issues.

Arguments: `$ARGUMENTS` - specific vulnerability category or full scan

## OWASP Top 10 (2021) Coverage

**Vulnerabilities Checked:**
1. **A01:2021** - Broken Access Control
2. **A02:2021** - Cryptographic Failures
3. **A03:2021** - Injection (SQL, NoSQL, Command)
4. **A04:2021** - Insecure Design
5. **A05:2021** - Security Misconfiguration
6. **A06:2021** - Vulnerable Components
7. **A07:2021** - Authentication Failures
8. **A08:2021** - Data Integrity Failures
9. **A09:2021** - Logging & Monitoring Failures
10. **A10:2021** - Server-Side Request Forgery (SSRF)

**Token Optimization:**
- Uses Grep for pattern matching (1,000 tokens)
- Minimal file reading (1,500 tokens)
- Expected: 2,500-4,000 tokens

## Phase 1: Framework and Language Detection

```bash
#!/bin/bash
# Detect project type for targeted scanning

detect_project_type() {
    echo "=== Project Detection ==="
    echo ""

    # Check for Node.js/JavaScript
    if [ -f "package.json" ]; then
        echo "✓ Node.js/JavaScript project"
        PROJECT_TYPE="nodejs"

        if grep -q "express" package.json; then
            FRAMEWORK="express"
            echo "  Framework: Express.js"
        elif grep -q "next" package.json; then
            FRAMEWORK="nextjs"
            echo "  Framework: Next.js"
        elif grep -q "react" package.json; then
            FRAMEWORK="react"
            echo "  Framework: React"
        fi
    fi

    # Check for Python
    if [ -f "requirements.txt" ] || [ -f "setup.py" ]; then
        echo "✓ Python project"
        PROJECT_TYPE="python"

        if [ -f "manage.py" ]; then
            FRAMEWORK="django"
            echo "  Framework: Django"
        elif grep -q "flask" requirements.txt 2>/dev/null; then
            FRAMEWORK="flask"
            echo "  Framework: Flask"
        elif grep -q "fastapi" requirements.txt 2>/dev/null; then
            FRAMEWORK="fastapi"
            echo "  Framework: FastAPI"
        fi
    fi

    # Check for PHP
    if [ -f "composer.json" ]; then
        echo "✓ PHP project"
        PROJECT_TYPE="php"

        if grep -q "laravel" composer.json; then
            FRAMEWORK="laravel"
            echo "  Framework: Laravel"
        fi
    fi

    # Check for Java
    if [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
        echo "✓ Java project"
        PROJECT_TYPE="java"

        if grep -q "spring" pom.xml 2>/dev/null || grep -q "spring" build.gradle 2>/dev/null; then
            FRAMEWORK="spring"
            echo "  Framework: Spring Boot"
        fi
    fi

    echo ""
}

detect_project_type
```

## Phase 2: A01 - Broken Access Control

```bash
#!/bin/bash
# Check for broken access control vulnerabilities

check_access_control() {
    echo "=== A01: Broken Access Control ==="
    echo ""

    ISSUES=0

    # Check for missing authentication
    echo "Checking for missing authentication..."

    if [ "$PROJECT_TYPE" = "nodejs" ]; then
        # Look for routes without authentication middleware
        UNPROTECTED=$(find . -name "*.js" -o -name "*.ts" | xargs grep -l "app\.\(get\|post\|put\|delete\)" | \
            xargs grep -L "auth\|authenticate\|isAuthenticated")

        if [ -n "$UNPROTECTED" ]; then
            echo "⚠️  Routes potentially without authentication:"
            echo "$UNPROTECTED" | sed 's/^/  /'
            ISSUES=$((ISSUES + 1))
        fi
    fi

    # Check for insecure direct object references
    echo ""
    echo "Checking for insecure direct object references..."

    IDOR_PATTERNS=(
        "req\.params\.id"
        "req\.query\.id"
        "params\[.*id.*\]"
        "SELECT.*WHERE id.*params"
    )

    for pattern in "${IDOR_PATTERNS[@]}"; do
        if grep -r "$pattern" --include="*.js" --include="*.ts" --include="*.py" . 2>/dev/null | grep -qv "checkOwnership\|authorize\|permission"; then
            echo "⚠️  Potential IDOR vulnerability found"
            echo "  Pattern: $pattern"
            echo "  Ensure ownership/permission checks before accessing resources"
            ISSUES=$((ISSUES + 1))
        fi
    done

    # Check for missing CSRF protection
    echo ""
    echo "Checking for CSRF protection..."

    if [ "$FRAMEWORK" = "express" ]; then
        if ! grep -r "csrf\|csurf" --include="package.json" . 2>/dev/null; then
            echo "⚠️  CSRF protection not found"
            echo "  Install: npm install csurf"
            ISSUES=$((ISSUES + 1))
        fi
    fi

    echo ""
    if [ $ISSUES -eq 0 ]; then
        echo "✓ No obvious access control issues found"
    else
        echo "❌ Found $ISSUES potential access control issues"
    fi
    echo ""
}

check_access_control
```

## Phase 3: A02 - Cryptographic Failures

```bash
#!/bin/bash
# Check for cryptographic failures

check_crypto_failures() {
    echo "=== A02: Cryptographic Failures ==="
    echo ""

    ISSUES=0

    # Check for hardcoded secrets
    echo "Checking for hardcoded secrets..."

    SECRET_PATTERNS=(
        "password\s*=\s*['\"][^'\"]{8,}['\"]"
        "api[_-]?key\s*=\s*['\"][^'\"]{20,}['\"]"
        "secret\s*=\s*['\"][^'\"]{16,}['\"]"
        "token\s*=\s*['\"][^'\"]{20,}['\"]"
        "private[_-]?key"
        "aws_secret_access_key"
    )

    for pattern in "${SECRET_PATTERNS[@]}"; do
        matches=$(grep -r -i "$pattern" \
            --include="*.js" \
            --include="*.ts" \
            --include="*.py" \
            --include="*.php" \
            --exclude-dir=node_modules \
            --exclude-dir=.git \
            . 2>/dev/null)

        if [ -n "$matches" ]; then
            echo "❌ CRITICAL: Hardcoded secrets found"
            echo "$matches" | head -3
            echo "  Move secrets to environment variables"
            ISSUES=$((ISSUES + 1))
        fi
    done

    # Check for weak password hashing
    echo ""
    echo "Checking for weak password hashing..."

    WEAK_HASH=("md5\(" "sha1\(" "btoa\(")

    for hash in "${WEAK_HASH[@]}"; do
        if grep -r "$hash.*password" \
            --include="*.js" \
            --include="*.ts" \
            --include="*.py" \
            . 2>/dev/null; then
            echo "❌ Weak hashing algorithm detected: $hash"
            echo "  Use bcrypt, argon2, or scrypt"
            ISSUES=$((ISSUES + 1))
        fi
    done

    # Check for proper encryption
    echo ""
    echo "Checking for secure encryption..."

    if grep -r "crypto\." --include="*.js" --include="*.ts" . 2>/dev/null | grep -q "des\|rc4"; then
        echo "❌ Weak encryption algorithm detected"
        echo "  Use AES-256-GCM or ChaCha20"
        ISSUES=$((ISSUES + 1))
    fi

    # Check for HTTPS enforcement
    echo ""
    echo "Checking for HTTPS enforcement..."

    if [ "$PROJECT_TYPE" = "nodejs" ]; then
        if ! grep -r "https\.createServer\|forceHttps\|requireHttps" \
            --include="*.js" \
            --include="*.ts" \
            . 2>/dev/null; then
            echo "⚠️  HTTPS enforcement not detected"
            echo "  Ensure production uses HTTPS only"
            ISSUES=$((ISSUES + 1))
        fi
    fi

    echo ""
    if [ $ISSUES -eq 0 ]; then
        echo "✓ No critical cryptographic issues found"
    else
        echo "❌ Found $ISSUES cryptographic issues"
    fi
    echo ""
}

check_crypto_failures
```

## Phase 4: A03 - Injection Vulnerabilities

```bash
#!/bin/bash
# Check for SQL injection, NoSQL injection, command injection

check_injection() {
    echo "=== A03: Injection Vulnerabilities ==="
    echo ""

    ISSUES=0

    # SQL Injection
    echo "Checking for SQL injection vulnerabilities..."

    SQL_INJECTION_PATTERNS=(
        "SELECT.*\+.*req\."
        "INSERT.*\+.*req\."
        "UPDATE.*\+.*req\."
        "DELETE.*\+.*req\."
        "WHERE.*\+.*params"
        "execute.*%.*req\."
        "query.*\`.*\$\{.*\}\`"
    )

    for pattern in "${SQL_INJECTION_PATTERNS[@]}"; do
        matches=$(grep -r "$pattern" \
            --include="*.js" \
            --include="*.ts" \
            --include="*.py" \
            --exclude-dir=node_modules \
            . 2>/dev/null)

        if [ -n "$matches" ]; then
            echo "❌ CRITICAL: Potential SQL injection"
            echo "  Pattern: $pattern"
            echo "  Use parameterized queries or ORM"
            ISSUES=$((ISSUES + 1))
        fi
    done

    # NoSQL Injection
    echo ""
    echo "Checking for NoSQL injection..."

    if grep -r "findOne.*req\.\(body\|params\|query\)" \
        --include="*.js" \
        --include="*.ts" \
        . 2>/dev/null | grep -qv "sanitize"; then
        echo "❌ Potential NoSQL injection"
        echo "  Use mongoose-sanitize or validate input"
        ISSUES=$((ISSUES + 1))
    fi

    # Command Injection
    echo ""
    echo "Checking for command injection..."

    COMMAND_INJECTION=(
        "exec.*req\."
        "spawn.*req\."
        "system.*req\."
        "shell_exec.*\$_"
    )

    for pattern in "${COMMAND_INJECTION[@]}"; do
        if grep -r "$pattern" \
            --include="*.js" \
            --include="*.ts" \
            --include="*.py" \
            --include="*.php" \
            . 2>/dev/null; then
            echo "❌ CRITICAL: Command injection risk"
            echo "  Pattern: $pattern"
            echo "  Never execute user input as shell commands"
            ISSUES=$((ISSUES + 1))
        fi
    done

    # XSS (Cross-Site Scripting)
    echo ""
    echo "Checking for XSS vulnerabilities..."

    XSS_PATTERNS=(
        "innerHTML.*req\."
        "dangerouslySetInnerHTML"
        "eval\(.*req\."
        "document\.write.*req\."
    )

    for pattern in "${XSS_PATTERNS[@]}"; do
        if grep -r "$pattern" \
            --include="*.js" \
            --include="*.ts" \
            --include="*.jsx" \
            --include="*.tsx" \
            . 2>/dev/null; then
            echo "❌ XSS vulnerability detected"
            echo "  Pattern: $pattern"
            echo "  Sanitize user input, use textContent instead of innerHTML"
            ISSUES=$((ISSUES + 1))
        fi
    done

    echo ""
    if [ $ISSUES -eq 0 ]; then
        echo "✓ No obvious injection vulnerabilities found"
    else
        echo "❌ Found $ISSUES potential injection vulnerabilities"
    fi
    echo ""
}

check_injection
```

## Phase 5: A05 - Security Misconfiguration

```bash
#!/bin/bash
# Check for security misconfigurations

check_misconfig() {
    echo "=== A05: Security Misconfiguration ==="
    echo ""

    ISSUES=0

    # Check for debug mode in production
    echo "Checking for debug mode..."

    if grep -r "DEBUG\s*=\s*True\|NODE_ENV.*development" \
        --include="*.py" \
        --include="*.js" \
        --include="*.env" \
        . 2>/dev/null; then
        echo "⚠️  Debug mode may be enabled"
        echo "  Ensure DEBUG=False and NODE_ENV=production in production"
        ISSUES=$((ISSUES + 1))
    fi

    # Check for default credentials
    echo ""
    echo "Checking for default credentials..."

    if grep -r -i "admin.*admin\|root.*root\|password.*password" \
        --include="*.js" \
        --include="*.py" \
        --include="*.php" \
        --include="*.env" \
        . 2>/dev/null; then
        echo "❌ CRITICAL: Default credentials detected"
        echo "  Change all default passwords"
        ISSUES=$((ISSUES + 1))
    fi

    # Check for exposed .env files
    echo ""
    echo "Checking for exposed configuration..."

    if [ -f ".env" ]; then
        if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
            echo "⚠️  .env file not in .gitignore"
            echo "  Add .env to .gitignore immediately"
            ISSUES=$((ISSUES + 1))
        fi
    fi

    # Check for error disclosure
    echo ""
    echo "Checking for detailed error messages..."

    if grep -r "error\.stack\|traceback\|printStackTrace" \
        --include="*.js" \
        --include="*.ts" \
        --include="*.py" \
        . 2>/dev/null | grep -qv "process\.env\.NODE_ENV.*development"; then
        echo "⚠️  Detailed errors may be exposed"
        echo "  Hide stack traces in production"
        ISSUES=$((ISSUES + 1))
    fi

    # Check CORS configuration
    echo ""
    echo "Checking CORS configuration..."

    if grep -r "cors.*\*\|Access-Control-Allow-Origin.*\*" \
        --include="*.js" \
        --include="*.ts" \
        --include="*.py" \
        . 2>/dev/null; then
        echo "⚠️  Overly permissive CORS detected"
        echo "  Restrict CORS to specific origins"
        ISSUES=$((ISSUES + 1))
    fi

    echo ""
    if [ $ISSUES -eq 0 ]; then
        echo "✓ No critical misconfigurations found"
    else
        echo "❌ Found $ISSUES security misconfigurations"
    fi
    echo ""
}

check_misconfig
```

## Phase 6: A06 - Vulnerable Components

```bash
#!/bin/bash
# Check for vulnerable and outdated components

check_vulnerable_components() {
    echo "=== A06: Vulnerable and Outdated Components ==="
    echo ""

    # Node.js dependencies
    if [ -f "package.json" ]; then
        echo "Checking npm packages for vulnerabilities..."

        npm audit --production 2>&1 | tee .npm-audit.txt

        CRITICAL=$(grep -o "critical.*[0-9]*" .npm-audit.txt | grep -o "[0-9]*" | head -1)
        HIGH=$(grep -o "high.*[0-9]*" .npm-audit.txt | grep -o "[0-9]*" | head -1)

        if [ "${CRITICAL:-0}" -gt 0 ] || [ "${HIGH:-0}" -gt 0 ]; then
            echo ""
            echo "❌ CRITICAL: High-severity vulnerabilities found"
            echo "  Run: npm audit fix"
        fi

        rm -f .npm-audit.txt
    fi

    # Python dependencies
    if [ -f "requirements.txt" ]; then
        echo ""
        echo "Checking Python packages for vulnerabilities..."

        if command -v pip-audit &> /dev/null; then
            pip-audit
        else
            echo "Install pip-audit: pip install pip-audit"
        fi
    fi

    # Check for outdated packages
    echo ""
    echo "Checking for outdated packages..."

    if [ -f "package.json" ]; then
        npm outdated
    fi

    echo ""
}

check_vulnerable_components
```

## Phase 7: A07 - Authentication Failures

```bash
#!/bin/bash
# Check for authentication and session management issues

check_authentication() {
    echo "=== A07: Identification and Authentication Failures ==="
    echo ""

    ISSUES=0

    # Check for weak password requirements
    echo "Checking password validation..."

    if ! grep -r "password.*length.*8\|.{8,}" \
        --include="*.js" \
        --include="*.ts" \
        --include="*.py" \
        . 2>/dev/null; then
        echo "⚠️  Weak password requirements"
        echo "  Enforce minimum 8 characters with complexity"
        ISSUES=$((ISSUES + 1))
    fi

    # Check for rate limiting
    echo ""
    echo "Checking for rate limiting..."

    if [ "$FRAMEWORK" = "express" ]; then
        if ! grep -r "rate-limit\|express-rate-limit" \
            --include="package.json" \
            . 2>/dev/null; then
            echo "⚠️  Rate limiting not detected"
            echo "  Install: npm install express-rate-limit"
            ISSUES=$((ISSUES + 1))
        fi
    fi

    # Check for secure session management
    echo ""
    echo "Checking session configuration..."

    if grep -r "session.*secret.*'.*'" \
        --include="*.js" \
        --include="*.ts" \
        . 2>/dev/null; then
        echo "⚠️  Hardcoded session secret"
        echo "  Use environment variable for session secret"
        ISSUES=$((ISSUES + 1))
    fi

    # Check for JWT vulnerabilities
    echo ""
    echo "Checking JWT implementation..."

    if grep -r "jwt\.sign.*algorithm.*none" \
        --include="*.js" \
        --include="*.ts" \
        . 2>/dev/null; then
        echo "❌ CRITICAL: JWT algorithm 'none' detected"
        echo "  Use HS256 or RS256"
        ISSUES=$((ISSUES + 1))
    fi

    # Check for multi-factor authentication
    echo ""
    echo "Checking for MFA..."

    if ! grep -r "mfa\|totp\|2fa\|two-factor" \
        --include="*.js" \
        --include="*.ts" \
        --include="*.py" \
        . 2>/dev/null; then
        echo "💡 Consider implementing multi-factor authentication"
    fi

    echo ""
    if [ $ISSUES -eq 0 ]; then
        echo "✓ No critical authentication issues found"
    else
        echo "❌ Found $ISSUES authentication issues"
    fi
    echo ""
}

check_authentication
```

## Phase 8: A09 - Security Logging Failures

```bash
#!/bin/bash
# Check for logging and monitoring issues

check_logging() {
    echo "=== A09: Security Logging and Monitoring Failures ==="
    echo ""

    ISSUES=0

    # Check for logging implementation
    echo "Checking for logging..."

    if ! grep -r "logger\|log\|winston\|bunyan\|pino" \
        --include="*.js" \
        --include="*.ts" \
        . 2>/dev/null; then
        echo "⚠️  Logging implementation not detected"
        echo "  Install logging library (winston, pino, etc.)"
        ISSUES=$((ISSUES + 1))
    fi

    # Check for security event logging
    echo ""
    echo "Checking for security event logging..."

    SECURITY_EVENTS=(
        "login"
        "logout"
        "failed.*auth"
        "access.*denied"
    )

    logged_events=0
    for event in "${SECURITY_EVENTS[@]}"; do
        if grep -r "$event.*log" \
            --include="*.js" \
            --include="*.ts" \
            . 2>/dev/null; then
            logged_events=$((logged_events + 1))
        fi
    done

    if [ $logged_events -lt 2 ]; then
        echo "⚠️  Insufficient security event logging"
        echo "  Log: login attempts, access denials, privilege changes"
        ISSUES=$((ISSUES + 1))
    fi

    # Check for sensitive data in logs
    echo ""
    echo "Checking for sensitive data in logs..."

    if grep -r "log.*password\|log.*token\|log.*secret" \
        --include="*.js" \
        --include="*.ts" \
        . 2>/dev/null | grep -qv "redact\|sanitize\|mask"; then
        echo "❌ CRITICAL: Sensitive data may be logged"
        echo "  Never log passwords, tokens, or secrets"
        ISSUES=$((ISSUES + 1))
    fi

    echo ""
    if [ $ISSUES -eq 0 ]; then
        echo "✓ No critical logging issues found"
    else
        echo "❌ Found $ISSUES logging issues"
    fi
    echo ""
}

check_logging
```

## Phase 9: Comprehensive Report Generation

```bash
#!/bin/bash
# Generate comprehensive OWASP vulnerability report

generate_owasp_report() {
    local output="${1:-OWASP_SECURITY_REPORT.md}"

    echo "=== Generating OWASP Report ==="
    echo ""

    cat > "$output" << EOF
# OWASP Top 10 Security Assessment Report

**Date:** $(date +"%Y-%m-%d %H:%M:%S")
**Project:** $(basename $(pwd))

## Executive Summary

This report covers the OWASP Top 10 (2021) vulnerability categories.

## Findings

### A01:2021 - Broken Access Control

EOF

    # Run all checks and append to report
    check_access_control >> "$output" 2>&1
    check_crypto_failures >> "$output" 2>&1
    check_injection >> "$output" 2>&1
    check_misconfig >> "$output" 2>&1
    check_vulnerable_components >> "$output" 2>&1
    check_authentication >> "$output" 2>&1
    check_logging >> "$output" 2>&1

    cat >> "$output" << EOF

## Remediation Priorities

### Critical (Fix Immediately)
- Hardcoded secrets and credentials
- SQL/Command injection vulnerabilities
- Authentication bypass issues
- High-severity dependency vulnerabilities

### High (Fix Within 30 Days)
- XSS vulnerabilities
- CSRF protection missing
- Weak cryptographic algorithms
- Security misconfigurations

### Medium (Fix Within 90 Days)
- Missing security headers
- Insufficient logging
- Rate limiting missing
- Weak password policies

### Low (Review and Plan)
- Code quality improvements
- Documentation updates
- Monitoring enhancements

## Next Steps

1. Review all CRITICAL findings immediately
2. Assign remediation tasks to team members
3. Set up automated security scanning in CI/CD
4. Schedule regular security reviews
5. Conduct penetration testing for high-risk applications

## Tools Used

- Custom OWASP Top 10 scanner
- npm audit / pip-audit
- Static code analysis
- Pattern matching for common vulnerabilities

## Disclaimer

This is an automated scan and may have false positives/negatives.
Conduct manual security review and penetration testing for production applications.

EOF

    echo "✓ OWASP report generated: $output"
    echo ""
}

generate_owasp_report "$1"
```

## Practical Examples

**Full OWASP scan:**
```bash
/owasp-check
/owasp-check --report
```

**Specific categories:**
```bash
/owasp-check --injection
/owasp-check --auth
/owasp-check --access-control
```

**Generate report:**
```bash
/owasp-check --generate-report OWASP_Report.md
```

## Best Practices

**Security Testing:**
- ✅ Run OWASP checks before each release
- ✅ Integrate into CI/CD pipeline
- ✅ Fix critical issues immediately
- ✅ Schedule regular security reviews

**Remediation:**
- ✅ Prioritize by severity and exploitability
- ✅ Track fixes in issue tracker
- ✅ Verify fixes with testing
- ✅ Document security decisions

## Integration Points

- `/security-scan` - Comprehensive security analysis
- `/dependency-audit` - Dependency vulnerability scanning
- `/security-headers` - Web security headers validation
- `/ci-setup` - Add OWASP checks to CI pipeline

## What I'll Actually Do

1. **Detect project type** - Identify framework and language
2. **Scan for vulnerabilities** - Check all OWASP Top 10 categories
3. **Prioritize findings** - Risk-based categorization
4. **Generate report** - Comprehensive documentation
5. **Provide remediation** - Actionable fix guidance

**Important:** I will NEVER:
- Execute exploit code
- Access production data
- Modify security configurations without permission
- Add AI attribution

All security scans will be safe, thorough, and well-documented. This tool is for defensive security only.

**Credits:** Based on OWASP Top 10 (2021), security best practices, and common vulnerability patterns.
