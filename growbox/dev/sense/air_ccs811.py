# -*- coding: utf-8 -*-

"""CCS811 air quality sensor"""


import time

from growbox.wire import Wire


class CCS811Sensor(Wire):
    """
    SparkFun's QWIIC CCS811 air quality sensor and corresponding interface.
    """
    address = 0x5B
    jump_address = 0x5A

    _humidity = None
    _temp_c = None

    start_time = time.time()

    def get_co2(self):
        pass

    def get_tvoc(self):
        pass

    def set_environment_data(self, humidity, temp_c):
        self._humidity = humidity
        self._temp_c = temp_c
