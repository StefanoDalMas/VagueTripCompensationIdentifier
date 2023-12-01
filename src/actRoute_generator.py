import json
from typing import List, Dict, Tuple
import numpy as np

from classes.Driver import Driver
from classes.Trip import Trip
from classes.StdRoute import StdRoute
from classes.ActRoute import ActRoute
from tools.parameters import Parameters as params

act_route_counter: int = 0  # For the id of the actual routes


# Get the drivers from the json file
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


# Get the standard routes from the json file
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
    actualRoute: ActRoute = {}
    id: int = "a" + str(act_route_counter)
    act_route_counter += 1
    actualRoute.update({"id": id})
    actualRoute.update({"driver": driver.id})
    actualRoute.update({"sroute:": std_route.id})
    actualRoute.update({"route": []})

    i = 0
    for stdTrip in std_route.route:
        actualTrip = {}

        """ CITIES """
        if (
            np.random.randint(0, 101) <= driver.citiesCrazyness
        ):  # We want to change the city
            # If the city is liked, we keep it
            if stdTrip._from in driver.likedCities:
                actualTrip.update({"from": stdTrip._from})
                actualTrip.update({"to": stdTrip.to})

            # If it's disliked we remove it
            elif stdTrip._from in driver.dislikedCities:
                if i > 0:
                    actualRoute.get("route")[i - 1].update({"to": stdTrip.to})

            # Otherwise, add a new city
            else:
                # Da mettere cap su file
                if (
                    np.random.randint(0, 101) <= params.CAP_ADD_NEW_CITY
                ):  # Check if we want to create a liked city or not
                    # Create a liked city
                    new_city = np.random.choice(driver.likedCities)
                    while new_city == stdTrip._from or new_city == stdTrip.to:
                        new_city = np.random.choice(driver.cities)

                    if i > 0:
                        actualRoute.get("route")[i - 1].update({"to": new_city})
                    actualTrip.update({"from": new_city})
                    actualTrip.update({"to": stdTrip.to})

                # Don't change anything
                else:
                    actualTrip.update({"from": stdTrip._from})
                    actualTrip.update({"to": stdTrip.to})

        # We don't have to change anything :P
        else:
            actualTrip.update({"from": stdTrip._from})
            actualTrip.update({"to": stdTrip.to})

        # If we removed the city skip products
        if actualTrip == {}:
            continue

        """ PRODUCTS """  # TODO it's not complete
        # We want to change the products
        if np.random.randint(0, 101) <= driver.productsCrazyness:
            # If the product is liked
            if stdTrip.merchandise in driver.likedProducts:
                actualTrip.update({"merchandise": stdTrip.merchandise})
            # It's the same if the product is disliked or not
            else:
                # Create a new product
                new_product = np.random.choice(driver.products)
                while (
                    new_product == stdTrip.merchandise
                    or new_product in driver.dislikedProducts
                ):
                    new_product = np.random.choice(driver.products)
                actualTrip.update({"merchandise": new_product})

        # We don't have to change anything :P
        else:
            actualTrip.update({"merchandise": stdTrip.merchandise})

        # Add the trip to the route
        actualRoute["route"].append(actualTrip)
        i += 1

    return actualRoute


def actRoute_generator() -> List[ActRoute]:
    # Create objects from the data
    drivers: List[Driver] = getDrivers()
    stdRoutes: List[StdRoute] = getStdRoutes()
    actualRoutes: List[ActRoute] = []

    for driver in drivers:
        DRIVER_ROUTES = np.random.randint(
            params.MIN_ROUTES_TO_DRIVERS, params.MAX_ROUTES_TO_DRIVERS + 1
        )
        for _ in range(DRIVER_ROUTES):
            selected_route: StdRoute = np.random.choice(stdRoutes)
            # Create actual routes
            actualRoutes.append(generateActualRoute(selected_route, driver))

    # Save the actual routes on a json file
    with open("./data/" + params.AROUTES_FILENAME, "w") as f:
        f.write(json.dumps(actualRoutes, indent=4))

    return actualRoutes


if __name__ == "__main__":
    actRoute_generator()
