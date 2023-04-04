from Upgrades.Upgrade import *


class Operation(Upgrade):

    def __int__(self, name, description, cost, stats, requirements):
        super().__init__(name, description, cost, stats, requirements)

    def action(self):
        for i in range(len(self.stats)) :
            if self.stats == StatIncrease.Infection_Rate:
                print("Global reduction for infection rates")
            elif self.stats == StatIncrease.Fatality_Rate:
                print("Global reduction for fatality rates")
            elif self.stats == StatIncrease.Research_Speed:
                print("Research speed has been increased")
            elif self.stats == StatIncrease.Authority:
                print("Authority has been increased")
            else:
                print("Unknown increase")

