from enum import Enum


class StatIncrease(Enum):
    # Corresponding base values for increase.
    Infection_Rate = 10 #Change later
    Protective = 0.4
    Awareness = 0.3
    Research_Speed = 0.1
    Fatality_Rate = -5
    Authority = 1
    Non_Compliance = 5


class Upgrade:
    def __init__(self, name, description, cost, stats, requirements):
        self.name = name
        self.description = description
        self.cost = cost
        # stats are which attributes are affected by an upgrade
        self.stats = stats
        self.requirements = requirements
        self.unlocked = False

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_cost(self):
        return self.cost

    def get_unlocked(self):
        return self.unlocked

    def get_stats(self):
        return self.stats

    def get_requirements(self):
        return self.requirements

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def set_cost(self, cost):
        self.cost = cost

    # this method is for testing

    def set_unlocked(self, unlocked):
        self.unlocked = unlocked

    def purchase(self, current, current_upgrades):
        requirements_met = False
        if len(self.requirements) == 0:
            requirements_met = True
        else:
            for x in current_upgrades:
                for y in self.requirements:
                    if x.get_name() == y:
                        requirements_met = True
                        break

        if self.cost > current:
            print("Insufficient credits, did not buy upgrade")
        elif self.unlocked:
            print("Upgrade already unlocked")
        elif not requirements_met:
            print("Need to purchase upgrades before this one")
        else:
            print("Upgrade: " + self.name + " unlocked")
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

    def action(self):
        upgrades = []
        i = 0

        while i < len(self.stats):
            value = 0
            if self.stats[i] == "research":
                print("Research has now started")
            elif self.stats[i] == StatIncrease.Protective:
                print("Update all countries in terms of protective equipment")
                value = self.stats[i + 1] * StatIncrease.Protective.value
                upgrades.append(StatIncrease.Protective)
            elif self.stats[i] == StatIncrease.Non_Compliance:
                print("Non-compliance has been reduced")
                value = self.stats[i + 1] * StatIncrease.Non_Compliance.value
                upgrades.append(StatIncrease.Non_Compliance)
            elif self.stats[i] == StatIncrease.Fatality_Rate:
                value = self.stats[i + 1] * StatIncrease.Fatality_Rate.value
                upgrades.append(StatIncrease.Fatality_Rate)
            elif self.stats[i] == StatIncrease.Research_Speed:
                print("Research speed has been increased")
                value = self.stats[i + 1] * StatIncrease.Research_Speed.value
                upgrades.append(StatIncrease.Research_Speed)
            elif self.stats[i] == StatIncrease.Authority:
                print("Authority has been increased")
                value = self.stats[i+1] * StatIncrease.Authority.value
                upgrades.append(StatIncrease.Authority)
            elif self.stats[i] == StatIncrease.Awareness:
                print("Global awareness for disease has been increased")
                value = self.stats[i+1] * StatIncrease.Awareness.value
                upgrades.append(StatIncrease.Awareness)

            if value != 0:
                upgrades.append(value)
            i = i + 2

        return upgrades
    