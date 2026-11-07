# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 0.2.x | Yes |
| < 0.2 | No |

Fixes target the `0.2.x` line. Older lines are not assumed to receive
backports.

## Reporting a vulnerability

Please **do not open a public issue** for a security problem.

Use GitHub's private vulnerability reporting:

<https://github.com/Furox-Art/polyglot-python/security/advisories/new>

Include the affected version (`polyglot-python --version`), a minimal
reproduction, the impact you believe it has, and any suggested fix.

## What this software is

`polyglot-python` is a local, offline keyword transpiler. The translation path
is deterministic: the same source, locale and version always produce
byte-identical Python. It has no runtime dependencies, makes no network calls,
and uses no randomness.

It is also published to npm as `polyglot-python`, but that package is a thin
Node shim only (`npm/bin/polyglot-python.js`). It contains no Python; it looks
for an interpreter that can `import polyglot_python` (`python`, `python3`, `py
-3`, or the path in the `POLYGLOT_PYTHON` environment variable) and re-executes
`python -m polyglot_python` with the arguments it was given. It never installs
anything.

## Expected behaviour, not vulnerabilities

- **`polyglot-python run FILE` executes the translated program** in the Python
  process, with your privileges, exactly like `python FILE`. Running untrusted
  source is as unsafe here as running it with CPython. Use `check`, which
  translates and compiles without executing, to validate untrusted input.
- **The translator does not sandbox anything.** It is a keyword rewriter, not an
  interpreter with a restricted mode.
- **Malformed or hostile locale tables** in `locales.json` are rejected at load
  time rather than silently accepted, but a locale is trusted data supplied with
  the installed package.
- **`POLYGLOT_PYTHON`** lets a user choose which interpreter the npm shim runs.
  That is an explicit user choice; an attacker who can already set your
  environment variables does not need this package.

## In scope

- A crafted localized source file that makes the translator emit Python whose
  meaning differs from the written source, beyond the keyword mapping.
- Non-determinism, where the same source, locale and version produce different
  output.
- A malformed locale table that produces arbitrary code rather than a load-time
  error.
- Supply chain: a substituted PyPI or npm artifact. Releases are published by
  the `Release` and `release-npm` workflows through Trusted Publishing (OIDC);
  the release workflow refuses a tag that does not match `v<version>` from
  `pyproject.toml`. No long-lived registry token is stored in the repository.

## Out of scope

- Vulnerabilities in CPython or in the program you asked to run.
- The consequences of executing untrusted code with `run` (see above).
- Reports that require the user to install a modified copy of this package.
