# -*- coding: utf-8 -*-

"""Main module."""


import time
import csv

from collections import OrderedDict

#from growbox.wire import Wire

# Device facades
#from growbox.actuation.relay import Relay
#from growbox.io import IOExpander

#from growbox.sensory.env import EnvironmentSensor
#from growbox.sensory.air import AirSensor
#from growbox.sensory.uv import UVSensor

from growbox.dev.actuation.relay import QuadRelay
from growbox.dev.io.sx1509 import SX1509IO, IOMode, IOLogic
from growbox.bme280 import BME280
#from growbox.ccs811 import CCS811
from growbox.veml6075 import VEML6075


#class ApplicationBuilder:
#    """Create a useable application."""
#    devices: dict = {
#        IOExpander,
#        Relay,
#        EnvironmentSensor,
#        AirSensor,
#        UVSensor
#    }
#    _devinsts: dict = {}
#
#    def build_generic_device(self, address, *args, cls=Wire, **kwargs):
#        device = cls(*args, address=address, **kwargs)
#        self._devinsts[cls.__name__] = device
#        return device
#
#    def build_app(self, devices=None):
#        if devices is not None:
#            assert isinstance(devices, dict)
#            # facade.__name__: growbox.wire.Wire type
#
#            self.devices = devices
#
#        for facade_name, device in self.devices:
#            # TODO: Work out integration
#            pass
#
#
#    def create_action(self, device, name, action, *args, **kwargs):
#        # TODO: Refactor devices, and add alias to specific device action
#        pass


class GrowBox:
    upper_fan_pins = [6, 7]
    lower_fan_pins = [4, 5]

    rate = 10  # rate in seconds at which to read values

    fields = {}

    relays = OrderedDict([
        ('humidifier', 0)
        ('heater', 1)
        ('lamp', 2)
        ('none', 3)
    ])

    def __init__(self):
        self.bme280 = BME280()
        #self.ccs811 = CCS811()
        self.veml = VEML6075()
        self.relays = QuadRelay()
        self.fans = SX1509IO()

    def setup_parameters(self):
        self.fields = OrderedDict(
            ('localtime', time),
            ('celsius', self.bme280),
            ('fahrenheit', self.bme280),
            ('pressure', self.bme280),
            ('altitude', self.bme280),
            ('co2', self.ccs811),
            ('tvoc', self.ccs811),
            ('uv_index', self.veml),
            ('uva', self.veml),
            ('uvb', self.veml),
            ('relays_status', self),
            ('fans_status', self),
        )

    def begin(self):
        self.relays.begin()
        self.setup_relays()

        self.fans.begin()
        self.setup_fans()

        self.setup_parameters()

    def run(self):
        with open('grobox.log', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, quoting=csv.QUOTE_MINIMAL,
                    fieldnames=self.fields.keys())

            while True:
                data = {}
                for field, obj in self.fields:
                    getter = getattr(obj, field)
                    value = getter
                    if callable(getter):
                        value = getter()
                        if isinstance(value, dict):
                            data[field

                self.process_logic(data)
                time.sleep(self.rate)

    # Relays

    def relay_status(self):
        return OrderedDict([
            ("relay{}".format(ix), str(val))
            for ix, val in enumerate(self.relays.status)
        ])

    # Fans

    def fan_status(self):
        return OrderedDict([
            ("fan{}".format(ix), str(val))
            for ix, val in enumerate(self.fans.status)
        ])

    def setup_fans(self):
        for pin in self.upper_fan_pins + self.lower_fan_pins:
            self.fans.pin_mode(pin, IOMode.ANALOG_OUTPUT)
            self.fans.analog_write(pin, IOLogic.HIGH)  # LOW=on; HIGH=off

    def add_oxygen(self):
        for pin in self.upper_fan_pins:
            self.fans.analog_write(pin, IOLogic.LOW)

    def remove_co2(self):
        for pin in self.lower_fan_pins:
            self.fans.analog_write(pin, IOLogic.LOW)
