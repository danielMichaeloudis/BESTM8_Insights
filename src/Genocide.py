import psutil


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


def murder(pid):
    if pid > 0:
        try:
            p = psutil.Process(pid)
            p.terminate()
            print("Killed " + str(pid))
        except:
            print("kill Failed")
    else:
        print("Failed to find process " + str(pid))


# ! this will kill processes using ports 8080 and 80, do not run if there is anything important on them
if __name__ == "__main__":
    # Kill front end
    pid = get_pid(8080)
    murder(pid)
    # Kill Back end
    pid = get_pid(80)
    murder(pid)
