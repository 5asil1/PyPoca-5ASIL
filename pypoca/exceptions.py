# -*- coding: utf-8 -*-

class PypocaException(Exception):
    pass


class RequestException(PypocaException):
    pass


class OMDbException(RequestException):
    pass


class TmdbException(RequestException):
    pass


class TraktException(RequestException):
    pass


class WhatIsMyMovieException(RequestException):
    pass


class NoResults(RequestException):
    pass
