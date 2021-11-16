# -*- coding: utf-8 -*-
from pypoca import utils


def test_format_datetime():
    date = "2020-12-31"
    date_formated = utils.format_datetime(date, "%Y-%m-%d", "%d/%m/%Y")
    assert date_formated == "31/12/2020"

    date = "2020-12-31"
    date_formated = utils.format_datetime(date, "%Y-%m-%d", "%Y/%m/%d")
    assert date_formated == "2020/12/31"

    date = "2020-12-31"
    date_formated = utils.format_datetime(date)
    assert date_formated == "2020/12/31"

    date = None
    date_formated = utils.format_datetime(date, "%Y-%m-%d", "%d/%m/%Y")
    assert date_formated is None

    date = ""
    date_formated = utils.format_datetime(date, "%Y-%m-%d", "%d/%m/%Y")
    assert date_formated is None


def test_format_duration():
    duration = 59
    duration_formated = utils.format_duration(duration)
    assert duration_formated == "59min"

    duration = 60
    duration_formated = utils.format_duration(duration)
    assert duration_formated == "1h"

    duration = 61
    duration_formated = utils.format_duration(duration)
    assert duration_formated == "1h 1min"

    duration = None
    duration_formated = utils.format_duration(duration)
    assert duration_formated is None

    duration = ""
    duration_formated = utils.format_duration(duration)
    assert duration_formated is None
