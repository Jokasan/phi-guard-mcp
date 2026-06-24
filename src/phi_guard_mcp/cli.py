"""Command line interface for phi-guard."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .benchmark import evaluate_benchmark
from .engine import audit_text, redact_text, scan_text, validate_no_phi
from .gate import run_gate


def main(argv: Sequence[str] | None = None) -> int:
    argv = tuple(sys.argv[1:] if argv is None else argv)
    parser = _build_parser()

    if argv in (("--help",), ("-h",)):
        parser.print_help()
        return 0
    if argv == ("--version",):
        print(f"phi-guard {__version__}")
        return 0

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    if args.command == "benchmark":
        result = evaluate_benchmark(args.cases_dir)
        payload = result.model_dump()
        if args.out:
            _write_json(args.out, payload)
        _print_json(payload)
        return 0

    if args.command == "gate":
        result = run_gate(args.path, config_path=args.config)
        _print_json(result.model_dump())
        return 0 if result.ok else 1

    text = _read_text(args.file)

    if args.command == "scan":
        _print_json(scan_text(text).model_dump())
        return 0

    if args.command == "redact":
        result = redact_text(text, mode=args.mode)
        out_path = Path(args.out)
        out_path.write_text(result.redacted_text, encoding="utf-8")
        _print_json(result.model_dump())
        return 0

    if args.command == "audit":
        _print_json(audit_text(text).model_dump())
        return 0

    if args.command == "validate":
        result = validate_no_phi(text)
        _print_json(result.model_dump())
        return 0 if result.ok else 1

    parser.error(f"Unknown command: {args.command}")
    return 2


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="phi-guard",
        description="Detect, redact, and audit PHI-like identifiers before text reaches AI agents.",
    )
    parser.add_argument("--version", action="version", version=f"phi-guard {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan", help="Scan a text file and output JSON findings.")
    scan_parser.add_argument("file", help="Path to .txt, .md, .json, or '-' for stdin.")

    redact_parser = subparsers.add_parser("redact", help="Redact a text file and write the result.")
    redact_parser.add_argument("file", help="Path to .txt, .md, .json, or '-' for stdin.")
    redact_parser.add_argument("--out", required=True, help="Path for the redacted output file.")
    redact_parser.add_argument("--mode", choices=["placeholder"], default="placeholder")

    audit_parser = subparsers.add_parser("audit", help="Output an audit JSON report.")
    audit_parser.add_argument("file", help="Path to .txt, .md, .json, or '-' for stdin.")

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate that no PHI-like identifiers are detected.",
    )
    validate_parser.add_argument("file", help="Path to .txt, .md, .json, or '-' for stdin.")

    benchmark_parser = subparsers.add_parser("benchmark", help="Run a synthetic benchmark.")
    benchmark_parser.add_argument("cases_dir", help="Directory containing synthetic benchmark JSON cases.")
    benchmark_parser.add_argument("--out", help="Optional path for the benchmark JSON report.")

    gate_parser = subparsers.add_parser("gate", help="Run the repository privacy gate.")
    gate_parser.add_argument("path", nargs="?", default=".", help="Directory or file to scan.")
    gate_parser.add_argument("--config", help="Path to .phi-guard.toml.")

    return parser


def _read_text(file_arg: str) -> str:
    if file_arg == "-":
        return sys.stdin.read()
    return Path(file_arg).read_text(encoding="utf-8")


def _print_json(payload: object) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def _write_json(path: str, payload: object) -> None:
    Path(path).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
