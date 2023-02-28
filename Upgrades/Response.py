import Upgrade
from Upgrade import *
from enum import Enum


class SubCategory(Enum):
    Infection_Prevention = 1
    Death_Prevention = 2
    Contact_Tracing = 3
    Border_Monitoring = 4


class Response(Upgrade):
    def __init__(self, name, category, description, cost, sub_category, stats):
        super().__init__(name, category, description, cost, stats)
        self.sub_category = sub_category

    def get_sub_category(self):
        return self.sub_category

    def set_sub_category(self, sub):
        self.sub_category = sub

    def action(self):
        for i in range(len(self.stats)):
            if self.stats == StatIncrease.Infection_Rate:
                print("Global reduction for infection rates")
