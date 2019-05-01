# -*- coding: utf-8 -*-

"""Generic interface for working with I/O expanders"""


from growbox.base import DeviceBase


class IOExpander(DeviceBase):
    display = ['status:I/O']
    monitor = ['status']
