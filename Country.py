from enum import Enum
from queue import Queue
from AirPort import *


class Activity(Enum):
    UNRESTRICTED = 1.5
    SLIGHT = 1.2
    LOW_RESTRICTION = 0.8
    RESTRICTED = 0.5
    LOCKDOWN = 0

# These numbers will need to be tweaked, at the moment highest division is 2.2, maybe can adjust based on infected value
# for testing though it is fine.


class Awareness(Enum):
    UNAWARE = 0.5
    SLIGHT = 0.6
    SOME = 0.7
    MOST = 0.8
    HEAVILY = 0.9
    ALL = 1.0


class Medical(Enum):
    POOR = 0.1
    FEW = 0.2
    MODERATE = 0.3
    MIDDLE = 0.4
    ADVANCED = 0.5
    HIGH = 0.6
    MASSIVE = 0.7


PERIOD = 14  # How long until no longer positive
Immunity = 20


class Country:
    def __init__(self, name, population, infected, activity, awareness, protective, medical):
        self.name = name
        self.population = population
        self.infected = infected
        self.activity = activity
        self.awareness = awareness
        self.protective = protective
        self.medical = medical
        self.history = Queue(maxsize=PERIOD)
        self.history.put(infected)
        self.airport = None
        self.able_to_be_infected = population
        self.immune_queue = Queue(maxsize=Immunity)

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

    def get_airport(self):
        return self.airport

    def get_able_to_be_infected(self):
        return self.able_to_be_infected

    def update_infected(self, infected):
        self.infected = self.infected + infected
        if self.history.full():
            not_infected = self.history.get()
            self.history.put(infected)
            self.infected = self.infected - not_infected
            self.update_immune(not_infected)
        else:
            self.history.put(infected)

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

    def set_airport(self, airport):
        self.airport = airport

    def update_immune(self, immunity):
        self.able_to_be_infected = self.able_to_be_infected - immunity
        if self.immune_queue.full():
            not_immune = self.immune_queue.get()
            self.immune_queue.put(immunity)
            self.able_to_be_infected = self.able_to_be_infected + not_immune
        else:
            self.immune_queue.put(immunity)

