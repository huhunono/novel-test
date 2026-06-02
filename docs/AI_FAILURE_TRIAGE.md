# AI-Assisted Failure Triage

## 1. Purpose

Manual triage of CI failures is expensive. When a nightly run finishes with 6 failures across 5
test suites, an engineer must open each failure, read the stack trace, decide what kind of problem
it is, and route it to the right owner. At scale this is 10–30 minutes per run.

The triage layer automates the classification step. After every nightly run, it reads all JSON
reports, classifies each failure by root cause, and posts a structured summary directly to the
GitHub Actions UI — no artifact download required.

---

## 2. Architecture

```
Nightly Workflow
│
├─ pytest (5 suites)
│    ├─ reports/smoke-report.json
│    ├─ reports/contract-report.json
│    ├─ reports/reg-ci-report.json
│    ├─ reports/regression-report.json
│    └─ reports/ui-report.json
│
└─ tools/triage/failure_triage.py
     │
     ├─ load_report()             reads + parses each JSON file
     ├─ extract_summary()         counts total / passed / failed / xfailed
     ├─ extract_failure_details() filters to failed / error / xfailed / xpassed
     ├─ _classify_root_cause()    8 keyword rules → category + confidence
     ├─ classify_failure()        wraps root cause with status layer
     └─ write_summary_markdown()  emits triage-summary.md
          │
          ├─ uploaded as CI artifact  (triage-summary-<run_id>)
          └─ posted to GitHub Actions Summary  ($GITHUB_STEP_SUMMARY)
```

The script is intentionally a single file with no external dependencies beyond the Python
standard library. It reads `report.json` files produced by `pytest-json-report` and writes
a Markdown file. Nothing else.

---

## 3. Dual-Layer Classification

Every failure is classified on two independent axes:

### Layer 1 — Status (was this failure expected?)

| Status | Condition | Emoji |
|---|---|---|
| **Known Issue** | `outcome == "xfailed"` — test carries `@pytest.mark.xfail` | 🔵 |
| **New Failure** | `outcome == "failed"` or `"error"` or `"xpassed"` | 🔴 |

This answers: *do I need to act on this right now?*
- 🔴 New Failure → needs immediate triage
- 🔵 Known Issue → already tracked, lower urgency

### Layer 2 — Root Cause (why did it fail?)

| Category | Signal | Confidence |
|---|---|---|
| **Contract / Schema** | `content-type`, `application/json`, `jsonschema`, `validationerror`, `schema` | High |
| **UI Issue** | test `nodeid` contains `tests/ui` | High |
| **DB / Data** | `pymysql`, `sqlalchemy`, `mysql`, `database`, `connection pool` | High |
| **Environment** | `connection refused`, `econnrefused`, `unreachable`, `connection error` | Medium |
| **Flaky / Timing** | `timed out`, `timeout`, `waitfor`, `eventually`, `retry` | Medium |
| **Test Bug** | `fixture`, `setup`, `teardown`, `parametrize`, `conftest` | Medium |
| **Product Bug** | `assert` in error text (after all other rules fail to match) | Medium |
| **Unknown** | no rule matched | Low |

This answers: *what kind of problem is this, and who owns it?*

### Why two layers?

The old single-layer approach assigned `"Known Issue"` to every `xfailed` test and stopped
there. That hides the actual problem type. A test can be a *known* Contract/Schema issue or a
*known* Product Bug — these have different owners and different fix timelines.

The dual-layer design preserves both pieces of information:

```
Old:  xfailed test  →  "Known Issue"
New:  xfailed test  →  status: "Known Issue"  +  category: "Contract / Schema"
```

---

## 4. Classification Logic

The two functions that implement classification are kept strictly separated:

### `_classify_root_cause(failure)`

Looks only at `error_message`, `longrepr`, and `nodeid`. Never looks at `outcome`.
This is what makes dual-layer possible — root cause is computed independently of status.

Rules execute in priority order. The first match wins:

```
1. Contract/Schema  — content-type / schema keywords        (High confidence)
2. UI Issue         — nodeid path starts with tests/ui       (High confidence)
3. DB / Data        — database driver / SQL keywords         (High confidence)
4. Environment      — connection refused / unreachable       (Medium)
   ↑ checked before Flaky because "connection refused" is stronger than "timeout"
5. Flaky / Timing   — timeout / waitfor / retry              (Medium)
6. Test Bug         — fixture / conftest / teardown          (Medium)
7. Product Bug      — assert present (catch-all for failures)(Medium)
8. Unknown          — default when nothing matches           (Low)
```

### `classify_failure(failure)`

Calls `_classify_root_cause()` first, then wraps the result with the status layer:

```python
root = _classify_root_cause(failure)

if outcome == "xfailed":
    status = "Known Issue"
elif outcome == "xpassed":   # expected-to-fail but passed — worth investigating
    status = "New Failure"
else:
    status = "New Failure"

return {status, category, confidence, reason}
```

`xpassed` is treated as a New Failure because it means a previously broken test now passes —
this could indicate a fix landed, or a false positive in the xfail marker. Either way it
needs a human to look at it.

---

## 5. Data Flow

A concrete trace through the full pipeline for one real failure:

**Input** — one entry in `reports/regression-report.json`:

```json
{
  "nodeid": "tests/regression/book/test_reg_queryBookDetail_negative.py::test_reg_queryBookDetail_nonexistent_bookId_should_fail",
  "outcome": "xfailed",
  "call": {
    "crash": {
      "message": "AssertionError: Expected application/json content-type, got: 'text/html;charset=UTF-8'"
    }
  }
}
```

**Step 1 — `extract_failure_details()`**

Outcome is `xfailed` → included. Crash message extracted as `error_message`.

```python
{
    "nodeid": "tests/regression/book/...::test_...",
    "outcome": "xfailed",
    "error_message": "AssertionError: Expected application/json content-type, got: 'text/html;charset=UTF-8'",
    "longrepr": "...",
    "keywords": []
}
```

**Step 2 — `_classify_root_cause()`**

```python
full_error = "assertionerror: expected application/json content-type, got: 'text/html;charset=utf-8'"

# Rule 1: contract_keywords check
"application/json" in full_error  →  True  →  match
```

Returns `{"category": "Contract / Schema", "confidence": "High", "reason": "..."}`.

**Step 3 — `classify_failure()`**

```python
outcome == "xfailed"  →  status = "Known Issue"
```

Returns `{"status": "Known Issue", "category": "Contract / Schema", "confidence": "High", ...}`.

**Step 4 — `failure.update(classification)`**

The two dicts are merged. `all_failures.append(failure)` adds the fully-enriched record.

**Step 5 — `write_summary_markdown()`**

Produces one table row:

```
| test_reg_queryBookDetail_nonexistent... | ⚠️ xfailed | 🔵 Known Issue | Contract / Schema | High | regression-report.json | AssertionError: Expected application/json... |
```

**Output** — `triage-summary.md` is written, uploaded as artifact, and posted to
`$GITHUB_STEP_SUMMARY` so it appears at the top of the GitHub Actions run page without
any file download.

---

## 6. CI Integration

Three steps were added to `nightly.yml` after the JSON report upload:

```yaml
# runs after all 5 pytest suites, even if some failed
- name: Generate failure triage summary
  if: always() && hashFiles('reports/*.json') != ''
  run: |
    python tools/triage/failure_triage.py \
      --reports reports/*.json \
      --output triage-summary.md

- name: Upload triage summary
  if: always() && hashFiles('triage-summary.md') != ''
  uses: actions/upload-artifact@v4
  with:
    name: triage-summary-${{ github.run_id }}
    path: triage-summary.md
    retention-days: 14

- name: Post triage summary to GitHub Actions UI
  if: always() && hashFiles('triage-summary.md') != ''
  run: cat triage-summary.md >> $GITHUB_STEP_SUMMARY
```

Key design decisions:

- `if: always()` — triage must run even when test steps fail; its purpose is to analyze failures
- `hashFiles(...)` guard — skips gracefully if no JSON reports were generated (e.g. backend failed to start)
- `reports/*.json` glob — aggregates all 5 suite reports in one pass
- `$GITHUB_STEP_SUMMARY` — GitHub renders this Markdown at the top of the run page; zero clicks to see results

---

## 7. Output Format

The triage summary contains three sections:

**Section 1 — Test Summary by Report**

One row per JSON file, showing counts for each outcome. Useful for spotting which test
suite is the source of failures at a glance.

**Section 2 — Status**

A one-line health indicator: `✅ All tests passed` or `⚠️ N test(s) failed or errored`.

**Section 3 — Failure Details**

One row per triage-relevant test (failed / error / xfailed / xpassed):

| Column | Content |
|---|---|
| Test | Full `nodeid` — clickable reference to the test file and function |
| Outcome | Raw pytest result with emoji (⚠️ xfailed / ❌ failed / 💥 error / ⚡ xpassed) |
| Status | 🔵 Known Issue or 🔴 New Failure |
| Root Cause | Classification category from Layer 2 |
| Confidence | High / Medium / Low — reflects rule specificity |
| Report | Which JSON file this failure came from |
| Error Message | First 150 characters of the crash message |

---

## 8. Limitations and Future Work

### Current limitations

- **Rule-based only** — keyword matching cannot handle novel failure patterns not covered
  by the 8 rules. Unrecognised failures fall through to `Unknown`.
- **No historical tracking** — each run produces a standalone summary. There is no database
  or file store that accumulates results over time, so week-over-week trend analysis is
  not possible without manual comparison of artifacts.
- **Confidence is static** — `High / Medium / Low` values are hard-coded per rule, not
  derived from empirical accuracy measurements.

### Planned extensions

| Extension | Value | Effort |
|---|---|---|
| LLM-assisted classification for `Unknown` failures | Handles long-tail cases rules can't reach | Medium |
| Historical result store (SQLite or append-only JSON) | Enables trend queries: "is this failure new?" | Medium |
| Per-category owner routing | Automatically tags Contract failures as backend, Test Bug as QA | Low |
| Accuracy validation against labelled dataset | Measures rule quality; guides confidence calibration | Low |
