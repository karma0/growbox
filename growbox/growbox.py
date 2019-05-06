# -*- coding: utf-8 -*-

"""Main module."""


import time
import csv

from collections import OrderedDict

import logging

#from growbox.wire import Wire

# Device facades
#from growbox.actuation.relay import Relay
#from growbox.io import IOExpander

#from growbox.sensory.env import EnvironmentSensor
#from growbox.sensory.air import AirSensor
#from growbox.sensory.uv import UVSensor

from growbox.dev.actuate.relay import QuadRelay
from growbox.dev.io.sx1509 import SX1509IO, IOMode, IOLogic
from growbox.bme280 import BME280
#from growbox.ccs811 import CCS811
from growbox.veml6075 import VEML6075


logger = logging.getLogger(__name__)

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


class Fans:
    upper_fan_pins = [6, 7]
    lower_fan_pins = [4, 5]

    def __init__(self, fans, pins=None):
        self.fans = fans

        if pins is not None:
            self.upper_fan_pins, self.lower_fan_pins = pins

        for pin in self.upper_fan_pins + self.lower_fan_pins:
            self.fans.pin_mode(pin, IOMode.ANALOG_OUTPUT)
            self.fans.analog_write(pin, IOLogic.HIGH)  # LOW=on; HIGH=off

    def upper_fans_on(self):
        logger.info("Upper fans on.")
        for pin in self.upper_fan_pins:
            self.fans.analog_write(pin, IOLogic.LOW)

    def upper_fans_off(self):
        logger.info("Upper fans off.")
        for pin in self.upper_fan_pins:
            self.fans.analog_write(pin, IOLogic.HIGH)

    def lower_fans_on(self):
        logger.info("Lower fans on.")
        for pin in self.lower_fan_pins:
            self.fans.analog_write(pin, IOLogic.LOW)

    def lower_fans_off(self):
        logger.info("Lower fans off.")
        for pin in self.lower_fan_pins:
            self.fans.analog_write(pin, IOLogic.HIGH)

    def add_oxygen(self):
        logger.info("Adding oxygen")
        self.upper_fans_on()
        time.sleep(5)
        self.upper_fans_off()

    def remove_co2(self):
        logger.info("Removing CO2")
        self.lower_fans_on()
        time.sleep(5)
        self.lower_fans_off()

    def exchange(self):
        logger.info("Exchanging air.")
        self.upper_fans_on()
        self.lower_fans_on()
        time.sleep(5)
        self.upper_fans_off()
        self.lower_fans_off()

    def status(self):
        pass


class Relay:
    def __init__(self, relays, relay_id=0):
        self.relays = relays
        self._id = relay_id

    def on(self):
        logger.info(f"Relay {self._id} on.")
        self.relays.on(self._id)
        time.sleep(5)

    def off(self):
        logger.info(f"Relay {self._id} off.")
        self.relays.off(self._id)
        time.sleep(5)

    def toggle(self):
        logger.info(f"Relay {self._id} toggle.")
        self.relays.toggle(self._id)

    @property
    def status(self):
        status = self.relays.get_status_by_id(self._id)
        logger.info("Relay {self._id} status = {status}")
        return status


class Timer:
    last_time = time.time()

    def __init__(self, action=None, **kwargs):
        self.action = action
        self.seconds = kwargs.pop('seconds', 0)
        self.seconds += kwargs.pop('minutes', 0) * 60
        self.seconds += kwargs.pop('hours', 0) * 60 * 60
        self.seconds += kwargs.pop('days', 0) * 60 * 60 * 24

    def __call__(self):
        """Call to update time"""
        if self.timesup:
            logger.info("Time is up on timer for {self.seconds} seconds.")
            self.last_time = time.time()
            if callable(self.action):
                self.action()

    @property
    def timesup(self):
        """Return True if time is up"""
        return self.last_time < (time.time() - self.seconds)


class Range:
    minval = 0
    maxval = 0

    def __init__(self, action=None, minval=None, maxval=None):
        self.action = action
        self.minval = minval
        self.maxval = maxval

    def valinrange(self, value):
        if self.maxval is None:
            return value > self.minval
        elif self.minval is None:
            return value < self.maxval

        return value > self.minval and value < self.maxval


class InRange(Range):
    """
    Ensures a value is in range, and if it isn't, will execute action.
    """
    def __call__(self, value):
        if self.valinrange(value):
            return True

        logger.info("Value ({value}) out of range: {self.minval}-{self.maxval}")
        if self.action is not None:
            self.action()

        return False


class OutOfRange(Range):
    """
    Ensures a value is out of range, and if it isn't, will execute action.
    """
    def __call__(self, value):
        if not self.valinrange(value):
            return True

        logger.info("Value ({value}) within range: {self.minval}-{self.maxval}")
        if self.action is not None:
            self.action()

        return False


class Profile:
    box = None  # growbox

    celsius = None
    humidity = None
    co2 = None
    uv_index = None
    air_exchange_rate = None

    def __init__(self, growbox=None, profile=None):
        self.box = growbox

        if profile is not None:
            self.profile = profile

    def __call__(self, data):

        #if not self.celsius(data['celsius']):
        #    if data['celsius'] < self.celsius.minval:
        #        self.box.fans.stop()
        #    elif data['celsius'] > self.celsius.maxval:
        #        self.box.fans.exchange()

        if not self.humidity(data['humidity']):
            if data['humidity'] < self.humidity.minval:
                self.box.mister.on()
            elif data['humidity'] > self.humidity.maxval:
                self.box.mister.off()

        if self.air_exchange_rate():
            self.box.mister.off()
            self.box.fans.exchange()

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, profile):
        self._profile = profile
        for key, valrange in profile:
            setattr(self, key, valrange)

        # Set some defaults
        #if self.celsius is None:
        #    self.celsius = InRange(18, 24)
        if self.humidity is None:
            self.humidity = InRange(95, 100)
        #if self.co2 is None:
        #    self.co2 = InRange(minval=5000)
        if self.air_exchange_rate is None:
            self.air_exchange_rate = Timer(minutes=20)

    @property
    def growbox(self):
        return self.box

    @growbox.setter
    def growbox(self, growbox):
        self.box = growbox


class GrowBox:

    rate = 10  # rate in seconds at which to read values

    fields = {}

    relays = OrderedDict([
        ('heater', 0)
        ('lamp', 1)
        ('none', 3)
        ('humidifier', 2)
    ])

    def __init__(self, profile):
        self.bme280 = BME280()
        #self.ccs811 = CCS811()
        self.veml = VEML6075()
        self.relays = QuadRelay()
        self.fans = Fans(SX1509IO())

        self.process = Profile(growbox=self, profile=profile)

    def setup_parameters(self):
        self.fields = OrderedDict(
            ('localtime', time),
            ('celsius', self.bme280),
            ('fahrenheit', self.bme280),
            ('pressure', self.bme280),
            ('altitude', self.bme280),
            #('co2', self.ccs811),
            #('tvoc', self.ccs811),
            ('uv_index', self.veml),
            ('uva', self.veml),
            ('uvb', self.veml),
            ('relays_status', self.relays),
            ('fans_status', self.fans),
        )

    def begin(self):
        self.relays.begin()
        self.setup_relays()

        self.fans.fans.begin()
        #self.fans.setup_fans()

        self.setup_parameters()

    def run(self):
        self.begin()

        with open('growbox.log', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, quoting=csv.QUOTE_MINIMAL,
                    fieldnames=self.fields.keys())

            while True:
                data = {}
                for field, obj in self.fields:
                    getter = getattr(obj, field)

                    if callable(getter):
                        value = getter()
                    else:
                        value = getter

                    if isinstance(value, dict):
                        data.update(value.items())
                    else:
                        data[field] = value

                writer.writerow(data)
                self.process(data)
                time.sleep(self.rate)

    # Relays

    def setup_relays(self):
        self.mister = Relay(self.relays, relay_id=4)

    def relay_status(self):
        return OrderedDict([
            ("relay{}".format(ix), str(val))
            for ix, val in enumerate(self.relays.status)
        ])
