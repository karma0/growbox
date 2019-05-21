# -*- coding: utf-8 -*-

"""Main module."""


class Environment:
    def __init__(self, thermometer, hygrometer):
        self.thermometer = thermometer
        self.hygrometer = hygrometer

    @property
    def fahrenheit(self):
        return self.thermometer.fahrenheit

    @property
    def temperature(self):
        return self.thermometer.temperature

    @property
    def celsius(self):
        return self.thermometer.celsius

    @property
    def humidity(self):
        return self.hygrometer.humidity
