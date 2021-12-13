# -*- coding: utf-8 -*-
import logging
import logging.config
from logging import Logger

import bugsnag
from bugsnag.handlers import BugsnagHandler


def config_logger(file_config: str, dict_config: dict, **basic_config) -> None:
    """Logging configuration.

    If 'file_config' has passed, read the logging configuration from a ConfigParser-format file.
    Else, if 'dict_config' has passed, start up a socket server on the specified port, and listen
    for new configurations. Else, do basic configuration for the logging system.
    """
    if file_config:
        logging.config.fileConfig(file_config)
    elif dict_config:
        logging.config.dictConfig(dict_config)
    else:
        logging.basicConfig(**basic_config)


def inject_bugsnag_handler(logger: Logger, api_key: str = None, **kwargs) -> BugsnagHandler:
    """Handler for Bugsnag notifier application-wide."""
    if api_key is None:
        logger.warning("No Bugsnag API key configured, couldn't notify")
        return None
    bugsnag.configure(api_key=api_key, **kwargs)
    bugsnag_handler = BugsnagHandler(extra_fields={"log": ["__repr__"], "locals": ["locals"], "ctx": ["ctx"]})
    bugsnag_handler.setLevel(logging.ERROR)
    logger.addHandler(bugsnag_handler)


def get_logger(
    name: str = None,
    *,
    file_config: str = None,
    dict_config: dict = None,
    bugsnag_config: dict = None,
    **basic_config,
) -> Logger:
    """Generate all configured loggers."""
    config_logger(file_config=file_config, dict_config=dict_config, **basic_config)
    logger = logging.getLogger(name)
    inject_bugsnag_handler(logger, **bugsnag_config)
    return logger
