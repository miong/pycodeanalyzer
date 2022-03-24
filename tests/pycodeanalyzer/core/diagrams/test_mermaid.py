import pytest

from pycodeanalyzer.core.diagrams.mermaid import ClassDiagramBuild
from pycodeanalyzer.core.abstraction.objects import (
    AbstractObjectLanguage,
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
)

class TestClassDiagramBuild:

    def test_buildEnum(self, mocker):
        enum = AbstractEnum("enumName", "enum::namespace", "dir/file.txt", ["value1", "value2", "value3"])
        builder = ClassDiagramBuild()
        builder.reset()
        builder.createEnum(enum)
        res = builder.build()
        expected = """classDiagram
class enumName {
<<Enum>>
+ value1
+ value2
+ value3
}
"""
        assert res == expected


    def test_buildClass(self, mocker):
        enum = AbstractEnum("enumName", "enum::namespace", "dir/file.txt", ["value1", "value2", "value3"])
        enum2 = AbstractEnum("enumName2", "enum::namespace", None, ["value1", "value2", "value3"])
        member = ("memberType", "memberName", "protected")
        member2 = ("memberType2", "memberName2", "public")
        methode = ("rtype", "name", [("Map<str, List<param1Type>>", "param1Name"),("enumName", "param2Name")], "private")
        parent = ("parentType", "parentType", "public")
        klass = AbstractClass("className", "class::namespace", "dir/file.txt")
        klassParent = AbstractClass("parentType", "class::namespace", "dir/file.txt")
        klassLinked = AbstractClass("param1Type", "", None)
        klass.language = AbstractObjectLanguage.CPP
        klass.addMember(*member)
        klass.addMember(*member2)
        klass.addMethod(*methode)
        klass.addParent(*parent)
        builder = ClassDiagramBuild()
        builder.reset()
        builder.createClass(klass, [klassParent, klassLinked], [enum, enum2], [])
        res = builder.build()
        expected = """classDiagram
class className {
<<Class>>
# memberType memberName
+ memberType2 memberName2
-name(Map&lt;str, List&lt;param1Type&gt;&gt; param1Name, enumName param2Name) rtype
}
class parentType {
<<Class>>
}
link parentType "class££class::namespace::parentType"
class param1Type
<<External>> param1Type
class enumName {
<<Enum>>
+ value1
+ value2
+ value3
}
link enumName "enum££enum::namespace::enumName"
class enumName2
<<External>> enumName2
className --|> parentType
className ..> param1Type
className ..> enumName
className ..> enumName2
"""
        assert res == expected
