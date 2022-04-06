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
        assert len(analyzer.mapping["Classes"]) == 31
        assert len(analyzer.mapping["Enums"]) == 1
        assert len(analyzer.mapping["Functions"]) == 15
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
        with open(getRessource("cpp_zlib_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        tree = analyzer.getClasseTree()
        print(tree)
        assert tree == {
            '__classes__': [
                'izstream',
                'ozstream',
                'zstringlen',
                'gzomanip2',
                'gzfilebuf',
                'gzfilestream_common',
                'gzifstream',
                'gzofstream',
                'gzomanip',
                'zlib_filefunc64_32_def',
                'zlib_filefunc64_def',
                'zlib_filefunc_def',
                'tm_unz',
                'unz64_file_pos',
                'unz_file_info',
                'unz_file_info64',
                'unz_file_pos',
                'unz_global_info',
                'unz_global_info64',
                'tm_zip',
                'zip_fileinfo',
                'gz_state',
                'inflate_state',
                'code',
                'StrangeMember',
                'gzFile_s',
                'gz_header',
                'z_stream'
            ],
            'zstringlen': {'__classes__': ['Val']}
        }

    def test_getEnumTree(self, mocker):
        objectList = []
        with open(getRessource("pycodeanalyzer_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        tree = analyzer.getEnumTree()
        print(tree)
        assert tree == {'pycodeanalyzer': {'core': {'abstraction': {'objects': {'__enums__': ['AbstractObjectLanguage']}}}}}

    def test_getFunctionTree(self, mocker):
        objectList = []
        with open(getRessource("pycodeanalyzer_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        analyzer = IdentityAnalyser()
        analyzer.analyze(objectList)
        tree = analyzer.getFunctionTree()
        print(tree)
        assert tree == {
            'pycodeanalyzer': {'__main__': {'__functions__': [{'fullDef': 'None '
                                                                          'pycodeanalyzer::__main__::main()',
                                                               'name': 'main'}]},
                               'core': {'abstraction': {'objects': {'__functions__': [{'fullDef': 'Tuple<str,str,str> '
                                                                                                  'pycodeanalyzer::core::abstraction::objects::compareAbstractObject(AbstractObject '
                                                                                                  'obj)',
                                                                                       'name': 'compareAbstractObject'},
                                                                                      {'fullDef': 'str '
                                                                                                  'pycodeanalyzer::core::abstraction::objects::platformIndependantPathHash(str '
                                                                                                  'path)',
                                                                                       'name': 'platformIndependantPathHash'}]}},
                                        'utils': {'containers': {'__functions__': [{'fullDef': 'Any '
                                                                                               'pycodeanalyzer::core::utils::containers::rindex(List<Any> '
                                                                                               'lst, '
                                                                                               'Any '
                                                                                               'value)',
                                                                                    'name': 'rindex'}]},
                                                  'math': {'__functions__': [{'fullDef': 'float '
                                                                                         'pycodeanalyzer::core::utils::math::round_up(float '
                                                                                         'n, '
                                                                                         'int '
                                                                                         'decimals)',
                                                                              'name': 'round_up'}]}}},
                               'ui': {'socketlistener': {'__functions__': [{'fullDef': 'None '
                                                                                       'pycodeanalyzer::ui::socketlistener::fetchAnalysedClassNames(Dict<str,Any> '
                                                                                       'json, '
                                                                                       'List<str> '
                                                                                       'methods)',
                                                                            'name': 'fetchAnalysedClassNames'},
                                                                           {'fullDef': 'None '
                                                                                       'pycodeanalyzer::ui::socketlistener::fetchAnalysedEnumNames(Dict<str,Any> '
                                                                                       'json, '
                                                                                       'List<str> '
                                                                                       'methods)',
                                                                            'name': 'fetchAnalysedEnumNames'},
                                                                           {'fullDef': 'None '
                                                                                       'pycodeanalyzer::ui::socketlistener::fetchAnalysedFileNames(Dict<str,Any> '
                                                                                       'json, '
                                                                                       'List<str> '
                                                                                       'methods)',
                                                                            'name': 'fetchAnalysedFileNames'},
                                                                           {'fullDef': 'None '
                                                                                       'pycodeanalyzer::ui::socketlistener::fetchAnalysedFunctionNames(Dict<str,Any> '
                                                                                       'json, '
                                                                                       'List<str> '
                                                                                       'methods)',
                                                                            'name': 'fetchAnalysedFunctionNames'},
                                                                           {'fullDef': 'None '
                                                                                       'pycodeanalyzer::ui::socketlistener::fetchClassData(Dict<str,Any> '
                                                                                       'json, '
                                                                                       'List<str> '
                                                                                       'methods)',
                                                                            'name': 'fetchClassData'},
                                                                           {'fullDef': 'None '
                                                                                       'pycodeanalyzer::ui::socketlistener::fetchEnumData(Dict<str,Any> '
                                                                                       'json, '
                                                                                       'List<str> '
                                                                                       'methods)',
                                                                            'name': 'fetchEnumData'},
                                                                           {'fullDef': 'None '
                                                                                       'pycodeanalyzer::ui::socketlistener::fetchFileData(Dict<str,Any> '
                                                                                       'json, '
                                                                                       'List<str> '
                                                                                       'methods)',
                                                                            'name': 'fetchFileData'},
                                                                           {'fullDef': 'None '
                                                                                       'pycodeanalyzer::ui::socketlistener::fetchFunctionData(Dict<str,Any> '
                                                                                       'json, '
                                                                                       'List<str> '
                                                                                       'methods)',
                                                                            'name': 'fetchFunctionData'},
                                                                           {'fullDef': 'None '
                                                                                       'pycodeanalyzer::ui::socketlistener::fetchStats(Dict<str,Any> '
                                                                                       'json, '
                                                                                       'List<str> '
                                                                                       'methods)',
                                                                            'name': 'fetchStats'},
                                                                           {'fullDef': 'None '
                                                                                       'pycodeanalyzer::ui::socketlistener::searchData(Dict<str,Any> '
                                                                                       'json, '
                                                                                       'List<str> '
                                                                                       'methods)',
                                                                            'name': 'searchData'}]}}},
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
                                                'identification.py',
                                                'search.py']},
                     'configuration': {'__files__': ['configuration.py']},
                     'console': {'__files__': ['console.py']},
                     'diagrams': {'__files__': ['mermaid.py']},
                     'encoding': {'__files__': ['encodings.py']},
                     'engine': {'__files__': ['engine.py']},
                     'filetree': {'__files__': ['filefetcher.py']},
                     'languages': {'__files__': ['analyzer.py',
                                                 'filedispatcher.py'],
                                   'analyzers': {'__files__': ['cppanalyzer.py',
                                                               'javaanalyzer.py',
                                                               'pythonanalyzer.py']}},
                     'logging': {'__files__': ['loggerfactory.py']},
                     'utils': {'__files__': ['containers.py',
                                             'math.py']}},
            'ui': {'__files__': ['app.py',
                                 'engineinterface.py',
                                 'socketlistener.py']},
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
            '/pycodeanalyzer/core/abstraction/objects.py',
            '/pycodeanalyzer/core/analyzer/dependancy.py',
            '/pycodeanalyzer/core/analyzer/identification.py',
            '/pycodeanalyzer/core/analyzer/search.py',
            '/pycodeanalyzer/core/configuration/configuration.py',
            '/pycodeanalyzer/core/console/console.py',
            '/pycodeanalyzer/core/diagrams/mermaid.py',
            '/pycodeanalyzer/core/encoding/encodings.py',
            '/pycodeanalyzer/core/engine/engine.py',
            '/pycodeanalyzer/core/filetree/filefetcher.py',
            '/pycodeanalyzer/core/languages/analyzer.py',
            '/pycodeanalyzer/core/languages/analyzers/cppanalyzer.py',
            '/pycodeanalyzer/core/languages/analyzers/javaanalyzer.py',
            '/pycodeanalyzer/core/languages/analyzers/pythonanalyzer.py',
            '/pycodeanalyzer/core/languages/filedispatcher.py',
            '/pycodeanalyzer/core/logging/loggerfactory.py',
            '/pycodeanalyzer/ui/app.py',
            '/pycodeanalyzer/ui/engineinterface.py',
            '/pycodeanalyzer/ui/socketlistener.py',
            '/pycodeanalyzer/core/utils/containers.py',
            '/pycodeanalyzer/core/utils/math.py',
            '/pycodeanalyzer/__main__.py',
        ]
