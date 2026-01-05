---
name: security-checklist
description: Prevents RCE, SQL injection, and common vulnerabilities through validation and safe coding practices. Use when implementing or reviewing security-sensitive code involving user input, database queries, or command execution.
---

# Security Checklist

## Instructions

### Critical prohibitions

**NEVER:**
- `eval()`, `exec()` with user input (RCE risk)
- `os.system()`, `subprocess` with `shell=True` and user input
- SQL string interpolation (injection risk)
- Unvalidated file paths

**ALWAYS:**
- Validate inputs (type, range, format)
- Use parameterized queries
- Hash passwords (bcrypt, argon2)

## Example

<!-- CUSTOMIZE: Add examples for {{MAIN_TECH_STACK}} -->

### Python
```python
# ❌ DANGEROUS
eval(request.json['code'])  # RCE!
query = f"SELECT * FROM users WHERE id = '{user_id}'"  # SQL injection!

# ✅ SAFE
ALLOWED = {'add': lambda a,b: a+b}
if op in ALLOWED:
    result = ALLOWED[op](a, b)

query = "SELECT * FROM users WHERE id = %s"
db.execute(query, (user_id,))
```

### JavaScript/Node.js
```javascript
// ❌ DANGEROUS
eval(req.body.code);  // RCE!
const query = `SELECT * FROM users WHERE id = '${userId}'`;  // SQL injection!

// ✅ SAFE
const ALLOWED = {add: (a,b) => a+b};
if (ALLOWED[op]) {
    result = ALLOWED[op](a, b);
}

const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

### Go
```go
// ❌ DANGEROUS
cmd := exec.Command("sh", "-c", userInput)  // RCE!
query := fmt.Sprintf("SELECT * FROM users WHERE id = '%s'", userId)  // SQL injection!

// ✅ SAFE
var allowed = map[string]func(int, int) int{
    "add": func(a, b int) int { return a + b },
}
if fn, ok := allowed[op]; ok {
    result = fn(a, b)
}

query := "SELECT * FROM users WHERE id = ?"
db.Query(query, userId)
```

## OWASP Top 10 Coverage

### 1. Injection (SQL, NoSQL, Command, LDAP)

**Vulnerable:**
```{{LANG}}
# SQL Injection
query = "SELECT * FROM users WHERE name = '" + userName + "'"

# Command Injection
os.system("ping " + userIP)

# NoSQL Injection
db.find({"user": req.body.user})  # MongoDB
```

**Secure:**
```{{LANG}}
# Parameterized SQL
query = "SELECT * FROM users WHERE name = ?"
db.execute(query, [userName])

# Allowlist validation + safe execution
if re.match(r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$', userIP):
    subprocess.run(["ping", "-c", "1", userIP], shell=False)

# Strict schema validation
if (typeof req.body.user === 'string') {
    db.find({user: req.body.user})
}
```

---

### 2. Broken Authentication

**Vulnerable:**
```{{LANG}}
# Weak password storage
password = hashlib.md5(password).hexdigest()  # MD5 broken!

# No rate limiting
if user.password == input_password:  # Brute force vulnerability
```

**Secure:**
```{{LANG}}
# Strong hashing
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Rate limiting
from flask_limiter import Limiter
@limiter.limit("5 per minute")
def login():
    ...
```

---

### 3. Sensitive Data Exposure

**Vulnerable:**
```{{LANG}}
# Plaintext secrets in code
API_KEY = "sk_live_abc123xyz"  # Hardcoded!

# Logging sensitive data
logger.info(f"User password: {password}")  # Password in logs!
```

**Secure:**
```{{LANG}}
# Environment variables
import os
API_KEY = os.getenv('API_KEY')

# Masked logging
logger.info(f"User: {username}, Password: [REDACTED]")
```

---

### 4. XML External Entities (XXE)

**Vulnerable:**
```{{LANG}}
# Python lxml (unsafe)
parser = etree.XMLParser()
doc = etree.parse(user_file, parser)

# Java (unsafe)
DocumentBuilderFactory.newInstance().newDocumentBuilder().parse(input);
```

**Secure:**
```{{LANG}}
# Python (safe)
parser = etree.XMLParser(resolve_entities=False, no_network=True)
doc = etree.parse(user_file, parser)

# Java (safe)
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
```

---

### 5. Broken Access Control

**Vulnerable:**
```{{LANG}}
# No authorization check
@app.route('/admin/users')
def admin_users():
    return User.query.all()  # Anyone can access!

# IDOR (Insecure Direct Object Reference)
@app.route('/user/<id>')
def get_user(id):
    return User.query.get(id)  # No ownership check!
```

**Secure:**
```{{LANG}}
# Role-based access control
@app.route('/admin/users')
@require_role('admin')
def admin_users():
    return User.query.all()

# Verify ownership
@app.route('/user/<id>')
def get_user(id):
    user = User.query.get(id)
    if user.id != current_user.id and not current_user.is_admin:
        abort(403)
    return user
```

---

### 6. Security Misconfiguration

**Vulnerable:**
```{{LANG}}
# Debug mode in production
app.run(debug=True)  # Exposes stack traces!

# Default credentials
DB_PASSWORD = "admin123"  # Weak default!
```

**Secure:**
```{{LANG}}
# Production configuration
app.run(debug=False, host='0.0.0.0')

# Strong credentials from environment
DB_PASSWORD = os.getenv('DB_PASSWORD')
if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD must be set")
```

---

### 7. Cross-Site Scripting (XSS)

**Vulnerable:**
```{{LANG}}
# Unescaped output (Python/Flask)
return f"<h1>Hello {user_name}</h1>"  # user_name = "<script>alert('XSS')</script>"

# Unsafe HTML (JavaScript)
div.innerHTML = userName;  # XSS!
```

**Secure:**
```{{LANG}}
# Auto-escaping (Flask Jinja2)
return render_template('hello.html', name=user_name)
# Template: <h1>Hello {{ name }}</h1>  (auto-escaped)

# Text content only (JavaScript)
div.textContent = userName;  // Safe

# Or sanitize HTML
import DOMPurify from 'dompurify';
div.innerHTML = DOMPurify.sanitize(userHTML);
```

---

### 8. Insecure Deserialization

**Vulnerable:**
```{{LANG}}
# Python pickle (unsafe)
import pickle
data = pickle.loads(user_input)  # RCE!

# YAML (unsafe)
import yaml
config = yaml.load(user_file)  # RCE!
```

**Secure:**
```{{LANG}}
# JSON only
import json
data = json.loads(user_input)  # Safe (no code execution)

# Safe YAML
config = yaml.safe_load(user_file)  # Restricted types
```

---

### 9. Using Components with Known Vulnerabilities

**Vulnerable:**
```
# Outdated dependencies
requests==2.6.0  # Has CVE-2015-2296!
```

**Secure:**
```bash
# Regular updates
pip install --upgrade requests

# Vulnerability scanning
pip install safety
safety check

# Or npm
npm audit
npm audit fix
```

---

### 10. Insufficient Logging & Monitoring

**Vulnerable:**
```{{LANG}}
# No security event logging
if auth_failed:
    return "Invalid credentials"  # Silent failure
```

**Secure:**
```{{LANG}}
# Log security events
if auth_failed:
    logger.warning(f"Failed login for user: {username}, IP: {request.remote_addr}")
    # Alert after N failures
    if failed_attempts > 5:
        alert_security_team(username, request.remote_addr)
    return "Invalid credentials"
```

---

## Checklist

```markdown
[ ] No eval/exec with user input?
[ ] SQL queries parameterized?
[ ] File paths validated?
[ ] All inputs validated?
[ ] Passwords hashed (bcrypt/argon2)?
[ ] Secrets in environment variables?
[ ] Authentication with rate limiting?
[ ] Authorization checks on all endpoints?
[ ] XSS prevention (auto-escaping)?
[ ] Deserialization uses safe formats (JSON)?
[ ] Dependencies regularly updated?
[ ] Security events logged?
```

## Additional Security Considerations

### File Upload Security
```{{LANG}}
# ✅ Safe file upload
from werkzeug.utils import secure_filename

# Validate extension
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
if not file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
    abort(400)

# Secure filename
filename = secure_filename(file.filename)

# Limit file size
if len(file.read()) > 5 * 1024 * 1024:  # 5MB
    abort(400)

# Store outside web root
file.save(os.path.join('/var/uploads', filename))
```

### CSRF Protection
```{{LANG}}
# Flask-WTF (automatic CSRF)
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# Or manual token validation
if request.form['csrf_token'] != session['csrf_token']:
    abort(403)
```

### HTTPS/TLS
```{{LANG}}
# Force HTTPS (Flask)
from flask_talisman import Talisman
Talisman(app, force_https=True)

# Secure cookies
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

---

**For detailed guidelines, see [reference.md](reference.md)**
**For more examples, see [examples.md](examples.md)**
