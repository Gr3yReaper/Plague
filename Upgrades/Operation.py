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
            elif self.stats[i] == StatIncrease.Protective:
                print("Update all countries in terms of protective equipment")
                protective = self.stats[i + 1] * StatIncrease.Protective.value
                upgrades.append(StatIncrease.Protective)
                upgrades.append(protective)
            elif self.stats[i] == StatIncrease.Non_Compliance:
                print("Non-compliance has been reduced")
                non_compliance = self.stats[i + 1] * StatIncrease.Non_Compliance.value
                upgrades.append(StatIncrease.Non_Compliance)
                upgrades.append(non_compliance)
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
                authority = self.stats[i+1] * StatIncrease.Authority.value
                upgrades.append(StatIncrease.Authority)
                upgrades.append(authority)
            i = i + 2

        return upgrades
