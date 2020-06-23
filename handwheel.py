#!/usr/bin/env python2.7
#    HAL userspace component to interface with Arduino board
#    by Colin Kingsbury (https://ckcnc.wordpress.com_)
#    Inspired by the earlier example from Jeff Epler
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
import serial
import hal
import sys
import time

DEBUG = False

# First we open the serial port. This should correspond to the port the Arduino
# is connected to. This can be found in the Arduino IDE in Tools->Serial Port
PORT = "/dev/handwheel0"
ser = serial.Serial(PORT, 115200)

# Now we create the HAL component and its pins
c = hal.component("handwheel")
c.newpin("plus", hal.HAL_BIT, hal.HAL_IN)
c.newpin("rapid", hal.HAL_BIT, hal.HAL_IN)
c.newpin("minus", hal.HAL_BIT, hal.HAL_IN)
c.newpin("act", hal.HAL_BIT, hal.HAL_IN)
# c.newpin("left",hal.HAL_U32,hal.HAL_IN)
# c.newpin("right",hal.HAL_U32,hal.HAL_IN)
c.newpin("enable-x", hal.HAL_BIT, hal.HAL_IN)
c.newpin("enable-y", hal.HAL_BIT, hal.HAL_IN)
c.newpin("enable-z", hal.HAL_BIT, hal.HAL_IN)
c.newpin("encoder", hal.HAL_S32, hal.HAL_IN)
c.newpin("scale", hal.HAL_FLOAT, hal.HAL_IN)
c.ready()

def debug(text):
    if DEBUG:
        print(text)

def set_enable(v):
    if v == 1:
        debug("enable X")
        c["enable-x"] = 1
        c["enable-y"] = 0
        c["enable-z"] = 0
    elif v == 2:
        debug("enable Y")
        c["enable-x"] = 0
        c["enable-y"] = 1
        c["enable-z"] = 0
    elif v == 3:
        debug("enable Z")
        c["enable-x"] = 0
        c["enable-y"] = 0
        c["enable-z"] = 1
    else:
        debug("disable all")
        c["enable-x"] = 0
        c["enable-y"] = 0
        c["enable-z"] = 0


def set_scale(v):
    if v == 1:
        debug("Scale 0.0")
        return 0.0
    elif v == 2:
        debug("Scale 0.0001")
        return 0.0001
    elif v == 3:
        debug("Scale 0.001")
        return 0.001
    elif v == 4:
        debug("Scale 0.01")
        return 0.01
    elif v == 5:
        debug("Scale 0.1")
        return 0.1
    elif v == 6:
        debug("Scale 1.0")
        return 1.0
    else:
        debug("Scale 0.0")
        return 0.0


try:
    while True:
        while ser.inWaiting():
            key = ser.readline()
            key = key.strip().lower()
            k, v = key.split(":")
            # Scale
            if k == "right":
                c["scale"] = set_scale(float(v))
            # Enable
            elif k == "left":
                set_enable(int(v))
            else:
                keys = ["plus", "rapid", "minus", "act", "encoder"]
                if k not in keys:
                    debug("unknown key {0} = {1}".format(k, v))
                else:
                    debug("key {0} = {1}".format(k, v))
                    c[k] = v


except KeyboardInterrupt:
    raise SystemExit
