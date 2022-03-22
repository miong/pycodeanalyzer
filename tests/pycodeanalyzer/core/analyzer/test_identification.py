import pytest
import jsonpickle
import os

from pycodeanalyzer.core.analyzer.identification import IdentityAnalyser
from pycodeanalyzer.core.abstraction.objects import (
    AbstractObjectLanguage,
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
)

def getRessource(res):
    here = os.path.dirname(os.path.realpath(__file__))
    resDir = os.path.abspath(os.path.join(here, os.pardir, os.pardir, os.pardir, "ressources"))
    res = os.path.abspath(os.path.join(resDir, res))
    return res


class TestIdentityAnalyser:

    def test_analyze(self, mocker):
        objectList = []
        with open(getRessource("pycodeanalyzer_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        assert len(analyzer.mapping["Classes"]) == 28
        assert len(analyzer.mapping["Enums"]) == 1
        assert len(analyzer.mapping["Functions"]) == 13
        for obj in objectList:
            if obj.type == "Class":
                assert obj in analyzer.mapping["Classes"]
            if obj.type == "Enum":
                assert obj in analyzer.mapping["Enums"]
            if obj.type == "Function":
                assert obj in analyzer.mapping["Functions"]

    def test_getClasses(self, mocker):
        objectList = []
        with open(getRessource("pycodeanalyzer_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        assert analyzer.getClasses() == analyzer.mapping["Classes"]

    def test_getEnums(self, mocker):
        objectList = []
        with open(getRessource("pycodeanalyzer_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        assert analyzer.getEnums() == analyzer.mapping["Enums"]

    def test_getFunctions(self, mocker):
        objectList = []
        with open(getRessource("pycodeanalyzer_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        assert analyzer.getFunctions() == analyzer.mapping["Functions"]

    def test_getClasseTree(self, mocker):
        objectList = []
        with open(getRessource("zlib_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        tree = analyzer.getClasseTree()
        print(tree)
        assert tree == {
        '__classes__': ['inflate_state',
                'code',
                'gz_state',
                'z_stream',
                'gz_header',
                'gzFile_s',
                'tm_unz',
                'unz_global_info64',
                'unz_global_info',
                'unz_file_info64',
                'unz_file_info',
                'unz_file_pos',
                'unz64_file_pos',
                'zlib_filefunc_def',
                'zlib_filefunc64_def',
                'zlib_filefunc64_32_def',
                'tm_zip',
                'zip_fileinfo',
                'zstringlen',
                'izstream',
                'ozstream',
                'gzfilebuf',
                'gzfilestream_common',
                'gzifstream',
                'gzofstream',
                'gzomanip',
                'gzomanip2'],
        'zstringlen': {'__classes__': ['Val']},
        }

    def test_getEnumTree(self, mocker):
        objectList = []
        with open(getRessource("pycodeanalyzer_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        tree = analyzer.getEnumTree()
        print(tree)
        assert tree == {'__enums__': ['AbstractObjectLanguage']}

    def test_getFunctionTree(self, mocker):
        objectList = []
        with open(getRessource("pycodeanalyzer_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        tree = analyzer.getFunctionTree()
        print(tree)
        assert tree == {
        '__functions__': [{'fullDef': 'None ::main()',
           'name': 'main'},
          {'fullDef': 'Any ::rindex(List<Any> lst, Any value)',
           'name': 'rindex'},
          {'fullDef': 'float ::round_up(float n, int decimals)',
           'name': 'round_up'},
          {'fullDef': 'None ::fetchStats(Dict<str,Any> json, '
                      'List<str> methods)',
           'name': 'fetchStats'},
          {'fullDef': 'None ::fetchAnalysedClassNames(Dict<str,Any> '
                      'json, List<str> methods)',
           'name': 'fetchAnalysedClassNames'},
          {'fullDef': 'None ::fetchAnalysedEnumNames(Dict<str,Any> '
                      'json, List<str> methods)',
           'name': 'fetchAnalysedEnumNames'},
          {'fullDef': 'None '
                      '::fetchAnalysedFunctionNames(Dict<str,Any> '
                      'json, List<str> methods)',
           'name': 'fetchAnalysedFunctionNames'},
          {'fullDef': 'None ::fetchAnalysedFileNames(Dict<str,Any> '
                      'json, List<str> methods)',
           'name': 'fetchAnalysedFileNames'},
          {'fullDef': 'None ::fetchClassData(Dict<str,Any> json, '
                      'List<str> methods)',
           'name': 'fetchClassData'},
          {'fullDef': 'None ::fetchEnumData(Dict<str,Any> json, '
                      'List<str> methods)',
           'name': 'fetchEnumData'},
          {'fullDef': 'None ::fetchFunctionData(Dict<str,Any> json, '
                      'List<str> methods)',
           'name': 'fetchFunctionData'},
          {'fullDef': 'None ::fetchFileData(Dict<str,Any> json, '
                      'List<str> methods)',
           'name': 'fetchFileData'},
          {'fullDef': 'None ::searchData(Dict<str,Any> json, '
                      'List<str> methods)',
           'name': 'searchData'}],
        }

    def test_getFileTree(self, mocker):
        objectList = []
        with open(getRessource("pycodeanalyzer_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        tree = analyzer.getFileTree()
        print(tree)
        assert tree == {
        '__files__': ['__main__.py'],
        'core': {'abstraction': {'__files__': ['objects.py']},
            'analyzer': {'__files__': ['dependancy.py',
                                    'search.py',
                                    'identification.py']},
            'console': {'__files__': ['console.py']},
            'diagrams': {'__files__': ['mermaid.py']},
            'encoding': {'__files__': ['encodings.py']},
            'engine': {'__files__': ['engine.py']},
            'filetree': {'__files__': ['filefetcher.py']},
            'languages': {'__files__': ['filedispatcher.py',
                                     'analyzer.py'],
                       'analyzers': {'__files__': ['pythonanalyzer.py',
                                                   'cppanalyzer.py']}},
            'logging': {'__files__': ['loggerfactory.py']},
            'utils': {'__files__': ['containers.py',
                                 'math.py']}},
        'ui': {'__files__': ['engineinterface.py',
                     'socketlistener.py',
                     'app.py']},
        }

    def test_getFiles(self, mocker):
        objectList = []
        with open(getRessource("pycodeanalyzer_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        list = analyzer.getFiles()
        print(list)
        assert list == [
            '/pycodeanalyzer/pycodeanalyzer/core/logging/loggerfactory.py',
            '/pycodeanalyzer/pycodeanalyzer/core/languages/filedispatcher.py',
            '/pycodeanalyzer/pycodeanalyzer/core/languages/analyzer.py',
            '/pycodeanalyzer/pycodeanalyzer/core/languages/analyzers/pythonanalyzer.py',
            '/pycodeanalyzer/pycodeanalyzer/core/languages/analyzers/cppanalyzer.py',
            '/pycodeanalyzer/pycodeanalyzer/core/analyzer/dependancy.py',
            '/pycodeanalyzer/pycodeanalyzer/core/analyzer/search.py',
            '/pycodeanalyzer/pycodeanalyzer/core/analyzer/identification.py',
            '/pycodeanalyzer/pycodeanalyzer/core/filetree/filefetcher.py',
            '/pycodeanalyzer/pycodeanalyzer/core/abstraction/objects.py',
            '/pycodeanalyzer/pycodeanalyzer/core/encoding/encodings.py',
            '/pycodeanalyzer/pycodeanalyzer/core/engine/engine.py',
            '/pycodeanalyzer/pycodeanalyzer/core/diagrams/mermaid.py',
            '/pycodeanalyzer/pycodeanalyzer/core/console/console.py',
            '/pycodeanalyzer/pycodeanalyzer/ui/engineinterface.py',
            '/pycodeanalyzer/pycodeanalyzer/ui/socketlistener.py',
            '/pycodeanalyzer/pycodeanalyzer/ui/app.py',
            '/pycodeanalyzer/pycodeanalyzer/__main__.py',
            '/pycodeanalyzer/pycodeanalyzer/core/utils/containers.py',
            '/pycodeanalyzer/pycodeanalyzer/core/utils/math.py'
        ]
