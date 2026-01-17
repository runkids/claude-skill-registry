# 📖 Code Explanation Skill

---
name: code-explanation
description: Explain complex code in simple terms, document logic, and help developers understand unfamiliar codebases
---

## 🎯 Purpose

อธิบาย code ที่ซับซ้อนให้เข้าใจง่าย ช่วยให้ developers เรียนรู้และเข้าใจ codebases ที่ไม่คุ้นเคย

## 📋 When to Use

- เจอ code ที่ซับซ้อนเข้าใจยาก
- ต้องการเรียนรู้จาก codebase
- Review code ที่คนอื่นเขียน
- Document legacy code
- Onboard team members ใหม่

## 🔧 Explanation Levels

### Level 1: High-Level Overview
```
"ฟังก์ชันนี้ทำหน้าที่ดึงข้อมูลผู้ใช้จาก API 
แล้ว cache ไว้เพื่อใช้ครั้งต่อไปโดยไม่ต้อง fetch ใหม่"
```

### Level 2: Step-by-Step
```
1. รับ userId เป็น parameter
2. เช็คว่ามี cached data หรือยัง
3. ถ้ามี → return cached data
4. ถ้าไม่มี → fetch จาก API
5. เก็บผลลัพธ์ใน cache
6. return data
```

### Level 3: Line-by-Line
```javascript
// ฟังก์ชัน async สำหรับดึงข้อมูล user
async function getUser(userId: string) {
  // ลองหาใน cache ก่อน
  const cached = cache.get(userId);
  
  // ถ้าเจอใน cache ก็ return เลย (เร็วกว่า)
  if (cached) return cached;
  
  // ถ้าไม่เจอต้อง fetch จาก API
  const user = await api.fetchUser(userId);
  
  // เก็บลง cache เพื่อใช้ครั้งหน้า
  cache.set(userId, user);
  
  return user;
}
```

## 📝 Explanation Template

```markdown
## 📖 Code Explanation

### Summary
{what the code does in 1-2 sentences}

### Purpose
{why this code exists, what problem it solves}

### How It Works
1. {step 1}
2. {step 2}
3. {step 3}

### Key Concepts
- **{concept 1}**: {explanation}
- **{concept 2}**: {explanation}

### Input/Output
- **Input**: {what it receives}
- **Output**: {what it returns}

### Side Effects
- {any side effects like API calls, state changes}

### Related Code
- {links to related files/functions}
```

## 🔍 Explanation Patterns

### Algorithm Explanation
```markdown
## Bubble Sort Algorithm

**What it does**: เรียงลำดับ array จากน้อยไปมาก

**How it works**:
1. เริ่มจากตัวแรกของ array
2. เปรียบเทียบกับตัวถัดไป
3. ถ้าตัวแรกมากกว่า → สลับที่
4. ทำซ้ำจนถึงตัวสุดท้าย (1 รอบ)
5. ทำซ้ำทั้งหมด n รอบ

**Time Complexity**: O(n²)
**Space Complexity**: O(1)

**Visual**:
[5, 3, 8, 1] → [3, 5, 1, 8] → [3, 1, 5, 8] → [1, 3, 5, 8]
```

### Design Pattern Explanation
```markdown
## Observer Pattern

**What it does**: ให้ objects หลายตัว "subscribe" เพื่อรับ notification 
เมื่อมีการเปลี่ยนแปลง

**Real-world analogy**: เหมือน YouTube subscription
- Channel = Subject
- Subscribers = Observers
- เมื่อมีวิดีโอใหม่ → แจ้ง subscribers ทุกคน

**Components**:
- Subject: เก็บ list ของ observers, notify ทุกครั้งที่มีการเปลี่ยนแปลง
- Observer: รอรับ notification และทำงานตาม

**Use cases**: Event systems, State management, Real-time updates
```

### API Endpoint Explanation
```markdown
## POST /api/users

**Purpose**: สร้าง user ใหม่ในระบบ

**Request**:
- Method: POST
- Headers: `Content-Type: application/json`
- Body: `{ name: string, email: string, password: string }`

**Response**:
- 201: User created successfully
- 400: Validation error
- 409: Email already exists

**Flow**:
1. Validate input
2. Hash password
3. Save to database
4. Return user (without password)
```

## 📊 Visual Aids

### Flowchart
```
┌─────────┐
│  Start  │
└────┬────┘
     │
     ▼
┌─────────┐    Yes   ┌─────────┐
│ Cached? │─────────▶│ Return  │
└────┬────┘          │ Cache   │
     │ No            └─────────┘
     ▼
┌─────────┐
│  Fetch  │
│  API    │
└────┬────┘
     │
     ▼
┌─────────┐
│  Cache  │
│  Store  │
└────┬────┘
     │
     ▼
┌─────────┐
│ Return  │
└─────────┘
```

### Data Flow
```
User Input
    │
    ▼
┌───────────┐     ┌──────────┐     ┌─────────┐
│ Component │────▶│  Store   │────▶│   API   │
└───────────┘     └──────────┘     └─────────┘
    ▲                   │
    │                   │
    └───────────────────┘
         (state update)
```

## ✅ Good Explanation Checklist

- [ ] ใช้ภาษาง่ายๆ ไม่ซับซ้อน
- [ ] มี analogy/ตัวอย่างในชีวิตจริง
- [ ] มี visual aids (diagrams, flowcharts)
- [ ] อธิบาย WHY ไม่ใช่แค่ WHAT
- [ ] เหมาะกับ level ของคนอ่าน
- [ ] มีตัวอย่าง input/output

## 🔗 Related Skills

- `documentation` - Write full docs
- `codebase-understanding` - Understand projects
- `code-review` - Review and explain changes
