import pytest
import subprocess
import time
import os

from pycodeanalyzer.injection import injector
from pycodeanalyzer.core.engine.engine import Engine

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
        subprocess.run(["python3", "tools/dumpobjAnon.py"])
        time.sleep(2)
        text = open("./dumpobj.json", "r").read().strip()
        expected = open("./tests/ressources/pycodeanalyzer_dumpobj.json", "r").read().strip()
        assert text == expected
