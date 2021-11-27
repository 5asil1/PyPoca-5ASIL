# -*- coding: utf-8 -*-
from pypoca.config import Config

if Config.bot.language == "en_US":
    from pypoca.languages.en_US import *  # NOQA
elif Config.bot.language == "pt_BR":
    from pypoca.languages.pt_BR import *  # NOQA
else:
    from pypoca.languages.en_US import *  # NOQA
