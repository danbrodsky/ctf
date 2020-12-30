import os
import subprocess
from time import sleep


def bash(cmd):
    return subprocess.check_output(cmd).decode("UTF-8")


visited = []
os.chdir("/mnt/")


def dfs(pathname, dirname):
    try:
        # print(os.getcwd())
        inode = os.popen("/bin/stat -c '%i' " + str(dirname)).read()
        if "links" in inode:
            raise EOFError
    except:
        return
    if inode in visited:
        return
    os.chdir(pathname)
    visited.append(inode)
    print(visited)

    for f in os.listdir():
        if f == "MATCH":
            print(pathname)
            sleep(1000)

        try:
            inode = os.popen("/bin/stat -c '%i' " + str(f)).read()
            if "links" in inode:
                raise EOFError
            dfs(pathname + "/" + f, f)
        except:
            continue


dfs("/mnt/test", "test")
