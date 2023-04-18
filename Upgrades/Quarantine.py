from Upgrades.Upgrade import *
from enum import Enum


class Quarantine(Upgrade):

    def __init__(self, name, description, cost, affected_countries, effect, requirements):
        super().__init__(name, description, cost, effect, requirements)
        self.affected_countries = affected_countries
        self.airports_closed = False
        self.land_closed = False
        self.current_lockdown = False

    SHUTDOWN_AIRPORTS_COST = 1
    SHUTDOWN_LAND_COST = 2
    LOCKDOWN = 5

    def close_air_access(self, current):
        # Parse in countries and set to corresponding value
        # Also could update flight log in this class
        if current > self.SHUTDOWN_AIRPORTS_COST and not self.airports_closed:
            current = current - self.SHUTDOWN_AIRPORTS_COST
            print(self.name + ": Airports have been closed")
            # Import the countries, loop through them, updating ones in affected_countries, to shut airports
            # Repeat this for each of the methods
            self.airports_closed = True
        else:
            if self.airports_closed and current > self.SHUTDOWN_AIRPORTS_COST:
                current = current - self.SHUTDOWN_AIRPORTS_COST
                print(self.name + ": Airports have been opened")
                self.airports_closed = False
            elif self.airports_closed:
                print("Unable to open airports")
            else:
                print("Unable to close airports")

        return current

    def close_land_access(self, current):
        if current > self.SHUTDOWN_LAND_COST and not self.land_closed:
            current = current - self.SHUTDOWN_LAND_COST
            print(self.name + ": Lands have been closed")
            self.land_closed = True
        else:
            if self.land_closed and current > self.SHUTDOWN_LAND_COST:
                current = current - self.SHUTDOWN_LAND_COST
                print(self.name + ": Lands have been opened")
                self.land_closed = False
            elif self.land_closed:
                print("Unable to open lands")
            else:
                print("Unable to close lands")
        return current

    def lockdown(self, current):
        if current > self.LOCKDOWN and not self.current_lockdown:
            current = current - self.LOCKDOWN
            print(self.name + ": is in lockdown")
            self.current_lockdown = True
        else:
            if self.current_lockdown and current > self.LOCKDOWN:
                current = current - self.LOCKDOWN
                print(self.name + ": Lockdown has been lifted")
                self.current_lockdown = False
            elif self.current_lockdown:
                print("Unable to lift lockdown")
            else:
                print("Unable to start lockdown")
        return current
