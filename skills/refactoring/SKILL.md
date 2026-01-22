---
name: Refactoring
description: ปรับปรุงโค้ดให้ดีขึ้นโดยไม่เปลี่ยน behavior
---

# Refactoring Skill

## Overview

Skill สำหรับปรับปรุงคุณภาพโค้ด ทำให้อ่านง่าย maintain ง่าย และมีประสิทธิภาพมากขึ้น

## Refactoring Principles

### SOLID Principles

1. **Single Responsibility** - แต่ละ class/function ทำหน้าที่เดียว
2. **Open/Closed** - เปิดสำหรับ extension, ปิดสำหรับ modification
3. **Liskov Substitution** - Subclass ใช้แทน parent ได้
4. **Interface Segregation** - Interface เล็กๆ เฉพาะทาง
5. **Dependency Inversion** - Depend on abstractions, not concretions

### Other Principles

- **DRY** - Don't Repeat Yourself
- **KISS** - Keep It Simple, Stupid
- **YAGNI** - You Aren't Gonna Need It

---

## Code Smells & Solutions

### Bloaters

| Smell                   | Solution                                           |
| ----------------------- | -------------------------------------------------- |
| **Long Method**         | Extract Method - แยกเป็น functions เล็กๆ           |
| **Large Class**         | Extract Class - แยกเป็น classes                    |
| **Long Parameter List** | Parameter Object - รวมเป็น object                  |
| **Data Clumps**         | Extract Class - สร้าง class รวม data ที่ใช้ด้วยกัน |

### Object-Orientation Abusers

| Smell                    | Solution                            |
| ------------------------ | ----------------------------------- |
| **Switch Statements**    | Replace with Polymorphism           |
| **Parallel Inheritance** | Merge hierarchies                   |
| **Refused Bequest**      | Replace Inheritance with Delegation |

### Change Preventers

| Smell                | Solution                             |
| -------------------- | ------------------------------------ |
| **Divergent Change** | Extract Class - แยก concerns         |
| **Shotgun Surgery**  | Move Method/Field - รวม related code |

### Dispensables

| Smell                    | Solution                                   |
| ------------------------ | ------------------------------------------ |
| **Dead Code**            | ลบทิ้ง                                     |
| **Duplicate Code**       | Extract Method/Class                       |
| **Lazy Class**           | Inline Class - รวมกับ class อื่น           |
| **Comments (excessive)** | Rename/Extract - ให้ code self-documenting |

### Couplers

| Smell              | Solution                                  |
| ------------------ | ----------------------------------------- |
| **Feature Envy**   | Move Method - ย้ายไปที่ class ที่ใช้ data |
| **Message Chains** | Hide Delegate - สร้าง wrapper method      |
| **Middle Man**     | Remove Middle Man - เรียกตรง              |

---

## Common Refactoring Techniques

### Extract Method

```javascript
// Before
function printUserInfo(user) {
  console.log("---USER INFO---");
  console.log(`Name: ${user.name}`);
  console.log(`Email: ${user.email}`);
  console.log(`Age: ${user.age}`);
  console.log("---------------");
}

// After
function printUserInfo(user) {
  printHeader();
  printDetails(user);
  printFooter();
}

function printHeader() {
  console.log("---USER INFO---");
}

function printDetails(user) {
  console.log(`Name: ${user.name}`);
  console.log(`Email: ${user.email}`);
  console.log(`Age: ${user.age}`);
}

function printFooter() {
  console.log("---------------");
}
```

### Replace Conditional with Polymorphism

```typescript
// Before
function calculateArea(shape: Shape): number {
  switch (shape.type) {
    case "circle":
      return Math.PI * shape.radius ** 2;
    case "rectangle":
      return shape.width * shape.height;
    case "triangle":
      return (shape.base * shape.height) / 2;
  }
}

// After
interface Shape {
  calculateArea(): number;
}

class Circle implements Shape {
  constructor(private radius: number) {}
  calculateArea(): number {
    return Math.PI * this.radius ** 2;
  }
}

class Rectangle implements Shape {
  constructor(
    private width: number,
    private height: number,
  ) {}
  calculateArea(): number {
    return this.width * this.height;
  }
}
```

### Introduce Parameter Object

```typescript
// Before
function createUser(name: string, email: string, age: number,
                    address: string, phone: string) { ... }

// After
interface UserData {
  name: string;
  email: string;
  age: number;
  address: string;
  phone: string;
}

function createUser(data: UserData) { ... }
```

---

## Refactoring Process

1. **Ensure Tests Exist** - มี tests ก่อน refactor
2. **Make Small Changes** - เปลี่ยนทีละน้อย
3. **Run Tests Often** - ทดสอบหลังทุกการเปลี่ยน
4. **Commit Frequently** - commit ทีละ refactoring
5. **Review** - ตรวจสอบผลลัพธ์

---

## Refactoring Checklist

- [ ] มี tests ครอบคลุมก่อน refactor
- [ ] ระบุ code smells ที่ต้องการแก้
- [ ] วางแผนการ refactor
- [ ] ทำทีละ step เล็กๆ
- [ ] Run tests หลังทุก step
- [ ] Review ว่า code ดีขึ้นจริง
- [ ] Update documentation ถ้าจำเป็น
