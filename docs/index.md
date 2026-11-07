# polyglot-python

Write Python in your own language, deterministically.

polyglot-python is a keyword transpiler for Python. You keep Python's grammar and write
programs with localized keywords; polyglot-python maps those keywords to the real Python
keywords and hands the result to CPython. No AI, no network, no randomness: the same
source, locale and version always produce byte-identical Python.

It is not a prose-to-code translator and it does not guess intent. It is Python syntax
with your words.

## Install

```bash
pip install polyglot-python
```

The npm package is a thin wrapper around the Python CLI, so the Python package must be
installed as well:

```bash
npm install -g polyglot-python
```

Requires Python 3.12+. Python 3.10/3.11 are not supported because their tokenizer splits
Indic combining marks, so several Hindi keywords would not translate. No runtime
dependencies.

## Quick start

`examples/classify.tr`:

```python
fonksiyon classify(n):
    eğer n % 15 == 0:
        döndür "FizzBuzz"
    değilse_eğer n % 3 == 0:
        döndür "Fizz"
    değilse_eğer n % 5 == 0:
        döndür "Buzz"
    değilse:
        döndür str(n)
```

## Where to go next

- Source, issues and releases: <https://github.com/Furox-Art/polyglot-python>
- The phase 2 design plan: [Roadmap](phase-2-plan.md)
- Package on PyPI: <https://pypi.org/project/polyglot-python/>

> This page summarises the repository README. The README is the authoritative
> description; every claim here is taken from it.
