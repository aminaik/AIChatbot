import json
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / "data"


def load_cases(name: str) -> list:
    """Load eval cases from data/<name>.json as pytest params.
    A case with "known_bug" set is marked xfail so it is tracked, not hidden."""
    params = []
    for case in json.loads((DATA_DIR / f"{name}.json").read_text()):
        marks = []
        if case.get("known_bug"):
            marks.append(pytest.mark.xfail(reason=case["known_bug"], strict=True))
        params.append(pytest.param(case, id=case["id"], marks=marks))
    return params


def check_reply(reply: str, case: dict) -> None:
    """Assert on properties of a reply instead of exact wording."""
    low = reply.lower()
    for word in case.get("must_contain", []):
        assert word.lower() in low, f"expected '{word}' in: {reply!r}"
    anyof = case.get("must_contain_any", [])
    if anyof:
        assert any(w.lower() in low for w in anyof), f"expected one of {anyof} in: {reply!r}"
    for word in case.get("must_not_contain", []):
        assert word.lower() not in low, f"unexpected '{word}' in: {reply!r}"
    if "max_words" in case:
        assert len(reply.split()) <= case["max_words"], f"too long: {reply!r}"
