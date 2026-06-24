# Safety Scope

`phi-guard-mcp` is a privacy guardrail for developer workflows that handle synthetic or already
authorized medical text. It detects PHI-like identifiers, redacts them with placeholders, and returns
structured audit data before text is sent to an AI agent.

## In Scope

- Plain text, Markdown, and JSON source text scanning.
- Local rule-based PHI-like identifier detection.
- Placeholder redaction.
- JSON audit summaries for developer review.
- MCP tools for agent workflows that need privacy checks before forwarding text.

## Out of Scope

- Diagnosis, treatment, triage, prognosis, or medication recommendations.
- Patient-specific clinical decision support.
- Claims of HIPAA compliance, regulatory certification, or legal sufficiency.
- Expert Determination services.
- PDF parsing, OCR, DICOM, FHIR ingestion, or EHR integration.
- External API calls or LLM-based PHI judgment in the v0.1.0 core.

## Regulatory Boundary

This project references public regulatory concepts only to explain scope. It is not legal advice.

HHS describes two approaches for de-identifying protected health information under HIPAA: Expert
Determination and Safe Harbor. `phi-guard-mcp` does not claim to perform either approach completely;
it helps identify and redact common PHI-like identifiers as one engineering control.

FDA guidance describes risk-based treatment of software functions, including clinical decision
support and device software. `phi-guard-mcp` intentionally avoids patient-specific clinical
recommendations and only provides privacy-oriented text processing.

References:

- HHS HIPAA de-identification guidance: https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html
- FDA Clinical Decision Support Software guidance: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software
- FDA device software functions: https://www.fda.gov/medical-devices/digital-health-center-excellence/device-software-functions-including-mobile-medical-applications

## Data Handling

- Use synthetic notes for development and tests.
- Do not commit real patient records.
- Do not rely on this package as the only privacy review step.
- Review findings manually before sharing redacted content externally.
