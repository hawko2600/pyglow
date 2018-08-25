"""
PyGlow.py.

AdaFruit makes these fun little GPIO boards for the Raspberry Pi called
PiGlow.  This Python module will let you watchen das blinkenlights.

Copyright 2015 Matthew Hawkins

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import print_function

from collections import OrderedDict
import types
import logging

try:
    from smbus import SMBus
    pass
except ImportError:
    print("This module requires python-smbus installed.  Exiting.")
    exit(1)

import RPi.GPIO as rpi


class PyGlow(object):

    """
    PyGlow class.

    Provides instance mathods to turn on leds in exciting ways.
    """

    led_map = OrderedDict({
        1: 0x07,
        2: 0x08,
        3: 0x09,
        4: 0x06,
        5: 0x05,
        6: 0x0A,
        7: 0x12,
        8: 0x11,
        9: 0x10,
        10: 0x0E,
        11: 0x0C,
        12: 0x0B,
        13: 0x01,
        14: 0x02,
        15: 0x03,
        16: 0x04,
        17: 0x0F,
        18: 0x0D
    })
    colours = {
        'white': [led_map[6], led_map[12], led_map[18]],
        'blue':  [led_map[5], led_map[11], led_map[17]],
        'green': [led_map[4], led_map[16], led_map[10]],
        'yellow': [led_map[3], led_map[15], led_map[9]],
        'orange': [led_map[2], led_map[14], led_map[8]],
        'red':   [led_map[1], led_map[13], led_map[7]]
    }
    col_map = OrderedDict({
        1: 'white',
        2: 'blue',
        3: 'green',
        4: 'yellow',
        5: 'orange',
        6: 'red'
    })
    i2c_addr = 0x54
    arm_led_list = map(tuple, (range(1, 7), range(7, 13), range(13, 19)))
    gamma_map = (0, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 1, 1, 1, 1, 1, 1, 1, 1,
                 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 2, 2, 2, 2, 2,
                 2, 2, 2, 3, 3, 3, 3, 3,
                 3, 3, 3, 3, 3, 3, 3, 3,
                 4, 4, 4, 4, 4, 4, 4, 4,
                 4, 4, 4, 5, 5, 5, 5, 5,
                 5, 5, 5, 6, 6, 6, 6, 6,
                 6, 6, 7, 7, 7, 7, 7, 7,
                 8, 8, 8, 8, 8, 8, 9, 9,
                 9, 9, 10, 10, 10, 10, 10, 11,
                 11, 11, 11, 12, 12, 12, 13, 13,
                 13, 13, 14, 14, 14, 15, 15, 15,
                 16, 16, 16, 17, 17, 18, 18, 18,
                 19, 19, 20, 20, 20, 21, 21, 22,
                 22, 23, 23, 24, 24, 25, 26, 26,
                 27, 27, 28, 29, 29, 30, 31, 31,
                 32, 33, 33, 34, 35, 36, 36, 37,
                 38, 39, 40, 41, 42, 42, 43, 44,
                 45, 46, 47, 48, 50, 51, 52, 53,
                 54, 55, 57, 58, 59, 60, 62, 63,
                 64, 66, 67, 69, 70, 72, 74, 75,
                 77, 79, 80, 82, 84, 86, 88, 90,
                 91, 94, 96, 98, 100, 102, 104, 107,
                 109, 111, 114, 116, 119, 122, 124, 127,
                 130, 133, 136, 139, 142, 145, 148, 151,
                 155, 158, 161, 165, 169, 172, 176, 180,
                 184, 188, 192, 196, 201, 205, 210, 214,
                 219, 224, 229, 234, 239, 244, 250, 255)

    def __init__(self):
        """Initialise an instance of PyGlow."""
        # Init GPIO.  First, check which RPi we have.
        if rpi.RPI_INFO['REVISION'] in ('0002', '0003'):
            i2c_bus = 0
        else:
            i2c_bus = 1
        # Setup the PyGlow on the SMBus
        self.bus = SMBus(i2c_bus)
        self.bus.write_i2c_block_data(self.i2c_addr, 0x00, [0x01])
        # Enable each LED arm.
        for i in [0x13, 0x14, 0x15]:
            self.bus.write_byte_data(self.i2c_addr, i, 0xFF)

        # init some access methods
        def make_colour(name):
            def colour(self, value=20):
                logging.debug("Colour: {}".format(name))
                self.set_leds(self.colours[name], value)
                return self.colours[name], value
            return colour
        for c in self.colours:
            setattr(self, c, types.MethodType(make_colour(c), self, PyGlow))

        def make_leds(lednum):
            def led(self, value=20):
                logging.debug("LED: {}".format(value))
                self.set_leds([self.led_map[lednum]], value)
                return self.led_map[lednum], value
            return led
        for j in range(18):
            setattr(self, 'led%d' % (j+1), types.MethodType(make_leds(j+1), self, PyGlow))

    def all(self, value=20):
        """Turn on all the LEDs."""
        die = False
        if isinstance(value, int) and 0 <= value <= 255:
            v = int(self.gamma_map[value])
            if isinstance(v, int) and 0 <= value <= 255:
                self.bus.write_i2c_block_data(self.i2c_addr, 0x01, [v]*18)
                self.bus.write_byte_data(self.i2c_addr, 0x16, 0xFF)
            else:
                die = True
        else:
            die = True
        if die:
            raise PyGlowException(self, "All Brightness(0-255): {}".format(value))

    def arm(self, arm, value=20):
        """Turn on all the LEDs in the given arm (1-3)."""
        if isinstance(arm, int) and 1 <= arm <= 3:
            leds = [self.led_map[l] for l in self.arm_led_list[arm-1]]
            self.set_leds(leds, value)
        else:
            raise PyGlowException(self, "Arm {} is invalid.".format(arm))

    def arm1(self, value=20):
        """Turn on all the LEDs in arm 1."""
        return self.arm(1, value)

    def arm2(self, value=20):
        """Turn on all the LEDs in arm 2."""
        return self.arm(2, value)

    def arm3(self, value=20):
        """Turn on all the LEDs in arm 3."""
        return self.arm(3, value)

    def led(self, led, value=20):
        """Turn on the given LED (1-18)."""
        self.set_leds([self.led_map[led]], value)

    def colour(self, colour, value=20):
        """Turn on all the LEDs of the given colour."""
        if isinstance(colour, int):
            c = self.col_map[colour]
        elif isinstance(colour, str):
            c = colour
        else:
            raise PyGlowException(self, "Unknown colour %s" % colour)
        self.set_leds(self.colours[c], value)

    def set_leds(self, leds, value=20):
        """Update LED settings."""
        if isinstance(value, int) and 0 <= value <= 255:
            for led in leds:
                self._update(led, self.gamma_map[value])
            self.bus.write_byte_data(self.i2c_addr, 0x16, 0xFF)
        else:
            raise PyGlowException(self, "Brightness(0-255): {}".format(value))

    def _update(self, led, value=20):
        if isinstance(led, int) and 1 <= led <= 18 and \
                isinstance(value, int) and 0 <= value <= 255:
            self.bus.write_byte_data(self.i2c_addr, led, value)
            logging.debug("write_byte_data(self.i2c_addr, {}, {})".format(led, value))
        else:
            raise PyGlowException(self, "LED(1-18): {} | Brightness(0-255): {}\n".format(led, value))


class PyGlowException(Exception):

    """Gracefully handle issues with PyGlow class."""

    def __init__(self, parent, msg):
        """Call using raise, pass in self and a message."""
        parent.all(0)  # turn off all the LEDs on error
        self.message = msg

    def __str__(self):
        """Give the error message."""
        return self.message
