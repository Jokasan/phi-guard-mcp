# phi-guard-mcp

[![CI](https://github.com/charlesree826/phi-guard-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/charlesree826/phi-guard-mcp/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/phi-guard-mcp.svg)](https://pypi.org/project/phi-guard-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/phi-guard-mcp.svg)](https://pypi.org/project/phi-guard-mcp/)
[![Release](https://img.shields.io/github/v/release/charlesree826/phi-guard-mcp.svg)](https://github.com/charlesree826/phi-guard-mcp/releases)
[![License](https://img.shields.io/github/license/charlesree826/phi-guard-mcp.svg)](LICENSE)

MCP server and CLI for detecting, redacting, and auditing PHI before medical text is sent to AI
agents.

`phi-guard-mcp` is healthcare AI safety infrastructure, not a clinical product. It is a local,
rule-based guardrail that helps developers identify PHI-like identifiers in plain text, redact them
with stable placeholders, and produce audit-friendly JSON before content reaches an AI agent or MCP
workflow.

Proof points for maintainers:

- Synthetic benchmark with exact-match PHI finding evaluation.
- Safe Harbor mapping audit fields for review workflows.
- CI privacy gate that blocks PHI-like identifiers in maintained source and docs.
- CLI, Python API, and MCP stdio tools sharing one stable JSON result model.

Important scope limits:

- Not for diagnosis, treatment, triage, medical advice, or medication recommendations.
- Not a HIPAA compliance guarantee and not a substitute for legal, privacy, or security review.
- Not an FDA-regulated clinical decision support or device software function.
- Do not test with real patient records. The examples in this repo are synthetic.

The project aligns its documentation vocabulary with HHS HIPAA de-identification concepts such as
Safe Harbor and Expert Determination, while intentionally avoiding clinical decision support scope.
See [HHS de-identification guidance](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html),
[FDA CDS guidance](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software),
and [FDA device software functions](https://www.fda.gov/medical-devices/digital-health-center-excellence/device-software-functions-including-mobile-medical-applications).

## Install

```bash
python -m pip install phi-guard-mcp
```

For local development:

```bash
python -m pip install -e ".[dev]"
```

## Quickstart

Scan a synthetic note:

```bash
phi-guard scan examples/synthetic_clinical_note.txt
```

Redact PHI-like identifiers:

```bash
phi-guard redact examples/synthetic_clinical_note.txt --out /tmp/synthetic_redacted.txt
```

Audit a note:

```bash
phi-guard audit examples/synthetic_clinical_note.txt
```

Validate text before it enters an AI agent:

```bash
phi-guard validate examples/synthetic_clean_note.txt
```

Run the synthetic benchmark:

```bash
phi-guard benchmark benchmarks/synthetic/cases --out benchmarks/synthetic-report.json
```

Run the repository privacy gate:

```bash
phi-guard gate --config .phi-guard.toml
```

All CLI commands output stable JSON for automation.

See [docs/demo.md](docs/demo.md) for a complete CLI and MCP transcript.

## MCP Server

Run the stdio MCP server:

```bash
phi-guard-mcp
```

Available tools:

- `scan_phi(text)`
- `redact_phi(text, mode="placeholder")`
- `audit_deidentification(text)`
- `validate_no_phi(text)`

MCP tools return the same finding schema as the CLI, including `safe_harbor_identifier`.

Example MCP client config:

```json
{
  "mcpServers": {
    "phi-guard": {
      "command": "phi-guard-mcp"
    }
  }
}
```

## Python API

```python
from phi_guard_mcp import audit_text, evaluate_benchmark, redact_text, scan_text, validate_no_phi

result = scan_text("Patient Name: Jordan Rivera, MRN: MRN-48291")
redacted = redact_text("Patient Name: Jordan Rivera, MRN: MRN-48291")
audit = audit_text("Patient Name: Jordan Rivera, MRN: MRN-48291")
validation = validate_no_phi("No identifiers are present in this synthetic note.")
benchmark = evaluate_benchmark("benchmarks/synthetic/cases")
```

## What It Detects

The first release focuses on plain text and common PHI-like identifiers:

- Names in clinical label contexts
- Dates
- Phone numbers
- Email addresses
- Address-like fragments
- Medical record numbers
- Social Security numbers
- URLs and IP addresses
- Medical facility names
- Account, member, policy, and patient ID tokens

This is a deterministic heuristic engine. It favors transparent behavior and repeatable JSON over
opaque model judgment.

Safe Harbor mapping is included as a review aid only. It does not make output HIPAA compliant and
does not replace Expert Determination or legal review.

## Project Docs

- [Demo](docs/demo.md)
- [Synthetic benchmark](docs/benchmark.md)
- [Privacy gate](docs/privacy-gate.md)
- [Safety scope](docs/safety-scope.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

## Development

```bash
python -m compileall -q src tests
python -m pytest -q
ruff check .
phi-guard gate --config .phi-guard.toml
python -m build
twine check dist/*
```
