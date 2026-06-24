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

The benchmark is not a clinical validation study. It is a maintainer workflow for repeatable
regression checks on synthetic data.
