from pycodeanalyzer.core.console.console import Console
from pycodeanalyzer.core.engine.engine import Engine
from pycodeanalyzer.injection import injector
from pycodeanalyzer.ui import socketlistener  # this start UI


def main():
    console = injector.get(Console)
    console.init()
    engine = injector.get(Engine)
    console.run(engine)


if __name__ == "__main__":
    main()
