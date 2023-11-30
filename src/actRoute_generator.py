import json
from typing import List, Dict, Tuple
import numpy as np

from classes.Driver import Driver
from classes.Trip import Trip
from classes.StdRoute import StdRoute
from classes.ActRoute import StdRoute as ActRoute  #dongi sei una merda
from tools.parameters import Parameters as params
from tools.cities_products import random_city

act_route_counter = 0
cap = 80


def getDrivers() -> List[Driver]:
    # reading drivers from json
    with open("./data/" + params.DRIVERS_FILENAME, "r") as driversFile:
        driversJson = json.load(driversFile)

    # Create objects from the data
    drivers: List[Driver] = []
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

    return drivers


def getStdRoutes() -> List[StdRoute]:
    # reading sRoutes from json
    with open("./data/" + params.SROUTES_FILENAME, "r") as driversFile:
        sRoutesJson = json.load(driversFile)

    # Create objects from the data
    stdRoutes: List[StdRoute] = []
    for sRouteJson in sRoutesJson:
        trips: List[Trip] = []
        # create list of Trip
        for tripJson in sRouteJson["route"]:
            trips.append(
                Trip(tripJson["from"], tripJson["to"], tripJson["merchandise"])
            )

        # create list of StdRoute
        stdRoutes.append(StdRoute(sRouteJson["id"], trips))

    return stdRoutes


def generateActualRoute(std_route: StdRoute, driver: Driver) -> ActRoute:
    global act_route_counter
    # Create actual route
    actualRoute: StdRoute = {}
    id = "a" + str(act_route_counter)
    act_route_counter += 1
    actualRoute.update({"id": id})
    actualRoute.update({"driver": driver.id})
    actualRoute.update({"sroute:": std_route.id})
    actualRoute.update({"route": []})
    changed = False # ricordarsi di capire cosa accade se ne cambia 2 di fila
    i = 0

    for stdTrip in std_route.route:
        actualTrip = {}
        if changed:
            changed = False
            actualTrip.update({"from": stdTrip._from})
            actualTrip.update({"to": stdTrip.to})
        # CITIES
        elif (
            np.random.randint(0, 101) <= driver.citiesCrazyness
        ):  # we want to change the city
            # if the city is liked, we keep it
            if stdTrip._from in driver.likedCities:
                actualTrip.update({"from": stdTrip._from})
                actualTrip.update({"to": stdTrip.to})
            # # if it's disliked we remove it
            elif stdTrip._from in driver.dislikedCities: 
                if i > 0:
                    actualRoute.get("route")[i - 1].update({"to": stdTrip.to})
                    i-=1
                    changed = True
            #otherwise, add a new city
            else:
                # da mettere cap su file
                # global cap
                # if (
                #     np.random.randint(0, 101) <= cap
                # ):  # check if we want to create a liked city or not
                #     # create a liked city
                #     new_city = np.random.choice(driver.likedCities)
                #     while new_city == stdTrip._from or new_city == stdTrip.to:
                #         new_city = np.random.choice(driver.cities)
                #     if i > 0:
                #         actualRoute.get("route")[i - 1].update({"to": new_city})
                #         actualTrip.update({"from": new_city})
                #         actualTrip.update({"to": stdTrip.to})
                #     else:
                #         actualTrip.update({"from": new_city})
                #         actualTrip.update({"to": stdTrip._from})
                actualTrip.update({"from": stdTrip._from})
                actualTrip.update({"to": stdTrip.to})
        else:
            # we don't have to change anything :P
            actualTrip.update({"from": stdTrip._from})
            actualTrip.update({"to": stdTrip.to})

        # Products (NEED TO COCK)
        # if np.random.randint(0, 101) <= driver.productsCrazyness:
        #     # if the product is liked
        #     if stdTrip.merchandise in driver.likedProducts:
        #         actualTrip.update({"merchandise": stdTrip.merchandise})
        #     # it's the same if the product is disliked or not
        #     else:
        #         new_product = np.random.choice(driver.products)
        #         while (
        #             new_product == stdTrip.merchandise
        #             or new_product in driver.dislikedProducts
        #         ):
        #             new_product = np.random.choice(driver.products)
        #         actualTrip.update({"merchandise": new_product})
        # else:
        #     actualTrip.update({"merchandise": stdTrip.merchandise})
        if actualTrip != {}:
            actualRoute["route"].append(actualTrip)
        i+=1

    return actualRoute


def actRoute_generator() -> List[ActRoute]:
    # Create objects from the data
    drivers: List[Driver] = getDrivers()
    stdRoutes: List[StdRoute] = getStdRoutes()
    actualRoute: ActRoute = {}
    actualRoutes :List[ActRoute] = []

    for driver in drivers:
        DRIVER_ROUTES = np.random.randint(
            params.MIN_ROUTES_TO_DRIVERS, params.MAX_ROUTES_TO_DRIVERS + 1
        )
        for _ in range(DRIVER_ROUTES):
            selected_route: StdRoute = np.random.choice(stdRoutes)
            # Create actual route
            actualRoutes.append(generateActualRoute(selected_route, driver))
    return actualRoutes


if __name__ == "__main__":
    actRoute_generator()
