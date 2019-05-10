# -*- coding: utf-8 -*-

"""1-Wire interface"""

import board
from adafruit_onewire.bus import OneWireBus


class OneWire:
    def __init__(self, pin=board.D12):
        """
        Create the 1-Wire Bus using the pin you've connected to on your
        board.
        """
        self.bus = OneWireBus(pin)

    def crc8(self, *args, **kwargs):
        return self.bus.crc8(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.bus.write(*args, **kwargs)

    def readinto(self, *args, **kwargs):
        return self.bus.readinto(*args, **kwargs)

    def reset(self):
        """
        Reset and check for presence pulse. This is basically -
        "is there anything out there?"
        """
        if not self.bus.reset():
            raise RuntimeError("Nothing found on bus.")

    @property
    def devices(self):
        """Run a scan to get all of the device ROM values"""
        return self.bus.scan()

    def show_devices(self):
        """For each device found, print out some info"""
        for idx, dev in enumerate(self.devices):
            print("Device {:>3}".format(idx))
            print("\tSerial Number = ", end='')
            for byte in dev.serial_number:
                print("0x{:02x} ".format(byte), end='')
            print("\n\tFamily = 0x{:02x}".format(dev.family_code))


class DS18B20(OneWire):
    valid_addrs = [0x10, 0x28]

    @property
    def temperature(self):
        dev = self.devices.pop()
        if not dev:
            self.reset()
            return None

        if self.crc8(dev, 7) != dev[7]:
            raise ValueError("Invalid CRC")

        if dev[0] not in self.valid_addrs:
            raise AttributeError("Device is not recognized")

        # Start conversion with parasite power on at the end
        self.reset()
        self.write(0x44, 1)

        # Read scratchpad
        self.reset()
        self.write(0xBE)

        data = []
        self.readinto(data, end=10)

        self.reset()

        lsb, msb = data[0], data[1]
        temp_sum = ((msb << 8) | lsb) / 16
        return (temp_sum * 18 + 5) / 10 + 32
