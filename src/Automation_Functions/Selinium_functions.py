import os
import json
import re
from playwright.sync_api import Page, expect, sync_playwright, Playwright
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# TODO not current config, do this some other way
with open(os.getcwd() + "\src\Current_Config.json", mode="rb") as fp:
    CONFIG = json.load(fp)

PORTAL_URL = CONFIG["server"]["url"]


class Test_Environment:
    def __init__(self, browser: str = "chrome", headless: bool = True):
        self.selenium = webdriver.Chrome()

    def __del__(self):
        self.selenium.close()

    def load_insights_portal(self):
        print("Loading Page: " + PORTAL_URL)
        self.selenium.get("http://" + PORTAL_URL)

    def enter_text_into_textbox_by_name(self, name: str, text_to_enter: str):
        element = self.selenium.find_element(By.ID, name)
        element.send_keys(text_to_enter)

    def click_button_with_text(self, text: str):
        button = self.selenium.find_element(By.CLASS_NAME, text)
        button.click()

    def check_for_title(self, title: str):
        try:
            element = WebDriverWait(self.selenium, 10).until(EC.title_contains(title))
            return True
        except Exception as e:
            print(e)
            error_message = e.args[0]
            error_match = re.search(r"Actual value: (.*)", error_message)
            if error_match:
                print("Unexpected Title Found: " + error_match.group(1))
            else:
                print("Unexpected error")
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
        if not self.check_for_title("BEST Insights - Login"):
            return False, "Unable to initialise page"
        self.enter_text_into_textbox_by_name("input-28", username)
        self.enter_text_into_textbox_by_name("input-31", password)
        self.click_button_with_text("v-btn--is-elevated")
        if self.check_for_title("BEST Insights - Home"):
            return True, "Success"
        try:
            # expect(
            #    self.page.get_by_text("Incorrect username and password")
            # ).to_be_visible
            return False, "Login Fail, incorrect Username/Password"
        except:
            return False, "Unknown Error"


if __name__ == "__main__":
    pw = sync_playwright().start()
    page = pw.chromium.launch().new_page()
    page.goto("http://localhost:8080")
