# -*- coding: utf-8 -*-

"""Environmental Measurement using the BME280"""


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
    DIG_T1_LSB = 0x88
    DIG_T1_MSB = 0x89
    DIG_T2_LSB = 0x8A
    DIG_T2_MSB = 0x8B
    DIG_T3_LSB = 0x8C
    DIG_T3_MSB = 0x8D
    DIG_P1_LSB = 0x8E
    DIG_P1_MSB = 0x8F
    DIG_P2_LSB = 0x90
    DIG_P2_MSB = 0x91
    DIG_P3_LSB = 0x92
    DIG_P3_MSB = 0x93
    DIG_P4_LSB = 0x94
    DIG_P4_MSB = 0x95
    DIG_P5_LSB = 0x96
    DIG_P5_MSB = 0x97
    DIG_P6_LSB = 0x98
    DIG_P6_MSB = 0x99
    DIG_P7_LSB = 0x9A
    DIG_P7_MSB = 0x9B
    DIG_P8_LSB = 0x9C
    DIG_P8_MSB = 0x9D
    DIG_P9_LSB = 0x9E
    DIG_P9_MSB = 0x9F
    DIG_H2_LSB = 0xE1
    DIG_H2_MSB = 0xE2
    DIG_H3 =     0xE3
    DIG_H4_MSB = 0xE4
    DIG_H4_LSB = 0xE5
    DIG_H5_MSB = 0xE6
    DIG_H6 =     0xE7


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
    DIG_H1 =           0xA1
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
    mode = BME280Mode.NORMAL
    standby_time = BME280StandbyTime.MS__50
    temperature_oversample = BME280SampleAmount.COEFF_1
    humidity_oversample = BME280SampleAmount.COEFF_1
    pressure_oversample = BME280SampleAmount.COEFF_1

    calibration_data = defaultdict(int)  # type: dict

    def begin(self, *args, **kwargs):
        super().begin(*args, **kwargs)

        # Reading all compensation data into self.calibration_data
        for reg in BME280CompensationRegister:
            sreg = str(reg)
            if 'DIG_H4_MSB' in sreg or 'DIG_H5_MSB' in sreg:
                self.calibration_data[sreg] += self.read(reg) << 4
            elif 'DIG_H4_LSB' in sreg:
                self.calibration_data[sreg] += self.read(reg) & 0x0F
            elif 'DIG_H5_LSB' in sreg:
                self.calibration_data[sreg] += (self.read(reg) >> 4) & 0x0F
            elif 'MSB' in sreg:
                self.calibration_data[sreg] += self.read(reg) << 8
            else:
                self.calibration_data[sreg] += self.read(reg)

        self.set_oversample('temperature')
        self.set_oversample('humidity')
        self.set_oversample('pressure')

    def set_mode(self, mode):
        if mode > 0b11:
            mode = BME280Mode.SLEEP

        ctrldata = self.read(BME280Register.CTRL_MEAS)
        ctrldata &= ~( (1<<1) | (1<<0) )  # Create mask for bits 1-2
        ctrldata |= mode
        self.write(BME280Register.CTRL_MEAS, ctrldata)

    def get_mode(self):
        # Mask 2 bits
        return self.read(BME280Register.CTRL_MEAS) & 0b00000011

    def set_standby_time(self, standby_time):
        if standby_time > 0b111:
            standby_time = BME280StandbyTime.MS__50

        ctrldata = self.read(BME280Register.CONFIG)
        ctrldata &= ~( (1<<7) | (1<<6) | (1<<5) )  # Create mask for bits 5-7
        ctrldata |= (standby_time << 5)  # Move to bits 5-7
        self.write(BME280Register.CONFIG, ctrldata)

    def set_filter(self, filter_setting):
        if filter_setting > 0b111:
            filter_setting = BME280Filter.OFF

        ctrldata = self.read(BME280Register.CONFIG)
        ctrldata &= ~( (1<<4) | (1<<3) | (1<<2) )  # Create mask for bits 2-4
        ctrldata |= (filter_setting << 2)  # Move to bits 2-4
        self.write(BME280Register.CONFIG, ctrldata)

    def set_oversample(self, attr, amount=None):
        if amount is not None:
            setattr(self, f"{attr}_oversample", amount)

        orig_mode = self.get_mode()
        self.set_mode(BME280Mode.SLEEP)

        ctrldata = self.read(BME280Register.CTRL_MEAS)

        bit_a = int(getattr(OverSampleOffset, attr.capitalize()))
        bit_b = bit_a + 1
        bit_c = bit_b + 1

        ctrldata &= ~( (1<<bit_c) | (1<<bit_b) | (1<<bit_a) )  # Create mask for bits 2-4
        ctrldata |= (getattr(self, f"{attr}_oversample") << bit_a)  # Move to bits 2-4
        self.write(BME280Register.CTRL_MEAS, ctrldata)

        self.set_mode(orig_mode)

    def is_measuring(self):
        return self.read(BME280Register.STAT) & (1<<3)

    def reset(self):
        self.write(BME280Register.RST, 0xB6)

    def read_temp_c(self):
        pass

    def read_temp_f(self):
        pass

    def read_humidity(self):
        pass
