from Upgrades.Upgrade import *


class Operation(Upgrade):

    def __int__(self, name, description, cost, stats, requirements):
        super().__init__(name, description, cost, stats, requirements)

    def action(self):
        upgrades = []
        i = 0

        while i < len(self.stats):
            if self.stats[i] == "research":
                print("Research has now started")
            elif self.stats[i] == "protective":
                print("Update all countries in terms of protective equipment")
            elif self.stats[i] == StatIncrease.Non_Compliance:
                print("Non-compliance has been reduced")
            elif self.stats[i] == StatIncrease.Infection_Rate:
                print("Global reduction for infection rates")
            elif self.stats[i] == StatIncrease.Fatality_Rate:
                fatality_rate = self.stats[i + 1] * StatIncrease.Fatality_Rate.value
                upgrades.append(StatIncrease.Fatality_Rate)
                upgrades.append(fatality_rate)
            elif self.stats[i] == StatIncrease.Research_Speed:
                print("Research speed has been increased")
                research_speed = self.stats[i + 1] * StatIncrease.Research_Speed.value
                upgrades.append(StatIncrease.Research_Speed)
                upgrades.append(research_speed)
            elif self.stats[i] == StatIncrease.Authority:
                print("Authority has been increased")
            else:
                print("Unknown increase")
            i = i + 2

        return upgrades
