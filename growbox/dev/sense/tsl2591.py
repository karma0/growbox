# -*- coding: utf-8 -*-

import time

import board
import busio

import adafruit_tsl2591


class TSL2591:
    def __init__(self, gain=None, integration_time=None):
        # Initialize the I2C bus.
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Initialize the sensor.
        self.sensor = adafruit_tsl2591.TSL2591(self.i2c)

        # You can optionally change the gain and integration time:
        #self.sensor.gain = adafruit_tsl2591.GAIN_LOW (1x gain)
        #self.sensor.gain = adafruit_tsl2591.GAIN_MED (25x gain, the default)
        #self.sensor.gain = adafruit_tsl2591.GAIN_HIGH (428x gain)
        #self.sensor.gain = adafruit_tsl2591.GAIN_MAX (9876x gain)
        self.sensor.gain = adafruit_tsl2591.GAIN_MED if gain is None else gain

        #sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS (100ms)
        #sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS (200ms)
        #sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS (300ms)
        #sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS (400ms)
        #sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_500MS (500ms)
        #sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS (600ms)
        self.sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS \
                if integration_time is None else integration_time

    @property
    def lux(self):
        return self.sensor.lux

    @property
    def infrared(self):
        """
        You can also read the raw infrared and visible light levels.
        These are unsigned, the higher the number the more light of that type.
        There are no units like lux.
        Infrared levels range from 0-65535 (16-bit)
        """
        return self.sensor.infrared

    @property
    def visible(self):
        """Visible-only levels range from 0-2147483647 (32-bit)"""
        return self.sensor.visible

    @property
    def full_spectrum(self):
        """Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)"""
        return self.sensor.full_spectrum


def main():
    tsl2591 = TSL2591()
    while True:
        lux = tsl2591.lux
        infrared = tsl2591.infrared
        visible = tsl2591.visible
        full_spectrum = tsl2591.full_spectrum

        print('Total light: {0}lux'.format(lux))
        print('Infrared light: {0}'.format(infrared))
        print('Visible light: {0}'.format(visible))
        print('Full spectrum (IR + visible) light: {0}'.format(full_spectrum))
        time.sleep(1.0)


if __name__ == "__main__":
    main()
