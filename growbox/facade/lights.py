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
    pin = board.D10  # MOSI (to run as user)
    pixel_count = 14
    order = neopixel.GRBW

    _value = [0, 0, 0, 0]  # RGBW

    def __init__(self):
        self.pixels = neopixel.NeoPixel(
            self.pin,
            self.pixel_count,
            brightness=.5,
            auto_write=False,
            pixel_order=self.order,
        )
        self.pixels.show()  # Reset the pixels

    @property
    def lights(self):
        return self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, rgbw):
        rgbw = [val if val < 256 else 255 for val in rgbw]
        rgbw = [val if val > 0 else 0 for val in rgbw]
        self._value = rgbw
        self.display()

    def wheel(self, pos):
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
        return (r, g, b) if self.order == neopixel.RGB or self.order == neopixel.GRB else (r, g, b, 0)

    def rainbow_cycle(self, wait):
        for j in range(255):
            for i in range(self.pixel_count):
                pixel_index = (i * 256 // self.pixel_count) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def display(self):
        self.pixels.fill(self.value)
        self.pixels.show()

    def on(self):
        logger.info("Lights on.")
        self.value = [255, 255, 255, 255]
        #self.display()

    def off(self):
        logger.info("Lights off.")
        self.value = [0, 0, 0, 0]  # RGBW
        #self.display()

    def darker(self, red=1, green=1, blue=1, white=1):
        self.value = list(map(sub, self.value, [red, green, blue, white]))
        #self.display()

    def brighter(self, red=1, green=1, blue=1, white=1):
        self.value = list(map(add, self.value, [red, green, blue, white]))
        #self.display()


def main():
    pixel_pin = board.D10
    num_pixels = 14
    order = neopixel.GRBW

    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, pixel_order=order,
                               brightness=0.3, auto_write=False)

    #lights = Lights()
    #red = 0x100000
    red = (255, 0, 0, 0)
    yellow = (255, 150, 0, 0)
    green = (0, 255, 0, 0)
    cyan = (0, 255, 255, 0)
    blue = (0, 0, 255, 0)
    purple = (180, 0, 255, 0)

    try:
        while True:
            pixels.fill(red)
            pixels.show()
            time.sleep(1)
            pixels.fill(yellow)
            pixels.show()
            time.sleep(1)
            pixels.fill(green)
            pixels.show()
            time.sleep(1)
            pixels.fill(cyan)
            pixels.show()
            time.sleep(1)
            pixels.fill(blue)
            pixels.show()
            time.sleep(1)
            pixels.fill(purple)
            pixels.show()
            time.sleep(1)
    except KeyboardInterrupt:
        pixels.fill((0, 0, 0, 0))
        pixels.show()
        pixels.deinit()

    #for i in range(len(lights.pixels)):
    #    lights.pixels[i] = red
    #time.sleep(5)

    #lights.pixels[::2] = [red] * (len(lights.pixels) // 2)
    #time.sleep(2)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    # lights.pixels.fill((255, 0, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    #lights.pixels.fill((255, 0, 0, 0))
    #lights.pixels.show()
    #time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    # lights.pixels.fill((0, 255, 0))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    #lights.pixels.fill((0, 255, 0, 0))
    #lights.pixels.show()
    #time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    # lights.pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    #lights.pixels.fill((0, 0, 255, 0))
    #lights.pixels.show()
    #time.sleep(1)

    # Comment this line out if you have RGBW/GRBW NeoPixels
    # lights.pixels.fill((0, 0, 255))
    # Uncomment this line if you have RGBW/GRBW NeoPixels
    #lights.pixels.fill((0, 0, 0, 255))
    #lights.pixels.show()
    #time.sleep(1)

    #lights.rainbow_cycle(0.1)    # rainbow cycle with 1ms delay per step

    #for _ in range(255):
    #    lights.brighten()
    #    time.sleep(.01)

    #for _ in range(255):
    #    lights.darken()
    #    time.sleep(.01)

    #lights.off()
    #time.sleep(5)
    #lights.on()
    #time.sleep(5)
    #lights.off()
    #time.sleep(1)
    #lights.pixels.deinit()


if __name__ == "__main__":
    main()
