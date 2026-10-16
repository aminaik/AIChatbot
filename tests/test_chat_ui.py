import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.ui


def test_page_loads(chat):
    expect(chat.page).to_have_title("HelpBot")
    expect(chat.input).to_be_visible()
    expect(chat.send_button).to_be_enabled()


def test_user_message_is_shown_and_bot_replies(chat):
    chat.send_message("Hello")
    expect(chat.user_messages).to_have_text(["Hello"])
    expect(chat.bot_messages).to_have_count(1, timeout=10_000)


def test_input_locked_and_typing_shown_while_waiting(chat):
    chat.send_message("What is the capital of France?")
    expect(chat.typing_indicator).to_be_visible()
    expect(chat.send_button).to_be_disabled()
    expect(chat.typing_indicator).to_be_hidden(timeout=10_000)
    expect(chat.send_button).to_be_enabled()


def test_conversation_history_keeps_order(chat):
    chat.ask("Hello")
    chat.ask("What is 2+2?")
    expect(chat.user_messages).to_have_text(["Hello", "What is 2+2?"])
    expect(chat.bot_messages).to_have_count(2)


def test_empty_message_is_rejected(chat):
    chat.send_message("   ")
    expect(chat.error_banner).to_contain_text("cannot be empty")
    expect(chat.bot_messages).to_have_count(0)


def test_overlong_message_shows_error(chat):
    chat.send_message("a" * 501)
    expect(chat.error_banner).to_contain_text("too long")
