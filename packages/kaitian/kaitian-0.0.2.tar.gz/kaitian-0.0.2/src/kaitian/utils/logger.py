import logging
import os
from pathlib import Path
from typing import Optional, Union

from rich.logging import RichHandler
from rich.traceback import install


def setup_logger(name: str, level: int) -> logging.Logger:
    """Logger setup tool.

    Setting up a logger with name and level, the handler is powered by
    `rich.logging.RichHandler` for better looking. The setup process will
    also clear all existing handlers in the logger.

    Parameters
    ----------
    name
        Name of logger, for the `logging.getLogger(name)` method.
    level
        Level of logger, will be set to the rich handler, the logger itself
        will be set to `logging.DEBUG` to catch all logs.

    Returns
    -------
        Logger object.

    Examples
    --------
    >>> logger = setup_logger("example", logging.INFO)
    >>> logger.debug("message of DEBUG level should not be displayed.")
    >>> logger.info("message of INFO level should be displayed.")
    [...] INFO message of INFO level should be displayed. <doctest logger.setup_logger...
    """
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG)

    handler = RichHandler(rich_tracebacks=True)
    formatter = logging.Formatter("%(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(level)
    install(show_locals=False)

    logger.addHandler(handler)
    return logger


def add_file_logger(
    logger: Union[str, logging.Logger],
    filepath: Union[Path, str],
    level: int,
    formatter: Optional[logging.Formatter] = None,
) -> logging.Logger:
    """Add a file handler for a logger.

    If the file logger already exists, it will be removed first,
    which means the new handler will replace the old one.

    Parameters
    ----------
    logger
        Logger name or `logging.Logger` object.
    filepath
        String for file or `pathlib.Path` object.
    level
        Logger level.
    formatter, optional
        Logger formatter, will use the default formatter if not provided.

    Returns
    -------
        Logger object.

    Raises
    ------
    TypeError
        If the logger is not string or `logging.Logger`, will raise this error.
    FileNotFoundError
        If the filepath's parent directory does not exist, will raise this error.

    Examples
    --------
    >>> logger = add_file_logger("example", "_not_exist_folder/example.log", logging.INFO)
    Traceback (most recent call last):
        ...
    FileNotFoundError: ...
    >>> logger = add_file_logger(1, "example.log", logging.INFO)
    Traceback (most recent call last):
        ...
    TypeError: ...
    """

    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    elif isinstance(logger, logging.Logger):
        logger = logger
    else:
        raise TypeError(f"Invalid type of logger: {type(logger)}")

    handler = logging.FileHandler(filepath, encoding="utf-8")
    if formatter is None:
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S",
        )
    handler.setFormatter(formatter)
    handler.setLevel(level)

    for hdlr in logger.handlers:
        if isinstance(hdlr, logging.FileHandler):
            if os.path.samefile(hdlr.baseFilename, handler.baseFilename):
                logger.removeHandler(hdlr)

    logger.addHandler(handler)
