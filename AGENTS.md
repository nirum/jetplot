# Developer Instructions

## Code Style
- Run `uv run ruff check .` before committing to ensure all Python code passes linting.
- Write clear docstrings for all public functions and classes.
- Use relative imports within the `jetplot` package.

## Testing
- Run `uv run pytest --cov=jetplot --cov-report=term` before committing to ensure all tests pass before submitting a PR.
- Run `uv run pyrefly check` before committing to ensure all pyrefly type checking passes.

## PR Guidelines
- Your pull request description must contain a **Summary** section explaining the changes.
- Include a **Testing** section describing the commands used to run lint and tests along with their results.
