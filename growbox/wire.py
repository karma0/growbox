# -*- coding: utf-8 -*-

"""Wire base module"""


from smbus2 import SMBus

from growbox.enum import Enum


class Wire:
    """
    A base class and interfaces to suit the relevant commands. Set the address
    attribute of your subclass and your jump_address to the appropriate
    alternate address if your device supports it.
    """

    address = 0  # type: int
    jump_address = 0  # type: int

    def __init__(self, address=None, channel=1, addr_jmp=False, **kwargs):
        # Set address of i2c to appropriate address, or override completely
        if address is not None:
            if address == 0:
                if self.jump_address != 0:
                    self.address = self.jump_address if addr_jmp else self.address
            else:
                self.address = address

        if self.address == 0:
            raise ValueError(f"No device I2C address specified.")

        self.bus = SMBus(channel)

    def begin(self, *args, **kwargs):
        """
        Override this function if your device has some I2C/SPI setup.
        """
        pass

    def word2bytes(self, data):
        msb = (data & 0xFF00) >> 8
        lsb = data & 0x00FF
        return [msb, lsb]

    def bytes2word(self, data):
        assert len(data) == 2
        msb, lsb = data
        return ((msb & 0x00FF) << 8) | (lsb & 0x00FF)

    def write(self, offset=0, data=None, retry=3):
        """
        Writes a set of bytes to the provided offset.  If no offset is
        provided, no register is assumed.
        """
        if data is None:
            data = offset
            offset = 0

        if isinstance(offset, Enum):
            offset = offset.value

        if isinstance(data, Enum):
            data = data.value

        if retry == 0:
            return None

        try:
            if isinstance(data, list):
                # Writes bytes
                return self.bus.write_i2c_block_data(self.address, offset, data)
            else:
                # Writes byte
                return self.bus.write_byte_data(self.address, offset, data)
        except OSError:
            return self.write(offset, data, retry - 1)

    def write_word(self, offset=0, data=None):
        """
        Writes a set of words to the provided offset.  If no offset is
        provided, no register is assumed.
        """
        if data is None:
            data = offset
            offset = 0

        if isinstance(data, list):
            idx = 0
            for word in data:
                word_offset = idx * 2 + offset
                self.write(offset=word_offset, data=self.word2bytes(word))
                idx += 1
        else:
            self.write(offset=offset, data=self.word2bytes(data))

    def read(self, offset=0, size=None, retry=3):
        """
        Reads a set of bytes from the provided offset.  If no offset is
        provided, no register is assumed. Specify size to read more than a
        single byte.
        """
        if isinstance(offset, Enum):
            offset = offset.value

        try:
            if size is None:
                return self.bus.read_byte_data(self.address, offset)
            else:
                return self.bus.read_i2c_block_data(self.address, offset, size)
        except OSError:
            return self.read(offset, size, retry - 1)

    def read_word(self, offset=0, size=None):
        """
        Reads a set of words from the provided offset.  If no offset is
        provided, no register is assumed. Specify size to read more than a
        single word.
        """
        if size is not None:
            size *= 2  # we're counting bytes as words
        else:
            size = 2

        return self.bytes2word(self.read(offset=offset, size=size))
