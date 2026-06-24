"""Stable result models shared by the Python API, CLI, and MCP server."""

from typing import Literal

from pydantic import BaseModel, Field

PHICategory = Literal[
    "NAME",
    "DATE",
    "PHONE",
    "EMAIL",
    "ADDRESS",
    "MRN",
    "SSN",
    "URL",
    "IP_ADDRESS",
    "MEDICAL_FACILITY",
    "ACCOUNT_ID",
]

RedactionMode = Literal["placeholder"]

SAFE_HARBOR_IDENTIFIERS: dict[PHICategory, str] = {
    "NAME": "Names",
    "DATE": "All elements of dates except year",
    "PHONE": "Telephone numbers",
    "EMAIL": "Email addresses",
    "ADDRESS": "Geographic subdivisions smaller than a state",
    "MRN": "Medical record numbers",
    "SSN": "Social Security numbers",
    "URL": "Web Universal Resource Locators",
    "IP_ADDRESS": "Internet Protocol addresses",
    "ACCOUNT_ID": "Account numbers",
    "MEDICAL_FACILITY": "Other unique identifying characteristic or code",
}


class Finding(BaseModel):
    category: PHICategory
    text: str
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    confidence: float = Field(ge=0.0, le=1.0)
    rule_id: str
    safe_harbor_identifier: str


class ScanResult(BaseModel):
    ok: bool = True
    text_length: int
    findings: list[Finding]
    summary: dict[str, int]


class RedactionResult(BaseModel):
    ok: bool = True
    mode: RedactionMode
    redacted_text: str
    findings: list[Finding]
    summary: dict[str, int]


class AuditReport(BaseModel):
    ok: bool = True
    text_length: int
    total_findings: int
    categories: dict[str, int]
    findings: list[Finding]
    safe_harbor_notes: list[str]
    limitations: list[str]


class ValidationResult(BaseModel):
    ok: bool
    has_phi: bool
    message: str
    findings: list[Finding]
    summary: dict[str, int]


class ExpectedFinding(BaseModel):
    category: PHICategory
    text: str


class BenchmarkCase(BaseModel):
    id: str
    text: str
    expected_findings: list[ExpectedFinding]


class BenchmarkCaseResult(BaseModel):
    id: str
    true_positive: int = Field(ge=0)
    false_positive: int = Field(ge=0)
    false_negative: int = Field(ge=0)
    precision: float = Field(ge=0.0, le=1.0)
    recall: float = Field(ge=0.0, le=1.0)
    f1: float = Field(ge=0.0, le=1.0)
    missing: list[ExpectedFinding]
    unexpected: list[ExpectedFinding]


class BenchmarkCategoryMetrics(BaseModel):
    expected: int = Field(ge=0)
    detected: int = Field(ge=0)
    true_positive: int = Field(ge=0)
    false_positive: int = Field(ge=0)
    false_negative: int = Field(ge=0)
    precision: float = Field(ge=0.0, le=1.0)
    recall: float = Field(ge=0.0, le=1.0)
    f1: float = Field(ge=0.0, le=1.0)


class BenchmarkReport(BaseModel):
    ok: bool = True
    cases_dir: str
    total_cases: int = Field(ge=0)
    true_positive: int = Field(ge=0)
    false_positive: int = Field(ge=0)
    false_negative: int = Field(ge=0)
    precision: float = Field(ge=0.0, le=1.0)
    recall: float = Field(ge=0.0, le=1.0)
    f1: float = Field(ge=0.0, le=1.0)
    per_category: dict[str, BenchmarkCategoryMetrics]
    cases: list[BenchmarkCaseResult]


class GateFileReport(BaseModel):
    path: str
    findings: list[Finding]
    summary: dict[str, int]


class GateReport(BaseModel):
    ok: bool
    root: str
    scanned_files: int = Field(ge=0)
    flagged_files: int = Field(ge=0)
    findings: list[GateFileReport]
