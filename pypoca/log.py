# -*- coding: utf-8 -*-
import logging
import logging.config
from logging import Logger

import bugsnag
from bugsnag.handlers import BugsnagHandler

from pypoca.config import BUGSNAG_KEY


logging.config.fileConfig("logging_config.ini")
log = logging.getLogger()
if BUGSNAG_KEY:
    bugsnag.configure(api_key=BUGSNAG_KEY)
    bugsnag_handler = BugsnagHandler(extra_fields={"log": ["__repr__"], "locals": ["locals"], "ctx": ["ctx"]})
    bugsnag_handler.setLevel(logging.ERROR)
    log.addHandler(bugsnag_handler)
else:
    log.warning("No Bugsnag API key configured, couldn't notify")
