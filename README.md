# pyglow
Python module for PiGlow board for RPi

## Setup

You'll need python-smbus and some other stuff.  Please see
https://github.com/pimoroni/piglow#setting-up-your-raspberry-pi

Enable i2c drivers

    sudo -e /etc/modules

Then ensure you have the following in there:

    i2c-dev
    i2c-bcm2708

You may also need to check these drivers aren't blacklisted:

    grep bcm2708 /etc/modprobe.d/raspi-blacklist.conf

If ```spi-bcm2708``` or ```i2c-bcm2708``` are there, comment them out.

Next up, install i2c libs and Python support:

    sudo apt-get install python-smbus

Finally, reboot your RPi.

    sudo shutdown -r now

