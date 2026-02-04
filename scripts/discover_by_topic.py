#!/usr/bin/env python3
"""
Discover skills by GitHub Topics
Uses GitHub Search API to find repositories with claude-code-skills or claude-skills topics
"""

import os
import json
import time
import logging
import requests
from datetime import datetime
from pathlib import Path

from utils import normalize_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"

# Topics to search for
SKILL_TOPICS = [
    "claude-code-skills",
    "claude-skills",
    "agent-skills",
    "codex-skills",
]

# Search queries for finding SKILL.md files
CODE_SEARCH_QUERIES = [
    "filename:SKILL.md",
    "filename:SKILL.md path:.claude/skills",
    "filename:SKILL.md path:skills",
]


class GitHubTopicDiscovery:
    """Discover skills using GitHub Topics and Code Search"""

    def __init__(self, token=None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/vnd.github.v3+json'
        if self.token:
            self.session.headers['Authorization'] = f'token {self.token}'
            logger.info("Using authenticated GitHub API")
        else:
            logger.warning("No token - rate limits will be strict (10 req/min)")

        self.discovered_repos = set()
        self.skills = []

    def _request(self, url, params=None):
        """Make rate-limited request (search API: 30 req/min for authenticated)"""
        time.sleep(2)
        try:
            resp = self.session.get(url, params=params, timeout=30)

            # Handle rate limiting
            if resp.status_code == 403:
                reset = int(resp.headers.get('X-RateLimit-Reset', 0))
                if reset:
                    wait = max(0, reset - time.time() + 1)
                    if wait < 3600:
                        logger.warning(f"Rate limited, waiting {wait:.0f}s")
                        time.sleep(wait)
                        return self._request(url, params)
                return None

            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None

    def discover_by_topics(self, topics=None):
        """Discover repositories by GitHub topics"""
        topics = topics or SKILL_TOPICS

        for topic in topics:
            logger.info(f"Searching topic: {topic}")

            page = 1
            while page <= 10:  # Max 1000 results
                url = f"{GITHUB_API}/search/repositories"
                params = {
                    'q': f'topic:{topic}',
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': 100,
                    'page': page,
                }

                result = self._request(url, params)
                if not result:
                    break

                items = result.get('items', [])
                if not items:
                    break

                for repo in items:
                    full_name = repo['full_name']
                    if full_name not in self.discovered_repos:
                        self.discovered_repos.add(full_name)
                        logger.info(f"  Found: {full_name} ({repo.get('stargazers_count', 0)} stars)")

                total = result.get('total_count', 0)
                if page * 100 >= total:
                    break
                page += 1

        logger.info(f"Discovered {len(self.discovered_repos)} repositories from topics")
        return list(self.discovered_repos)

    def discover_by_code_search(self, queries=None):
        """Discover SKILL.md files using GitHub Code Search"""
        queries = queries or CODE_SEARCH_QUERIES

        for query in queries:
            logger.info(f"Code search: {query}")

            page = 1
            while page <= 10:
                url = f"{GITHUB_API}/search/code"
                params = {
                    'q': query,
                    'per_page': 100,
                    'page': page,
                }

                result = self._request(url, params)
                if not result:
                    break

                items = result.get('items', [])
                if not items:
                    break

                for item in items:
                    repo = item['repository']['full_name']
                    path = item['path']

                    if repo not in self.discovered_repos:
                        self.discovered_repos.add(repo)
                        logger.info(f"  Found: {repo} - {path}")

                total = result.get('total_count', 0)
                if page * 100 >= total:
                    break
                page += 1

        logger.info(f"Total discovered: {len(self.discovered_repos)} repositories")
        return list(self.discovered_repos)

    def get_skill_files_from_repo(self, repo):
        """Find all SKILL.md files in a repository"""
        skills = []

        # Common skill locations
        paths_to_check = [
            '',
            'skills',
            '.claude/skills',
            '.codex/skills',
        ]

        # First try to search the repo for SKILL.md files
        url = f"{GITHUB_API}/search/code"
        params = {
            'q': f'filename:SKILL.md repo:{repo}',
            'per_page': 100,
        }

        result = self._request(url, params)
        if result and result.get('items'):
            for item in result['items']:
                skills.append({
                    'repo': repo,
                    'path': item['path'],
                    'html_url': item['html_url'],
                })

        return skills

    def run(self, output_json: str = 'sources/discovered.json'):
        """Run discovery pipeline and write `sources/discovered.json`."""

        # Load previously discovered repos to skip
        existing_repos = set()
        if Path(output_json).exists():
            try:
                with open(output_json) as f:
                    prev = json.load(f)
                existing_repos = set(prev.get('repos', []))
                logger.info(f"Skipping {len(existing_repos)} previously discovered repos")
            except Exception:
                pass

        # Phase 1: Discover by topics
        logger.info("=== Phase 1: Topic Discovery ===")
        self.discover_by_topics()

        # Phase 2: Discover by code search
        logger.info("\n=== Phase 2: Code Search ===")
        self.discover_by_code_search()

        # Filter to only new repos
        new_repos = self.discovered_repos - existing_repos
        logger.info(f"New repos to scan: {len(new_repos)} (total discovered: {len(self.discovered_repos)})")

        # Phase 3: Download skills from new repos (concurrent)
        logger.info("\n=== Phase 3: Collect SKILL.md paths ===")

        # Collect all skill files to download
        download_tasks = []
        for repo in new_repos:
            logger.info(f"Scanning {repo}...")
            skill_files = self.get_skill_files_from_repo(repo)
            for skill in skill_files:
                download_tasks.append((repo, skill['path']))

        logger.info(f"Skills to download: {len(download_tasks)}")

        for repo, path in download_tasks:
            skill_name = repo.split("/")[-1]
            if path and path != "SKILL.md":
                skill_name = path.replace("\\", "/").rsplit("/", 1)[0].split("/")[-1]

            self.skills.append(
                {
                    "name": normalize_name(skill_name),
                    "repo": repo,
                    "path": path,  # repo-relative file path to SKILL.md (preferred)
                    "category": "other",
                    "tags": [],
                    "stars": 0,
                    "source": f"github.com/{repo}",
                }
            )

        # Merge with existing repos for the output
        self.discovered_repos |= existing_repos

        # Save discovery results
        Path(output_json).parent.mkdir(parents=True, exist_ok=True)
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump({
                'discovered_at': datetime.utcnow().isoformat() + 'Z',
                'total_repos': len(self.discovered_repos),
                'total_skills': len(self.skills),
                'repos': list(self.discovered_repos),
                'skills': self.skills,
            }, f, indent=2, ensure_ascii=False)

        logger.info(f"\n=== Summary ===")
        logger.info(f"Repositories discovered: {len(self.discovered_repos)}")
        logger.info(f"Skill references collected: {len(self.skills)}")
        logger.info(f"Results saved to: {output_json}")

        return self.skills


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Discover skills from GitHub')
    parser.add_argument('--token', help='GitHub token (or set GITHUB_TOKEN env)')
    parser.add_argument('--json', default='sources/discovered.json', help='JSON output')

    args = parser.parse_args()

    discoverer = GitHubTopicDiscovery(token=args.token)
    discoverer.run(output_json=args.json)


if __name__ == '__main__':
    main()
