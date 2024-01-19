import os
import sys

print(os.getcwd())
sys.path.append(os.getcwd())
from src.Automation_Functions.Playwright_functions import *


def test1():
    print("running test 1")
    input("aaaaaaa")
    my_environment = Test_Environment()
    my_environment.load_insights_portal()
    my_environment.enter_text_into_textbox_by_name("username", "sysadmin")
    my_environment.enter_text_into_textbox_by_name("password", "password")
    my_environment.click_button_with_text("Log In")
    print(my_environment.check_for_title("BEST Insights - Debrief"))


if __name__ == "__main__":
    print("running main")
    test1()
