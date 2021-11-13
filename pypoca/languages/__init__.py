# -*- coding: utf-8 -*-
from pypoca.config import BotConfig

if BotConfig.language == "en_US":
    from pypoca.languages.en_US import *  # NOQA
elif BotConfig.language == "pt_BR":
    from pypoca.languages.pt_BR import *  # NOQA
else:
    from pypoca.languages.en_US import *  # NOQA
