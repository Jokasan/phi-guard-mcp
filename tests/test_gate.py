from pathlib import Path

from phi_guard_mcp.gate import run_gate


def test_gate_ignores_allowlisted_synthetic_fixture_paths(tmp_path: Path) -> None:
    fixture_dir = tmp_path / "benchmarks" / "synthetic" / "cases"
    fixture_dir.mkdir(parents=True)
    (fixture_dir / "case.json").write_text(
        '{"text": "Patient Name: Jordan Rivera", "expected_findings": []}',
        encoding="utf-8",
    )

    report = run_gate(tmp_path)

    assert report.ok is True
    assert report.flagged_files == 0


def test_gate_flags_phi_like_data_in_docs(tmp_path: Path) -> None:
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "leak.md").write_text("Patient Name: Jordan Rivera\n", encoding="utf-8")

    report = run_gate(tmp_path)

    assert report.ok is False
    assert report.flagged_files == 1
    assert report.findings[0].path == "docs/leak.md"
    assert report.findings[0].summary["NAME"] == 1


def test_gate_config_allows_public_reference_urls(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("Reference: https://example.invalid/public\n", encoding="utf-8")
    (tmp_path / ".phi-guard.toml").write_text(
        """
[gate]
include = ["README.md"]
exclude = []
allow_text = ["https://example.invalid/public"]
""",
        encoding="utf-8",
    )

    report = run_gate(tmp_path)

    assert report.ok is True
    assert report.scanned_files == 1
