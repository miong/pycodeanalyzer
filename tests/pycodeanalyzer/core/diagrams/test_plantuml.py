import pytest

from pycodeanalyzer.core.diagrams.plantuml import PlantUMLClassDiagramBuild
from pycodeanalyzer.core.abstraction.objects import (
    AbstractObjectLanguage,
    AbstractClassClassifier,
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
)

class TestPlantUMLClassDiagramBuild:

    def test_buildEnum(self, mocker):
        enum = AbstractEnum("enumName", "enum::namespace", "dir/file.txt", ["value1", "value2", "value3"])
        builder = PlantUMLClassDiagramBuild()
        builder.reset()
        builder.createEnum(enum)
        res = builder.build()
        expected = """@startuml
enum enumName <<Enum>>
{
value1
value2
value3
}
@enduml
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
        klassLinked.addClassifier(AbstractClassClassifier.External)
        klass.objectLanguage = AbstractObjectLanguage.CPP
        klass.addMember(*member)
        klass.addMember(*member2)
        klass.addMethod(*methode)
        klass.addParent(*parent)
        builder = PlantUMLClassDiagramBuild()
        builder.reset()
        builder.createClass(klass, [klassParent, klassLinked], [enum, enum2], [])
        res = builder.build()
        expected = """@startuml
class className <<Class>>
{
# memberType memberName
+ memberType2 memberName2
-rtype name(Map<str, List<param1Type>> param1Name, enumName param2Name)
}
class parentType <<Class>>
{
}
class param1Type <<External>>
enum enumName <<Enum>>
{
value1
value2
value3
}
enum enumName2 <<External>>
className --|> parentType
className ..|> param1Type
className ..|> enumName
className ..|> enumName2
@enduml
"""
        assert res == expected
