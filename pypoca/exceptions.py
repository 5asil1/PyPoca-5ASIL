# -*- coding: utf-8 -*-

class PypocaException(BaseException):
    pass


class RequestException(PypocaException):
    pass


class TmdbException(RequestException):
    pass


class TraktException(RequestException):
    pass


class WhatIsMyMovieException(RequestException):
    pass


class NoResults(RequestException):
    pass
