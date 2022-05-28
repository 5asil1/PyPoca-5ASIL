# -*- coding: utf-8 -*-
import json
import os

ALL = {}

for filename in os.listdir("pypoca/locale"):
    with open(f"pypoca/locale/{filename}", "r") as file:
        ALL[filename[:-5]] = json.load(file)

DEFAULT_LANGUAGE = "en_US"
DEFAULT_REGION = "US"
DEFAULT = ALL[DEFAULT_LANGUAGE]
