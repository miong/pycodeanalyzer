import pytest
import jsonpickle
import os

from pycodeanalyzer.core.analyzer.dependancy import DependancyAnalyser
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

class TestDependancyAnalyser:

    def test_findEnum(self, mocker):
        enums = [
            AbstractEnum("enum", "", "file.xx", ["A", "B", "C"]),
            AbstractEnum("enum2", "namespace", "file.xx", ["A", "B", "C"]),
            AbstractEnum("enum3", "namespace::class", "file.xx", ["A", "B", "C"]),
            AbstractEnum("enum4", "totoNS", "file.xx", ["A", "B", "C"]),
            AbstractEnum("enum5", "totoNS::secondNS", "file.xx", ["A", "B", "C"]),
            AbstractEnum("enum6", "someNS::secondNS", "file.xx", ["A", "B", "C"]),
            AbstractEnum("enum7", "someNS::secondNS::thirdNS", "file.xx", ["A", "B", "C"]),
        ]
        analyzer = DependancyAnalyser()
        res = analyzer._DependancyAnalyser__findEnum("", "enum", enums, "currentNS", "currentClass", ["totoNS", "titiNS"])
        assert res == enums[0]
        res = analyzer._DependancyAnalyser__findEnum("namespace", "enum2", enums, "currentNS", "currentClass", ["totoNS", "titiNS"])
        assert res == enums[1]
        res = analyzer._DependancyAnalyser__findEnum("", "enum2", enums, "namespace", "currentClass", ["totoNS", "titiNS"])
        assert res == enums[1]
        res = analyzer._DependancyAnalyser__findEnum("", "enum2", enums, "", "namespace", ["totoNS", "titiNS"])
        assert res == enums[1]
        res = analyzer._DependancyAnalyser__findEnum("", "enum3", enums, "namespace", "class", ["totoNS", "titiNS"])
        assert res == enums[2]
        res = analyzer._DependancyAnalyser__findEnum("", "enum4", enums, "currentNS", "currentClass", ["totoNS", "titiNS"])
        assert res == enums[3]
        res = analyzer._DependancyAnalyser__findEnum("secondNS", "enum5", enums, "currentNS", "currentClass", ["totoNS", "titiNS"])
        assert res == enums[4]
        res = analyzer._DependancyAnalyser__findEnum("secondNS", "enum6", enums, "someNS", "currentClass", ["totoNS", "titiNS"])
        assert res == enums[5]
        res = analyzer._DependancyAnalyser__findEnum("secondNS", "enum6", enums, "", "someNS", ["totoNS", "titiNS"])
        assert res == enums[5]
        res = analyzer._DependancyAnalyser__findEnum("thirdNS", "enum7", enums, "someNS", "secondNS", ["totoNS", "titiNS"])
        assert res == enums[6]
        res = analyzer._DependancyAnalyser__findEnum("", "enumUnknow", enums, "", "", ["totoNS", "titiNS"])
        assert res == None
        res = analyzer._DependancyAnalyser__findEnum("thirdNS", "enum7", enums, "", "", ["totoNS", "titiNS"])
        assert res == None
        res = analyzer._DependancyAnalyser__findEnum("secondNS::thirdNS", "enum7", enums, "", "", ["totoNS", "titiNS"])
        assert res == None


    def test_findClass(self, mocker):
        classes = [
            AbstractClass("class", "", "file.xx",),
            AbstractClass("class2", "namespace", "file.xx"),
            AbstractClass("class3", "namespace::class", "file.xx"),
            AbstractClass("class4", "totoNS", "file.xx"),
            AbstractClass("class5", "totoNS::secondNS", "file.xx"),
            AbstractClass("class6", "someNS::secondNS", "file.xx"),
            AbstractClass("class7", "someNS::secondNS::thirdNS", "file.xx"),
        ]
        analyzer = DependancyAnalyser()
        res = analyzer._DependancyAnalyser__findClass("", "class", classes, "currentNS", "currentClass", ["totoNS", "titiNS"])
        assert res == classes[0]
        res = analyzer._DependancyAnalyser__findClass("namespace", "class2", classes, "currentNS", "currentClass", ["totoNS", "titiNS"])
        assert res == classes[1]
        res = analyzer._DependancyAnalyser__findClass("", "class2", classes, "namespace", "currentClass", ["totoNS", "titiNS"])
        assert res == classes[1]
        res = analyzer._DependancyAnalyser__findClass("", "class2", classes, "", "namespace", ["totoNS", "titiNS"])
        assert res == classes[1]
        res = analyzer._DependancyAnalyser__findClass("", "class3", classes, "namespace", "class", ["totoNS", "titiNS"])
        assert res == classes[2]
        res = analyzer._DependancyAnalyser__findClass("", "class4", classes, "currentNS", "currentClass", ["totoNS", "titiNS"])
        assert res == classes[3]
        res = analyzer._DependancyAnalyser__findClass("secondNS", "class5", classes, "currentNS", "currentClass", ["totoNS", "titiNS"])
        assert res == classes[4]
        res = analyzer._DependancyAnalyser__findClass("secondNS", "class6", classes, "someNS", "currentClass", ["totoNS", "titiNS"])
        assert res == classes[5]
        res = analyzer._DependancyAnalyser__findClass("secondNS", "class6", classes, "", "someNS", ["totoNS", "titiNS"])
        assert res == classes[5]
        res = analyzer._DependancyAnalyser__findClass("thirdNS", "class7", classes, "someNS", "secondNS", ["totoNS", "titiNS"])
        assert res == classes[6]
        res = analyzer._DependancyAnalyser__findClass("", "classUnknow", classes, "", "", ["totoNS", "titiNS"])
        assert res == None
        res = analyzer._DependancyAnalyser__findClass("thirdNS", "class7", classes, "", "", ["totoNS", "titiNS"])
        assert res == None
        res = analyzer._DependancyAnalyser__findClass("secondNS::thirdNS", "class7", classes, "", "", ["totoNS", "titiNS"])
        assert res == None

    def test_analyze(self, mocker):
        objectList = []
        with open(getRessource("pycodeanalyzer_dumpobj.json"),"r") as dataFile:
            objectList = jsonpickle.decode(dataFile.read())
        mapping = {
            "Classes": [],
            "Enums": [],
        }
        for object in objectList:
            if object.type == "Class":
                mapping["Classes"].append(object)
            elif object.type == "Enum":
                mapping["Enums"].append(object)
        analyzer = DependancyAnalyser()

        engineObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::core::engine::engine", "Engine", mapping["Classes"], "", "", [])
        abstractClassObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::core::abstraction::objects", "AbstractClass", mapping["Classes"], "", "", [])
        abstractObjectObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::core::abstraction::objects", "AbstractObject", mapping["Classes"], "", "", [])
        abstractObjectLanguageObj = analyzer._DependancyAnalyser__findEnum("pycodeanalyzer::core::abstraction::objects", "AbstractObjectLanguage", mapping["Enums"], "", "", [])
        fileFetcherObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::core::filetree::filefetcher", "FileFetcher", mapping["Classes"], "", "", [])
        fileDispatcherObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::core::languages::filedispatcher", "FileDispatcher", mapping["Classes"], "", "", [])
        identityAnalyserObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::core::analyzer::identification", "IdentityAnalyser", mapping["Classes"], "", "", [])
        dependancyAnalyserObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::core::analyzer::dependancy", "DependancyAnalyser", mapping["Classes"], "", "", [])
        searchAnalyserObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::core::analyzer::search", "SearchAnalyser", mapping["Classes"], "", "", [])
        uiStatListenerObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::ui::app", "UiStatListener", mapping["Classes"], "", "", [])
        uiBrowseListenerObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::ui::app", "UiBrowseListener", mapping["Classes"], "", "", [])
        classDiagramBuildObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::core::diagrams::mermaid", "ClassDiagramBuild", mapping["Classes"], "", "", [])
        configurationObj = analyzer._DependancyAnalyser__findClass("pycodeanalyzer::core::configuration::configuration", "Configuration", mapping["Classes"], "", "", [])

        madupClass = AbstractClass("class", "", "file.xx",)
        madupClass.addMember("someNS::type", "name", "public")

        target, classes, enums, functions = analyzer.analyze(mapping["Classes"], mapping["Enums"], abstractObjectObj)
        assert target == abstractObjectObj
        assert classes == []
        assert enums == [abstractObjectLanguageObj]
        target, classes, enums, functions = analyzer.analyze(mapping["Classes"], mapping["Enums"], abstractClassObj)
        assert target == abstractClassObj
        assert classes == [abstractObjectObj]
        assert enums == []
        target, classes, enums, functions = analyzer.analyze(mapping["Classes"], mapping["Enums"], engineObj)
        assert target == engineObj
        assert classes == [
            fileFetcherObj,
            fileDispatcherObj,
            identityAnalyserObj,
            dependancyAnalyserObj,
            searchAnalyserObj,
            uiStatListenerObj,
            uiBrowseListenerObj,
            classDiagramBuildObj,
            configurationObj,
        ]
        assert enums == []
        target, classes, enums, functions = analyzer.analyze(mapping["Classes"], mapping["Enums"], madupClass)
        assert target == madupClass
        assert len(classes) == 1
        assert classes[0].name == "type"
        assert classes[0].namespace == "someNS"
        assert classes[0].origin == None
        assert enums == []
