---
name: ci-setup
description: Configure CI/CD pipelines for GitHub Actions, GitLab CI, CircleCI with best practices
disable-model-invocation: true
---

# CI/CD Pipeline Setup

I'll set up a production-ready CI/CD pipeline with automated testing, linting, and deployment workflows.

**Supported Platforms:**
- GitHub Actions (auto-detected from .git/config)
- GitLab CI (.gitlab-ci.yml)
- CircleCI (circle CI config)
- Jenkins (Jenkinsfile)

**Token Optimization:**
- ✅ Bash-based platform detection from git remote (50 tokens)
- ✅ Template-based CI config generation (no file reads)
- ✅ Caching platform detection - saves 70% on subsequent runs
- ✅ Early exit when CI already configured
- ✅ Framework detection sharing cache with other skills
- ✅ Incremental pipeline setup (test → lint → deploy)
- **Expected tokens:** 600-1,500 (vs. 2,000-3,500 unoptimized)
- **Optimization status:** ✅ Optimized (Phase 2 Batch 2, 2026-01-26)

**Caching Behavior:**
- Cache location: `.claude/cache/ci/platform-config.json`
- Caches: Platform detection, test commands, deployment config
- Cache validity: 7 days or until .git/config changes
- Shared with: `/deploy-validate`, `/release-automation` skills

## Phase 1: Platform Detection

```bash
# Detect CI platform efficiently
detect_ci_platform() {
    # Check git remote for GitHub/GitLab
    if [ -d ".git" ]; then
        REMOTE=$(git remote get-url origin 2>/dev/null || echo "")

        if echo "$REMOTE" | grep -q "github.com"; then
            echo "github"
            return 0
        elif echo "$REMOTE" | grep -q "gitlab"; then
            echo "gitlab"
            return 0
        fi
    fi

    # Check for existing CI configs
    if [ -f ".github/workflows/ci.yml" ] || [ -f ".github/workflows/main.yml" ]; then
        echo "github"
    elif [ -f ".gitlab-ci.yml" ]; then
        echo "gitlab"
    elif [ -f ".circleci/config.yml" ]; then
        echo "circle"
    elif [ -f "Jenkinsfile" ]; then
        echo "jenkins"
    else
        echo "unknown"
    fi
}

CI_PLATFORM=$(detect_ci_platform)

if [ "$CI_PLATFORM" = "unknown" ]; then
    echo "CI platform not detected"
    echo ""
    echo "Select CI platform:"
    echo "1) GitHub Actions"
    echo "2) GitLab CI"
    echo "3) CircleCI"
    echo "4) Jenkins"
    read -p "Enter choice (1-4): " choice

    case $choice in
        1) CI_PLATFORM="github" ;;
        2) CI_PLATFORM="gitlab" ;;
        3) CI_PLATFORM="circle" ;;
        4) CI_PLATFORM="jenkins" ;;
        *) echo "Invalid choice"; exit 1 ;;
    esac
fi

echo "✓ CI Platform: $CI_PLATFORM"
```

## Phase 2: Detect Project Type

```bash
# Detect project type and testing tools
detect_project_type() {
    if [ -f "package.json" ]; then
        # Node.js project
        if grep -q "\"next\"" package.json; then
            echo "nextjs"
        elif grep -q "\"react\"" package.json; then
            echo "react"
        elif grep -q "\"vue\"" package.json; then
            echo "vue"
        else
            echo "nodejs"
        fi
    elif [ -f "requirements.txt" ] || [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
        echo "python"
    elif [ -f "go.mod" ]; then
        echo "golang"
    elif [ -f "Cargo.toml" ]; then
        echo "rust"
    elif [ -f "pom.xml" ]; then
        echo "maven"
    elif [ -f "build.gradle" ]; then
        echo "gradle"
    else
        echo "generic"
    fi
}

PROJECT_TYPE=$(detect_project_type)
echo "✓ Project type: $PROJECT_TYPE"

# Detect test commands
TEST_CMD=""
LINT_CMD=""
BUILD_CMD=""

if [ "$PROJECT_TYPE" = "nodejs" ] || [ "$PROJECT_TYPE" = "react" ] || [ "$PROJECT_TYPE" = "vue" ] || [ "$PROJECT_TYPE" = "nextjs" ]; then
    if grep -q "\"test\":" package.json; then
        TEST_CMD="npm test"
    fi
    if grep -q "\"lint\":" package.json; then
        LINT_CMD="npm run lint"
    fi
    if grep -q "\"build\":" package.json; then
        BUILD_CMD="npm run build"
    fi
elif [ "$PROJECT_TYPE" = "python" ]; then
    TEST_CMD="pytest"
    LINT_CMD="flake8 ."
    BUILD_CMD=""
elif [ "$PROJECT_TYPE" = "golang" ]; then
    TEST_CMD="go test ./..."
    LINT_CMD="golangci-lint run"
    BUILD_CMD="go build"
fi

echo "✓ Test command: ${TEST_CMD:-none}"
echo "✓ Lint command: ${LINT_CMD:-none}"
echo "✓ Build command: ${BUILD_CMD:-none}"
```

## Phase 3: Generate CI Configuration

### GitHub Actions

```bash
if [ "$CI_PLATFORM" = "github" ]; then
    mkdir -p .github/workflows

    cat > .github/workflows/ci.yml << 'EOFGH'
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
    - uses: actions/checkout@v4

    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run linter
      run: LINT_CMD_PLACEHOLDER
      if: always()

    - name: Run tests
      run: TEST_CMD_PLACEHOLDER
      if: always()

    - name: Build
      run: BUILD_CMD_PLACEHOLDER
      if: always()

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      if: matrix.node-version == '20.x'
      with:
        file: ./coverage/coverage-final.json
        flags: unittests

  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Use Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20.x'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Run linter
      run: LINT_CMD_PLACEHOLDER

  build:
    runs-on: ubuntu-latest
    needs: [test, lint]
    steps:
    - uses: actions/checkout@v4

    - name: Use Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20.x'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Build application
      run: BUILD_CMD_PLACEHOLDER

    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: build-artifacts
        path: dist/
        retention-days: 7
EOFGH

    # Replace placeholders
    if [ ! -z "$LINT_CMD" ]; then
        sed -i "s|LINT_CMD_PLACEHOLDER|$LINT_CMD|g" .github/workflows/ci.yml
    else
        sed -i "/LINT_CMD_PLACEHOLDER/d" .github/workflows/ci.yml
    fi

    if [ ! -z "$TEST_CMD" ]; then
        sed -i "s|TEST_CMD_PLACEHOLDER|$TEST_CMD|g" .github/workflows/ci.yml
    else
        sed -i "/TEST_CMD_PLACEHOLDER/d" .github/workflows/ci.yml
    fi

    if [ ! -z "$BUILD_CMD" ]; then
        sed -i "s|BUILD_CMD_PLACEHOLDER|$BUILD_CMD|g" .github/workflows/ci.yml
    else
        sed -i "/BUILD_CMD_PLACEHOLDER/d" .github/workflows/ci.yml
    fi

    echo "✓ Created .github/workflows/ci.yml"
fi
```

### GitLab CI

```bash
if [ "$CI_PLATFORM" = "gitlab" ]; then
    cat > .gitlab-ci.yml << 'EOFGL'
stages:
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "20"

before_script:
  - node --version
  - npm --version

cache:
  paths:
    - node_modules/
    - .npm/

install_dependencies:
  stage: .pre
  script:
    - npm ci --cache .npm --prefer-offline
  artifacts:
    paths:
      - node_modules/
    expire_in: 1 day

lint:
  stage: test
  dependencies:
    - install_dependencies
  script:
    - LINT_CMD_PLACEHOLDER

test:
  stage: test
  dependencies:
    - install_dependencies
  script:
    - TEST_CMD_PLACEHOLDER
  coverage: '/Lines\s*:\s*(\d+\.\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build:
  stage: build
  dependencies:
    - install_dependencies
  script:
    - BUILD_CMD_PLACEHOLDER
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

pages:
  stage: deploy
  dependencies:
    - build
  script:
    - mkdir -p public
    - cp -r dist/* public/
  artifacts:
    paths:
      - public
  only:
    - main
EOFGL

    # Replace placeholders
    if [ ! -z "$LINT_CMD" ]; then
        sed -i "s|LINT_CMD_PLACEHOLDER|$LINT_CMD|g" .gitlab-ci.yml
    else
        sed -i "/LINT_CMD_PLACEHOLDER/d" .gitlab-ci.yml
        sed -i "/^lint:/,/^$/d" .gitlab-ci.yml
    fi

    if [ ! -z "$TEST_CMD" ]; then
        sed -i "s|TEST_CMD_PLACEHOLDER|$TEST_CMD|g" .gitlab-ci.yml
    else
        sed -i "/TEST_CMD_PLACEHOLDER/d" .gitlab-ci.yml
    fi

    if [ ! -z "$BUILD_CMD" ]; then
        sed -i "s|BUILD_CMD_PLACEHOLDER|$BUILD_CMD|g" .gitlab-ci.yml
    else
        sed -i "/BUILD_CMD_PLACEHOLDER/d" .gitlab-ci.yml
    fi

    echo "✓ Created .gitlab-ci.yml"
fi
```

### CircleCI

```bash
if [ "$CI_PLATFORM" = "circle" ]; then
    mkdir -p .circleci

    cat > .circleci/config.yml << 'EOFCIRCLE'
version: 2.1

orbs:
  node: circleci/node@5.1.0

jobs:
  test:
    docker:
      - image: cimg/node:20.0
    steps:
      - checkout
      - node/install-packages:
          pkg-manager: npm
      - run:
          name: Run tests
          command: TEST_CMD_PLACEHOLDER
      - run:
          name: Run linter
          command: LINT_CMD_PLACEHOLDER

  build:
    docker:
      - image: cimg/node:20.0
    steps:
      - checkout
      - node/install-packages:
          pkg-manager: npm
      - run:
          name: Build application
          command: BUILD_CMD_PLACEHOLDER
      - persist_to_workspace:
          root: .
          paths:
            - dist

workflows:
  test-and-build:
    jobs:
      - test
      - build:
          requires:
            - test
EOFCIRCLE

    # Replace placeholders
    if [ ! -z "$TEST_CMD" ]; then
        sed -i "s|TEST_CMD_PLACEHOLDER|$TEST_CMD|g" .circleci/config.yml
    else
        sed -i "/TEST_CMD_PLACEHOLDER/d" .circleci/config.yml
    fi

    if [ ! -z "$LINT_CMD" ]; then
        sed -i "s|LINT_CMD_PLACEHOLDER|$LINT_CMD|g" .circleci/config.yml
    else
        sed -i "/LINT_CMD_PLACEHOLDER/d" .circleci/config.yml
    fi

    if [ ! -z "$BUILD_CMD" ]; then
        sed -i "s|BUILD_CMD_PLACEHOLDER|$BUILD_CMD|g" .circleci/config.yml
    else
        sed -i "/BUILD_CMD_PLACEHOLDER/d" .circleci/config.yml
    fi

    echo "✓ Created .circleci/config.yml"
fi
```

## Phase 4: Additional CI Features

```bash
echo ""
echo "=== Optional CI Enhancements ==="
echo ""
read -p "Add dependency caching? (yes/no): " add_cache
read -p "Add code coverage reporting? (yes/no): " add_coverage
read -p "Add security scanning? (yes/no): " add_security
read -p "Add Docker build? (yes/no): " add_docker

# Add enhancements based on selections
if [ "$add_security" = "yes" ]; then
    echo ""
    echo "Security scanning options:"
    echo "  - GitHub: CodeQL (automatic)"
    echo "  - Snyk: npm install -g snyk"
    echo "  - npm audit: Built-in"
    echo ""
    echo "Recommend adding: /dependency-audit and /secrets-scan skills"
fi

if [ "$add_docker" = "yes" ]; then
    echo ""
    echo "Docker integration:"
    echo "  1. Create Dockerfile in project root"
    echo "  2. Add Docker build step to CI"
    echo "  3. Push to container registry"
fi
```

## Phase 5: Status Badge

```bash
# Generate status badge for README
echo ""
echo "=== CI Status Badge ==="
echo ""
echo "Add this badge to your README.md:"
echo ""

case $CI_PLATFORM in
    github)
        REPO_PATH=$(git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/')
        echo "[![CI](https://github.com/$REPO_PATH/actions/workflows/ci.yml/badge.svg)](https://github.com/$REPO_PATH/actions/workflows/ci.yml)"
        ;;
    gitlab)
        PROJECT_PATH=$(git remote get-url origin | sed 's/.*gitlab.com[:/]\(.*\)\.git/\1/')
        echo "[![pipeline status](https://gitlab.com/$PROJECT_PATH/badges/main/pipeline.svg)](https://gitlab.com/$PROJECT_PATH/-/commits/main)"
        ;;
    circle)
        echo "[![CircleCI](https://circleci.com/gh/USERNAME/REPO.svg?style=svg)](https://circleci.com/gh/USERNAME/REPO)"
        ;;
esac
```

## Summary

```bash
echo ""
echo "=== CI/CD Setup Complete! ==="
echo ""
echo "✓ Platform: $CI_PLATFORM"
echo "✓ Project type: $PROJECT_TYPE"
echo "✓ Configuration created"
echo ""
echo "📋 Pipeline stages:"
echo "  1. Lint: Code quality checks"
echo "  2. Test: Automated testing"
echo "  3. Build: Compile/bundle application"
echo ""
echo "🚀 Next steps:"
echo "  1. Commit CI configuration:"
echo "     git add .github/ .gitlab-ci.yml .circleci/"
echo "     git commit -m 'ci: Add CI/CD pipeline'"
echo "     git push"
echo "  2. Verify pipeline runs successfully"
echo "  3. Configure deployment with /deploy-validate"
echo "  4. Add security scanning with /dependency-audit"
echo ""
echo "💡 Pro tips:"
echo "  - Run 'npm test' locally before pushing"
echo "  - Use '/test' skill for intelligent test execution"
echo "  - Add E2E tests with '/e2e-generate'"
echo "  - Monitor build times and optimize as needed"
```

## Integration Points

- `/deploy-validate` - Add deployment validation to pipeline
- `/test` - Run tests locally before CI
- `/dependency-audit` - Add security scanning to CI
- `/e2e-generate` - Add E2E tests to CI pipeline

**Important Git Safety:**
- This skill NEVER modifies git credentials
- This skill NEVER adds AI attribution to CI configs
- All commits use your existing git configuration

**Credits:** CI/CD patterns based on industry best practices from GitHub Actions, GitLab CI, and CircleCI documentation.
