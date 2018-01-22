import sys
from time import sleep
from datetime import timedelta, datetime, date, time
import logging

logger = logging.getLogger(__name__)

import milight as mi

MORNING_ZONE = 3


def init():
    logging.info("On and set min brightness")
    mi.on(MORNING_ZONE)
    mi.brightness(0)
    sleep(1)
    mi.off(MORNING_ZONE)


def morning(testing=False):
    logger.info("Morning occurred")
    logger.info("On, prepare for fade")
    mi.on(MORNING_ZONE)
    sleep(1)
    logger.info("Fade")
    mi.fade_brightness(60*15 if not testing else 10)


def evening():
    logger.info("Evening occurred")
    logger.info("Fading out")
    mi.fade_brightness(60*5, fadeout=True)


def time_to_morning():
    time_to_next_time(time(hour=7, minute=30))


def next_time(clock: time):
    today = date.today()
    dt = datetime.combine(today, clock)

    now = datetime.now()
    if(now < dt):
        return dt
    else:
        # Next time is tomorrow (After 24:00 today)
        return (dt + timedelta(days=1))


def wait_until(dt: datetime):
    wait_time = dt - datetime.now()
    logger.debug("Waiting until {}, will take {} ({}s)".format(str(dt), str(wait_time), wait_time.total_seconds()))
    sleep(wait_time.total_seconds())


assert next_time(time(hour=7, minute=30)) > datetime.now()
assert next_time(time(hour=20, minute=00)) > datetime.now()

if __name__ == "__main__":
    testing = "--testing" in sys.argv

    logging.basicConfig(level=logging.DEBUG if testing else logging.INFO)

    init()

    morning_time = time(hour=7, minute=00)
    evening_time = time(hour=18, minute=0)

    if testing:
        morning_time = (datetime.now() + timedelta(seconds=5)).time()

    while True:
        if next_time(morning_time) < next_time(evening_time):
            logger.info("Waiting for morning")
            wait_until(next_time(morning_time))
            morning(testing=testing)
        else:
            print("Waiting for evening")
            mi.on(MORNING_ZONE)
            mi.brightness(19)
            wait_until(next_time(evening_time))
            evening()
