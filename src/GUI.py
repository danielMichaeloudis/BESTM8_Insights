import tkinter as tk
from tkinter import ttk
import re
import os
from pathlib import Path

from src.Module import Module
from src.Insights_Runner import *
from src.utils import Logger

logger = Logger()


class BESTM8:
    MODULES_PATH = str(Path.cwd()) + r"/Modules/"
    CWD = str(Path.cwd())

    def __init__(self, root):
        self.root = root
        self.run_button = tk.Button(root, text="Run", command=self.show_modules)
        self.create_template_button = tk.Button(
            root, text="Create Template", command=self.create_template
        )

        self.run_button.pack()
        self.create_template_button.pack()

    def show_modules(self):
        self.module_list = tk.Toplevel(self.root)
        self.modules = os.listdir(self.MODULES_PATH)
        self.modules_tree = ttk.Treeview(
            self.module_list,
            columns="Module",
            height=20,
            selectmode="extended",
        )
        self.modules_tree.pack(padx=5, pady=5)
        i = 0
        print(self.modules)
        for module in self.modules:
            self.modules_tree.insert(
                "",
                tk.END,
                iid=i,
                text=module,
            )
            i += 1
        self.run_module_button = tk.Button(
            self.module_list,
            text="Run Module",
            command=self.setup_insights,
        )
        self.run_module_button.pack()

    def setup_insights(self):
        module = self.modules_tree.item(self.modules_tree.selection()[0])["text"]
        self.current_module = Module(path=self.MODULES_PATH + module)
        self.insights_portal = Insights_Portal(
            self.current_module.insights_source_path,
            self.MODULES_PATH + module + "/config.json",
        )
        self.insights_portal.await_setup(self.run_module, module)
        self.module_list.destroy()

    def run_module(self, module):
        # TODO Multiple modules concurrently
        logger.log("Running Module")
        os.chdir(self.CWD)
        subprocess.run(
            ["python", self.MODULES_PATH + module[0] + "/main.py"],
            stdout=open(self.MODULES_PATH + module[0] + "/log.log", "w"),
        )

    def create_template(self):
        pass
