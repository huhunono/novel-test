from playwright.sync_api import Page, expect


class LoginPage:
    """Page Object for the login page (/user/login.html).

    Encapsulates all login form interactions and post-login assertions.
    Other layers (Flow, Test) should never access login DOM elements directly.
    """

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        """Navigate to the login page."""
        self.page.goto(f"{self.base_url}/user/login.html")

    def login(self, username: str, password: str) -> None:
        """Fill in credentials and click the login button."""
        self.page.get_by_placeholder("手机号码").fill(username)
        self.page.get_by_placeholder("密码").fill(password)
        self.page.get_by_role("button", name="登录").click()

    def assert_login_success(self) -> None:
        """Verify the user has been redirected away from login page."""
        expect(self.page).not_to_have_url(f"{self.base_url}/user/login.html")
        expect(self.page.get_by_role("link", name="我的书架")).to_be_visible()
        expect(self.page.get_by_role("link", name="退出")).to_be_visible()

    def assert_login_failed(self) -> None:
        """Verify the user is still on login page with an error message."""
        expect(self.page).to_have_url(f"{self.base_url}/user/login.html")
        expect(self.page.locator("#LabErr")).to_have_text("手机号或密码错误！")