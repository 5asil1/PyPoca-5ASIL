# -*- coding: utf-8 -*-
from pypoca.config import Config
from pypoca.log import Log

log = Log(filename=Config.logger.filename, bugsnag_key=Config.bugsnag.key)

__all__ = ("Config", "log")
