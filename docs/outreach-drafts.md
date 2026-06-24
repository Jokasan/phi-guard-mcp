# Outreach Drafts

These drafts are for later manual posting. Do not post automatically.

## GitHub Description

MCP server and CLI for detecting, redacting, and auditing PHI before medical text is sent to AI
agents.

## Short Post

I released `phi-guard-mcp`, an open-source MCP server and CLI for healthcare AI privacy workflows.
It detects PHI-like identifiers, redacts them with stable placeholders, returns audit-friendly JSON,
and includes a synthetic benchmark plus CI privacy gate. It is local and rule-based, uses synthetic
examples only, and is explicitly not a diagnosis, treatment, triage, or HIPAA compliance tool.

Repo: https://github.com/dcl632/phi-guard-mcp

## MCP Directory Draft

`phi-guard-mcp` is a local MCP stdio server for AI agent workflows that need PHI-like identifier
detection before medical text enters an agent context. It provides `scan_phi`, `redact_phi`,
`audit_deidentification`, and `validate_no_phi`, with deterministic JSON output and Safe Harbor
mapping fields as review aids.

## Hacker News / Reddit Draft

Show HN: phi-guard-mcp, a local PHI redaction guardrail for AI agents

I built a small open-source MCP server and CLI for healthcare AI privacy workflows. It is meant to
sit before an AI agent and detect/redact PHI-like identifiers in plain text. The first release is
local, rule-based, synthetic-data-only, and deliberately avoids diagnosis, treatment, triage, or
compliance claims.

It includes:

- CLI and MCP stdio server
- PHI-like identifier findings with stable JSON
- Placeholder redaction
- Safe Harbor mapping fields as review aids
- Synthetic benchmark
- CI privacy gate for source and docs

Repo: https://github.com/dcl632/phi-guard-mcp
