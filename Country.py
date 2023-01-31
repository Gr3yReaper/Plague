from enum import Enum


class Activity(Enum):
    UNRESTRICTED = 2
    SLIGHT = 1.5
    LOW_RESTRICTION = 1
    RESTRICTED = 0.5
    LOCKDOWN = 0


class Awareness(Enum):
    UNAWARE = 0.5
    SLIGHT = 0.6
    SOME = 0.7
    MOST = 0.8
    HEAVILY = 0.9
    ALL = 1.0


class Protective(Enum):
    NONE = 0.0
    LITTLE = 0.2
    MODERATE = 0.3
    HEAVY = 0.4
    MANDATORY = 0.5


class Medical(Enum):
    POOR = 0.1
    FEW = 0.2
    MODERATE = 0.3
    MIDDLE = 0.4
    ADVANCED = 0.5
    HIGH = 0.6
    MASSIVE = 0.7


class Country:
    def __init__(self, name, population, infected, activity, awareness, protective, medical):
        self.name = name
        self.population = population
        self.infected = infected
        self.activity = activity
        self.awareness = awareness
        self.protective = protective
        self.medical = medical

    def get_name(self):
        return self.name

    def get_infected(self):
        return self.infected

    def get_population(self):
        return self.population

    def get_activity(self):
        return self.activity

    def get_awareness(self):
        return self.awareness

    def get_protective(self):
        return self.protective

    def get_medical(self):
        return self.medical

    def update_infected(self, infected):
        self.infected = infected

    def update_population(self, population):
        self.population = population

    def update_activity(self, activity):
        self.activity = activity

    def update_awareness(self, awareness):
        self.awareness = awareness

    def update_protective(self, protective):
        self.protective = protective

    def update_medical(self, medical):
        self.medical = medical
