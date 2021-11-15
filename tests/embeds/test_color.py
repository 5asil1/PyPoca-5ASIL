# -*- coding: utf-8 -*-
from pypoca.embeds.color import Color


def test_color_bot():
    assert Color.bot == Color.blue == 0x42C2A1


def test_color_error():
    assert Color.error == Color.red == 0xE74C3C
