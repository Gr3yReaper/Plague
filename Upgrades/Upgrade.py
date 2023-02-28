from enum import Enum


class Category(Enum):
    Quarantine = 1
    Response = 2
    Operation = 3
    Unique = 4


class StatIncrease(Enum):
    Infection_Rate = 1
    Research_Speed = 2
    Fatality_Rate = 3
    Authority = 4
    # Unsure if Authority and non-compliance should be different


class Upgrade:
    def __init__(self, name, category, description, cost, stats):
        self.name = name
        self.category = category
        self.description = description
        self.cost = cost
        # stats are which attributes are affected by an upgrade
        self.stats = stats
        self.unlocked = False

    def get_name(self):
        return self.name

    def get_category(self):
        return self.category

    def get_description(self):
        return self.description

    def get_cost(self):
        return self.cost

    def get_unlocked(self):
        return self.unlocked

    def get_stats(self):
        return self.stats

    def set_name(self, name):
        self.name = name

    def set_category(self, category):
        self.category = category

    def set_description(self, description):
        self.description = description

    def set_cost(self, cost):
        self.cost = cost

    # this method is for testing

    def set_unlocked(self, unlocked):
        self.unlocked = unlocked

    def purchase(self, current):
        if self.cost > current:
            print("Insufficient credits, did not buy upgrade")
        else:
            print("Upgrade unlocked")
            current = current - self.cost
            self.unlocked = True
        return current

    def sell(self, current):
        if self.unlocked:
            current = current + self.cost
            self.unlocked = False
            print("Upgrade has been sold")
        else:
            print("Failure as upgrade has not been purchased")
        return current



