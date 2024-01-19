import tkinter as tk
import pyuac
import sys
import subprocess
import os
import win32com
import ctypes

from src.utils import logger
from src.GUI import BESTM8


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


try:
    # ! this will kill processes using ports 8080 and 80, do not run if there is anything important on them
    if __name__ == "__main__":
        logger.log(os.getcwd())
        input("aaa")
        if not is_admin():
            print("relaunching as Admin")
            pyuac.runAsAdmin()
            sys.exit(0)
        logger.clear_log()
        root = tk.Tk()
        app = BESTM8(root)
        root.mainloop()
except Exception as e:
    input(e)
