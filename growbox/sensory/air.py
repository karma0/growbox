# -*- coding: utf-8 -*-

"""Generic interface for working with air quality sensors"""


from growbox.base import DeviceBase


class AirSensor(DeviceBase):
    display = [
        'co2:CO2',
    ]

    monitor = [
        'co2',
        't_voc',
        'error',
    ]

    def update(self):
        if self.device.data_available:
            self.device.read_algorithm_results()
        elif self.device.error_status:
            return self.device.error
