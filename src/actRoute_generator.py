import json
from typing import List, Dict, Tuple
import numpy as np

from classes.Driver import Driver
from classes.Trip import Trip
from classes.StdRoute import StdRoute
from tools.parameters import Parameters as params

act_route_counter = 0


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


def generateActualRoute(std_route: StdRoute, driver: Driver) -> StdRoute:
    global act_route_counter
    # Create actual route
    actualRoute: StdRoute = {}
    id = "a" + str(act_route_counter)
    act_route_counter += 1
    actualRoute.update({"id": id})
    actualRoute.update({"driver": driver.id})
    actualRoute.update({"sroute:": std_route.id})
    actualRoute.update({"route": []})

    for i, stdTrip in enumerate(std_route.route):
        actualTrip = {}

        # Cities (NEED TO CHECK)
        if np.random.randint(0, 101) <= driver.citiesCrazyness:
            # if the city is liked
            if stdTrip._from in driver.likedCities:
                actualTrip.update({"from": stdTrip._from})
                actualTrip.update({"to": stdTrip.to})
            # it's the same if the city is disliked or not
            elif stdTrip._from in driver.dislikedCities:
                actualRoute[i - 1].to = stdTrip.to
                continue
            else:
                # da mettere cap su file
                if np.random.randint(0, 101) <= 80:
                    new_city = np.random.choice(driver.likedCities)
                    while (
                        new_city == stdTrip._from
                        or new_city == stdTrip.to
                    ):
                        new_city = np.random.choice(driver.cities)
                else:


                # new_city = np.random.choice(driver.cities)
                # while (
                #     new_city == stdTrip._from
                #     or new_city == stdTrip.to
                #     or new_city in driver.dislikedCities
                # ):
                #     new_city = np.random.choice(driver.cities)
                # new_city = np.random.choice(driver.cities)
                # actualTrip.update({"from": new_city})
                # actualTrip.update({"to": stdTrip.to})
                # std_route.route[i - 1]._from = new_city
        else:
            actualTrip.update({"from": stdTrip._from})
            actualTrip.update({"to": stdTrip.to})

        # Products (NEED TO CHECK)
        if np.random.randint(0, 101) <= driver.productsCrazyness:
            # if the product is liked
            if stdTrip.merchandise in driver.likedProducts:
                actualTrip.update({"merchandise": stdTrip.merchandise})
            # it's the same if the product is disliked or not
            else:
                new_product = np.random.choice(driver.products)
                while (
                    new_product == stdTrip.merchandise
                    or new_product in driver.dislikedProducts
                ):
                    new_product = np.random.choice(driver.products)
                actualTrip.update({"merchandise": new_product})
        else:
            actualTrip.update({"merchandise": stdTrip.merchandise})

        actualRoute["route"].append(actualTrip)

    return actualRoute


def actRoute_generator():
    # Create objects from the data
    drivers: List[Driver] = getDrivers()
    stdRoutes: List[StdRoute] = getStdRoutes()

    for driver in drivers:
        DRIVER_ROUTES = np.random.randint(
            params.MIN_ROUTES_TO_DRIVERS, params.MAX_ROUTES_TO_DRIVERS + 1
        )
        for _ in range(DRIVER_ROUTES):
            selected_route: StdRoute = np.random.choice(stdRoutes)
            # Create actual route
            actualRoute = generateActualRoute(selected_route, driver)
            print(actualRoute)


if __name__ == "__main__":
    actRoute_generator()
