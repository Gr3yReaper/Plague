import math
import random

# Will keep healthy members for each country for now as a fixed 0.7, might need to adjust later on
ACTIVE_PEOPLE = 0.7


def update(current, activity_level, awareness, protective, medical):
    factor = random.randint(1, 10)
    factor = factor / 10
    current = (current * activity_level * ACTIVE_PEOPLE * factor) / (awareness + protective + medical)
    return math.ceil(current)
