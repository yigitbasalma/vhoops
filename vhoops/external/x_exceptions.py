#!/usr/bin/python
# -*- coding: utf-8 -*-

class CustomBaseException(Exception):
    """
    Security related exception class
    """
    def __init__(self, severity, message):
        self.items = (severity, message)

    def __getitem__(self, item):
        return self.items[item]


class ResourceError(CustomBaseException):
    """
    Resource related exception class
    """
    pass


class ConditionError(CustomBaseException):
    """
    Resource related exception class
    """
    pass


class DependencyError(CustomBaseException):
    """
    Resource related exception class
    """
    pass


class SecurityError(CustomBaseException):
    """
    Security related exception class
    """
    pass


class ItemNotFoundError(CustomBaseException):
    """
    Resource related exception class
    """
    pass


class ValidationError(CustomBaseException):
    """
    Resource related exception class
    """
    pass
