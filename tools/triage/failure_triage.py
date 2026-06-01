"""Command-line entry point for the failure triage MVP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_OUTPUT = "triage-summary.md"

# Failure classification categories
CATEGORY_KNOWN_ISSUE = "Known Issue"
CATEGORY_CONTRACT_SCHEMA = "Contract / Schema Issue"
CATEGORY_UI_ISSUE = "UI Issue"
CATEGORY_DB_DATA = "DB / Data Issue"
CATEGORY_ENVIRONMENT = "Environment Issue"
CATEGORY_FLAKY_TIMING = "Flaky / Timing Issue"
CATEGORY_TEST_BUG = "Test Bug"
CATEGORY_PRODUCT_BUG = "Product Bug"
CATEGORY_UNKNOWN = "Unknown"


def classify_failure(failure: dict[str, Any]) -> dict[str, str]:
    """Classify a test failure into a category.
    
    Args:
        failure: A dict containing nodeid, outcome, error_message, longrepr, keywords
    
    Returns:
        A dict with:
        - category: The failure category (e.g., "Known Issue", "Product Bug")
        - confidence: Classification confidence ("High", "Medium", "Low")
        - reason: Brief explanation of why this category was chosen
    """
    nodeid = failure.get("nodeid", "")
    outcome = failure.get("outcome", "")
    error_message = failure.get("error_message", "")
    longrepr = failure.get("longrepr", "")
    keywords = failure.get("keywords", [])
    
    # Combine error_message and longrepr for pattern matching
    full_error = f"{error_message} {longrepr}".lower()
    
    # Rule 1: Known Issue - tests marked as xfailed
    if outcome == "xfailed":
        return {
            "category": CATEGORY_KNOWN_ISSUE,
            "confidence": "High",
            "reason": "Test is marked xfail (expected failure)",
        }
    
    # Rule 2: Contract / Schema Issue - JSON schema validation errors
    contract_keywords = ["jsonschema", "validationerror", "schema", "application/json", "content-type"]
    if any(keyword in full_error for keyword in contract_keywords):
        return {
            "category": CATEGORY_CONTRACT_SCHEMA,
            "confidence": "High",
            "reason": "Error message contains JSON schema or content-type validation keywords",
        }
    
    # Rule 3: UI Issue - tests in tests/ui path
    if "tests/ui" in nodeid.lower():
        return {
            "category": CATEGORY_UI_ISSUE,
            "confidence": "High",
            "reason": "Test is located in tests/ui directory",
        }
    
    # Rule 4: DB / Data Issue - database related errors
    db_keywords = ["pymysql", "sqlalchemy", "database", "connection pool", "mysql", "sql"]
    if any(keyword in full_error for keyword in db_keywords):
        return {
            "category": CATEGORY_DB_DATA,
            "confidence": "High",
            "reason": "Error message contains database-related keywords",
        }
    
    # Rule 5: Environment Issue - connection and environment problems
    env_keywords = ["connection refused", "connection error", "econnrefused", "network", "timeout", "unreachable"]
    if any(keyword in full_error for keyword in env_keywords):
        return {
            "category": CATEGORY_ENVIRONMENT,
            "confidence": "Medium",
            "reason": "Error message indicates connection or environment issue",
        }
    
    # Rule 6: Flaky / Timing Issue - timeout and intermittent failures
    flaky_keywords = ["timeout", "timed out", "waitfor", "eventually", "retry"]
    if any(keyword in full_error for keyword in flaky_keywords):
        return {
            "category": CATEGORY_FLAKY_TIMING,
            "confidence": "Medium",
            "reason": "Error message suggests timing or flaky test issue",
        }
    
    # Rule 7: Test Bug - test code issues (fixtures, setup, teardown)
    test_bug_keywords = ["fixture", "setup", "teardown", "parametrize", "conftest"]
    if any(keyword in full_error for keyword in test_bug_keywords):
        return {
            "category": CATEGORY_TEST_BUG,
            "confidence": "Medium",
            "reason": "Error message indicates test infrastructure issue",
        }
    
    # Rule 8: Product Bug - assertion failures (likely real bugs)
    if outcome in ("failed", "error") and "assert" in full_error:
        return {
            "category": CATEGORY_PRODUCT_BUG,
            "confidence": "Medium",
            "reason": "Test failed with assertion error",
        }
    
    # Default: Unknown
    return {
        "category": CATEGORY_UNKNOWN,
        "confidence": "Low",
        "reason": "No classification rule matched",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a lightweight failure triage summary from pytest JSON reports."
    )
    parser.add_argument(
        "--reports",
        nargs="+",
        required=True,
        help="One or more pytest-json-report files, for example: reports/*.json",
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
    """Extract test summary counts from a pytest-json-report.
    
    Returns a dict with keys: total, passed, failed, error, xfailed, xpassed, skipped.
    """
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
    """Extract detailed information about failed/error/xfailed/xpassed tests.
    
    Returns a list of dicts, each containing:
    - nodeid: test identifier (e.g., "tests/smoke/test_login.py::test_login_success")
    - outcome: test result (failed, error, xfailed, xpassed)
    - error_message: short error message from crash.message or first line of longrepr
    - longrepr: full error traceback/representation
    - keywords: list of pytest markers/keywords
    """
    tests = report.get("tests", [])
    failures = []
    
    for test in tests:
        outcome = test.get("outcome", "")
        
        # Only extract tests that need triage
        if outcome not in ("failed", "error", "xfailed", "xpassed"):
            continue
        
        nodeid = test.get("nodeid", "unknown")
        keywords = test.get("keywords", [])
        
        # Extract error message
        error_message = ""
        longrepr = ""
        
        # Try to get crash message first (most concise)
        call_info = test.get("call", {})
        crash = call_info.get("crash", {})
        if crash:
            error_message = crash.get("message", "")
        
        # If no crash message, try longrepr
        if not error_message:
            longrepr_raw = call_info.get("longrepr", "")
            if longrepr_raw:
                longrepr = longrepr_raw
                # Extract first meaningful line as error message
                lines = longrepr_raw.split("\n")
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith("_") and not line.startswith("="):
                        error_message = line[:200]  # Limit to 200 chars
                        break
        
        # Fallback: use outcome as message
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
    """Generate a Markdown summary from parsed reports."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True) if output.parent != Path(".") else None

    lines = [
        "# Failure Triage Summary",
        "",
        "## Test Summary by Report",
        "",
        "| Report | Total | Passed | Failed | Error | XFailed | XPassed | Skipped |",
        "|--------|------:|-------:|-------:|------:|--------:|--------:|--------:|",
    ]

    # Aggregate totals across all reports
    totals = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "error": 0,
        "xfailed": 0,
        "xpassed": 0,
        "skipped": 0,
    }
    
    # Collect all failures across reports
    all_failures = []

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
        
        # Extract failure details from this report
        failures = extract_failure_details(report)
        for failure in failures:
            failure["report"] = report_name
            # Classify each failure (Step 4.1: framework only, returns "Unknown")
            classification = classify_failure(failure)
            failure["category"] = classification["category"]
            failure["confidence"] = classification["confidence"]
            failure["reason"] = classification["reason"]
        all_failures.extend(failures)

    # Add totals row
    lines.extend([
        f"| **Total** "
        f"| **{totals['total']}** "
        f"| **{totals['passed']}** "
        f"| **{totals['failed']}** "
        f"| **{totals['error']}** "
        f"| **{totals['xfailed']}** "
        f"| **{totals['xpassed']}** "
        f"| **{totals['skipped']}** |",
        "",
    ])

    # Add status message
    if totals["failed"] > 0 or totals["error"] > 0:
        lines.extend([
            "## Status",
            "",
            f"⚠️ **{totals['failed'] + totals['error']} test(s) failed or errored.**",
            "",
        ])
    elif totals["xfailed"] > 0:
        lines.extend([
            "## Status",
            "",
            f"✅ All tests passed. {totals['xfailed']} known issue(s) are still present (xfailed).",
            "",
        ])
    else:
        lines.extend([
            "## Status",
            "",
            "✅ All tests passed.",
            "",
        ])

    # Add failure details table if there are any failures
    if all_failures:
        lines.extend([
            "## Failure Details",
            "",
            "| Test | Outcome | Category | Report | Error Message |",
            "|------|---------|----------|--------|---------------|",
        ])
        
        for failure in all_failures:
            nodeid = failure["nodeid"]
            outcome = failure["outcome"]
            category = failure.get("category", CATEGORY_UNKNOWN)
            report = failure["report"]
            error_msg = failure["error_message"].replace("|", "\\|").replace("\n", " ")[:150]
            
            # Add emoji for outcome
            outcome_emoji = {
                "failed": "❌",
                "error": "💥",
                "xfailed": "⚠️",
                "xpassed": "⚡",
            }.get(outcome, "")
            
            lines.append(
                f"| `{nodeid}` | {outcome_emoji} {outcome} | {category} | `{report}` | {error_msg} |"
            )
        
        lines.append("")
        lines.append("_Note: Step 4.3 complete - all classification rules implemented. Categories: Known Issue, Contract/Schema, UI, DB/Data, Environment, Flaky/Timing, Test Bug, Product Bug._")
        lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    
    # Load all reports
    reports = [load_report(path) for path in args.reports]
    
    # Generate summary
    write_summary_markdown(args.reports, reports, args.output)
    
    print(f"Failure triage summary written to {args.output}")


if __name__ == "__main__":
    main()
