from playwright.sync_api import Page, expect


class ChatPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.input = page.locator('[data-test="message-input"]')
        self.send_button = page.locator('[data-test="send-button"]')
        self.typing_indicator = page.locator('[data-test="typing-indicator"]')
        self.error_banner = page.locator('[data-test="error-banner"]')
        self.user_messages = page.locator('[data-test="message-user"]')
        self.bot_messages = page.locator('[data-test="message-bot"]')

    def open(self) -> None:
        self.page.goto("/")

    def send_message(self, text: str) -> None:
        self.input.fill(text)
        self.send_button.click()

    def last_response(self) -> str:
        return self.bot_messages.last.inner_text()

    def ask(self, text: str, timeout: int = 10_000) -> str:
        """Send a message, wait for exactly one new bot reply, return its text."""
        before = self.bot_messages.count()
        self.send_message(text)
        expect(self.bot_messages).to_have_count(before + 1, timeout=timeout)
        return self.last_response()
