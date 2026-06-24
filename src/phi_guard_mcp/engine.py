"""Transparent rule-based PHI-like identifier detection."""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from re import Pattern

from .models import (
    SAFE_HARBOR_IDENTIFIERS,
    AuditReport,
    Finding,
    PHICategory,
    RedactionMode,
    RedactionResult,
    ScanResult,
    ValidationResult,
)


@dataclass(frozen=True)
class Rule:
    rule_id: str
    category: PHICategory
    pattern: Pattern[str]
    confidence: float
    group: str | None = None


MONTH_PATTERN = (
    r"Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|"
    r"Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?"
)


RULES: tuple[Rule, ...] = (
    Rule(
        rule_id="email.basic",
        category="EMAIL",
        pattern=re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
        confidence=0.99,
    ),
    Rule(
        rule_id="ssn.us",
        category="SSN",
        pattern=re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        confidence=0.98,
    ),
    Rule(
        rule_id="phone.us",
        category="PHONE",
        pattern=re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}(?!\d)"),
        confidence=0.92,
    ),
    Rule(
        rule_id="url.http",
        category="URL",
        pattern=re.compile(r"\bhttps?://[^\s)>\"\]`']+", re.IGNORECASE),
        confidence=0.97,
    ),
    Rule(
        rule_id="ip.v4",
        category="IP_ADDRESS",
        pattern=re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        confidence=0.90,
    ),
    Rule(
        rule_id="mrn.labeled",
        category="MRN",
        pattern=re.compile(
            r"\b(?:MRN|Medical[ \t]+Record(?:[ \t]+Number)?|Record[ \t]+No\.?)"
            r"[:# \t-]*(?P<phi>(?=[A-Z0-9-]*\d)[A-Z0-9][A-Z0-9-]{3,})\b",
            re.IGNORECASE,
        ),
        confidence=0.96,
        group="phi",
    ),
    Rule(
        rule_id="account.labeled",
        category="ACCOUNT_ID",
        pattern=re.compile(
            r"\b(?:Account|Acct|Patient[ \t]+ID|Member[ \t]+ID|Policy)"
            r"[:# \t-]*(?P<phi>(?=[A-Z0-9-]*\d)[A-Z0-9][A-Z0-9-]{3,})\b",
            re.IGNORECASE,
        ),
        confidence=0.90,
        group="phi",
    ),
    Rule(
        rule_id="date.iso_or_us",
        category="DATE",
        pattern=re.compile(r"\b(?:\d{4}[/-]\d{1,2}[/-]\d{1,2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b"),
        confidence=0.90,
    ),
    Rule(
        rule_id="date.month_name",
        category="DATE",
        pattern=re.compile(rf"\b(?:{MONTH_PATTERN})\s+\d{{1,2}},\s+\d{{4}}\b", re.IGNORECASE),
        confidence=0.90,
    ),
    Rule(
        rule_id="address.street",
        category="ADDRESS",
        pattern=re.compile(
            r"\b\d{1,6}\s+[A-Z][A-Za-z0-9.'-]*"
            r"(?:\s+[A-Z][A-Za-z0-9.'-]*){0,4}\s+"
            r"(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive|Lane|Ln|Way|Court|Ct)\b",
            re.IGNORECASE,
        ),
        confidence=0.82,
    ),
    Rule(
        rule_id="facility.named",
        category="MEDICAL_FACILITY",
        pattern=re.compile(
            r"\b[A-Z][A-Za-z&.'-]*(?:[ \t]+[A-Z][A-Za-z&.'-]*){0,4}[ \t]+"
            r"(?:Hospital|Clinic|Medical[ \t]+Center|Health[ \t]+System|Urgent[ \t]+Care)\b"
        ),
        confidence=0.82,
    ),
    Rule(
        rule_id="name.clinical_label",
        category="NAME",
        pattern=re.compile(
            r"\b(?:Patient[ \t]+Name|Name|Patient|Provider|Physician)[:# \t-]+"
            r"(?P<phi>[A-Z][a-z]+(?:[ \t]+[A-Z][a-z]+){1,2})\b"
        ),
        confidence=0.84,
        group="phi",
    ),
)

PLACEHOLDERS: dict[PHICategory, str] = {
    "NAME": "[NAME]",
    "DATE": "[DATE]",
    "PHONE": "[PHONE]",
    "EMAIL": "[EMAIL]",
    "ADDRESS": "[ADDRESS]",
    "MRN": "[MRN]",
    "SSN": "[SSN]",
    "URL": "[URL]",
    "IP_ADDRESS": "[IP_ADDRESS]",
    "MEDICAL_FACILITY": "[MEDICAL_FACILITY]",
    "ACCOUNT_ID": "[ACCOUNT_ID]",
}


def scan_text(text: str) -> ScanResult:
    """Scan plain text for PHI-like identifiers."""

    findings = _deduplicate_findings(_collect_findings(text))
    return ScanResult(
        text_length=len(text),
        findings=findings,
        summary=_summarize(findings),
    )


def redact_text(text: str, mode: RedactionMode = "placeholder") -> RedactionResult:
    """Redact detected PHI-like identifiers with stable placeholders."""

    if mode != "placeholder":
        raise ValueError("Only placeholder redaction is supported in v0.1.0.")

    scan = scan_text(text)
    redacted = text
    for finding in sorted(scan.findings, key=lambda item: item.start, reverse=True):
        redacted = redacted[: finding.start] + PLACEHOLDERS[finding.category] + redacted[finding.end :]

    return RedactionResult(
        mode=mode,
        redacted_text=redacted,
        findings=scan.findings,
        summary=scan.summary,
    )


def audit_text(text: str) -> AuditReport:
    """Return an audit-oriented summary of PHI-like identifiers."""

    scan = scan_text(text)
    return AuditReport(
        text_length=scan.text_length,
        total_findings=len(scan.findings),
        categories=scan.summary,
        findings=scan.findings,
        safe_harbor_notes=[
            "This report can support common identifier review, but it is not a full "
            "Safe Harbor determination.",
            "Manual review is required before using output in a regulated environment.",
        ],
        limitations=[
            "Rule-based matching can miss identifiers and can produce false positives.",
            "This package does not provide diagnosis, treatment, triage, CDS, or HIPAA compliance.",
            "Use synthetic or properly authorized text only.",
        ],
    )


def validate_no_phi(text: str) -> ValidationResult:
    """Validate whether text contains detected PHI-like identifiers."""

    scan = scan_text(text)
    has_phi = bool(scan.findings)
    return ValidationResult(
        ok=not has_phi,
        has_phi=has_phi,
        message="No PHI-like identifiers detected." if not has_phi else "PHI-like identifiers detected.",
        findings=scan.findings,
        summary=scan.summary,
    )


def _collect_findings(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for rule in RULES:
        for match in rule.pattern.finditer(text):
            if rule.category == "IP_ADDRESS" and not _is_valid_ipv4(match.group(0)):
                continue

            start, end = match.span(rule.group) if rule.group else match.span()
            value = text[start:end]
            if not value.strip():
                continue

            findings.append(
                Finding(
                    category=rule.category,
                    text=value,
                    start=start,
                    end=end,
                    confidence=rule.confidence,
                    rule_id=rule.rule_id,
                    safe_harbor_identifier=SAFE_HARBOR_IDENTIFIERS[rule.category],
                )
            )
    return findings


def _deduplicate_findings(findings: list[Finding]) -> list[Finding]:
    ordered = sorted(
        findings,
        key=lambda item: (
            item.start,
            -(item.end - item.start),
            -item.confidence,
            item.category,
            item.rule_id,
        ),
    )
    selected: list[Finding] = []
    occupied: list[tuple[int, int]] = []

    for finding in ordered:
        if any(_overlaps((finding.start, finding.end), existing) for existing in occupied):
            continue
        selected.append(finding)
        occupied.append((finding.start, finding.end))

    return sorted(selected, key=lambda item: (item.start, item.end, item.category, item.rule_id))


def _overlaps(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[0] < right[1] and right[0] < left[1]


def _summarize(findings: list[Finding]) -> dict[str, int]:
    counts = Counter(finding.category for finding in findings)
    return dict(sorted(counts.items()))


def _is_valid_ipv4(value: str) -> bool:
    parts = value.split(".")
    return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)
