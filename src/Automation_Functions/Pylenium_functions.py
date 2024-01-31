import os
import json
import re
from playwright.sync_api import Page, expect, sync_playwright, Playwright
from pylenium.driver import Pylenium
from pylenium.config import PyleniumConfig

# TODO not current config, do this some other way
with open(os.getcwd() + "\src\Current_Config.json", mode="rb") as fp:
    CONFIG = json.load(fp)

PORTAL_URL = "http://" + CONFIG["server"]["url"]


class Test_Environment:
    def __init__(self, browser: str = "chrome", headless: bool = True):
        self.config = PyleniumConfig()
        self.py = Pylenium(self.config)

    def __del__(self):
        self.py.quit()

    def load_insights_portal(self):
        print("Loading Page: " + PORTAL_URL)
        self.py.visit(PORTAL_URL)

    def enter_text_into_textbox_by_name(self, name: str, text_to_enter: str):
        textbox = self.py.contains(name)
        if textbox.tag_name() == "input" or textbox.tag_name() == "textbox":
            textbox.type(text_to_enter)
            return
        if textbox.tag_name() == "label":
            id = textbox.get_attribute("for")
            textbox = self.py.get("#" + id)
            textbox.type(text_to_enter)

    def click_button_with_text(self, text: str):
        button = self.py.contains(text)
        return button.click()

    def check_for_title(self, title: str):
        try:
            print(self.py.title())
            return self.py.title() == title
        except Exception as e:
            print("Unexpected error:")
            print(e)
            return False

    def run_and_log_in(self, user_id=0, username=None, password=None):
        if password is None:
            if "users" in CONFIG:
                if user_id in CONFIG["users"]:
                    username = CONFIG["users"][user_id]["username"]
                    password = CONFIG["users"][user_id]["password"]
                else:
                    print(CONFIG)
                    return False, "User Not Found"
            else:
                return False, "No Users Found"

        self.load_insights_portal()
        self.enter_text_into_textbox_by_name("Name", username)
        self.enter_text_into_textbox_by_name("Password", password)
        self.click_button_with_text("Log In")
        try:
            self.py.wait().until(lambda _: self.py.title() == "BEST Insights - Home")
            return True, "Success"
        except:
            print("login Failed, title = " + self.py.title())
        try:
            self.py.contains("Incorrect username and password")
            return False, "Login Fail, incorrect Username/Password"
        except:
            return False, "Unknown Error"


if __name__ == "__main__":
    pw = sync_playwright().start()
    page = pw.chromium.launch().new_page()
    page.goto("http://localhost:8080")
