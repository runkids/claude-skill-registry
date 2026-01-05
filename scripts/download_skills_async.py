#!/usr/bin/env python3
"""
Async skill downloader for Claude Code Skills Registry.
Downloads SKILL.md files from GitHub repos with high concurrency.
"""

import asyncio
import aiohttp
import json
import os
import sys
from pathlib import Path
from typing import Optional
import time
from collections import defaultdict

# Configuration
MAX_CONCURRENT = 100  # Number of concurrent downloads
TIMEOUT = 30  # Request timeout in seconds
RETRY_ATTEMPTS = 3
RATE_LIMIT_DELAY = 0.1  # Delay between batches

# GitHub raw content base URL
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"

# Stats
stats = {
    "total": 0,
    "downloaded": 0,
    "skipped": 0,
    "failed": 0,
    "already_exists": 0,
}


async def fetch_skill_md(
    session: aiohttp.ClientSession,
    skill: dict,
    semaphore: asyncio.Semaphore,
) -> tuple[str, Optional[str], Optional[str]]:
    """Fetch SKILL.md content from GitHub."""
    repo = skill.get("repo", skill.get("install", ""))
    name = skill["name"]
    path = skill.get("path", "")

    if not repo:
        return name, None, "No repo specified"

    # Build the URL for SKILL.md
    if path:
        url = f"{GITHUB_RAW_BASE}/{repo}/main/{path}/SKILL.md"
    else:
        url = f"{GITHUB_RAW_BASE}/{repo}/main/.claude/skills/{name}/SKILL.md"

    # Alternative URLs to try
    alt_urls = [
        f"{GITHUB_RAW_BASE}/{repo}/main/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/master/.claude/skills/{name}/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/master/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/main/.claude/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/master/.claude/SKILL.md",
    ]

    async with semaphore:
        for attempt in range(RETRY_ATTEMPTS):
            try:
                # Try primary URL first
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
                    if resp.status == 200:
                        content = await resp.text()
                        return name, content, None

                # Try alternative URLs
                for alt_url in alt_urls:
                    try:
                        async with session.get(alt_url, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
                            if resp.status == 200:
                                content = await resp.text()
                                return name, content, None
                    except:
                        continue

                return name, None, f"Not found (tried {len(alt_urls) + 1} URLs)"

            except asyncio.TimeoutError:
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(1)
                    continue
                return name, None, "Timeout"
            except Exception as e:
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(1)
                    continue
                return name, None, str(e)

    return name, None, "Max retries exceeded"


async def download_batch(
    session: aiohttp.ClientSession,
    skills: list[dict],
    output_dir: Path,
    semaphore: asyncio.Semaphore,
) -> None:
    """Download a batch of skills concurrently."""
    tasks = []

    for skill in skills:
        name = skill["name"]
        category = skill.get("category", "uncategorized")
        skill_dir = output_dir / category / name
        skill_file = skill_dir / "SKILL.md"

        # Skip if already exists
        if skill_file.exists():
            stats["already_exists"] += 1
            stats["skipped"] += 1
            continue

        tasks.append(fetch_skill_md(session, skill, semaphore))

    if not tasks:
        return

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for result in results:
        if isinstance(result, Exception):
            stats["failed"] += 1
            continue

        name, content, error = result

        if content:
            # Find the skill to get category
            skill = next((s for s in skills if s["name"] == name), None)
            if skill:
                category = skill.get("category", "uncategorized")
                skill_dir = output_dir / category / name
                skill_dir.mkdir(parents=True, exist_ok=True)

                # Write SKILL.md
                (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")

                # Write metadata.json
                metadata = {
                    "name": name,
                    "description": skill.get("description", ""),
                    "repo": skill.get("repo", skill.get("install", "")),
                    "category": category,
                    "tags": skill.get("tags", []),
                    "stars": skill.get("stars", 0),
                    "source": skill.get("source", ""),
                }
                (skill_dir / "metadata.json").write_text(
                    json.dumps(metadata, indent=2, ensure_ascii=False),
                    encoding="utf-8"
                )

                stats["downloaded"] += 1
        else:
            stats["failed"] += 1


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
    print(f"⬇️  To download: {len(skills) - existing}")
    print()

    # Create semaphore for rate limiting
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)

    # Create aiohttp session
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT, limit_per_host=50)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Process in batches
        batch_size = 500
        start_time = time.time()

        for i in range(0, len(skills), batch_size):
            batch = skills[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(skills) + batch_size - 1) // batch_size

            print(f"🔄 Processing batch {batch_num}/{total_batches} ({len(batch)} skills)...")

            await download_batch(session, batch, output_dir, semaphore)

            elapsed = time.time() - start_time
            processed = stats["downloaded"] + stats["skipped"] + stats["failed"]
            rate = processed / elapsed if elapsed > 0 else 0

            print(f"   ✅ Downloaded: {stats['downloaded']} | ⏭️  Skipped: {stats['skipped']} | ❌ Failed: {stats['failed']} | ⚡ {rate:.1f}/s")

            # Small delay between batches
            await asyncio.sleep(RATE_LIMIT_DELAY)

    # Final stats
    elapsed = time.time() - start_time
    print()
    print("=" * 50)
    print(f"✨ Download complete!")
    print(f"   Total: {stats['total']}")
    print(f"   Downloaded: {stats['downloaded']}")
    print(f"   Already existed: {stats['already_exists']}")
    print(f"   Failed: {stats['failed']}")
    print(f"   Time: {elapsed:.1f}s")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
