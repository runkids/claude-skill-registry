#!/usr/bin/env python3
"""
Normalization helpers for building a consistent registry.

This repo aggregates skills from many sources with inconsistent metadata.
These helpers enforce a small canonical category set and stable GitHub paths.
"""

from __future__ import annotations

from dataclasses import dataclass


CANONICAL_CATEGORIES: set[str] = {
    "development",
    "devops",
    "security",
    "documents",
    "design",
    "testing",
    "product",
    "marketing",
    "productivity",
    "data",
    "official",
    "other",
}


OFFICIAL_REPOS: set[str] = {
    "anthropics/skills",
    "anthropics/claude-code",
    "openai/codex",
    "openai/openai-agents-python",
}


def normalize_repo(repo: str) -> str:
    if not repo:
        return ""
    repo = repo.strip()
    if repo.startswith("https://github.com/"):
        repo = repo.replace("https://github.com/", "", 1)
    repo = repo.split("/tree/")[0]
    repo = repo.strip("/")

    # Keep only "owner/repo". Anything else is either invalid or belongs in "path".
    parts = [p for p in repo.split("/") if p]
    if len(parts) < 2:
        return ""
    return f"{parts[0]}/{parts[1]}"


def _contains_any(value: str, needles: tuple[str, ...]) -> bool:
    return any(n in value for n in needles)


def canonicalize_category(category: str | None, repo: str = "") -> str:
    """
    Map arbitrary category strings to a small canonical set.

    This is intentionally opinionated (breaking): unknown categories collapse to "other".
    """
    repo = normalize_repo(repo)
    if repo in OFFICIAL_REPOS:
        return "official"

    raw = (category or "").strip().lower()
    if not raw:
        return "other"

    if raw in CANONICAL_CATEGORIES:
        return raw

    # Normalize common variants and compound labels
    if _contains_any(raw, ("devops", "ops", "ci", "cd", "k8s", "kubernetes", "docker", "helm", "terraform", "infra")):
        return "devops"

    if _contains_any(raw, ("security", "auth", "vuln", "vulnerability", "pentest", "owasp", "threat", "incident")):
        return "security"

    # "document-processing" etc.
    if _contains_any(raw, ("doc", "document", "pdf", "docx", "ppt", "pptx", "xlsx", "word", "excel")):
        return "documents"

    if _contains_any(raw, ("design", "ui", "ux", "css", "theme", "theming", "visual", "brand")):
        return "design"

    if _contains_any(raw, ("test", "testing", "qa", "playwright", "jest", "vitest", "cypress")):
        return "testing"

    if _contains_any(raw, ("data", "analytics", "analysis", "etl", "sql", "database", "warehouse", "ml", "model")):
        return "data"

    if _contains_any(raw, ("marketing", "seo", "content", "growth", "social", "ads")):
        return "marketing"

    if _contains_any(raw, ("productivity", "automation", "workflow", "ops-tools", "tooling")):
        return "productivity"

    if _contains_any(raw, ("product", "pm", "roadmap", "requirements")):
        return "product"

    if _contains_any(raw, ("dev", "development", "code", "engineering")):
        return "development"

    return "other"


def normalize_github_path(value: str | None) -> str:
    """
    Normalize a repo-relative skill path to a directory path.

    Accepts either a directory path or a file path ending in SKILL.md.
    """
    if not value:
        return ""
    path = str(value).strip().lstrip("/")
    if not path:
        return ""
    if path == "SKILL.md":
        return ""
    if path.endswith("/SKILL.md"):
        return path[: -len("/SKILL.md")]
    return path


@dataclass(frozen=True)
class GitHubLocation:
    path: str
    branch: str


def extract_github_location(metadata: dict) -> GitHubLocation:
    """
    Extract (path, branch) from heterogeneous metadata formats.

    Rules:
    - Prefer `github_path`, fall back to `path`
    - Normalize to directory path (no trailing /SKILL.md)
    - Prefer `github_branch`, fall back to `branch`, default "main"
    """
    github_path = normalize_github_path(metadata.get("github_path") or metadata.get("path"))

    branch = metadata.get("github_branch") or metadata.get("branch") or "main"
    branch = str(branch).strip() if branch is not None else "main"
    if not branch:
        branch = "main"

    return GitHubLocation(path=github_path, branch=branch)
