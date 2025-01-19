# Development Guide

This document describes how to set up your development environment to work on smoosh.

## Initial Setup

1. Clone the repository:
```bash
git clone https://github.com/j-mcnamara/smoosh.git
cd smoosh
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv .venv

# Activate on macOS/Linux
source .venv/bin/activate
# Or on Windows
# .venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Set up pre-commit hooks:
```bash
pre-commit install
```

## VS Code Setup

If you're using VS Code, install these recommended extensions:
- Python (Microsoft)
- Pylance
- Black Formatter
- isort

Our `.vscode/settings.json` contains the recommended settings for these extensions.

## Code Quality Tools

This project uses several tools to maintain code quality:

- **black**: Code formatter (line length: 88 characters)
- **isort**: Import sorter (configured to work with black)
- **flake8**: Linter with docstring checking
- **mypy**: Static type checker
- **pytest**: Testing framework with coverage reporting

These tools run automatically on commit via pre-commit hooks. You can also run them manually:

```bash
# Format code
black .
isort .

# Run type checking
mypy src/smoosh

# Run linting
flake8 src/smoosh

# Run tests with coverage
pytest
```

## Commit Style Guide

- Use imperative present tense ("add" not "adds" or "adding")
- First line should be < 50 characters when possible
- Follow with a blank line and detailed description if needed
- Example good commit messages:
  ```bash
  # Short commit for simple changes
  git commit -m "add user authentication module"

  # Multi-line commit for more complex changes
  git commit -m "add error handling for network timeouts" \
            -m "- Add retry mechanism for failed requests
- Implement exponential backoff strategy
- Add timeout configuration options
- Update documentation with new error handling details
- Add tests for retry mechanism"

  # Alternative syntax for multi-line (opens editor)
  git commit

  # This opens your editor with:
  add comprehensive error handling system

  - Implement request retry mechanism with exponential backoff
  - Add configuration options for timeouts and max retries
  - Create custom exceptions for different failure modes
  - Add detailed logging for debugging failed requests
  - Update documentation with error handling procedures

  Testing:
  - Add integration tests for retry mechanism
  - Add unit tests for timeout configurations
  - Add error scenario test cases

  Closes #123
  ```

## Project Structure

```
smoosh/
├── src/smoosh/        # Main package code
├── tests/             # Test files
├── .vscode/           # VS Code settings
├── .pre-commit-config.yaml  # Pre-commit hook config
└── pyproject.toml     # Project configuration
```

## Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=smoosh

# Run specific test file
pytest tests/test_specific.py
```

## Type Checking

The project uses strict type checking. All functions should have type annotations:

```python
def process_data(input_data: str) -> dict[str, Any]:
    """Process input data.

    Args:
        input_data: The input string to process

    Returns:
        Processed data as a dictionary
    """
    ...
```

## Common Tasks

### Adding a New Dependency

1. Add to `dependencies` in `pyproject.toml`
2. If it needs type stubs, add to `dev` dependencies
3. Update mypy config in pre-commit if needed

### Before Submitting a Pull Request

1. Ensure all tests pass: `pytest`
2. Check type hints: `mypy src/smoosh`
3. Verify code formatting: `black . --check`
4. Run pre-commit on all files: `pre-commit run --all-files`
