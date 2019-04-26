# -*- coding: utf-8 -*-

"""CCS811 air quality sensor"""


import time
from math import log

from growbox.enum import Enum
from growbox.wire import Wire


class CSS811Register(Enum):
    STATUS 0x00
    MEAS_MODE 0x01
    ALG_RESULT_DATA 0x02
    RAW_DATA 0x03
    ENV_DATA 0x05
    NTC 0x06
    THRESHOLDS 0x10
    BASELINE 0x11
    HW_ID 0x20
    HW_VERSION 0x21
    FW_BOOT_VERSION 0x23
    FW_APP_VERSION 0x24
    ERROR_ID 0xE0
    APP_START 0xF4
    SW_RESET 0xFF


class CSS811Error(Enum):
    SUCCESS = 0x00
    ID_ERROR = 0x01
    I2C_ERROR = 0x02
    INTERNAL_ERROR = 0x03
    GENERIC_ERROR = 0x04


class CSS811DriveMode(Enum):
    IDLE       = 0
    SECONDS_1  = 1
    SECONDS_10 = 2
    SECONDS_60 = 3
    RAW        = 4


class CCS811Sensor(Wire):
    """
    SparkFun's QWIIC CCS811 air quality sensor and corresponding interface.
    """
    address = 0x5B
    jump_address = 0x5A

    temperature = 0
    resistance = 0
    t_voc = 0
    co2 = 0

    # Environmental modifiers
    _environment = None
    humidity = None
    celsius = None

    reference_resistance = 10000

    start_time = time.time()

    def begin(self):
        reset_key = [0x11, 0xE5, 0x72, 0x8A]
        self.begin_core()
        self.write(CSS811Register.SW_RESET, reset_key)

        temp = 0
        for step in range(200000):
            temp += 1

        if self.error_status or not self.app_valid:
            return CSS811Error.INTERNAL_ERROR

        if self.write(CSS811Register.APP_START) != 0:
            return CSS811Error.I2C_ERROR

        self.drive_mode = CSS811DriveMode.SECONDS_1

    def read_algorithm_results(self):
        data = self.read(CSS811Register.ALG_RESULT_DATA, 4)

        # Data ordered:
	# co2MSB, co2LSB, tvocMSB, tvocLSB
        self.co2 = (data[0] << 8) | data[1]
        self.t_voc = (data[2] << 8) | data[3]

        return CSS811Error.SUCCESS

    @property
    def error_status(self):
        return self.read(CSS811Register.STATUS) & 1 << 0

    @property
    def data_available(self):
        return self.read(CSS811Register.STATUS) & 1 << 3

    @property
    def app_valid(self):
        return self.read(CSS811Register.STATUS) & 1 << 4

    @property
    def error(self):
        return CSS811Error(self.read(CSS811Register.ERROR_ID))

    @property
    def baseline(self):
        data = self.read(CSS811Register.BASELINE, 2)
        return data[0] << 8 | data[1]

    @baseline.setter
    def baseline(self, baseline):
        data = [
            (baseline >> 8) & 0x00FF,
            baseline & 0x00FF,
        ]
        return self.write(CSS811Register.BASELINE, data)

    @property
    def drive_mode(self):
        return self._drive_mode

    @drive_mode.setter
    def drive_mode(self, mode):
        self._drive_mode = mode
        value = self.read(CSS811Register.MEAS_MODE)
        value &= ~(0b00000111 << 4)
        value |= mode << 4
        self.write(CSS811Register.MEAS_MODE, value)

    @property
    def environment(self):
        return self._environment

    @property.setter
    def environment(self, environment):
        self._environment = environment
        humidity = self._environment.humidity * 1000
        celsius = self._environment.celsius * 1000
        celsius += 25000  # Add the 25C offset

        data = [
            (humidity + 250) / 500, 0,
            (celsius + 250) / 500, 0,
        ]
        self.write(CSS811Register.ENV_DATA, data)

    def read_ntc(self):
        data = self.read(CSS811Register.NTC, 4)
        vref_counts = (data[0] << 8) | data[1]
        ntc_counts = (data[2] << 8) | data[3]
        self.resistance = ntc_counts * self.reference_resistance / vref_counts
        self.temperature = log(self.resistance)
        self.temperature = 1 / (
            0.001129148 + (
                0.000234125 * temperature
            ) + (
                0.0000000876741 * (temperature ** 3)
            )
        )
        self.temperature -= 273.15  # Convert Kelvin to Celsius
