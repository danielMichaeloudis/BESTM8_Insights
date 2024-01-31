import datetime
from pathlib import Path

LOG_PATH = str(Path.cwd()) + "/src/logs"


class Logger:
    def log(self, message: str):
        with open(LOG_PATH + "/M8_LOG.txt", "a") as log_file:
            log_file.write(
                f"[{datetime.datetime.now().time().isoformat(timespec='milliseconds')}]: {message}\n"
            )

    def clear_log(self):
        with open(LOG_PATH + "/M8_LOG.txt", "w") as log_file:
            log_file.write("")
