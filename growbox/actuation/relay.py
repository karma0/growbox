# -*- coding: utf-8 -*-

"""Generic interface for working with relays"""


from growbox.base import DeviceBase


class RelayActuator(DeviceBase):
    display = ['status:Act']
    monitor = ['status']

    status = None

    def update(self):
        status = self.device.status
        if isinstance(status, list):
            self.status = [
                'X' if stat else 'O'
                for stat in status
            ]
        else:
            self.status = 'X' if status else 'O'
