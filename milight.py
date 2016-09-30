"""
A small library for controlling Milights.


Usage:

 - Call the on(zone) function with the zone of choice
 - Use any of the other commands to control the lamp turned on with on(zone)

"""

import socket
from time import sleep

# Zones used for selecting and turning on lamps,
# the array used for turning lamps off is similar (see `off()` function)
_ZONE_ARRAY = [0x42, 0x45, 0x47, 0x49, 0x4B]

# The values below 0x02 do nothing, values above 0x1B also do nothing
_BRIGHTNESS_ARRAY = list(range(0x02, 0x1C))
#assert len(_BRIGHTNESS_ARRAY) == 19

BRIGHTNESS_LEVELS = len(_BRIGHTNESS_ARRAY)

HUE_RED = 174;
HUE_BLUE = 240;

def _get_zone(zone):
    return _ZONE_ARRAY[zone]

def _msg(b1, b2=0x00, b3=0x55):
    return bytes([b1, b2, b3])

def _print_cmd(cmd):
    print(list(map(hex, cmd)))

def on(zone):
    msg = _msg(_get_zone(zone))
    return msg

def off(zone):
    if zone == 0:
        return _msg(0x41)
    else:
        return _msg(_get_zone(zone)+1)

def hue(h):
    """h should be a value in the range 0-255"""
    return _msg(0x40, h)

def brightness(b):
    """b should be in range 0-19"""
    return _msg(0x4E, _BRIGHTNESS_ARRAY[b])

def whitemode():
    return _msg(0xC2)

def send_cmd(cmd):
    _print_cmd(cmd)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(cmd, ('255.255.255.255', 8899))

    # Ensures that the call is respected, calling repeatedly without this may cause package loss
    sleep(0.5)

def blink(loop=False):
    while True:
        ZONE = 0
        SLEEP_TIME = 1
        send_cmd(on(ZONE))
        sleep(SLEEP_TIME)
        send_cmd(off(ZONE))
        if not loop:
            break
        sleep(SLEEP_TIME)

def test_brightness_levels():
    send_cmd(on(4))
    sleep(1)
    send_cmd(whitemode())
    for b in range(len(_BRIGHTNESS_ARRAY)):
        send_cmd(brightness(0))
        sleep(1)
        send_cmd(brightness(b))
        sleep(1)

def fade_brightness(time, fadein=True):
    """
    Fades in from lowest to highest during a total of the passed argument time.
    If argument fadein is set to False it will instead fade out from the highest to lowest.
    """
    step = time/BRIGHTNESS_LEVELS
    for i in range(BRIGHTNESS_LEVELS):
        if not fadein:
            i = (BRIGHTNESS_LEVELS-1) - i
        send_cmd(brightness(i))
        sleep(step)


if __name__ == "__main__":
    #blink(loop=False)
    #test_brightness_levels()
    send_cmd(on(3))
    send_cmd(hue(HUE_RED))
    fade_brightness(15, fadein=False)

