# Contributing to phi-guard-mcp

Thanks for helping improve `phi-guard-mcp`. This project is healthcare AI privacy infrastructure,
not a clinical decision support tool. Contributions should keep that boundary clear.

## Ground Rules

- Do not submit real patient records, real medical identifiers, or private account data.
- Use synthetic examples only.
- Do not add diagnosis, treatment, triage, prognosis, medication, or clinical risk-scoring features.
- Keep outputs deterministic and reviewable.
- Preserve the stable JSON shape used by the Python API, CLI, and MCP tools unless a change is
  explicitly discussed first.

## Development

Use Python 3.12.

```bash
python -m pip install -e ".[dev]"
python -m compileall -q src tests
python -m pytest -q
ruff check .
phi-guard gate --config .phi-guard.toml
python -m build
twine check dist/*
```

## Pull Requests

Please include:

- What changed and why.
- Whether the change affects PHI detection, redaction, audit output, CLI, or MCP behavior.
- The synthetic fixtures or tests used.
- Confirmation that no real PHI or private identifiers were added.

## Benchmark Cases

Benchmark cases must be synthetic. Expected findings should use exact `category` and `text` pairs so
regressions are easy to review.

## Security and Privacy Reports

Do not open a public issue with real PHI, secrets, exploit details, or private infrastructure data.
Use the process in `SECURITY.md`.
