# Repository Guidelines

## Project Structure & Module Organization
Source lives under `src/jetplot/`, split into focused modules such as `colors.py`, `plots.py`, and `style.py`. Add new utilities in cohesive files and keep imports relative (e.g. `from .colors import Palette`). Tests reside in `tests/` and should mirror the module layout; prefer descriptive folders like `tests/test_plots.py` to match the feature under test. Documentation content is maintained in `docs/` and rendered via MkDocs, while build artefacts land in `build/` and `dist/`.

## Build, Test, and Development Commands
Run `uv run ruff check .` to ensure linting passes and style expectations are met. Use `uv run pytest --cov=jetplot --cov-report=term` for the full suite with coverage feedback, and `uv run pyrefly check` to validate typing across the package. When iterating on documentation, launch `uv run mkdocs serve` for a live preview. Regenerate distributions with `uv build` once changes are ready to publish.

## Coding Style & Naming Conventions
Follow PEP 8 defaults: four-space indentation, snake_case for functions and module-level variables, and CapWords for classes. Exported constants stay upper-case with underscores. Provide clear docstrings for every public function or class that describes inputs, return values, and side effects. Keep modules small, favor pure functions, and rely on the shared helpers already defined in `style.py` and `chart_utils.py` instead of duplicating logic.

## Testing Guidelines
Write pytest-based tests alongside new functionality, naming files `test_<feature>.py` and individual tests `test_<behavior>`. Prefer parametrization to cover edge cases concisely. Aim to maintain or raise the coverage reported by the standard coverage command; unexpected drops should block merges. Include regression tests when fixing bugs so future refactors stay guarded.

## Commit & Pull Request Guidelines
Commits use short, imperative summaries (e.g. `Add palette cycler helper`). Break large efforts into logical commits that pass linting and tests independently. Pull requests must include **Summary** and **Testing** sections outlining what changed and the exact commands run (`uv run ruff check .`, `uv run pytest --cov=jetplot --cov-report=term`, `uv run pyrefly check`). Link relevant issues and add screenshots when UI-facing artifacts such as documentation pages change.

## Documentation Tips
Reference existing examples in `docs/` when adding guides, and keep code snippets synced with the APIs under `src/jetplot/`. Rebuild the site locally with `uv run mkdocs serve` after edits to verify navigation, formatting, and cross-links before submitting your changes.
