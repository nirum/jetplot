default: test

build:
  uv build

publish:
  uv publish

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

autoapi:
  mkdir -p docs/api/
  @for f in ./src/jetplot/*.py; do \
    name="${f##*/}"; \
    name="${name%.py}"; \
    [[ "$name" == "__init__" ]] && continue; \
    printf "# %s\n::: jetplot.%s\n" "${name}" "$name" > "docs/api/${name}.md"; \
    echo "wrote ${name}.md"; \
  done
