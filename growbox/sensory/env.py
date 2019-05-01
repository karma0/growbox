# -*- coding: utf-8 -*-

"""Generic interface for working with air quality sensors"""


from growbox.base import DeviceBase


class EnvironmentSensor(DeviceBase):
    display = [
        'fahrenheit:F',
        'humidity:%',
    ]

    monitor = [
        'celsius',
        'humidity',
    ]
