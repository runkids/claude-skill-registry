#!/usr/bin/env python3
"""
Build Search Index - Generate lightweight search index for fast client-side search

This script generates multiple index files:
1. search-index.json - Minimal index for CLI/Web search (~1MB gzip)
2. categories/*.json - Category-based indexes for filtering
3. featured.json - Top skills for homepage display
"""

import json
import gzip
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List
import argparse
import logging

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
    return CATEGORY_CODES.get(category.lower(), "oth")


def build_search_index(registry_path: Path, output_dir: Path) -> Dict[str, Any]:
    """Build the lightweight search index."""
    logger.info(f"Loading registry from {registry_path}")

    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    skills = registry.get('skills', [])
    logger.info(f"Processing {len(skills)} skills...")

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
        path = skill.get('path', '')

        # Build install path
        if path:
            install = f"{repo}/{path}"
        else:
            install = repo

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
            "path": path,
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


def main():
    parser = argparse.ArgumentParser(description='Build search index for skill registry')
    parser.add_argument(
        '--registry', '-r',
        default='registry.json',
        help='Path to registry.json'
    )
    parser.add_argument(
        '--output', '-o',
        default='docs',
        help='Output directory for index files'
    )

    args = parser.parse_args()

    registry_path = Path(args.registry)
    output_dir = Path(args.output)

    if not registry_path.exists():
        logger.error(f"Registry not found: {registry_path}")
        exit(1)

    build_search_index(registry_path, output_dir)


if __name__ == '__main__':
    main()
