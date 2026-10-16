import pytest

from utils import check_reply, load_cases

pytestmark = pytest.mark.quality


@pytest.mark.parametrize("case", load_cases("quality_cases"))
def test_answer_properties(chat, case):
    check_reply(chat.ask(case["prompt"]), case)


def test_answer_is_consistent_across_runs(chat):
    """AI output varies, so sample several times and require a high pass rate."""
    runs = 5
    passes = sum("paris" in chat.ask("What is the capital of France?").lower() for _ in range(runs))
    assert passes / runs >= 0.9, f"only {passes}/{runs} replies mentioned Paris"
