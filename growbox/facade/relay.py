# -*- coding: utf-8 -*-

"""Main module."""


import time
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Relay:
    def __init__(self, quad_relay, relay_id=0):
        self.quad_relay = quad_relay
        self._id = relay_id

    def on(self):
        logger.info(f"Relay {self._id} on.")
        self.quad_relay.on(self._id)

    def off(self):
        logger.info(f"Relay {self._id} off.")
        self.quad_relay.off(self._id)

    def toggle(self):
        logger.info(f"Relay {self._id} toggle.")
        self.quad_relay.toggle(self._id)

    def humidify(self):
        self.on()
        time.sleep(10)
        self.off()

    @property
    def status(self):
        status = self.quad_relay.get_status_by_id(self._id)
        return None if status is None else int(status)
