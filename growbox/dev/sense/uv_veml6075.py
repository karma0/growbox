# -*- coding: utf-8 -*-

"""UV sensor implementations for the VEML6075 chip."""


from growbox.wire import Wire

from enum import Enum


class Resolution(Enum):
    NORMAL = 0
    HIGH = 1
    INVALID = 2


class UVIntegration(Enum):
    IT_50MS = 50
    IT_100MS = 100
    IT_200MS = 200
    IT_400MS = 400
    IT_800MS = 800


class VEML6075Error(Enum):
    ERROR_READ = -4
    ERROR_WRITE = -3
    ERROR_INVALID_ADDRESS = -2
    ERROR_UNDEFINED = -1
    ERROR_SUCCESS = 1


class Registers(Enum):
    UV_CONF = 0x00
    UVA_DATA = 0x07
    UVB_DATA = 0x09
    UVCOMP1_DATA = 0x0A
    UVCOMP2_DATA = 0x0B
    ID = 0x0C


class UVSensor(Wire):
    """
    SparkFun's QWIIC VEML6075 UV sensor and corresponding interface.
    """
    address = 0x10

    status = VEML6075Error.ERROR_UNDEFINED

    uv_integration = UVIntegration.IT_100MS

    raw_uva = 0
    raw_uvb = 0
    raw_dark = 0
    raw_ir = 0
    raw_viz = 0

    config

    def __init__(self, *args, samplerate=None, **kwargs):
        if samplerate is not None:
            if not isinstance(samplerate, UVIntegration):
                raise ValueError("Invalid UVIntegration as a samplerate: "
                                 f"{samplerate}")
            self.uv_integration = samplerate
            self.set_integration_time()

        super().__init__(*args, **kwargs)
        self.config |= 

    def set_integration_time(self, samplerate=None):
        if samplerate is not None:
            self.uv_integration = samplerate

        self.read(Registers.UV_CONF)

