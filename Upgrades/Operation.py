from Upgrades.Upgrade import *


class Operation(Upgrade):

    def __int__(self, name, description, cost, stats, requirements):
        super().__init__(name, description, cost, stats, requirements)

    def action(self, research_speed):
        i = 0

        while i < len(self.stats):
            if self.stats[i] == "research":
                print("Research has now started")
            elif self.stats[i] == "research_speed":
                print("Research speed has been increased")
                research_speed = research_speed + self.stats[i + 1]
            elif self.stats[i] == StatIncrease.Infection_Rate:
                print("Global reduction for infection rates")
            elif self.stats[i] == StatIncrease.Fatality_Rate:
                print("Global reduction for fatality rates")
            elif self.stats[i] == StatIncrease.Research_Speed:
                print("Research speed has been increased")
            elif self.stats[i] == StatIncrease.Authority:
                print("Authority has been increased")
            else:
                print("Unknown increase")
            i = i + 2

        return research_speed
