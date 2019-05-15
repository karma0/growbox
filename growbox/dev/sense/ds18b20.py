# -*- coding: utf-8 -*-


"""DS18B20 Linux one wire interface"""

import glob
import time


class DS18B20:
    base_dir = '/sys/bus/w1/devices/'
    device_file = glob.glob(base_dir + '28*')[0] + '/w1_slave'

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f

    @property
    def celsius(self):
        return self.read_temp()[0]

    @property
    def fahrenheit(self):
        return self.read_temp()[1]

    @property
    def temperature(self):
        return self.celsius


def main():
    ds18b20 = DS18B20()
    while True:
        print(ds18b20.fahrenheit)
        time.sleep(1)


if __name__ == "__main__":
    main()
