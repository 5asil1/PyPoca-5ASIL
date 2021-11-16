# -*- coding: utf-8 -*-
from datetime import datetime

from pypoca.languages import DATETIME_STR


def format_datetime(value: str, from_format: str = "%Y-%m-%d", to_format: str = DATETIME_STR) -> str:
    """Convert a datetime string to different string format."""
    if not value:
        return None
    return datetime.strptime(value, from_format).strftime(to_format)


def format_duration(value: str) -> str:
    """Convert a duration in minutes to a duration in hours and minutes."""
    if not value:
        return None
    hours, minutes = divmod(int(value), 60)
    if hours == 0:
        return f"{minutes}min"
    if minutes == 0:
        return f"{hours}h"
    return f"{hours}h {minutes}min"
