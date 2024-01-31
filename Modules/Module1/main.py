import os
import sys

sys.path.append(os.getcwd())
from src.Automation_Functions.Pylenium_functions import *


def test1():
    print("running test 1, module 1")
    my_environment = Test_Environment()
    res = my_environment.run_and_log_in("admin")
    if res[0]:
        print("Success")
    else:
        print("Fail")
        print(res[1])


if __name__ == "__main__":
    test1()
