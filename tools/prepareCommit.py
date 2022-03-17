import subprocess
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
    res = subprocess.run(["coverage","run","--source=pycodeanalyzer","-m","pytest","-v","tests/pycodeanalyzer"]).returncode == 0
    if res:
        subprocess.run(["coverage","report","-m"])
    return res

def runQA():
    res = subprocess.run(["flake8","pycodeanalyzer","--count","--select=E9,F63,F7,F82","--show-source","--statistics"]).returncode == 0
    if res:
        subprocess.run(["flake8","pycodeanalyzer","--count","--ignore=E203,W503","--exit-zero","--max-complexity=20","--max-line-length=127","--statistics"])
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
