from utils.logger import get_logger


class BasePage:

    def __init__(self, page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def click(self, locator):
        self.logger.info(f"Clicking on: {locator}")
        self.page.locator(locator).click()

    def type(self, locator, text):
        self.logger.info(f"Typing into: {locator}")
        self.page.locator(locator).fill(text)

    def get_text(self, locator):
        self.logger.info(f"Getting text from: {locator}")
        return self.page.locator(locator).inner_text()
