# Synthetic Benchmark

`phi-guard-mcp` includes a synthetic benchmark to make detector behavior measurable without using
real patient data.

Run it from the repository root:

```bash
phi-guard benchmark benchmarks/synthetic/cases --out benchmarks/synthetic-report.json
```

Each benchmark case is a JSON file with:

- `id`: stable case identifier.
- `text`: synthetic clinical-style note text.
- `expected_findings`: exact `category` and `text` pairs expected from the rule engine.

The report includes precision, recall, F1, true positives, false positives, false negatives, and
per-category metrics. Matching is intentionally strict: a finding is correct only when both category
and exact text match the expected fixture.

## Current Report

The checked-in synthetic report is generated from 20 synthetic cases:

- Precision: 1.0
- Recall: 1.0
- F1: 1.0

These numbers are expected for the current fixture set because the benchmark is a regression suite
for known synthetic examples. They should not be read as clinical validation, real-world recall, or
proof that PHI has been fully removed from arbitrary medical text.

## Limitations

- All cases are synthetic and rule-oriented.
- The benchmark does not measure performance on real patient records.
- The benchmark does not prove HIPAA compliance, Expert Determination, or legal sufficiency.
- False positives and false negatives should be reviewed through public issues using synthetic
  examples only.

The roadmap tracks expansion into harder synthetic edge cases, detector-level reporting, and a
documented review workflow for false-positive and false-negative reports.
