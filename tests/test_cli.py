import json
from pathlib import Path

import pytest

from phi_guard_mcp.cli import main


def test_help(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--help"]) == 0
    output = capsys.readouterr().out

    assert "phi-guard" in output
    assert "scan" in output


def test_version(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--version"]) == 0
    assert "phi-guard 0.1.1" in capsys.readouterr().out


def test_scan_outputs_json(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "note.txt"
    source.write_text("Patient Name: Jordan Rivera\nEmail: jordan.rivera@example.invalid\n", encoding="utf-8")

    assert main(["scan", str(source)]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["ok"] is True
    assert payload["summary"]["NAME"] == 1
    assert payload["summary"]["EMAIL"] == 1


def test_redact_writes_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "note.txt"
    output = tmp_path / "redacted.txt"
    source.write_text("MRN: MRN-48291\nPhone: (415) 555-0198\n", encoding="utf-8")

    assert main(["redact", str(source), "--out", str(output)]) == 0
    payload = json.loads(capsys.readouterr().out)
    redacted = output.read_text(encoding="utf-8")

    assert payload["summary"]["MRN"] == 1
    assert payload["summary"]["PHONE"] == 1
    assert "MRN-48291" not in redacted
    assert "(415) 555-0198" not in redacted
    assert "[MRN]" in redacted


def test_audit_outputs_category_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "note.txt"
    source.write_text("SSN: 123-45-6789\nDOB: 1980-04-12\n", encoding="utf-8")

    assert main(["audit", str(source)]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["total_findings"] == 2
    assert payload["categories"]["SSN"] == 1
    assert payload["categories"]["DATE"] == 1


def test_validate_exit_code(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "note.txt"
    source.write_text("Patient Name: Jordan Rivera\n", encoding="utf-8")

    assert main(["validate", str(source)]) == 1
    payload = json.loads(capsys.readouterr().out)

    assert payload["ok"] is False
    assert payload["has_phi"] is True


def test_benchmark_outputs_metrics_and_writes_report(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    report_path = tmp_path / "benchmark-report.json"

    assert main(["benchmark", "benchmarks/synthetic/cases", "--out", str(report_path)]) == 0
    payload = json.loads(capsys.readouterr().out)
    written = json.loads(report_path.read_text(encoding="utf-8"))

    assert payload["total_cases"] == 20
    assert payload["f1"] == 1.0
    assert written["total_cases"] == 20


def test_gate_clean_repo_config_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["gate", "--config", ".phi-guard.toml"]) == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload["ok"] is True


def test_gate_path_with_phi_exits_one(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (tmp_path / "leak.md").write_text("Patient Name: Jordan Rivera\n", encoding="utf-8")

    assert main(["gate", str(tmp_path)]) == 1
    payload = json.loads(capsys.readouterr().out)

    assert payload["ok"] is False
    assert payload["flagged_files"] == 1
