# API Automation Test Project

This project implements a **layered API automation testing strategy**
for a novel reading platform, focusing on **stability**, **contract integrity**,
and **core business regression coverage**.

The test suite is designed to reflect **real-world automation practices**
used by QA / SDET teams, rather than exhaustive endpoint coverage.

---

## 1. Testing Goals

- Verify core APIs are **reachable and stable**
- Protect API **response contracts** from breaking changes
- Detect **critical business regressions** across key user flows
- Keep the suite **fast, reliable, and CI-friendly**

---

## 2. Testing Layers Overview

| Layer      | Purpose                               | Characteristics |
|-----------|----------------------------------------|----------------|
| Smoke     | Service availability check             | Fast, read-only, minimal assertions |
| Contract  | API response structure validation      | Schema-based, P0 endpoints only |
| Regression| Business behavior & state consistency  | Cross-API, state-changing flows |

---

## 3. Smoke Test Scope

**Principles**
- Stable and fast
- Prefer read-only APIs
- No complex business dependencies

### Included Smoke APIs

- `GET /book/listBookCategory`
- `GET /book/queryBookDetail/{bookId}`
- `GET /book/queryIndexList?bookId=`
- `GET /news/listIndexNews`
- `GET /book/listRank`
- `POST /user/login`
- `GET /user/userInfo`
- `GET /book/searchByPage`

> Smoke tests validate basic availability and response success,
> without enforcing detailed schema or business logic.

---

## 4. Contract Test Scope (Schema Validation)
**Principles:** 
- P0 externally consumed APIs, focus on structure integrity.
- Endpoint-level schemas


### 4.1 Schema Modularization & Reuse (Key Architecture)
To ensure **DRY (Don't Repeat Yourself)** principles and high maintainability, the project uses a modular schema composition strategy:

* **`BASE_RESPONSE_SCHEMA`** (`base_response.py`): The universal "envelope" for all responses, defining `code`, `ok`, `msg`, and `data`.
* **`pagination_schema()`** (`common_pagination.py`): A high-order function that wraps business models into a standard pagination structure,
including `pageNum`, `pageSize`, `total`, `list`, and `pages`.


### Covered Contract APIs

- `GET /book/listBookCategory`
- `GET /book/listRank`
- `GET /book/queryBookDetail/{bookId}`
- `GET /book/queryIndexList`
- `GET /book/searchByPage`
- `GET /news/listIndexNews`
- `POST /user/login` (token schema)
- `GET /user/userInfo`
- `GET /user/listBookShelfByPage`
- `GET /user/queryIsInShelf`

These tests ensure:
- Required fields exist
- Field types remain compatible
- Pagination structures do not break consumers

---

## 5. Regression Test Plan (In Progress)

Regression tests focus on **business-critical flows**
and **cross-API consistency**, rather than field-level assertions.

### Planned P0 Regression Scenarios

#### Authentication
- `login → userInfo` (token validity)
- `login → refreshToken → userInfo` (token refresh)

#### Bookshelf State Flow
- `addToBookShelf`
→ `queryIsInShelf == true`
→ `listBookShelfByPage` contains book
→ `removeFromBookShelf`
→ `queryIsInShelf == false`

#### Book Data Consistency
- `searchByPage → queryBookDetail(bookId)`
- `queryBookDetail(bookId) → queryIndexList(bookId)`
  (all items reference the same bookId)

#### Comment Flow
- `addBookComment (unique content)`
→ `listCommentByPage` contains new comment

> Regression tests validate **behavior and state changes**,
> not just response structure.

---

## 6. Out-of-Scope APIs

The following APIs are intentionally excluded from regression testing:

- **Payment APIs** (`/pay/*`)
  - External gateway dependency
  - Asynchronous callbacks
  - Risk of flaky tests
- **Author / CMS APIs**
  - Do not affect core reader user flow
  - Higher change frequency

Optional mock-based payment tests may be added in a separate suite.

---

## 7. Test Execution

```bash
# Run smoke tests
pytest tests/smoke

# Run contract tests
pytest tests/contract

# Run regression tests
pytest tests/regression
