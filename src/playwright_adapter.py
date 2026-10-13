import time
from typing import Callable

from playwright.sync_api import Frame, Locator, Page, TimeoutError as PlaywrightTimeoutError


class By:
    CSS_SELECTOR = "css selector"
    XPATH = "xpath"
    ID = "id"
    TAG_NAME = "tag name"


def _selector(by: str, value: str) -> str:
    if by == By.XPATH:
        return f"xpath={value}"
    if by == By.ID:
        return f"#{value}"
    if by == By.TAG_NAME:
        return value
    if by == By.CSS_SELECTOR:
        return value
    raise ValueError(f"Unsupported locator strategy: {by}")


class PlaywrightElement:
    def __init__(self, locator: Locator):
        self._locator = locator

    @property
    def text(self) -> str:
        return self._locator.inner_text()

    def get_attribute(self, name: str) -> str | None:
        if name == "href":
            return self._locator.evaluate(
                "(element) => element.href || null"
            )
        return self._locator.get_attribute(name)

    def find_element(self, by: str, value: str) -> "PlaywrightElement":
        return PlaywrightElement(self._locator.locator(_selector(by, value)).first)

    def find_elements(self, by: str, value: str) -> list["PlaywrightElement"]:
        elements = self._locator.locator(_selector(by, value))
        return [PlaywrightElement(elements.nth(index)) for index in range(elements.count())]

    def click(self) -> None:
        self._locator.click()

    def is_displayed(self) -> bool:
        return self._locator.is_visible()


class _FrameSwitcher:
    def __init__(self, page: "PlaywrightPageAdapter"):
        self._page = page

    def frame(self, iframe: PlaywrightElement) -> None:
        element_handle = iframe._locator.element_handle()
        if element_handle is None:
            raise RuntimeError("Iframe is no longer attached to the page")
        frame = element_handle.content_frame()
        if frame is None:
            raise RuntimeError("Unable to access iframe content")
        self._page._context = frame

    def default_content(self) -> None:
        self._page._context = self._page._page


class PlaywrightPageAdapter:
    def __init__(self, page: Page):
        self._page = page
        self._context: Page | Frame = page
        self.switch_to = _FrameSwitcher(self)

    def get(self, url: str) -> None:
        self._page.goto(url, wait_until="domcontentloaded", timeout=60_000)

    def implicitly_wait(self, seconds: float) -> None:
        self._page.set_default_timeout(seconds * 1_000)

    def find_element(self, by: str, value: str) -> PlaywrightElement:
        return PlaywrightElement(self._context.locator(_selector(by, value)).first)

    def find_elements(self, by: str, value: str) -> list[PlaywrightElement]:
        elements = self._context.locator(_selector(by, value))
        return [PlaywrightElement(elements.nth(index)) for index in range(elements.count())]

    def execute_script(self, script: str, *args):
        if args:
            if all(isinstance(argument, PlaywrightElement) for argument in args):
                element = args[0]
                body = script.replace("arguments[0]", "element")
                return element._locator.evaluate(f"(element) => {{ {body} }}")
            return self._context.evaluate(
                f"(args) => {{ return (function() {{ {script} }}).apply(null, args); }}",
                list(args),
            )
        return self._context.evaluate(f"() => {{ {script} }}")

    def close(self) -> None:
        self._page.close()

    quit = close


class PlaywrightWait:
    def __init__(self, page: PlaywrightPageAdapter, timeout: float, poll_interval: float = 0.1):
        self.page = page
        self.timeout = timeout
        self.poll_interval = poll_interval

    def until(self, condition: Callable[[PlaywrightPageAdapter], object]):
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            try:
                result = condition(self.page)
            except PlaywrightTimeoutError:
                result = False
            if result:
                return result
            time.sleep(self.poll_interval)
        raise TimeoutError("Playwright condition was not satisfied before the timeout")


class PlaywrightConditions:
    @staticmethod
    def presence_of_element_located(locator: tuple[str, str]):
        def condition(page: PlaywrightPageAdapter):
            element = page.find_element(*locator)
            return element if element._locator.count() else False

        return condition

    @staticmethod
    def presence_of_all_elements_located(locator: tuple[str, str]):
        def condition(page: PlaywrightPageAdapter):
            elements = page.find_elements(*locator)
            return elements or False

        return condition
