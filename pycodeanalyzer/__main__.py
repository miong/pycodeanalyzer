from pycodeanalyzer.core.console.console import Console
from pycodeanalyzer.core.engine.engine import Engine
from pycodeanalyzer.injection import injector

# socketlistener need to be imported just to init socket listening
from pycodeanalyzer.ui import socketlistener  # noqa


def main() -> None:
    """Main function of pycodeanalyzer"""
    console = injector.get(Console)
    console.init()
    engine = injector.get(Engine)
    console.run(engine)


if __name__ == "__main__":
    main()
