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
        logger.info(f"Relays {self._id} & {self._id + 1} on.")
        self.quad_relay.on(self._id)
        self.quad_relay.on(self._id + 1)

    def off(self):
        logger.info(f"Relays {self._id} & {self._id + 1} off.")
        self.quad_relay.off(self._id)
        self.quad_relay.off(self._id + 1)

    def toggle(self):
        logger.info(f"Relays {self._id} & {self._id + 1} toggle.")
        self.quad_relay.toggle(self._id)
        self.quad_relay.toggle(self._id + 1)

    def humidify(self):
        self.on()
        time.sleep(10)
        self.off()

    @property
    def status(self):
        status = self.quad_relay.get_status_by_id(self._id)
        return None if status is None else int(status)
