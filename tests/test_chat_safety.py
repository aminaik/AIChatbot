import pytest

from utils import check_reply, load_cases

pytestmark = pytest.mark.safety


@pytest.mark.parametrize("case", load_cases("safety_cases"))
def test_refusals_and_no_prompt_leak(chat, case):
    check_reply(chat.ask(case["prompt"]), case)
