import Ninja, json, time
from Print import Print
from playwright.sync_api import sync_playwright


class NinjaAuth:

    def __init__(self):
        self.headers = None
        self.metadata = {}

    def set_metadata(self, page):
        try:

            cookies = page.context.cookies()

            local_cookies = ["HyojiMode=1", "HyojiSu=999"]

            for cookie in cookies: local_cookies.append(f"{cookie['name']}={cookie['value']}")

            self.headers = {
                "Cookie": '; '.join(local_cookies),
                "User-Agent": page.evaluate(f"navigator.userAgent;"),
                **json.load(open('headers_default.json'))
            }

            memberCode = page.locator("#memberCode").input_value()

            branchCode = page.locator("#branchCode").input_value()

            buyerId = page.locator("#buyerId").input_value()

            self.metadata = {"memberCode": memberCode, "branchCode": branchCode, "buyerId": buyerId}

        except Exception as e:
            Print.error(e)

    def auth(self):

        Print.log('[+] Authorizing')
        login = "****************"
        pwd = "****************"

        try:
            with sync_playwright() as playwright:

                browser = playwright.chromium.launch(headless=False)

                page = browser.new_page()

                page.goto("https://www.ninja-cartrade.jp")

                page.locator("#loginId").fill(login)

                page.locator("#password").fill(pwd)

                page.locator('xpath=//a[@onclick="login()"]').click()

                counter = 0

                while counter < 500:

                    time.sleep(1)

                    if self.redirect_handle(page): break

                    counter += 1

        except Exception as e:
            Print.error(e)

    def redirect_handle(self, page):

        try:
            res = page.evaluate("window.location.href")

            if "https://www.ninja-cartrade.jp/ninja/login.action" in res:

                res_text = page.locator('xpath=//div[@class="resultText"]')

                if "A different user is already logged in with this login ID" in res_text.inner_text():

                    page.locator('xpath=//a[@onclick="seniToSearchcondition();return false"]').click()

                    self.set_metadata(page)

                    return True
                
                else:
                    Print.ok("[+] good session! is that still not panic?")

        except Exception as e:
            Print.error( e)