import json
from pathlib import Path


class Module:
    name: str = ""
    path: str = ""

    def __init__(self, **kwargs):
        if "path" in kwargs:
            with open(kwargs["path"] + "/config.json", "r") as fp:
                current_module = json.load(fp)
                print(current_module)

            self.name = current_module.get("name")
            self.insights_source_path = current_module.get("insights_source_path")
