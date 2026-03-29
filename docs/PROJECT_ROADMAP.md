# Project Roadmap

This document tracks the implementation phases of the Novel Platform API Test Quality Platform.
It reflects the actual state of the project — completed work is only marked as such when it is
fully implemented and verified in CI.

---

## Phase 1 — Foundation
**Status: Complete**

Establish the core automation framework and test infrastructure.

- [x] Project structure and directory layout
- [x] `BaseClient` + domain clients (`BookClient`, `UserClient`, `NewsClient`)
- [x] `conftest.py` fixture system (session-scoped auth, DB connection, client injection)
- [x] `validators/` layer (`response_validator`, `schema_validator`)
- [x] `schemas/` layer (base envelope, pagination factory, endpoint schemas)
- [x] `tests/data/` layer (static constants + dynamic generators)
- [x] `tests/utils/` (DB helpers, assertion shim)
- [x] Four test layers: smoke / contract / reg_ci / regression
- [x] `pytest.ini` with marker registration and timeout config
- [x] `requirements.txt` with pinned dependencies
- [x] `.env.example` for local environment setup

---

## Phase 2 — CI/CD and Stability
**Status: Complete**

Automate test execution and integrate with backend lifecycle.

- [x] PR Gate workflow (`pr-gate.yml`): smoke + contract + reg_ci on every push/PR
- [x] Nightly workflow (`nightly.yml`): full suite including regression, daily schedule + manual trigger
- [x] Backend checkout, Maven build, and Docker Compose lifecycle in CI
- [x] Backend readiness check before test execution
- [x] `allure-results/` artifact upload per nightly run (14-day retention)
- [x] `report.json` artifact upload
- [x] `if: always()` teardown guarantees
- [x] Secrets-based credential management (no plaintext in workflow files)
- [x] `continue-on-error` strategy on nightly for full result collection

---

## Phase 3 — Documentation and Observability
**Status: Complete (core docs) / In Progress (reporting)**

Capture design decisions and improve result visibility.

- [x] `README.md` — project overview, architecture summary, CI/CD links, getting started
- [x] `docs/ARCHITECTURE.md` — layer responsibilities, request flow, design principles
- [x] `docs/TEST_STRATEGY.md` — test layer boundaries, CI strategy, xfail policy, data strategy
- [x] `docs/PROJECT_ROADMAP.md` — this document
- [ ] Allure HTML report generation and GitHub Pages publishing *(planned)*
- [ ] Stable public URL for latest nightly report *(planned)*

---

## Phase 4 — AI-Assisted Failure Triage
**Status: Planned**

Reduce manual triage time by automatically classifying and summarizing CI failures.

- [ ] `ai_assist/analyze_failures.py` — parse `report.json`, classify failures by type
- [ ] Failure categories: infra / data / contract / regression
- [ ] Summary output: human-readable triage report per nightly run
- [ ] `requirements-ai.txt` with AI-specific dependencies
- [ ] Optional: post triage summary as GitHub Actions step summary

This phase depends on Phase 3 reporting being stable.

---

## Phase 5 — UI Validation Layer
**Status: Optional / Planned**

Add a lightweight UI smoke layer for critical user-facing flows.

- [ ] Playwright-based smoke tests for P0 user journeys (login, browse, search)
- [ ] Separate `tests/ui_smoke/` directory
- [ ] Isolated from API tests — runs as an optional CI step, not part of PR Gate
- [ ] `requirements-ui.txt` with Playwright dependencies

This phase is lower priority than Phase 4 and will only proceed if API coverage
proves insufficient for catching regressions.

---

## Long-Term Direction

- Integrate with a centralized test reporting tool (Allure Server or Report Portal)
  for historical trend analysis across nightly runs
- Expand contract test coverage to include response time SLAs
- Explore mutation testing or property-based testing for high-risk business logic
- Consider parameterized environment support (staging / production read-only smoke)
