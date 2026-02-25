# ...existing code...
from typing import Optional

class DriverFactory:
    """Wrapper around pytest-playwright's `page` fixture. Do not call sync_playwright() here."""

    def __init__(self, page, config: Optional[dict] = None):
        self.page = page
        self.config = config or {}

    def screenshot(self, path: str):
        return self.page.screenshot(path=path)

    def set_timeout(self, ms: int):
        return self.page.set_default_timeout(ms)

    def goto(self, url: str):
        return self.page.goto(url)

    def get_page(self):
        return self.page
# ...existing code...