import pytest
import subprocess
import time
import os
import platform

from pycodeanalyzer.injection import injector
from pycodeanalyzer.core.engine.engine import Engine

pythonCmd = 'python'
if platform.system() == 'Linux' or platform.system() == 'Darwin':
    pythonCmd = 'python3'

class Object(object):
    pass

class TestPythonIntegration:

    def test_python_analysis(self, mocker):
        if os.path.exists("./dumpobj.json"):
            os.remove("./dumpobj.json")
        engine = injector.get(Engine)
        args = Object()
        args.dumpobj = True
        args.no_ui = True
        args.loglevel = "DEBUG"
        args.path = ["pycodeanalyzer"]
        engine.run(args)
        subprocess.run([pythonCmd, "tools/dumpobjAnon.py"])
        time.sleep(2)
        text = open("./dumpobj.json", "r").read().strip()
        expected = open("./tests/ressources/pycodeanalyzer_dumpobj.json", "r").read().strip()
        assert text == expected
