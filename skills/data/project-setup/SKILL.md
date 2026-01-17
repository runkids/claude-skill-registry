---
name: project-setup
description: Set up new projects with proper structure, configuration, and best practices. Use this skill when creating new projects or initializing new codebases.
---

# 🚀 Project Setup Skill

## Web Project Structure

```
📁 project-name/
   📁 src/
      📁 components/    ← UI Components
      📁 pages/         ← Page Components
      📁 hooks/         ← Custom Hooks
      📁 utils/         ← Utility Functions
      📁 types/         ← TypeScript Types
      📁 services/      ← API Services
      📁 stores/        ← State Management
      📁 assets/        ← Images, Fonts
   📁 public/           ← Static files
   📁 tests/            ← Test files
   📄 .gitignore
   📄 .env.example
   📄 package.json
   📄 README.md
   📄 tsconfig.json
```

## Essential Files

### .gitignore
```
node_modules/
dist/
.env
*.log
.DS_Store
```

### .env.example
```
# Server
PORT=3000

# Database
DATABASE_URL=

# API Keys (replace with your own)
API_KEY=
```

### package.json scripts
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "vitest",
    "lint": "eslint src/",
    "format": "prettier --write src/"
  }
}
```

## Setup Checklist

### 1. Initialize
```powershell
# Create project
npx -y create-vite@latest ./ --template react-ts

# Install dependencies
npm install
```

### 2. Configure Linting
```powershell
# ESLint + Prettier
npm install -D eslint prettier eslint-config-prettier
```

### 3. Git Setup
```powershell
git init
git add .
git commit -m "Initial commit"
```

### 4. Environment
```powershell
# Copy example env
Copy-Item .env.example .env
```

## Framework-Specific Setup

### React + Vite
```powershell
npx -y create-vite@latest ./ --template react-ts
```

### Next.js
```powershell
npx -y create-next-app@latest ./ --typescript --tailwind --eslint
```

### Chrome Extension
```
📁 extension/
   📄 manifest.json   ← V3 manifest
   📁 src/
      📄 background.js
      📄 content.js
      📄 popup.html
```

## Post-Setup Verification

- [ ] `npm run dev` works
- [ ] `npm run build` succeeds
- [ ] `npm run test` passed
- [ ] `.env` is in `.gitignore`
- [ ] README has setup instructions
