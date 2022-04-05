from typing import List, Optional, Tuple

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
)


class DependancyAnalyser:
    """Analyzer for object dependancies"""

    def analyze(
        self,
        klasses: List[AbstractClass],
        enums: List[AbstractEnum],
        target: AbstractClass,
    ) -> Tuple[
        AbstractClass, List[AbstractClass], List[AbstractEnum], List[AbstractFunction]
    ]:
        linkedClasses: List[AbstractClass] = []
        linkedEnums: List[AbstractEnum] = []
        linkedFunctions: List[
            AbstractFunction
        ] = []  # TODO : need to process called function
        for type in target.getLinkedTypes():
            typeDeclaredNamespace = ""
            typeName = ""
            if "::" in type:
                lastSeparatorIndx = type.rindex("::")
                typeDeclaredNamespace = type[:lastSeparatorIndx]
                typeName = type[lastSeparatorIndx + 2 :]
            else:
                typeName = type
            linkedClass = self.__findClass(
                typeDeclaredNamespace,
                typeName,
                klasses,
                target.namespace,
                target.name,
                target.usingNS,
            )
            linkedEnum = self.__findEnum(
                typeDeclaredNamespace,
                typeName,
                enums,
                target.namespace,
                target.name,
                target.usingNS,
            )
            if linkedEnum:
                if linkedEnum != target:
                    linkedEnums.append(linkedEnum)
            elif linkedClass:
                if linkedClass != target:
                    linkedClasses.append(linkedClass)
            else:
                linkedClasses.append(
                    AbstractClass(typeName, typeDeclaredNamespace, None)
                )
        return (target, linkedClasses, linkedEnums, linkedFunctions)

    def getParent(
        self, klasses: List[AbstractClass], target: AbstractClass, parentName: str
    ) -> Optional[AbstractClass]:
        typeDeclaredNamespace = ""
        typeName = ""
        if "::" in parentName:
            lastSeparatorIndx = parentName.rindex("::")
            typeDeclaredNamespace = parentName[:lastSeparatorIndx]
            typeName = parentName[lastSeparatorIndx + 2 :]
        else:
            typeName = parentName
        return self.__findClass(
            typeDeclaredNamespace,
            typeName,
            klasses,
            target.namespace,
            target.name,
            target.usingNS,
        )

    def __findClass(
        self,
        namespace: str,
        name: str,
        klasses: List[AbstractClass],
        currentNamespace: str,
        currentClassName: str,
        usingNS: List[str],
    ) -> Optional[AbstractClass]:
        for klass in klasses:
            if klass.namespace == namespace and klass.name == name:
                return klass
            if klass.namespace == currentClassName and klass.name == name:
                return klass
            if klass.namespace == currentNamespace and klass.name == name:
                return klass
            if (
                klass.namespace == currentNamespace + "::" + namespace
                and klass.name == name
            ):
                return klass
            if (
                klass.namespace == currentClassName + "::" + namespace
                and klass.name == name
            ):
                return klass
            if (
                klass.namespace == currentNamespace + "::" + currentClassName
                and klass.name == name
            ):
                return klass
            if (
                klass.namespace
                == currentNamespace + "::" + currentClassName + "::" + namespace
                and klass.name == name
            ):
                return klass
            for ns in usingNS:
                if klass.namespace == ns and klass.name == name:
                    return klass
                if klass.namespace == ns + "::" + namespace and klass.name == name:
                    return klass
        return None

    def __findEnum(
        self,
        namespace: str,
        name: str,
        enums: List[AbstractEnum],
        currentNamespace: str,
        currentClassName: str,
        usingNS: List[str],
    ) -> Optional[AbstractEnum]:
        for enum in enums:
            if enum.namespace == namespace and enum.name == name:
                return enum
            if enum.namespace == currentClassName and enum.name == name:
                return enum
            if enum.namespace == currentNamespace and enum.name == name:
                return enum
            if (
                enum.namespace == currentNamespace + "::" + namespace
                and enum.name == name
            ):
                return enum
            if (
                enum.namespace == currentClassName + "::" + namespace
                and enum.name == name
            ):
                return enum
            if (
                enum.namespace == currentNamespace + "::" + currentClassName
                and enum.name == name
            ):
                return enum
            if (
                enum.namespace
                == currentNamespace + "::" + currentClassName + "::" + namespace
                and enum.name == name
            ):
                return enum
            for ns in usingNS:
                if enum.namespace == ns and enum.name == name:
                    return enum
                if enum.namespace == ns + "::" + namespace and enum.name == name:
                    return enum
        return None
