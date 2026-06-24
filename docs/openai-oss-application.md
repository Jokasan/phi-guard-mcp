# OpenAI OSS Application Draft

This document is a draft for the OpenAI Codex for OSS application. Do not write private OpenAI,
billing, email, or organization account details into the repository.

## Project

- GitHub username: `dcl632`
- Repository URL: `https://github.com/dcl632/phi-guard-mcp`
- Role: primary maintainer and original AI-assisted implementation owner
- License: MIT

## Qualification Draft

`phi-guard-mcp` is an open-source MCP server and CLI for healthcare AI privacy workflows with
synthetic evals and CI maintainer tooling. It helps developers detect, redact, audit, and gate
PHI-like identifiers before medical text is sent to AI agents. The project is intentionally scoped
away from diagnosis, treatment, triage, and clinical decision support. Its v0.1.0 core is local and
rule-based, producing stable JSON findings that can be used by CLI scripts, MCP tools, tests,
privacy gates, and human review.

Healthcare AI needs privacy infrastructure at the agent boundary. Many agent demos can read and
summarize text, but production-facing medical workflows require explicit controls before text leaves
a local process or enters an agent context. `phi-guard-mcp` focuses on that gap: PHI-like identifier
detection, placeholder redaction, validation, Safe Harbor mapping, synthetic benchmark metrics, and
audit summaries with transparent rules.

## Maintenance Evidence

- MIT-licensed Python package with CLI and MCP stdio server.
- Synthetic-only examples and tests.
- Stable JSON API shared by Python, CLI, and MCP interfaces.
- Synthetic benchmark with precision, recall, F1, and per-category metrics.
- CI privacy gate for maintained source and documentation.
- Safe Harbor mapping fields as a review aid, with explicit non-compliance caveats.
- GitHub Actions plan for Ubuntu and Windows with lint, tests, compile checks, package build, and
  package metadata validation.
- Explicit safety scope documenting non-goals and avoiding clinical decision support claims.

## API Credits Draft

Use credits to improve Codex-assisted development of healthcare AI safety infrastructure: expand
synthetic PHI test coverage, review redaction edge cases, improve MCP tool ergonomics, write clearer
privacy documentation, and evaluate the project for security and release readiness. Credits would
not be used to process real patient data.

## Issue Ideas

- Add more synthetic name and date fixtures.
- Add configurable redaction modes for hash and fixed-token replacement.
- Add a rule report command that lists every detector and confidence value.
- Add Windows and macOS smoke-test instructions for MCP clients.
- Add a documented false-positive and false-negative review workflow.
