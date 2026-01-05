---
name: forms
description: HTML5 forms, Constraint Validation API, accessible form patterns, and modern input types
sasmp_version: "1.3.0"
bonded_agent: html-expert
bond_type: PRIMARY_BOND
version: "2.0.0"

# Skill Metadata
category: forms
complexity: intermediate
dependencies:
  - html-basics
  - accessibility

# Parameter Validation
parameters:
  form_type:
    type: string
    required: true
    enum: [contact, login, registration, search, checkout, survey, multi-step]
  validation_mode:
    type: string
    default: "html5"
    enum: [html5, javascript, hybrid]
  accessibility_level:
    type: string
    default: "AA"
    enum: ["A", "AA", "AAA"]

# Retry Configuration
retry:
  max_attempts: 3
  backoff_ms: [1000, 2000, 4000]
  retryable_errors: [VALIDATION_ERROR, PARSE_ERROR]
---

# Forms Skill

Production-grade HTML5 forms with Constraint Validation API and accessible patterns.

## 🎯 Purpose

Provide atomic, single-responsibility operations for:
- Form structure and layout
- Input types and validation
- Constraint Validation API usage
- Accessible form patterns
- Error handling and display
- Multi-step form logic

---

## 📥 Input Schema

```typescript
interface FormsInput {
  operation: 'create' | 'validate' | 'pattern' | 'convert';
  form_type: FormType;
  fields?: FieldDefinition[];
  options?: {
    validation_mode: 'html5' | 'javascript' | 'hybrid';
    accessibility_level: 'A' | 'AA' | 'AAA';
    autocomplete: boolean;
    novalidate: boolean;
  };
}

type FormType =
  | 'contact'       // Name, email, message
  | 'login'         // Email/username, password
  | 'registration'  // Full user signup
  | 'search'        // Search input
  | 'checkout'      // Payment form
  | 'survey'        // Questions, ratings
  | 'multi-step';   // Wizard-style form

interface FieldDefinition {
  name: string;
  type: InputType;
  label: string;
  required?: boolean;
  pattern?: string;
  validation?: ValidationRule[];
}
```

## 📤 Output Schema

```typescript
interface FormsOutput {
  success: boolean;
  markup: string;
  validation_script?: string;
  accessibility_score: number;
  issues: FormIssue[];
}
```

---

## 🛠️ Core Patterns

### 1. Input Types Reference

| Type | Purpose | Validation | Keyboard |
|------|---------|------------|----------|
| `text` | Generic text | pattern | text |
| `email` | Email address | Built-in email | email |
| `password` | Passwords | pattern | text |
| `tel` | Phone numbers | pattern | tel |
| `url` | URLs | Built-in URL | url |
| `number` | Numeric values | min/max/step | numeric |
| `date` | Date picker | min/max | date |
| `time` | Time picker | min/max/step | time |
| `datetime-local` | Date + time | min/max | datetime |
| `search` | Search queries | None | search |
| `color` | Color picker | None | - |
| `range` | Slider | min/max/step | - |
| `file` | File upload | accept | - |

### 2. Complete Form Template

```html
<form id="contact-form"
      action="/api/contact"
      method="POST"
      novalidate
      aria-labelledby="form-title">

  <h2 id="form-title">Contact Us</h2>

  <!-- Error Summary (initially hidden) -->
  <div id="error-summary"
       role="alert"
       aria-live="polite"
       hidden>
    <h3>Please fix the following errors:</h3>
    <ul id="error-list"></ul>
  </div>

  <!-- Name Field -->
  <div class="field">
    <label for="name">
      Full Name
      <span class="required" aria-hidden="true">*</span>
    </label>
    <input type="text"
           id="name"
           name="name"
           required
           aria-required="true"
           autocomplete="name"
           aria-describedby="name-hint">
    <p id="name-hint" class="hint">Enter your full name</p>
    <p id="name-error" class="error" aria-live="polite"></p>
  </div>

  <!-- Email Field -->
  <div class="field">
    <label for="email">
      Email
      <span class="required" aria-hidden="true">*</span>
    </label>
    <input type="email"
           id="email"
           name="email"
           required
           aria-required="true"
           autocomplete="email"
           aria-describedby="email-hint email-error">
    <p id="email-hint" class="hint">We'll never share your email</p>
    <p id="email-error" class="error" aria-live="polite"></p>
  </div>

  <!-- Message Field -->
  <div class="field">
    <label for="message">
      Message
      <span class="required" aria-hidden="true">*</span>
    </label>
    <textarea id="message"
              name="message"
              rows="5"
              required
              aria-required="true"
              minlength="10"
              maxlength="1000"
              aria-describedby="message-hint message-count"></textarea>
    <p id="message-hint" class="hint">10-1000 characters</p>
    <p id="message-count" class="hint" aria-live="polite">0/1000</p>
    <p id="message-error" class="error" aria-live="polite"></p>
  </div>

  <button type="submit">Send Message</button>
</form>
```

### 3. Constraint Validation API

```javascript
const form = document.getElementById('contact-form');
const inputs = form.querySelectorAll('input, textarea, select');

// Disable browser default validation UI
form.setAttribute('novalidate', '');

// Validate on submit
form.addEventListener('submit', (e) => {
  if (!validateForm()) {
    e.preventDefault();
    showErrorSummary();
    focusFirstError();
  }
});

// Validate on blur for immediate feedback
inputs.forEach(input => {
  input.addEventListener('blur', () => validateField(input));
  input.addEventListener('input', () => {
    if (input.classList.contains('invalid')) {
      validateField(input);
    }
  });
});

function validateForm() {
  let isValid = true;
  inputs.forEach(input => {
    if (!validateField(input)) {
      isValid = false;
    }
  });
  return isValid;
}

function validateField(input) {
  const errorEl = document.getElementById(`${input.id}-error`);

  // Check validity using Constraint Validation API
  if (!input.checkValidity()) {
    const message = getErrorMessage(input);
    showError(input, errorEl, message);
    return false;
  }

  clearError(input, errorEl);
  return true;
}

function getErrorMessage(input) {
  const validity = input.validity;

  if (validity.valueMissing) {
    return `${input.labels[0].textContent} is required`;
  }
  if (validity.typeMismatch) {
    return `Please enter a valid ${input.type}`;
  }
  if (validity.patternMismatch) {
    return input.dataset.patternError || 'Please match the requested format';
  }
  if (validity.tooShort) {
    return `Must be at least ${input.minLength} characters`;
  }
  if (validity.tooLong) {
    return `Must be no more than ${input.maxLength} characters`;
  }
  if (validity.rangeUnderflow) {
    return `Must be at least ${input.min}`;
  }
  if (validity.rangeOverflow) {
    return `Must be no more than ${input.max}`;
  }

  return input.validationMessage;
}

function showError(input, errorEl, message) {
  input.classList.add('invalid');
  input.setAttribute('aria-invalid', 'true');
  input.setAttribute('aria-errormessage', errorEl.id);
  errorEl.textContent = message;
  errorEl.hidden = false;
}

function clearError(input, errorEl) {
  input.classList.remove('invalid');
  input.removeAttribute('aria-invalid');
  input.removeAttribute('aria-errormessage');
  errorEl.textContent = '';
  errorEl.hidden = true;
}

function focusFirstError() {
  const firstError = form.querySelector('.invalid');
  if (firstError) {
    firstError.focus();
  }
}
```

---

## ⚠️ Error Handling

### Error Codes

| Code | Description | Recovery |
|------|-------------|----------|
| `FORM001` | Missing form label | Add aria-labelledby or aria-label |
| `FORM002` | Input without label | Add `<label>` element |
| `FORM003` | Invalid pattern regex | Fix regex syntax |
| `FORM004` | Missing required indicator | Add visual + aria indicator |
| `FORM005` | No error message element | Add aria-live region |
| `FORM006` | Autocomplete missing | Add autocomplete attribute |
| `FORM007` | Submit without action | Add form action |
| `FORM008` | Fieldset without legend | Add legend element |

### ValidityState Properties

| Property | True When |
|----------|-----------|
| `valid` | All constraints satisfied |
| `valueMissing` | Required field is empty |
| `typeMismatch` | Value doesn't match type (email, url) |
| `patternMismatch` | Value doesn't match pattern |
| `tooLong` | Value exceeds maxlength |
| `tooShort` | Value below minlength |
| `rangeUnderflow` | Value below min |
| `rangeOverflow` | Value above max |
| `stepMismatch` | Value doesn't match step |
| `badInput` | Browser can't convert input |
| `customError` | setCustomValidity() called |

---

## 🔍 Troubleshooting

### Problem: Form not validating

```
Debug Checklist:
□ novalidate attribute set?
□ JavaScript calling checkValidity()?
□ Required attribute on mandatory fields?
□ Pattern regex valid?
□ Type attribute correct?
□ Min/max values valid?
```

### Problem: Errors not announced

```
Debug Checklist:
□ Error container has role="alert"?
□ aria-live="polite" or "assertive" set?
□ Error linked via aria-errormessage?
□ aria-invalid="true" on field?
□ Error content actually changing?
```

### Problem: Autocomplete not working

```
Debug Checklist:
□ autocomplete attribute present?
□ Correct autocomplete value?
□ Input has name attribute?
□ Form has action?
□ Browser autocomplete enabled?
```

### Autocomplete Values

| Value | Purpose |
|-------|---------|
| `name` | Full name |
| `given-name` | First name |
| `family-name` | Last name |
| `email` | Email address |
| `tel` | Phone number |
| `street-address` | Street address |
| `postal-code` | ZIP/Postal code |
| `country` | Country |
| `cc-number` | Credit card number |
| `cc-exp` | Card expiration |
| `cc-csc` | Security code |
| `username` | Username |
| `current-password` | Current password |
| `new-password` | New password |

---

## 📊 Form Types

### Login Form

```html
<form action="/login" method="POST" aria-labelledby="login-title">
  <h2 id="login-title">Sign In</h2>

  <div class="field">
    <label for="username">Email or Username</label>
    <input type="text"
           id="username"
           name="username"
           required
           autocomplete="username"
           autofocus>
  </div>

  <div class="field">
    <label for="password">Password</label>
    <input type="password"
           id="password"
           name="password"
           required
           autocomplete="current-password"
           minlength="8">
    <a href="/forgot-password">Forgot password?</a>
  </div>

  <label class="checkbox">
    <input type="checkbox" name="remember" value="1">
    Remember me
  </label>

  <button type="submit">Sign In</button>

  <p>Don't have an account? <a href="/register">Sign up</a></p>
</form>
```

### Search Form

```html
<form role="search"
      action="/search"
      method="GET"
      aria-label="Site search">
  <label for="search-input" class="visually-hidden">
    Search
  </label>
  <input type="search"
         id="search-input"
         name="q"
         placeholder="Search..."
         autocomplete="off"
         aria-describedby="search-hint">
  <button type="submit" aria-label="Submit search">
    <svg aria-hidden="true">...</svg>
  </button>
  <p id="search-hint" class="visually-hidden">
    Enter keywords to search
  </p>
</form>
```

### Multi-Step Form

```html
<form id="wizard" aria-labelledby="wizard-title">
  <h2 id="wizard-title">Registration</h2>

  <!-- Progress indicator -->
  <nav aria-label="Registration progress">
    <ol>
      <li aria-current="step">
        <span class="step-number">1</span>
        <span class="step-label">Account</span>
      </li>
      <li>
        <span class="step-number">2</span>
        <span class="step-label">Profile</span>
      </li>
      <li>
        <span class="step-number">3</span>
        <span class="step-label">Confirm</span>
      </li>
    </ol>
  </nav>

  <!-- Step 1: Account -->
  <fieldset id="step-1" class="step active">
    <legend>Account Information</legend>
    <div class="field">
      <label for="email">Email</label>
      <input type="email" id="email" name="email" required>
    </div>
    <div class="field">
      <label for="password">Password</label>
      <input type="password"
             id="password"
             name="password"
             required
             minlength="8"
             autocomplete="new-password">
    </div>
    <button type="button" onclick="nextStep(1)">Next</button>
  </fieldset>

  <!-- Step 2: Profile (hidden initially) -->
  <fieldset id="step-2" class="step" hidden>
    <legend>Profile Information</legend>
    <!-- fields -->
    <button type="button" onclick="prevStep(2)">Back</button>
    <button type="button" onclick="nextStep(2)">Next</button>
  </fieldset>

  <!-- Step 3: Confirm (hidden initially) -->
  <fieldset id="step-3" class="step" hidden>
    <legend>Confirm Details</legend>
    <!-- summary -->
    <button type="button" onclick="prevStep(3)">Back</button>
    <button type="submit">Create Account</button>
  </fieldset>
</form>
```

---

## 📋 Usage Examples

```yaml
# Create contact form
skill: forms
operation: create
form_type: contact
options:
  validation_mode: hybrid
  accessibility_level: "AA"
  autocomplete: true

# Validate form markup
skill: forms
operation: validate
markup: "<form>...</form>"

# Get login form pattern
skill: forms
operation: pattern
form_type: login
```

---

## 🔗 References

- [MDN Form Validation](https://developer.mozilla.org/en-US/docs/Learn/Forms/Form_validation)
- [Constraint Validation API](https://developer.mozilla.org/en-US/docs/Web/HTML/Constraint_validation)
- [HTML Autocomplete](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete)
- [WCAG Forms](https://www.w3.org/WAI/tutorials/forms/)
