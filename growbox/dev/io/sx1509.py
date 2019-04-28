# -*- coding: utf-8 -*-

"""SX1509 I2C I/O Breakout Board"""


import time

from growbox.enum import Enum
from growbox.wire import Wire


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


class SX1509Register(Enum):
    INPUT_DISABLE_B     = 0x00    #    RegInputDisableB Input buffer disable register _ I/O[15_8] (Bank B) 0000 0000
    INPUT_DISABLE_A     = 0x01    #    RegInputDisableA Input buffer disable register _ I/O[7_0] (Bank A) 0000 0000
    LONG_SLEW_B         = 0x02    #    RegLongSlewB Output buffer long slew register _ I/O[15_8] (Bank B) 0000 0000
    LONG_SLEW_A         = 0x03    #    RegLongSlewA Output buffer long slew register _ I/O[7_0] (Bank A) 0000 0000
    LOW_DRIVE_B         = 0x04    #    RegLowDriveB Output buffer low drive register _ I/O[15_8] (Bank B) 0000 0000
    LOW_DRIVE_A         = 0x05    #    RegLowDriveA Output buffer low drive register _ I/O[7_0] (Bank A) 0000 0000
    PULL_UP_B           = 0x06    #    RegPullUpB Pull_up register _ I/O[15_8] (Bank B) 0000 0000
    PULL_UP_A           = 0x07    #    RegPullUpA Pull_up register _ I/O[7_0] (Bank A) 0000 0000
    PULL_DOWN_B         = 0x08    #    RegPullDownB Pull_down register _ I/O[15_8] (Bank B) 0000 0000
    PULL_DOWN_A         = 0x09    #    RegPullDownA Pull_down register _ I/O[7_0] (Bank A) 0000 0000
    OPEN_DRAIN_B        = 0x0A    #    RegOpenDrainB Open drain register _ I/O[15_8] (Bank B) 0000 0000
    OPEN_DRAIN_A        = 0x0B    #    RegOpenDrainA Open drain register _ I/O[7_0] (Bank A) 0000 0000
    POLARITY_B          = 0x0C    #    RegPolarityB Polarity register _ I/O[15_8] (Bank B) 0000 0000
    POLARITY_A          = 0x0D    #    RegPolarityA Polarity register _ I/O[7_0] (Bank A) 0000 0000
    DIR_B               = 0x0E    #    RegDirB Direction register _ I/O[15_8] (Bank B) 1111 1111
    DIR_A               = 0x0F    #    RegDirA Direction register _ I/O[7_0] (Bank A) 1111 1111
    DATA_B              = 0x10    #    RegDataB Data register _ I/O[15_8] (Bank B) 1111 1111*
    DATA_A              = 0x11    #    RegDataA Data register _ I/O[7_0] (Bank A) 1111 1111*
    INTERRUPT_MASK_B    = 0x12    #    RegInterruptMaskB Interrupt mask register _ I/O[15_8] (Bank B) 1111 1111
    INTERRUPT_MASK_A    = 0x13    #    RegInterruptMaskA Interrupt mask register _ I/O[7_0] (Bank A) 1111 1111
    SENSE_HIGH_B        = 0x14    #    RegSenseHighB Sense register for I/O[15:12] 0000 0000
    SENSE_LOW_B         = 0x15    #    RegSenseLowB Sense register for I/O[11:8] 0000 0000
    SENSE_HIGH_A        = 0x16    #    RegSenseHighA Sense register for I/O[7:4] 0000 0000
    SENSE_LOW_A         = 0x17    #    RegSenseLowA Sense register for I/O[3:0] 0000 0000
    INTERRUPT_SOURCE_B  = 0x18    #    RegInterruptSourceB Interrupt source register _ I/O[15_8] (Bank B) 0000 0000
    INTERRUPT_SOURCE_A  = 0x19    #    RegInterruptSourceA Interrupt source register _ I/O[7_0] (Bank A) 0000 0000
    EVENT_STATUS_B      = 0x1A    #    RegEventStatusB Event status register _ I/O[15_8] (Bank B) 0000 0000
    EVENT_STATUS_A      = 0x1B    #    RegEventStatusA Event status register _ I/O[7_0] (Bank A) 0000 0000
    LEVEL_SHIFTER_1     = 0x1C    #    RegLevelShifter1 Level shifter register 0000 0000
    LEVEL_SHIFTER_2     = 0x1D    #    RegLevelShifter2 Level shifter register 0000 0000
    CLOCK               = 0x1E    #    RegClock Clock management register 0000 0000
    MISC                = 0x1F    #    RegMisc Miscellaneous device settings register 0000 0000
    LED_DRIVER_ENABLE_B = 0x20    #    RegLEDDriverEnableB LED driver enable register _ I/O[15_8] (Bank B) 0000 0000
    LED_DRIVER_ENABLE_A = 0x21    #    RegLEDDriverEnableA LED driver enable register _ I/O[7_0] (Bank A) 0000 0000
# Debounce and Keypad Engine
    DEBOUNCE_CONFIG     = 0x22    #    RegDebounceConfig Debounce configuration register 0000 0000
    DEBOUNCE_ENABLE_B   = 0x23    #    RegDebounceEnableB Debounce enable register _ I/O[15_8] (Bank B) 0000 0000
    DEBOUNCE_ENABLE_A   = 0x24    #    RegDebounceEnableA Debounce enable register _ I/O[7_0] (Bank A) 0000 0000
    KEY_CONFIG_1        = 0x25    #    RegKeyConfig1 Key scan configuration register 0000 0000
    KEY_CONFIG_2        = 0x26    #    RegKeyConfig2 Key scan configuration register 0000 0000
    KEY_DATA_1          = 0x27    #    RegKeyData1 Key value (column) 1111 1111
    KEY_DATA_2          = 0x28    #    RegKeyData2 Key value (row) 1111 1111
# LED Driver (PWM, blinking, breathing)
    T_ON_0              = 0x29    #    RegTOn0 ON time register for I/O[0] 0000 0000
    I_ON_0              = 0x2A    #    RegIOn0 ON intensity register for I/O[0] 1111 1111
    OFF_0               = 0x2B    #    RegOff0 OFF time/intensity register for I/O[0] 0000 0000
    T_ON_1              = 0x2C    #    RegTOn1 ON time register for I/O[1] 0000 0000
    I_ON_1              = 0x2D    #    RegIOn1 ON intensity register for I/O[1] 1111 1111
    OFF_1               = 0x2E    #    RegOff1 OFF time/intensity register for I/O[1] 0000 0000
    T_ON_2              = 0x2F    #    RegTOn2 ON time register for I/O[2] 0000 0000
    I_ON_2              = 0x30    #    RegIOn2 ON intensity register for I/O[2] 1111 1111
    OFF_2               = 0x31    #    RegOff2 OFF time/intensity register for I/O[2] 0000 0000
    T_ON_3              = 0x32    #    RegTOn3 ON time register for I/O[3] 0000 0000
    I_ON_3              = 0x33    #    RegIOn3 ON intensity register for I/O[3] 1111 1111
    OFF_3               = 0x34    #    RegOff3 OFF time/intensity register for I/O[3] 0000 0000
    T_ON_4              = 0x35    #    RegTOn4 ON time register for I/O[4] 0000 0000
    I_ON_4              = 0x36    #    RegIOn4 ON intensity register for I/O[4] 1111 1111
    OFF_4               = 0x37    #    RegOff4 OFF time/intensity register for I/O[4] 0000 0000
    T_RISE_4            = 0x38    #    RegTRise4 Fade in register for I/O[4] 0000 0000
    T_FALL_4            = 0x39    #    RegTFall4 Fade out register for I/O[4] 0000 0000
    T_ON_5              = 0x3A    #    RegTOn5 ON time register for I/O[5] 0000 0000
    I_ON_5              = 0x3B    #    RegIOn5 ON intensity register for I/O[5] 1111 1111
    OFF_5               = 0x3C    #    RegOff5 OFF time/intensity register for I/O[5] 0000 0000
    T_RISE_5            = 0x3D    #    RegTRise5 Fade in register for I/O[5] 0000 0000
    T_FALL_5            = 0x3E    #    RegTFall5 Fade out register for I/O[5] 0000 0000
    T_ON_6              = 0x3F    #    RegTOn6 ON time register for I/O[6] 0000 0000
    I_ON_6              = 0x40    #    RegIOn6 ON intensity register for I/O[6] 1111 1111
    OFF_6               = 0x41    #    RegOff6 OFF time/intensity register for I/O[6] 0000 0000
    T_RISE_6            = 0x42    #    RegTRise6 Fade in register for I/O[6] 0000 0000
    T_FALL_6            = 0x43    #    RegTFall6 Fade out register for I/O[6] 0000 0000
    T_ON_7              = 0x44    #    RegTOn7 ON time register for I/O[7] 0000 0000
    I_ON_7              = 0x45    #    RegIOn7 ON intensity register for I/O[7] 1111 1111
    OFF_7               = 0x46    #    RegOff7 OFF time/intensity register for I/O[7] 0000 0000
    T_RISE_7            = 0x47    #    RegTRise7 Fade in register for I/O[7] 0000 0000
    T_FALL_7            = 0x48    #    RegTFall7 Fade out register for I/O[7] 0000 0000
    T_ON_8              = 0x49    #    RegTOn8 ON time register for I/O[8] 0000 0000
    I_ON_8              = 0x4A    #    RegIOn8 ON intensity register for I/O[8] 1111 1111
    OFF_8               = 0x4B    #    RegOff8 OFF time/intensity register for I/O[8] 0000 0000
    T_ON_9              = 0x4C    #    RegTOn9 ON time register for I/O[9] 0000 0000
    I_ON_9              = 0x4D    #    RegIOn9 ON intensity register for I/O[9] 1111 1111
    OFF_9               = 0x4E    #    RegOff9 OFF time/intensity register for I/O[9] 0000 0000
    T_ON_10             = 0x4F    #    RegTOn10 ON time register for I/O[10] 0000 0000
    I_ON_10             = 0x50    #    RegIOn10 ON intensity register for I/O[10] 1111 1111
    OFF_10              = 0x51    #    RegOff10 OFF time/intensity register for I/O[10] 0000 0000
    T_ON_11             = 0x52    #    RegTOn11 ON time register for I/O[11] 0000 0000
    I_ON_11             = 0x53    #    RegIOn11 ON intensity register for I/O[11] 1111 1111
    OFF_11              = 0x54    #    RegOff11 OFF time/intensity register for I/O[11] 0000 0000
    T_ON_12             = 0x55    #    RegTOn12 ON time register for I/O[12] 0000 0000
    I_ON_12             = 0x56    #    RegIOn12 ON intensity register for I/O[12] 1111 1111
    OFF_12              = 0x57    #    RegOff12 OFF time/intensity register for I/O[12] 0000 0000
    T_RISE_12           = 0x58    #    RegTRise12 Fade in register for I/O[12] 0000 0000
    T_FALL_12           = 0x59    #    RegTFall12 Fade out register for I/O[12] 0000 0000
    T_ON_13             = 0x5A    #    RegTOn13 ON time register for I/O[13] 0000 0000
    I_ON_13             = 0x5B    #    RegIOn13 ON intensity register for I/O[13] 1111 1111
    OFF_13              = 0x5C    #    RegOff13 OFF time/intensity register for I/O[13] 0000 0000
    T_RISE_13           = 0x5D    #    RegTRise13 Fade in register for I/O[13] 0000 0000
    T_FALL_13           = 0x5E    #    RegTFall13 Fade out register for I/O[13] 0000 0000
    T_ON_14             = 0x5F    #    RegTOn14 ON time register for I/O[14] 0000 0000
    I_ON_14             = 0x60    #    RegIOn14 ON intensity register for I/O[14] 1111 1111
    OFF_14              = 0x61    #    RegOff14 OFF time/intensity register for I/O[14] 0000 0000
    T_RISE_14           = 0x62    #    RegTRise14 Fade in register for I/O[14] 0000 0000
    T_FALL_14           = 0x63    #    RegTFall14 Fade out register for I/O[14] 0000 0000
    T_ON_15             = 0x64    #    RegTOn15 ON time register for I/O[15] 0000 0000
    I_ON_15             = 0x65    #    RegIOn15 ON intensity register for I/O[15] 1111 1111
    OFF_15              = 0x66    #    RegOff15 OFF time/intensity register for I/O[15] 0000 0000
    T_RISE_15           = 0x67    #    RegTRise15 Fade in register for I/O[15] 0000 0000
    T_FALL_15           = 0x68    #    RegTFall15 Fade out register for I/O[15] 0000 0000
# Miscellaneous
    HIGH_INPUT_B        = 0x69    #    RegHighInputB High input enable register _ I/O[15_8] (Bank B) 0000 0000
    HIGH_INPUT_A        = 0x6A    #    RegHighInputA High input enable register _ I/O[7_0] (Bank A) 0000 0000
# Software Reset
    RESET               = 0x7D    #    RegReset Software reset register 0000 0000
    TEST_1              = 0x7E    #    RegTest1 Test register 0000 0000
    TEST_2              = 0x7F    #    RegTest2 Test register 0000 0000

class IOModes(Enum):
    INPUT             = 0x00
    OUTPUT            = 0x01
    INPUT_PULLUP      = 0x02
    ANALOG_OUTPUT     = 0x03
    INPUT_PULLDOWN_16 = 0x04 # PULLDOWN only possible for pin16
    WAKEUP_PULLUP     = 0x05
    WAKEUP_PULLDOWN   = 0x07


class IOLogic(Enum):
    LOW  = 0x00
    HIGH = 0x01


class SX1509IO(Wire):
    """
    SparkFun's QWIIC SX1509 IO breakout board and corresponding interface.
    """
    # Alternates can also be 0x70 and 0x71, respectively
    address = 0x3E
    jump_address = 0x3F

    pin_reset = 0xFF

    # Clock settings
    internal_clock_2MHz = 2
    external_clock = 1

    _clk = 0

    def begin(self, reset_pin=None):
        if reset_pin is not None:
            self.pin_reset = reset_pin

        if self.pin_reset != 255:
            self.reset(1)
        else:
            self.reset(0)

        data = self.read(SX1509Register.INTERRUPT_MASK_A, 2)
        if data == [0xFF, 0x00]:
            self.clock(self.internal_clock_2MHz)
            return 1
        return 0

    def reset(self, hardware):
        if hardware:
            misc = self.read(SX1509Register.MISC)
            if misc & (1 << 2):
                misc &= ~(1 << 2)
                self.write(SX1509Register.MISC, misc)

            self.pin_mode(self.pin_reset, IOModes.OUTPUT)
            self.digital_write(self.reset_pin, IOLogic.LOW)
            time.sleep(.01)  # Wait for the pin to settle
            self.digital_write(self.reset_pin, IOLogic.HIGH)

        else:
            # Software reset sequence
            self.write(SX1509Register.RESET, 0x12)
            self.write(SX1509Register.RESET, 0x34)

    def pin_dir(self, pin, iomode):
        if iomode == IOModes.OUTPUT or iomode == IOModes.ANALOG_OUTPUT:
            mode = 0
        else:
            mode = 1

        dirb = self.read_word(SX1509Register.DIR_B)
        if mode:
            dirb |= (1 << pin)
        else:
            dirb &= ~(1 << pin)
        self.write_word(SX1509Register.DIR_B, dirb)

        if iomode == IOModes.INPUT_PULLUP:
            self.write_pin(pin, IOLogic.HIGH)
        elif iomode == IOModes.ANALOG_OUTPUT:
            self.led_driver_init(pin)

    def pin_mode(self, pin, iomode):
        self.pin_dir(pin, iomode)

    def write_pin(self, pin, iologic):
        dirb = self.read_word(SX1509Register.DIR_B)
        if (0xFFFF ^ dirb) & (1 << pin):  # If the pin is an output, write high/low
            reg_data = self.read_word(SX1509Register.DATA_B)
            if iologic:
                reg_data |= 1 << pin
            else:
                reg_data &= ~(1 << pin)
            self.write_word(SX1509Register.DATA_B, reg_data)
        else:  # Otherwise the pin is an input, pull-up/down
            pullup = self.read_word(SX1509Register.PULL_UP_B)
            pulldn = self.read_word(SX1509Register.PULL_DOWN_B)

            if iologic:
                pullup |= 1 << pin
                pulldn &= ~(1 << pin)
            else:
                pulldn |= 1 << pin
                pullup &= ~(1 << pin)

            self.write_word(SX1509Register.PULL_UP_B, pullup)
            self.write_word(SX1509Register.PULL_DOWN_B, pulldn)

    def digital_write(self, pin, iologic):
        return self.write_pin(pin, iologic)

    def read_pin(self, pin):
        dirb = self.read_word(SX1509Register.DIR_B)

        if dirb & (1 << pin):
            datab = self.read_word(SX1509Register.DATA_B)
            if datab & (1 << pin):
                return 1
        return 0

    def digital_read(self, pin):
        return self.read_pin(pin)

    def led_driver_init(self, pin, freq=1, log=False):
        # Disable input buffer
        indisable = self.read_word(SX1509Register.INPUT_DISABLE_B)
        indisable |= 1 << pin
        self.write_word(SX1509Register.INPUT_DISABLE_B, indisable)

        # Disable pull-up
        pullup = self.read_word(SX1509Register.PULL_UP_B)
        pullup &= ~(1 << pin)
        self.write_word(SX1509Register.PULL_UP_B, pullup)

        # Set direction to output
        direction = self.read_word(SX1509Register.DIR_B)
        direction &= ~(1 << pin)
        self.write_word(SX1509Register.DIR_B, direction)

        # Enable oscillator
        clock = self.read(SX1509Register.CLOCK)
        clock |= 1 << 6  # Internal 2MHz oscillator part 1 (set bit 6)
        clock &= ~(1 << 5)  # Internal 2MHz oscillator part 2 (clear bit 5)
        self.write(SX1509Register.CLOCK, clock)

        misc = self.read(SX1509Register.MISC)
        if log:  # set log mode
            misc |= 1 << 7
            misc |= 1 << 3
        else:  # set linear mode
            misc |= ~(1 << 7)
            misc |= ~(1 << 3)

        # Use config clock to setup the clock divider
        if self._clk == 0:
            self._clk = 2000000 / (1 << (1 - 1))
            freq = (1 & 0x07) << 4
            misc |= freq

        self.write(SX1509Register.MISC, misc)

        # Enable LED driver operation
        driver = self.read_word(SX1509Register.LED_DRIVER_ENABLE_B)
        driver |= 1 << pin
        self.write_word(SX1509Register.LED_DRIVER_ENABLE_B, driver)

        # Set DATA bit low ~ LED driver started
        data = self.read_word(SX1509Register.DATA_B)
        data &= ~(1 << pin)
        self.write_word(SX1509Register.DATA_B, data)

    def pwm(self, pin, intensity):
        # Just intensity or relative to log(intensity)
        self.write(getattr(SX1509Register, f"I_ON_{pin}"), intensity)

    def analog_write(self, pin, intensity):
        self.pwm(pin, intensity)

    def blink(self, pin, time_on, time_off, max_intensity, min_intensity):
        on_reg = self.calculate_led_t_reg(time_on)
        off_reg = self.calculate_led_t_reg(time_off)
        self.setup_blink(
            pin, on_reg, off_reg, max_intensity, min_intensity, 0, 0)

    def breathe(self, pin, time_on, time_off, rise, fall, max_intensity,
                min_intensity, log=False):
        min_intensity = constrain(min_intensity, 0, 7)

        on_reg = self.calculate_led_t_reg(time_on)
        off_reg = self.calculate_led_t_reg(time_off)

        rise_time = self.calculate_slope_reg(rise, max_intensity, min_intensity)
        fall_time = self.calculate_slope_reg(fall, max_intensity, min_intensity)

        self.setup_blink(pin, on_reg, off_reg, max_intensity, min_intensity,
                         rise_time, fall_time, log)

    def setup_blink(self, pin, time_on, time_off, max_intensity, min_intensity,
            time_rise, time_fall, log=False):
        self.led_driver_init(pin, log)

        # Should be 5-bit values
        time_on &= 0x1F
        time_off &= 0x1F
        time_rise &= 0x1F
        time_fall &= 0x1F
        min_intensity &= 0x07  # 3-bit value

        # Write the time on
	# 1-15:  TON = 64 * time_on * (255/self._clk)
	# 16-31: TON = 512 * time_on * (255/self._clk)
	self.write(getattr(SX1509Register, f"T_ON_{pin}", time_on))

        # Write the time/intensity off register
	# 1-15:  TOFF = 64 * time_off * (255/ClkX)
	# 16-31: TOFF = 512 * time_off * (255/ClkX)
	# linear Mode - IOff = 4 * min_intensity
	# log mode - Ioff = f(4 * min_intensity)
	self.write(getattr(SX1509Register, f"OFF_{pin}"),
                    (time_off << 3) | min_intensity)

	self.write(getattr(SX1509Register, f"I_ON_{pin}"), max_intensity)

        # Write regTRise
	# 0: Off
	# 1-15:  TRise =      (regIOn - (4 * min_intensity)) * time_rise * (255/_clk)
	# 16-31: TRise = 16 * (regIOn - (4 * min_intensity)) * time_rise * (255/_clk)
        if getattr(SX1509Register, f"T_RISE_{pin}") != 0xFF:
            self.write(getattr(SX1509Register, f"T_RISE_{pin}"), time_rise);

	# Write regTFall
	# 0: off
	# 1-15:  TFall =      (regIOn - (4 * min_intensity)) * time_fall * (255/clk)
	# 16-31: TFall = 16 * (regIOn - (4 * min_intensity)) * time_fall * (255/clk)
        if getattr(SX1509Register, f"T_FALL_{pin}") != 0xFF:
            self.write(getattr(SX1509Register, f"T_FALL_{pin}"), time_fall);

    def clock(osc_src, osc_divider, osc_pin_func, osc_freq_out):
        self.config_clock(osc_src, osc_divider, osc_pin_func, osc_freq_out):

    def config_clock(osc_src, osc_divider, osc_pin_func, osc_freq_out):
        # RegClock constructed as follows:
	#	6:5 - Oscillator frequency souce
	#		00: off, 01: external input, 10: internal 2MHz, 1: reserved
	#	4 - OSCIO pin function
	#		0: input, 1 ouptut
	#	3:0 - Frequency of oscout pin
	#		0: LOW, 0xF: high, else fOSCOUT = FoSC/(2^(RegClock[3:0]-1))
	osc_source = (osc_source & 0b11) << 5  # 2-bit value, bits 6:5
	osc_pin_func = (osc_pin_func & 1) << 4  # 1-bit value bit 4
	osc_freq_out = (osc_freq_out & 0b1111)  # 4-bit value, bits 3:0
	clock = osc_source | osc_pin_function | osc_freq_out
	self.write(SX1509Register.CLOCK, clock)

        # Config RegMisc[6:4] with oscDivider
	# 0: off, else ClkX = fOSC / (2^(RegMisc[6:4] -1))
	osc_divider = constrain(osc_divider, 1, 7)
	self._clk = 2000000.0 / (1 << (osc_divider - 1))  # Update private clock variable
	osc_divider = (osc_divider & 0b111) << 4  # 3-bit value, bits 6:4

	misc = self.read(SX1509Register.MISC);
	misc &= ~(0b111 << 4)
	misc |= osc_divider
	self.write(SX1509Register.MISC, misc);

    def calculate_led_t_reg(self, ms):
        if self._clk == 0:
            return 0

        on1 = (ms / 1000.0) / (64.0 * 255.0 / float(self._clk))
        on2 = on1 / 8
        on1 = constrain(on1, 1, 15)
        on2 = constrain(on2, 16, 31)

        time_on1 = 64.0 * on1 * 255.0 / self._clk * 1000.0
        time_on2 = 512.0 * on2 * 255.0 / self._clk * 1000.0

        if abs(time_on1 - ms) < abs(time_on2 - ms):
            return on1
        return on2

    def calculate_slope_reg(ms, max_intensity, min_intensity):
        if self._clk == 0:
            return 0

        time_factor = max_intensity - (4.0 * min_intensity) * 255.0 / self._clk
        time_s = ms / 1000.0

        slope1 = time_s / time_factor
        slope2 = slope1 / 16
        slope1 = constrain(slope1, 1, 15)
        slope2 = constrain(slope2, 16, 31)

        time1 = slope1 * time_factor * 1000.0
        time2 = 16 * slope1

        if abs(time1 - ms) < abs(time2 - ms):
            return slope1
        return slope2
