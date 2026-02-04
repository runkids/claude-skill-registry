#!/usr/bin/env python3
"""
Rebuild registry.json from downloaded skills.

Scans all skills/*/SKILL.md files and rebuilds the registry index.
"""

import json
import os
import re
import logging
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import yaml

from registry_normalization import CANONICAL_CATEGORIES, canonicalize_category, extract_github_location, normalize_repo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def infer_category_from_rel_parts(rel_parts: tuple[str, ...]) -> str | None:
    """
    Infer category from the path under `skills/`.

    This repo historically stored many skills under `skills/data/` (a legacy container
    directory) and also has a mix of flat and categorized layouts. We only infer a
    category when the directory structure clearly indicates it.
    """
    if not rel_parts:
        return None

    # Legacy storage container (NOT the canonical "data" category).
    if rel_parts[0] in {"data", "_legacy_data"}:
        return None

    if rel_parts[0] in CANONICAL_CATEGORIES:
        return rel_parts[0]

    return None


def extract_repo_from_frontmatter(frontmatter: dict) -> str:
    """Best-effort repo extraction from frontmatter fields."""
    if not frontmatter:
        return ""
    repo = frontmatter.get("repo") or frontmatter.get("repository") or ""
    if not repo:
        return ""
    return normalize_repo(str(repo))


def extract_repo_from_source(source_value: str) -> str:
    """Parse `github.com/{owner}/{repo}` style strings."""
    if not source_value:
        return ""
    source_value = str(source_value).strip()
    if source_value.startswith("github.com/"):
        return normalize_repo(source_value[len("github.com/"):])
    if "github.com/" in source_value:
        return normalize_repo(source_value.split("github.com/", 1)[1])
    return ""


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from SKILL.md."""
    if not content.startswith("---"):
        return {}

    try:
        # Find the closing ---
        end_idx = content.find("---", 3)
        if end_idx == -1:
            return {}

        frontmatter = content[3:end_idx].strip()
        data = yaml.safe_load(frontmatter)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def extract_description(content: str) -> str:
    """Extract description from content."""
    # Try frontmatter first
    fm = extract_frontmatter(content)
    if fm.get("description"):
        return fm["description"][:200]

    # Try first paragraph after frontmatter
    lines = content.split("\n")
    in_frontmatter = False

    for line in lines:
        line = line.strip()
        if line == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if line.startswith("#"):
            continue
        if line and not line.startswith("```"):
            # Clean markdown
            line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
            line = re.sub(r'[*_`]', '', line)
            return line[:200]

    return ""


def safe_load_metadata(metadata_path: Path) -> dict:
    """Safely load metadata.json"""
    if not metadata_path.exists():
        return {}
    try:
        with open(metadata_path, encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse error in {metadata_path}: {e}")
        return {}
    except Exception as e:
        logger.warning(f"Error reading {metadata_path}: {e}")
        return {}


def safe_write_registry(registry_path: Path, registry: dict) -> bool:
    """Safely write registry.json with atomic operation"""
    temp_path = registry_path.with_suffix('.json.tmp')
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)

        os.replace(temp_path, registry_path)
        return True
    except Exception as e:
        logger.error(f"Failed to write registry: {e}")
        if temp_path.exists():
            temp_path.unlink()
        return False


def scan_skills(skills_dir: Path) -> list:
    """
    Scan archived skills and build a normalized index.

    Supports mixed layouts seen in the archive:
    - <root>/<skill>/SKILL.md
    - <root>/data/<skill>/SKILL.md
    - <root>/<category>/<skill>/SKILL.md

    We detect a "skill directory" by the presence of both SKILL.md and metadata.json
    in the same folder, which avoids mis-parsing category folders.
    """
    skills = []

    if not skills_dir.exists():
        logger.warning(f"Skills directory not found: {skills_dir}")
        return skills

    for metadata_path in skills_dir.rglob("metadata.json"):
        skill_dir = metadata_path.parent
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        rel_dir = skill_dir.relative_to(skills_dir)
        rel_parts = rel_dir.parts

        # Skip "category root" folders that also contain many sub-skill folders.
        try:
            has_subskills = any((p / "SKILL.md").exists() for p in skill_dir.iterdir() if p.is_dir())
        except Exception:
            has_subskills = False
        if has_subskills:
            continue

        metadata = safe_load_metadata(metadata_path)

        repo = normalize_repo(metadata.get("repo", "")) or extract_repo_from_source(metadata.get("source", ""))

        # Read SKILL.md for frontmatter + description
        frontmatter = {}
        description = metadata.get("description", "")
        tags = metadata.get("tags", [])
        category_hint = infer_category_from_rel_parts(rel_parts)

        try:
            # Full file read is expensive but gives most accurate description.
            content = skill_md.read_text(encoding="utf-8")
            frontmatter = extract_frontmatter(content)
            if not description:
                description = extract_description(content)
            if not tags and isinstance(frontmatter.get("tags"), list):
                tags = frontmatter.get("tags", [])
        except UnicodeDecodeError as e:
            logger.warning(f"Encoding error reading {skill_md}: {e}")
        except Exception as e:
            logger.warning(f"Error reading {skill_md}: {e}")

        if not repo:
            repo = extract_repo_from_frontmatter(frontmatter)

        location = extract_github_location(metadata)

        # If metadata lacks github_path/path, try to use frontmatter "path" as fallback.
        if not location.path and frontmatter.get("path"):
            location = extract_github_location({"path": frontmatter.get("path"), "branch": frontmatter.get("branch")})

        raw_category = metadata.get("category") or frontmatter.get("category") or category_hint or "other"
        cat = canonicalize_category(str(raw_category), repo=repo)

        # Name selection: metadata > frontmatter > directory name
        name = metadata.get("name") or frontmatter.get("name") or skill_dir.name
        name = str(name).strip() if name is not None else skill_dir.name
        if not name:
            name = skill_dir.name

        stars = metadata.get("stars", 0)
        try:
            stars = int(stars) if stars is not None else 0
        except Exception:
            stars = 0

        if location.path and repo:
            install = f"{repo}/{location.path}"
        elif repo:
            install = repo
        else:
            # Must not look like a GitHub owner/repo path (the web UI builds links from this).
            install = f"local:{rel_dir.as_posix().replace('/', '~')}"

        skill_entry_data = {
            "name": name,
            "description": description[:200] if description else f"Skill: {name}",
            "repo": repo,
            "path": location.path,
            "branch": location.branch,
            "category": cat,
            "tags": tags or [],
            "stars": stars,
            "install": install,
            "source": metadata.get("source", "local"),
        }

        skills.append(skill_entry_data)

    return skills


def sanitize_category(category: str) -> str:
    """Sanitize category name for use as filename."""
    # Replace / and other problematic characters with -
    return category.replace("/", "-").replace("\\", "-").replace(":", "-")


def build_category_indexes(skills: list, output_dir: Path):
    """Build category-based indexes."""
    # This is intentionally destructive: categories are derived artifacts.
    # Keeping stale files makes the API and repo size explode.
    if output_dir.exists():
        for p in output_dir.glob("*.json"):
            try:
                p.unlink()
            except OSError:
                pass

    categories = defaultdict(list)

    for skill in skills:
        cat = skill.get("category", "other")
        # Sanitize category for filename safety
        safe_cat = sanitize_category(cat)
        categories[safe_cat].append(skill)

    output_dir.mkdir(exist_ok=True)

    for cat, cat_skills in categories.items():
        cat_file = output_dir / f"{cat}.json"
        cat_data = {
            "category": cat,
            "count": len(cat_skills),
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "skills": sorted(cat_skills, key=lambda x: (-x.get("stars", 0), x["name"])),
        }
        with open(cat_file, "w", encoding="utf-8") as f:
            json.dump(cat_data, f, indent=2, ensure_ascii=False)
        print(f"  {cat}: {len(cat_skills)} skills")

    # Index file
    index = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "categories": [
            {"name": cat, "count": len(skills)}
            for cat, skills in sorted(categories.items())
        ]
    }
    with open(output_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


def main():
    script_dir = Path(__file__).parent
    registry_dir = script_dir.parent
    skills_dir = registry_dir / "skills"
    categories_dir = registry_dir / "categories"

    print("=" * 60)
    print("REBUILDING REGISTRY FROM DOWNLOADED SKILLS")
    print("=" * 60)
    print()

    print("Scanning skills directory...")
    skills = scan_skills(skills_dir)
    print(f"Found {len(skills)} skills")
    print()

    # Remove duplicates by repo:path (more accurate than name-only)
    # This prevents losing skills with same name but different sources
    seen = set()
    unique_skills = []
    duplicates_removed = 0

    for s in skills:
        # Use repo:path as unique key (most accurate)
        repo = s.get("repo", "")
        path = s.get("path", "")

        if repo and path:
            key = f"{repo}:{path}"
        elif repo:
            # Avoid collapsing multiple skills in one repo when path is unknown.
            key = f"{repo}::{s.get('name', '')}"
        else:
            # Fallback to install (guaranteed not to look like owner/repo).
            key = s.get("install", "") or f"local::{s.get('name', '')}"

        if key not in seen:
            seen.add(key)
            unique_skills.append(s)
        else:
            duplicates_removed += 1

    print(f"Duplicates removed: {duplicates_removed}")

    print(f"Unique skills: {len(unique_skills)}")
    print()

    # Sort by stars then name
    unique_skills.sort(key=lambda x: (-x.get("stars", 0), x["name"].lower()))

    # Build registry
    registry = {
        "version": "2.0.0",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "total_count": len(unique_skills),
        "skills": unique_skills,
    }

    registry_path = registry_dir / "registry.json"
    if safe_write_registry(registry_path, registry):
        print(f"Written registry.json with {len(unique_skills)} skills")
    else:
        print(f"Failed to write registry.json!")
        return
    print()

    # Build category indexes (canonical categories only)
    print("Building category indexes...")
    build_category_indexes(unique_skills, categories_dir)
    print()

    # Stats
    print("=" * 60)
    print("CATEGORY DISTRIBUTION")
    print("=" * 60)
    cat_counts = defaultdict(int)
    for s in unique_skills:
        cat_counts[s.get("category", "other")] += 1

    for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
        pct = count / len(unique_skills) * 100 if unique_skills else 0
        bar = "█" * int(pct / 2)
        print(f"  {cat:15} {count:6} ({pct:5.1f}%) {bar}")

    print()
    print("=" * 60)
    print("DONE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
