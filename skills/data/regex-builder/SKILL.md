# 🔤 Regex Builder Skill

---
name: regex-builder
description: Build and explain regular expressions from natural language descriptions
---

## 🎯 Purpose

สร้าง Regular Expressions จาก natural language และอธิบาย regex ที่ซับซ้อนให้เข้าใจง่าย

## 📋 When to Use

- ต้องการสร้าง regex ใหม่
- ต้องการเข้าใจ regex ที่มีอยู่
- Validate input patterns
- Extract data จาก text
- Search and replace patterns

## 🔧 Common Patterns

### Email Validation
```regex
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```
**Explanation:**
- `^` - เริ่มต้น string
- `[a-zA-Z0-9._%+-]+` - username (ตัวอักษร, ตัวเลข, ., _, %, +, -)
- `@` - ต้องมี @
- `[a-zA-Z0-9.-]+` - domain name
- `\.` - ต้องมี .
- `[a-zA-Z]{2,}$` - TLD อย่างน้อย 2 ตัวอักษร

### Phone Number (Thai)
```regex
^(0[689]\d{8}|0[2-9]\d{7,8})$
```
**Explanation:**
- `0[689]\d{8}` - มือถือ (06, 08, 09 + 8 หลัก)
- `0[2-9]\d{7,8}` - บ้าน (02-09 + 7-8 หลัก)

### URL
```regex
^https?:\/\/[^\s]+$
```

### Date (YYYY-MM-DD)
```regex
^\d{4}-\d{2}-\d{2}$
```

### Password (Strong)
```regex
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
```
**Explanation:**
- `(?=.*[a-z])` - ต้องมี lowercase
- `(?=.*[A-Z])` - ต้องมี uppercase
- `(?=.*\d)` - ต้องมีตัวเลข
- `(?=.*[@$!%*?&])` - ต้องมี special char
- `{8,}` - อย่างน้อย 8 ตัว

## 📊 Regex Cheat Sheet

### Character Classes
| Pattern | Meaning |
|---------|---------|
| `.` | Any character (except newline) |
| `\d` | Digit (0-9) |
| `\D` | Non-digit |
| `\w` | Word character (a-z, A-Z, 0-9, _) |
| `\W` | Non-word character |
| `\s` | Whitespace |
| `\S` | Non-whitespace |

### Quantifiers
| Pattern | Meaning |
|---------|---------|
| `*` | 0 or more |
| `+` | 1 or more |
| `?` | 0 or 1 |
| `{n}` | Exactly n |
| `{n,}` | n or more |
| `{n,m}` | Between n and m |

### Anchors
| Pattern | Meaning |
|---------|---------|
| `^` | Start of string |
| `$` | End of string |
| `\b` | Word boundary |

### Groups
| Pattern | Meaning |
|---------|---------|
| `(...)` | Capture group |
| `(?:...)` | Non-capture group |
| `(?=...)` | Positive lookahead |
| `(?!...)` | Negative lookahead |

## 📝 Natural Language → Regex

| Natural Language | Regex |
|-----------------|-------|
| "starts with A" | `^A` |
| "ends with .com" | `\.com$` |
| "contains numbers" | `\d+` |
| "exactly 5 digits" | `^\d{5}$` |
| "optional dashes" | `-?` |
| "one or more words" | `\w+` |
| "either cat or dog" | `(cat\|dog)` |

## 🔧 JavaScript Usage

```javascript
// Test pattern
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
emailRegex.test('user@example.com'); // true

// Extract matches
const text = 'Call 081-234-5678 or 089-876-5432';
const phones = text.match(/0[689]\d-?\d{3}-?\d{4}/g);
// ['081-234-5678', '089-876-5432']

// Replace
const cleaned = text.replace(/[^\d]/g, '');
// '08123456780898765432'

// Named groups
const dateRegex = /(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})/;
const match = '2024-01-15'.match(dateRegex);
console.log(match.groups.year); // '2024'
```

## 🔍 Regex Debugging

### Test Online
- [regex101.com](https://regex101.com) - With explanation
- [regexr.com](https://regexr.com) - Visual

### Common Mistakes
| Mistake | Fix |
|---------|-----|
| Forgot to escape `.` | Use `\.` |
| Greedy matching | Use `*?` or `+?` |
| Missing anchors | Add `^` and `$` |
| Global flag missing | Add `g` flag |

## ✅ Regex Checklist

- [ ] Handles edge cases
- [ ] Not too greedy
- [ ] Anchored properly
- [ ] Tested with valid inputs
- [ ] Tested with invalid inputs
- [ ] Performance acceptable

## 🔗 Related Skills

- `code-search` - Search patterns in code
- `data-analysis` - Extract data from text
- `testing` - Test regex patterns
