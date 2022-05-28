# -*- coding: utf-8 -*-

class PypocaException(BaseException):
    pass


class RequestException(PypocaException):
    pass


class TmdbException(RequestException):
    pass


class NoResults(TmdbException):
    pass


class TraktException(RequestException):
    pass
