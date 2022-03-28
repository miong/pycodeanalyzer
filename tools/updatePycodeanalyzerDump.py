import subprocess
import os
import platform
import time
import shutil

pythonCmd = 'python'
if platform.system() == 'Linux' or platform.system() == 'Darwin':
    pythonCmd = 'python3'

def update():
    try:
        assert subprocess.run(["pycodeanalyzer", "--no-ui", "--dumpobj", "pycodeanalyzer"]).returncode == 0
        assert subprocess.run([pythonCmd, "tools/dumpobjAnon.py"]).returncode == 0
    except AssertionError:
        print("Error wile dumping the source from pycodeanalyzer")
        exit(1)
    time.sleep(2)
    shutil.move("dumpobj.json", "./tests/ressources/pycodeanalyzer_dumpobj.json")

def main():
    update()

if __name__ == "__main__":
    main()
