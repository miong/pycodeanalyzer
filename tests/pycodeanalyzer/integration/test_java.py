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

class TestJavaIntegration:

    def test_java_analysis(self, mocker):
        if os.path.exists("./dumpobj.json"):
            os.remove("./dumpobj.json")
        engine = injector.get(Engine)
        args = Object()
        args.dumpobj = True
        args.no_ui = True
        args.loglevel = "DEBUG"
        args.path = ["tests/ressources/code/java_zlib"]
        args.exportPath = None
        args.configfile = None
        args.templatefile = None
        engine.run(args)
        assert subprocess.run([pythonCmd, "tools/dumpobjAnon.py"]).returncode == 0
        time.sleep(2)
        text = open("./dumpobj.json", "r").read().strip().replace("\r\n", "\n")
        expected = open("./tests/ressources/java_zlib_dumpobj.json", "r").read().strip().replace("\r\n", "\n")
        assert text == expected
