import subprocess
import os
import platform
import time
import difflib

pythonCmd = 'python'
if platform.system() == 'Linux' or platform.system() == 'Darwin':
    pythonCmd = 'python3'

def verify(path, data):
    try:
        assert subprocess.run(["pycodeanalyzer", "--no-ui", "--dumpobj", path]).returncode == 0
        assert subprocess.run([pythonCmd, "tools/dumpobjAnon.py"]).returncode == 0
    except AssertionError:
        print("Error wile dumping the source from", path)
        exit(1)
    time.sleep(2)
    text = open("./dumpobj.json", "r").read().strip().replace("\r\n", "\n")
    expected = open(data, "r").read().strip().replace("\r\n", "\n")
    try:
        assert text == expected
    except AssertionError:
        print("Result differs from expectation :")
        for line in difflib.unified_diff(expected.splitlines(), text.splitlines()):
            print(line)
        exit(1)

def main():
    verify("./tests/ressources/code/cpp_zlib","./tests/ressources/zlib_dumpobj.json")
    verify("pycodeanalyzer", "./tests/ressources/pycodeanalyzer_dumpobj.json")

if __name__ == "__main__":
    main()
