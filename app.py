import tkinter as tk
import pyuac
import sys
import subprocess
import os
import win32com
import ctypes

from src.utils import Logger
from src.GUI import BESTM8


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# ! this will kill processes using ports 8080 and 80, do not run if there is anything important on them
if __name__ == "__main__":
    Logger = Logger()
    Logger.log(os.getcwd())
    if not is_admin():
        print("relaunching as Admin")
        pyuac.runAsAdmin()
        sys.exit(0)
    Logger.clear_log()
    root = tk.Tk()
    app = BESTM8(root)
    root.mainloop()
try:
    pass
except Exception as e:
    input(e)
