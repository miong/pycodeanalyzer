import pytest

from pycodeanalyzer.core.languages.filedispatcher import FileDispatcher
from pycodeanalyzer.ui.app import UiFileDispatcherListener
from pycodeanalyzer.core.languages.analyzer import Analyzer
from pycodeanalyzer.core.abstraction.objects import AbstractObject

class TestFileDispatcher:

    def test_dispatchRoots(self, mocker):
        cppAnalyzerMock = Analyzer("cppAnalyzerMock")
        pythonAnalyzerMock = Analyzer("pythonAnalyzerMock")
        javaAnalyzerMock = Analyzer("javaAnalyzerMock")
        uiListenerMock = UiFileDispatcherListener()
        abstractObjectsExpected = [AbstractObject("fake", "/home/dir/toto2"), AbstractObject("items", "/home/dir/toto3")]
        roots = [("/home/dir", ["toto", "toto2"]), ("/home/dir2", ["toto3", "toto4"])]
        uiListenerMock.notifyAnalysisEnd = mocker.MagicMock()
        dispatcher = FileDispatcher(cppAnalyzerMock, pythonAnalyzerMock, javaAnalyzerMock, uiListenerMock)
        dispatcher.dispatch = mocker.MagicMock(side_effect=[abstractObjectsExpected, []])
        abstractObjects = dispatcher.dispatchRoots(roots)
        dispatcher.dispatch.assert_has_calls([
            mocker.call(*roots[0]),
            mocker.call(*roots[1]),
        ])
        assert dispatcher.dispatch.call_count == 2
        uiListenerMock.notifyAnalysisEnd.assert_called()
        assert uiListenerMock.notifyAnalysisEnd.call_count == 1
        assert abstractObjects == abstractObjectsExpected

    def test_dispatchCPP(self, mocker):
        totoClassAsbtraction = object()
        toto2ClassAsbtraction = object()
        cppAnalyzerMock = Analyzer("cppAnalyzerMock")
        pythonAnalyzerMock = Analyzer("pythonAnalyzerMock")
        javaAnalyzerMock = Analyzer("javaAnalyzerMock")
        uiListenerMock = UiFileDispatcherListener()
        cppAnalyzerMock.analyze = mocker.MagicMock(side_effect=[[totoClassAsbtraction], [toto2ClassAsbtraction]])
        uiListenerMock.notifyAnalyzing = mocker.MagicMock()
        dispatcher = FileDispatcher(cppAnalyzerMock, pythonAnalyzerMock, javaAnalyzerMock, uiListenerMock)
        abstractObjects = dispatcher.dispatch("/home/dir", ["toto.h", "toto2.hpp"])
        cppAnalyzerMock.analyze.assert_has_calls([
            mocker.call("/home/dir", "toto.h"),
            mocker.call("/home/dir", "toto2.hpp"),
        ])
        assert cppAnalyzerMock.analyze.call_count == 2
        uiListenerMock.notifyAnalyzing.assert_has_calls([
            mocker.call("toto.h"),
            mocker.call("toto2.hpp"),
        ])
        assert uiListenerMock.notifyAnalyzing.call_count == 2
        assert len(abstractObjects) == 2
        assert abstractObjects[0] == totoClassAsbtraction
        assert abstractObjects[1] == toto2ClassAsbtraction

    def test_dispatchPython(self, mocker):
        totoClassAsbtraction = object()
        toto2ClassAsbtraction = object()
        cppAnalyzerMock = Analyzer("cppAnalyzerMock")
        pythonAnalyzerMock = Analyzer("pythonAnalyzerMock")
        javaAnalyzerMock = Analyzer("javaAnalyzerMock")
        uiListenerMock = UiFileDispatcherListener()
        pythonAnalyzerMock.analyze = mocker.MagicMock(side_effect=[[totoClassAsbtraction], [toto2ClassAsbtraction]])
        uiListenerMock.notifyAnalyzing = mocker.MagicMock()
        dispatcher = FileDispatcher(cppAnalyzerMock, pythonAnalyzerMock, javaAnalyzerMock, uiListenerMock)
        abstractObjects = dispatcher.dispatch("/home/dir", ["toto.py", "toto2.py"])
        pythonAnalyzerMock.analyze.assert_has_calls([
            mocker.call("/home/dir", "toto.py"),
            mocker.call("/home/dir", "toto2.py"),
        ])
        assert pythonAnalyzerMock.analyze.call_count == 2
        uiListenerMock.notifyAnalyzing.assert_has_calls([
            mocker.call("toto.py"),
            mocker.call("toto2.py"),
        ])
        assert uiListenerMock.notifyAnalyzing.call_count == 2
        assert len(abstractObjects) == 2
        assert abstractObjects[0] == totoClassAsbtraction
        assert abstractObjects[1] == toto2ClassAsbtraction

    def test_dispatchJava(self, mocker):
        totoClassAsbtraction = object()
        toto2ClassAsbtraction = object()
        cppAnalyzerMock = Analyzer("cppAnalyzerMock")
        pythonAnalyzerMock = Analyzer("pythonAnalyzerMock")
        javaAnalyzerMock = Analyzer("javaAnalyzerMock")
        uiListenerMock = UiFileDispatcherListener()
        javaAnalyzerMock.analyze = mocker.MagicMock(side_effect=[[totoClassAsbtraction], [toto2ClassAsbtraction]])
        uiListenerMock.notifyAnalyzing = mocker.MagicMock()
        dispatcher = FileDispatcher(cppAnalyzerMock, pythonAnalyzerMock, javaAnalyzerMock, uiListenerMock)
        abstractObjects = dispatcher.dispatch("/home/dir", ["toto.java", "toto2.java"])
        javaAnalyzerMock.analyze.assert_has_calls([
            mocker.call("/home/dir", "toto.java"),
            mocker.call("/home/dir", "toto2.java"),
        ])
        assert javaAnalyzerMock.analyze.call_count == 2
        uiListenerMock.notifyAnalyzing.assert_has_calls([
            mocker.call("toto.java"),
            mocker.call("toto2.java"),
        ])
        assert uiListenerMock.notifyAnalyzing.call_count == 2
        assert len(abstractObjects) == 2
        assert abstractObjects[0] == totoClassAsbtraction
        assert abstractObjects[1] == toto2ClassAsbtraction
