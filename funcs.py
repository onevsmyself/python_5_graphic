from random import randint
from math import sin, cos, radians


def bird_fly(x, y, is_day):
    if is_day:
        return y
    else:
        return abs(round(randint(1, 3) * sin(x / 40) + y))


def calc_speed_orb(time, fps):
    degrees_per_second = 360 / time  # Градусов в секунду
    orbit_speed = degrees_per_second / fps  # Скорость вращения в градусах за кадр
    return orbit_speed
