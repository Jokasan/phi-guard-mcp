# MCP Client Setup

This guide shows how to wire `phi-guard-mcp` into local MCP-compatible agent clients.
All examples use synthetic text only. No real patient data is required or shown.

## 1. Install

```bash
pip install phi-guard-mcp
```

Verify the server binary is on your PATH:

```bash
phi-guard-mcp --version
```

## 2. Minimal stdio server config

All MCP-compatible clients accept a JSON block that names the stdio command. The minimal config is the same everywhere — only the file location differs.

```json
{
  "mcpServers": {
    "phi-guard": {
      "command": "phi-guard-mcp"
    }
  }
}
```

### Where to put it

| Client | Config file |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor (project) | `.cursor/mcp.json` |
| Cursor (global) | `~/.cursor/mcp.json` |
| Cline (VS Code) | Cline sidebar → MCP Servers → Edit config |
| Claude Code (CLI) | `claude mcp add phi-guard phi-guard-mcp` |

Restart the client after saving. The server registers four tools:
`scan_phi`, `redact_phi`, `audit_deidentification`, `validate_no_phi`.

## 3. Example: scan_phi

Detects PHI-like identifiers and returns structured findings with Safe Harbor mapping.

**Tool call input**

```json
{
  "text": "Patient Name: Jordan Rivera, MRN: MRN-48291"
}
```

**Response**

```json
{
  "ok": true,
  "text_length": 43,
  "findings": [
    {
      "category": "NAME",
      "text": "Jordan Rivera",
      "start": 14,
      "end": 27,
      "confidence": 0.84,
      "rule_id": "name.clinical_label",
      "safe_harbor_identifier": "Names"
    },
    {
      "category": "MRN",
      "text": "MRN-48291",
      "start": 34,
      "end": 43,
      "confidence": 0.96,
      "rule_id": "mrn.labeled",
      "safe_harbor_identifier": "Medical record numbers"
    }
  ],
  "summary": {
    "MRN": 1,
    "NAME": 1
  }
}
```

## 4. Example: redact_phi

Replaces PHI-like identifiers with stable category placeholders.

**Tool call input**

```json
{
  "text": "Patient Name: Jordan Rivera, MRN: MRN-48291",
  "mode": "placeholder"
}
```

**Response**

```json
{
  "ok": true,
  "mode": "placeholder",
  "redacted_text": "Patient Name: [NAME], MRN: [MRN]",
  "findings": [
    {
      "category": "NAME",
      "text": "Jordan Rivera",
      "start": 14,
      "end": 27,
      "confidence": 0.84,
      "rule_id": "name.clinical_label",
      "safe_harbor_identifier": "Names"
    },
    {
      "category": "MRN",
      "text": "MRN-48291",
      "start": 34,
      "end": 43,
      "confidence": 0.96,
      "rule_id": "mrn.labeled",
      "safe_harbor_identifier": "Medical record numbers"
    }
  ],
  "summary": {
    "MRN": 1,
    "NAME": 1
  }
}
```

## Notes

- The `mode` field in `redact_phi` is optional; `"placeholder"` is the default and current only supported value.
- All four tools return the same `Finding` schema, so downstream automation can treat results uniformly.
- Do not pass real patient records. Use synthetic or properly authorized text only.
- `phi-guard-mcp` is a local, rule-based guardrail. It is not a HIPAA compliance guarantee and not a substitute for legal or privacy review. See [Safety scope](safety-scope.md).
