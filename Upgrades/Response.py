from Upgrades.Upgrade import *
from enum import Enum


class SubCategory(Enum):
    Infection_Prevention = 1
    Death_Prevention = 2
    Contact_Tracing = 3
    Border_Monitoring = 4


class Response(Upgrade):
    def __init__(self, name, description, cost, sub_category, stats, requirements):
        super().__init__(name, description, cost, stats, requirements)
        self.sub_category = sub_category

    def get_sub_category(self):
        return self.sub_category

    def set_sub_category(self, sub):
        self.sub_category = sub
