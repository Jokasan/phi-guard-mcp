"""MCP stdio server for PHI guard tools."""

from __future__ import annotations

import json
import sys
from importlib import metadata
from typing import Any

import anyio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field

from . import __version__
from .engine import audit_text, redact_text, scan_text, validate_no_phi
from .models import RedactionMode

SERVER_NAME = "phi-guard-mcp"

_HELP = """phi-guard-mcp

MCP stdio server for detecting, redacting, and auditing PHI-like identifiers
before medical text is sent to AI agents.

Usage:
  phi-guard-mcp            Start the MCP stdio server
  phi-guard-mcp --help     Show this help
  phi-guard-mcp --version  Show package version

CLI:
  phi-guard scan <file>
  phi-guard redact <file> --out <file>
  phi-guard audit <file>
  phi-guard validate <file>
"""


class TextArgs(BaseModel):
    text: str = Field(min_length=0, description="Plain text to inspect.")


class RedactArgs(TextArgs):
    mode: RedactionMode = Field(default="placeholder", description="Redaction mode.")


async def _scan_phi(args: TextArgs) -> dict[str, Any]:
    return scan_text(args.text).model_dump()


async def _redact_phi(args: RedactArgs) -> dict[str, Any]:
    return redact_text(args.text, mode=args.mode).model_dump()


async def _audit_deidentification(args: TextArgs) -> dict[str, Any]:
    return audit_text(args.text).model_dump()


async def _validate_no_phi(args: TextArgs) -> dict[str, Any]:
    return validate_no_phi(args.text).model_dump()


TOOL_REGISTRY: dict[str, tuple[type[BaseModel], Any, str]] = {
    "scan_phi": (
        TextArgs,
        _scan_phi,
        "Detect PHI-like identifiers and return structured findings.",
    ),
    "redact_phi": (
        RedactArgs,
        _redact_phi,
        "Detect and redact PHI-like identifiers with placeholders.",
    ),
    "audit_deidentification": (
        TextArgs,
        _audit_deidentification,
        "Return an audit-oriented summary of PHI-like identifiers and limitations.",
    ),
    "validate_no_phi": (
        TextArgs,
        _validate_no_phi,
        "Validate whether text has no detected PHI-like identifiers.",
    ),
}

server = Server(SERVER_NAME)


@server.list_tools()
async def _list_tools() -> list[Tool]:
    return [
        Tool(
            name=name,
            description=description,
            inputSchema=schema_cls.model_json_schema(),
        )
        for name, (schema_cls, _handler, description) in TOOL_REGISTRY.items()
    ]


@server.call_tool()
async def _call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
    if name not in TOOL_REGISTRY:
        raise ValueError(f"Unknown tool: {name}")

    schema_cls, handler, _description = TOOL_REGISTRY[name]
    parsed_args = schema_cls.model_validate(arguments or {})
    result = await handler(parsed_args)
    return [TextContent(type="text", text=json.dumps(result, indent=2, ensure_ascii=False))]


async def _run_stdio_server() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def _package_version() -> str:
    try:
        return metadata.version("phi-guard-mcp")
    except metadata.PackageNotFoundError:
        return __version__


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    if args in (["--help"], ["-h"]):
        print(_HELP)
        return
    if args == ["--version"]:
        print(f"phi-guard-mcp {_package_version()}")
        return
    if args:
        print(_HELP, file=sys.stderr)
        raise SystemExit(2)
    anyio.run(_run_stdio_server)


if __name__ == "__main__":
    main()
