"""Command-line entry point for the failure triage MVP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT = "triage-summary.md"

# Status layer — answers "was this expected?"
STATUS_KNOWN_ISSUE = "Known Issue"
STATUS_NEW_FAILURE = "New Failure"

# Root-cause layer — answers "why did it fail?"
CATEGORY_CONTRACT_SCHEMA = "Contract / Schema"
CATEGORY_UI_ISSUE = "UI Issue"
CATEGORY_DB_DATA = "DB / Data"
CATEGORY_ENVIRONMENT = "Environment"
CATEGORY_FLAKY_TIMING = "Flaky / Timing"
CATEGORY_TEST_BUG = "Test Bug"
CATEGORY_PRODUCT_BUG = "Product Bug"
CATEGORY_UNKNOWN = "Unknown"


def _classify_root_cause(failure: dict[str, Any]) -> dict[str, str]:
    """Determine WHY a test failed, independent of whether it was expected.

    This function only looks at error content and test location — it never
    looks at outcome (xfailed / failed / error).  That separation is what
    makes dual-layer classification possible.

    Returns a dict with category, confidence, and reason.
    """
    nodeid = failure.get("nodeid", "")
    error_message = failure.get("error_message", "")
    longrepr = failure.get("longrepr", "")

    full_error = f"{error_message} {longrepr}".lower()

    contract_keywords = [
        "jsonschema", "validationerror", "schema",
        "application/json", "content-type",
    ]
    if any(kw in full_error for kw in contract_keywords):
        return {
            "category": CATEGORY_CONTRACT_SCHEMA,
            "confidence": "High",
            "reason": "Error contains JSON schema or content-type validation keywords",
        }

    if "tests/ui" in nodeid.lower():
        return {
            "category": CATEGORY_UI_ISSUE,
            "confidence": "High",
            "reason": "Test is located in the tests/ui directory",
        }

    db_keywords = ["pymysql", "sqlalchemy", "database", "connection pool", "mysql", "sql"]
    if any(kw in full_error for kw in db_keywords):
        return {
            "category": CATEGORY_DB_DATA,
            "confidence": "High",
            "reason": "Error contains database-related keywords",
        }

    # Check environment before flaky because both may contain "timeout";
    # "connection refused" is a stronger signal for environment problems.
    env_keywords = ["connection refused", "connection error", "econnrefused", "unreachable"]
    if any(kw in full_error for kw in env_keywords):
        return {
            "category": CATEGORY_ENVIRONMENT,
            "confidence": "Medium",
            "reason": "Error indicates a connection or environment problem",
        }

    flaky_keywords = ["timed out", "waitfor", "eventually", "retry", "timeout"]
    if any(kw in full_error for kw in flaky_keywords):
        return {
            "category": CATEGORY_FLAKY_TIMING,
            "confidence": "Medium",
            "reason": "Error suggests a timing or intermittent failure",
        }

    test_bug_keywords = ["fixture", "setup", "teardown", "parametrize", "conftest"]
    if any(kw in full_error for kw in test_bug_keywords):
        return {
            "category": CATEGORY_TEST_BUG,
            "confidence": "Medium",
            "reason": "Error points to test infrastructure (fixture / setup)",
        }

    if "assert" in full_error:
        return {
            "category": CATEGORY_PRODUCT_BUG,
            "confidence": "Medium",
            "reason": "Assertion failure — likely a real product defect",
        }

    return {
        "category": CATEGORY_UNKNOWN,
        "confidence": "Low",
        "reason": "No classification rule matched",
    }


def classify_failure(failure: dict[str, Any]) -> dict[str, str]:
    """Dual-layer classification: status (was it expected?) + root cause (why?).

    Layer 1 — status:
        Known Issue  → outcome is xfailed (test is @pytest.mark.xfail)
        New Failure  → outcome is failed or error

    Layer 2 — root cause:
        Always derived from error content via _classify_root_cause().
        Applied to both Known Issues and New Failures so that every entry
        carries an actionable reason, not just a lifecycle label.

    Returns a dict with status, category, confidence, and reason.
    """
    outcome = failure.get("outcome", "")

    root = _classify_root_cause(failure)

    if outcome == "xfailed":
        status = STATUS_KNOWN_ISSUE
    elif outcome == "xpassed":
        # xpassed means a test that was expected to fail actually passed —
        # treat as a new signal worth investigating.
        status = STATUS_NEW_FAILURE
    else:
        status = STATUS_NEW_FAILURE

    return {
        "status": status,
        "category": root["category"],
        "confidence": root["confidence"],
        "reason": root["reason"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a lightweight failure triage summary from pytest JSON reports."
    )
    parser.add_argument(
        "--reports",
        nargs="+",
        required=True,
        help="One or more pytest-json-report files, e.g. reports/*.json",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Markdown output file path. Default: {DEFAULT_OUTPUT}",
    )
    return parser.parse_args()


def load_report(report_path: str) -> dict[str, Any] | None:
    """Load a single pytest-json-report file.

    Returns None if the file does not exist or cannot be parsed.
    """
    path = Path(report_path)
    if not path.exists():
        print(f"Warning: Report file not found: {report_path}")
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"Warning: Failed to parse {report_path}: {e}")
        return None


def extract_summary(report: dict[str, Any]) -> dict[str, int]:
    """Extract test result counts from a pytest-json-report summary block."""
    summary = report.get("summary", {})
    return {
        "total": summary.get("total", 0) or summary.get("collected", 0),
        "passed": summary.get("passed", 0),
        "failed": summary.get("failed", 0),
        "error": summary.get("error", 0),
        "xfailed": summary.get("xfailed", 0),
        "xpassed": summary.get("xpassed", 0),
        "skipped": summary.get("skipped", 0),
    }


def extract_failure_details(report: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract triage-relevant tests: failed, error, xfailed, xpassed."""
    failures = []

    for test in report.get("tests", []):
        outcome = test.get("outcome", "")
        if outcome not in ("failed", "error", "xfailed", "xpassed"):
            continue

        nodeid = test.get("nodeid", "unknown")
        keywords = test.get("keywords", [])
        call_info = test.get("call", {})

        error_message = ""
        longrepr = ""

        crash = call_info.get("crash", {})
        if crash:
            error_message = crash.get("message", "")

        if not error_message:
            longrepr_raw = call_info.get("longrepr", "")
            if longrepr_raw:
                longrepr = longrepr_raw
                for line in longrepr_raw.split("\n"):
                    line = line.strip()
                    if line and not line.startswith("_") and not line.startswith("="):
                        error_message = line[:200]
                        break

        if not error_message:
            error_message = f"Test {outcome}"

        failures.append({
            "nodeid": nodeid,
            "outcome": outcome,
            "error_message": error_message,
            "longrepr": longrepr,
            "keywords": keywords,
        })

    return failures


def write_summary_markdown(
    report_paths: list[str],
    reports: list[dict[str, Any]],
    output_path: str,
) -> None:
    """Generate a Markdown triage summary from one or more parsed reports."""
    output = Path(output_path)
    if output.parent != Path("."):
        output.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Failure Triage Summary",
        "",
        "## Test Summary by Report",
        "",
        "| Report | Total | Passed | Failed | Error | XFailed | XPassed | Skipped |",
        "|--------|------:|-------:|-------:|------:|--------:|--------:|--------:|",
    ]

    totals: dict[str, int] = {
        "total": 0, "passed": 0, "failed": 0, "error": 0,
        "xfailed": 0, "xpassed": 0, "skipped": 0,
    }
    all_failures: list[dict[str, Any]] = []

    for report_path, report in zip(report_paths, reports):
        if report is None:
            continue

        summary = extract_summary(report)
        report_name = Path(report_path).name

        lines.append(
            f"| `{report_name}` "
            f"| {summary['total']} "
            f"| {summary['passed']} "
            f"| {summary['failed']} "
            f"| {summary['error']} "
            f"| {summary['xfailed']} "
            f"| {summary['xpassed']} "
            f"| {summary['skipped']} |"
        )

        for key in totals:
            totals[key] += summary[key]

        for failure in extract_failure_details(report):
            failure["report"] = report_name
            classification = classify_failure(failure)
            failure.update(classification)
            all_failures.append(failure)

    lines += [
        f"| **Total** "
        f"| **{totals['total']}** "
        f"| **{totals['passed']}** "
        f"| **{totals['failed']}** "
        f"| **{totals['error']}** "
        f"| **{totals['xfailed']}** "
        f"| **{totals['xpassed']}** "
        f"| **{totals['skipped']}** |",
        "",
    ]

    if totals["failed"] > 0 or totals["error"] > 0:
        lines += [
            "## Status",
            "",
            f"⚠️ **{totals['failed'] + totals['error']} test(s) failed or errored.**",
            "",
        ]
    elif totals["xfailed"] > 0:
        lines += [
            "## Status",
            "",
            f"✅ All tests passed. {totals['xfailed']} known issue(s) still present (xfailed).",
            "",
        ]
    else:
        lines += ["## Status", "", "✅ All tests passed.", ""]

    if all_failures:
        lines += [
            "## Failure Details",
            "",
            "| Test | Outcome | Status | Root Cause | Confidence | Report | Error Message |",
            "|------|---------|--------|------------|------------|--------|---------------|",
        ]

        outcome_emoji = {
            "failed": "❌", "error": "💥", "xfailed": "⚠️", "xpassed": "⚡",
        }
        status_emoji = {
            STATUS_KNOWN_ISSUE: "🔵",
            STATUS_NEW_FAILURE: "🔴",
        }

        for f in all_failures:
            o_icon = outcome_emoji.get(f["outcome"], "")
            s_icon = status_emoji.get(f.get("status", ""), "")
            error_msg = f["error_message"].replace("|", "\\|").replace("\n", " ")[:150]

            lines.append(
                f"| `{f['nodeid']}` "
                f"| {o_icon} {f['outcome']} "
                f"| {s_icon} {f.get('status', '')} "
                f"| {f.get('category', CATEGORY_UNKNOWN)} "
                f"| {f.get('confidence', 'Low')} "
                f"| `{f['report']}` "
                f"| {error_msg} |"
            )

        lines += [
            "",
            "**Status key:** 🔵 Known Issue (xfail marker present) · 🔴 New Failure (needs immediate triage)",
            "",
            "**Root Cause key:** Contract/Schema · UI Issue · DB/Data · "
            "Environment · Flaky/Timing · Test Bug · Product Bug · Unknown",
            "",
        ]

    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    reports = [load_report(p) for p in args.reports]
    write_summary_markdown(args.reports, reports, args.output)
    print(f"Triage summary written to {args.output}")


if __name__ == "__main__":
    main()
