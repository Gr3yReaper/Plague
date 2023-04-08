from Upgrades.Upgrade import *
from enum import Enum


class Quarantine(Upgrade):

    def __init__(self, name, description, cost, affected_countries, effect, requirements):
        super().__init__(name, description, cost, effect, requirements)
        self.affected_countries = affected_countries

    def action(self):
        for i in range(len(self.stats)) :
            print("Area has been quarantined")
