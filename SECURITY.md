# Security Policy

`phi-guard-mcp` is a local, rule-based privacy guardrail for developer workflows. It is not a HIPAA
compliance guarantee, legal review, clinical decision support system, or medical device software.

## Supported Versions

The latest released version receives security and privacy fixes.

| Version | Supported |
| --- | --- |
| 0.1.x | Yes |

## Reporting a Vulnerability

Do not include real patient data, secrets, credentials, or private infrastructure details in a
public GitHub issue.

If the issue can be described with synthetic data, open a GitHub issue and mark it as a security or
privacy concern. If the report requires sensitive details, contact the maintainer through GitHub and
request a private reporting path before sharing details.

Useful reports include:

- False negatives where PHI-like identifiers are not detected.
- False positives that make safe text unusable.
- Redaction output that leaks original identifiers.
- MCP tool behavior that could expose sensitive text unexpectedly.
- Packaging or dependency issues with security impact.

## Data Handling

- Use synthetic examples only.
- Do not test with real patient records.
- Do not upload real PHI into GitHub issues, pull requests, logs, screenshots, or benchmark cases.
- Treat Safe Harbor mapping fields as review aids, not compliance determinations.
