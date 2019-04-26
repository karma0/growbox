# -*- coding: utf-8 -*-

"""Environmental Measurement using the BME280"""


from math import log10, log
from enum import Enum
from collections import defaultdict

from growbox.wire import Wire


class BME280Mode(Enum):
    SLEEP  = 0b00
    FORCED = 0b01
    NORMAL = 0b11


class BME280SampleAmount(Enum):
    OFF      = 0
    COEFF_1  = 1
    COEFF_2  = 2
    COEFF_4  = 3
    COEFF_8  = 4
    COEFF_16 = 5


class BME280Filter(Enum):
    OFF      = 0
    COEFF_2  = 1
    COEFF_4  = 2
    COEFF_8  = 3
    COEFF_16 = 4


class BME280StandbyTime(Enum):
    MS__50  = 0
    MS_62_5 = 1
    MS_125  = 2
    MS_250  = 3
    MS_500  = 4
    MS_1000 = 5
    MS_10   = 6
    MS_20   = 7


class BME280CompensationRegister(Enum):
    T1_LSB = 0x88
    T1_MSB = 0x89
    T2_LSB = 0x8A
    T2_MSB = 0x8B
    T3_LSB = 0x8C
    T3_MSB = 0x8D
    P1_LSB = 0x8E
    P1_MSB = 0x8F
    P2_LSB = 0x90
    P2_MSB = 0x91
    P3_LSB = 0x92
    P3_MSB = 0x93
    P4_LSB = 0x94
    P4_MSB = 0x95
    P5_LSB = 0x96
    P5_MSB = 0x97
    P6_LSB = 0x98
    P6_MSB = 0x99
    P7_LSB = 0x9A
    P7_MSB = 0x9B
    P8_LSB = 0x9C
    P8_MSB = 0x9D
    P9_LSB = 0x9E
    P9_MSB = 0x9F
    H1 =     0xA1
    H2_LSB = 0xE1
    H2_MSB = 0xE2
    H3 =     0xE3
    H4_MSB = 0xE4
    H4_LSB = 0xE5
    H5_MSB = 0xE6
    H6 =     0xE7


class BME280Register(Enum):
    CTRL_HUMIDITY =    0xF2  # Ctrl Humidity Reg
    STAT =             0xF3  # Status Reg
    CTRL_MEAS =        0xF4  # Ctrl Measure Reg
    CONFIG =           0xF5  # Configuration Reg
    PRESSURE_MSB =     0xF7  # Pressure MSB
    PRESSURE_LSB =     0xF8  # Pressure LSB
    PRESSURE_XLSB =    0xF9  # Pressure XLSB
    TEMPERATURE_MSB =  0xFA  # Temperature MSB
    TEMPERATURE_LSB =  0xFB  # Temperature LSB
    TEMPERATURE_XLSB = 0xFC  # Temperature XLSB
    HUMIDITY_MSB =     0xFD  # Humidity MSB
    HUMIDITY_LSB =     0xFE  # Humidity LSB
    CHIP_ID =          0xD0  # Chip ID
    RST =              0xE0  # Softreset Reg


class OverSampleOffset(Enum):
    HUMIDITY    = 0
    PRESSURE    = 2
    TEMPERATURE = 5


class BME280Sensor(Wire):
    """
    SparkFun's QWIIC BME280 environmental sensor and corresponding interface.
    """
    address = 0x77
    jump_address = 0x76

    # Settings and their defaults
    _mode = BME280Mode.NORMAL
    _standby_time = BME280StandbyTime.MS__50
    _filter = BME280Filter.COEFF_2

    _temperature_oversample = BME280SampleAmount.COEFF_1
    _humidity_oversample = BME280SampleAmount.COEFF_1
    _pressure_oversample = BME280SampleAmount.COEFF_1

    temperature_correction = 12.25
    """temperature adjustment to account for operating temperature changes."""

    reference_pressure = 101325.0

    calibration_data = defaultdict(int)  # type: dict

    def begin(self, *args, **kwargs):
        super().begin(*args, **kwargs)

        # Reading all compensation data into self.calibration_data
        for reg in BME280CompensationRegister:
            sreg = str(reg)
            k_sreg = sreg[:-4]

            if sreg == 'H1' or sreg == 'H3' or sreg == 'H6':
                k_sreg = sreg

            if 'H4_MSB' in sreg or 'H5_MSB' in sreg:
                self.calibration_data[k_sreg] += self.read(reg.value) << 4
            elif 'H4_LSB' in sreg:
                self.calibration_data[k_sreg] += self.read(reg.value) & 0x0F
            elif 'H5_LSB' in sreg:
                self.calibration_data[k_sreg] += (self.read(reg.value) >> 4) & 0x0F
            elif 'MSB' in sreg:
                self.calibration_data[k_sreg] += self.read(reg.value) << 8
            else:
                self.calibration_data[k_sreg] += self.read(reg.value)

        # Init settings to their defaults
        self.mode = self._mode
        self.standby_time = self._standby_time
        self.filter = self._filter

        self.set_oversample('temperature')
        self.set_oversample('humidity')
        self.set_oversample('pressure')

    # Getters and setters

    @property
    def mode(self):
        # Mask 2 bits
        self._mode = BME280Mode(
            self.read(BME280Register.CTRL_MEAS.value) & 0b00000011)
        return self._mode

    @mode.setter
    def mode(self, mode):
        if mode.value > 0b11:
            mode = BME280Mode.SLEEP
        self._mode = mode

        ctrldata = self.read(BME280Register.CTRL_MEAS.value)
        ctrldata &= ~( (1<<1) | (1<<0) )  # Create mask for bits 1-2
        ctrldata |= mode.value
        self.write(BME280Register.CTRL_MEAS.value, ctrldata)

    @property
    def standby_time(self):
        return self._standby_time

    @standby_time.setter
    def standby_time(self, standby_time):
        if standby_time.value > 0b111:
            standby_time = BME280StandbyTime.MS__50
        self._standby_time = standby_time

        ctrldata = self.read(BME280Register.CONFIG.value)
        ctrldata &= ~( (1<<7) | (1<<6) | (1<<5) )  # Create mask for bits 5-7
        ctrldata |= (standby_time << 5)  # Move to bits 5-7
        self.write(BME280Register.CONFIG.value, ctrldata)

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, filter_setting):
        if filter_setting > 0b111:
            filter_setting = BME280Filter.OFF
        self._filter = filter_setting

        ctrldata = self.read(BME280Register.CONFIG.value)
        ctrldata &= ~( (1<<4) | (1<<3) | (1<<2) )  # Create mask for bits 2-4
        ctrldata |= (filter_setting << 2)  # Move to bits 2-4
        self.write(BME280Register.CONFIG.value, ctrldata)

    def set_oversample(self, attr, amount=None):
        if amount is not None:
            setattr(self, f"{attr}_oversample", amount)

        orig_mode = self.mode
        self.mode = BME280Mode.SLEEP

        ctrldata = self.read(BME280Register.CTRL_MEAS.value)

        bit_a = int(getattr(OverSampleOffset, attr.capitalize()).value)
        bit_b = bit_a + 1
        bit_c = bit_b + 1

        ctrldata &= ~( (1<<bit_c) | (1<<bit_b) | (1<<bit_a) )  # Create mask for bits 2-4
        ctrldata |= (getattr(self, f"{attr}_oversample") << bit_a)  # Move to bits 2-4
        self.write(BME280Register.CTRL_MEAS.value, ctrldata)

        self.mode = orig_mode

    def is_measuring(self):
        return self.read(BME280Register.STAT.value) & (1<<3)

    def reset(self):
        self.write(BME280Register.RST.value, 0xB6)

    # Pressure

    @property
    def pressure(self):
        buffer = self.read(BME280Register.PRESSURE_MSB.value, 3)
        adc_p = (int(buffer[0]) << 12) | \
                (int(buffer[1]) << 4) | \
                ((int(buffer[2]) >> 4) & 0x0F)

        var1 = self.t_fine - 128000
        var2 = var1 * var1 * self.calibration_data['P6']
        var2 = var2 + ((var1 * self.calibration_data['P5']) << 17)
        var2 = var2 + (self.calibration_data['P4'] << 35)
        var1 = (var1 * var1 * self.calibration_data['P3'] >> 8) + \
            ((var1 * self.calibration_data['P2']) << 12)
        var1 = ((1 << 47) + var1) * self.calibration_data['P1'] >> 33

        p_acc = 1048576 - adc_p
        try:
            p_acc = (((p_acc << 31) - var2) * 3125) / var1
        except ZeroDivisionError:  # var1 == 0
            return 0

        var1 = (self.calibration_data['P9'] * ((p_acc >> 13) ** 2)) >> 25
        var2 = (self.calibration_data['P8'] * p_acc) >> 19
        p_acc = ((p_acc + var1 + var2) >> 8) + \
                (self.calibration_data['P7'] << 4)

        return p_acc / 256.0

    @property
    def altitude_meters(self):
        return -44330.77 * (
            (self.pressure / self.reference_pressure) ** 0.190263
        ) - 1.0

    @property
    def altitude_feet(self):
        return  self.altitude_meters * 3.28084

    # Humidity

    @property
    def humidity(self):
        buffer = self.read(BME280Register.HUMIDITY_MSB.value, 2)
        adc_h = (buffer[0] << 8) | buffer[1]

        var1 = self.t_fine - 76800
        var1 = (
            (
                (
                    (adc_h << 14)
                    - (self.calibration_data['H4'] << 20)
                    - (self.calibration_data['H5'] * var1)
                ) + 16384
            ) >> 15
        ) * (
            (
                (
                    (
                        (
                            (
                                (
                                    var1 * self.calibration_data['H6']
                                ) >> 10
                            ) * (
                                (
                                    (
                                        var1 * self.calibration_data['H3']
                                    ) >> 11
                                ) + 32768
                            )
                        ) >> 10
                    ) + 2097152
                ) * self.calibration_data['H2'] + 8192
            ) >> 14
        )
        var1 = var1 - (
            (
                (
                    (
                        (var1 >> 15) ** 2
                    ) >> 7
                ) * self.calibration_data['H1']
            ) >> 4
        )

        if var1 < 0:
            var1 = 0
        elif var1 > 419430400:
            var1 = 419430400

        return (var1 >> 12) / 1024.0

    # Temperature

    @property
    def celsius(self):
        buffer = self.read(BME280Register.TEMPERATURE_MSB.value, 3)
        adc_t = (int(buffer[0]) << 12) | \
                (int(buffer[1]) << 4) | \
                ((int(buffer[2]) >> 4) & 0x0F)

        var1 = (
            (
                (adc_t >> 3)
                - (self.calibration_data['T1'] << 1)
            ) * self.calibration_data['T2']
        ) >> 11

        var2 = (
            (
                (
                    (
                        (adc_t >> 4)
                        - self.calibration_data['T1']
                    ) * (
                        (adc_t >> 4)
                        - self.calibration_data['T1']
                    )
                ) >> 12
            ) * self.calibration_data['T3']
        ) >> 14

        self.t_fine = var1 + var2
        output = (self.t_fine * 5 + 128) >> 8
        output /= 100
        output += self.temperature_correction
        return output

    @property
    def fahrenheit(self):
        return self.c2f(self.celsius)

    @property
    def dew_point_c(self):
        ratio = 373.15 / (273.15 + self.celsius)
        rhs = -7.90298 * (ratio - 1)
        rhs += 5.02808 * log10(ratio)
        rhs += -1.3816e-7 * (pow(10, (11.344 * (1 - 1/ratio))) - 1)
        rhs += 8.1328e-3 * (pow(10, (-3.49149 * (ratio - 1))) - 1)
        rhs += log10(1013.246)

        vp = pow(10, rhs - 3) * self.humidity
        temp = log(vp / 0.61078)
        return (241.88 * temp) / (17.558 - temp)

    @property
    def dew_point_f(self):
        return self.c2f(self.dew_point_c)

    def c2f(self, celsius):
        return (celsius * (9 / 5)) + 32

    def f2c(self, fahrenheit):
        return (fahrenheit - 32) * (5 / 9)
