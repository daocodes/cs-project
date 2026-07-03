# Progress Log

## 2026-07-02

### Completed
- Standardized backend auth provider contract across `backend/app/auth/mock.py`, `backend/app/auth/cognito.py`, `backend/app/auth/factory.py`, and `backend/app/auth/deps.py`.
- Added shared auth user type in `backend/app/auth/types.py` and updated auth modules to import from it.
- Fixed mock verifier method naming mismatch by using `resolve_user(...)` consistently.
- Fixed Cognito verifier constructor field assignment (`user_pool_id`) and added missing-authorization guard behavior.
- Updated auth factory to:
  - validate required Cognito settings when `AUTH_MODE=cognito`,
  - select verifier using Cognito-specific env vars,
  - return a typed verifier interface.
- Updated test setup in `backend/tests/conftest.py` to override `get_current_user` and support mutable auth context per test.
- Updated `backend/tests/test_applications.py` to:
  - remove client-provided `user_id` assumptions,
  - assert ownership is derived from injected current user,
  - add cross-user access protection coverage (`GET`/`PATCH`/`DELETE` return `404` for non-owners).

### Validation
- `python -m pytest tests/test_applications.py` passed (`7 passed`).
- `python -m ruff check app/auth tests/conftest.py tests/test_applications.py` passed.

### Next
- Frontend auth UX for issue #8:
  - sign-in + session persistence across refresh,
  - protected-route redirect for unauthenticated users,
  - README auth flow documentation.
