"""Synthetic benchmark evaluation for PHI-like identifier detection."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from .engine import scan_text
from .models import (
    BenchmarkCase,
    BenchmarkCaseResult,
    BenchmarkCategoryMetrics,
    BenchmarkReport,
    ExpectedFinding,
)

FindingKey = tuple[str, str]


def evaluate_benchmark(cases_dir: str | Path) -> BenchmarkReport:
    """Evaluate detector output against synthetic benchmark cases."""

    root = Path(cases_dir)
    case_paths = sorted(root.glob("*.json"))
    if not case_paths:
        raise ValueError(f"No benchmark case JSON files found in {root}")

    total_tp = 0
    total_fp = 0
    total_fn = 0
    case_results: list[BenchmarkCaseResult] = []
    category_counts: dict[str, Counter[str]] = defaultdict(Counter)

    for case_path in case_paths:
        case = BenchmarkCase.model_validate(json.loads(case_path.read_text(encoding="utf-8")))
        scan = scan_text(case.text)

        expected = Counter((item.category, item.text) for item in case.expected_findings)
        detected = Counter((item.category, item.text) for item in scan.findings)
        matched = expected & detected
        false_positive = detected - matched
        false_negative = expected - matched

        tp = sum(matched.values())
        fp = sum(false_positive.values())
        fn = sum(false_negative.values())
        total_tp += tp
        total_fp += fp
        total_fn += fn

        _count_categories(category_counts, "expected", expected)
        _count_categories(category_counts, "detected", detected)
        _count_categories(category_counts, "true_positive", matched)
        _count_categories(category_counts, "false_positive", false_positive)
        _count_categories(category_counts, "false_negative", false_negative)

        case_results.append(
            BenchmarkCaseResult(
                id=case.id,
                true_positive=tp,
                false_positive=fp,
                false_negative=fn,
                precision=_precision(tp, fp),
                recall=_recall(tp, fn),
                f1=_f1(tp, fp, fn),
                missing=_keys_to_findings(false_negative),
                unexpected=_keys_to_findings(false_positive),
            )
        )

    return BenchmarkReport(
        cases_dir=str(root),
        total_cases=len(case_results),
        true_positive=total_tp,
        false_positive=total_fp,
        false_negative=total_fn,
        precision=_precision(total_tp, total_fp),
        recall=_recall(total_tp, total_fn),
        f1=_f1(total_tp, total_fp, total_fn),
        per_category=_category_metrics(category_counts),
        cases=case_results,
    )


def _count_categories(
    category_counts: dict[str, Counter[str]],
    metric: str,
    values: Counter[FindingKey],
) -> None:
    for (category, _text), count in values.items():
        category_counts[category][metric] += count


def _category_metrics(category_counts: dict[str, Counter[str]]) -> dict[str, BenchmarkCategoryMetrics]:
    metrics: dict[str, BenchmarkCategoryMetrics] = {}
    for category in sorted(category_counts):
        counts = category_counts[category]
        tp = counts["true_positive"]
        fp = counts["false_positive"]
        fn = counts["false_negative"]
        metrics[category] = BenchmarkCategoryMetrics(
            expected=counts["expected"],
            detected=counts["detected"],
            true_positive=tp,
            false_positive=fp,
            false_negative=fn,
            precision=_precision(tp, fp),
            recall=_recall(tp, fn),
            f1=_f1(tp, fp, fn),
        )
    return metrics


def _keys_to_findings(values: Counter[FindingKey]) -> list[ExpectedFinding]:
    findings: list[ExpectedFinding] = []
    for category, text in sorted(values):
        findings.extend(
            ExpectedFinding(category=category, text=text)
            for _ in range(values[(category, text)])
        )
    return findings


def _precision(true_positive: int, false_positive: int) -> float:
    denominator = true_positive + false_positive
    return round(true_positive / denominator, 6) if denominator else 1.0


def _recall(true_positive: int, false_negative: int) -> float:
    denominator = true_positive + false_negative
    return round(true_positive / denominator, 6) if denominator else 1.0


def _f1(true_positive: int, false_positive: int, false_negative: int) -> float:
    precision = _precision(true_positive, false_positive)
    recall = _recall(true_positive, false_negative)
    denominator = precision + recall
    return round(2 * precision * recall / denominator, 6) if denominator else 0.0
