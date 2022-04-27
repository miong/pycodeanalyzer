from typing import List

from pycodeanalyzer.core.abstraction.objects import (
    AbstractClass,
    AbstractEnum,
    AbstractFunction,
)
from pycodeanalyzer.core.logging.loggerfactory import LoggerFactory


class IClassDiagramBuild:
    """Base class for Class Diagram builder."""

    def __init__(self, name: str) -> None:
        self.logger = LoggerFactory.createLogger(name)

    def reset(self) -> None:
        self.logger.error(
            "Use of abstract method : reset from IClassDiagramBuild class"
        )
        raise NotImplementedError(
            "A subclass should be defined and implement this interface"
        )

    def createClass(
        self,
        target: AbstractClass,
        linkedClasses: List[AbstractClass],
        linkedEnums: List[AbstractEnum],
        linkedFunctions: List[AbstractFunction],
    ) -> None:
        self.logger.error(
            "Use of abstract method : createClass from IClassDiagramBuild class"
        )
        raise NotImplementedError(
            "A subclass should be defined and implement this interface"
        )

    def createEnum(self, target: AbstractEnum) -> None:
        self.logger.error(
            "Use of abstract method : createEnum from IClassDiagramBuild class"
        )
        raise NotImplementedError(
            "A subclass should be defined and implement this interface"
        )

    def build(self) -> str:
        self.logger.error(
            "Use of abstract method : build from IClassDiagramBuild class"
        )
        raise NotImplementedError(
            "A subclass should be defined and implement this interface"
        )
