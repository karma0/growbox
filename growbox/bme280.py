import board
import digitalio
import busio
import time
import adafruit_bme280

class BME280:
    address = 0x77
    #address = 0x76

    def __init__(self, address=None):
        # Create library object using our Bus I2C port
        self.i2c = busio.I2C(board.SCL, board.SDA)

        if address is not None:
            self.address = address

        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(
            self.i2c,
            address=self.address,
        )

        # OR create library object using our Bus SPI port
        #self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        #self.bme_cs = digitalio.DigitalInOut(board.D10)
        #self.bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

        self.sea_level_pressure = 1013.25

    @property
    def sea_level_pressure(self):
        return self.bme280.sea_level_pressure

    @sea_level_pressure.setter
    def sea_level_pressure(self, sea_level_pressure):
        """
        Change this to match the location's pressure (hPa) at sea level.
        """
        self.bme280.sea_level_pressure = sea_level_pressure

    @property
    def temperature(self):
        """Temperature in Celsius"""
        return self.bme280.temperature

    @property
    def celsius(self):
        """Temperature in Celsius"""
        return self.bme280.temperature

    @property
    def fahrenheit(self):
        """Temperature in Fahrenheit"""
        return (self.bme280.temperature * 9/5) + 32

    @property
    def humidity(self):
        """Humidity (in %)"""
        return self.bme280.humidity

    @property
    def pressure(self):
        """Air pressure"""
        return self.bme280.pressure

    @property
    def altitude(self):
        """Altitude (in meters)"""
        return self.bme280.altitude


def main():
    """Main CLI execution"""
    bme280 = BME280()

    while True:
        print("\nTemperature: %0.1f C" % bme280.temperature)
        print("Humidity: %0.1f %%" % bme280.humidity)
        print("Pressure: %0.1f hPa" % bme280.pressure)
        print("Altitude = %0.2f meters" % bme280.altitude)
        time.sleep(2)


if __name__ == "__main__":
    main()
