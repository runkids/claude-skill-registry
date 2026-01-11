#!/usr/bin/env python3
"""
Rebuild registry.json from downloaded skills.

Scans all skills/*/SKILL.md files and rebuilds the registry index.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import yaml


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
        return yaml.safe_load(frontmatter) or {}
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


def scan_skills(skills_dir: Path) -> list:
    """Scan all skills and build index."""
    skills = []

    for skill_md in skills_dir.rglob("SKILL.md"):
        rel_path = skill_md.relative_to(skills_dir)
        parts = rel_path.parts

        if len(parts) < 2:
            continue

        category = parts[0]
        name = parts[1]

        # Skip if category is 'data' (flat structure)
        if category == "data":
            # In data/, structure is data/{name}/SKILL.md
            pass

        # Read metadata.json if exists
        metadata_path = skill_md.parent / "metadata.json"
        metadata = {}
        if metadata_path.exists():
            try:
                with open(metadata_path) as f:
                    metadata = json.load(f)
            except Exception:
                pass

        # Read SKILL.md for description
        try:
            content = skill_md.read_text(encoding="utf-8")
            description = metadata.get("description") or extract_description(content)
        except Exception:
            description = ""

        skill_entry = {
            "name": name,
            "description": description[:200] if description else f"Skill: {name}",
            "repo": metadata.get("repo", ""),
            "path": str(rel_path.parent),
            "category": metadata.get("category", category),
            "tags": metadata.get("tags", []),
            "stars": metadata.get("stars", 0),
            "source": metadata.get("source", "local"),
        }

        skills.append(skill_entry)

    return skills


def build_category_indexes(skills: list, output_dir: Path):
    """Build category-based indexes."""
    categories = defaultdict(list)

    for skill in skills:
        cat = skill.get("category", "other")
        categories[cat].append(skill)

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

    # Remove duplicates by name
    seen = set()
    unique_skills = []
    for s in skills:
        if s["name"] not in seen:
            seen.add(s["name"])
            unique_skills.append(s)

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
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    print(f"Written registry.json with {len(unique_skills)} skills")
    print()

    # Build category indexes
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
        pct = count / len(unique_skills) * 100
        bar = "█" * int(pct / 2)
        print(f"  {cat:15} {count:6} ({pct:5.1f}%) {bar}")

    print()
    print("=" * 60)
    print("DONE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
