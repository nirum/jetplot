default: test

build:
  uv build

upload:
  uv upload

docs:
  mkdocs build --strict

format:
  uv run ruff format

typecheck:
  uv run pyrefly check

test:
  uv run pytest --cov=jetplot --cov-report=term

loop:
  find {src,tests} -name "*.py" | entr -c just test
