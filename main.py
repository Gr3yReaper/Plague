import diseaseGrowth
from Country import Country, Activity  # Seems to solve the error of object creation in other classes

countries = [Country("UK", 6733000000, 10, Activity.SLIGHT), Country("Russia", 1434000000, 0, Activity.UNAWARE)]

while not any([n.getInfected() >= 100 for n in countries]):
    # Calculates the new infected numbers for each country then updates the objects
    newInfected = [diseaseGrowth.update(n.getInfected(), n.getActivity().value) for n in countries]
    for x in range(len(countries)):
        countries[x].updateInfected(newInfected[x])

    # Need amount of ports and airports per country
    # Random chance one will start (pick a random country with a free port/ airport
    # around 0.8% when unaware, 0.5 when slight, 0.3 when aware, 0.1 when reduced, and 0 for lockdown rough values

print([n.getInfected() for n in countries])
print("out of loop")
