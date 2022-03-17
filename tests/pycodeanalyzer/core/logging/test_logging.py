import pytest

import logging
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory

class TestLoggerFactory:

    def test_init(self):
        LoggerFactory.init()
        assert logging.root == LoggerFactory.defaultLogger
        assert logging.root.level == logging.INFO

    def test_setLoggerLevel(self):
        LoggerFactory.init()
        assert logging.root == LoggerFactory.defaultLogger
        assert logging.root.level == logging.INFO
        LoggerFactory.setLoggerLevel("DEBUG")
        assert logging.root.level == logging.DEBUG
        LoggerFactory.setLoggerLevel("INFO")
        assert logging.root.level == logging.INFO
        LoggerFactory.setLoggerLevel("WARNING")
        assert logging.root.level == logging.WARNING
        LoggerFactory.setLoggerLevel("ERROR")
        assert logging.root.level == logging.ERROR
        with pytest.raises(ValueError):
            LoggerFactory.setLoggerLevel("TOTO")
