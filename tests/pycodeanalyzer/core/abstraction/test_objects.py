import pytest

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
    AbstractObject,
    AbstractObjectLanguage,
)

class TestAbstractEnum:

    def test_getFullName(self, mocker):
        enum = AbstractEnum("enumName", "enum::namespace", "dir/file.txt", ["value1", "value2", "value3"])
        assert enum.getFullName() == "enum::namespace::enumName"
        enum = AbstractEnum("enumName", "", "dir/file.txt", ["value1", "value2", "value3"])
        assert enum.getFullName() == "enumName"

class TestAbstractFunction:

    def test_getFullName(self, mocker):
        func = AbstractFunction("funcName", "dir/file.txt", "funcRType", [("param1Type", "param1Name"),("param2Type", "param2Name")],"func::namespace", "funcDoxygen")
        assert func.getFullDef() == "funcRType func::namespace::funcName(param1Type param1Name, param2Type param2Name)"
        func = AbstractFunction("funcName", "dir/file.txt", "funcRType", [],"func::namespace", "funcDoxygen")
        assert func.getFullDef() == "funcRType func::namespace::funcName()"
        func = AbstractFunction("funcName", "dir/file.txt", "funcRType", [], "", "funcDoxygen")
        assert func.getFullDef() == "funcRType ::funcName()"

class TestAbstractClass:

    def test_addMember(self, mocker):
        member = ("memberType", "memberName", "public")
        klass = AbstractClass("className", "class::namespace", "dir/file.txt")
        klass.addMember(*member)
        assert len(klass.members) == 1
        assert klass.members[0] == member

    def test_addMethod(self, mocker):
        methode = ("rtype", "name", [("param1Type", "param1Name"),("param2Type", "param2Name")], "public")
        klass = AbstractClass("className", "class::namespace", "dir/file.txt")
        klass.addMethod(*methode)
        assert len(klass.methodes) == 1
        assert klass.methodes[0] == methode

    def test_addParent(self, mocker):
        parent = ("some::namespace::parentType", "parentType", "public")
        klass = AbstractClass("className", "class::namespace", "dir/file.txt")
        klass.addParent(*parent)
        assert len(klass.parents) == 1
        assert klass.parents[0] == parent

    def test_getLinkedTypes_simple(self, mocker):
        member = ("memberType", "memberName", "public")
        methode = ("rtype", "name", [("param1Type", "param1Name"),("param2Type", "param2Name")], "public")
        parent = ("parentType", "parentType", "public")
        klass = AbstractClass("className", "class::namespace", "dir/file.txt")
        klass.objectLanguage = AbstractObjectLanguage.CPP
        klass.addMember(*member)
        klass.addMethod(*methode)
        klass.addParent(*parent)
        assert klass.getLinkedTypes() == ['parentType', 'rtype', 'param1Type', 'param2Type', 'memberType']

    def test_getLinkedTypes_complexe(self, mocker):
        member = ("std::map<std::string,List<memberType>>", "memberName", "public")
        methode = ("rtype *", "name", [("const param1Type&", "param1Name"),("param2Type", "param2Name")], "public")
        parent = ("std::share_ptr<Holder<parentType, int>>", "parentType", "public")
        klass = AbstractClass("className", "class::namespace", "dir/file.txt")
        klass.objectLanguage = AbstractObjectLanguage.CPP
        klass.addMember(*member)
        klass.addMethod(*methode)
        klass.addParent(*parent)
        assert klass.getLinkedTypes() == ['parentType', "Holder", 'rtype', 'param1Type', 'param2Type', 'memberType', "List"]

    def test_removeNoneObjectTypes(self, mocker):
        for language in AbstractObjectLanguage:
            klass = AbstractClass("className", "class::namespace", "dir/file.txt")
            klass.objectLanguage = language
            for type in AbstractClass.NonObjectTypes[language]:
                member = (type, "member_"+type, "public")
                methode = (type, "func_"+type, [(type, "param")], "public")
                klass.addMember(*member)
                klass.addMethod(*methode)
            assert klass.getLinkedTypes() == []

    def test_getFullName(self, mocker):
        klass = AbstractClass("className", "class::namespace", "dir/file.txt")
        assert klass.getFullName() == "class::namespace::className"
        klass = AbstractClass("className", "", "dir/file.txt")
        assert klass.getFullName() == "className"

    def test_isParent(self, mocker):
        klass = AbstractClass("className", "class::namespace", "dir/file.txt")
        klassParent = AbstractClass("parentType", "class::namespace", "dir/file.txt")
        klassParent2 = AbstractClass("parentType2", "class::namespace", "dir/file.txt")
        klassNotParent = AbstractClass("parentType3", "class::namespace", "dir/file.txt")
        parent = ("parentType", "parentType", "public")
        parent2 = ("parentType2", "parentType2", "public")
        klass.addParent(*parent)
        klass.addParent(*parent2)
        assert klass.isParent(klassParent)
        assert klass.isParent(klassParent2)
        assert not  klass.isParent(klassNotParent)
