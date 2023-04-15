from Upgrades.Upgrade import *


class Operation(Upgrade):

    def __int__(self, name, description, cost, stats, requirements):
        super().__init__(name, description, cost, stats, requirements)

