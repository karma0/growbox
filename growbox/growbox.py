# -*- coding: utf-8 -*-

"""Main module."""


from growbox.wire import Wire

# Device facades
from growbox.actuation.relay import Relay
from growbox.io import IOExpander

from growbox.sensory.env import EnvironmentSensor
from growbox.sensory.air import AirSensor
from growbox.sensory.uv import UVSensor


class ApplicationBuilder:
    """Create a useable application."""
    devices: dict = {
        IOExpander,
        Relay,
        EnvironmentSensor,
        AirSensor,
        UVSensor
    }
    _devinsts: dict = {}

    def build_generic_device(self, address, *args, cls=Wire, **kwargs):
        device = cls(*args, address=address, **kwargs)
        self._devinsts[cls.__name__] = device
        return device

    def build_app(self, devices=None):
        if devices is not None:
            assert isinstance(devices, dict)
            # facade.__name__: growbox.wire.Wire type

            self.devices = devices

        for facade_name, device in self.devices:
            # TODO: Work out integration
            pass


    def create_action(self, device, name, action, *args, **kwargs):
        # TODO: Refactor devices, and add alias to specific device action
        pass


class GrowBox:
    devices = [
    ]
