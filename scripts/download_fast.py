#!/usr/bin/env python3
"""
Ultra-fast skill downloader using multiple independent processes.
Each process handles a slice of repos with high concurrency.
"""

import asyncio
import aiohttp
import json
import os
import sys
from pathlib import Path
from typing import Optional, List, Tuple
from collections import defaultdict
import time
import subprocess

# Configuration
NUM_WORKERS = 16
CONCURRENT_REQUESTS = 200
TIMEOUT = 10
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"


async def fetch_with_fallback(
    session: aiohttp.ClientSession,
    repo: str,
    skill_name: str,
    semaphore: asyncio.Semaphore,
) -> Optional[str]:
    """Try to fetch SKILL.md with multiple URL patterns."""

    # Quick patterns - try most common first
    patterns = [
        f"{GITHUB_RAW_BASE}/{repo}/main/.claude/skills/{skill_name}/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/main/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/master/.claude/skills/{skill_name}/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/master/SKILL.md",
        f"{GITHUB_RAW_BASE}/{repo}/main/.claude/{skill_name}/SKILL.md",
    ]

    async with semaphore:
        for url in patterns:
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
                    if resp.status == 200:
                        content = await resp.text()
                        # Validate it's a proper SKILL.md
                        if content.startswith("---") or "description:" in content[:500]:
                            return content
            except:
                continue
    return None


async def process_skills(
    skills: List[dict],
    output_dir: Path,
    worker_id: int,
) -> Tuple[int, int]:
    """Process a list of skills asynchronously."""

    success = 0
    failed = 0
    semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

    connector = aiohttp.TCPConnector(limit=CONCURRENT_REQUESTS, limit_per_host=50)
    async with aiohttp.ClientSession(connector=connector) as session:

        async def download_one(skill: dict) -> bool:
            nonlocal success, failed

            name = skill["name"]
            category = skill.get("category", "uncategorized")
            repo = skill.get("repo", skill.get("install", ""))

            if not repo:
                failed += 1
                return False

            skill_dir = output_dir / category / name
            skill_file = skill_dir / "SKILL.md"

            if skill_file.exists():
                return True  # Skip already downloaded

            content = await fetch_with_fallback(session, repo, name, semaphore)

            if content:
                skill_dir.mkdir(parents=True, exist_ok=True)
                skill_file.write_text(content, encoding="utf-8")

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
                success += 1
                return True
            else:
                failed += 1
                return False

        # Process in batches
        batch_size = 500
        total = len(skills)

        for i in range(0, total, batch_size):
            batch = skills[i:i + batch_size]
            tasks = [download_one(s) for s in batch]
            await asyncio.gather(*tasks, return_exceptions=True)

            progress = min(i + batch_size, total)
            print(f"[W{worker_id}] {progress}/{total} | ✅ {success} | ❌ {failed}", flush=True)

    return success, failed


def worker_main(worker_id: int, total_workers: int):
    """Main function for each worker process."""

    registry_path = Path(__file__).parent.parent / "registry.json"
    output_dir = Path(__file__).parent.parent / "skills"

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    all_skills = registry.get("skills", [])

    # Get existing skills to skip
    existing = set()
    for skill_md in output_dir.rglob("SKILL.md"):
        rel_path = skill_md.relative_to(output_dir)
        if len(rel_path.parts) >= 2:
            existing.add(f"{rel_path.parts[0]}/{rel_path.parts[1]}")

    # Filter to pending skills only
    pending_skills = [
        s for s in all_skills
        if f"{s.get('category', 'uncategorized')}/{s['name']}" not in existing
    ]

    # Slice for this worker
    chunk_size = len(pending_skills) // total_workers + 1
    start_idx = worker_id * chunk_size
    end_idx = min(start_idx + chunk_size, len(pending_skills))
    my_skills = pending_skills[start_idx:end_idx]

    if not my_skills:
        print(f"[W{worker_id}] No skills to process", flush=True)
        return

    print(f"[W{worker_id}] Processing {len(my_skills)} skills (index {start_idx}-{end_idx})", flush=True)

    success, failed = asyncio.run(process_skills(my_skills, output_dir, worker_id))
    print(f"[W{worker_id}] Done: ✅ {success} | ❌ {failed}", flush=True)


def main():
    if len(sys.argv) > 1:
        # Worker mode
        worker_id = int(sys.argv[1])
        total_workers = int(sys.argv[2])
        worker_main(worker_id, total_workers)
        return

    # Master mode - spawn workers
    registry_path = Path(__file__).parent.parent / "registry.json"
    output_dir = Path(__file__).parent.parent / "skills"

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    total_skills = len(registry.get("skills", []))
    existing = sum(1 for _ in output_dir.rglob("SKILL.md"))

    print(f"📦 Total skills: {total_skills}")
    print(f"📁 Already downloaded: {existing}")
    print(f"⬇️  Pending: ~{total_skills - existing}")
    print(f"🚀 Spawning {NUM_WORKERS} worker processes...")
    print()

    start_time = time.time()

    # Spawn worker processes
    script_path = Path(__file__)
    processes = []

    for i in range(NUM_WORKERS):
        p = subprocess.Popen(
            [sys.executable, str(script_path), str(i), str(NUM_WORKERS)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        processes.append(p)

    # Monitor progress
    try:
        while any(p.poll() is None for p in processes):
            # Print output from all processes
            for p in processes:
                if p.stdout:
                    line = p.stdout.readline()
                    if line:
                        print(line.rstrip())

            time.sleep(0.1)

        # Get remaining output
        for p in processes:
            if p.stdout:
                for line in p.stdout:
                    print(line.rstrip())

    except KeyboardInterrupt:
        print("\n⚠️ Interrupting workers...")
        for p in processes:
            p.terminate()

    elapsed = time.time() - start_time
    final_count = sum(1 for _ in output_dir.rglob("SKILL.md"))
    downloaded = final_count - existing

    print()
    print("=" * 50)
    print(f"✨ Download complete!")
    print(f"   Total downloaded: {final_count}")
    print(f"   New in this run: {downloaded}")
    print(f"   Time: {elapsed:.1f}s")
    print(f"   Rate: {downloaded / elapsed:.1f} skills/s")
    print("=" * 50)


if __name__ == "__main__":
    main()
