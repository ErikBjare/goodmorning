"""
A small library for controlling Milights.


Usage:

 - Call the on(zone) function with the zone of choice
 - Use any of the other commands to control the lamp turned on with on(zone)

"""

import socket
from time import sleep

import logging

logger = logging.getLogger(__name__)

# Zones used for selecting and turning on lamps,
# the array used for turning lamps off is similar (see `off()` function)
_ZONE_ARRAY = [0x42, 0x45, 0x47, 0x49, 0x4B]

# The values below 0x02 do nothing, values above 0x1B also do nothing
_BRIGHTNESS_ARRAY = list(range(0x02, 0x1C))

BRIGHTNESS_LEVELS = len(_BRIGHTNESS_ARRAY)

HUE_RED = 174
HUE_BLUE = 240


def _get_zone(zone) -> int:
    return _ZONE_ARRAY[zone]


def _msg(b1, b2=0x00, b3=0x55) -> bytes:
    return bytes([b1, b2, b3])


def _repr_cmd(cmd) -> str:
    return str(list(map(hex, cmd)))


def _on(zone) -> bytes:
    msg = _msg(_get_zone(zone))
    return msg


def _off(zone):
    if zone == 0:
        return _msg(0x41)
    else:
        return _msg(_get_zone(zone) + 1)


def _hue_msg(h) -> bytes:
    """h should be a value in the range 0-255"""
    return _msg(0x40, h)


def _brightness_msg(b):
    """b should be in range 0-19"""
    return _msg(0x4E, _BRIGHTNESS_ARRAY[b])


def _whitemode_msg():
    return _msg(0xC2)


"""
"
"  Public API
"
"""


def send_cmd(cmd: bytes):
    logger.debug(_repr_cmd(cmd))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(cmd, ('255.255.255.255', 8899))

    # Ensures that the call is respected, calling repeatedly without this may cause package loss
    sleep(0.5)


def on(zone) -> None:
    logger.info(f"Turning ON zone {zone}")
    send_cmd(_on(zone))


def off(zone):
    logger.info(f"Turning OFF zone {zone}")
    send_cmd(_off(zone))


def hue(h):
    logger.info(f"Setting hue {h}")
    send_cmd(_hue_msg(h))


def brightness(b):
    logger.info(f"Setting brightness {b}")
    send_cmd(_brightness_msg(b))


def whitemode():
    send_cmd(_whitemode_msg())


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


def fade_brightness(time, fadeout=False):
    """
    Fades in from lowest to highest during a total of the passed argument time.
    If argument fadein is set to False it will instead fade out from the highest to lowest.
    """
    logger.info(f"Fading {'out' if fadeout else 'in'} for {time} seconds")
    step = time / BRIGHTNESS_LEVELS
    for i in range(BRIGHTNESS_LEVELS):
        if fadeout:
            i = (BRIGHTNESS_LEVELS - 1) - i
        brightness(i)
        sleep(step)


if __name__ == "__main__":
    #blink(loop=False)
    #test_brightness_levels()
    on(3)
    hue(HUE_RED)
    fade_brightness(15)
    fade_brightness(15, fadeout=True)

