# -*- coding: utf-8 -*-
import logging
import logging.config
from logging import Formatter, Logger, StreamHandler
from logging.handlers import TimedRotatingFileHandler

import bugsnag
from bugsnag.handlers import BugsnagHandler

DEFAULT_LEVEL = "INFO"
DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(module)s.py:%(lineno)s %(message)s"


def get_stream_handler(
    level: str = "INFO", format: str = DEFAULT_FORMAT, **kwargs
) -> StreamHandler:
    """Handler which writes logging records to a stream."""
    stream_handler = StreamHandler(**kwargs)
    stream_handler.setLevel(level)
    stream_handler.setFormatter(Formatter(format))
    return stream_handler


def get_file_handler(
    filename: str = ".log", when: str = "MIDNIGHT", level: str = "WARNING", format: str = DEFAULT_FORMAT, **kwargs
) -> TimedRotatingFileHandler:
    """Handler for logging to a file, rotating the log file at certain timed intervals."""
    file_handler = TimedRotatingFileHandler(filename, when=when, **kwargs)
    file_handler.setLevel(level)
    file_handler.setFormatter(Formatter(format))
    return file_handler


def get_bugsnag_handler(
    api_key: str = None, level: str = "ERROR", **kwargs
) -> BugsnagHandler:
    """Handler for Bugsnag notifier application-wide."""
    bugsnag.configure(api_key=api_key, **kwargs)
    bugsnag_handler = BugsnagHandler(extra_fields={"log": ["__repr__"], "locals": ["locals"], "ctx": ["ctx"]})
    bugsnag_handler.setLevel(level)
    return bugsnag_handler


def config_logger(filename: str, config: dict, level: str, format: str) -> None:
    """Logging configuration.

    If 'filename' has passed, read the logging configuration from a ConfigParser-format file.
    Else, if 'config' has passed, start up a socket server on the specified port, and listen
    for new configurations. Else, do basic configuration for the logging system.
    """
    if filename:
        logging.config.fileConfig(filename)
    elif config:
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=level, format=format)


def get_logger(
    name: str = None,
    *,
    filename_config: str = None,
    dict_config: dict = {},
    level: str = DEFAULT_LEVEL,
    format: str = DEFAULT_FORMAT,
    file_handler_config: dict = {},
    stream_handler_config: dict = {},
    bugsnag_handler_config: dict = {},
) -> Logger:
    """Generate all configured loggers."""
    config_logger(filename=filename_config, config=dict_config, level=level, format=format)
    logger = logging.getLogger(name)
    logger.addHandler(get_file_handler(**stream_handler_config))
    logger.addHandler(get_bugsnag_handler(**bugsnag_handler_config))
    return logger
