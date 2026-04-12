"""Tests for i18n locale files (en.json / ko.json).

Validates that both locale files are well-formed JSON, share the same key
set, and preserve interpolation placeholders.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

_LOCALES_DIR = (
    Path(__file__).resolve().parents[1] / "src" / "memtomem" / "web" / "static" / "locales"
)

_PLACEHOLDER_RE = re.compile(r"\{(\w+)\}")


def _load_locale(name: str) -> dict[str, str]:
    path = _LOCALES_DIR / f"{name}.json"
    assert path.exists(), f"Locale file missing: {path}"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict), f"{name}.json root must be an object"
    return data


@pytest.fixture(scope="module")
def en() -> dict[str, str]:
    return _load_locale("en")


@pytest.fixture(scope="module")
def ko() -> dict[str, str]:
    return _load_locale("ko")


class TestLocaleFiles:
    """Structural tests for locale JSON files."""

    def test_en_is_valid_json(self, en: dict[str, str]) -> None:
        assert len(en) > 0, "en.json must not be empty"

    def test_ko_is_valid_json(self, ko: dict[str, str]) -> None:
        assert len(ko) > 0, "ko.json must not be empty"

    def test_ko_has_all_en_keys(self, en: dict[str, str], ko: dict[str, str]) -> None:
        missing = set(en) - set(ko)
        assert not missing, f"Keys in en.json missing from ko.json: {sorted(missing)}"

    def test_en_has_all_ko_keys(self, en: dict[str, str], ko: dict[str, str]) -> None:
        orphan = set(ko) - set(en)
        assert not orphan, f"Keys in ko.json missing from en.json: {sorted(orphan)}"

    def test_placeholder_parity(self, en: dict[str, str], ko: dict[str, str]) -> None:
        """Each key's {param} placeholders must match between en and ko."""
        mismatches: list[str] = []
        for key in en:
            if key not in ko:
                continue
            en_ph = set(_PLACEHOLDER_RE.findall(en[key]))
            ko_ph = set(_PLACEHOLDER_RE.findall(ko[key]))
            if en_ph != ko_ph:
                mismatches.append(f"  {key}: en={en_ph} ko={ko_ph}")
        assert not mismatches, "Placeholder mismatch:\n" + "\n".join(mismatches)

    def test_all_values_are_strings(self, en: dict[str, str], ko: dict[str, str]) -> None:
        for name, data in [("en", en), ("ko", ko)]:
            bad = [k for k, v in data.items() if not isinstance(v, str)]
            assert not bad, f"Non-string values in {name}.json: {bad}"

    def test_no_empty_values(self, en: dict[str, str], ko: dict[str, str]) -> None:
        for name, data in [("en", en), ("ko", ko)]:
            empty = [k for k, v in data.items() if not v.strip()]
            assert not empty, f"Empty values in {name}.json: {empty}"
