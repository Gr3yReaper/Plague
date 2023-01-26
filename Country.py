from enum import Enum


class Activity(Enum):
    UNAWARE = 2
    SLIGHT = 1.5
    AWARE = 1
    REDUCED = 0.5
    LOCKDOWN = 0


class Country:
    def __init__(self, name, population, infected, activity):
        self.name = name
        self.population = population
        self.infected = infected
        self.activity = activity

    def getName(self):
        return self.name

    def getInfected(self):
        return self.infected

    def getPopulation(self):
        return self.population

    def getActivity(self):
        return self.activity

    def updateInfected(self, infected):
        self.infected = infected

    def updatePopulation(self, population):
        self.population = population

    def updateActivity(self, activity):
        self.activity = activity
