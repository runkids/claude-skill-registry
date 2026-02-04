#!/usr/bin/env python3
"""
Build Search Index v2.0 - Generate lightweight search index

Output files:
- search-index.json - Minimal index (~1-2MB gzip)
- categories/*.json - Canonical category indexes (12 files)
- featured.json - Top 100 skills by stars
"""

import json
import gzip
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List
import argparse
import logging
import re
import yaml

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Category short codes
CATEGORY_CODES = {
    "development": "dev",
    "devops": "ops",
    "security": "sec",
    "documents": "doc",
    "design": "des",
    "testing": "tst",
    "product": "prd",
    "marketing": "mkt",
    "productivity": "pro",
    "data": "dat",
    "official": "off",
    "other": "oth",
}

CODE_TO_NAME = {
    "dev": "Development",
    "ops": "DevOps",
    "sec": "Security",
    "doc": "Documents",
    "des": "Design",
    "tst": "Testing",
    "prd": "Product",
    "mkt": "Marketing",
    "pro": "Productivity",
    "dat": "Data",
    "off": "Official",
    "oth": "Other",
}


def truncate_text(text: Any, max_length: int) -> str:
    """Truncate text to max length with ellipsis."""
    if not text:
        return ""
    if isinstance(text, list):
        text = " ".join(str(t) for t in text if t)
    text = str(text).strip().replace("\n", " ").replace("\r", "")
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def get_category_code(category: str) -> str:
    """Get short code for category."""
    if not category:
        return "oth"
    return CATEGORY_CODES.get(category.lower(), "oth")


def extract_description(skill_content: str) -> str:
    """Extract description from SKILL.md content."""
    # Try YAML frontmatter
    if skill_content.startswith("---"):
        try:
            end_idx = skill_content.find("---", 3)
            if end_idx > 0:
                frontmatter = skill_content[3:end_idx].strip()
                data = yaml.safe_load(frontmatter)
                if data and data.get("description"):
                    return data["description"]
        except Exception:
            pass

    # Try first paragraph
    lines = skill_content.split("\n")
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
        if line and not line.startswith("```") and len(line) > 20:
            line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
            line = re.sub(r'[*_`]', '', line)
            return line

    return ""


def build_search_index(skills: List[Dict], output_dir: Path, source_name: str = "skills") -> Dict[str, Any]:
    """Build the lightweight search index."""
    logger.info(f"Building index from {len(skills)} {source_name}...")

    # Build minimal search index
    search_index = {
        "v": datetime.utcnow().strftime("%Y-%m-%d"),
        "t": len(skills),
        "s": []
    }

    # Category indexes (canonical category names)
    categories: Dict[str, List[Dict]] = {}
    code_counts: Dict[str, int] = {}

    # Featured skills
    featured_skills = []

    for skill in skills:
        name = skill.get('name', '')
        description = skill.get('description', '')
        category = (skill.get('category') or 'other').lower()
        tags = skill.get('tags', [])
        stars = skill.get('stars', 0)
        repo = skill.get('repo', '')
        path = skill.get('path', '')
        install = skill.get('install') or (f"{repo}/{path}" if repo and path else repo)
        branch = skill.get('branch', 'main')
        code = get_category_code(category)

        # Minimal record
        mini_record = {
            "n": name,
            "d": truncate_text(description, 80),
            "c": code,
            "g": tags[:5] if tags else [],
            "r": stars,
            "i": install,
            "b": branch  # branch for GitHub URL
        }
        search_index["s"].append(mini_record)

        # Full record
        full_record = {
            "name": name,
            "description": truncate_text(description, 200),
            "repo": repo,
            "path": path,
            "branch": branch,
            "category": category,
            "tags": tags[:10] if tags else [],
            "stars": stars,
            "install": install,
            "source": skill.get('source', '')
        }

        # Add to category
        canonical_category = category if category in CATEGORY_CODES else "other"
        if canonical_category not in categories:
            categories[canonical_category] = []
        categories[canonical_category].append(full_record)
        code_counts[code] = code_counts.get(code, 0) + 1

        # Track for featured
        if stars > 0:
            featured_skills.append(full_record)

    # Sort by stars
    search_index["s"].sort(key=lambda x: x.get("r", 0), reverse=True)
    featured_skills.sort(key=lambda x: x.get("stars", 0), reverse=True)
    featured_skills = featured_skills[:100]

    # Create output directories
    output_dir.mkdir(parents=True, exist_ok=True)
    categories_dir = output_dir / "categories"
    categories_dir.mkdir(exist_ok=True)

    # Write search index
    search_index_path = output_dir / "search-index.json"
    with open(search_index_path, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, separators=(',', ':'))

    # Write gzipped version
    search_index_gz_path = output_dir / "search-index.json.gz"
    with gzip.open(search_index_gz_path, 'wt', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, separators=(',', ':'))

    logger.info(f"  search-index.json: {search_index_path.stat().st_size / 1024 / 1024:.2f} MB")
    logger.info(f"  search-index.json.gz: {search_index_gz_path.stat().st_size / 1024 / 1024:.2f} MB")

    # Write category indexes (clean old derived files)
    category_index = {"updated_at": datetime.utcnow().isoformat() + "Z", "categories": []}

    for p in categories_dir.glob("*.json"):
        try:
            p.unlink()
        except OSError:
            pass

    for category in CATEGORY_CODES.keys():
        cat_skills = categories.get(category, [])
        if not cat_skills:
            continue
        cat_skills.sort(key=lambda x: x.get("stars", 0), reverse=True)

        cat_data = {
            "category": category,
            "code": get_category_code(category),
            "count": len(cat_skills),
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "skills": cat_skills
        }

        cat_path = categories_dir / f"{category}.json"
        with open(cat_path, 'w', encoding='utf-8') as f:
            json.dump(cat_data, f, ensure_ascii=False, indent=2)

        category_index["categories"].append({
            "name": CODE_TO_NAME[get_category_code(category)],
            "code": get_category_code(category),
            "count": len(cat_skills)
        })

        logger.info(f"  categories/{category}.json: {len(cat_skills)} skills")

    # Write category index
    with open(categories_dir / "index.json", 'w', encoding='utf-8') as f:
        json.dump(category_index, f, ensure_ascii=False, indent=2)

    # Write featured
    featured_data = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "count": len(featured_skills),
        "skills": featured_skills
    }
    with open(output_dir / "featured.json", 'w', encoding='utf-8') as f:
        json.dump(featured_data, f, ensure_ascii=False, indent=2)

    logger.info(f"  featured.json: {len(featured_skills)} skills")

    # Write stats
    stats = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "total_skills": len(skills),
        "categories": len(categories),
        "featured_count": len(featured_skills),
        "index_size_bytes": search_index_path.stat().st_size,
        "index_size_gzip_bytes": search_index_gz_path.stat().st_size,
    }
    with open(output_dir / "stats.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    logger.info(f"\nIndex build complete!")
    logger.info(f"  Total skills: {len(skills)}")
    logger.info(f"  Categories: {len(categories)}")

    return stats


def load_from_registry(registry_path: Path) -> List[Dict]:
    """Load skills from registry.json."""
    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    skills = registry.get('skills', [])

    return skills


def main():
    parser = argparse.ArgumentParser(description='Build search index for skill registry')
    parser.add_argument('--registry', '-r', default='registry.json', help='Registry.json input')
    parser.add_argument('--output', '-o', default='docs', help='Output directory')

    args = parser.parse_args()

    registry_path = Path(args.registry)
    output_dir = Path(args.output)

    if registry_path.exists():
        logger.info(f"Loading from registry: {registry_path}")
        skills = load_from_registry(registry_path)
        source_name = "registry entries"
    else:
        logger.error("No skills source found!")
        exit(1)

    if not skills:
        logger.error("No skills found!")
        exit(1)

    build_search_index(skills, output_dir, source_name)


if __name__ == '__main__':
    main()
