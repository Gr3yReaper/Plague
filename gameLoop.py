import diseaseGrowth
import pygame
from Country import *
from AirPort import *


def run(countries, airport_list, airport_countries, UPGRADE_LIST, bought_upgrades, tokens):
    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((300, 300))
    research = 0

    for x in bought_upgrades:
        print("Upgrade has been applied")

    while research < 100 and not any([n.get_infected() >= 1000000 for n in countries]):
        # Calculates the new infected numbers for each country then updates the objects
        # Work out rough chance of said airport travelling, randomly pick location etc
        # At 1 million should have 5% research without any other upgrades.
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
                        tokens = tokens + 1
                        print("Plane left: " + airport_countries[x] + ", Headed for: " + countries[y].get_name())

        # One airport/ boat per country for now
        # Random chance one will start (pick a random country with a free port/ airport
        # around 0.8% when unaware, 0.5 when slight, 0.3 when aware, 0.1 when reduced, and 0 for lockdown rough values
        print([n.get_infected() for n in countries])
        for event in pygame.event.get():
            # This method checks if the event is a pressing of a key (any key)

            if event.type == pygame.KEYDOWN:
                # This then elaborates it further by checking for the specific key pressed.
                tokens_before = tokens
                if event.key == pygame.K_0:
                    tokens = UPGRADE_LIST[0].purchase(tokens)
                    upgrade_bought = 0

                    # print("You have " + str(tokens) + " left")
                    # airport_list = "" using this can shut down airports
                elif event.key == pygame.K_1:
                    tokens = UPGRADE_LIST[1].purchase(tokens)
                    upgrade_bought = 1
                elif event.key == pygame.K_2:
                    tokens = UPGRADE_LIST[2].purchase(tokens)
                    upgrade_bought = 2
                elif event.key == pygame.K_3:
                    tokens = UPGRADE_LIST[3].purchase(tokens)
                    upgrade_bought = 3
                else:
                    print("a key has been pressed")
                    countries[0].update_activity(Activity.RESTRICTED)
                if tokens_before != tokens:
                    bought_upgrades.append(UPGRADE_LIST[upgrade_bought])
                    UPGRADE_LIST[upgrade_bought].action()
        # Token acquisition system, crude and needs more added to it.
        tokens = tokens + 0.2 #Might need to be increased
        research = research + 0.1
        research = round(research, 1)
        tokens = round(tokens, 1)
        print(tokens)
        print(bought_upgrades)
        clock.tick(10)
