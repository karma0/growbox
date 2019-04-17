# -*- coding: utf-8 -*-

"""Wire base module"""


from smbus2 import SMBus


class Wire:
    """A base class and interfaces to suit the relative commands."""
    def __init__(self, address=None, channel=1, **kwargs):
        self.address = self.address if address is None else address
        self.bus = SMBus(channel)

    def write_block(self, offset, data):
        self.bus.write_i2c_block_data(self.address, offset, data)

    def write(self, offset, data):
        self.bus.write_byte_data(self.address, offset, data)

    def read_block(self, offset, size):
        return self.bus.read_i2c_block_data(self.address, offset, size)

    def read(self, offset):
        return self.bus.read_byte_data(self.address, offset)

    def request_response(self, request, response_size):
        self.write(0, request)
        return self.read_block(0, response_size)
