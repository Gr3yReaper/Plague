from Country import *
from AirPort import *

import gameLoop
from threading import Thread

from Upgrades.Response import *
from Upgrades.Operation import *

BASE_ACTIVITY = 20
AIRPORT_COUNTRIES = ["UK", "Russia", "Russia 2"]
AIRPORT_DETAILS = [["UK", ["Russia", "Russia 2"], BASE_ACTIVITY], ["Russia", ["UK", "Russia 2"], BASE_ACTIVITY],
                   ["Russia 2", [""], BASE_ACTIVITY]]

# Reduced list of upgrades will add more when needed
# Will add vaccine creation/ manufacture upgrades as needed.

# Upgrades need to be added in list in form of
# Upgrade_Tree_Name(Title, Description, Cost, [Stats], [Unlock_Requirements]

UPGRADE_LIST = ["OPERATION", [Operation("Investigate Outbreaks", "Search For Local Disease Outbreaks", 4,
                              [], [])],

                [Operation("Deploy Field Operatives", "Team to help surveil disease and reduce infection", 2,
                 ["protective", 1], ["Investigate Outbreaks"])],

                [Operation("Emergency Care", "Field Operatives help reduce fatality rate", 5,
                 ["fatality", 1], ["Deploy Field Operatives"])],

                [Operation("Vaccine Research", "Start researching a cure for the disease", 10,
                 ["research", True, "research_speed", 1], ["Investigate Outbreaks"])],

                [Operation("Accelerated Research", "Round the clock working, research speed increased", 9,
                           ["research_speed", 1], ["Vaccine Research"])],

                [Operation("Global Research Treaty", "Transparent information exchange between countries", 21,
                           ["research_speed", 2], ["Accelerated Research"])],

                [Operation("Field Research", "Field Operatives help research cure", 7,
                           ["research_speed", 1], ["Vaccine Research"])],

                [Operation("Furlough Schemes", "Reduce financial stress by paying staff wages, decreased non-compliance", 7
                           ["non-compliance", 1], ["Investigate Outbreaks"])],

                [Operation("Adapt Society", "Provide resources to accommodate new normal for education and wellness", 10
                           ["non-compliance", 1], ["Furlough Schemes"])],

                [Operation("Mortgage and Rent Relief", "Freeze mortgage and rent payments and ban evictions", 13
                           ["non-compliance", 1], ["Adapt Society"])],

                [Operation("National Stimulus", "Implement tax cuts and business loans, decreases non-compliance", 18
                           ["non-compliance", 1], ["Mortgage and Rent Relief"])],

                [Operation("Authority 1",
                           "Brief world leaders on importance of response to pandemic, slightly increased authority", 7
                           ["authority", 1], ["Investigate Outbreaks"])],

                [Operation("Authority 2",
                           "Make pleas for global co-operation and coordination to contain pandemic, significant authority increase",
                           13, ["authority", 2], ["Authority 1"])],

                [Operation("Authority 3",
                           "Emphasis world threat of pandemic, massively increased authority", 18
                           ["authority", 3], ["Investigate Outbreaks"])],

                # Could add fake news to freeze authority but will be left for now.

                "RESPONSE", [Response("Hand Washing", "Reduces infection by promoting hand washing", 6,
                                      SubCategory.Infection_Prevention, ["protective", 1], ["Investigate Outbreaks"])],

                [Response("Public Awareness",
                          "Promote personal responsibility for hygiene, reduces infection", 3,
                          SubCategory.Infection_Prevention, ["awareness", 1], ["Investigate Outbreaks"])],

                [Response("Disinfectant Supplies",
                          "Distribute bleach and cleaning supplies, reduce infection", 5,
                          SubCategory.Infection_Prevention, ["protective", 1], ["Investigate Outbreaks"])],

                [Response("Self-Isolation",
                          "Symptomatic people can not interact with others, reduce infection", 5,
                          SubCategory.Infection_Prevention, ["protective", 1], ["Hand Washing", "Public Awareness"])],

                [Response("Social Distancing",
                          "People need to stay 2m away from each other, reduce infection, increased non-compliance",
                          9, SubCategory.Infection_Prevention, ["awareness", 1, "protective", 1, "non-compliance", 1],
                          ["Self-Isolation"])],

                [Response("Local Lockdowns",
                          "Force lockdowns in areas, reduce infection significantly but increase non-compliance",
                          20, SubCategory.Infection_Prevention, ["protective", 2, "awareness", 1, "non-compliance", 1],
                          ["Social Distancing"])],

                [Response("PPE Package 1",
                          "Distribute personal protective equipment, reduce infection and slightly fatality rate",
                          7, SubCategory.Infection_Prevention, ["protective", 1, "fatality", 0.5],
                          ["Hand Washing", "Disinfectant Supplies"])],

                [Response("PPE Package 2",
                          "Distribute personal protective equipment, reduce infection and slightly fatality rate",
                          13, SubCategory.Infection_Prevention, ["protective", 1, "fatality", 0.5], ["PPE Package 1"])],

                [Response("Mask Wearing", "People must wear masks, significantly reduce infection", 1,
                          SubCategory.Infection_Prevention, ["protective", 1, "awareness", 2],
                          ["PPE Package 2", "Social Distancing"])],

                [Response("Emergency Preparation", "Brief staff and stock supplies reduce fatality", 8,
                          SubCategory.Death_Prevention, ["fatality", 1],
                          ["Investigate Outbreaks"])],

                [Response("Clinical Treatment", "Usual medicines used to alleviate symptoms, slightly reduced fatality", 3,
                          SubCategory.Death_Prevention, ["fatality", 0.5],
                          ["Investigate Outbreaks"])],

                [Response("Respiratory Support", "Machinery to help patients struggling to breathe, reduced fatality", 7,
                          SubCategory.Death_Prevention, ["fatality", 1],
                          ["Clinical Treatment"])],

                [Response("IV Therapy", "IV therapy to help prevent homeostasis, significantly reduced fatality", 9,
                          SubCategory.Death_Prevention, ["fatality", 2],
                          ["Investigate Outbreaks"])],

                [Response("Staff Expansion", "Retrain staff and bring in students/ retired, reduced fatality", 7,
                          SubCategory.Death_Prevention, ["fatality", 1, "protective", -0.5],
                          ["Emergency Preparation"])],

                [Response("Critical Care", "Brief staff on best practices, reduced fatality", 5,
                          SubCategory.Death_Prevention, ["fatality", 1],
                          ["Emergency Preparations", "Clinical Treatment"])],

                [Response("Treatment Efficiencies", "Specialist treatment squads created, reduced fatality", 13,
                          SubCategory.Death_Prevention, ["fatality", 2],
                          ["Critical Care"])],

                [Response("New Infrastructure", "Invest in new infrastructure, reduced fatality and authority loss", 12,
                          SubCategory.Death_Prevention, ["fatality", 0.5, "authority_loss", -1],
                          ["Staff Expansion"])],

                [Response("Surge Protocols", "All appointments online and no longer face to face, reduced fatality and infection", 14,
                          SubCategory.Death_Prevention, ["protective", 0.5, "fatality", 1],
                          ["New Infrastructure", "Treatment Efficiencies"])],

                [Response("Advanced Antibiotics", "Experimental treatments to target pathogen, reduced fatality and increased research speed", 11,
                          SubCategory.Death_Prevention, ["fatality", 1, "research_speed", 1],
                          ["IV Therapy", "Treatment Efficiencies"])],

                [Response("Triage Protocols", "Strict criteria to be administered, reduced fatality but lose authority", 6,
                          SubCategory.Death_Prevention, ["fatality", 1, "authority_loss", 2],
                          ["New Infrastructure"])]
                # Potentially add border surveilance to reduce chance of flight taking place from countries with infected.
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
    variable = gameLoop.run(countries, airport_list, AIRPORT_COUNTRIES)
    print(variable)

# gameLoop.run(countries, airport_list, AIRPORT_COUNTRIES)


game_thread = Thread(target=game)

game_thread.start()
game_thread.join()
print("out of loop")
