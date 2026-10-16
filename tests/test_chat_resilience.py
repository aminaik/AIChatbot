import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.resilience


def test_server_error_shows_friendly_message(page, chat):
    page.route("**/api/chat", lambda route: route.fulfill(
        status=500, content_type="application/json", body="{}"))
    chat.send_message("Hello")
    expect(chat.error_banner).to_be_visible()
    expect(chat.bot_messages).to_have_count(0)
    expect(chat.send_button).to_be_enabled()  # user can retry


def test_slow_response_still_renders(page, chat):
    def slow(route):
        page.wait_for_timeout(3000)  # simulate a slow model
        route.continue_()
    page.route("**/api/chat", slow)
    chat.send_message("Hello")
    expect(chat.typing_indicator).to_be_visible()
    expect(chat.bot_messages).to_have_count(1, timeout=15_000)


def test_network_failure_recovers(page, chat):
    page.route("**/api/chat", lambda route: route.abort())
    chat.send_message("Hello")
    expect(chat.error_banner).to_be_visible()
    page.unroute("**/api/chat")
    chat.ask("Hello")  # works again after the outage
