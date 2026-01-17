# 📊 Diagram Generator Skill

---
name: diagram-generator
description: Generate visual diagrams from code, text descriptions, or data structures using Mermaid
---

## 🎯 Purpose

สร้าง diagrams จาก code, text descriptions, หรือ data structures โดยใช้ Mermaid syntax

## 📋 When to Use

- Document architecture
- Explain flows
- Visualize relationships
- Create documentation
- Present to stakeholders

## 🔧 Diagram Types

### 1. Flowchart
```mermaid
flowchart TD
    A[Start] --> B{Condition?}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
```

### 2. Sequence Diagram
```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant A as API
    participant D as Database
    
    U->>F: Click Login
    F->>A: POST /auth/login
    A->>D: Query User
    D-->>A: User Data
    A-->>F: JWT Token
    F-->>U: Redirect to Dashboard
```

### 3. Class Diagram
```mermaid
classDiagram
    class User {
        +String id
        +String name
        +String email
        +login()
        +logout()
    }
    
    class Order {
        +String id
        +User user
        +Item[] items
        +calculate()
    }
    
    User "1" --> "*" Order
```

### 4. Entity Relationship
```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ITEM : contains
    USER {
        int id PK
        string name
        string email
    }
    ORDER {
        int id PK
        int user_id FK
        date created_at
    }
```

### 5. State Diagram
```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Pending: Submit
    Pending --> Approved: Approve
    Pending --> Rejected: Reject
    Rejected --> Draft: Edit
    Approved --> [*]
```

### 6. Pie Chart
```mermaid
pie title Distribution
    "Category A" : 40
    "Category B" : 30
    "Category C" : 20
    "Category D" : 10
```

## 📝 Generation From Code

### From Function Flow
```javascript
// Input: Code
async function processOrder(order) {
  validate(order);
  const payment = await processPayment(order);
  if (payment.success) {
    await fulfillOrder(order);
    sendConfirmation(order);
  } else {
    handleFailure(order);
  }
}
```

```mermaid
flowchart TD
    A[processOrder] --> B[validate]
    B --> C[processPayment]
    C --> D{payment.success?}
    D -->|Yes| E[fulfillOrder]
    E --> F[sendConfirmation]
    D -->|No| G[handleFailure]
```

### From Component Tree
```jsx
// Input: React Components
<App>
  <Header />
  <Main>
    <Sidebar />
    <Content>
      <ArticleList />
    </Content>
  </Main>
  <Footer />
</App>
```

```mermaid
graph TD
    App --> Header
    App --> Main
    App --> Footer
    Main --> Sidebar
    Main --> Content
    Content --> ArticleList
```

## 🎨 Styling

```mermaid
flowchart TD
    A[Start]:::green --> B{Check}
    B -->|Pass| C[Success]:::green
    B -->|Fail| D[Error]:::red
    
    classDef green fill:#10b981,color:white
    classDef red fill:#ef4444,color:white
```

## ✅ Best Practices

- [ ] Keep diagrams simple
- [ ] Use meaningful labels
- [ ] Group related items
- [ ] Choose right diagram type
- [ ] Add colors for clarity
- [ ] Include legend if needed

## 🔗 Related Skills

- `documentation` - Create docs
- `codebase-understanding` - Understand structure
- `code-explanation` - Explain with visuals
