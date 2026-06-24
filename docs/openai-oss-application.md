# OpenAI OSS Application Draft

This document is a draft for the OpenAI Codex for OSS application. Do not write private OpenAI,
billing, email, or organization account details into the repository.

Official references:

- Codex for OSS: https://developers.openai.com/community/codex-for-oss
- Program Terms: https://developers.openai.com/codex/codex-for-oss-terms

## Project

- GitHub username: `dcl632`
- Repository URL: `https://github.com/dcl632/phi-guard-mcp`
- PyPI package: `https://pypi.org/project/phi-guard-mcp/`
- Role: primary maintainer and original AI-assisted implementation owner
- License: MIT
- Current release: `v0.1.1`

## Qualification Draft

`phi-guard-mcp` is an open-source MCP server and CLI for healthcare AI privacy workflows with
synthetic evals, Safe Harbor mapping fields, and CI maintainer tooling. It helps developers detect,
redact, audit, and gate PHI-like identifiers before medical text is sent to AI agents. The project
is intentionally scoped away from diagnosis, treatment, triage, and clinical decision support. Its
core is local and rule-based, producing stable JSON findings that can be used by CLI scripts, MCP
tools, tests, privacy gates, and human review.

Healthcare AI needs privacy infrastructure at the agent boundary. Many agent demos can read and
summarize text, but production-facing medical workflows require explicit controls before text leaves
a local process or enters an agent context. `phi-guard-mcp` focuses on that gap: PHI-like identifier
detection, placeholder redaction, validation, Safe Harbor mapping as a review aid, synthetic
benchmark metrics, and audit summaries with transparent deterministic rules.

This is a new project, so the application should not overstate adoption. The ecosystem importance is
the gap it targets: local privacy guardrails for AI agent workflows that may handle medical text,
without turning the project into regulated clinical decision support.

## Maintenance Evidence

- MIT-licensed Python package with CLI and MCP stdio server.
- Public GitHub release `v0.1.1` with wheel and source distribution.
- PyPI package for `pip install phi-guard-mcp`.
- GitHub Actions on Ubuntu and Windows for lint, tests, compile checks, privacy gate, package build,
  and package metadata validation.
- Community files: contributing guide, security policy, code of conduct, issue templates, and pull
  request template.
- Public roadmap issues for benchmark expansion, MCP setup docs, installation smoke tests, security
  review, and external tester feedback.
- Synthetic-only examples, tests, and benchmark cases.
- Stable JSON API shared by Python, CLI, and MCP interfaces.
- CI privacy gate for maintained source and documentation.
- Explicit safety scope documenting non-goals and avoiding clinical decision support claims.

## API Credits Draft

Use credits to improve Codex-assisted development of healthcare AI safety infrastructure: expand
synthetic PHI test coverage, review redaction edge cases, improve MCP tool ergonomics, write clearer
privacy documentation, triage public issues, and evaluate the project for security and release
readiness. Credits would not be used to process real patient data.

## Stars / Downloads / Ecosystem Importance Draft

This is a new repository, so public adoption metrics are early. The project is being positioned
around ecosystem importance rather than existing scale: AI agents need local, deterministic privacy
guardrails before medical text is passed into model contexts. `phi-guard-mcp` provides that boundary
as a small composable MCP server and CLI, with synthetic evals and CI workflows that other
maintainers can inspect and extend.

## Application Safety Notes

- Do not claim HIPAA compliance.
- Do not claim clinical validation.
- Do not claim diagnosis, treatment, triage, or clinical decision support.
- Do not include private OpenAI account, billing, org, or email details in this repository.
