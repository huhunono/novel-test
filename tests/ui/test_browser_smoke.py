from tests.data.users import VALID_USER

def test_login_submit_only(browser_page, base_url):
    browser_page.goto(f"{base_url}/user/login.html", wait_until="domcontentloaded", timeout=10000)

    print("step 1: fill username")
    browser_page.locator("#txtUName").fill(VALID_USER["username"])

    print("step 2: fill password")
    browser_page.locator("#txtPassword").fill(VALID_USER["password"])

    print("step 3: click login")
    browser_page.locator("#btnLogin").click()

    browser_page.wait_for_timeout(3000)
    print("step 4: current url:", browser_page.url)
    print("step 5: body text:")
    print(browser_page.locator("body").inner_text()[:1500])