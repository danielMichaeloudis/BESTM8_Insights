import os
import sys

sys.path.append(os.getcwd())
from src.Automation_Functions.Playwright_functions import *


def test1():
    print("running test 1, Module 2")
    my_environment = Test_Environment(headless=True)
    print("created test env")
    my_environment.load_insights_portal()
    print("loaded portal")
    my_environment.enter_text_into_textbox_by_name("Name", "sysadmin")
    print("input username")
    my_environment.enter_text_into_textbox_by_name("Password", "password")
    print("input password")
    my_environment.click_button_with_text("Log In")
    print("clicked log in")
    print(my_environment.check_for_title("BEST Insights - Home"))
    print("done!!!")


if __name__ == "__main__":
    print("running main")
    test1()
