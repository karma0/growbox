# -*- coding: utf-8 -*-

"""Wire base module"""


from smbus2 import SMBus


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

    def write(self, offset=0, data=None):
        """
        Writes a set of values to the provided offset.  If no offset is
        provided, no register is assumed.
        """
        if data is None:
            data = offset
            offset = 0

        if isinstance(data, list):
            # Writes bytes
            return self.bus.write_i2c_block_data(self.address, offset, data)
        else:
            # Writes byte
            return self.bus.write_byte_data(self.address, offset, data)

    def read(self, offset=0, size=None):
        """
        Reads a set of values from the provided offset.  If no offset is
        provided, no register is assumed. Specify size to read more than a
        single byte.
        """
        if size is None:
            return self.bus.read_byte_data(self.address, offset)
        else:
            return self.bus.read_i2c_block_data(self.address, offset, size)
