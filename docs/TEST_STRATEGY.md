# Test Strategy

## 1. Philosophy

This platform applies **risk-based, layered testing** rather than exhaustive coverage.
The goal is to maximize defect detection at the earliest possible stage while keeping
CI execution fast and deterministic. Every test exists because of a concrete risk,
not because of a coverage target.

Core principle: **the cost of a failing PR gate must be lower than the cost of a
production regression.** This shapes every layer boundary and CI trigger decision.

---

## 2. Test Layer Design

### Why Four Layers

A single test suite cannot satisfy both fast feedback (PR) and deep validation (Nightly).
Each layer answers a different question:

| Layer | Question answered | Max acceptable runtime |
|---|---|---|
| **Smoke** | Is the service reachable? | Seconds |
| **Contract** | Did the API shape change? | < 1 min |
| **reg_ci** | Are P0 business flows broken? | < 3 min |
| **Regression** | Are business invariants holding? | No hard limit |

### Layer Boundaries

**Smoke** (`tests/smoke/`)
- Only asserts HTTP 200 + `ok=True`
- No schema enforcement, no cross-API calls
- Read-only endpoints preferred
- If smoke fails, all other layers are irrelevant — the service is down

**Contract** (`tests/contract/`)
- Validates response structure against JSON Schema dicts in `schemas/endpoints/`
- Does not assert business correctness (field values, state transitions)
- Catches breaking changes that would silently corrupt consumers
- Schema composition (`BASE_RESPONSE_SCHEMA` + domain schemas) ensures envelope
  changes propagate to all contracts automatically

**reg_ci** (`tests/reg_ci/`)
- Minimal, deterministic subset of P0 business scenarios
- Explicitly designed to be state-safe: pre-cleans state before run, uses `try/finally` cleanup
- No large data setup, no non-deterministic dependencies
- Runs on every PR — must never be flaky
- Example: `test_reg_ci_bookshelf_minimal_flow` — Add → QueryTrue → Remove → QueryFalse

**Regression** (`tests/regression/`)
- Full business validation: scenario-based, equivalence partitioning, boundary value analysis
- Includes cross-API consistency checks, negative paths, security edge cases
- May have known failures documented as `xfail` (see section 5)
- Runs Nightly only — not suitable for PR gate due to complexity and runtime

---

## 3. CI/CD Strategy

### PR Gate (`pr-gate.yml`)

```
Trigger:   push or pull_request → main / develop
Runs:      smoke → contract → reg_ci
Behavior:  --maxfail=1 per suite (fail fast)
Goal:      Catch regressions before merge; keep loop under 10 minutes
Artifact:  report.json
```

**Why `--maxfail=1`:** A broken smoke means the service is unreachable.
Running contract tests against a dead service produces noise, not signal.
Each layer fails independently and stops immediately.

**What is excluded from PR Gate:**
- `tests/regression/` — stateful, cross-API flows that are too slow and occasionally flaky
- Any test marked `@pytest.mark.regression` — by convention, not run in PR gate

### Nightly (`nightly.yml`)

```
Trigger:   schedule (02:00 CST) + workflow_dispatch
Runs:      smoke → contract → reg_ci → regression
Behavior:  continue-on-error per suite (collect full results)
Goal:      Deep validation; surface failure trends via Allure
Artifact:  allure-results/ (14 days) + report.json
```

**Why `continue-on-error`:** Nightly exists to collect a complete picture.
Stopping at first failure would hide downstream failures that could be
independent regressions. Allure aggregates all results for triage.

---

## 4. Test Data Strategy

### Static Constants (`tests/data/books.py`, `users.py`)
Used where the same resource is referenced across multiple suites.
IDs are documented with which test files depend on them.
Credentials read from env vars with local fallback defaults.

```python
BOOK_ID_DETAIL: int = 2010824442059300864  # smoke + contract + reg_ci + regression
BOOK_ID_SHELF_CI: str = "2010826914387599360"  # reg_ci bookshelf flow only
```

### Dynamic Generators (`tests/data/generators.py`)
Used where static data would cause duplicate-entry errors across runs.
Implemented with stdlib only (`time` + `random` + `string`) — no external dependencies.

```python
unique_comment()   # "cmt-1711234567890-a3kz" — used in regression comment flow
unique_username()  # "usr_a3kz9f"            — available for future registration tests
```

### DB Validation (`tests/utils/db_helpers.py`)
Some state transitions cannot be verified through the API alone.
`db_one()` and `db_all()` provide direct SQL validation via the `db_conn` session fixture.
Used sparingly — only when HTTP response is insufficient to verify state.

---

## 5. Known Issues and xfail Policy

`@pytest.mark.xfail` is used when a test exposes a **known backend defect or inconsistency**
that is documented but not yet fixed. The intent is to:
1. Keep the test in the suite (preserves intent and will catch the fix automatically)
2. Prevent the known issue from blocking CI
3. Provide a permanent record of the defect in test code

Current xfail cases:

| Test | Reason |
|---|---|
| `test_reg_bookshelf_consistency_nonexistent_bookId_query_true_but_not_in_list` | Backend accepts non-existent bookId; `queryIsInShelf=true` but book absent from list page — inconsistent contract |
| `test_reg_comment_add_then_visible_in_list` | Comment feature disabled server-side (`code=3001`) |

**xfail convention:**
- Always include `reason=` with a clear description
- Use `strict=False` unless the failure mode is 100% predictable
- Remove xfail when the backend fix is confirmed

---

## 6. Out-of-Scope APIs

The following API groups are intentionally excluded from all test layers:

| API Group | Reason |
|---|---|
| `/pay/*` Payment APIs | External gateway dependency; async callbacks; high flakiness risk |
| Author / CMS APIs | Do not affect core reader flow; high change frequency |

Exclusion is a deliberate risk decision, not an oversight.

---

## 7. Observability

- **`pytest-json-report`** generates `report.json` per Nightly run — machine-readable,
  intended as input for future AI triage (`ai_assist/`, Phase 4)
- **`allure-pytest`** generates `allure-results/` per Nightly run — uploaded as artifact,
  viewable locally via `allure serve allure-results/`
- PR Gate uploads `report.json` only; Allure artifact is Nightly-only
