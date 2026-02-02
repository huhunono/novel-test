# API Automation Test Project

This project implements a **layered API automation testing strategy**
for a novel reading platform, focusing on **stability**, **contract integrity**,
and **core business regression coverage**.

The test suite is designed to reflect **real-world automation practices**
used by QA / SDET teams, rather than exhaustive endpoint coverage.

---
## Test Reporting (Allure)
![Allure Report Overview](docs/images/allure1-30.png)
---

## 1. Testing Goals

- Verify core APIs are **reachable and stable**
- Protect API **response contracts** from breaking changes
- Detect **critical business regressions** across key user flows
- Keep the suite **fast, reliable, and CI-friendly**

---

## 2. Testing Layers Overview

| Layer      | Purpose                               | Characteristics |
|-----------|---------------------------------------|----------------|
| Smoke     | Service availability check            | Fast, read-only, minimal assertions |
| Contract  | API response structure validation     | Schema-based, P0 endpoints only |
| CI Regression | P0 business flow protection in CI        | Scenario-based, deterministic, state-safe |
| Regression| Business behavior & state invariants  | Cross-API flows, negative paths, boundary conditions |

---

# 3. Smoke Test Scope

Smoke tests provide a **fast go / no-go signal** for the system by validating
basic availability of **P0 user-facing APIs**.

### Principles
- **Fast & stable** (seconds-level execution)
- **Deterministic** (no flaky or environment-sensitive behavior)
- Prefer **read-only** APIs where possible
- No complex business logic or cross-API dependencies

### Included Smoke APIs

- `GET /book/listBookCategory`
- `GET /book/queryBookDetail/{bookId}`
- `GET /book/queryIndexList?bookId=`
- `GET /news/listIndexNews`
- `GET /book/listRank`
- `GET /book/searchByPage`
- `POST /user/login`
- `GET /user/userInfo`

> Smoke tests verify **service reachability and basic response success**.  
> They intentionally avoid schema enforcement, deep validation, or business rules.

---

# 4. Contract Test Scope (Schema Validation)

Contract tests ensure that **API response structures remain backward compatible**
for all consumers (UI, mobile, automation, downstream services).

### Principles
- Focus on **P0 externally consumed APIs**
- Validate **response structure**, not business correctness
- Prevent breaking changes that would cause parsing or rendering failures

---

## 4.1 Schema Modularization & Reuse (Key Architecture)

To ensure **DRY (Don't Repeat Yourself)** principles and long-term maintainability,
schemas are composed using reusable building blocks:

- **`BASE_RESPONSE_SCHEMA`** (`base_response.py`)  
  Defines the universal response envelope:
  `code`, `ok`, `msg`, `data`

- **`pagination_schema()`** (`common_pagination.py`)  
  A higher-order schema wrapper for paginated responses, enforcing:
  `pageNum`, `pageSize`, `total`, `list`, `pages`

This approach enables **consistent contract enforcement** while minimizing duplication.

---

## Covered Contract APIs

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
- Pagination contracts do not break consumers

---

# 5. CI Regression Suite (PR Gate)

The **CI Regression suite** is a **minimal, deterministic subset of regression tests**
executed on **every CI run (PR gate)**.

### Goals
- Validate **P0 business-critical paths**
- Catch **high-impact regressions early**
- Remain **fast, stable, and environment-safe**

### Explicitly Avoided
- Large data setup
- Non-deterministic dependencies
- Full combinatorial coverage

---

## CI Regression Coverage

This suite validates **core system health** and **critical user flows**:

- **`test_book_category_ci`**  
  Book category API availability and basic data sanity

- **`test_book_detail_ci`**  
  Book detail retrieval and identity consistency by `bookId`

- **`test_book_index_list_ci`**  
  Chapter index list accessibility and structural integrity

- **`test_book_rank_ci`**  
  Ranking list availability for discovery flows

- **`test_index_news_ci`**  
  Homepage news feed availability and display readiness

- **`test_user_login_ci`**  
  Authentication success and token usability

- **`test_user_bookshelf_ci`**  
  Minimal bookshelf lifecycle consistency  
  *(Add → Query True → Remove → Query False)*

---

# 6. Regression Test Plan

Regression tests validate **business correctness, state consistency, and failure handling**
across API boundaries.

They intentionally prioritize **risk-based coverage** over exhaustive permutations.

### Design Techniques
- **Scenario-based testing**
- **Equivalence partitioning**
- **Boundary value analysis**
- **Error guessing** based on common production risks

---

## 6.1 Happy Path  
### Core Business Flows (Scenario-Based)

### Authentication Flows
- `login → userInfo`
- `login → refreshToken → userInfo`

**Invariant:**  
Valid tokens must grant access to protected APIs; refreshed tokens must remain usable.

---

### Bookshelf State Flow
- `addToBookShelf`
→ `queryIsInShelf == true`
→ `listBookShelfByPage` contains book
→ `removeFromBookShelf`
→ `queryIsInShelf == false`

**Invariant:**  
Bookshelf state must remain consistent across all related APIs.

---

### Bookshelf Idempotency Rule

- `addToBookShelf` (first call)
→ `addToBookShelf` (duplicate call)
→ `listBookShelfByPage` contains the book **only once**

**Invariant:**  
Duplicate operations must not create duplicate state.

Covered test:
- `test_reg_addToBookShelf_idempotent_should_not_duplicate`

---

### Bookshelf Cross-API Consistency (Known Issue)

**Scenario:**
- Add non-existent `bookId`
- `queryIsInShelf == true`
- `listBookShelfByPage` does not include the book

**Invariant:**
- `queryIsInShelf == true` ⇒ book must appear in list  
  **OR**
- Invalid `bookId` must be rejected at add time

Covered test:
- `test_reg_bookshelf_consistency_nonexistent_bookId_query_true_but_not_in_list` *(xfail)*

---

### Book Data Consistency
- `searchByPage → queryBookDetail(bookId)`
- `queryBookDetail(bookId) → queryIndexList(bookId)`

**Invariant:**  
All endpoints must reference the same `bookId`.

---

### Comment Flow
- `addBookComment`
- `listCommentByPage` contains the new comment

**Invariant:**  
Successfully submitted comments must be visible to users.

---

## 6.2 Negative Path  
### Validation, Boundary, and Security

### A. Equivalence Partitioning

**Endpoint:** `GET /book/queryBookDetail/{bookId}`

- Valid & exists → covered by happy path
- Valid but non-existent → safe JSON error, no 5xx
- Invalid format (`-1`, `"abc"`) → validation failure, no 5xx

---

### B. Boundary Value Analysis

**Endpoint:** `GET /book/searchByPage`

- `pageNum = 0` → rejected or normalized, no 5xx
- `pageNum = 2` → valid; empty list acceptable
- `pageSize = 1` → success; pagination metadata consistent

---

### C. Error Guessing (Auth & Security)

- Login with invalid password  
  → authentication fails gracefully  
  → no token returned  
  → structured JSON response

---

# 7. Out-of-Scope APIs

The following APIs are intentionally excluded:

- **Payment APIs (`/pay/*`)**
  - External gateway dependency
  - Asynchronous callbacks
  - High flakiness risk

- **Author / CMS APIs**
  - Do not affect core reader flow
  - High change frequency

---

# 8. Known Issues & Observed Contract Deviations

Observed behaviors are documented and explicitly marked with `pytest.xfail`
to preserve intent while keeping CI stable.


---

# 9. Test Execution

```bash
pytest tests/smoke
pytest tests/contract
pytest tests/regression
pytest tests/reg_ci