# Safety tests: the bot should refuse harmful requests and never leak
# its hidden system prompt, even when the user tries to trick it.
import pytest

from utils import check_reply, load_cases

pytestmark = pytest.mark.safety


# Data-driven: runs once per entry in data/safety_cases.json.
# - must_contain checks that the bot refused.
# - must_not_contain checks that no secret text leaked
#   (a refusal alone is not enough if the reply also quotes the prompt).
# A case with "known_bug" is marked strict xfail: it shows as "x" while the
# bug exists, and pytest flags it as soon as the bug is fixed.
@pytest.mark.parametrize("case", load_cases("safety_cases"))
def test_refusals_and_no_prompt_leak(chat, case):
    check_reply(chat.ask(case["prompt"]), case)
