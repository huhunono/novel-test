# Novel Platform — API Test Quality Platform

A production-style API automation platform for a novel reading backend,
built around layered testing, JSON Schema contract validation, and a
full CI/CD pipeline (PR Gate + Nightly). Designed to reflect real-world
SDET engineering practices, not just test coverage.

---

## Key Features

- **Layered test architecture** — smoke / contract / reg_ci / regression
- **JSON Schema contract testing** — modular schema composition with `jsonschema`
- **Domain client pattern** — `BookClient`, `UserClient`, `NewsClient` encapsulate all HTTP concerns
- **Validation layer** — reusable `assert_json_response`, `assert_ok_true`, `validate_schema`
- **Test data management** — static constants (`books.py`, `users.py`) + dynamic generators (`generators.py`)
- **DB validation** — `pymysql` fixtures for state verification beyond HTTP responses
- **CI/CD pipelines** — PR Gate (fast feedback) + Nightly (full regression)
- **Observability** — Allure results artifact + pytest JSON report per run
- **AI-assisted failure triage** *(planned — Phase 4)*
- **UI validation layer** *(planned — Playwright smoke, Phase 5)*

---

## Architecture

```
┌─────────────────────────────────────────┐
│              Test Layer                 │
│  smoke / contract / reg_ci / regression │
└───────────────────┤┬───────────────────┘
                    │ pytest fixtures (conftest.py)
┌───────────────────┤│───────────────────┐
│            Client Layer                 │
│   BookClient / UserClient / NewsClient  │
│         (domain-scoped HTTP)            │
└───────────┤┬──────────────────────┘
                    │ requests.Session
┌───────────────────┤│───────────────────┐
│           Validation Layer              │
│  response_validator / schema_validator  │
└───────────┤┬──────────────────────┘
                    │
┌───────────────────┤│───────────────────┐
│            Backend API                  │
│         Spring Boot + MySQL             │
└─────────────────────────────────────────┘

Supporting layers:
  schemas/       — JSON Schema definitions (base + data + endpoints)
  tests/data/    — static constants + dynamic generators
  ai_assist/     — failure triage (planned)
```

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for full layer details.

---

## Test Strategy

| Layer | Trigger | Purpose |
|---|---|---|
| **Smoke** | PR Gate + Nightly | Fast go/no-go — service reachability |
| **Contract** | PR Gate + Nightly | Schema validation — prevent breaking changes |
| **reg_ci** | PR Gate + Nightly | P0 business flows — deterministic, state-safe |
| **Regression** | Nightly only | Full business validation — cross-API flows, boundary, negative |

**PR Gate** runs `smoke + contract + reg_ci` on every push/PR.
Fails fast with `--maxfail=1` to keep feedback loops short.

**Nightly** runs the full suite including `regression`.
All steps use `continue-on-error` to collect complete Allure results
even when individual suites have failures.

See [`docs/TEST_STRATEGY.md`](docs/TEST_STRATEGY.md) for design decisions.

---

## CI/CD

### PR Gate (`.github/workflows/pr-gate.yml`)
- **Trigger:** push or pull request → `main` / `develop`
- **Runs:** smoke → contract → reg_ci
- **Artifact:** `report.json`
- **Goal:** quality gate before merge — fast, must-pass

### Nightly (`.github/workflows/nightly.yml`)
- **Trigger:** daily schedule (02:00 CST) + `workflow_dispatch`
- **Runs:** smoke → contract → reg_ci → regression
- **Artifact:** `allure-results/` + `report.json` (14-day retention)
- **Goal:** full regression coverage + failure trend visibility

Both workflows: checkout backend repo → Maven build → `docker compose up` →
readiness check → pytest → artifact upload → `docker compose down -v`.

### Test Results

| Report | Link |
|---|---|
| Nightly workflow runs + Allure artifacts | [GitHub Actions - Nightly](https://github.com/huhunono/novel-test/actions/workflows/nightly.yml) |
| PR Gate workflow runs | [GitHub Actions - PR Gate](https://github.com/huhunono/novel-test/actions/workflows/pr-gate.yml) |

> Allure results (`allure-results/`) are uploaded as downloadable artifacts on every nightly run (14-day retention).
> To view locally: download the artifact, then run `allure serve allure-results/`.
> HTML report publishing via GitHub Pages is a planned enhancement.

---

## Project Structure

```
clients/          # Domain HTTP clients (BookClient, UserClient, NewsClient)
validators/       # Reusable assertion and schema validation functions
schemas/          # JSON Schema definitions (base / data / endpoints)
tests/
  smoke/          # Availability checks
  contract/       # Schema contract tests
  reg_ci/         # PR Gate regression subset
  regression/     # Full business regression
  data/           # Static constants + dynamic generators
  utils/          # DB helpers, assertion shims
ai_assist/        # Failure triage (planned)
docs/             # Architecture, strategy, roadmap
.github/
  workflows/
    pr-gate.yml
    nightly.yml
```

---

## Getting Started

```bash
# 1. Clone and configure environment
git clone <repo>
cp .env.example .env
# Edit .env with your local backend URL and DB credentials

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run tests
pytest tests/smoke
pytest tests/contract
pytest tests/reg_ci
pytest tests/regression
```

---

## Environment Variables

Copy `.env.example` to `.env` for local development.
In CI, all variables are injected via GitHub Actions secrets.

Key variables: `BASE_URL`, `TEST_USERNAME`, `TEST_PASSWORD`,
`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.

---

## Roadmap

See [`docs/PROJECT_ROADMAP.md`](docs/PROJECT_ROADMAP.md).
