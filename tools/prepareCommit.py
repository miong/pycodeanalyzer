import subprocess
import os
import platform

from updateReadme import updateReadme

pythonCmd = 'python'
if platform.system() == 'Linux' or platform.system() == 'Darwin':
    pythonCmd = 'python3'

def runISort():
    return subprocess.run(["isort", "pycodeanalyzer"]).returncode == 0

def runBlack():
    return subprocess.run(["black", "pycodeanalyzer"]).returncode == 0

def runUT():
    res = subprocess.run(["coverage","run","--source=pycodeanalyzer","-m","pytest","-vv", os.path.join("tests", "pycodeanalyzer")]).returncode == 0
    if res:
        subprocess.run(["coverage","report","-m"])
    return res

def runMypy():
    return subprocess.run(["mypy","--config-file",".mypy.ini","pycodeanalyzer"]).returncode == 0

def runQA():
    res = subprocess.run(["flake8","pycodeanalyzer","--count","--select=E9,F63,F7,F82,F401","--show-source","--statistics"]).returncode == 0
    if res:
        subprocess.run(["flake8","pycodeanalyzer","--count","--ignore=E203,W503","--exit-zero","--max-complexity=20","--max-line-length=127","--statistics"])
    return res

def runUpdateDocs():
    res = subprocess.run(["sphinx-apidoc","-o","docs/source/code","pycodeanalyzer"]).returncode == 0
    return res

def runUpdateReadme():
    updateReadme()

def main():
    print("Preparing to commit")
    if not runISort():
        print("Isort not passing, it's strange...")
        exit(1)
    print("Isort done")
    if not runBlack():
        print("Black not passing, it's strange...")
        exit(1)
    print("Black done")
    if not runMypy():
        print("Mypy not passing, fix before commit")
        exit(1)
    print("Mypy passing")
    if not runUpdateDocs():
        print("Failed to update the documentation, fix before commit")
        exit(1)
    print("Source code documentation updated")
    if not runUT():
        print("Unit test not passing, fix before commit")
        exit(1)
    print("Unit test passing")
    if not runQA():
        print("QA is not passing, fix before commit")
        exit(1)
    print("QA is passing")
    runUpdateReadme()

if __name__ == "__main__":
    main()
