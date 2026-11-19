import json
import re
import tomllib
from pathlib import Path

import polyglot_python

ROOT = Path(__file__).resolve().parents[1]


def test_version_matches_pyproject():
    metadata = tomllib.loads(
        ROOT.joinpath("pyproject.toml").read_text(encoding="utf-8")
    )
    assert polyglot_python.__version__ == metadata["project"]["version"]


def test_changelog_mentions_current_version():
    changelog = ROOT.joinpath("CHANGELOG.md").read_text(encoding="utf-8")
    assert f"## [{polyglot_python.__version__}]" in changelog


def test_npm_wrapper_matches_version():
    package = json.loads(ROOT.joinpath("npm", "package.json").read_text(encoding="utf-8"))
    assert package["name"] == "polyglot-python"
    assert package["version"] == polyglot_python.__version__
    binary = ROOT.joinpath("npm", package["bin"]["polyglot-python"])
    assert binary.is_file()
    assert binary.read_text(encoding="utf-8").startswith("#!/usr/bin/env node\n")


def _shipped_locales():
    return json.loads(
        ROOT.joinpath("src", "polyglot_python", "locales.json").read_text(encoding="utf-8")
    )["locales"]


def test_mkdocs_site_description_matches_shipped_locale_count():
    mkdocs = ROOT.joinpath("mkdocs.yml").read_text(encoding="utf-8")
    match = re.search(r"(?ms)^site_description: >-\n(.*?)(?=^\S)", mkdocs)
    assert match is not None, "mkdocs.yml must declare a site_description"
    description = " ".join(match.group(1).split())
    assert f"{len(_shipped_locales())} locales" in description


def test_readme_locale_table_covers_every_shipped_locale():
    readme = ROOT.joinpath("README.md").read_text(encoding="utf-8")
    for code in _shipped_locales():
        assert re.search(rf"(?m)^\|\s*{re.escape(code)}\s*\|", readme), code
