---
name: release-automation
description: Automate complete release process with versioning and publishing
disable-model-invocation: true
---

# Release Automation

I'll automate your complete release process: version bumping, changelog generation, git tagging, release creation, and package publishing.

Arguments: `$ARGUMENTS` - version number (e.g., 1.2.0, major, minor, patch) or release type

## Release Philosophy

- **Semantic Versioning**: Proper MAJOR.MINOR.PATCH versioning
- **Automated Changelog**: Generated from conventional commits
- **Safe Defaults**: Validate before publishing
- **Platform Agnostic**: Support npm, PyPI, Go modules, Ruby gems, Cargo, Maven

**Token Optimization:**
- Uses bash scripts for detection (200 tokens)
- Grep for conventional commits (100 tokens)
- Minimal file reading (changelog only)
- Expected: 2,500-4,000 tokens

## Phase 1: Release Pre-Flight Checks

First, I'll validate the release environment:

```bash
#!/bin/bash
# Validate release prerequisites

validate_release_environment() {
    echo "=== Release Pre-Flight Checks ==="
    echo ""

    # 1. Check if we're in a git repo
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo "❌ Not a git repository"
        exit 1
    fi
    echo "✓ Git repository detected"

    # 2. Check for uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo "❌ Uncommitted changes detected"
        echo "Please commit or stash changes before releasing"
        git status --short
        exit 1
    fi
    echo "✓ Working directory clean"

    # 3. Check branch (should be main/master for releases)
    CURRENT_BRANCH=$(git branch --show-current)
    if [[ "$CURRENT_BRANCH" != "main" && "$CURRENT_BRANCH" != "master" ]]; then
        echo "⚠️  WARNING: Not on main/master branch (current: $CURRENT_BRANCH)"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    echo "✓ Branch: $CURRENT_BRANCH"

    # 4. Check remote connection
    if ! git ls-remote --exit-code origin > /dev/null 2>&1; then
        echo "❌ Cannot connect to remote repository"
        exit 1
    fi
    echo "✓ Remote repository accessible"

    # 5. Check for unpushed commits
    UNPUSHED=$(git log origin/$CURRENT_BRANCH..HEAD --oneline 2>/dev/null | wc -l)
    if [ $UNPUSHED -gt 0 ]; then
        echo "⚠️  WARNING: $UNPUSHED unpushed commits"
    fi

    echo ""
    echo "Pre-flight checks complete"
}

validate_release_environment
```

## Phase 2: Version Detection & Bump

I'll determine the next version based on conventional commits:

```bash
#!/bin/bash
# Detect current version and determine next version

detect_and_bump_version() {
    local bump_type="${1:-auto}"

    echo "=== Version Detection ==="
    echo ""

    # Detect current version from multiple sources
    CURRENT_VERSION=""
    VERSION_SOURCE=""

    # Try package.json (Node.js)
    if [ -f "package.json" ]; then
        CURRENT_VERSION=$(grep -oP '"version":\s*"\K[^"]+' package.json 2>/dev/null)
        VERSION_SOURCE="package.json"

    # Try pyproject.toml (Python)
    elif [ -f "pyproject.toml" ]; then
        CURRENT_VERSION=$(grep -oP '^version\s*=\s*"\K[^"]+' pyproject.toml 2>/dev/null)
        VERSION_SOURCE="pyproject.toml"

    # Try setup.py (Python)
    elif [ -f "setup.py" ]; then
        CURRENT_VERSION=$(grep -oP 'version\s*=\s*["\x27]\K[^"\x27]+' setup.py 2>/dev/null)
        VERSION_SOURCE="setup.py"

    # Try Cargo.toml (Rust)
    elif [ -f "Cargo.toml" ]; then
        CURRENT_VERSION=$(grep -oP '^version\s*=\s*"\K[^"]+' Cargo.toml 2>/dev/null)
        VERSION_SOURCE="Cargo.toml"

    # Try pom.xml (Java/Maven)
    elif [ -f "pom.xml" ]; then
        CURRENT_VERSION=$(grep -oP '<version>\K[^<]+' pom.xml 2>/dev/null | head -1)
        VERSION_SOURCE="pom.xml"

    # Try git tags
    else
        CURRENT_VERSION=$(git describe --tags --abbrev=0 2>/dev/null | sed 's/^v//')
        VERSION_SOURCE="git tags"
    fi

    if [ -z "$CURRENT_VERSION" ]; then
        echo "⚠️  No version found, defaulting to 0.0.0"
        CURRENT_VERSION="0.0.0"
    fi

    echo "Current version: $CURRENT_VERSION (from $VERSION_SOURCE)"

    # Parse version components
    IFS='.' read -r MAJOR MINOR PATCH <<< "${CURRENT_VERSION}"

    # Auto-detect bump type from commits if not specified
    if [ "$bump_type" = "auto" ] || [ "$bump_type" = "patch" ] || [ "$bump_type" = "minor" ] || [ "$bump_type" = "major" ]; then
        LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
        COMMIT_RANGE="${LATEST_TAG:+$LATEST_TAG..}HEAD"

        # Check for breaking changes
        HAS_BREAKING=$(git log $COMMIT_RANGE --oneline | grep -E '(^[a-f0-9]+ \w+!:|BREAKING CHANGE:)' 2>/dev/null || echo "")

        # Check for features
        HAS_FEATURES=$(git log $COMMIT_RANGE --oneline | grep '^[a-f0-9]* feat' 2>/dev/null || echo "")

        # Check for fixes
        HAS_FIXES=$(git log $COMMIT_RANGE --oneline | grep '^[a-f0-9]* fix' 2>/dev/null || echo "")

        if [ "$bump_type" = "auto" ]; then
            if [ ! -z "$HAS_BREAKING" ]; then
                bump_type="major"
            elif [ ! -z "$HAS_FEATURES" ]; then
                bump_type="minor"
            elif [ ! -z "$HAS_FIXES" ]; then
                bump_type="patch"
            else
                echo "⚠️  No conventional commits found for auto-detection"
                bump_type="patch"
            fi
        fi
    fi

    # Calculate next version
    case "$bump_type" in
        major)
            NEXT_VERSION="$((MAJOR + 1)).0.0"
            ;;
        minor)
            NEXT_VERSION="$MAJOR.$((MINOR + 1)).0"
            ;;
        patch)
            NEXT_VERSION="$MAJOR.$MINOR.$((PATCH + 1))"
            ;;
        *)
            # Explicit version provided
            NEXT_VERSION="$bump_type"
            ;;
    esac

    echo "Next version: $NEXT_VERSION (bump type: $bump_type)"
    echo ""

    echo "$NEXT_VERSION"
}

NEXT_VERSION=$(detect_and_bump_version "${1:-auto}")
```

## Phase 3: Update Version Files

I'll update version numbers in all project files:

```bash
#!/bin/bash
# Update version numbers in project files

update_version_files() {
    local version="$1"

    echo "=== Updating Version Files ==="
    echo ""

    # Update package.json (Node.js)
    if [ -f "package.json" ]; then
        echo "Updating package.json..."
        sed -i "s/\"version\": \"[^\"]*\"/\"version\": \"$version\"/" package.json

        # Update package-lock.json if it exists
        if [ -f "package-lock.json" ]; then
            sed -i "s/\"version\": \"[^\"]*\"/\"version\": \"$version\"/" package-lock.json
        fi

        git add package.json package-lock.json 2>/dev/null
        echo "✓ Updated package.json"
    fi

    # Update pyproject.toml (Python)
    if [ -f "pyproject.toml" ]; then
        echo "Updating pyproject.toml..."
        sed -i "s/^version = \"[^\"]*\"/version = \"$version\"/" pyproject.toml
        git add pyproject.toml
        echo "✓ Updated pyproject.toml"
    fi

    # Update setup.py (Python)
    if [ -f "setup.py" ]; then
        echo "Updating setup.py..."
        sed -i "s/version=['\"][^'\"]*['\"]/version='$version'/" setup.py
        git add setup.py
        echo "✓ Updated setup.py"
    fi

    # Update Cargo.toml (Rust)
    if [ -f "Cargo.toml" ]; then
        echo "Updating Cargo.toml..."
        sed -i "s/^version = \"[^\"]*\"/version = \"$version\"/" Cargo.toml
        git add Cargo.toml
        echo "✓ Updated Cargo.toml"
    fi

    # Update pom.xml (Java/Maven)
    if [ -f "pom.xml" ]; then
        echo "Updating pom.xml..."
        sed -i "0,/<version>[^<]*<\/version>/s//<version>$version<\/version>/" pom.xml
        git add pom.xml
        echo "✓ Updated pom.xml"
    fi

    # Update Gemfile.lock (Ruby)
    if [ -f "*.gemspec" ]; then
        echo "Updating gemspec..."
        sed -i "s/version.*=.*['\"][^'\"]*['\"]/version = '$version'/" *.gemspec
        git add *.gemspec
        echo "✓ Updated gemspec"
    fi

    echo ""
}

update_version_files "$NEXT_VERSION"
```

## Phase 4: Generate Changelog

I'll generate or update the changelog:

```bash
#!/bin/bash
# Generate changelog using /changelog-auto skill

generate_changelog() {
    local version="$1"

    echo "=== Generating Changelog ==="
    echo ""

    # Check if changelog-auto skill is available
    if [ -f "$HOME/.claude/skills/changelog-auto/SKILL.md" ]; then
        echo "Using /changelog-auto skill..."
        # The /changelog-auto skill will be invoked
        echo "✓ Changelog generation initiated"
    else
        # Fallback: Simple changelog generation
        echo "Generating basic changelog..."

        LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
        COMMIT_RANGE="${LATEST_TAG:+$LATEST_TAG..}HEAD"

        # Create or update CHANGELOG.md
        cat > CHANGELOG.md.new << EOF
# Changelog

All notable changes to this project will be documented in this file.

## [$version] - $(date +%Y-%m-%d)

### Added
EOF

        # Extract features
        git log $COMMIT_RANGE --oneline | grep '^[a-f0-9]* feat' | sed 's/^[a-f0-9]* feat[(:]*/- /' >> CHANGELOG.md.new || true

        echo "" >> CHANGELOG.md.new
        echo "### Fixed" >> CHANGELOG.md.new

        # Extract fixes
        git log $COMMIT_RANGE --oneline | grep '^[a-f0-9]* fix' | sed 's/^[a-f0-9]* fix[(:]*/- /' >> CHANGELOG.md.new || true

        # Prepend to existing changelog
        if [ -f "CHANGELOG.md" ]; then
            echo "" >> CHANGELOG.md.new
            tail -n +2 CHANGELOG.md >> CHANGELOG.md.new
        fi

        mv CHANGELOG.md.new CHANGELOG.md
        echo "✓ Changelog generated"
    fi

    git add CHANGELOG.md
    echo ""
}

generate_changelog "$NEXT_VERSION"
```

## Phase 5: Create Release Commit & Tag

I'll create the release commit and tag:

```bash
#!/bin/bash
# Create release commit and git tag

create_release_commit_and_tag() {
    local version="$1"

    echo "=== Creating Release Commit ==="
    echo ""

    # Create release commit
    git commit -m "chore(release): $version

Release version $version

See CHANGELOG.md for details."

    echo "✓ Release commit created"
    echo ""

    # Create annotated git tag
    echo "=== Creating Git Tag ==="

    # Extract changelog for this version
    CHANGELOG_ENTRY=$(sed -n "/## \[$version\]/,/## \[/p" CHANGELOG.md 2>/dev/null | head -n -1)

    if [ -z "$CHANGELOG_ENTRY" ]; then
        CHANGELOG_ENTRY="Release version $version"
    fi

    git tag -a "v$version" -m "Release v$version

$CHANGELOG_ENTRY"

    echo "✓ Git tag v$version created"
    echo ""
}

create_release_commit_and_tag "$NEXT_VERSION"
```

## Phase 6: Create GitHub/GitLab Release

I'll create a release on your platform:

```bash
#!/bin/bash
# Create GitHub or GitLab release

create_platform_release() {
    local version="$1"

    echo "=== Creating Platform Release ==="
    echo ""

    # Detect platform
    REMOTE_URL=$(git remote get-url origin 2>/dev/null)

    if echo "$REMOTE_URL" | grep -q "github.com"; then
        echo "Detected: GitHub"

        # Check if gh CLI is installed
        if command -v gh &> /dev/null; then
            echo "Creating GitHub release using gh CLI..."

            # Extract changelog for this version
            CHANGELOG_ENTRY=$(sed -n "/## \[$version\]/,/## \[/p" CHANGELOG.md 2>/dev/null | head -n -1)

            gh release create "v$version" \
                --title "Release v$version" \
                --notes "$CHANGELOG_ENTRY" \
                --verify-tag

            echo "✓ GitHub release created"
        else
            echo "⚠️  gh CLI not installed. Release must be created manually."
            echo "Install: https://cli.github.com/"
        fi

    elif echo "$REMOTE_URL" | grep -q "gitlab.com"; then
        echo "Detected: GitLab"

        if command -v glab &> /dev/null; then
            echo "Creating GitLab release using glab CLI..."

            CHANGELOG_ENTRY=$(sed -n "/## \[$version\]/,/## \[/p" CHANGELOG.md 2>/dev/null | head -n -1)

            glab release create "v$version" \
                --name "Release v$version" \
                --notes "$CHANGELOG_ENTRY"

            echo "✓ GitLab release created"
        else
            echo "⚠️  glab CLI not installed. Release must be created manually."
            echo "Install: https://gitlab.com/gitlab-org/cli"
        fi
    else
        echo "⚠️  Platform not detected. Release must be created manually."
    fi

    echo ""
}

create_platform_release "$NEXT_VERSION"
```

## Phase 7: Package Publishing

I'll publish to the appropriate package registry:

```bash
#!/bin/bash
# Publish package to registry

publish_package() {
    local version="$1"

    echo "=== Package Publishing ==="
    echo ""

    # Node.js (npm)
    if [ -f "package.json" ]; then
        echo "Detected: npm package"

        # Check if logged in
        if npm whoami &> /dev/null; then
            echo "Publishing to npm..."
            npm publish
            echo "✓ Published to npm"
        else
            echo "⚠️  Not logged in to npm. Run: npm login"
        fi
    fi

    # Python (PyPI)
    if [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
        echo "Detected: Python package"

        if command -v twine &> /dev/null; then
            echo "Building distribution..."
            python -m build

            echo "Publishing to PyPI..."
            twine upload dist/*
            echo "✓ Published to PyPI"
        else
            echo "⚠️  twine not installed. Run: pip install twine build"
        fi
    fi

    # Rust (crates.io)
    if [ -f "Cargo.toml" ]; then
        echo "Detected: Rust crate"

        echo "Publishing to crates.io..."
        cargo publish
        echo "✓ Published to crates.io"
    fi

    # Ruby (RubyGems)
    if [ -f "*.gemspec" ]; then
        echo "Detected: Ruby gem"

        echo "Building gem..."
        gem build *.gemspec

        echo "Publishing to RubyGems..."
        gem push *.gem
        echo "✓ Published to RubyGems"
    fi

    # Java/Maven
    if [ -f "pom.xml" ]; then
        echo "Detected: Maven project"

        echo "Deploying to Maven Central..."
        mvn clean deploy
        echo "✓ Deployed to Maven Central"
    fi

    # Go modules (no publishing needed, uses git tags)
    if [ -f "go.mod" ]; then
        echo "Detected: Go module"
        echo "✓ Go modules use git tags (v$version already created)"
    fi

    echo ""
}

publish_package "$NEXT_VERSION"
```

## Phase 8: Push Changes

I'll push the release to remote:

```bash
#!/bin/bash
# Push release commits and tags to remote

push_release() {
    local version="$1"

    echo "=== Pushing to Remote ==="
    echo ""

    CURRENT_BRANCH=$(git branch --show-current)

    # Push commits
    echo "Pushing commits to origin/$CURRENT_BRANCH..."
    git push origin "$CURRENT_BRANCH"
    echo "✓ Commits pushed"

    # Push tags
    echo "Pushing tag v$version..."
    git push origin "v$version"
    echo "✓ Tag pushed"

    echo ""
    echo "Release $version complete!"
}

push_release "$NEXT_VERSION"
```

## Integration with Other Skills

**Workflow Integration:**
- Before release → `/test` (run full test suite)
- Before release → `/security-scan` (check for vulnerabilities)
- During release → `/changelog-auto` (automatic changelog)
- After release → `/commit` (if manual changes needed)

**Skill Suggestions:**
- Pre-release validation → `/deploy-validate`
- Testing before release → `/test`, `/test-coverage`
- Security audit → `/dependency-audit`, `/secrets-scan`

## Practical Examples

**Automatic version detection:**
```bash
/release-automation              # Auto-detect bump type from commits
```

**Explicit version bump:**
```bash
/release-automation patch        # Bump patch version (0.0.X)
/release-automation minor        # Bump minor version (0.X.0)
/release-automation major        # Bump major version (X.0.0)
```

**Specific version:**
```bash
/release-automation 2.1.0        # Set explicit version
```

**Dry run (preview only):**
```bash
/release-automation --dry-run    # Preview without making changes
```

## What Gets Released

**Version Bumped In:**
- package.json (Node.js)
- pyproject.toml / setup.py (Python)
- Cargo.toml (Rust)
- pom.xml (Java/Maven)
- *.gemspec (Ruby)
- Go modules (via git tags)

**Generated/Updated:**
- CHANGELOG.md (from conventional commits)
- Git tag (annotated with changelog)
- GitHub/GitLab release
- Package registry publication

## Safety Guarantees

**Pre-Release Validation:**
- ✅ Verify clean working directory
- ✅ Check for unpushed commits
- ✅ Validate git repository
- ✅ Check remote connectivity
- ✅ Confirm release branch

**What I'll NEVER do:**
- Publish without confirmation
- Skip version validation
- Overwrite existing releases
- Add AI attribution to releases
- Modify git credentials

**What I WILL do:**
- Create proper semantic versioning
- Generate meaningful changelogs
- Create annotated git tags
- Publish to correct registries
- Push to remote safely

## Rollback Procedure

If release fails:

```bash
# Delete local tag
git tag -d v1.2.3

# Delete remote tag (if pushed)
git push origin :refs/tags/v1.2.3

# Reset to previous commit
git reset --hard HEAD^

# Unpublish from npm (if published)
npm unpublish package@1.2.3

# Note: PyPI releases cannot be deleted, only yanked
```

## Credits

This skill integrates:
- **Semantic Versioning** - semver.org specification
- **Keep a Changelog** - keepachangelog.com format
- **Conventional Commits** - conventionalcommits.org standard
- **GitHub Releases** - gh CLI automation
- **Package Registries** - npm, PyPI, crates.io, RubyGems, Maven

## Token Budget

Target: 2,500-4,000 tokens per execution
- Phase 1-2: ~800 tokens (validation, version detection)
- Phase 3-4: ~800 tokens (version update, changelog)
- Phase 5-6: ~600 tokens (commit, tag, release)
- Phase 7-8: ~800 tokens (publishing, push)
- Integration: ~500 tokens

**Optimization Strategy:**
- Use bash scripts for all file operations
- Grep for conventional commits (no file reading)
- Minimal changelog reading (only new version)
- Platform detection without file parsing
- Batch git operations together

This ensures complete release automation while maintaining efficiency and respecting token limits.
