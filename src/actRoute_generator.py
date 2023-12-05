import json
from typing import List, Dict, Tuple
import numpy as np
import os

from classes.Driver import Driver
from classes.Trip import Trip
from classes.StdRoute import StdRoute
from classes.ActRoute import ActRoute
from tools.parameters import Parameters as params
from tools.utils import delete_folder

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

    if not os.path.exists("./tests/operations/driver_" + str(driver.id)):
        os.makedirs("./tests/operations/driver_" + str(driver.id))
    with open(f"./tests/operations/driver_{driver.id}/{std_route.id}.txt", "w") as file:
        i = 0
        for stdTrip in std_route.route:
            if params.DEBUG:
                file.write(f"ciclo numero {i}, driver numero {driver.id}\n")
            actualTrip = {}
            actualTripCityAdded = {}

            """ CITIES """
            if (
                np.random.randint(0, 101) <= driver.citiesCrazyness
            ):  # We want to change the city
                if params.DEBUG:
                    file.write("first dice is TRUE -> let's modify!\n")
                # If the city is liked, we keep it
                if stdTrip._from in driver.likedCities:

                    if params.DEBUG:
                        file.write(
                            "but I like the city I come from! I won't change anything\n"
                        )
                    actualTrip.update({"from": stdTrip._from})
                    actualTrip.update({"to": stdTrip.to})

                # If it's disliked we remove it
                elif stdTrip._from in driver.dislikedCities:
                    if params.DEBUG:
                        file.write("I come from a city that sucks! Remove it!\n")
                    if i > 0 and actualRoute.get("route")[i - 1]["from"] != stdTrip.to:
                        actualRoute.get("route")[i - 1].update({"to": stdTrip.to})
                    elif i > 0:
                        actualTrip.update({"from": stdTrip._from})
                        actualTrip.update({"to": stdTrip.to})
                    # TODO se non si può eliminare lasciamo così o sostituiamo?

                # Otherwise, add a new city
                else:
                    if params.DEBUG: file.write("let's add a city\n")
                    if (
                        np.random.randint(0, 101) <= params.CAP_ADD_NEW_CITY
                        and len(driver.likedCities) > 0
                    ):  # Check if we want to create a liked city or a normal one
                        # Create a liked city
                        new_city = np.random.choice(driver.likedCities)
                        while (
                            new_city == stdTrip._from
                            or new_city == stdTrip.to
                            or (
                                i > 0
                                and new_city == (actualRoute.get("route")[i - 1])["from"]
                            )
                        ):
                            new_city = np.random.choice(driver.likedCities)

                        if i > 0:
                            actualRoute.get("route")[i - 1].update({"to": new_city})
                        actualTrip.update({"from": new_city})
                        actualTrip.update({"to": stdTrip._from})
                        actualTripCityAdded.update({"from": stdTrip._from})
                        actualTripCityAdded.update({"to": stdTrip.to})


                        if params.DEBUG:
                            file.write(
                                f"second dice is TRUE -> let's add an awsome city: {new_city}\n"
                            )

                    else:
                        # Create a normal city
                        new_city = np.random.choice(driver.cities)
                        while (
                            new_city == stdTrip._from
                            or new_city == stdTrip.to
                            or (
                                i > 0
                                and new_city
                                == (actualRoute.get("route")[i - 1])["from"]
                            )
                        ):
                            new_city = np.random.choice(driver.cities)
                        
                        if i > 0:
                            actualRoute.get("route")[i - 1].update({"to": new_city})
                        actualTrip.update({"from": new_city})
                        actualTrip.update({"to": stdTrip._from})
                        actualTripCityAdded.update({"from": stdTrip._from})
                        actualTripCityAdded.update({"to": stdTrip.to})

                        if params.DEBUG:
                            file.write(
                                f"second dice is FALSE -> let's add a normal city: {new_city}\n"
                            )

            # We don't have to change anything :P
            else:
                if params.DEBUG:
                    file.write("first dice is FALSE -> I'm not going to modify anithyng\n")
                actualTrip.update({"from": stdTrip._from})
                actualTrip.update({"to": stdTrip.to})

            # If we removed the city skip products
            if actualTrip == {}:
                if (params.DEBUG): file.write("\n\n")
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

            # For now we just skip the trip if the from and to are the same
            if actualTrip["from"] == actualTrip["to"]:
                continue

            # Add the trip to the route
            actualRoute["route"].append(actualTrip)
            if actualTripCityAdded != {}:
                actualRoute["route"].append(actualTripCityAdded)
                i += 1
            i += 1

            if params.DEBUG:
                file.write("\n\n")

        return actualRoute


def actRoute_generator() -> List[ActRoute]:
    # Create objects from the data
    drivers: List[Driver] = getDrivers()
    stdRoutes: List[StdRoute] = getStdRoutes()
    actualRoutes: List[ActRoute] = []
    selected_stdRoutes: List[str] = []
    selected_route: StdRoute

    for driver in drivers:
        DRIVER_ROUTES = np.random.randint(
            params.MIN_ROUTES_TO_DRIVERS, params.MAX_ROUTES_TO_DRIVERS + 1
        )
        for i in range(DRIVER_ROUTES):
            selected_route = np.random.choice(stdRoutes)
            if i == 0:
                selected_stdRoutes.append(selected_route.id)
                actualRoutes.append(generateActualRoute(selected_route, driver))
            else:
                while selected_route.id in selected_stdRoutes:
                    selected_route = np.random.choice(stdRoutes)
                selected_stdRoutes.append(selected_route.id)
                actualRoutes.append(generateActualRoute(selected_route, driver))
        selected_stdRoutes.clear()

    # Save the actual routes on a json file
    with open("./data/" + params.AROUTES_FILENAME, "w") as f:
        f.write(json.dumps(actualRoutes, indent=4))

    return actualRoutes


if __name__ == "__main__":
    delete_folder("./tests/operations/")
    os.makedirs("./tests/operations/")
    actRoute_generator()
