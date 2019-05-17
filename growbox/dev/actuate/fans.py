# -*- coding: utf-8 -*-

"""Main module."""


import time
import logging
from collections import OrderedDict

import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor.motor import DCMotor

from growbox.common.enum import Enum


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Motors(Enum):
    MOTOR1 = 0
    MOTOR2 = 2
    MOTOR3 = 4
    MOTOR4 = 5


class Fans:
    address = 0x40

    upper_fans = (Motors.MOTOR1, Motors.MOTOR2)
    lower_fans = (Motors.MOTOR3, Motors.MOTOR4)

    status = OrderedDict([
        ('upper_fans', 0),
        ('lower_fans', 0),
    ])

    def __init__(self, address=None, pins=None):
        if address is not None:
            self.address = address

        self.i2c = busio.I2C(SCL, SDA)
        self.pca = PCA9685(self.i2c, address=address)
        self.pca.frequency = 100

        if pins is not None:
            self.upper_fans = pins[:len(pins)//2]
            self.lower_fans = pins[len(pins)//2:]

        self.fans = [self.get_motor(motor) for motor in
                     self.upper_fans + self.lower_fans]

    def get_motor(self, motor):
        return DCMotor(self.pca.channels[motor.value],
                       self.pca.channels[motor.value + 2])

    def upper_fans_on(self):
        logger.info("Upper fans on.")
        self.status['upper_fans'] = 1

        for motor in self.upper_fans:
            self.fans[motor.value].throttle = 1

    def upper_fans_off(self):
        logger.info("Upper fans off.")
        self.status['upper_fans'] = 0

        for motor in self.upper_fans:
            self.fans[motor.value].throttle = None

    def lower_fans_on(self):
        logger.info("Lower fans on.")
        self.status['lower_fans'] = 1

        for motor in self.lower_fans:
            self.fans[motor.value].throttle = 1

    def lower_fans_off(self):
        logger.info("Lower fans off.")
        self.status['lower_fans'] = 0

        for motor in self.lower_fans:
            self.fans[motor.value].throttle = None

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

    @property
    def upper_fans_status(self):
        return self.status['upper_fans']

    @property
    def lower_fans_status(self):
        return self.status['lower_fans']