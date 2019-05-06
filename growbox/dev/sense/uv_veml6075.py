# -*- coding: utf-8 -*-

"""UV sensor implementations for the VEML6075 chip."""


import time

from growbox.common.enum import Enum
from growbox.common.wire import Wire


class VEML6075Resolution(Enum):
    NORMAL = 0
    HIGH = 1
    INVALID = 2


class UVIntegrationTime(Enum):
    IT_50MS  = 0
    IT_100MS = 1
    IT_200MS = 2
    IT_400MS = 3
    IT_800MS = 4


class VEML6075Trigger(Enum):
    NO_TRIGGER = 0
    TRIGGER_ONE_OR_UV_TRIG = 1
    TRIGGER_INVALID = 2


class VEML6075AutoForce(Enum):
    DISABLE = 0
    ENABLE = 1
    INVALID = 2


class VEML6075Error(Enum):
    READ = -4
    WRITE = -3
    INVALID_ADDRESS = -2
    UNDEFINED = -1
    SUCCESS = 1


class VEML6075Power(Enum):
    POWER_ON = 0
    SHUTDOWN = 1
    INVALID  = 2


class VEML6075Registers(Enum):
    UV_CONF = 0x00
    UVA_DATA = 0x07
    UVB_DATA = 0x09
    UVCOMP1_DATA = 0x0A
    UVCOMP2_DATA = 0x0B
    ID = 0x0C


class ConfMask(Enum):
    SHUTDOWN = 0x01
    AF       = 0x02
    TRIG     = 0x04
    HD       = 0x08
    UV_IT    = 0x70


class ConfShift(Enum):
    SHUTDOWN = 0
    AF       = 1
    TRIG     = 2
    HD       = 3
    UV_IT    = 4


class UVSensor(Wire):
    """
    SparkFun's QWIIC VEML6075 UV sensor and corresponding interface.
    """
    address = 0x10

    status = VEML6075Error.UNDEFINED

    # Primary configuration
    integration_time = UVIntegrationTime.IT_800MS
    resolution = VEML6075Resolution.HIGH
    autoforce = VEML6075AutoForce.DISABLE

    raw_dark = 0
    raw_ir = 0
    raw_viz = 0

    hd_scalar = 2.0

    uv_alpha = 1.0
    uv_beta  = 1.0
    uv_gamma = 1.0
    uv_delta = 1.0

    uva_a_coef = 2.22
    uva_b_coef = 1.33
    uva_c_coef = 2.95
    uva_d_coef = 1.75

    uva_responsivity_100ms_uncovered = 0.001111
    uvb_responsivity_100ms_uncovered = 0.00125

    uv_it_ms = [
        50,
        100,
        200,
        400,
        800,
    ]

    uva_responsivity = [
        uva_responsivity_100ms_uncovered / 0.5016286645,  # 50ms
        uva_responsivity_100ms_uncovered,                 # 100ms
        uva_responsivity_100ms_uncovered / 2.039087948,   # 200ms
        uva_responsivity_100ms_uncovered / 3.781758958,   # 400ms
        uva_responsivity_100ms_uncovered / 7.371335505    # 800ms
    ]

    uvb_responsivity = [
        uvb_responsivity_100ms_uncovered / 0.5016286645,  # 50ms
        uvb_responsivity_100ms_uncovered,                 # 100ms
        uvb_responsivity_100ms_uncovered / 2.039087948,   # 200ms
        uvb_responsivity_100ms_uncovered / 3.781758958,   # 400ms
        uvb_responsivity_100ms_uncovered / 7.371335505    # 800ms
    ]

    _a_responsivity = uva_responsivity_100ms_uncovered
    _b_responsivity = uvb_responsivity_100ms_uncovered

    _last_read_time = 0
    _last_index = 0.0
    _hd_enabled = False

    def begin(self):
        self.status = VEML6075Error.SUCCESS
        return self.status

    def _getsection(self, section):
        mask = getattr(ConfMask, section).value
        shift = getattr(ConfShift, section).value
        return (mask, shift)

    def _getter(self, section, etype):
        mask, shift = self._getsection(section)
        data = self.read(VEML6075Registers.UV_CONF)
        return etype((data & mask) >> shift)

    def _setter(self, section, data):
        mask, shift = self._getsection(section)
        config = self.read(VEML6075Registers.UV_CONF)
        config &= ~(mask)
        config |= data << shift
        self.write(VEML6075Registers.UV_CONF, config)

    @property
    def integration_time(self):
        return self._getter('UV_IT', UVIntegrationTime)

    @integration_time.setter
    def integration_time(self, integration_time):
        self._setter('UV_IT', integration_time)
        self._a_responsivity = self.uva_responsivity[integration_time.value]
        self._b_responsivity = self.uvb_responsivity[integration_time.value]

    @property
    def resolution(self):  # "HighDynamic"
        return self._getter('HD', VEML6075Resolution)

    @resolution.setter
    def resolution(self, resolution):  # "HighDynamic"
        self._setter('HD', resolution)
        self._hd_enabled = resolution is VEML6075Resolution.HIGH

    @property
    def trigger(self):
        return self._getter('TRIG', VEML6075Trigger)

    @trigger.setter
    def trigger(self, trigger):
        self._setter('TRIG', trigger)

    @property
    def autoforce(self):
        return self._getter('AF', VEML6075AutoForce)

    @autoforce.setter
    def autoforce(self, autoforce):
        self._setter('AF', autoforce)

    def shutdown(self, shutdown=True):
        self._setter('SHUTDOWN', VEML6075Power(int(shutdown)))

    @property
    def uva(self):
        return (
            self.raw_uva
            - ((self.uva_a_coef * self.uv_alpha * self.uv_comp1) / self.uv_gamma)
            - ((self.uva_b_coef * self.uv_alpha * self.uv_comp2) / self.uv_delta)
        )

    @property
    def uvb(self):
        return (
            self.raw_uvb
            - ((self.uva_c_coef * self.uv_beta * self.uv_comp1) / self.uv_gamma)
            - ((self.uva_d_coef * self.uv_beta * self.uv_comp2) / self.uv_delta)
        )

    @property
    def raw_uva(self):
        data = self.read(VEML6075Registers.UVA_DATA, 2)
        self._last_read_time = time.time()
        return (data[0] & 0x00FF) | ((data[1] & 0x00FF) << 8)

    @property
    def raw_uvb(self):
        data = self.read(VEML6075Registers.UVB_DATA, 2)
        self._last_read_time = time.time()
        return (data[0] & 0x00FF) | ((data[1] & 0x00FF) << 8)

    @property
    def index(self):
        uvia = self.uva * (1.0 / self.uv_alpha) * self._a_responsivity
        uvib = self.uvb * (1.0 / self.uv_beta) * self._b_responsivity
        self._last_index = (uvia + uvib) / 2.0

        if self._hd_enabled:
            self._last_index *= self.hd_scalar

        self._last_read_time = time.time()
        return self._last_index

    @property
    def uv_comp1(self):
        data = self.read(VEML6075Registers.UVCOMP1_DATA, 2)
        return (data[0] & 0x00FF) | ((data[1] & 0x00FF) << 8)

    @property
    def uv_comp2(self):
        data = self.read(VEML6075Registers.UVCOMP2_DATA, 2)
        return (data[0] & 0x00FF) | ((data[1] & 0x00FF) << 8)

    @property
    def visible_compensation(self):
        return self.uv_comp1

    @property
    def ir_compensation(self):
        return self.uv_comp2
