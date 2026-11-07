# Contributing to polyglot-python

Thanks for helping. `polyglot-python` is a small, deterministic keyword
transpiler: you write Python grammar with localized keywords and it maps them
back to real Python keywords. There is no AI, no network access and no
randomness anywhere in the translation path, and that property is a design
constraint, not an implementation detail.

## Requirements

- CPython 3.12 or newer. This is not negotiable for contributors: 3.10/3.11
  tokenizers split Indic combining marks, so several Hindi keywords would not
  translate (see the "Limitations" section of the README).
- Node.js 20, only if you touch `npm/`.

## Development setup

```bash
python -m venv .venv
```

Windows (cmd / Git Bash), matching the commands in the README:

```bash
.venv/Scripts/pip install -e ".[dev]"
.venv/Scripts/python -m pytest -q --cov=polyglot_python --cov-fail-under=100
```

Linux and macOS:

```bash
source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q --cov=polyglot_python --cov-fail-under=100
```

The `dev` extra installs `pytest>=8` and `pytest-cov>=5`. There are no runtime
dependencies, and there should never be any.

## Tests

The suite is plain **pytest** — there is no `unittest` runner, no `tox`, and no
`nox`. Test configuration lives in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

`pythonpath = ["src"]` means the package is imported from the source tree, so an
editable install is convenient but not required to run the tests.

Run everything:

```bash
python -m pytest -q
```

The suite currently collects 242 tests. It covers every keyword in both
directions for all 20 locales, every example file through the CLI, and version
consistency between `pyproject.toml`, `polyglot_python.__version__`, the
changelog heading (`## [<version>]`) and `npm/package.json`.

**Coverage gate:** CI enforces 100% statement coverage. Reproduce it locally
with the same command CI uses:

```bash
python -m pytest -q --cov=polyglot_python --cov-fail-under=100
```

If you add a code path, add the test that covers it. A PR that lowers coverage
will fail CI.

## Pre-commit hooks

If `.pre-commit-config.yaml` is present:

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

The hooks are generic file hygiene checks (trailing whitespace, end-of-file,
YAML/TOML/JSON validity, large files, merge and case conflicts, LF line
endings). They do not reformat Python source. See the comment block in
`.pre-commit-config.yaml` for why `ruff` is deliberately not a hook here.

## CI

`.github/workflows/ci.yml` is the source of truth. It runs four jobs:

| Job | What it enforces |
|---|---|
| `test` | Ubuntu on Python 3.12, 3.13, 3.14, 3.15 plus Windows and macOS on 3.12. The 100% coverage gate applies to the Linux 3.12 leg only. |
| `determinism` | Every `examples/classify.*` and `examples/tour.*` is translated twice on Ubuntu, Windows and macOS; the two byte streams must be identical and the newline count must match the source. |
| `package` | Builds sdist + wheel, installs the wheel into a clean venv, runs `polyglot-python check examples` and executes one example end to end. |
| `npm` | Smoke-tests `npm/bin/polyglot-python.js` against the installed Python package and runs `npm pack --dry-run`. |

Superseded runs are cancelled and every job has a timeout.

## Changing locales

Locales are data, not code. All 20 tables live in
`src/polyglot_python/locales.json`, which is shipped as package data
(`[tool.setuptools.package-data]`). Add or change a locale there; malformed
tables are rejected at load time.

If you add a locale, also add `examples/classify.<code>` and
`examples/tour.<code>` — `tests/test_examples.py` runs every example, and the
determinism job translates every example twice.

## Determinism rules

- No network calls, no `random`, no time or locale-dependent formatting in the
  translation path.
- Key order and output ordering must be explicit; do not rely on set or dict
  iteration order for anything that reaches output.
- Output must be byte-identical across runs. The `determinism` CI job exists to
  catch violations.

## Pull requests

1. Fork, then branch: `git checkout -b fix/short-description`.
2. Keep the change focused; unrelated refactors belong in their own PR.
3. Add or update tests. Coverage must stay at 100%.
4. Run `python -m pytest -q --cov=polyglot_python --cov-fail-under=100`.
5. If you change user-visible behaviour, add an entry under `## [Unreleased]` in
   `CHANGELOG.md` using Keep a Changelog headings (`Added`, `Changed`,
   `Deprecated`, `Removed`, `Fixed`, `Security`).
6. Do **not** bump the version or edit released changelog sections; releases are
   cut by the maintainer.

The version in `pyproject.toml` must stay in lockstep with
`src/polyglot_python/__init__.py`, `npm/package.json` and the changelog heading;
`tests/test_metadata.py` enforces this and the release workflow refuses a tag
that does not equal `v<version>`.

## Reporting bugs

Open an issue at
<https://github.com/Furox-Art/polyglot-python/issues> with the locale code, a
minimal localized source that reproduces the problem, the observed output, and
your Python version (`python -VV`). Security issues go through
[SECURITY.md](SECURITY.md) instead.

## License

Contributions are accepted under the MIT license in [LICENSE](LICENSE).
