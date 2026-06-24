import pytest

from phi_guard_mcp import audit_text, redact_text, scan_text, validate_no_phi

SYNTHETIC_NOTE = """Synthetic data only.

Patient Name: Jordan Rivera
DOB: 1980-04-12
MRN: MRN-48291
SSN: 123-45-6789
Phone: (415) 555-0198
Email: jordan.rivera@example.invalid
Address: 1200 Market Street
Facility: North Valley Medical Center
Patient ID: PT-7788-XY
Portal: https://portal.example.invalid/patient/PT-7788-XY
"""


def test_scan_detects_common_phi_like_categories() -> None:
    result = scan_text(SYNTHETIC_NOTE)

    assert result.ok is True
    assert result.summary["NAME"] == 1
    assert result.summary["DATE"] == 1
    assert result.summary["MRN"] == 1
    assert result.summary["SSN"] == 1
    assert result.summary["PHONE"] == 1
    assert result.summary["EMAIL"] == 1
    assert result.summary["ADDRESS"] == 1
    assert result.summary["MEDICAL_FACILITY"] == 1
    assert result.summary["ACCOUNT_ID"] == 1
    assert result.summary["URL"] == 1


def test_scan_returns_stable_findings() -> None:
    result = scan_text(SYNTHETIC_NOTE)
    starts = [finding.start for finding in result.findings]

    assert starts == sorted(starts)
    for finding in result.findings:
        assert SYNTHETIC_NOTE[finding.start : finding.end] == finding.text
        assert finding.start < finding.end
        assert 0.0 <= finding.confidence <= 1.0
        assert finding.rule_id


def test_redact_removes_original_phi_values() -> None:
    result = redact_text(SYNTHETIC_NOTE)

    for value in [
        "Jordan Rivera",
        "1980-04-12",
        "MRN-48291",
        "123-45-6789",
        "(415) 555-0198",
        "jordan.rivera@example.invalid",
        "1200 Market Street",
        "North Valley Medical Center",
        "PT-7788-XY",
        "https://portal.example.invalid/patient/PT-7788-XY",
    ]:
        assert value not in result.redacted_text

    assert "[NAME]" in result.redacted_text
    assert "[MRN]" in result.redacted_text
    assert "[URL]" in result.redacted_text


def test_validate_no_phi_passes_and_fails() -> None:
    clean = validate_no_phi("Synthetic note without direct identifiers.")
    dirty = validate_no_phi("Patient Name: Jordan Rivera")

    assert clean.ok is True
    assert clean.has_phi is False
    assert dirty.ok is False
    assert dirty.has_phi is True


def test_overlapping_matches_are_not_duplicated() -> None:
    text = "Portal: https://portal.example.invalid/patient/PT-7788-XY"
    result = scan_text(text)

    assert len(result.findings) == 1
    assert result.findings[0].category == "URL"
    assert result.findings[0].text == "https://portal.example.invalid/patient/PT-7788-XY"


def test_audit_includes_summary_and_limitations() -> None:
    report = audit_text(SYNTHETIC_NOTE)

    assert report.ok is True
    assert report.total_findings == len(report.findings)
    assert report.categories["EMAIL"] == 1
    assert report.safe_harbor_notes
    assert report.limitations


def test_unsupported_redaction_mode_errors() -> None:
    with pytest.raises(ValueError, match="Only placeholder"):
        redact_text(SYNTHETIC_NOTE, mode="hash")  # type: ignore[arg-type]
