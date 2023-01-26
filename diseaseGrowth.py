import math

# Will keep healthy members for each country for now as a fixed 0.7, might need to adjust later on
ACTIVE_PEOPLE = 0.7


def update(current, activityLevel):
    current = current * activityLevel * ACTIVE_PEOPLE
    return math.ceil(current)
