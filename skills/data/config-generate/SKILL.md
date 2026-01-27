---
name: config-generate
description: Generate configuration files for development tools
disable-model-invocation: true
---

# Configuration File Generator

I'll generate configuration files for common development tools: TypeScript, ESLint, Prettier, Jest, Vitest, and more.

Arguments: `$ARGUMENTS` - config type (tsconfig, eslint, prettier, jest, etc.)

**Supported Configs:**
- TypeScript: tsconfig.json
- Linting: .eslintrc.js, .eslintignore
- Formatting: .prettierrc, .prettierignore
- Testing: jest.config.js, vitest.config.ts
- Bundling: vite.config.ts, webpack.config.js
- Git: .gitignore, .gitattributes

**Token Optimization:**
- Framework detection (100 tokens)
- Template selection (200 tokens)
- Config generation (800-1,200 tokens)
- Expected: 1,500-2,500 tokens total

## Phase 1: Detect Project Requirements

```bash
#!/bin/bash
# Detect project type and requirements

echo "=== Analyzing Project ==="
echo ""

# Detect package manager
detect_package_manager() {
    if [ -f "pnpm-lock.yaml" ]; then
        echo "pnpm"
    elif [ -f "yarn.lock" ]; then
        echo "yarn"
    elif [ -f "package-lock.json" ]; then
        echo "npm"
    elif [ -f "bun.lockb" ]; then
        echo "bun"
    else
        echo "npm"
    fi
}

PKG_MANAGER=$(detect_package_manager)
echo "✓ Package manager: $PKG_MANAGER"

# Detect TypeScript
if [ -f "package.json" ]; then
    if grep -q "\"typescript\"" package.json; then
        HAS_TYPESCRIPT=true
        echo "✓ TypeScript detected"
    else
        HAS_TYPESCRIPT=false
    fi

    # Detect frameworks
    if grep -q "\"react\"" package.json; then
        FRAMEWORK="react"
        echo "✓ Framework: React"
    elif grep -q "\"vue\"" package.json; then
        FRAMEWORK="vue"
        echo "✓ Framework: Vue"
    elif grep -q "\"next\"" package.json; then
        FRAMEWORK="nextjs"
        echo "✓ Framework: Next.js"
    fi

    # Detect test framework
    if grep -q "\"jest\"" package.json; then
        TEST_FRAMEWORK="jest"
        echo "✓ Test framework: Jest"
    elif grep -q "\"vitest\"" package.json; then
        TEST_FRAMEWORK="vitest"
        echo "✓ Test framework: Vitest"
    fi
fi

echo ""
```

## Phase 2: Generate tsconfig.json

```json
{
  "compilerOptions": {
    /* Language and Environment */
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "jsx": "react-jsx",
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,

    /* Modules */
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@components/*": ["./src/components/*"],
      "@utils/*": ["./src/utils/*"],
      "@types/*": ["./src/types/*"]
    },

    /* Emit */
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "outDir": "./dist",
    "removeComments": true,
    "noEmit": true,

    /* Interop Constraints */
    "isolatedModules": true,
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,

    /* Type Checking */
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "noImplicitReturns": true,
    "noUncheckedIndexedAccess": true,

    /* Completeness */
    "skipLibCheck": true
  },
  "include": [
    "src/**/*",
    "tests/**/*",
    "*.ts",
    "*.tsx"
  ],
  "exclude": [
    "node_modules",
    "dist",
    "build",
    "coverage"
  ]
}
```

**Framework-specific variations:**

```json
// Next.js tsconfig.json
{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

## Phase 3: Generate ESLint Configuration

```javascript
// .eslintrc.js - Comprehensive ESLint config
module.exports = {
  root: true,
  env: {
    browser: true,
    es2022: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:jsx-a11y/recommended',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'prettier', // Must be last
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
    project: './tsconfig.json',
  },
  plugins: [
    '@typescript-eslint',
    'react',
    'react-hooks',
    'jsx-a11y',
    'import',
  ],
  settings: {
    react: {
      version: 'detect',
    },
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
        project: './tsconfig.json',
      },
    },
  },
  rules: {
    // TypeScript specific rules
    '@typescript-eslint/no-unused-vars': [
      'error',
      { argsIgnorePattern: '^_', varsIgnorePattern: '^_' },
    ],
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/explicit-function-return-type': 'off',
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-non-null-assertion': 'warn',
    '@typescript-eslint/consistent-type-imports': [
      'error',
      { prefer: 'type-imports' },
    ],

    // React specific rules
    'react/react-in-jsx-scope': 'off', // Not needed in React 17+
    'react/prop-types': 'off', // TypeScript handles this
    'react/jsx-uses-react': 'off',
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',

    // Import rules
    'import/order': [
      'error',
      {
        groups: [
          'builtin',
          'external',
          'internal',
          'parent',
          'sibling',
          'index',
        ],
        'newlines-between': 'always',
        alphabetize: { order: 'asc', caseInsensitive: true },
      },
    ],
    'import/no-unresolved': 'error',
    'import/no-cycle': 'error',

    // General rules
    'no-console': ['warn', { allow: ['warn', 'error'] }],
    'no-debugger': 'warn',
    'prefer-const': 'error',
    'no-var': 'error',
  },
  overrides: [
    {
      // Test files
      files: ['**/*.test.ts', '**/*.test.tsx', '**/*.spec.ts'],
      env: {
        jest: true,
      },
      rules: {
        '@typescript-eslint/no-explicit-any': 'off',
      },
    },
  ],
};
```

```
# .eslintignore
node_modules/
dist/
build/
coverage/
.next/
out/
*.min.js
*.config.js
public/
```

## Phase 4: Generate Prettier Configuration

```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false,
  "arrowParens": "always",
  "endOfLine": "lf",
  "bracketSpacing": true,
  "jsxSingleQuote": false,
  "jsxBracketSameLine": false,
  "proseWrap": "preserve",
  "quoteProps": "as-needed",
  "overrides": [
    {
      "files": "*.json",
      "options": {
        "printWidth": 120
      }
    },
    {
      "files": "*.md",
      "options": {
        "proseWrap": "always"
      }
    }
  ]
}
```

```
# .prettierignore
node_modules/
dist/
build/
coverage/
.next/
out/
pnpm-lock.yaml
package-lock.json
yarn.lock
*.min.js
*.min.css
```

## Phase 5: Generate Jest Configuration

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  testMatch: [
    '**/__tests__/**/*.+(ts|tsx|js)',
    '**/?(*.)+(spec|test).+(ts|tsx|js)',
  ],
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest',
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.tsx',
    '!src/index.tsx',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@components/(.*)$': '<rootDir>/src/components/$1',
    '^@utils/(.*)$': '<rootDir>/src/utils/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/__mocks__/fileMock.js',
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  globals: {
    'ts-jest': {
      tsconfig: {
        jsx: 'react',
      },
    },
  },
  testPathIgnorePatterns: ['/node_modules/', '/dist/', '/build/'],
  watchPathIgnorePatterns: ['/node_modules/', '/dist/', '/build/'],
};
```

```javascript
// jest.setup.js
import '@testing-library/jest-dom';

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return [];
  }
  unobserve() {}
};
```

## Phase 6: Generate Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./vitest.setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/mockData/',
      ],
      thresholds: {
        lines: 70,
        functions: 70,
        branches: 70,
        statements: 70,
      },
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },
});
```

## Phase 7: Generate .gitignore

```
# Dependencies
node_modules/
.pnp
.pnp.js

# Testing
coverage/
.nyc_output

# Production
build/
dist/
out/
.next/

# Misc
.DS_Store
*.pem
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Local env files
.env
.env*.local
.env.development.local
.env.test.local
.env.production.local

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
```

## Phase 8: Generate Vite Configuration

```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@utils': path.resolve(__dirname, './src/utils'),
    },
  },
  server: {
    port: 3000,
    open: true,
    cors: true,
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
  optimizeDeps: {
    include: ['react', 'react-dom'],
  },
});
```

## Summary

```bash
echo ""
echo "=== ✓ Configuration Generation Complete ==="
echo ""
echo "📁 Generated configuration files:"

if [ "$HAS_TYPESCRIPT" = true ]; then
    echo "  ✓ tsconfig.json          # TypeScript configuration"
fi

echo "  ✓ .eslintrc.js           # ESLint rules"
echo "  ✓ .eslintignore          # ESLint ignore patterns"
echo "  ✓ .prettierrc            # Prettier formatting"
echo "  ✓ .prettierignore        # Prettier ignore patterns"

if [ "$TEST_FRAMEWORK" = "jest" ]; then
    echo "  ✓ jest.config.js         # Jest test configuration"
    echo "  ✓ jest.setup.js          # Jest setup file"
elif [ "$TEST_FRAMEWORK" = "vitest" ]; then
    echo "  ✓ vitest.config.ts       # Vitest configuration"
    echo "  ✓ vitest.setup.ts        # Vitest setup file"
fi

echo "  ✓ .gitignore             # Git ignore patterns"

echo ""
echo "📦 Install required dependencies:"
echo ""

if [ "$HAS_TYPESCRIPT" = true ]; then
    echo "$PKG_MANAGER add -D typescript @types/node"
fi

echo "$PKG_MANAGER add -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin"
echo "$PKG_MANAGER add -D prettier eslint-config-prettier"

if [ "$FRAMEWORK" = "react" ]; then
    echo "$PKG_MANAGER add -D eslint-plugin-react eslint-plugin-react-hooks"
    echo "$PKG_MANAGER add -D eslint-plugin-jsx-a11y"
fi

echo "$PKG_MANAGER add -D eslint-plugin-import"

if [ "$TEST_FRAMEWORK" = "jest" ]; then
    echo "$PKG_MANAGER add -D jest ts-jest @testing-library/react @testing-library/jest-dom"
elif [ "$TEST_FRAMEWORK" = "vitest" ]; then
    echo "$PKG_MANAGER add -D vitest @vitest/ui @testing-library/react"
fi

echo ""
echo "🚀 Add scripts to package.json:"
echo ""
echo '  "scripts": {'
echo '    "lint": "eslint . --ext .ts,.tsx",'
echo '    "lint:fix": "eslint . --ext .ts,.tsx --fix",'
echo '    "format": "prettier --write \"src/**/*.{ts,tsx,json,md}\"",'
echo '    "format:check": "prettier --check \"src/**/*.{ts,tsx,json,md}\"",'
echo '    "type-check": "tsc --noEmit"'
echo '  }'
echo ""
echo "💡 Next steps:"
echo "  1. Install dependencies"
echo "  2. Run: $PKG_MANAGER run lint"
echo "  3. Run: $PKG_MANAGER run format"
echo "  4. Configure IDE to use these configs"
```

## Best Practices

**Configuration Quality:**
- Start with strict settings
- Relax rules only when needed
- Use framework-specific presets
- Keep configs in sync

**Maintenance:**
- Update dependencies regularly
- Review deprecated rules
- Test config changes
- Document custom rules

**Integration Points:**
- `/ci-setup` - Add to CI pipeline
- `/format` - Use for code formatting
- `/review` - Check code quality

## What I'll Actually Do

1. **Detect project** - Framework and tools
2. **Generate configs** - Optimized for project
3. **Add best practices** - Strict but practical
4. **Framework-specific** - Tailored settings
5. **Complete setup** - All necessary files

**Important:** I will NEVER add AI attribution.

**Credits:** Configuration patterns based on TypeScript, ESLint, Prettier, Jest, and Vitest official documentation and community best practices.
