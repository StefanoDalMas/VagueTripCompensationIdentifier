import json
from typing import List, Dict, Tuple

from classes.Driver import Driver
from classes.Trip import Trip
from classes.StdRoute import StdRoute
from tools.parameters import Parameters as p

# reading drivers from json
with open("./data/" + p.DRIVERS_FILENAME, "r") as driversFile:
    driversJson = json.load(driversFile)

# Create objects from the data
drivers = []
for driverJson in driversJson:
    driver = Driver(
        driverJson["id"],
        driverJson["citiesCrazyness"],
        driverJson["productsCrazyness"],
        driverJson["likedCities"],
        driverJson["likedProducts"],
        driverJson["dislikedCities"],
        driverJson["dislikedProducts"],
        driverJson["cities"],
        driverJson["products"],
)
    drivers.append(driver)

# print
# for i in range(len(drivers)):
#     print(drivers[i])


# reading sRoutes from json
with open("./data/" + p.SROUTES_FILENAME, "r") as driversFile:
    sRoutesJson = json.load(driversFile)


sRoutes: List[StdRoute] = []
for sRouteJson in sRoutesJson:
    trips: List[Trip] = []
    # create list of Trip
    for tripJson in sRouteJson["route"]:
        trips.append(Trip(tripJson["from"],
                          tripJson["to"],
                          tripJson["merchandise"]))
    
    # create list of StdRoute
    sRoutes.append(StdRoute(
        sRouteJson["id"],
        trips
    ))

# print
for i in range(len(sRoutes)):
    print(sRoutes[i])


# ----------
# here drivers and sRoutes ready to be used!