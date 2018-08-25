#!/usr/bin/env python

"""
CPU monitor using the PiGlow LEDs.

Due to the use of GPIO, you need to be root.

sudo pigl_cpu.py start

It uses python-daemon to run in the background.

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

from pyglow import PyGlow
from time import sleep
import psutil
import atexit
from daemon import runner
from itertools import cycle
import numpy as np


class PyGlowCPU(object):

    """Main PyGlowCPU app."""

    def __init__(self, method=1):
        """Setup daemon stuff."""
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = '/var/run/pyglowcpu.pid'
        self.pidfile_timeout = 5
        self.method = method

    def run(self):
        """Entry point for DaemonRunner.do_action()."""
        self.piglow = PyGlow()
        atexit.register(lambda: self.piglow.all(0))
        mth = getattr(self, 'method%d' % (self.method))
        mth()

    def method1(self):
        """CPU load increases ring usage every 20%."""
        while True:
            cpu = psutil.cpu_percent()
            self.piglow.all(0)
            if 0 < cpu < 10:
                pass
            elif 10 < cpu < 20:
                self.piglow.red(20)
            elif cpu < 20:
                self.piglow.red(20)
                self.piglow.orange(20)
            elif cpu < 40:
                self.piglow.red(20)
                self.piglow.orange(20)
                self.piglow.yellow(20)
            elif cpu < 60:
                self.piglow.red(20)
                self.piglow.orange(20)
                self.piglow.yellow(20)
                self.piglow.green(20)
            elif cpu < 80:
                self.piglow.red(50)
                self.piglow.orange(50)
                self.piglow.yellow(50)
                self.piglow.green(50)
                self.piglow.blue(50)
            else:
                self.piglow.all(100)
            sleep(0.2)

    def method2(self):
        """Represent 20% on arm1."""
        while True:
            cpu = psutil.cpu_percent()
            self.piglow.all(0)

            if 0 < cpu < 10:
                pass
            elif 10 < cpu < 20:
                self.piglow.led1(20)
            elif cpu < 20:
                self.piglow.led1(20)
                self.piglow.led2(20)
            elif cpu < 40:
                self.piglow.led1(20)
                self.piglow.led2(20)
                self.piglow.led3(20)
            elif cpu < 60:
                self.piglow.led1(30)
                self.piglow.led2(30)
                self.piglow.led3(30)
                self.piglow.led4(30)
            elif cpu < 80:
                self.piglow.led1(60)
                self.piglow.led2(60)
                self.piglow.led3(60)
                self.piglow.led4(60)
                self.piglow.led5(60)
            else:
                self.piglow.arm1(100)
            sleep(0.2)

    def method3(self):
        """Represent 20% on arm2."""
        while True:
            cpu = psutil.cpu_percent()
            self.piglow.all(0)

            if 0 < cpu < 10:
                pass
            elif 10 < cpu < 20:
                self.piglow.led7(20)
            elif cpu < 20:
                self.piglow.led7(20)
                self.piglow.led8(20)
            elif cpu < 40:
                self.piglow.led7(20)
                self.piglow.led8(20)
                self.piglow.led9(20)
            elif cpu < 60:
                self.piglow.led7(30)
                self.piglow.led8(30)
                self.piglow.led9(30)
                self.piglow.led10(30)
            elif cpu < 80:
                self.piglow.led7(60)
                self.piglow.led8(60)
                self.piglow.led9(60)
                self.piglow.led10(60)
                self.piglow.led11(60)
            else:
                self.piglow.arm2(100)
            sleep(0.2)

    def method4(self):
        """Represent 20% on arm3."""
        while True:
            cpu = psutil.cpu_percent()
            self.piglow.all(0)

            if 0 < cpu < 10:
                pass
            elif 10 < cpu < 20:
                self.piglow.led13(20)
            elif cpu < 20:
                self.piglow.led13(20)
                self.piglow.led14(20)
            elif cpu < 40:
                self.piglow.led13(20)
                self.piglow.led14(20)
                self.piglow.led15(20)
            elif cpu < 60:
                self.piglow.led13(30)
                self.piglow.led14(30)
                self.piglow.led15(30)
                self.piglow.led16(30)
            elif cpu < 80:
                self.piglow.led13(60)
                self.piglow.led14(60)
                self.piglow.led15(60)
                self.piglow.led16(60)
                self.piglow.led17(60)
            else:
                self.piglow.arm3(100)
            sleep(0.2)

    def method5(self):
        """Represent using gamma."""
        while True:
            cpu = psutil.cpu_percent()
            self.piglow.all(int(cpu*2))
            sleep(0.2)

    def method6(self):
        """Rotate the arms CW."""
        armiter = cycle((1,2,3))
        for target_arm in armiter:
            cpu = psutil.cpu_percent()
            self.piglow.all(0)

            target_arm -= 1  # 0-based indexing
            a = np.array([0,1,2,3,4,5])
            p = np.floor(np.percentile(a, cpu))
            for x in range(int(p)+1):
                f = getattr(self.piglow, 'led%d' % self.piglow.arm_led_list[target_arm][x])
                f(20)

            sleep(0.2)

    def method7(self):
        """Rotate the arms CCW."""
        armiter = cycle((3,2,1))
        for target_arm in armiter:
            cpu = psutil.cpu_percent()
            self.piglow.all(0)

            target_arm -= 1  # 0-based indexing
            a = np.array([0,1,2,3,4,5])
            p = np.floor(np.percentile(a, cpu))
            for x in range(int(p)+1):
                f = getattr(self.piglow, 'led%d' % self.piglow.arm_led_list[target_arm][x])
                f(20)

            sleep(0.2)


app = PyGlowCPU(method=7)
d = runner.DaemonRunner(app)
d.do_action()
