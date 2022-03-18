import pytest

import os

from build.lib.pycodeanalyzer.core.encoding.encodings import Encoding
from pycodeanalyzer.core.filetree.filefetcher import FileFetcher

class TestFileFetcher:

    def test_isAnalyzed(self, mocker):
        fetcher = FileFetcher()
        encodingMock = Encoding()
        fetcher.encoding = encodingMock
        encodingMock.getFileEncoding = mocker.MagicMock(return_value="utf-8")
        extensions = [".h", ".hpp"];
        #file type
        for ext in extensions:
            assert fetcher.isAnalyzed("toto"+ext)
            assert fetcher.isAnalyzed("dir/toto"+ext)
            assert fetcher.isAnalyzed("complex/file/tree/dir/toto"+ext)
        #avoid hidden files
        for ext in extensions:
            assert not fetcher.isAnalyzed(".toto"+ext)
            assert not fetcher.isAnalyzed("dir/.toto"+ext)
            assert not fetcher.isAnalyzed("complex/file/tree/dir/.toto"+ext)
        #file encoding
        encodingMock.getFileEncoding = mocker.MagicMock(return_value="binary")
        assert not fetcher.isAnalyzed("complex/file/tree/dir/toto.hpp")
        encodingMock.getFileEncoding = mocker.MagicMock(return_value="unknown-8bit")
        assert not fetcher.isAnalyzed("complex/file/tree/dir/toto.hpp")

    def test_fetch(self, mocker):
        fetcher = FileFetcher()
        mocker.patch.object(fetcher, "isAnalyzed", return_value=True)
        mocker.patch.object(os.path, "abspath", return_value="/home/toto/dir")
        filelist = fetcher.fetch("toto/dir")
        assert len(filelist) == 0
        mocker.patch.object(os.path, "isdir", return_value=True)
        mocker.patch.object(os, "walk", return_value=[("/home/toto/dir", (), ())])
        filelist = fetcher.fetch("toto/dir")
        assert len(filelist) == 0
        mocker.patch.object(os.path, "isfile", return_value=True)
        mocker.patch.object(os, "walk", return_value=[("/home/toto/dir", (), ("toto.h",))])
        filelist = fetcher.fetch("toto/dir")
        assert len(filelist) == 1
        assert filelist[0] == os.path.join("/home/toto/dir","toto.h")
        mocker.patch.object(os, "walk", return_value=[("/home/toto/dir", (), ("toto.h", "titi.h",)), ("/home/toto/dir2", (), ("tutu.h",))])
        filelist = fetcher.fetch("toto/dir")
        assert len(filelist) == 3
        assert filelist[0] == os.path.join("/home/toto/dir","toto.h")
        assert filelist[1] == os.path.join("/home/toto/dir","titi.h")
        assert filelist[2] == os.path.join("/home/toto/dir2","tutu.h")
        mocker.patch.object(fetcher, "isAnalyzed", return_value=False)
        filelist = fetcher.fetch("toto/dir")
        assert len(filelist) == 0
