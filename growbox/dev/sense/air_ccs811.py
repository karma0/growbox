# -*- coding: utf-8 -*-

"""CCS811 air quality sensor"""


import time
from math import log

from growbox.common.enum import Enum
from growbox.common.wire import Wire


class CCS811Register(Enum):
    STATUS          = 0x00
    MEAS_MODE       = 0x01
    ALG_RESULT_DATA = 0x02
    RAW_DATA        = 0x03
    ENV_DATA        = 0x05
    NTC             = 0x06
    THRESHOLDS      = 0x10
    BASELINE        = 0x11
    HW_ID           = 0x20
    HW_VERSION      = 0x21
    FW_BOOT_VERSION = 0x23
    FW_APP_VERSION  = 0x24
    ERROR_ID        = 0xE0
    APP_START       = 0xF4
    SW_RESET        = 0xFF


class CCS811Error(Enum):
    SUCCESS = 0x00
    ID_ERROR = 0x01
    I2C_ERROR = 0x02
    INTERNAL_ERROR = 0x03
    GENERIC_ERROR = 0x04


class CCS811DriveMode(Enum):
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

    def __init__(self, *args, **kwargs):
        env = kwargs.pop('environment', None)
        if env is not None:
            self._environment = env

        super().__init__(*args, **kwargs)

    def reset(self):
        self.write(CCS811Register.SW_RESET, [0x11, 0xE5, 0x72, 0x8A])
        time.sleep(.1)

    def begin(self):
        time.sleep(.1)

        #print("Fetching HW_ID")
        #hw_id = self.read(CCS811Register.HW_ID)
        #print(f"HW_ID: {hw_id}")
        #if hw_id != 0x81:
        #    return CCS811Error.ID_ERROR

        print("Resetting.")
        self.reset()
        time.sleep(.1)
        print("Reset.")

        print("Checking error_status.")
        if self.error_status:
            print(f"Error: {self.error}")
            return self.error

        print("Checking APP_VALID.")
        if not self.app_valid:
            print(f"App invalid: {self.app_valid}")
            return CCS811Error.INTERNAL_ERROR

        print("Starting app.")
        self.write(CCS811Register.APP_START)
        time.sleep(.1)
        print("App started.")

        print("Setting drive_mode")
        self.drive_mode = CCS811DriveMode.SECONDS_1

        if self._environment is not None:
            print("Setting environment")
            self.environment = self._environment

    def read_algorithm_results(self):
        data = self.read(CCS811Register.ALG_RESULT_DATA, 4)

        # Data ordered:
        # co2MSB, co2LSB, tvocMSB, tvocLSB
        self.co2 = (data[0] << 8) | data[1]
        self.t_voc = (data[2] << 8) | data[3]

        return CCS811Error.SUCCESS

    @property
    def error_status(self):
        return self.read(CCS811Register.STATUS) & 1 << 0

    @property
    def data_available(self):
        return self.read(CCS811Register.STATUS) & 1 << 3

    @property
    def app_valid(self):
        return self.read(CCS811Register.STATUS) & 1 << 4

    @property
    def error(self):
        return CCS811Error(self.read(CCS811Register.ERROR_ID))

    @property
    def baseline(self):
        data = self.read(CCS811Register.BASELINE, 2)
        return data[0] << 8 | data[1]

    @baseline.setter
    def baseline(self, baseline):
        data = [
            (baseline >> 8) & 0x00FF,
            baseline & 0x00FF,
        ]
        return self.write(CCS811Register.BASELINE, data)

    @property
    def drive_mode(self):
        return self._drive_mode

    @drive_mode.setter
    def drive_mode(self, mode):
        self._drive_mode = mode
        value = self.read(CCS811Register.MEAS_MODE)
        value &= ~(0b00000111 << 4)
        value |= mode << 4
        self.write(CCS811Register.MEAS_MODE, value)

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, environment):
        self._environment = environment
        celsius = self._environment.celsius * 1000
        humidity = self._environment.humidity * 1000
        celsius += 25000  # Add the 25C offset

        data = [
            int((humidity + 250) / 500),
            0,
            int((celsius + 250) / 500),
            0,
        ]
        self.write(CCS811Register.ENV_DATA, data)

    def read_ntc(self):
        data = self.read(CCS811Register.NTC, 4)
        vref_counts = (data[0] << 8) | data[1]
        ntc_counts = (data[2] << 8) | data[3]
        self.resistance = ntc_counts * self.reference_resistance / vref_counts
        self.temperature = log(self.resistance)
        self.temperature = 1 / (
            0.001129148 + (
                0.000234125 * self.temperature
            ) + (
                0.0000000876741 * (self.temperature ** 3)
            )
        )
        self.temperature -= 273.15  # Convert Kelvin to Celsius
