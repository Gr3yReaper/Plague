# This class needs to be the same as gameLoop but instead use if statements to make decisions
import diseaseGrowth
import pygame
import random
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


def upgrade_builder(bought_upgrades, UPGRADE_LIST, goal_upgrade):
    result = [0, []]
    if goal_upgrade in bought_upgrades:
        # Returns empty as have the upgrade
        return result
    else:
        requirements = goal_upgrade.get_requirements()
        upgrade_req = []
        # Convert requirements string to upgrade
        while len(requirements) != 0:
            for x in UPGRADE_LIST:
                if requirements[0] == x.get_name():
                    upgrade_req.append(x)
                    requirements.pop(0)
                    break
        if len(upgrade_req) == 2:
            lhs = upgrade_builder(bought_upgrades, UPGRADE_LIST, upgrade_req[0])
            rhs = upgrade_builder(bought_upgrades, UPGRADE_LIST, upgrade_req[1])
            if lhs[0] < rhs[0]:
                result = lhs
                result[0] = result[0] + upgrade_req[0].get_cost()
                result[1].append(upgrade_req[0])
            else:
                result = rhs
                result[0] = result[0] + upgrade_req[1].get_cost()
                result[1].append(upgrade_req[1])
        if len(upgrade_req) == 1:
            result = upgrade_builder(bought_upgrades, UPGRADE_LIST, upgrade_req[0])
            result[0] = result[0] + upgrade_req[0].get_cost()
            result[1].append(upgrade_req[0])
        return result


def run(countries, airport_list, airport_countries, UPGRADE_LIST, bought_upgrades, tokens, authority, non_compliance,
        fatality_rate):

    pygame.init()
    clock = pygame.time.Clock()
    research = 0
    research_speed = 0
    current_authority_upgrade = 11
    current_research_upgrade = keyToUpgrade.key_conversion('r')
    new_upgrades = "none"
    purch_planned_upgrades = "none"
    planned_upgrades = []

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
        tokens = tokens + 0.2
        # Creation of AI

        if not UPGRADE_LIST[0].get_unlocked() and tokens >= UPGRADE_LIST[0].get_cost():
            tokens = UPGRADE_LIST[0].purchase(tokens, bought_upgrades)
            new_upgrades = 0
        elif authority < 85 and tokens >= UPGRADE_LIST[current_authority_upgrade].get_cost() and current_authority_upgrade < 14:
            tokens = UPGRADE_LIST[current_authority_upgrade].purchase(tokens, bought_upgrades)
            new_upgrades = current_authority_upgrade
            current_authority_upgrade = current_authority_upgrade + 1
        elif len(planned_upgrades) != 0:
            if tokens >= planned_upgrades[0].get_cost():
                if not planned_upgrades[0].get_unlocked():
                    tokens = planned_upgrades[0].purchase(tokens, bought_upgrades)
                    purch_planned_upgrades = planned_upgrades[0]
                planned_upgrades.pop(0)
        else:
            # This in only taken if the AI doesn't have a plan yet
            if tokens >= UPGRADE_LIST[current_research_upgrade].get_cost() and \
                    current_research_upgrade < (keyToUpgrade.key_conversion('r') + 4):
                tokens = UPGRADE_LIST[current_research_upgrade].purchase(tokens, bought_upgrades)
                new_upgrades = current_research_upgrade
                current_research_upgrade = current_research_upgrade + 1
            else:
                decided_upgrade = random.randint(1, len(UPGRADE_LIST) - 1)
                while decided_upgrade == 11 or decided_upgrade == 12 or decided_upgrade == 13 or UPGRADE_LIST[decided_upgrade].get_unlocked():
                    decided_upgrade = random.randint(1, len(UPGRADE_LIST) - 1)
                planned_upgrades = upgrade_builder(bought_upgrades, UPGRADE_LIST, UPGRADE_LIST[decided_upgrade])
                planned_upgrades = planned_upgrades[1]
                planned_upgrades.append(UPGRADE_LIST[decided_upgrade])

        if new_upgrades != "none":
            upgrades_to_apply = UPGRADE_LIST[new_upgrades].action()
            bought_upgrades.append(UPGRADE_LIST[new_upgrades])
            new_upgrades = "none"

        if purch_planned_upgrades != "none":
            upgrades_to_apply = purch_planned_upgrades.action()
            bought_upgrades.append(purch_planned_upgrades)
            purch_planned_upgrades = "none"

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

        research = research + research_speed # 0.1 is base speed
        research = round(research, 1)
        tokens = round(tokens, 1)
        print("Current tokens are: " + str(tokens))
        print("Research is at: " + str(research))
        print("Authority is at: " + str(authority))
        print("Fatality is at: " + str(fatality_rate))
        print()
        clock.tick(8)
    return [countries, authority, research, bought_upgrades]
