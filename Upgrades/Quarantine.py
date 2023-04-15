from Upgrades.Upgrade import *
from enum import Enum


class Quarantine(Upgrade):

    def __init__(self, name, description, cost, affected_countries, effect, requirements):
        super().__init__(name, description, cost, effect, requirements)
        self.affected_countries = affected_countries
        self.airports_closed = False
        self.land_closed = False

    SHUTDOWN_AIRPORTS_COST = 1
    SHUTDOWN_LAND_COST = 2
    LOCKDOWN = 5

    def close_air_access(self, current):
        # Parse in countries and set to corresponding value
        # Also could update flight log in this class
        if current > self.SHUTDOWN_AIRPORTS_COST:
            current = current - self.SHUTDOWN_AIRPORTS_COST
            print(self.name + ": Airports have been closed")
            self.airports_closed = True
        else:
            print("Unable to close airports")
        return current

    def close_land_access(self, current):
        if current > self.SHUTDOWN_LAND_COST:
            current = current - self.SHUTDOWN_LAND_COST
            print(self.name + ": Lands have been closed")
            self.land_closed = True
        else:
            print("Unable to close lands")

    def lockdown(self, current):
        if current > self.LOCKDOWN:
            current = current - self.LOCKDOWN
            print(self.name + ": is in lockdown")
        else:
            print("Unable to start lockdown")
        return current
