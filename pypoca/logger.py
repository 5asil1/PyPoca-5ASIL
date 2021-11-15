# -*- coding: utf-8 -*-
import logging
import logging.config
from logging import Logger

import bugsnag
from bugsnag.handlers import BugsnagHandler

DEFAULT_LEVEL = "INFO"
DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(module)s.py:%(lineno)s %(message)s"


def get_bugsnag_handler(api_key: str = None, level: str = "ERROR", **kwargs) -> BugsnagHandler:
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
    bugsnag_handler_config: dict = {},
) -> Logger:
    """Generate all configured loggers."""
    config_logger(filename=filename_config, config=dict_config, level=level, format=format)
    logger = logging.getLogger(name)
    logger.addHandler(get_bugsnag_handler(**bugsnag_handler_config))
    return logger
