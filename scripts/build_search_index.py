#!/usr/bin/env python3
"""
Build Search Index - Generate lightweight search index for fast client-side search

This script generates multiple index files from VERIFIED downloaded skills:
1. search-index.json - Minimal index for CLI/Web search (~1MB gzip)
2. categories/*.json - Category-based indexes for filtering
3. featured.json - Top skills for homepage display

Key improvement: Only indexes skills that have been actually downloaded,
using the original GitHub paths stored in metadata.json.
"""

import json
import gzip
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
import argparse
import logging
import re
import yaml

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Category short codes mapping
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

# Reverse mapping
CODE_TO_CATEGORY = {v: k for k, v in CATEGORY_CODES.items()}


def truncate_text(text: Any, max_length: int) -> str:
    """Truncate text to max length with ellipsis."""
    if not text:
        return ""
    # Handle list-type descriptions
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


def extract_description_from_skill(skill_content: str) -> str:
    """Extract description from SKILL.md content."""
    # Try YAML frontmatter first
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

    # Try first meaningful paragraph
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
            # Clean markdown
            line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
            line = re.sub(r'[*_`]', '', line)
            return line

    return ""


def scan_downloaded_skills(skills_dir: Path) -> List[Dict]:
    """Scan downloaded skills directory and build skill list."""
    skills = []

    # Look for SKILL.md files in skills/data/*/
    data_dir = skills_dir / "data"
    if not data_dir.exists():
        logger.warning(f"Skills data directory not found: {data_dir}")
        return skills

    for skill_dir in data_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_md = skill_dir / "SKILL.md"
        metadata_file = skill_dir / "metadata.json"

        if not skill_md.exists():
            continue

        name = skill_dir.name

        # Read metadata
        metadata = {}
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
            except Exception:
                pass

        # Read SKILL.md for description if not in metadata
        description = metadata.get("description", "")
        if not description:
            try:
                content = skill_md.read_text(encoding='utf-8')
                description = extract_description_from_skill(content)
            except Exception:
                pass

        if not description:
            description = f"Skill: {name}"

        # Get install path - use github_path if available
        repo = metadata.get("repo", "")
        github_path = metadata.get("github_path", "")

        if github_path and repo:
            # Use the original GitHub path
            install = f"{repo}/{github_path}"
        elif repo:
            install = repo
        else:
            # Fallback - won't be installable but at least indexed
            install = f"unknown/{name}"

        skill_entry = {
            "name": name,
            "description": description,
            "repo": repo,
            "path": github_path,  # Original GitHub path
            "category": metadata.get("category", "other"),
            "tags": metadata.get("tags", []),
            "stars": metadata.get("stars", 0),
            "source": metadata.get("source", "downloaded"),
            "install": install,
        }

        skills.append(skill_entry)

    return skills


def build_search_index(
    skills: List[Dict],
    output_dir: Path,
    source_name: str = "downloaded skills"
) -> Dict[str, Any]:
    """Build the lightweight search index from skill list."""
    logger.info(f"Building index from {len(skills)} {source_name}...")

    # Build minimal search index
    search_index = {
        "v": datetime.utcnow().strftime("%Y-%m-%d"),
        "t": len(skills),
        "s": []
    }

    # Category indexes
    categories: Dict[str, List[Dict]] = {}

    # Featured skills (top 100 by stars)
    featured_skills = []

    for skill in skills:
        name = skill.get('name', '')
        description = skill.get('description', '')
        category = skill.get('category', 'other')
        tags = skill.get('tags', [])
        stars = skill.get('stars', 0)
        repo = skill.get('repo', '')
        install = skill.get('install', repo)

        # Minimal record for search index
        mini_record = {
            "n": name,
            "d": truncate_text(description, 80),
            "c": get_category_code(category),
            "g": tags[:5] if tags else [],  # Max 5 tags
            "r": stars,
            "i": install
        }
        search_index["s"].append(mini_record)

        # Full record for category index
        full_record = {
            "name": name,
            "description": truncate_text(description, 200),
            "repo": repo,
            "path": skill.get('path', ''),
            "category": category,
            "tags": tags[:10] if tags else [],
            "stars": stars,
            "install": install,
            "source": skill.get('source', '')
        }

        # Add to category
        if category not in categories:
            categories[category] = []
        categories[category].append(full_record)

        # Track for featured
        if stars > 0:
            featured_skills.append(full_record)

    # Sort search index by stars (descending)
    search_index["s"].sort(key=lambda x: x.get("r", 0), reverse=True)

    # Sort featured by stars and take top 100
    featured_skills.sort(key=lambda x: x.get("stars", 0), reverse=True)
    featured_skills = featured_skills[:100]

    # Create output directory
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

    # Write category indexes
    category_index = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "categories": []
    }

    for category, cat_skills in sorted(categories.items()):
        # Sort by stars
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
            "name": category,
            "code": get_category_code(category),
            "count": len(cat_skills)
        })

        logger.info(f"  categories/{category}.json: {len(cat_skills)} skills")

    # Write category index
    category_index_path = categories_dir / "index.json"
    with open(category_index_path, 'w', encoding='utf-8') as f:
        json.dump(category_index, f, ensure_ascii=False, indent=2)

    # Write featured skills
    featured_data = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "count": len(featured_skills),
        "skills": featured_skills
    }
    featured_path = output_dir / "featured.json"
    with open(featured_path, 'w', encoding='utf-8') as f:
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
    stats_path = output_dir / "stats.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    logger.info(f"\nIndex build complete!")
    logger.info(f"  Total skills: {len(skills)}")
    logger.info(f"  Categories: {len(categories)}")
    logger.info(f"  Output: {output_dir}")

    return stats


def load_from_registry(registry_path: Path) -> List[Dict]:
    """Load skills from registry.json (legacy mode)."""
    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    skills = registry.get('skills', [])

    # Add install path
    for skill in skills:
        repo = skill.get('repo', '')
        path = skill.get('path', '')
        if path:
            skill['install'] = f"{repo}/{path}"
        else:
            skill['install'] = repo

    return skills


def main():
    parser = argparse.ArgumentParser(
        description='Build search index for skill registry (from downloaded skills or registry.json)'
    )
    parser.add_argument(
        '--skills-dir', '-s',
        default='skills',
        help='Path to downloaded skills directory (preferred)'
    )
    parser.add_argument(
        '--registry', '-r',
        default='registry.json',
        help='Path to registry.json (fallback)'
    )
    parser.add_argument(
        '--output', '-o',
        default='docs',
        help='Output directory for index files'
    )
    parser.add_argument(
        '--use-registry',
        action='store_true',
        help='Force using registry.json instead of skills directory'
    )

    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    registry_path = Path(args.registry)
    output_dir = Path(args.output)

    # Prefer scanning downloaded skills unless --use-registry is specified
    if not args.use_registry and (skills_dir / "data").exists():
        logger.info(f"Scanning downloaded skills from {skills_dir}")
        skills = scan_downloaded_skills(skills_dir)
        source_name = "verified downloaded skills"
    elif registry_path.exists():
        logger.info(f"Loading from registry: {registry_path}")
        skills = load_from_registry(registry_path)
        source_name = "registry entries"
    else:
        logger.error("No skills source found!")
        logger.error(f"  Skills directory: {skills_dir}/data (not found)")
        logger.error(f"  Registry: {registry_path} (not found)")
        exit(1)

    if not skills:
        logger.error("No skills found!")
        exit(1)

    build_search_index(skills, output_dir, source_name)


if __name__ == '__main__':
    main()
