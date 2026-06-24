import json
from pathlib import Path

from phi_guard_mcp import evaluate_benchmark
from phi_guard_mcp.models import SAFE_HARBOR_IDENTIFIERS


def test_packaged_synthetic_benchmark_is_perfect() -> None:
    report = evaluate_benchmark("benchmarks/synthetic/cases")

    assert report.total_cases == 20
    assert report.false_positive == 0
    assert report.false_negative == 0
    assert report.precision == 1.0
    assert report.recall == 1.0
    assert report.f1 == 1.0
    assert "MRN" in report.per_category


def test_benchmark_reports_false_positive_and_false_negative(tmp_path: Path) -> None:
    cases_dir = tmp_path / "cases"
    cases_dir.mkdir()
    _write_case(
        cases_dir / "case_001.json",
        "case_001",
        "Patient Name: Jordan Rivera",
        [{"category": "NAME", "text": "Jordan Rivera"}],
    )
    _write_case(cases_dir / "case_002.json", "case_002", "Phone: 415-555-0198", [])
    _write_case(
        cases_dir / "case_003.json",
        "case_003",
        "No direct identifiers in this note.",
        [{"category": "EMAIL", "text": "missing@example.invalid"}],
    )

    report = evaluate_benchmark(cases_dir)

    assert report.true_positive == 1
    assert report.false_positive == 1
    assert report.false_negative == 1
    assert report.precision == 0.5
    assert report.recall == 0.5
    assert report.f1 == 0.5
    assert report.cases[1].unexpected[0].category == "PHONE"
    assert report.cases[2].missing[0].category == "EMAIL"


def test_safe_harbor_mapping_covers_all_categories() -> None:
    assert set(SAFE_HARBOR_IDENTIFIERS) == {
        "NAME",
        "DATE",
        "PHONE",
        "EMAIL",
        "ADDRESS",
        "MRN",
        "SSN",
        "URL",
        "IP_ADDRESS",
        "ACCOUNT_ID",
        "MEDICAL_FACILITY",
    }
    assert SAFE_HARBOR_IDENTIFIERS["MRN"] == "Medical record numbers"


def _write_case(path: Path, case_id: str, text: str, expected_findings: list[dict[str, str]]) -> None:
    path.write_text(
        json.dumps(
            {
                "id": case_id,
                "text": text,
                "expected_findings": expected_findings,
            }
        ),
        encoding="utf-8",
    )
