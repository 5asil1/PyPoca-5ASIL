# -*- coding: utf-8 -*-


class PyPocaException(Exception):
    """Base exception class for PyPoca."""


class RequestFailed(PyPocaException):
    """An HTTP exception occurred."""


class NotFound(PyPocaException):
    """Command request returns no results."""
