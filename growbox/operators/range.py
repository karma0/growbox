# -*- coding: utf-8 -*-

"""Main module."""


import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Range:
    minval = 0
    maxval = 0
    action = None

    def __init__(self, minval=None, maxval=None, action=None):
        self.minval = minval
        self.maxval = maxval
        self.action = action

    def valinrange(self, value):
        if self.maxval is None:
            return value > self.minval
        elif self.minval is None:
            return value < self.maxval

        return value > self.minval and value < self.maxval


class InRange(Range):
    """
    Ensures a value is in range, and if it isn't, will execute action.
    """
    def __call__(self, value):
        if self.valinrange(value):
            return True

        logger.info(f"Value ({value}) out of range: {self.minval}-{self.maxval}")
        if self.action is not None:
            self.action()

        return False


class OutOfRange(Range):
    """
    Ensures a value is out of range, and if it isn't, will execute action.
    """
    def __call__(self, value):
        if not self.valinrange(value):
            return True

        logger.info(f"Value ({value}) within range: {self.minval}-{self.maxval}")
        if self.action is not None:
            self.action()

        return False
