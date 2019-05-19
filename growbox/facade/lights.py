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
            autowrite=False,
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

    def wheel(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b) if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)

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

    for _ in range(255):
        lights.brighten()
        time.sleep(.01)

    for _ in range(255):
        lights.darken()
        time.sleep(.01)

    lights.off()
    time.sleep(5)
    lights.on()
    time.sleep(5)
    lights.off()


if __name__ == "__main__":
    main()
