# UI behavior tests: does the chat page itself work correctly,
# regardless of what the bot says?
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


# Smoke test: the page loads and the main controls are present.
# If this fails, every other test would fail too, so it is the first check.
def test_page_loads(chat):
    expect(chat.page).to_have_title("HelpBot")
    expect(chat.input).to_be_visible()
    expect(chat.send_button).to_be_enabled()


# Happy path: the user's message appears in the chat log,
# and exactly one bot reply follows it.
def test_user_message_is_shown_and_bot_replies(chat):
    chat.send_message("Hello")
    expect(chat.user_messages).to_have_text(["Hello"])
    expect(chat.bot_messages).to_have_count(1, timeout=10_000)



# Loading state: while the bot is "thinking", the typing indicator shows
# and Send is disabled (prevents double submits). Both reset afterwards.
def test_input_locked_and_typing_shown_while_waiting(chat):
    chat.send_message("What is the capital of France?")
    expect(chat.typing_indicator).to_be_visible()
    expect(chat.send_button).to_be_disabled()
    expect(chat.typing_indicator).to_be_hidden(timeout=10_000)
    expect(chat.send_button).to_be_enabled()


# Conversation history: two questions produce two replies,
# and the user messages stay in the order they were sent.
def test_conversation_history_keeps_order(chat):
    chat.ask("Hello")
    chat.ask("What is 2+2?")
    expect(chat.user_messages).to_have_text(["Hello", "What is 2+2?"])
    expect(chat.bot_messages).to_have_count(2)


# Input validation: a blank message is rejected with an error,
# and no request reaches the bot (zero bot messages).
def test_empty_message_is_rejected(chat):
    chat.send_message("   ")
    expect(chat.error_banner).to_contain_text("cannot be empty")
    expect(chat.bot_messages).to_have_count(0)


# Boundary test: 501 characters is one over the 500-character limit,
# so the app should show a "too long" error.
def test_overlong_message_shows_error(chat):
    chat.send_message("a" * 501)
    expect(chat.error_banner).to_contain_text("too long")
