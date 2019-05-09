# -*- coding: utf-8 -*-

"""Main module."""

import logging

from growbox.operators.range import InRange
from growbox.operators.timer import Timer


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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

        #if self.celsius is not None:
        #    if not self.celsius(data['celsius']):
        #        if data['celsius'] < self.celsius.minval:
        #            self.box.fans.stop()
        #        elif data['celsius'] > self.celsius.maxval:
        #            self.box.fans.exchange()

        if self.humidity is not None:
            if not self.humidity(data['humidity']):
                if data['humidity'] < self.humidity.minval:
                    self.box.mister.humidify()
                elif data['humidity'] > self.humidity.maxval:
                    self.box.fans.exchange()

        if self.air_exchange_rate is not None:
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
            self.air_exchange_rate = Timer(minutes=1)

    @property
    def growbox(self):
        return self.box

    @growbox.setter
    def growbox(self, growbox):
        self.box = growbox
