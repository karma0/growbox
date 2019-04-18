# -*- coding: utf-8 -*-

"""Main module."""


from growbox.wire import Wire

from growbox.dev.actuate.relay import *

from growbox.dev.sense.env_bme280 import *
from growbox.dev.sense.air_ccs811 import *
from growbox.dev.sense.uv_veml6075 import *


class ApplicationBuilder:
    """Create a useable application."""
    devices: list = []

    def build_generic_device(self, address, *args, cls=Wire, **kwargs):
        device = cls(*args, address=address, **kwargs)
        self.devices.append(device)
        return device

    #def build_switch(self, *args, address=None, **kwargs):
    #    return self.build_generic_device(address, *args, cls=Relay, **kwargs)

    def build_quad_switch(self, *args, address=None, **kwargs):
        return self.build_generic_device(address, *args, cls=QuadRelay, **kwargs)

    def build_uv_sensor(self, *args, address=None, **kwargs):
        return self.build_generic_device(address, *args, cls=UVSensor, **kwargs)
