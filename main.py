import diseaseGrowth
from Country import *

countries = [Country("UK", 6733000000, 1, Activity.SLIGHT, Awareness.SLIGHT,
                     Protective.LITTLE, Medical.HIGH),
             Country("Russia", 1434000000, 0, Activity.UNRESTRICTED, Awareness.UNAWARE,
                     Protective.NONE, Medical.ADVANCED)]

while not any([n.get_infected() >= 1000 for n in countries]):
    # Calculates the new infected numbers for each country then updates the objects
    newInfected = [diseaseGrowth.update(n.get_infected(), n.get_activity().value,
                                        n.get_awareness().value, n.get_protective().value,
                                        n.get_medical().value) for n in countries]

    # Modified algorithm to add people as infected
    for x in range(len(countries)):
        countries[x].update_infected(newInfected[x])

    # Need amount of ports and airports per country
    # Random chance one will start (pick a random country with a free port/ airport
    # around 0.8% when unaware, 0.5 when slight, 0.3 when aware, 0.1 when reduced, and 0 for lockdown rough values
    # Implement queue to remove people after 14 days, originally instantiated with 1 as that is starting infected.

print([n.get_infected() for n in countries])
print("out of loop")
