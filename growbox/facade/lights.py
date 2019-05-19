# -*- coding: utf-8 -*-

"""Main module."""


import time
import logging
from operator import add, sub

import board
import neopixel


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Lights:
    pin = board.D10
    pixel_count = 14
    order = neopixel.RGBW

    _value = [0, 0, 0, 0]  # RGBW

    def __init__(self):
        self.pixels = neopixel.NeoPixel(
            self.pin,
            self.pixel_count,
            pixel_order=self.order,
        )

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, rgbw):
        rgbw = [val if val < 256 else 255 for val in rgbw]
        rgbw = [val if val > 0 else 0 for val in rgbw]
        self._value = rgbw

    def on(self):
        logger.info("Lights on.")
        self.value = [255, 255, 255, 255]
        self.pixels.fill(self.value)

    def off(self):
        logger.info("Lights off.")
        self.value = [0, 0, 0, 0]  # RGBW
        self.pixels.fill(self.value)

    def darken(self, red=1, green=1, blue=1, white=1):
        self.value = list(map(sub, self.value, [red, green, blue, white]))
        self.pixels.fill(self.value)

    def brighten(self, red=1, green=1, blue=1, white=1):
        self.value = list(map(add, self.value, [red, green, blue, white]))
        self.pixels.fill(self.value)


def main():
    lights = Lights()

    for i  in range(255):
        lights.brighten(i, i, i, i)
        time.sleep(.01)

    for i  in range(255):
        lights.darken(i, i, i, i)
        time.sleep(.01)


if __name__ == "__main__":
    main()
