import pytest

from pycodeanalyzer.core.languages.filedispatcher import FileDispatcher
from pycodeanalyzer.ui.app import UiFileDispatcherListener
from pycodeanalyzer.core.languages.analyzer import Analyzer

class TestFileDispatcher:

    def test_dispatchCPP(self, mocker):
        totoClassAsbtraction = object()
        toto2ClassAsbtraction = object()
        cppAnalyzerMock = Analyzer()
        uiListenerMock = UiFileDispatcherListener()
        cppAnalyzerMock.analyze = mocker.MagicMock(side_effect=[[totoClassAsbtraction], [toto2ClassAsbtraction]])
        uiListenerMock.notifyAnalyzing = mocker.MagicMock()
        uiListenerMock.notifyAnalysisEnd = mocker.MagicMock()
        dispatcher = FileDispatcher(cppAnalyzerMock, uiListenerMock)
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
        uiListenerMock.notifyAnalysisEnd.assert_called()
        assert uiListenerMock.notifyAnalysisEnd.call_count == 1
        assert len(abstractObjects) == 2
        assert abstractObjects[0] == totoClassAsbtraction
        assert abstractObjects[1] == toto2ClassAsbtraction
