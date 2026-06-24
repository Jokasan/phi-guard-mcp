"""Repository privacy gate for PHI-like identifiers."""

from __future__ import annotations

import fnmatch
import tomllib
from pathlib import Path

from .engine import scan_text
from .models import Finding, GateFileReport, GateReport

DEFAULT_INCLUDE = [
    "**/*.txt",
    "**/*.md",
    "**/*.py",
    "**/*.json",
    "pyproject.toml",
]

DEFAULT_EXCLUDE = [
    ".git/**",
    ".venv/**",
    "dist/**",
    "build/**",
    "examples/**",
    "tests/**",
    "benchmarks/**",
    "__pycache__/**",
]


def run_gate(root: str | Path = ".", config_path: str | Path | None = None) -> GateReport:
    """Scan configured repository paths and fail when PHI-like identifiers are found."""

    root_path = Path(root).resolve()
    include, exclude, allow_text = _load_config(root_path, config_path)
    files = _discover_files(root_path, include, exclude)

    flagged: list[GateFileReport] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        scan = scan_text(text)
        findings = [finding for finding in scan.findings if finding.text not in allow_text]
        if findings:
            flagged.append(
                GateFileReport(
                    path=path.relative_to(root_path).as_posix(),
                    findings=findings,
                    summary=_summarize_findings(findings),
                )
            )

    return GateReport(
        ok=not flagged,
        root=str(root_path),
        scanned_files=len(files),
        flagged_files=len(flagged),
        findings=flagged,
    )


def _load_config(root: Path, config_path: str | Path | None) -> tuple[list[str], list[str], set[str]]:
    resolved_config = _resolve_config_path(root, config_path)
    if resolved_config is None:
        return DEFAULT_INCLUDE, DEFAULT_EXCLUDE, set()

    data = tomllib.loads(resolved_config.read_text(encoding="utf-8"))
    gate_config = data.get("gate", {})
    return (
        list(gate_config.get("include", DEFAULT_INCLUDE)),
        list(gate_config.get("exclude", DEFAULT_EXCLUDE)),
        set(gate_config.get("allow_text", [])),
    )


def _resolve_config_path(root: Path, config_path: str | Path | None) -> Path | None:
    if config_path is not None:
        candidate = Path(config_path)
        if not candidate.is_absolute():
            candidate = root / candidate
        if not candidate.exists():
            raise FileNotFoundError(candidate)
        return candidate

    default_config = root / ".phi-guard.toml"
    return default_config if default_config.exists() else None


def _discover_files(root: Path, include: list[str], exclude: list[str]) -> list[Path]:
    if root.is_file():
        return [root]

    paths: set[Path] = set()
    for pattern in include:
        for candidate in root.glob(pattern):
            if candidate.is_file() and not _is_excluded(candidate.relative_to(root), exclude):
                paths.add(candidate)
    return sorted(paths)


def _is_excluded(relative_path: Path, exclude: list[str]) -> bool:
    path = relative_path.as_posix()
    return any(fnmatch.fnmatch(path, pattern) for pattern in exclude)


def _summarize_findings(findings: list[Finding]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for finding in findings:
        summary[finding.category] = summary.get(finding.category, 0) + 1
    return dict(sorted(summary.items()))
