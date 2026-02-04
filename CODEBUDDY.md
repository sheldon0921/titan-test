# CODEBUDDY.md This file provides guidance to CodeBuddy when working with code in this repository.

## Common Commands

### Environment Setup
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/login_ddt.py

# Run specific test function
pytest tests/login_ddt.py::TestLogin::test_login_scenarios

# Run tests with verbose output
pytest -v

# Run tests with detailed output
pytest -vv

# Stop on first failure
pytest -x

# Run tests matching a keyword
pytest -k "login"

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

### Environment Configuration
```bash
# Set environment (dev/prod/test/staging)
ENV=dev pytest
```

### Allure Test Reports
```bash
# Generate HTML report (after tests run)
allure generate allure-results -o allure-report

# Open report in browser
allure open allure-report

# Clean and regenerate
allure generate --clean allure-results -o allure-report
```

### Docker
```bash
# Build Docker image
docker build -t titan-test .

# Run tests in Docker
docker run --rm titan-test
```

## Architecture Overview

Titan-Test is a Python-based API testing framework using pytest with data-driven testing, Allure reporting, and database validation capabilities.

### Core Design Patterns

**API Object Pattern**: The `api/` directory contains API wrapper classes that extend `ApiClient`. Each business module (e.g., AuthApi) encapsulates related endpoints with Allure step decorators. These classes inherit common functionality from `ApiClient` including session management, timeout handling, and request/response logging.

**Data-Driven Testing**: Test cases use YAML files in `data/` as data sources. The `load_yaml_data()` utility loads these files, and `@pytest.mark.parametrize` injects data into test functions. Each test case entry contains `title`, `payload`, `headers` (optional), and `expected` fields. Test IDs are generated from case titles for better report readability.

**Fixture-Based Authentication**: The `auth_client` fixture in `conftest.py` provides session-scoped authentication. It first checks if a token exists in the config; if so, it bypasses login and directly injects the token. Otherwise, it performs login using credentials from config. This pattern reduces API calls during test runs.

**Configuration Management**: Environment-specific settings are stored in `config/env.yaml` with keys for dev, prod, staging, and test. The `config` object in `settings.py` loads the appropriate environment based on the `ENV` environment variable (defaults to dev). All other modules import this single config object.

**Layered API Client**: `ApiClient` is the base HTTP client with built-in Allure integration. It automatically attaches request bodies, params, and responses to Allure reports. It handles common exceptions (Timeout, ConnectionError, RequestException) with proper logging and re-raising. Session-level headers (Accept, Content-Type, Connection) are set once and reused.

**Database Utilities**: `DBUtils` provides MySQL operations using PyMySQL with dictionary cursors (returns `{'id': 1}` instead of `(1,)`). It supports `query_one()`, `query_all()`, `execute()` for DML with auto-commit, and a `transaction()` context manager. The class also supports both standalone usage and context manager protocol (`with DBUtils() as db:`).

### Test Execution Flow

1. pytest reads `pytest.ini` configuration
2. `conftest.py` fixtures initialize (session-scoped auth_client adds environment properties to allure-results)
3. Test classes load YAML data files via `load_yaml_data()`
4. Tests receive `auth_client` fixture (already authenticated) and `case_info` from parametrize
5. Tests make API calls through API wrapper classes
6. Allure automatically captures request/response details
7. Assertions validate status codes and response data

### Key Integration Points

- **conftest.py**: Central fixture location. The `auth_client` fixture is the primary dependency injection point for authenticated API calls. The `add_allure_environment_property` fixture ensures test environment metadata appears in reports.
- **config/settings.py**: Single source of truth for configuration. Always use `config.get('key', default)` pattern to access values.
- **lib/utils.py**: Provides `load_yaml_data()` for data-driven testing and `get_json_value()` using JsonPath expressions for extracting data from JSON responses.
- **lib/api_client.py**: Never bypass this class for HTTP requests. All API interactions should go through wrapper classes that inherit from it.

### Testing Best Practices

- Use `pytest.skip()` when test data is incomplete rather than failing the test
- Prefer `.get()` method on dictionaries over direct key access to avoid KeyError
- Use `allure.dynamic.title()` to set meaningful test names from case data
- Leverage the `transaction()` context manager for multi-step database operations
- Import test data utilities from `lib.utils` rather than reimplementing YAML parsing
