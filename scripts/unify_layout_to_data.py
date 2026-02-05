#!/usr/bin/env python3
"""
Unify main repo layout to a single flat archive under skills/data.

Moves any skill directory outside skills/data into skills/data, preserving
all skills and resolving conflicts with __dup-<hash> suffixes.
"""

import json
import shutil
import argparse
import hashlib
from pathlib import Path
from collections import defaultdict

from utils import build_skill_key, normalize_name


def load_metadata(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Unify skills layout to skills/data")
    parser.add_argument("--max-moves", type=int, default=0, help="Limit moves for batch runs")
    parser.add_argument("--progress-every", type=int, default=1000, help="Print progress every N moves")
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    skills_dir = repo_root / "skills"
    data_dir = skills_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Build set of skill dirs (avoid nested skill dirs)
    skill_dirs = {p.parent for p in skills_dir.rglob("SKILL.md")}
    filtered = []
    for skill_dir in skill_dirs:
        if data_dir in skill_dir.parents or skill_dir == data_dir:
            continue
        # skip if any parent is also a skill dir
        parent = skill_dir.parent
        nested = False
        while parent != skills_dir and parent != parent.parent:
            if parent in skill_dirs:
                nested = True
                break
            parent = parent.parent
        if not nested:
            filtered.append(skill_dir)
    skill_dirs = filtered

    # Existing names in data dir (lowercase -> count)
    existing = defaultdict(int)
    for d in data_dir.iterdir():
        if d.is_dir():
            existing[d.name.lower()] += 1

    moved = 0
    skipped = 0

    for skill_dir in sorted(skill_dirs):
        meta_path = skill_dir / "metadata.json"
        meta = load_metadata(meta_path)

        name = meta.get("name") or meta.get("dir_name") or skill_dir.name
        name = normalize_name(name)
        category = meta.get("category", "")
        repo = meta.get("repo", "")
        path = meta.get("path") or meta.get("github_path") or meta.get("source_path") or ""

        key = build_skill_key(repo, path, name=name, category=category)
        suffix_hash = hashlib.sha1((key or name).encode("utf-8", errors="ignore")).hexdigest()[:8]

        base = normalize_name(name)
        target_name = base
        if existing[target_name.lower()] > 0:
            suffix = f"__dup-{suffix_hash or 'unknown'}"
            target_name = f"{base}{suffix}"
            counter = 2
            while existing[target_name.lower()] > 0:
                target_name = f"{base}{suffix}-{counter}"
                counter += 1
        target_dir = data_dir / target_name
        existing[target_name.lower()] += 1

        if target_dir.resolve() == skill_dir.resolve():
            skipped += 1
            continue

        target_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(skill_dir), str(target_dir))

        meta_out = meta.copy() if meta else {}
        if meta_out:
            meta_out["dir_name"] = target_dir.name
            if not meta_out.get("category"):
                meta_out["category"] = "other"
            (target_dir / "metadata.json").write_text(
                json.dumps(meta_out, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )

        moved += 1
        if args.progress_every and moved % args.progress_every == 0:
            print(f"Moved: {moved} (skipped {skipped})")
        if args.max_moves and moved >= args.max_moves:
            break

    print(f"Moved: {moved}")
    print(f"Skipped: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
