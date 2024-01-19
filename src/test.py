import subprocess
import urllib.request
import os
import tkinter
import socket
from pathlib import Path

try:
    log_path = str(Path.cwd())
    os.chdir("C:/Projects/Insights/Features/31849/Source\\Portal\\src")
    subprocess.run(
        "npm.cmd run serve", stdout=open(log_path + "/logs/FrontEndLog.txt", "w")
    )
except Exception as e:
    print(e)

input("aaa")
