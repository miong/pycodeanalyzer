import pytest
import argparse

from pycodeanalyzer.core.console.console import Console
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory

class Object(object):
    pass

class TestConsole:

    def test_init(self, mocker):
        args = Object()
        args.loglevel = 0
        savedInit = LoggerFactory.init
        savedSetLoggerLevel = LoggerFactory.setLoggerLevel
        LoggerFactory.init = mocker.MagicMock(return_value=None)
        LoggerFactory.setLoggerLevel = mocker.MagicMock(return_value=None)
        console = Console()
        console._parseArgs = mocker.MagicMock(return_value=args)
        console.init()
        initCount = LoggerFactory.init.call_count
        setLoggerLevelCount = LoggerFactory.setLoggerLevel.call_count
        LoggerFactory.init = savedInit
        LoggerFactory.setLoggerLevel = savedSetLoggerLevel
        assert initCount == 1
        assert setLoggerLevelCount == 1

    def test_loglevel(self, mocker):
        args = Object()
        args.loglevel = 18
        savedInit = LoggerFactory.init
        savedSetLoggerLevel = LoggerFactory.setLoggerLevel
        LoggerFactory.init = mocker.MagicMock(return_value=None)
        LoggerFactory.setLoggerLevel = mocker.MagicMock(return_value=None)
        console = Console()
        console._parseArgs = mocker.MagicMock(return_value=args)
        console.init()
        initCount = LoggerFactory.init.call_count
        setLoggerLevelCount = LoggerFactory.setLoggerLevel.call_count
        setLoggerLevelMock = LoggerFactory.setLoggerLevel
        LoggerFactory.init = savedInit
        LoggerFactory.setLoggerLevel = savedSetLoggerLevel
        assert initCount == 1
        assert setLoggerLevelCount == 1
        setLoggerLevelMock.assert_has_calls([
            mocker.call(18),
        ])

    def test_run(self, mocker):
        args = Object()
        args.loglevel = "INFO"
        engineMock = Object()
        engineMock.run = mocker.MagicMock(return_value=None)
        console = Console()
        console._parseArgs = mocker.MagicMock(return_value=args)
        console.init()
        console.run(engineMock)
        engineMock.run.assert_has_calls([
            mocker.call(args),
        ])
