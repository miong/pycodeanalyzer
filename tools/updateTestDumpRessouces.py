import subprocess
import os
import platform
import time
import shutil

pythonCmd = 'python'
if platform.system() == 'Linux' or platform.system() == 'Darwin':
    pythonCmd = 'python3'

def update(path, ressouce):
    try:
        assert subprocess.run([pythonCmd, "-m", "pycodeanalyzer", "--no-ui", "--dumpobj", path]).returncode == 0
        assert subprocess.run([pythonCmd, "tools/dumpobjAnon.py"]).returncode == 0
    except AssertionError:
        print("Error wile dumping the source from", path)
        exit(1)
    time.sleep(2)
    shutil.move("dumpobj.json", ressouce)

def main():
    update("./tests/ressources/code/cpp_zlib","./tests/ressources/cpp_zlib_dumpobj.json")
    update("./tests/ressources/code/java_zlib","./tests/ressources/java_zlib_dumpobj.json")
    update("./tests/ressources/code/kotlin_android_clean_architecture","./tests/ressources/kotlin_android_clean_architecture_dumpobj.json")
    update("pycodeanalyzer", "./tests/ressources/pycodeanalyzer_dumpobj.json")

if __name__ == "__main__":
    main()
