import os
import tomllib
import asyncio
from playwright.sync_api import Page, expect, sync_playwright, Playwright

# TODO not current config, do this some other way
with open(os.getcwd() + "\src\Current_Config.toml", mode="rb") as fp:
    CONFIG = tomllib.load(fp)

PORTAL_URL = CONFIG["server"]["portalHost"] + ":" + CONFIG["server"]["portalPort"]


class Test_Environment:
    def __init__(self, browser: str = "chrome"):
        self.playwright = sync_playwright().start()
        self.page = self.playwright.chromium.launch().new_page()

    def __del__(self):
        self.playwright.stop()

    def load_insights_portal(self):
        print("Loading Page: " + PORTAL_URL)
        self.page.goto(PORTAL_URL)

    def enter_text_into_textbox_by_name(self, name: str, text_to_enter: str):
        self.page.get_by_role("textbox", name=name).fill(text_to_enter)

    def click_button_with_text(self, text: str):
        self.page.get_by_role("button", name=text)

    def check_for_title(self, title: str):
        try:
            expect(self.page).to_have_title(title)
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == "__main__":
    pw = sync_playwright().start()
    page = pw.chromium.launch().new_page()
    page.goto("http://localhost:8080")
