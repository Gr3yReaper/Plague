import diseaseGrowth
import pygame
from Country import *
from AirPort import *


def run(countries, airport_list, airport_countries):
    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((300, 300))

    while not any([n.get_infected() >= 1000000 for n in countries]):
        # Calculates the new infected numbers for each country then updates the objects
        # Work out rough chance of said airport travelling, randomly pick location etc
        flight_log = ([n.get_airport().flight(n.get_infected()) for n in airport_list])
        new_infected = [diseaseGrowth.update(n.get_infected(), n.get_activity().value,
                                             n.get_awareness().value, n.get_protective().value,
                                             n.get_medical().value) for n in countries]
        # Modified algorithm to add people as infected
        for x in range(len(countries)):
            countries[x].update_infected(new_infected[x])

        for x in range(len(flight_log)):
            if flight_log[x] is not None:
                for y in range(len(countries)):
                    if countries[y].get_name() == flight_log[x] and countries[y].get_infected() == 0:
                        countries[y].update_infected(1)  # Set as 1 for now to start infection
                        print("Plane left: " + airport_countries[x] + ", Headed for: " + countries[y].get_name())

        # One airport/ boat per country for now
        # Random chance one will start (pick a random country with a free port/ airport
        # around 0.8% when unaware, 0.5 when slight, 0.3 when aware, 0.1 when reduced, and 0 for lockdown rough values
        print([n.get_infected() for n in countries])
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print("a key has been pressed")
                # airport_list = "" using this can shut down airports
                countries[0].update_activity(Activity.RESTRICTED)
        clock.tick(10)
