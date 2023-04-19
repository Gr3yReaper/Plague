import diseaseGrowth
import pygame
from Country import *
from AirPort import *
import keyToUpgrade
from Upgrades.Upgrade import StatIncrease


def update_countries(countries, stats):
    while len(stats) != 0:
        if stats[0] == StatIncrease.Protective:
            for x in range(len(countries)):
                new_value = countries[x].get_protective() + stats[1]
                new_value = round(new_value, 1)
                countries[x].update_protective(new_value)
        elif stats[0] == StatIncrease.Awareness:
            for x in range(len(countries)):
                new_value = countries[x].get_awareness() + stats[1]
                new_value = round(new_value, 2)
                countries[x].update_awareness(new_value)
        elif stats[0] == "airport":
            list_affected = stats[1]
            # True means trying to open airports
            if stats[2]:
                for x in range(len(countries)):
                    if countries[x] in list_affected:
                        current = countries[x].get_activity()
                        if current == Activity.AIRPORT_RESTRICTIONS:
                            countries[x].update_activity(Activity.UNRESTRICTED)
                        elif current == Activity.BOTH_RESTRICTED:
                            countries[x].update_activity(Activity.LAND_RESTRICTIONS)
                        elif current == Activity.LOCKDOWN:
                            countries[x].update_activity(Activity.BOTH_RESTRICTED)
            # Else try to close
            else:
                for x in range(len(countries)):
                    if countries[x] in list_affected:
                        current = countries[x].get_activity()
                        if current == Activity.UNRESTRICTED:
                            countries[x].update_activity(Activity.AIRPORT_RESTRICTIONS)
                        elif current == Activity.LAND_RESTRICTIONS:
                            countries[x].update_activity(Activity.BOTH_RESTRICTED)
            stats.pop(2)
        elif stats[0] == "land":
            list_affected = stats[1]
            if stats[2]:
                for x in range(len(countries)):
                    if countries[x] in list_affected:
                        current = countries[x].get_activity()
                        if current == Activity.LAND_RESTRICTIONS:
                            countries[x].update_activity(Activity.UNRESTRICTED)
                        elif current == Activity.BOTH_RESTRICTED:
                            countries[x].update_activity(Activity.AIRPORT_RESTRICTIONS)
                        elif current == Activity.LOCKDOWN:
                            countries[x].update_activity(Activity.BOTH_RESTRICTED)
            else:
                for x in range(len(countries)):
                    if countries[x] in list_affected:
                        current = countries[x].get_activity()
                        if current == Activity.AIRPORT_RESTRICTIONS:
                            countries[x].update_activity(Activity.BOTH_RESTRICTED)
                        elif current == Activity.UNRESTRICTED:
                            countries[x].update_activity(Activity.LAND_RESTRICTIONS)
            stats.pop(2)
        elif stats[0] == "lockdown":
            list_affected = stats[1]
            lockdown_stats = stats[2]
            if lockdown_stats[0]:
                for x in range(len(countries)):
                    if countries[x] in list_affected:
                        if lockdown_stats[1] and lockdown_stats[2]:
                            countries[x].update_activity(Activity.BOTH_RESTRICTED)
                        elif lockdown_stats[1] and not lockdown_stats[2]:
                            countries[x].update_activity(Activity.AIRPORT_RESTRICTIONS)
                        elif lockdown_stats[2] and not lockdown_stats[1]:
                            countries[x].update_activity(Activity.LAND_RESTRICTIONS)
                        else:
                            countries[x].update_activity(Activity.UNRESTRICTED)
            else:
                for x in range(len(countries)):
                    if countries[x] in list_affected:
                        countries[x].update_activity(Activity.LOCKDOWN)
            stats.pop(2)
        stats.pop(1)
        stats.pop(0)
    return countries


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
                                             n.get_awareness(), n.get_protective(),
                                             n.get_medical().value) for n in countries]
        # Modified algorithm to add people as infected
        for x in range(len(countries)):
            total_infected = new_infected[x] + countries[x].get_infected()
            if total_infected > countries[x].get_able_to_be_infected():
                new_infected[x] = countries[x].get_able_to_be_infected() - countries[x].get_infected()
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
        print([n.get_name() + ": " + str(n.get_infected()) for n in countries])

        for event in pygame.event.get():
            # This method checks if the event is a pressing of a key (any key)
            keys = pygame.key.get_pressed()
            upgrade_chosen = False
            upgrade_keys = []
            tokens_before = tokens
            if keys[pygame.K_EQUALS]:
                print("Simulation ended")
                return
            elif keys[pygame.K_1] and keys[pygame.K_l]:
                if UPGRADE_LIST[35].get_unlocked():
                    tokens = UPGRADE_LIST[35].close_land_access(tokens)
                    closed_land = UPGRADE_LIST[35].get_land_closed()
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[35].get_affected_countries()
                        stats = ["land", list_countries, closed_land]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_1] and keys[pygame.K_f]:
                if UPGRADE_LIST[35].get_unlocked():
                    closed_airports = UPGRADE_LIST[35].get_airports_closed()
                    tokens = UPGRADE_LIST[35].close_air_access(tokens)
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[35].get_affected_countries()
                        stats = ["airport", list_countries, closed_airports]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_1] and keys[pygame.K_e]:
                if UPGRADE_LIST[35].get_unlocked():
                    lockdown_stats = UPGRADE_LIST[35].get_lockdown()
                    tokens = UPGRADE_LIST[35].lockdown(tokens)
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[35].get_affected_countries()
                        stats = ["lockdown", list_countries, lockdown_stats]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_2] and keys[pygame.K_l]:
                if UPGRADE_LIST[36].get_unlocked():
                    tokens = UPGRADE_LIST[36].close_land_access(tokens)
                    closed_land = UPGRADE_LIST[36].get_land_closed()
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[36].get_affected_countries()
                        stats = ["land", list_countries, closed_land]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_2] and keys[pygame.K_f]:
                if UPGRADE_LIST[36].get_unlocked():
                    closed_airports = UPGRADE_LIST[36].get_airports_closed()
                    tokens = UPGRADE_LIST[36].close_air_access(tokens)
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[36].get_affected_countries()
                        stats = ["airport", list_countries, closed_airports]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_2] and keys[pygame.K_e]:
                if UPGRADE_LIST[36].get_unlocked():
                    lockdown_stats = UPGRADE_LIST[36].get_lockdown()
                    tokens = UPGRADE_LIST[36].lockdown(tokens)
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[36].get_affected_countries()
                        stats = ["lockdown", list_countries, lockdown_stats]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_3] and keys[pygame.K_l]:
                if UPGRADE_LIST[37].get_unlocked():
                    tokens = UPGRADE_LIST[37].close_land_access(tokens)
                    closed_land = UPGRADE_LIST[37].get_land_closed()
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[37].get_affected_countries()
                        stats = ["land", list_countries, closed_land]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_3] and keys[pygame.K_f]:
                if UPGRADE_LIST[37].get_unlocked():
                    closed_airports = UPGRADE_LIST[37].get_airports_closed()
                    tokens = UPGRADE_LIST[37].close_air_access(tokens)
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[37].get_affected_countries()
                        stats = ["airport", list_countries, closed_airports]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_3] and keys[pygame.K_e]:
                if UPGRADE_LIST[37].get_unlocked():
                    lockdown_stats = UPGRADE_LIST[37].get_lockdown()
                    tokens = UPGRADE_LIST[37].lockdown(tokens)
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[37].get_affected_countries()
                        stats = ["lockdown", list_countries, lockdown_stats]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_4] and keys[pygame.K_l]:
                if UPGRADE_LIST[38].get_unlocked():
                    tokens = UPGRADE_LIST[38].close_land_access(tokens)
                    closed_land = UPGRADE_LIST[38].get_land_closed()
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[38].get_affected_countries()
                        stats = ["land", list_countries, closed_land]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_4] and keys[pygame.K_f]:
                if UPGRADE_LIST[38].get_unlocked():
                    closed_airports = UPGRADE_LIST[38].get_airports_closed()
                    tokens = UPGRADE_LIST[38].close_air_access(tokens)
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[38].get_affected_countries()
                        stats = ["airport", list_countries, closed_airports]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_4] and keys[pygame.K_e]:
                if UPGRADE_LIST[38].get_unlocked():
                    lockdown_stats = UPGRADE_LIST[38].get_lockdown()
                    tokens = UPGRADE_LIST[38].lockdown(tokens)
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[38].get_affected_countries()
                        stats = ["lockdown", list_countries, lockdown_stats]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_q] and keys[pygame.K_l]:
                if UPGRADE_LIST[34].get_unlocked():
                    tokens = UPGRADE_LIST[34].close_land_access(tokens)
                    closed_land = UPGRADE_LIST[34].get_land_closed()
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[34].get_affected_countries()
                        stats = ["land", list_countries, closed_land]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_q] and keys[pygame.K_f]:
                if UPGRADE_LIST[34].get_unlocked():
                    closed_airports = UPGRADE_LIST[34].get_airports_closed()
                    tokens = UPGRADE_LIST[34].close_air_access(tokens)
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[34].get_affected_countries()
                        stats = ["airport", list_countries, closed_airports]
                        countries = update_countries(countries, stats)
                    break
            elif keys[pygame.K_q] and keys[pygame.K_e]:
                if UPGRADE_LIST[34].get_unlocked():
                    lockdown_stats = UPGRADE_LIST[34].get_lockdown()
                    tokens = UPGRADE_LIST[34].lockdown(tokens)
                    if tokens != tokens_before:
                        list_countries = UPGRADE_LIST[34].get_affected_countries()
                        stats = ["lockdown", list_countries, lockdown_stats]
                        countries = update_countries(countries, stats)
                    break
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
            elif keys[pygame.K_p] and keys[pygame.K_1]:
                upgrade_keys = ['p', 1]
            elif keys[pygame.K_q] and keys[pygame.K_1]:
                upgrade_keys = ['q', 1]
            elif keys[pygame.K_q] and keys[pygame.K_2]:
                upgrade_keys = ['q', 2]
            elif keys[pygame.K_q] and keys[pygame.K_3]:
                upgrade_keys = ['q', 3]
            elif keys[pygame.K_q] and keys[pygame.K_4]:
                upgrade_keys = ['q', 4]
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
            elif keys[pygame.K_3]:
                upgrade_keys = [3]
            elif keys[pygame.K_4]:
                upgrade_keys = [4]
            elif keys[pygame.K_5]:
                upgrade_keys = [5]
            elif keys[pygame.K_6]:
                upgrade_keys = [6]
            elif keys[pygame.K_7]:
                upgrade_keys = [7]
            elif keys[pygame.K_8]:
                upgrade_keys = [8]
            elif keys[pygame.K_p]:
                upgrade_keys = ['p']
            elif keys[pygame.K_9]:
                upgrade_keys = [9]
            elif keys[pygame.K_z]:
                upgrade_keys = ['z']
            elif keys[pygame.K_x]:
                upgrade_keys = ['x']
            elif keys[pygame.K_c]:
                upgrade_keys = ['c']
            elif keys[pygame.K_v]:
                upgrade_keys = ['v']
            elif keys[pygame.K_b]:
                upgrade_keys = ['b']
            elif keys[pygame.K_m]:
                upgrade_keys = ['m']
            elif keys[pygame.K_s]:
                upgrade_keys = ['s']
            elif keys[pygame.K_d]:
                upgrade_keys = ['d']
            elif keys[pygame.K_f]:
                upgrade_keys = ['f']
            elif keys[pygame.K_g]:
                upgrade_keys = ['g']
            elif keys[pygame.K_h]:
                upgrade_keys = ['h']
            elif keys[pygame.K_q]:
                upgrade_keys = ['q']

            #countries[0].update_activity(Activity.RESTRICTED)

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
                    elif upgrades_to_apply[0] == StatIncrease.Fatality_Rate:
                        fatality_rate = fatality_rate + upgrades_to_apply[1]
                    elif upgrades_to_apply[0] == StatIncrease.Authority:
                        authority = authority * upgrades_to_apply[1]
                        if authority > 100:
                            authority = 100
                        else:
                            authority = round(authority, 1)
                    elif upgrades_to_apply[0] == StatIncrease.Non_Compliance:
                        non_compliance = non_compliance - upgrades_to_apply[1]
                        # Need to explore how to actually implement
                    elif upgrades_to_apply[0] == StatIncrease.Protective:
                        # Call a method to change all countries protective value
                        stat_list = [StatIncrease.Protective, upgrades_to_apply[1]]
                        countries = update_countries(countries, stat_list)
                    elif upgrades_to_apply[0] == StatIncrease.Awareness:
                        stat_list = [StatIncrease.Awareness, upgrades_to_apply[1]]
                        countries = update_countries(countries, stat_list)
                    else:
                        print("Different upgrade from research")
                    upgrades_to_apply.pop(1)
                    upgrades_to_apply.pop(0)

        # Token acquisition system, crude and needs more added to it.

        tokens = tokens + 0.2 # Might need to be increased
        research = research + research_speed # 0.1 is base speed
        research = round(research, 1)
        tokens = round(tokens, 1)
        print("Current tokens are: " + str(tokens))
        print("Research is at: " + str(research))
        print("Authority is at: " + str(authority))
        print("Fatality is at: " + str(fatality_rate))
        print()
        clock.tick(10)
