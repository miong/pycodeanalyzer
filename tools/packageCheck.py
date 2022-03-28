import subprocess
import os
import platform
import time

pythonCmd = 'python'
if platform.system() == 'Linux' or platform.system() == 'Darwin':
    pythonCmd = 'python3'

def verify(path, data):
    assert subprocess.run(["pycodeanalyzer", "--no-ui", "--dumpobj", path]).returncode == 0
    subprocess.run([pythonCmd, "tools/dumpobjAnon.py"])
    time.sleep(2)
    text = open("./dumpobj.json", "r").read().strip().replace("\r\n", "\n")
    expected = open(data, "r").read().strip().replace("\r\n", "\n")
    assert text == expected

def main():
    verify("./tests/ressources/code/cpp_zlib","./tests/ressources/zlib_dumpobj.json")
    verify("pycodeanalyzer", "./tests/ressources/pycodeanalyzer_dumpobj.json")

if __name__ == "__main__":
    main()
