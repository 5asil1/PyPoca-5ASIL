# -*- coding: utf-8 -*-
from deep_translator import GoogleTranslator


class Translator:
    def translate(self, text: str, source: str = "auto", target: str = "en") -> str:
        return GoogleTranslator(source=source, target=target).translate(text)
