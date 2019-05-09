# -*- coding: utf-8 -*-

"""Main module."""


import time
import csv

from collections import OrderedDict

import logging

from growbox.dev.actuate.relay import QuadRelay
from growbox.dev.io.sx1509 import SX1509IO
from growbox.dev.sense.bme280 import BME280
#from growbox.dev.sense.ccs811 import CCS811
from growbox.dev.sense.veml6075 import VEML6075

from growbox.facade.relay import Relay
from growbox.facade.fans import Fans
from growbox.profile import Profile


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GrowBox:

    rate = 10  # rate in seconds at which to read values
    fields = None

    relays = OrderedDict([
        ('mister', 0),
        ('heater', 1),
        ('lamp', 2),
        ('none', 3),
    ])

    def __init__(self, profile=None, logfile='growbox.log'):
        self.logfile = logfile

        self.bme280 = BME280()
        #self.ccs811 = CCS811()
        self.veml = VEML6075()
        self.quad_relay = QuadRelay()
        self.mister = Relay(self.quad_relay, relay_id=self.relays.get('mister'))
        self.fans = Fans(SX1509IO())

        self.process = Profile(growbox=self, profile=profile)
        self.process.profile = {}

        self.fields = OrderedDict([
            ('localtime', time),
            ('celsius', self.bme280),
            ('fahrenheit', self.bme280),
            ('altitude', self.bme280),
            ('humidity', self.bme280),
            #('co2', self.ccs811),
            #('tvoc', self.ccs811),
            ('uv_index', self.veml),
            ('uva', self.veml),
            ('uvb', self.veml),
            ('mister_status', self),
            ('upper_fans_status', self.fans),
            ('lower_fans_status', self.fans),
        ])

    def begin(self):
        self.quad_relay.begin()
        self.fans.fans.begin()

    def run(self):
        self.begin()

        with open(self.logfile, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, quoting=csv.QUOTE_MINIMAL,
                                    fieldnames=self.fields.keys())

            logger.info("Looping...")
            while True:
                start = time.time()
                data = {}

                for field, obj in self.fields.items():
                    getter = getattr(obj, field)
                    value = getter() if callable(getter) else getter

                    if isinstance(value, dict):
                        data.update(value.items())
                    else:
                        data[field] = value

                writer.writerow(data)

                logger.info("Processing data")
                self.process(data)

                left = start + self.rate - time.time()
                logger.info(f"Sleeping {left} seconds")
                if left > 0:
                    time.sleep(left)

    def mister_status(self):
        return self.mister.status
