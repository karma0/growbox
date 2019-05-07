import time
import board
import busio
import adafruit_veml6075


class VEML6075:
    """AF CP VEML6075 wrapper"""
    address = 0x10

    def __init__(self, address=None, integration_time=100):
        self.i2c = busio.I2C(board.SCL, board.SDA)

        if address is not None:
            self.address = address

        self.veml = adafruit_veml6075.VEML6075(
            self.i2c,
            integration_time=integration_time,
            address=self.address,
        )

    @property
    def integration_time(self):
        """Integration time"""
        return self.veml.integration_time

    @integration_time.setter
    def integration_time(self, integration_time):
        """
        Set integration_time -- amount of time to collect data from the sensor
        before calculating values.
        """
        self.veml.integration_time = integration_time

    @property
    def uv_index(self):
        """UV Index"""
        return self.veml.uv_index

    @property
    def index(self):
        """UV Index"""
        return self.veml.uv_index

    @property
    def uva(self):
        """UVA"""
        return self.veml.uva

    @property
    def uvb(self):
        """UVB"""
        return self.veml.uvb


def main():
    """Main CLI function"""
    veml = VEML6075()
    print("Integration time: %d ms" % veml.integration_time)

    while True:
        print(veml.uv_index)
        time.sleep(1)


if __name__ == "__main__":
    main()
