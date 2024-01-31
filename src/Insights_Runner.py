import subprocess
import os
import psutil
import json
import asyncio
import time
import socket
from pathlib import Path

from src.utils import My_Log

logger = My_Log.Logger()


def get_pid(port):
    connections = psutil.net_connections()
    for con in connections:
        if con.raddr != tuple():
            if con.raddr.port == port:
                return con.pid
        if con.laddr != tuple():
            if con.laddr.port == port:
                return con.pid
    return -1


def check_port(host, port, timeout=2):
    logger.log("checking port: " + str(port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # presumably
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
    except:
        return False
    else:
        sock.close()
        return True


class BESTAPI:
    async def run(self, source_path: str):
        self.API_log = open(My_Log.LOG_PATH + "/APILog.txt", "w")
        # TODO add in support for building api
        # os.chdir(source_path + "/BESTAPI")
        # subprocess.run("msbuild BESTAPI.sln /p:configuration=Release")
        cwd = os.getcwd()
        os.chdir(source_path + "/bin")
        cmd = ["BESTAPI.exe"]
        try:
            self.front_process = await asyncio.create_subprocess_exec(
                *cmd, stdout=self.API_log
            )
        except Exception as e:
            logger.log("Unable To Run Best API")
        os.chdir(cwd)


class Insights_Portal:
    config_json = None
    front, back, BESTAPI = None, None, None

    def __init__(self, source_path: str, config_file: str = None):
        self.front_log_file = open(My_Log.LOG_PATH + "/FrontEndLog.txt", "w")
        self.back_log_file = open(My_Log.LOG_PATH + "/BackEndLog.txt", "w")
        self.kill_front(False)
        self.kill_back(False)
        if config_file is not None:
            with open(config_file) as fp:
                self.config_json = json.load(fp)
            logger.log("Starting to run portal")
            self.BESTAPI = BESTAPI()
            if "insights_source_path" in self.config_json:
                self.set_current_url()
                asyncio.run(self.initialise_portal(source_path))
            if "portal" in self.config_json:
                self.set_current_url(self.config_json["portal"]["url"])

    def __del__(self):
        self.kill_front()
        self.kill_back()
        self.front_log_file.close()
        self.back_log_file.close()
        if self.BESTAPI is not None:
            del self.BESTAPI

    async def initialise_portal(self, source_path):
        await asyncio.gather(
            self.run_front(source_path),
            self.run_back(source_path),
            self.BESTAPI.run(source_path),
        )

    async def run_front(self, source_path: str):
        # TODO add support for npm i
        cwd = os.getcwd()
        os.chdir(source_path + "\\Portal\\src")
        cmd = ["npm.cmd", "run", "serve"]
        self.front_process = await asyncio.create_subprocess_exec(
            *cmd, stdout=self.front_log_file
        )
        os.chdir(cwd)

    def kill_front(self, log_on_fail=True):
        pid = get_pid(8080)
        if pid > 0:
            try:
                p = psutil.Process(pid)
                p.terminate()
                logger.log("Killed Front End")
            except:
                logger.log("kill Failed")
        elif log_on_fail:
            logger.log("Failed to find process on port 8080")

    async def run_back(self, source_path: str):
        # setup BESTAPI config
        if self.config_json is not None and "BESTAPI" in self.config_json:
            bestAPI_config_path = (
                source_path + "/Portal/Server/app/config/bestapi.config.json"
            )
            with open(bestAPI_config_path) as fp:
                api_config = json.load(fp)
            if "HOST" in api_config:
                api_config["HOST"] = self.config_json["BESTAPI"].get(
                    "HOST", api_config["HOST"]
                )
            if "PORT" in api_config:
                api_config["PORT"] = self.config_json["BESTAPI"].get(
                    "PORT", api_config["PORT"]
                )
            if "MQ" in api_config:
                api_config["MQ"] = self.config_json["BESTAPI"].get(
                    "MQ", api_config["MQ"]
                )
            if "TIMEOUT" in api_config:
                api_config["TIMEOUT"] = self.config_json["BESTAPI"].get(
                    "TIMEOUT", api_config["TIMEOUT"]
                )
            with open(bestAPI_config_path, "w") as fp:
                fp.write(json.dumps(api_config, indent=4))

        cwd = os.getcwd()
        os.chdir(source_path + "\\Portal")
        cmd = ["npm.cmd", "run", "start:server"]
        self.front_process = await asyncio.create_subprocess_exec(
            *cmd, stdout=self.back_log_file
        )
        os.chdir(cwd)

    def kill_back(self, log_on_fail=False):
        pid = get_pid(80)
        if pid > 0:
            try:
                p = psutil.Process(pid)
                p.terminate()
                logger.log("Killed Back End")
            except:
                logger.log("kill Failed")
        elif log_on_fail:
            logger.log("Failed to find process on port 80")

    def await_setup(self, return_func, *return_func_args, timeout: int = 60):
        ready = False
        time_waited = 0
        front_ready, back_ready, api_ready = False, False, False
        while not ready:
            if time_waited >= timeout:
                logger.log("Failed To Connect")
                return
            try:
                if not front_ready and check_port("localhost", 8080):
                    front_ready = True
                    logger.log("front ready")
                if not back_ready and check_port("localhost", 80):
                    back_ready = True
                    logger.log("back ready")
                if not api_ready and check_port("localhost", 5500):
                    api_ready = True
                    logger.log("api ready")
            except:
                pass
            ready = front_ready and back_ready and api_ready
            time.sleep(1)
            time_waited += 1
        if ready:
            logger.log(return_func_args)
            return_func(return_func_args)

    def set_current_url(self, url: str = "localhost:8080"):
        with open("src/Current_Config.json") as cc:
            a = cc.read()
            cc_json = json.loads(a)
        cc_json["server"]["url"] = url
        if "users" in self.config_json:
            print(self.config_json["users"])
            cc_json["users"] = self.config_json["users"]
            print("added users")
            print(cc_json)
        with open("src/Current_Config.json", "w") as cc:
            cc.write(json.dumps(cc_json, indent=4))


if __name__ == "__main__":
    i = Insights_Portal(
        "C:/Projects/Insights/Features/31849/Source",
        "C:/Users/DanielMichaeloudis/Documents/BESTM8_Insights/Modules/Module1/config.json",
    )
    i.await_setup(None, None)
