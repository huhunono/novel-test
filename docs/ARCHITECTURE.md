# Architecture

## 1. Overview

This project is an API-first automation testing platform built for a novel reading backend.
It is structured as a multi-layer system where each layer has a single, bounded responsibility.
The platform is designed to support both fast PR-gate feedback and deep nightly regression,
with CI/CD pipelines as first-class citizens rather than an afterthought.

---

## 2. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        CI/CD Layer                               │
│            PR Gate (pr-gate.yml) + Nightly (nightly.yml)         │
└──────────────────────────────┬───────────────────────────────────┘
                               │ triggers
┌──────────────────────────────▼───────────────────────────────────┐
│                        Test Layer                                │
│         smoke / contract / reg_ci / regression (pytest)          │
└──────────┬───────────────────────────────────────┬──────────────┘
           │ uses fixtures (conftest.py)            │ reads
┌──────────▼──────────┐                 ┌──────────▼──────────────┐
│    Client Layer     │                 │    Test Data Layer       │
│  BookClient         │                 │  users.py / books.py     │
│  UserClient         │                 │  generators.py           │
│  NewsClient         │                 └─────────────────────────┘
│  BaseClient         │
└──────────┬──────────┘
           │ HTTP (requests.Session)
┌──────────▼──────────┐
│  Validation Layer   │
│  response_validator │
│  schema_validator   │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│    Backend API      │
│  Spring Boot :8083  │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│     Database        │
│  MySQL (novel_plus) │
└─────────────────────┘

┌─────────────────────────────────┐
│     AI Assist Layer  [planned]  │
│  scripts/analyze_failures.py    │
│  requirements-ai.txt            │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│  UI Validation Layer [planned]  │
│  Playwright smoke (optional)    │
└─────────────────────────────────┘
```

---

## 3. Layer Responsibilities

### Client Layer
`clients/`

**Purpose:** Encapsulate all HTTP communication behind domain-scoped interfaces.

**Responsibilities:**
- `BaseClient` owns the `requests.Session`, base URL construction, and header management
- `BookClient`, `UserClient`, `NewsClient` expose business-meaningful method signatures
- All clients accept `**kwargs` and pass them through to the underlying session call

**Does not own:** assertions, schema definitions, test data, fixture lifecycle

---

### Validation Layer
`validators/`

**Purpose:** Provide reusable, composable assertion functions decoupled from test logic.

**Responsibilities:**
- `response_validator.py` — HTTP status, Content-Type, JSON parseability, envelope assertions (`ok`, `code`)
- `schema_validator.py` — wraps `jsonschema.validate()` with structured error output (path + rule)
- `assert_response_with_schema()` — single-call full contract validation for contract tests
- `tests/utils/assertions.py` — backward-compatible re-export shim; contains no logic

**Does not own:** schema definitions, HTTP execution, test data

---

### Schema Layer
`schemas/`

**Purpose:** Define the expected shape of API responses as composable JSON Schema dicts.

**Responsibilities:**
- `schemas/base/response.py` — universal envelope schema (`ok`, `code`, `msg`, `data`)
- `schemas/common/pagination.py` — reusable factory function for paginated response structures
- `schemas/data/` — field-level schemas per domain object (BookDetail, UserInfo, etc.)
- `schemas/endpoints/` — composed endpoint schemas (envelope + data) used directly in contract tests

**Does not own:** validation execution, test assertions, HTTP concerns

---

### Test Data Layer
`tests/data/`

**Purpose:** Supply test inputs without coupling test logic to data construction.

**Responsibilities:**
- `users.py` — stable credentials read from env vars with local fallback defaults
- `books.py` — stable book ID constants used across multiple test suites
- `generators.py` — dynamic unique-per-run data (comments, usernames, emails, phone numbers)

**Does not own:** fixture lifecycle, DB seeding, assertions

---

### Test Layer
`tests/`

**Purpose:** Express test intent clearly; delegate mechanics to lower layers.

**Responsibilities:**

| Suite | Scope | Runs in |
|---|---|---|
| `smoke/` | Availability check — HTTP 200 + ok=True | PR Gate + Nightly |
| `contract/` | Schema validation — response shape stability | PR Gate + Nightly |
| `reg_ci/` | P0 business flows — deterministic, state-safe | PR Gate + Nightly |
| `regression/` | Full business validation — cross-API, boundary, negative | Nightly only |

`conftest.py` owns fixture lifecycle: session-scoped auth token, client instantiation, DB connection.

**Does not own:** HTTP mechanics, schema definitions, assertion implementations

---

### CI/CD Layer
`.github/workflows/`

**Purpose:** Automate the full test execution lifecycle from backend build to artifact upload.

**Responsibilities:**
- `pr-gate.yml` — triggered on push/PR; runs smoke + contract + reg_ci; fast-fail with `--maxfail=1`
- `nightly.yml` — triggered on schedule + manual dispatch; runs full suite; collects Allure results
- Both workflows own: backend checkout, Maven build, Docker Compose lifecycle, readiness check, teardown

**Does not own:** test logic, schema definitions, assertion implementations

---

### AI Assist Layer *(planned)*
`ai_assist/` — not yet implemented

**Planned purpose:** Analyze `report.json` from nightly runs to surface failure patterns,
classify failures by type, and generate triage summaries.

**Planned responsibilities:**
- Parse `pytest-json-report` output
- Classify failures (infra / data / contract / regression)
- Generate human-readable triage report

---

### Documentation Layer
`docs/`

**Purpose:** Capture design decisions, strategy, and roadmap in a form that outlasts code comments.

**Responsibilities:**
- `ARCHITECTURE.md` — this document; system design and layer boundaries
- `TEST_STRATEGY.md` — testing philosophy, layer selection criteria, CI strategy
- `PROJECT_ROADMAP.md` — phase-by-phase implementation plan

---

## 4. Request Flow

A typical authenticated test execution follows this path:

```
1. pytest collects test
2. conftest.py resolves fixtures:
   a. base_url  ← os.getenv("BASE_URL")
   b. auth_token ← POST /user/login (session-scoped, cached)
   c. user_client ← UserClient(BaseClient(base_url, auth_header))

3. Test calls: user_client.user_info()
4. UserClient calls: self._client.get("/user/userInfo")
5. BaseClient sends: GET http://localhost:8083/user/userInfo
                     Authorization: <token>

6. Backend returns: HTTP 200, application/json, {ok, code, msg, data}

7. Test calls: body = assert_json_response(resp)
   → validates status code, Content-Type, JSON parseability

8. Test calls: assert_ok_true(body)
   → validates envelope ok=True

9. [contract tests only]: validate_schema(body, SCHEMA)
   → validates response shape against JSON Schema dict

10. [reg_ci / regression only]: optional DB assertion
    db_one(db_conn, "SELECT ...") → verifies state at DB level
```

---

## 5. Design Principles

**API-first over UI-first**
Backend API contracts are more stable and faster to test than UI rendering.
UI layer is optional and planned only as a lightweight smoke supplement.

**Thin client pattern**
Clients translate business intent into HTTP calls and nothing else.
They do not assert, parse business logic, or manage state.
This keeps clients reusable across test suites and test types.

**Validation reuse**
All assertion logic lives in `validators/`, not in individual test files.
Tests express *what* to verify; validators express *how* to verify it.
This prevents assertion drift across 38 test files.

**Test data separation**
Static constants and dynamic generators are isolated in `tests/data/`.
Test files never construct test data inline.
This makes data dependencies explicit and refactorable.

**Schema composition over duplication**
`BASE_RESPONSE_SCHEMA` and `pagination_schema()` are composed into endpoint schemas.
Changing the envelope structure requires one edit, not 10.

**PR Gate for fast feedback, Nightly for deep validation**
PR Gate runs a deterministic, state-safe subset (`reg_ci`) to keep merge cycles fast.
Nightly runs the full suite including stateful, cross-API regression tests.
This split prevents flaky regression tests from blocking PRs.

---

## 6. Current State vs Planned Expansion

### Implemented

| Layer | Status |
|---|---|
| Client Layer (3 domain clients + BaseClient) | ✅ Complete |
| Validation Layer (response + schema validators) | ✅ Complete |
| Schema Layer (base + data + endpoint schemas) | ✅ Complete |
| Test Data Layer (static constants + generators) | ✅ Complete |
| Test Layer (smoke + contract + reg_ci + regression) | ✅ Complete |
| DB validation fixtures | ✅ Complete |
| PR Gate workflow | ✅ Complete |
| Nightly workflow + Allure artifact | ✅ Complete |

### Planned

| Layer | Status | Phase |
|---|---|---|
| AI Assist — failure triage (`analyze_failures.py`) | 🔲 Planned | Phase 4 |
| UI Validation — Playwright smoke | 🔲 Optional | Phase 5 |
| `docs/TEST_STRATEGY.md` | 🔲 Planned | Phase 3 |
| `docs/PROJECT_ROADMAP.md` | 🔲 Planned | Phase 3 |
