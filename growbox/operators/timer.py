# -*- coding: utf-8 -*-

"""Main module."""


import time
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Timer:
    def __init__(self, action=None, **kwargs):
        self.action = action
        self.seconds = kwargs.pop('seconds', 0)
        self.seconds += kwargs.pop('minutes', 0) * 60
        self.seconds += kwargs.pop('hours', 0) * 60 * 60
        self.seconds += kwargs.pop('days', 0) * 60 * 60 * 24
        self.set_timer()

    def set_timer(self):
        self.next_time = time.time() + self.seconds

    def __call__(self):
        """Call to update time"""
        if self.timesup:
            logger.info(f"Time is up on timer for {self.seconds} seconds.")
            self.set_timer()
            if callable(self.action):
                self.action()
            return True
        return False

    @property
    def timesup(self):
        """Return True if time is up"""
        return self.next_time < time.time()
