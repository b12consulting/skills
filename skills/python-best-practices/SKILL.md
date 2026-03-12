---
name: python-best-practices
description: Python coding best practices for data and consulting projects. Use this skill when writing, reviewing, or refactoring Python code to ensure consistent quality, readability, and maintainability. Applies to data pipelines, scripts, APIs, and general Python development.
license: MIT
metadata:
  author: b12consulting
  version: "1.0.0"
---

# Python Best Practices

Guidelines for writing high-quality Python code in data and consulting projects.

## When to Apply

Reference these guidelines when:
- Writing new Python scripts or modules
- Reviewing or refactoring existing Python code
- Building data pipelines or ETL workflows
- Developing APIs or CLI tools
- Conducting code reviews

## Code Style and Readability

- Follow [PEP 8](https://peps.python.org/pep-0008/) for code formatting
- Use [Ruff](https://docs.astral.sh/ruff/) for formatting and linting
- Limit line length to 88 characters (Black default)
- Use descriptive variable and function names
- Write docstrings for all public functions, classes, and modules (Google or NumPy style)

## Type Hints

- Use type hints for all function signatures
- Use `from __future__ import annotations` for forward references
- Use `Optional[T]` or `T | None` for nullable values
- Use `TypedDict` for structured dictionaries
- Run `mypy` or `pyright` for static type checking

```python
# Good
def process_data(records: list[dict[str, str]], max_rows: int = 1000) -> pd.DataFrame:
    ...

# Avoid
def process_data(records, max_rows=1000):
    ...
```

## Error Handling

- Use specific exception types rather than bare `except`
- Log errors with context before re-raising or handling
- Use custom exception classes for domain-specific errors
- Never silently swallow exceptions

```python
# Good
try:
    result = fetch_data(url)
except requests.Timeout:
    logger.error("Request timed out for URL: %s", url)
    raise
except requests.HTTPError as e:
    logger.error("HTTP error %s for URL: %s", e.response.status_code, url)
    raise

# Avoid
try:
    result = fetch_data(url)
except Exception:
    pass
```

## Project Structure

Organize projects consistently:

```
my-project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── pyproject.toml
└── README.md
```

- Use `pyproject.toml` for project configuration
- Use a `src/` layout to prevent import errors during development
- Keep tests alongside or adjacent to source code

## Dependencies

- Pin dependencies with exact versions in `requirements.txt` or lock files
- Use virtual environments (`venv`, `conda`, or `uv`)
- Separate dev dependencies from production dependencies in `pyproject.toml`
- Prefer [uv](https://docs.astral.sh/uv/) for fast dependency management
- Always use `uv add ...` to add packages, which ensures that pyproject.toml and uv.lock remain the source of truth.
- Use virtual environments through `uv`, i.e. `uv venv`, `uv sync`, `uv run ...`.
- Use `uv add --dev ...` to add dev dependencies.

## Data Handling

- Use `polars` for tabular data together with `patito` if schema definition and validation is needed.
- Load only necessary columns when reading large files
- Use chunking or streaming for files that don't fit in memory
- Validate data schemas at ingestion boundaries (e.g., with `patito/pydantic`)

```python
# Good — validate early
from pydantic import BaseModel

class Record(BaseModel):
    id: int
    name: str
    value: float

records = [Record(**row) for row in raw_data]
```

## Testing

- Write unit tests with `pytest`
- Aim for meaningful test coverage, not just high percentages
- Use `pytest-mock` or `unittest.mock` for mocking external dependencies
- Use fixtures for reusable test setup
- Test edge cases and error paths, not just the happy path
- If appropriate, consider using `dirty-equals`, `hypothesis`, `inline-snapshot` to write cleaner tests.

## Logging

- Use Python's built-in `logging` module, not `print`
- Configure logging at the application entry point only
- Use structured logging (e.g., `structlog`) for production services
- Include relevant context in log messages

```python
import logging

logger = logging.getLogger(__name__)

# Good
logger.info("Processing %d records from %s", len(records), source)

# Avoid
print(f"Processing {len(records)} records from {source}")
```

## Security

- Never hardcode secrets or credentials in source code
- Use environment variables or a secrets manager for sensitive configuration. Use `uv run --env-file=.env ...` to activate the environment variables.
- Validate and sanitize all external inputs
- Use `bandit` for static security analysis

## Scripts

Ready-to-use helper scripts are in the `scripts/` directory:

| Script | Purpose |
|--------|---------|
| `scripts/lint.sh [path]` | Run Black, Ruff, mypy, and Bandit checks on the project |
| `scripts/setup-project.sh <name>` | Scaffold a new Python project with the recommended `src/` layout |

**Lint a project:**

```bash
bash scripts/lint.sh ./src
```

**Create a new project:**

```bash
bash scripts/setup-project.sh my-new-service
cd my-new-service
uv venv && uv pip install -e ".[dev]"
```

## References

Supporting files in the `references/` directory:

| File | Purpose |
|------|---------|
| `references/pyproject-template.toml` | Starter `pyproject.toml` with Black, Ruff, mypy, Bandit, and pytest configured |
| `references/logging-config.py` | Reference logging setup — stdlib JSON formatter and structlog patterns |

**Bootstrap `pyproject.toml` from the template:**

```bash
cp references/pyproject-template.toml ./pyproject.toml
# Replace placeholder values:
sed -i 's/YOUR-PROJECT-NAME/my-service/g; s/your_package_name/my_service/g' pyproject.toml
```

**Use the logging reference** — copy the relevant `setup_*` function into your application entry point.
