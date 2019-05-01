# -*- coding: utf-8 -*-

"""Generic interface for working with UV Sensors"""


from growbox.base import DeviceBase


class UVSensor(DeviceBase):
    display = [
        'index:UV Index',
    ]

    monitor = [
        'uva',
        'uvb',
        'index',
    ]
