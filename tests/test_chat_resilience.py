# Resilience tests: how does the UI behave when the backend misbehaves?
# page.route() intercepts the browser's network call, so we can fake
# failures without changing the app.
import pytest
from playwright.sync_api import expect

pytestmark = pytest.mark.resilience

# Server error: the API returns HTTP 500. The user should see an error
# message, no fake bot reply, and the Send button should come back so
# they can retry.
def test_server_error_shows_friendly_message(page, chat):
    page.route("**/api/chat", lambda route: route.fulfill(
        status=500, content_type="application/json", body="{}"))
    chat.send_message("Hello")
    expect(chat.error_banner).to_be_visible()
    expect(chat.bot_messages).to_have_count(0)
    expect(chat.send_button).to_be_enabled()  # user can retry


# Slow model: the request is delayed 3 seconds. The typing indicator should
# show while waiting, and the reply should still render when it arrives.
def test_slow_response_still_renders(page, chat):
    def slow(route):
        page.wait_for_timeout(3000)  # simulate a slow model
        route.continue_()
    page.route("**/api/chat", slow)
    chat.send_message("Hello")
    expect(chat.typing_indicator).to_be_visible()
    expect(chat.bot_messages).to_have_count(1, timeout=15_000)



# Network failure and recovery: the request is aborted, so the user sees an
# error. After removing the fake failure, a new message works again,
# which proves the UI recovers without a page reload.
def test_network_failure_recovers(page, chat):
    page.route("**/api/chat", lambda route: route.abort())
    chat.send_message("Hello")
    expect(chat.error_banner).to_be_visible()
    page.unroute("**/api/chat")
    chat.ask("Hello")  # works again after the outage
