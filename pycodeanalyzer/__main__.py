from injector import Injector

from pycodeanalyzer.core.console.console import Console
from pycodeanalyzer.core.engine.engine import Engine


def main():
    injector = Injector()
    console = injector.get(Console)
    console.init()
    engine = injector.get(Engine)
    console.run(engine)


if __name__ == "__main__":
    main()