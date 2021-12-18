# -*- coding: utf-8 -*-
from pypoca.log import Log
from pypoca.config import Config

log = Log(
    filename=Config.logger.filename,
    bugsnag_key=Config.bugsnag.key,
)

__all__ = "log"
