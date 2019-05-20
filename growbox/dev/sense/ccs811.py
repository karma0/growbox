import time
import board
import busio
import adafruit_ccs811

class CCS811:
    """AF CP CCS811 wrapper"""
    #address = 0x5A
    address = 0x5B

    def __init__(self, address=None):
        self.i2c = busio.I2C(board.SCL, board.SDA)

        if address is not None:
            self.address = address

        self.ccs811 = adafruit_ccs811.CCS811(self.i2c, address=self.address)

        # Wait for the sensor to be ready and calibrate the thermistor
        while not self.ready:
            pass

        # Set temp offset to a sane default
        self.set_temperature_offset(25)

    def set_temperature_offset(self, temp):
        """
        The chip will generate some heat, so we remove it from final
        calculations.
        """
        self.ccs811.temp_offset = self.temperature - temp

    @property
    def ready(self):
        return self.ccs811.data_ready

    @property
    def eco2(self):
        """Another name for CO2"""
        return self.ccs811.eco2

    @property
    def co2(self):
        """CO2 parts-per-million"""
        return self.ccs811.eco2

    @property
    def tvoc(self):
        """T-VOC"""
        return self.ccs811.tvoc

    @property
    def temperature(self):
        """Temperature in Celsius"""
        return self.ccs811.temperature


def main():
    """Main CLI function"""
    ccs811 = CCS811()
    while True:
        print("CO2: {} PPM, TVOC: {} PPM, Temp: {} C"
              .format(ccs811.eco2, ccs811.tvoc, ccs811.temperature))
        time.sleep(0.5)


if __name__ == "__main__":
    main()
