# Jetplot

[![Tests](https://github.com/nirum/jetplot/actions/workflows/ci.yml/badge.svg)](https://github.com/nirum/jetplot/actions/workflows/ci.yml)
[![Typecheck](https://github.com/nirum/jetplot/actions/workflows/typecheck.yml/badge.svg)](https://github.com/nirum/jetplot/actions/workflows/typecheck.yml)
[![codecov](https://codecov.io/gh/nirum/jetplot/branch/master/graph/badge.svg)](https://codecov.io/gh/nirum/jetplot)

## About

`jetplot` is collection of miscellaneous utils for Matplotlib.


## Installation

```bash
pip install jetplot
```

## Documentation

Documentation is built with [MkDocs](https://www.mkdocs.org/). To view the
pages locally run:

```bash
mkdocs serve
```
The documentation sources live in the [`docs/`](docs/) folder.

## Changelog

| Version | Release Date | Description                                                                                                                                                                                                     |
| ------: | :----------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 0.6.0   | Jul 21 2024  | Migrated from setup.py to pyproject.toml.                                                                                                                                                     |
| 0.5.3   | Aug 30 2022  | Stops jetplot from updating Matplotlib rcParams on import.                                                                                                                                                     |
| 0.5.0   | Jul 15 2022  | Updates default color palettes, adds new Palette class, adds ridgeline plot.                                                                                                                                                     |
| 0.4.0   | Oct 20 2021  | Name change! Package renamed to `jetplot`.                                                                                                                                                       |
| 0.3.0   | Oct 13 2021  | Drops animation module and the `moviepy` dependency                                                                                                                                                             |
| 0.0.0   | Jan 19 2015  | Initial commit                                                                                                                                                                                                  |

## License

MIT. See [`LICENSE.md`](./LICENSE.md)
