---
name: security-headers
description: Web security headers validation and configuration generation
disable-model-invocation: true
---

# Security Headers Validation

I'll analyze and implement web security headers (CSP, HSTS, X-Frame-Options, etc.) to protect against common attacks.

Arguments: `$ARGUMENTS` - URL to check, or framework for configuration generation

## Security Headers Overview

**Essential Headers:**
- **Content-Security-Policy (CSP)** - Prevent XSS and injection attacks
- **Strict-Transport-Security (HSTS)** - Enforce HTTPS
- **X-Frame-Options** - Prevent clickjacking
- **X-Content-Type-Options** - Prevent MIME sniffing
- **Referrer-Policy** - Control referrer information
- **Permissions-Policy** - Feature access control

**Token Optimization:**
- Uses curl for header inspection (200 tokens)
- Framework detection via Grep (100 tokens)
- Expected: 2,000-3,500 tokens

## Phase 1: Header Detection and Analysis

```bash
#!/bin/bash
# Check current security headers

check_security_headers() {
    local url="${1:-http://localhost:3000}"

    echo "=== Security Headers Analysis ==="
    echo "URL: $url"
    echo ""

    # Fetch headers
    echo "Fetching headers..."
    HEADERS=$(curl -sI "$url" 2>/dev/null)

    if [ -z "$HEADERS" ]; then
        echo "❌ Failed to fetch headers from $url"
        echo "Make sure the server is running"
        exit 1
    fi

    echo ""
    echo "=== Security Header Status ==="
    echo ""

    # Check each security header
    check_header "Content-Security-Policy" "CSP"
    check_header "Strict-Transport-Security" "HSTS"
    check_header "X-Frame-Options" "Clickjacking Protection"
    check_header "X-Content-Type-Options" "MIME Sniffing Protection"
    check_header "X-XSS-Protection" "XSS Protection"
    check_header "Referrer-Policy" "Referrer Policy"
    check_header "Permissions-Policy" "Permissions Policy"

    echo ""
    echo "=== Security Score ==="
    calculate_security_score
    echo ""
}

check_header() {
    local header_name="$1"
    local description="$2"

    if echo "$HEADERS" | grep -iq "^$header_name:"; then
        header_value=$(echo "$HEADERS" | grep -i "^$header_name:" | cut -d: -f2- | xargs)
        echo "✓ $description"
        echo "  $header_name: $header_value"
    else
        echo "❌ $description - MISSING"
        echo "  $header_name: Not set"
    fi
    echo ""
}

calculate_security_score() {
    local score=0
    local total=7

    echo "$HEADERS" | grep -iq "^Content-Security-Policy:" && score=$((score + 1))
    echo "$HEADERS" | grep -iq "^Strict-Transport-Security:" && score=$((score + 1))
    echo "$HEADERS" | grep -iq "^X-Frame-Options:" && score=$((score + 1))
    echo "$HEADERS" | grep -iq "^X-Content-Type-Options:" && score=$((score + 1))
    echo "$HEADERS" | grep -iq "^X-XSS-Protection:" && score=$((score + 1))
    echo "$HEADERS" | grep -iq "^Referrer-Policy:" && score=$((score + 1))
    echo "$HEADERS" | grep -iq "^Permissions-Policy:" && score=$((score + 1))

    local percentage=$((score * 100 / total))

    echo "Score: $score/$total ($percentage%)"

    if [ $percentage -ge 90 ]; then
        echo "Grade: A - Excellent security"
    elif [ $percentage -ge 70 ]; then
        echo "Grade: B - Good, but room for improvement"
    elif [ $percentage -ge 50 ]; then
        echo "Grade: C - Needs improvement"
    else
        echo "Grade: F - Poor security posture"
    fi
}

check_security_headers "$1"
```

## Phase 2: Detailed Header Analysis

```bash
#!/bin/bash
# Analyze specific security header configurations

analyze_csp() {
    local csp_header=$(echo "$HEADERS" | grep -i "^Content-Security-Policy:" | cut -d: -f2- | xargs)

    echo "=== Content Security Policy Analysis ==="
    echo ""

    if [ -z "$csp_header" ]; then
        echo "❌ CSP header not set"
        echo ""
        echo "Risks:"
        echo "  - XSS attacks possible"
        echo "  - Code injection vulnerabilities"
        echo "  - Data exfiltration possible"
        return
    fi

    echo "Current CSP:"
    echo "$csp_header"
    echo ""

    # Check for unsafe directives
    echo "Security Review:"

    if echo "$csp_header" | grep -q "'unsafe-inline'"; then
        echo "⚠️  WARNING: 'unsafe-inline' detected"
        echo "   Allows inline scripts/styles (reduces XSS protection)"
    fi

    if echo "$csp_header" | grep -q "'unsafe-eval'"; then
        echo "⚠️  WARNING: 'unsafe-eval' detected"
        echo "   Allows eval() (significant security risk)"
    fi

    if echo "$csp_header" | grep -q "\*"; then
        echo "⚠️  WARNING: Wildcard (*) sources detected"
        echo "   Too permissive, reduce scope"
    fi

    if echo "$csp_header" | grep -q "default-src 'self'"; then
        echo "✓ Good: default-src 'self' set (restricts to same origin)"
    fi

    if echo "$csp_header" | grep -q "script-src"; then
        echo "✓ Good: script-src defined (controls script sources)"
    else
        echo "⚠️  Missing: script-src directive"
    fi

    if echo "$csp_header" | grep -q "img-src"; then
        echo "✓ Good: img-src defined"
    fi

    echo ""
}

analyze_hsts() {
    local hsts_header=$(echo "$HEADERS" | grep -i "^Strict-Transport-Security:" | cut -d: -f2- | xargs)

    echo "=== HSTS Analysis ==="
    echo ""

    if [ -z "$hsts_header" ]; then
        echo "❌ HSTS header not set"
        echo ""
        echo "Risks:"
        echo "  - Man-in-the-middle attacks"
        echo "  - Protocol downgrade attacks"
        echo "  - No HTTPS enforcement"
        return
    fi

    echo "Current HSTS:"
    echo "$hsts_header"
    echo ""

    # Parse max-age
    max_age=$(echo "$hsts_header" | grep -o "max-age=[0-9]*" | cut -d= -f2)

    if [ -n "$max_age" ]; then
        echo "Max-age: $max_age seconds"

        # Convert to days
        days=$((max_age / 86400))
        echo "  ($days days)"

        if [ $days -ge 365 ]; then
            echo "✓ Good: max-age >= 1 year (recommended)"
        else
            echo "⚠️  Warning: max-age < 1 year (consider 31536000)"
        fi
    fi

    if echo "$hsts_header" | grep -q "includeSubDomains"; then
        echo "✓ Good: includeSubDomains set"
    else
        echo "⚠️  Consider: includeSubDomains"
    fi

    if echo "$hsts_header" | grep -q "preload"; then
        echo "✓ Excellent: preload directive set"
    else
        echo "💡 Optional: Add 'preload' for HSTS preload list"
    fi

    echo ""
}

analyze_frame_options() {
    local frame_header=$(echo "$HEADERS" | grep -i "^X-Frame-Options:" | cut -d: -f2- | xargs)

    echo "=== X-Frame-Options Analysis ==="
    echo ""

    if [ -z "$frame_header" ]; then
        echo "❌ X-Frame-Options not set"
        echo ""
        echo "Risks:"
        echo "  - Clickjacking attacks"
        echo "  - UI redressing"
        return
    fi

    echo "Current setting: $frame_header"
    echo ""

    case "${frame_header,,}" in
        deny)
            echo "✓ Excellent: DENY (prevents all framing)"
            ;;
        sameorigin)
            echo "✓ Good: SAMEORIGIN (allows same-origin framing)"
            ;;
        allow-from*)
            echo "⚠️  Warning: ALLOW-FROM is deprecated"
            echo "   Use CSP frame-ancestors instead"
            ;;
        *)
            echo "⚠️  Unknown value"
            ;;
    esac

    echo ""
}

# Run analyses
analyze_csp
analyze_hsts
analyze_frame_options
```

## Phase 3: Framework-Specific Configuration

### Express.js (Node.js)

```javascript
// middleware/security-headers.js
const helmet = require('helmet');

/**
 * Security headers middleware for Express.js
 * Using Helmet for comprehensive security header management
 */
module.exports = function securityHeaders(app) {
  // Use Helmet with custom configuration
  app.use(
    helmet({
      // Content Security Policy
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: [
            "'self'",
            "'unsafe-inline'", // Remove if possible, use nonces instead
            "https://trusted-cdn.com"
          ],
          styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
          imgSrc: ["'self'", "data:", "https:"],
          fontSrc: ["'self'", "https://fonts.gstatic.com"],
          connectSrc: ["'self'", "https://api.example.com"],
          frameSrc: ["'none'"],
          objectSrc: ["'none'"],
          upgradeInsecureRequests: [],
        },
      },

      // Strict Transport Security (HSTS)
      strictTransportSecurity: {
        maxAge: 31536000, // 1 year
        includeSubDomains: true,
        preload: true,
      },

      // X-Frame-Options
      frameguard: {
        action: 'deny',
      },

      // X-Content-Type-Options
      noSniff: true,

      // Referrer-Policy
      referrerPolicy: {
        policy: 'strict-origin-when-cross-origin',
      },

      // Permissions-Policy (formerly Feature-Policy)
      permissionsPolicy: {
        features: {
          geolocation: ["'self'"],
          microphone: ["'none'"],
          camera: ["'none'"],
          payment: ["'self'"],
        },
      },

      // Remove X-Powered-By header
      hidePoweredBy: true,

      // DNS Prefetch Control
      dnsPrefetchControl: {
        allow: false,
      },

      // IE No Open
      ieNoOpen: true,

      // X-XSS-Protection (legacy, CSP is preferred)
      xssFilter: true,
    })
  );

  // Additional custom headers
  app.use((req, res, next) => {
    // Cross-Origin policies
    res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
    res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
    res.setHeader('Cross-Origin-Resource-Policy', 'same-origin');

    next();
  });
};
```

**Installation script:**

```bash
#!/bin/bash
# Install and configure Helmet for Express.js

install_helmet() {
    echo "=== Installing Helmet for Express.js ==="
    echo ""

    # Install Helmet
    npm install helmet

    # Create security headers middleware
    mkdir -p middleware

    cat > middleware/security-headers.js << 'EOF'
const helmet = require('helmet');

module.exports = function securityHeaders(app) {
  app.use(
    helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: ["'self'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          imgSrc: ["'self'", "data:", "https:"],
          fontSrc: ["'self'"],
          connectSrc: ["'self'"],
          frameSrc: ["'none'"],
          objectSrc: ["'none'"],
        },
      },
      strictTransportSecurity: {
        maxAge: 31536000,
        includeSubDomains: true,
        preload: true,
      },
      frameguard: { action: 'deny' },
      referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
    })
  );
};
EOF

    echo "✓ Helmet middleware created: middleware/security-headers.js"
    echo ""
    echo "Add to your Express app:"
    echo ""
    echo "  const securityHeaders = require('./middleware/security-headers');"
    echo "  securityHeaders(app);"
    echo ""
}

install_helmet
```

### Next.js

```javascript
// next.config.js
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: [
      "default-src 'self'",
      "script-src 'self' 'unsafe-eval' 'unsafe-inline'",
      "style-src 'self' 'unsafe-inline'",
      "img-src 'self' data: https:",
      "font-src 'self'",
      "connect-src 'self'",
      "frame-src 'none'",
      "object-src 'none'",
    ].join('; '),
  },
  {
    key: 'Strict-Transport-Security',
    value: 'max-age=31536000; includeSubDomains; preload',
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY',
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff',
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin',
  },
  {
    key: 'Permissions-Policy',
    value: 'geolocation=(), microphone=(), camera=()',
  },
];

module.exports = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: securityHeaders,
      },
    ];
  },
};
```

### Nginx

```nginx
# nginx-security-headers.conf
# Add to your nginx server block

# Content Security Policy
add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-src 'none'; object-src 'none';" always;

# Strict Transport Security
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

# X-Frame-Options
add_header X-Frame-Options "DENY" always;

# X-Content-Type-Options
add_header X-Content-Type-Options "nosniff" always;

# X-XSS-Protection (legacy)
add_header X-XSS-Protection "1; mode=block" always;

# Referrer Policy
add_header Referrer-Policy "strict-origin-when-cross-origin" always;

# Permissions Policy
add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

# Cross-Origin policies
add_header Cross-Origin-Opener-Policy "same-origin" always;
add_header Cross-Origin-Embedder-Policy "require-corp" always;
add_header Cross-Origin-Resource-Policy "same-origin" always;

# Remove server version
server_tokens off;
```

### Apache

```apache
# .htaccess or httpd.conf
# Security headers for Apache

<IfModule mod_headers.c>
    # Content Security Policy
    Header always set Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-src 'none'; object-src 'none';"

    # Strict Transport Security
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"

    # X-Frame-Options
    Header always set X-Frame-Options "DENY"

    # X-Content-Type-Options
    Header always set X-Content-Type-Options "nosniff"

    # X-XSS-Protection
    Header always set X-XSS-Protection "1; mode=block"

    # Referrer Policy
    Header always set Referrer-Policy "strict-origin-when-cross-origin"

    # Permissions Policy
    Header always set Permissions-Policy "geolocation=(), microphone=(), camera=()"

    # Remove server signature
    Header unset Server
    Header unset X-Powered-By
</IfModule>

ServerSignature Off
ServerTokens Prod
```

## Phase 4: CSP Nonce Generation

```javascript
// middleware/csp-nonce.js
const crypto = require('crypto');

/**
 * Generate CSP nonces for inline scripts and styles
 * More secure than 'unsafe-inline'
 */
module.exports = function cspNonce(req, res, next) {
  // Generate random nonce
  const nonce = crypto.randomBytes(16).toString('base64');

  // Store nonce in locals for use in templates
  res.locals.cspNonce = nonce;

  // Set CSP header with nonce
  res.setHeader(
    'Content-Security-Policy',
    `default-src 'self'; ` +
    `script-src 'self' 'nonce-${nonce}'; ` +
    `style-src 'self' 'nonce-${nonce}'; ` +
    `img-src 'self' data: https:; ` +
    `font-src 'self'; ` +
    `connect-src 'self'; ` +
    `frame-src 'none'; ` +
    `object-src 'none';`
  );

  next();
};
```

**Usage in templates:**

```html
<!-- EJS example -->
<script nonce="<%= cspNonce %>">
  // Your inline script
  console.log('This script is allowed by CSP nonce');
</script>

<style nonce="<%= cspNonce %>">
  /* Your inline styles */
  body { margin: 0; }
</style>
```

## Phase 5: Testing Security Headers

```bash
#!/bin/bash
# Automated security header testing

test_security_headers() {
    local url="$1"

    echo "=== Security Header Testing ==="
    echo "URL: $url"
    echo ""

    # Test suite
    tests_passed=0
    tests_failed=0

    run_test() {
        local header="$1"
        local description="$2"

        if curl -sI "$url" | grep -iq "^$header:"; then
            echo "✓ $description"
            tests_passed=$((tests_passed + 1))
        else
            echo "❌ $description"
            tests_failed=$((tests_failed + 1))
        fi
    }

    run_test "Content-Security-Policy" "CSP header present"
    run_test "Strict-Transport-Security" "HSTS header present"
    run_test "X-Frame-Options" "X-Frame-Options present"
    run_test "X-Content-Type-Options" "X-Content-Type-Options present"
    run_test "Referrer-Policy" "Referrer-Policy present"
    run_test "Permissions-Policy" "Permissions-Policy present"

    echo ""
    echo "=== Test Results ==="
    echo "Passed: $tests_passed"
    echo "Failed: $tests_failed"
    echo ""

    if [ $tests_failed -eq 0 ]; then
        echo "✓ All security headers configured correctly"
        exit 0
    else
        echo "❌ Some security headers are missing"
        exit 1
    fi
}

test_security_headers "$1"
```

## Phase 6: Online Tools Integration

```bash
#!/bin/bash
# Use online security header scanners

check_with_online_tools() {
    local url="$1"

    echo "=== Online Security Header Scanners ==="
    echo ""

    echo "Check your site with these tools:"
    echo ""
    echo "1. Security Headers: https://securityheaders.com/?q=$url"
    echo "2. Mozilla Observatory: https://observatory.mozilla.org/analyze/$url"
    echo "3. CSP Evaluator: https://csp-evaluator.withgoogle.com/"
    echo ""

    # Try to fetch and display Security Headers grade
    if command -v curl &> /dev/null && command -v jq &> /dev/null; then
        echo "Fetching Security Headers analysis..."
        curl -s "https://securityheaders.com/?q=$url&followRedirects=on" | grep -o "grade-[A-F]" | head -1 | cut -d- -f2
    fi
}

check_with_online_tools "$1"
```

## Practical Examples

**Check headers:**
```bash
/security-headers https://example.com
/security-headers http://localhost:3000
```

**Generate config:**
```bash
/security-headers --express
/security-headers --nextjs
/security-headers --nginx
```

**Test implementation:**
```bash
/security-headers --test https://example.com
```

## Best Practices

**CSP Implementation:**
- ✅ Start with restrictive policy, relax as needed
- ✅ Use nonces or hashes instead of 'unsafe-inline'
- ✅ Avoid 'unsafe-eval'
- ✅ Test thoroughly before deploying

**HSTS Configuration:**
- ✅ Use max-age >= 31536000 (1 year)
- ✅ Include includeSubDomains
- ✅ Add to HSTS preload list
- ✅ Test on non-production first

**Common Mistakes:**
- ❌ Too permissive CSP (using * wildcards)
- ❌ Short HSTS max-age values
- ❌ Missing headers on some routes
- ❌ Not testing in all browsers

## Integration Points

- `/security-scan` - Comprehensive security analysis
- `/ci-setup` - Add header validation to CI
- `/deploy-validate` - Verify headers before deployment

## What I'll Actually Do

1. **Analyze current headers** - Check what's configured
2. **Identify gaps** - Find missing security headers
3. **Generate configuration** - Framework-specific setup
4. **Provide guidance** - Implementation instructions
5. **Test implementation** - Verify headers work correctly

**Important:** I will NEVER:
- Generate overly permissive policies
- Skip CSP configuration
- Ignore framework differences
- Add AI attribution

All security header configurations will be strict, tested, and well-documented.

**Credits:** Based on OWASP security header best practices and Mozilla Observatory recommendations.
