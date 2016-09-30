from time import sleep
import milight as mi
from datetime import timedelta, datetime, date, time

MORNING_ZONE = 3


def init():
    print("On and set min brightness")
    mi.on(MORNING_ZONE)
    mi.brightness(0)
    sleep(1)
    mi.off(MORNING_ZONE)


def morning(testing=False):
    print("Morning occurred")
    print("On, prepare for fade")
    mi.on(MORNING_ZONE)
    sleep(1)
    print("Fade")
    mi.fade_brightness(60*5 if not testing else 10)


def evening():
    print("Evening occurred")
    print("Fading out")
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
    print("Waiting until {}, will take {} ({}s)".format(str(dt), str(wait_time), wait_time.total_seconds()))
    sleep(wait_time.total_seconds())


assert next_time(time(hour=7, minute=30)) > datetime.now()
assert next_time(time(hour=20, minute=00)) > datetime.now()

if __name__ == "__main__":
    testing = False

    init()

    morning_time = time(hour=7, minute=30)
    evening_time = time(hour=20, minute=0)

    if testing:
        morning_time = (datetime.now() + timedelta(seconds=5)).time()

    while True:
        if next_time(morning_time) < next_time(evening_time):
            print("Waiting for morning")
            wait_until(next_time(morning_time))
            morning(testing=testing)
        else:
            print("Waiting for evening")
            mi.on(MORNING_ZONE)
            mi.brightness(19)
            wait_until(next_time(evening_time))
            evening()
