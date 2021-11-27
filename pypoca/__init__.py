# -*- coding: utf-8 -*-
from pypoca import logger
from pypoca.config import Config

log = logger.get_logger(
    file_config=Config.logger.filename,
    bugsnag_config={"api_key": Config.bugsnag.key},
)

__all__ = "log"
