#!/usr/bin/env python3
"""
Skill Downloader v2 - Download missing SKILL.md files from GitHub.

Storage:
  - Downloaded skills are stored under `skills/data/<dir_name>/SKILL.md`.

Inputs:
  - By default, reads all `sources/*.json` files that contain a top-level `skills` array.
  - Optionally can also include `registry.json` entries via `--include-registry`.

This script intentionally does not try to reorganize the existing `skills/` tree. It
only ensures missing skills are downloaded, and writes/updates `metadata.json` next
to each downloaded SKILL.md with normalized `repo`, `github_path`, `github_branch`,
and canonical `category`.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import re
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import aiohttp

from utils import normalize_name, ensure_unique_dir, build_skill_key

from registry_normalization import (
    canonicalize_category,
    normalize_github_path,
    normalize_repo,
)

# Configuration
MAX_CONCURRENT = 50
TIMEOUT = 15
RETRY_ATTEMPTS = 2
BATCH_SIZE = 200

GITHUB_RAW_BASE = "https://raw.githubusercontent.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_repo_suffix(repo: str) -> str:
    """Get a short suffix from repo: owner-repo."""
    repo = normalize_repo(repo)
    if not repo or "/" not in repo:
        return "unknown"
    owner, repo_name = repo.split("/", 1)
    owner = normalize_name(owner)[:20]
    repo_name = normalize_name(repo_name)[:20]
    return f"{owner}-{repo_name}"


def derive_name(skill: dict) -> str:
    """Best-effort name derivation when sources omit it."""
    name = skill.get("name")
    if name:
        return str(name)
    path = skill.get("path") or skill.get("github_path") or ""
    path = str(path).strip()
    if path:
        # Use directory name of provided path
        path = path.replace("\\", "/")
        if path.endswith("SKILL.md"):
            path = path[: -len("SKILL.md")].rstrip("/")
        if path:
            return path.split("/")[-1]
    repo = normalize_repo(skill.get("repo", "") or "")
    if repo:
        return repo.split("/")[-1]
    return "unknown"


class ExistingSkillIndex:
    """Index existing skills (repo + github_path) across the entire skills tree."""

    def __init__(self, skills_dir: Path):
        self.keys: Set[str] = set()
        self.by_repo: Dict[str, Set[str]] = defaultdict(set)
        self._scan(skills_dir)

    def _scan(self, skills_dir: Path) -> None:
        if not skills_dir.exists():
            return

        scanned = 0
        for metadata_path in skills_dir.rglob("metadata.json"):
            scanned += 1
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            except Exception:
                continue

            repo = normalize_repo(metadata.get("repo", ""))
            if not repo or "/" not in repo:
                continue

            path = normalize_github_path(metadata.get("github_path") or metadata.get("path"))
            key = f"{repo}:{path}"
            self.keys.add(key)
            self.by_repo[repo].add(path)

        logger.info(f"Indexed existing skills: {len(self.keys)} unique repo:path keys (metadata scanned: {scanned})")

    def has(self, repo: str, path: str) -> bool:
        return f"{repo}:{path}" in self.keys

    def add(self, repo: str, path: str) -> None:
        key = f"{repo}:{path}"
        self.keys.add(key)
        self.by_repo.setdefault(repo, set()).add(path)


def get_url_patterns(repo: str, skill_name: str, skill_path: str = "") -> List[str]:
    """Generate URL patterns to try for downloading SKILL.md."""
    patterns: List[str] = []
    branches = ["main", "master"]

    repo = normalize_repo(repo)
    skill_name = normalize_name(skill_name)
    skill_path = str(skill_path or "").strip().lstrip("/")

    if skill_path:
        for branch in branches:
            if skill_path.endswith("SKILL.md"):
                patterns.append(f"{GITHUB_RAW_BASE}/{repo}/{branch}/{skill_path}")
            else:
                patterns.append(f"{GITHUB_RAW_BASE}/{repo}/{branch}/{skill_path}/SKILL.md")

    for branch in branches:
        patterns.extend(
            [
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/.claude/skills/{skill_name}/SKILL.md",
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/.claude/{skill_name}/SKILL.md",
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/.claude/SKILL.md",
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/skills/{skill_name}/SKILL.md",
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/{skill_name}/SKILL.md",
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/SKILL.md",
            ]
        )

    # Remove duplicates while preserving order
    seen: Set[str] = set()
    out: List[str] = []
    for p in patterns:
        if p in seen:
            continue
        seen.add(p)
        out.append(p)
    return out


async def fetch_url(
    session: aiohttp.ClientSession,
    url: str,
    semaphore: asyncio.Semaphore,
) -> Tuple[Optional[str], int]:
    """Fetch URL with status code."""
    async with semaphore:
        for attempt in range(RETRY_ATTEMPTS):
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
                    if resp.status == 200:
                        return await resp.text(), 200
                    if resp.status == 404:
                        return None, 404
                    if resp.status in (403, 429):
                        await asyncio.sleep(2**attempt)
                        continue
                    return None, resp.status
            except Exception:
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(0.5)
        return None, -1


def is_valid_skill_content(content: str) -> bool:
    """Validate that content looks like a SKILL.md file."""
    if not content or len(content) < 50:
        return False
    head = content[:800].lower()
    return content.strip().startswith("---") or "description:" in head or "# " in content[:200] or "skill" in head


def extract_location_from_raw_url(url: str) -> tuple[str, str]:
    """
    Extract (branch, github_path_dir) from a raw.githubusercontent.com URL.

    Returns ("main", "") on failure.
    """
    try:
        url_parts = url.replace(GITHUB_RAW_BASE + "/", "").split("/")
        if len(url_parts) <= 3:
            return "main", ""
        branch = url_parts[2] or "main"
        raw_path = "/".join(url_parts[3:])
        github_path_dir = normalize_github_path(raw_path)
        return branch, github_path_dir
    except Exception:
        return "main", ""


def choose_dir_name(base_name: str, repo: str, output_dir: Path, key: str) -> str:
    """Pick a case-safe directory name under skills/data."""
    base_name = normalize_name(base_name)
    return ensure_unique_dir(output_dir, base_name, key).name


async def download_skill(
    session: aiohttp.ClientSession,
    skill: dict,
    output_dir: Path,
    semaphore: asyncio.Semaphore,
    existing: ExistingSkillIndex,
    stats: dict,
) -> bool:
    """Download a single skill if missing."""
    repo = normalize_repo(skill.get("repo", "") or skill.get("install", "") or "")
    if not repo or "/" not in repo:
        stats["skipped"] += 1
        return False

    name = derive_name(skill)
    provided_path = skill.get("path") or skill.get("github_path") or ""
    normalized_path = normalize_github_path(provided_path)

    # Skip if already present anywhere in skills/
    if existing.has(repo, normalized_path):
        stats["skipped"] += 1
        return False

    base_name = normalize_name(name)
    key = build_skill_key(repo, normalized_path, name=base_name, category=skill.get("category", ""))
    dir_name = choose_dir_name(base_name, repo, output_dir, key)
    skill_dir = output_dir / dir_name
    skill_file = skill_dir / "SKILL.md"

    if skill_file.exists():
        stats["skipped"] += 1
        return False

    patterns = get_url_patterns(repo, base_name, provided_path)

    for url in patterns[:10]:
        content, status = await fetch_url(session, url, semaphore)

        if content and is_valid_skill_content(content):
            branch, github_path_dir = extract_location_from_raw_url(url)

            # Create directory and save
            skill_dir.mkdir(parents=True, exist_ok=True)
            skill_file.write_text(content, encoding="utf-8")

            # Save metadata (normalized)
            category = canonicalize_category(skill.get("category", "other"), repo=repo)
            metadata = {
                "name": normalize_name(name),
                "description": str(skill.get("description", "") or "")[:200],
                "repo": repo,
                "category": category,
                "tags": skill.get("tags", []) or [],
                "stars": int(skill.get("stars", 0) or 0),
                "source": skill.get("source", ""),
                "github_path": github_path_dir,
                "github_branch": branch,
                "dir_name": dir_name,
                "downloaded_at": datetime.utcnow().isoformat() + "Z",
            }
            (skill_dir / "metadata.json").write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

            existing.add(repo, github_path_dir)
            stats["downloaded"] += 1
            return True

        if status == 403:
            stats["rate_limited"] += 1
            return False

    stats["not_found"] += 1
    return False


def load_skill_sources(sources_dir: Path) -> List[dict]:
    skills: List[dict] = []
    if not sources_dir.exists():
        return skills
    for source_file in sorted(sources_dir.glob("*.json")):
        try:
            data = json.loads(source_file.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning(f"Failed to load {source_file}: {e}")
            continue
        skills.extend(data.get("skills", []))
    return skills


def load_registry_entries(registry_path: Path) -> List[dict]:
    if not registry_path.exists():
        return []
    try:
        data = json.loads(registry_path.read_text(encoding="utf-8"))
        return data.get("skills", [])
    except Exception as e:
        logger.warning(f"Failed to load {registry_path}: {e}")
        return []


def dedupe_skills(skills: List[dict]) -> List[dict]:
    """Deduplicate by repo + normalized path (preferred), else repo+name."""
    seen: Set[str] = set()
    out: List[dict] = []

    for s in skills:
        repo = normalize_repo(s.get("repo", "") or s.get("install", "") or "")
        if not repo:
            continue
        path = normalize_github_path(s.get("path") or s.get("github_path") or "")
        name = normalize_name(s.get("name") or derive_name(s))
        key = f"{repo}:{path}" if path else f"{repo}::{name}"
        if key in seen:
            continue
        seen.add(key)
        out.append(s)

    return out


async def main_async(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).parent.parent
    skills_dir = repo_root / args.skills_dir
    output_dir = skills_dir / "data"

    # Load inputs
    skills: List[dict] = []
    skills.extend(load_skill_sources(repo_root / args.sources_dir))
    if args.include_registry:
        skills.extend(load_registry_entries(repo_root / args.registry))

    skills = dedupe_skills(skills)

    logger.info(f"Total skill refs to process: {len(skills)}")

    # Index existing
    existing = ExistingSkillIndex(skills_dir)

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    stats = {"downloaded": 0, "skipped": 0, "not_found": 0, "rate_limited": 0}

    headers = {"User-Agent": "Claude-Skills-Registry/2.0"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
        logger.info("Using GitHub token")

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT * 2)

    start_time = time.time()

    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        for i in range(0, len(skills), BATCH_SIZE):
            batch = skills[i : i + BATCH_SIZE]
            batch_num = i // BATCH_SIZE + 1
            total_batches = (len(skills) + BATCH_SIZE - 1) // BATCH_SIZE

            logger.info(f"Batch {batch_num}/{total_batches} ({len(batch)} skills)")

            tasks = [
                download_skill(session, skill, output_dir, semaphore, existing, stats)
                for skill in batch
            ]
            await asyncio.gather(*tasks, return_exceptions=True)

            elapsed = time.time() - start_time
            done = stats["downloaded"] + stats["skipped"] + stats["not_found"]
            rate = done / elapsed if elapsed > 0 else 0

            logger.info(
                f"Progress: ✅ {stats['downloaded']} | ⏭️ {stats['skipped']} | "
                f"❌ {stats['not_found']} | ⚡ {rate:.1f}/s"
            )

            await asyncio.sleep(0.2)

    elapsed = time.time() - start_time
    logger.info("DOWNLOAD COMPLETE")
    logger.info(f"  Downloaded:   {stats['downloaded']}")
    logger.info(f"  Skipped:      {stats['skipped']}")
    logger.info(f"  Not found:    {stats['not_found']}")
    logger.info(f"  Rate limited: {stats['rate_limited']}")
    logger.info(f"  Time:         {elapsed:.1f}s")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Download missing SKILL.md files")
    parser.add_argument("--skills-dir", default="skills", help="Skills directory (default: skills)")
    parser.add_argument("--sources-dir", default="sources", help="Sources directory (default: sources)")
    parser.add_argument("--registry", default="registry.json", help="Registry path (default: registry.json)")
    parser.add_argument(
        "--include-registry",
        action="store_true",
        help="Also process entries from registry.json (default: off)",
    )

    args = parser.parse_args()
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    raise SystemExit(main())
