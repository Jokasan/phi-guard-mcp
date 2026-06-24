# Demo

This demo uses synthetic data only.

## CLI Scan

Create a short synthetic note:

```bash
printf 'Patient Name: Jordan Rivera, MRN: MRN-48291\n' > /tmp/phi-guard-demo.txt
```

Scan the note:

```bash
phi-guard scan /tmp/phi-guard-demo.txt
```

Expected output shape:

```json
{
  "findings": [
    {
      "category": "NAME",
      "text": "Jordan Rivera",
      "start": 14,
      "end": 27,
      "confidence": 0.9,
      "rule_id": "name_label",
      "safe_harbor_identifier": "Names"
    },
    {
      "category": "MRN",
      "text": "MRN-48291",
      "start": 34,
      "end": 43,
      "confidence": 0.98,
      "rule_id": "mrn",
      "safe_harbor_identifier": "Medical record numbers"
    }
  ]
}
```

## CLI Redact

```bash
phi-guard redact /tmp/phi-guard-demo.txt --out /tmp/phi-guard-redacted.txt
cat /tmp/phi-guard-redacted.txt
```

Expected redacted text:

```text
Patient Name: [NAME], MRN: [MRN]
```

## CLI Audit

```bash
phi-guard audit /tmp/phi-guard-demo.txt
```

Audit output includes category counts, Safe Harbor review-aid mapping, and explicit limitations.

## MCP Client Config

Install the package and point an MCP-compatible client at the stdio command:

```json
{
  "mcpServers": {
    "phi-guard": {
      "command": "phi-guard-mcp"
    }
  }
}
```

The server exposes:

- `scan_phi(text)`
- `redact_phi(text, mode="placeholder")`
- `audit_deidentification(text)`
- `validate_no_phi(text)`

Example tool input:

```json
{
  "text": "Patient Name: Jordan Rivera, MRN: MRN-48291"
}
```

Example `validate_no_phi` result:

```json
{
  "ok": false,
  "finding_count": 2
}
```

The MCP tools return the same structured finding fields as the CLI.
