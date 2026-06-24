# Roadmap

This roadmap tracks privacy infrastructure improvements that stay outside clinical decision support,
diagnosis, treatment, triage, medication, and compliance certification.

## v0.1.x

- Expand synthetic benchmark hard cases for names, dates, IDs, and addresses.
- Add a documented false-positive and false-negative review workflow.
- Add MCP client setup examples for common local agent clients.
- Add package installation smoke tests for released wheels.
- Add a detector rule inventory command for maintainer review.
- Add a security and privacy threat model.

## v0.2

- Add configurable redaction modes such as stable token replacement and irreversible hashing.
- Add richer benchmark reporting for detector-level precision and recall.
- Add maintainer docs for reviewing privacy-gate failures in pull requests.

## Non-Goals

- No real patient data fixtures.
- No diagnosis, treatment, triage, medication, or clinical risk scoring.
- No claim of HIPAA compliance, Expert Determination, legal sufficiency, or FDA clearance.
- No external API calls in the core rule-based engine.
