# -*- coding: utf-8 -*-

"""Main module."""


import time
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Lights:
    def __init__(self):
        pass

    def on(self):
        logger.info(f"Lights on.")
        self.quad_relay.on(self._id)

    def off(self):
        logger.info(f"Lights off.")
        self.quad_relay.off(self._id)

    def darken(self):
        pass

    def brighten(self):
        pass
