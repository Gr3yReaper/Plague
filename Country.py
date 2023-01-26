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


class Country:
    def __init__(self, name, population, infected, activity, awareness):
        self.name = name
        self.population = population
        self.infected = infected
        self.activity = activity
        self.awareness = awareness

    def getName(self):
        return self.name

    def getInfected(self):
        return self.infected

    def getPopulation(self):
        return self.population

    def getActivity(self):
        return self.activity

    def getAwareness(self):
        return self.awareness

    def updateInfected(self, infected):
        self.infected = infected

    def updatePopulation(self, population):
        self.population = population

    def updateActivity(self, activity):
        self.activity = activity

    def updateAwareness(self, awareness):
        self.awareness = awareness
