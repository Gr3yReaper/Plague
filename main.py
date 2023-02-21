import diseaseGrowth
from Country import *
from AirPort import *

BASE_ACTIVITY = 80
AIRPORT_COUNTRIES = ["UK", "Russia", "Russia 2"]
AIRPORT_DETAILS = [["UK", ["Russia", "Russia 2"], BASE_ACTIVITY], ["Russia", ["UK", "Russia 2"], BASE_ACTIVITY],
                   ["Russia 2", [""], BASE_ACTIVITY]]
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

while not any([n.get_infected() >= 10000 for n in countries]):
    # Calculates the new infected numbers for each country then updates the objects
    # Work out rough chance of said airport travelling, randomly pick location etc
    flight_log = ([n.get_airport().flight(n.get_infected()) for n in airport_list])
    newInfected = [diseaseGrowth.update(n.get_infected(), n.get_activity().value,
                                        n.get_awareness().value, n.get_protective().value,
                                        n.get_medical().value) for n in countries]
    # Modified algorithm to add people as infected
    for x in range(len(countries)):
        countries[x].update_infected(newInfected[x])

    for x in range(len(flight_log)):
        if flight_log[x] is not None:
            for y in range(len(countries)):
                if countries[y].get_name() == flight_log[x] and countries[y].get_infected() == 0:
                    countries[y].update_infected(1)  # Set as 1 for now to start infection
                    print("Plane left: " + AIRPORT_COUNTRIES[x] + ", Headed for: " + countries[y].get_name())

    # One airport/ boat per country for now
    # Random chance one will start (pick a random country with a free port/ airport
    # around 0.8% when unaware, 0.5 when slight, 0.3 when aware, 0.1 when reduced, and 0 for lockdown rough values
    print([n.get_infected() for n in countries])
print("out of loop")
