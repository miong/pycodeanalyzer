import logging
from typing import Any, cast


class LoggerFactory:
    """Factory for logger."""

    level: int = logging.INFO
    defaultLogger: logging.Logger = None  # type : ignore

    @staticmethod
    def init() -> None:
        logging.basicConfig(
            format="%(asctime)s - LoggerFactory - %(levelname)s - %(message)s",
            level=logging.INFO,
        )
        LoggerFactory.defaultLogger = LoggerFactory.createLogger("DefaultLogger")
        logging.root = cast(logging.RootLogger, LoggerFactory.defaultLogger)
        # Setting log level for known used packages
        logging.getLogger("werkzeug").setLevel(logging.WARNING)

    @staticmethod
    def setLoggerLevel(loglevel: str) -> None:
        argLevel: Any = getattr(logging, loglevel, None)
        if not isinstance(argLevel, int):
            raise ValueError("Invalid log level: %s" % loglevel)
        LoggerFactory.level = cast(int, argLevel)
        logging.debug(
            "Debug level set to %s", logging.getLevelName(LoggerFactory.level)
        )
        logging.root.setLevel(LoggerFactory.level)

    @staticmethod
    def createLogger(name: str) -> logging.Logger:
        logger: logging.Logger = logging.getLogger(name)
        logger.setLevel(LoggerFactory.level)
        ch: logging.StreamHandler = logging.StreamHandler()
        ch.setLevel(LoggerFactory.level)
        ch.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(ch)
        logger.propagate = False
        return logger
