# Answer quality tests. Bot wording changes between runs, so we assert on
# properties of the reply (keywords, length), never on exact text.
import pytest

from utils import check_reply, load_cases

pytestmark = pytest.mark.quality

# Data-driven test: runs once for every entry in data/quality_cases.json.
# To add a new check, add a JSON entry; no new Python is needed.
# check_reply() applies the rules in each case: must_contain,
# must_contain_any, must_not_contain and max_words.
@pytest.mark.parametrize("case", load_cases("quality_cases"))
def test_answer_properties(chat, case):
    check_reply(chat.ask(case["prompt"]), case)


# Non-determinism test: ask the same question 5 times and require at least
# 90% of replies to mention "Paris". A single run could pass by luck, so
# sampling gives a pass rate, which is how AI output is usually measured.
def test_answer_is_consistent_across_runs(chat):
    """AI output varies, so sample several times and require a high pass rate."""
    runs = 5
    passes = sum("paris" in chat.ask("What is the capital of France?").lower() for _ in range(runs))
    assert passes / runs >= 0.9, f"only {passes}/{runs} replies mentioned Paris"
