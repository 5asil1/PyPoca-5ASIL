# -*- coding: utf-8 -*-
import logging
import logging.config
from logging import Logger

import bugsnag
from bugsnag.handlers import BugsnagHandler

__all__ = "Log"


class Log(Logger):
    """Initialize the Logger with configuration from a file, a dictionary or kwargs."""

    def __new__(cls, filename: str = None, dictionary: dict = {}, bugsnag_key: str = None, **kwargs) -> Logger:
        if filename:
            cls.config_from_file(filename)
        elif dictionary:
            cls.config_from_dict(dictionary)
        else:
            cls.config_from_args(**kwargs)
        logger = logging.getLogger()
        cls.inject_bugsnag_handler(logger, bugsnag_key)
        return logger

    @staticmethod
    def config_from_file(filename: str) -> None:
        """Read the logging configuration from a ConfigParser-format file."""
        logging.config.fileConfig(filename)

    @staticmethod
    def config_from_dict(dictionary: dict) -> None:
        """Configure logging using a dictionary."""
        logging.config.dictConfig(dictionary)

    @staticmethod
    def config_from_args(**kwargs) -> None:
        """Do basic configuration for the logging system."""
        logging.basicConfig(**kwargs)

    @staticmethod
    def inject_bugsnag_handler(logger: Logger, key: str = None) -> None:
        """Handler for Bugsnag notifier application-wide."""
        if key:
            bugsnag.configure(api_key=key)
            bugsnag_handler = BugsnagHandler(extra_fields={"log": ["__repr__"], "locals": ["locals"], "ctx": ["ctx"]})
            bugsnag_handler.setLevel(logging.ERROR)
            logger.addHandler(bugsnag_handler)
        else:
            logger.warning("No Bugsnag API key configured, couldn't notify")
