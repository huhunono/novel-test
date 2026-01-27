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
| Regression| Business behavior, validation & state invariants  | Cross-API flows, negative paths, boundary conditions |

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

## 5. Regression Test Plan 

Regression tests focus on **business-critical flows**
and **cross-API consistency**, rather than field-level assertions.

### 5.1 Happy Path (Core Business Flows with Scenario-Based Testing)

#### Authentication
- `login → userInfo` (token validity)
- `login → refreshToken → userInfo` (token refresh)

#### Bookshelf State Flow
- `addToBookShelf`
→ `queryIsInShelf == true`
→ `listBookShelfByPage` contains book
→ `removeFromBookShelf`
→ `queryIsInShelf == false`

#### Bookshelf Idempotency Rule (Regression Invariant)

- `addToBookShelf` (first call)
→ `addToBookShelf` (duplicate call)
→ `listBookShelfByPage` contains the book **only once** (no duplicates)

Covered Tests:
- `test_reg_addToBookShelf_idempotent_should_not_duplicate`


#### Bookshelf Cross-API Consistency (Known Issue)

- Scenario:
  - `addToBookShelf` with a **non-existent bookId`
  - `queryIsInShelf` returns `true`
  - `listBookShelfByPage` does **not** display the book

- Expected Invariant:
  - If `queryIsInShelf == true`,
    the book should be visible in `listBookShelfByPage`
  - **OR**
    `addToBookShelf` should reject non-existent `bookId`

- Current Behavior:
  - Inconsistent contract across APIs (known issue)

Covered Tests:
- `test_reg_bookshelf_consistency_nonexistent_bookId_query_true_but_not_in_list` *(xfail)*

#### Book Data Consistency
- `searchByPage → queryBookDetail(bookId)`
- `queryBookDetail(bookId) → queryIndexList(bookId)`
  (all items reference the same bookId)

#### Comment Flow
- `addBookComment (unique content)`
→ `listCommentByPage` contains new comment

---

### 5.2 Negative Path (Validation, Boundary, Security)

### A. Equivalence Partitioning (Data Validity)

#### 1) GET /book/queryBookDetail/{bookId}
- **Valid & Exists**
  - Covered by scenario-based tests (happy path).

- **Valid but Non-existent**
  - Expected: JSON error response (HTTP 404 or `code != 200`).
  - Current behavior: returns HTML "Not Found" page (contract violation).

- **Invalid Format**
  - Expected: JSON validation error (HTTP 400 or `code != 200`).
  - Current behavior: returns HTML error page (contract violation).



---

### B. Boundary Value Analysis (Pagination)

Applied to pagination APIs, which are common sources of off-by-one errors.

#### GET /book/searchByPage

- **pageNum = 0** (invalid lower boundary)
  - Expected: rejected (4xx / `ok=false`) or corrected to `pageNum >= 1` (no 5xx).
  - Actual: returns **HTTP 200 + ok=true** with `pageNum="0"` and empty list.
  - Status: flagged by regression test as a boundary defect  
    (`test_reg_searchByPage_pageNum_zero_should_be_rejected_or_corrected`).

- **pageNum = 2** (valid just-inside value)
  - Expected: handled normally; empty list is acceptable when `pageNum > pages`.
  - Actual: returns **HTTP 200 + ok=true** with `pageNum="2"` and empty list (passes).
  - Status: covered by regression test  
    (`test_reg_searchByPage_pageNum_two_should_return_empty_or_valid_result`).

- **pageNum = 1** (default valid)
  - Covered by scenario-based regression flow tests (happy path), no duplication here.

- **pageSize = 1** (minimum valid boundary)
  - Expected: succeeds; result list size `<= 1`; pagination metadata remains consistent.
  - Actual: succeeds and meets expectations.
  - Status: covered by regression test  
    (`test_reg_searchByPage_pageSize_one_should_return_at_most_one_item`).



---

### C. Error Guessing (Security & Missing Params)

Error guessing tests are designed based on experience with similar systems,
focusing on high-risk failure scenarios that are easy to overlook but critical
to system correctness and security.

- **login invalid password**
  - Scenario: submit valid username with incorrect password.
  - Expected: authentication fails gracefully (`ok=false` / `code!=200`), no token returne
  
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
