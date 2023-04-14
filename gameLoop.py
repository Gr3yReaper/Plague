import diseaseGrowth
import pygame
from Country import *
from AirPort import *
import keyToUpgrade
from Upgrades.Upgrade import StatIncrease


def run(countries, airport_list, airport_countries, UPGRADE_LIST, bought_upgrades, tokens, authority, non_compliance,
        fatality_rate):

    pygame.init()
    clock = pygame.time.Clock()
    display = pygame.display.set_mode((300, 300))
    research = 0
    research_speed = 0

    for x in bought_upgrades:
        print("Upgrade " + x.get_name() + " been applied")

    while authority > 0 and research < 100:
        # Calculates the new infected numbers for each country then updates the objects
        # Work out rough chance of said airport travelling, randomly pick location etc
        # At 1 million should have 5% research without any other upgrades.
        upgrades_to_apply = []
        flight_log = ([n.get_airport().flight(n.get_infected()) for n in airport_list])
        new_infected = [diseaseGrowth.update(n.get_infected(), n.get_activity().value,
                                             n.get_awareness().value, n.get_protective().value,
                                             n.get_medical().value) for n in countries]
        # Modified algorithm to add people as infected
        for x in range(len(countries)):
            countries[x].update_infected(new_infected[x])
            if (countries[x].get_population() * 0.00001) < new_infected[x]:
                authority = authority - 0.1
                authority = round(authority, 1)

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
            keys = pygame.key.get_pressed()
            upgrade_chosen = False
            upgrade_keys = []
            tokens_before = tokens
            if keys[pygame.K_EQUALS]:
                print("Simulation ended")
                return
            elif keys[pygame.K_r] and keys[pygame.K_1]:
                upgrade_keys = ['r', 1]
            elif keys[pygame.K_r] and keys[pygame.K_2]:
                upgrade_keys = ['r', 2]
            elif keys[pygame.K_r] and keys[pygame.K_3]:
                upgrade_keys = ['r', 3]
            elif keys[pygame.K_n] and keys[pygame.K_1]:
                upgrade_keys = ['n', 1]
            elif keys[pygame.K_n] and keys[pygame.K_2]:
                upgrade_keys = ['n', 2]
            elif keys[pygame.K_n] and keys[pygame.K_3]:
                upgrade_keys = ['n', 3]
            elif keys[pygame.K_a] and keys[pygame.K_1]:
                upgrade_keys = ['a', 1]
            elif keys[pygame.K_n] and keys[pygame.K_2]:
                upgrade_keys = ['a', 2]
            elif keys[pygame.K_0]:
                upgrade_keys = [0]
            elif keys[pygame.K_1]:
                upgrade_keys = [1]
            elif keys[pygame.K_2]:
                upgrade_keys = [2]
            elif keys[pygame.K_r]:
                upgrade_keys = ['r']
            elif keys[pygame.K_n]:
                upgrade_keys = ['n']
            elif keys[pygame.K_a]:
                upgrade_keys = ['a']
            else:
                print("a key has been pressed")
                countries[0].update_activity(Activity.RESTRICTED)

            if len(upgrade_keys) == 1:
                upgrade_number = keyToUpgrade.key_conversion(upgrade_keys[0])
                upgrade_chosen = True
            elif len(upgrade_keys) == 2:
                upgrade_number = keyToUpgrade.key_conversion(upgrade_keys[0]) + upgrade_keys[1]
                upgrade_chosen = True
            if upgrade_chosen:
                print(upgrade_number)
                tokens = UPGRADE_LIST[upgrade_number].purchase(tokens, bought_upgrades)
                upgrade_bought = upgrade_number

            if tokens_before != tokens:
                bought_upgrades.append(UPGRADE_LIST[upgrade_bought])
                upgrades_to_apply = UPGRADE_LIST[upgrade_bought].action()

            if len(upgrades_to_apply) != 0:
                while len(upgrades_to_apply) != 0:
                    if upgrades_to_apply[0] == StatIncrease.Research_Speed:
                        research_speed = research_speed + upgrades_to_apply[1]
                        upgrades_to_apply.pop(1)
                        upgrades_to_apply.pop(0)
                    elif upgrades_to_apply[0] == StatIncrease.Fatality_Rate:
                        fatality_rate = fatality_rate + upgrades_to_apply[1]
                        upgrades_to_apply.pop(1)
                        upgrades_to_apply.pop(0)
                    else:
                        print("Different upgrade from research")

        # Token acquisition system, crude and needs more added to it.

        tokens = tokens + 0.2 # Might need to be increased
        research = research + research_speed # 0.1 is base speed
        research = round(research, 1)
        tokens = round(tokens, 1)
        print(tokens)
        print(research)
        print("Authority is at: " + str(authority))
        print("Fatality is at: " + str(fatality_rate))
        clock.tick(10)
