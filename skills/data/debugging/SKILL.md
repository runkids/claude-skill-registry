---
name: Debugging
description: วิเคราะห์และแก้ไขบั๊กอย่างเป็นระบบ
---

# Debugging Skill

## Overview

Skill สำหรับวิเคราะห์ปัญหา หาสาเหตุ และแก้ไขบั๊กอย่างมีประสิทธิภาพ

## Debugging Process

### Step 1: รวบรวมข้อมูล

1. **อ่าน Error Message** - เข้าใจ error ที่เกิดขึ้น
2. **ดู Stack Trace** - หา line และ file ที่เกิดปัญหา
3. **ตรวจสอบ Logs** - หา pattern หรือ context เพิ่มเติม
4. **ถาม Context** - สอบถามผู้ใช้ว่าเกิดอะไรขึ้นก่อนหน้า

### Step 2: วิเคราะห์ปัญหา

1. **Reproduce** - พยายามทำซ้ำปัญหา
2. **Isolate** - แยกส่วนที่มีปัญหาออกมา
3. **Hypothesis** - ตั้งสมมติฐานสาเหตุ
4. **Verify** - ทดสอบสมมติฐาน

### Step 3: แก้ไข

1. **Fix** - แก้ไขปัญหา
2. **Test** - ทดสอบว่าแก้ได้จริง
3. **Verify Side Effects** - ตรวจสอบผลกระทบอื่นๆ
4. **Document** - บันทึกสิ่งที่แก้ไข

---

## Common Error Patterns

### Frontend Errors

#### React

| Error                               | สาเหตุที่พบบ่อย                          |
| ----------------------------------- | ---------------------------------------- |
| "Cannot read property of undefined" | ไม่ได้เช็ค null/undefined ก่อนใช้        |
| "Too many re-renders"               | State update ใน render loop              |
| "Invalid hook call"                 | Hook เรียกนอก component หรือ conditional |
| "Key prop missing"                  | ไม่ใส่ key ใน list items                 |

#### Angular

| Error                                    | สาเหตุที่พบบ่อย                |
| ---------------------------------------- | ------------------------------ |
| "ExpressionChangedAfterItHasBeenChecked" | State change ใน lifecycle hook |
| "NullInjectorError"                      | ไม่ได้ provide service         |
| "Template parse errors"                  | Syntax ผิดใน template          |

#### Vue

| Error                                   | สาเหตุที่พบบ่อย                 |
| --------------------------------------- | ------------------------------- |
| "Property X was accessed during render" | Reactive property ไม่ถูก define |
| "Maximum recursive updates exceeded"    | Watcher loop                    |

---

### Backend Errors

#### Spring Boot

| Error                             | สาเหตุที่พบบ่อย               |
| --------------------------------- | ----------------------------- |
| "No qualifying bean"              | Bean ไม่ถูก inject            |
| "LazyInitializationException"     | Entity access นอก transaction |
| "ConstraintViolationException"    | Database constraint violation |
| "HttpMessageNotReadableException" | JSON parse error              |

#### Node.js

| Error           | สาเหตุที่พบบ่อย           |
| --------------- | ------------------------- |
| "ECONNREFUSED"  | Service/Database ไม่พร้อม |
| "CORS error"    | CORS ไม่ถูกตั้งค่า        |
| "JWT malformed" | Token format ผิด          |

#### Python

| Error             | สาเหตุที่พบบ่อย                 |
| ----------------- | ------------------------------- |
| "IntegrityError"  | Duplicate key หรือ FK violation |
| "ValidationError" | Pydantic validation fail        |
| "ImportError"     | Module ไม่ถูก install           |

---

### Database Errors

| Error                   | สาเหตุที่พบบ่อย                      |
| ----------------------- | ------------------------------------ |
| "Connection refused"    | Database ไม่ running หรือ config ผิด |
| "Duplicate key"         | Primary key หรือ unique constraint   |
| "Foreign key violation" | Reference ไปยัง row ที่ไม่มี         |
| "Deadlock"              | Transaction conflict                 |

---

## Debugging Tools

### Browser DevTools

- **Console** - ดู errors และ logs
- **Network** - ตรวจสอบ API calls
- **Sources** - Breakpoints และ step through
- **React/Vue/Angular DevTools** - Component inspection

### Backend Debugging

- **Logging** - เพิ่ม log statements
- **Debugger** - Attach debugger (VSCode, IntelliJ)
- **Postman/Insomnia** - Test API endpoints
- **Database clients** - ตรวจสอบ data

### Performance Debugging

- **Lighthouse** - Web performance
- **Chrome Performance tab** - Runtime performance
- **Memory profiler** - Memory leaks
- **SQL EXPLAIN** - Query optimization

---

## Debugging Checklist

- [ ] อ่าน error message ให้ละเอียด
- [ ] ดู full stack trace
- [ ] ตรวจสอบ recent changes
- [ ] ลอง reproduce ปัญหา
- [ ] เพิ่ม logging ถ้าจำเป็น
- [ ] ตรวจสอบ dependencies/versions
- [ ] ค้นหา similar issues
- [ ] ทดสอบ fix อย่างละเอียด
