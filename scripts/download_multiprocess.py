#!/usr/bin/env python3
"""
High-performance multi-process skill downloader.
Uses multiprocessing + asyncio for maximum throughput.
Groups skills by repo to minimize redundant requests.
"""

import asyncio
import aiohttp
import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from multiprocessing import Pool, Manager, cpu_count
from collections import defaultdict
import time
import signal

# Configuration
NUM_PROCESSES = cpu_count() * 2  # Use more processes than cores for I/O bound tasks
CONCURRENT_PER_PROCESS = 100
TIMEOUT = 15
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"

# Shared stats (using Manager for cross-process sharing)
manager = None
stats = None


def init_worker():
    """Initialize worker process - ignore SIGINT for clean shutdown."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)


async def fetch_url(session: aiohttp.ClientSession, url: str) -> Optional[str]:
    """Fetch a URL and return content or None."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
            if resp.status == 200:
                return await resp.text()
    except:
        pass
    return None


async def download_repo_skills(
    repo: str,
    skills: List[dict],
    output_dir: Path,
    downloaded_names: set,
) -> Tuple[int, int]:
    """Download all skills from a single repo."""
    success = 0
    failed = 0

    # First, try to detect repo structure (main vs master branch)
    connector = aiohttp.TCPConnector(limit=CONCURRENT_PER_PROCESS)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Detect default branch
        branch = "main"
        test_url = f"{GITHUB_RAW_BASE}/{repo}/main/README.md"
        content = await fetch_url(session, test_url)
        if content is None:
            branch = "master"

        # Try to get repo's skill directory structure
        skills_base_urls = [
            f"{GITHUB_RAW_BASE}/{repo}/{branch}/.claude/skills",
            f"{GITHUB_RAW_BASE}/{repo}/{branch}/skills",
            f"{GITHUB_RAW_BASE}/{repo}/{branch}/.claude",
            f"{GITHUB_RAW_BASE}/{repo}/{branch}",
        ]

        for skill in skills:
            name = skill["name"]
            category = skill.get("category", "uncategorized")
            skill_key = f"{category}/{name}"

            if skill_key in downloaded_names:
                continue

            skill_dir = output_dir / category / name
            skill_file = skill_dir / "SKILL.md"

            if skill_file.exists():
                downloaded_names.add(skill_key)
                continue

            # Try different URL patterns
            urls_to_try = [
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/.claude/skills/{name}/SKILL.md",
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/skills/{name}/SKILL.md",
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/.claude/{name}/SKILL.md",
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/{name}/SKILL.md",
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/SKILL.md",
            ]

            content = None
            for url in urls_to_try:
                content = await fetch_url(session, url)
                if content and "---" in content[:500]:  # Valid SKILL.md has frontmatter
                    break
                content = None

            if content:
                skill_dir.mkdir(parents=True, exist_ok=True)
                skill_file.write_text(content, encoding="utf-8")

                # Write metadata
                metadata = {
                    "name": name,
                    "description": skill.get("description", ""),
                    "repo": repo,
                    "category": category,
                    "tags": skill.get("tags", []),
                    "stars": skill.get("stars", 0),
                }
                (skill_dir / "metadata.json").write_text(
                    json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
                )

                downloaded_names.add(skill_key)
                success += 1
            else:
                failed += 1

    return success, failed


def process_repo_batch(args) -> Tuple[int, int, int]:
    """Process a batch of repos in a single process."""
    repo_skills_batch, output_dir_str, existing_skills = args
    output_dir = Path(output_dir_str)
    downloaded_names = set(existing_skills)

    total_success = 0
    total_failed = 0
    repos_processed = 0

    async def run_batch():
        nonlocal total_success, total_failed, repos_processed
        for repo, skills in repo_skills_batch:
            success, failed = await download_repo_skills(repo, skills, output_dir, downloaded_names)
            total_success += success
            total_failed += failed
            repos_processed += 1

    asyncio.run(run_batch())
    return total_success, total_failed, repos_processed


def main():
    # Load registry
    registry_path = Path(__file__).parent.parent / "registry.json"
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    skills = registry.get("skills", [])
    print(f"📦 Total skills in registry: {len(skills)}")

    # Output directory
    output_dir = Path(__file__).parent.parent / "skills"
    output_dir.mkdir(exist_ok=True)

    # Get existing skills
    existing_skills = set()
    for skill_md in output_dir.rglob("SKILL.md"):
        rel_path = skill_md.relative_to(output_dir)
        if len(rel_path.parts) >= 2:
            existing_skills.add(f"{rel_path.parts[0]}/{rel_path.parts[1]}")

    print(f"📁 Already downloaded: {len(existing_skills)}")

    # Group skills by repo
    repo_skills: Dict[str, List[dict]] = defaultdict(list)
    for skill in skills:
        repo = skill.get("repo", skill.get("install", ""))
        if repo:
            repo_skills[repo].append(skill)

    print(f"🔗 Unique repos: {len(repo_skills)}")

    # Convert to list and sort by number of skills (process repos with more skills first)
    repo_list = sorted(repo_skills.items(), key=lambda x: -len(x[1]))

    # Filter out repos where all skills are already downloaded
    pending_repos = []
    for repo, skills_list in repo_list:
        pending_skills = [
            s for s in skills_list
            if f"{s.get('category', 'uncategorized')}/{s['name']}" not in existing_skills
        ]
        if pending_skills:
            pending_repos.append((repo, pending_skills))

    total_pending = sum(len(skills) for _, skills in pending_repos)
    print(f"⬇️  Pending skills: {total_pending} across {len(pending_repos)} repos")
    print(f"🚀 Using {NUM_PROCESSES} processes")
    print()

    if not pending_repos:
        print("✨ All skills already downloaded!")
        return

    # Split repos into batches for each process
    batch_size = max(1, len(pending_repos) // NUM_PROCESSES)
    batches = []
    for i in range(0, len(pending_repos), batch_size):
        batch = pending_repos[i:i + batch_size]
        batches.append((batch, str(output_dir), list(existing_skills)))

    start_time = time.time()

    # Process with multiprocessing pool
    try:
        with Pool(NUM_PROCESSES, initializer=init_worker) as pool:
            results = []
            for i, result in enumerate(pool.imap_unordered(process_repo_batch, batches)):
                success, failed, repos = result
                elapsed = time.time() - start_time
                results.append((success, failed))
                total_success = sum(r[0] for r in results)
                total_failed = sum(r[1] for r in results)
                rate = (total_success + total_failed) / elapsed if elapsed > 0 else 0
                print(f"🔄 Batch {i+1}/{len(batches)}: ✅ {total_success} | ❌ {total_failed} | ⚡ {rate:.0f}/s")

    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")

    # Final stats
    elapsed = time.time() - start_time
    final_count = sum(1 for _ in output_dir.rglob("SKILL.md"))
    print()
    print("=" * 50)
    print(f"✨ Download complete!")
    print(f"   Total downloaded: {final_count}")
    print(f"   Time: {elapsed:.1f}s")
    print(f"   Rate: {(final_count - len(existing_skills)) / elapsed:.1f} skills/s")
    print("=" * 50)


if __name__ == "__main__":
    main()
