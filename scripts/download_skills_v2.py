#!/usr/bin/env python3
"""
Smart async skill downloader for Claude Code Skills Registry.
Analyzes repo structure first, then downloads SKILL.md files efficiently.
"""

import asyncio
import aiohttp
import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, List, Set
import time
from collections import defaultdict
import re

# Configuration
MAX_CONCURRENT = 50
TIMEOUT = 20
RETRY_ATTEMPTS = 2

GITHUB_RAW_BASE = "https://raw.githubusercontent.com"
GITHUB_API_BASE = "https://api.github.com"

# Stats
stats = {
    "total": 0,
    "downloaded": 0,
    "skipped": 0,
    "failed": 0,
    "already_exists": 0,
}


async def try_fetch_url(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore,
) -> Optional[str]:
    """Try to fetch content from a URL."""
    async with semaphore:
        for attempt in range(RETRY_ATTEMPTS):
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
                    if resp.status == 200:
                        return await resp.text()
                    elif resp.status == 404:
                        return None
            except Exception:
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(0.5)
                continue
    return None


async def find_skill_md_in_repo(
    session: aiohttp.ClientSession,
    repo: str,
    skill_name: str,
    semaphore: asyncio.Semaphore,
) -> Optional[str]:
    """Try multiple URL patterns to find SKILL.md."""

    # URL patterns to try, ordered by likelihood
    patterns = [
        # Standard .claude/skills/{name}/SKILL.md pattern
        f"{GITHUB_RAW_BASE}/{repo}/main/.claude/skills/{skill_name}/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/master/.claude/skills/{skill_name}/SKILL.md",

        # Direct in .claude directory
        f"{GITHUB_RAW_BASE}/{repo}/main/.claude/{skill_name}/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/master/.claude/{skill_name}/SKILL.md",

        # Skills directory at root
        f"{GITHUB_RAW_BASE}/{repo}/main/skills/{skill_name}/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/master/skills/{skill_name}/SKILL.md",

        # Direct skill name directory
        f"{GITHUB_RAW_BASE}/{repo}/main/{skill_name}/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/master/{skill_name}/SKILL.md",

        # Root SKILL.md (for single-skill repos)
        f"{GITHUB_RAW_BASE}/{repo}/main/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/master/SKILL.md",
    ]

    for url in patterns:
        content = await try_fetch_url(session, url, semaphore)
        if content and "---" in content:  # Basic validation - SKILL.md should have frontmatter
            return content

    return None


async def download_skill(
    session: aiohttp.ClientSession,
    skill: dict,
    output_dir: Path,
    semaphore: asyncio.Semaphore,
    downloaded_set: Set[str],
) -> bool:
    """Download a single skill."""
    name = skill["name"]
    category = skill.get("category", "uncategorized")
    repo = skill.get("repo", skill.get("install", ""))

    # Create unique key to avoid duplicates
    skill_key = f"{category}/{name}"
    if skill_key in downloaded_set:
        return False

    skill_dir = output_dir / category / name
    skill_file = skill_dir / "SKILL.md"

    # Skip if already exists
    if skill_file.exists():
        downloaded_set.add(skill_key)
        stats["already_exists"] += 1
        return False

    if not repo:
        stats["failed"] += 1
        return False

    # Try to fetch SKILL.md
    content = await find_skill_md_in_repo(session, repo, name, semaphore)

    if content:
        skill_dir.mkdir(parents=True, exist_ok=True)

        # Write SKILL.md
        skill_file.write_text(content, encoding="utf-8")

        # Write metadata.json
        metadata = {
            "name": name,
            "description": skill.get("description", ""),
            "repo": repo,
            "category": category,
            "tags": skill.get("tags", []),
            "stars": skill.get("stars", 0),
            "source": skill.get("source", ""),
        }
        (skill_dir / "metadata.json").write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        downloaded_set.add(skill_key)
        stats["downloaded"] += 1
        return True
    else:
        stats["failed"] += 1
        return False


async def main():
    # Load registry
    registry_path = Path(__file__).parent.parent / "registry.json"
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    skills = registry.get("skills", [])
    stats["total"] = len(skills)

    print(f"📦 Total skills in registry: {len(skills)}")

    # Output directory
    output_dir = Path(__file__).parent.parent / "skills"
    output_dir.mkdir(exist_ok=True)

    # Check existing
    existing = sum(1 for _ in output_dir.rglob("SKILL.md"))
    print(f"📁 Already downloaded: {existing}")
    print(f"⬇️  To download: ~{len(skills) - existing}")
    print()

    # Track downloaded skills to avoid duplicates
    downloaded_set: Set[str] = set()

    # Pre-populate with existing skills
    for skill_md in output_dir.rglob("SKILL.md"):
        rel_path = skill_md.relative_to(output_dir)
        if len(rel_path.parts) >= 2:
            category = rel_path.parts[0]
            name = rel_path.parts[1]
            downloaded_set.add(f"{category}/{name}")

    # Create semaphore for rate limiting
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    # Create aiohttp session with custom headers
    headers = {
        "User-Agent": "Claude-Skills-Downloader/1.0",
        "Accept": "text/plain,application/json",
    }
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT * 2, limit_per_host=20)

    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        # Process in batches
        batch_size = 200
        start_time = time.time()

        for i in range(0, len(skills), batch_size):
            batch = skills[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(skills) + batch_size - 1) // batch_size

            print(f"🔄 Batch {batch_num}/{total_batches} ({len(batch)} skills)...", end=" ", flush=True)

            # Create tasks for this batch
            tasks = [
                download_skill(session, skill, output_dir, semaphore, downloaded_set)
                for skill in batch
            ]

            await asyncio.gather(*tasks, return_exceptions=True)

            elapsed = time.time() - start_time
            processed = stats["downloaded"] + stats["already_exists"] + stats["failed"]
            rate = processed / elapsed if elapsed > 0 else 0

            print(f"✅ {stats['downloaded']} | ⏭️ {stats['already_exists']} | ❌ {stats['failed']} | ⚡ {rate:.0f}/s")

            # Small delay between batches to avoid rate limiting
            await asyncio.sleep(0.2)

    # Final stats
    elapsed = time.time() - start_time
    print()
    print("=" * 50)
    print(f"✨ Download complete!")
    print(f"   Total in registry: {stats['total']}")
    print(f"   Downloaded: {stats['downloaded']}")
    print(f"   Already existed: {stats['already_exists']}")
    print(f"   Failed/Not found: {stats['failed']}")
    print(f"   Time: {elapsed:.1f}s")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
