"""Rule-based PHI detection, redaction, audit, and validation helpers."""

from .benchmark import evaluate_benchmark
from .engine import audit_text, redact_text, scan_text, validate_no_phi
from .gate import run_gate
from .models import (
    AuditReport,
    BenchmarkReport,
    Finding,
    GateReport,
    RedactionResult,
    ScanResult,
    ValidationResult,
)

__all__ = [
    "AuditReport",
    "BenchmarkReport",
    "Finding",
    "GateReport",
    "RedactionResult",
    "ScanResult",
    "ValidationResult",
    "audit_text",
    "evaluate_benchmark",
    "redact_text",
    "run_gate",
    "scan_text",
    "validate_no_phi",
]

__version__ = "0.1.1"
