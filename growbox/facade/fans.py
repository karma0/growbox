# -*- coding: utf-8 -*-

"""Main module."""


import time
import logging
from collections import OrderedDict

from growbox.dev.io.sx1509 import IOLogic, IOMode


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Fans:
    upper_fan_pins = (6, 7)
    lower_fan_pins = (4, 5)

    status = OrderedDict([
        ('upper_fans', 0),
        ('lower_fans', 0),
    ])

    def __init__(self, fans, pins=None):
        self.fans = fans

        if pins is not None:
            self.upper_fan_pins, self.lower_fan_pins = pins

        for pin in self.upper_fan_pins + self.lower_fan_pins:
            self.fans.pin_mode(pin, IOMode.ANALOG_OUTPUT)
            self.fans.analog_write(pin, IOLogic.HIGH)  # LOW=on; HIGH=off

    def upper_fans_on(self):
        logger.info("Upper fans on.")
        self.status['upper_fans'] = 1

        for pin in self.upper_fan_pins:
            self.fans.analog_write(pin, IOLogic.LOW)

    def upper_fans_off(self):
        logger.info("Upper fans off.")
        self.status['upper_fans'] = 0

        for pin in self.upper_fan_pins:
            self.fans.analog_write(pin, IOLogic.HIGH)

    def lower_fans_on(self):
        logger.info("Lower fans on.")
        self.status['lower_fans'] = 1

        for pin in self.lower_fan_pins:
            self.fans.analog_write(pin, IOLogic.LOW)

    def lower_fans_off(self):
        logger.info("Lower fans off.")
        self.status['lower_fans'] = 0

        for pin in self.lower_fan_pins:
            self.fans.analog_write(pin, IOLogic.HIGH)

    def add_oxygen(self):
        logger.info("Adding oxygen")
        self.upper_fans_on()
        time.sleep(5)
        self.upper_fans_off()

    def remove_co2(self):
        logger.info("Removing CO2")
        self.lower_fans_on()
        time.sleep(5)
        self.lower_fans_off()

    def exchange(self):
        logger.info("Exchanging air.")
        self.upper_fans_on()
        self.lower_fans_on()
        time.sleep(5)
        self.upper_fans_off()
        self.lower_fans_off()

    @property
    def upper_fans_status(self):
        return self.status['upper_fans']

    @property
    def lower_fans_status(self):
        return self.status['lower_fans']
