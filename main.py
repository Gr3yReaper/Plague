from Country import *
from AirPort import *
from Upgrades.Response import *

import gameLoop
from threading import Thread

BASE_ACTIVITY = 20
AIRPORT_COUNTRIES = ["UK", "Russia", "Russia 2"]
AIRPORT_DETAILS = [["UK", ["Russia", "Russia 2"], BASE_ACTIVITY], ["Russia", ["UK", "Russia 2"], BASE_ACTIVITY],
                   ["Russia 2", [""], BASE_ACTIVITY]]

# Reduced list of upgrades will add more when needed
UPGRADE_LIST = ["RESPONSE", ["Hand Washing", "Reduces infection by promoting hand washing", 6,
                             SubCategory.Infection_Prevention, ["protective", 1]],
                            ["Public Awareness", "Promote personal responsibility for hygiene, reduces infection", 3,
                             SubCategory.Infection_Prevention, ["awareness", 1]],
                            ["Disinfectant Supplies", "Distribute bleach and cleaning supplies, reduce infection", 5,
                             SubCategory.Infection_Prevention, ["protective", 1]],
                            ["Self-Isolation", "Symptomatic people can not interact with others, reduce infection", 5,
                             SubCategory.Infection_Prevention, ["protective", 1]],
                            ["Social Distancing",
                             "People need to stay 2m away from each other, reduce infection, increased non-compliance",
                             9, SubCategory.Infection_Prevention, ["protective", 2, "non-compliance", 1]]
                ]

PORT_COUNTRIES = ["UK", "Russia"]

countries = [Country("UK", 6733000000, 1, Activity.SLIGHT, Awareness.SLIGHT,
                     Protective.LITTLE, Medical.HIGH),
             Country("Russia", 1434000000, 0, Activity.UNRESTRICTED, Awareness.UNAWARE,
                     Protective.MANDATORY, Medical.ADVANCED),
             Country("Russia 2", 1434000000, 0, Activity.UNRESTRICTED, Awareness.UNAWARE,
                     Protective.MANDATORY, Medical.ADVANCED)]

airport_list = []

for x in range(len(countries)):
    if countries[x].get_name() in AIRPORT_COUNTRIES:
        # Use the index to get the location of the country
        location = AIRPORT_COUNTRIES.index(countries[x].get_name())
        individual = AIRPORT_DETAILS[location]
        airport = AirPort(individual[0], individual[1], individual[2])
        countries[x].set_airport(airport)
        airport_list.append(countries[x])


def game():
    gameLoop.run(countries, airport_list, AIRPORT_COUNTRIES)


# gameLoop.run(countries, airport_list, AIRPORT_COUNTRIES)


game_thread = Thread(target=game)

game_thread.start()
game_thread.join()
print("out of loop")
