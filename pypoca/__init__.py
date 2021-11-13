# -*- coding: utf-8 -*-
from pypoca import logger
from pypoca.config import BugsnagConfig, LoggerConfig

log = logger.get_logger(
    filename_config=LoggerConfig.filename,
    bugsnag_handler_config={"api_key": BugsnagConfig.key},
)

__all__ = ("log")
