import math


def update(current, activityLevel):
    current = current * activityLevel
    return math.ceil(current)
