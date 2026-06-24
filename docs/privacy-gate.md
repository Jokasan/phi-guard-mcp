# Privacy Gate

The privacy gate scans maintained source and documentation before release or pull request review:

```bash
phi-guard gate --config .phi-guard.toml
```

The default repository config scans:

- `README.md`
- `docs/**/*.md`
- `src/**/*.py`
- `pyproject.toml`

It excludes synthetic fixtures, tests, generated packages, virtual environments, and build outputs.
This keeps the gate focused on accidental PHI-like identifiers in project-maintained content, while
allowing synthetic benchmark and test data to exist in clearly labeled folders.

The gate returns JSON and exits with code `1` when it finds unallowed PHI-like identifiers. Public
reference URLs can be allowed by exact text in `.phi-guard.toml`; this should only be used for known
documentation links, not patient data.
