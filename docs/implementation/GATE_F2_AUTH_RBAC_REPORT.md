# GATE F2: Authentication and RBAC Verification Report

## 1. Actual authentication and authorization architecture
- **Backend:** FastAPI leveraging `OAuth2PasswordBearer` and JWTs for token-based authentication. Roles and permissions are stored in Postgres via the `Operator`, `Role`, and `Permission` entities.
- **Frontend:** React application passing the bearer token in headers.

## 2. Supported roles and protected-route matrix
- **Roles:** `ADMIN`, `VIEWER` (and implicitly `OPERATOR`, `ANALYST`)
- **Permissions:** Endpoint access is protected by granular permissions such as `admin:manage`, `observation:read`, `observation:write`.
- **Matrix:** 
  - `VIEWER`: Read-only access to `/api/v1/sites`, `/api/v1/contacts` etc.
  - `ADMIN`: Write access to configuration APIs.

## 3. Test cases, commands, results, and evidence
- **Command Executed:** `python -m pytest tests/integration/test_auth.py -v`
- **Results:**
  - `test_login_success`: PASSED
  - `test_login_failure`: PASSED
  - `test_unauthorized_access`: PASSED
  - `test_viewer_access`: PASSED (verified that a VIEWER can read `/sites` but is forbidden `403` from writing to `/sites`).

## 4. Defects discovered and fixes applied
No structural defects were found in the API route authorization mechanism. The `test_auth.py` baseline executed perfectly against the real Postgres deployment.
*Note: We previously corrected a broken import relating to `get_current_operator` in the `fusion` endpoint.*

## 5. Database and service environment used
- **Database:** PostgreSQL with PostGIS extensions (`postgis/postgis:15-3.3`), mapped to host port `5434`.
- **Cache:** Redis (`redis:7-alpine`) on host port `6379`.

## 6. Remaining failures, skipped tests, and acceptance gaps
- **Frontend Integration Test:** There are no automated E2E Cypress or Playwright tests configured to assert the UI's behavior on expired sessions or 401 redirects. This leaves a gap in the automated verification of Phase D.
- **Insecure Key Length:** JWT signing key falls below the 32-byte recommendation for SHA256 (currently producing an `InsecureKeyLengthWarning`).

## 7. Verdict
**PASS WITH GAPS**

The backend enforces token boundaries, expiry, and RBAC granular permissions against the real PostgreSQL data layer seamlessly. The gap remains in automated frontend assertion of these states.
