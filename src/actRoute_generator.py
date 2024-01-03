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
from tools.cities_products import shopping_list as sl, random_item_value, merch_maker

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
    with open("./data/" + params.SROUTES_FILENAME, "r") as std_file:
        std_routes_json = json.load(std_file)

    # Create objects from the data
    std_routes: List[StdRoute] = []
    for std_route_json in std_routes_json:
        trips: List[Trip] = []
        # create list of Trip
        for trip_json in std_route_json["route"]:
            trips.append(
                Trip(trip_json["from"], trip_json["to"], trip_json["merchandise"])
            )

        # create list of StdRoute
        std_routes.append(StdRoute(std_route_json["id"], trips))

    return std_routes

# Get the standard routes from the json file
def getActRoutes() -> List[ActRoute]:
    # reading sRoutes from json
    with open("./data/" + params.AROUTES_FILENAME, "r") as act_file:
        act_routes_json = json.load(act_file)

    # Create objects from the data
    act_routes: List[ActRoute] = []
    for act_route_json in act_routes_json:
        trips: List[Trip] = []
        # Create list of Trip
        for trip_json in act_route_json["route"]:
            trips.append(
                Trip(trip_json["from"], trip_json["to"], trip_json["merchandise"])
            )

        act_id = act_route_json["id"]
        driver_id = act_route_json["driver"]
        sroute_id = act_route_json["sroute"]

        # Create list of ActRoute
        act_routes.append(ActRoute(act_id, driver_id, sroute_id, trips))

    return act_routes

# Generate the cities
def genCities(
    driver: Driver,
    stdTrip: Trip,
    actualRoute: ActRoute,
    i: int,
    file,
) -> Tuple[Trip, Trip]:
    actualTrip = Trip("", "", {})
    actualTripCityAdded = Trip("", "", {})

    if (
        np.random.randint(0, 101) <= driver.citiesCrazyness
    ):  # We want to change the city
        if params.DEBUG:
            file.write("first dice is TRUE -> let's modify!\n")
        # If the city is liked, we keep it
        if stdTrip._from in driver.likedCities:
            if params.DEBUG:
                file.write("but I like the city I come from! I won't change anything\n")
            # actualTrip.update({"from": stdTrip._from})
            # actualTrip.update({"to": stdTrip.to})
            actualTrip._from = stdTrip._from
            actualTrip.to = stdTrip.to

        # If it's disliked we remove it
        elif stdTrip._from in driver.dislikedCities:
            if params.DEBUG:
                file.write("I come from a city that sucks! Remove it!\n")
            if i > 0:
                if actualRoute.aRoute[i - 1]._from != stdTrip.to:
                    actualRoute.aRoute[i - 1].to = stdTrip.to  # update({"to": stdTrip.to})
                else:
                    # actualTrip.update({"from": stdTrip._from})
                    # actualTrip.update({"to": stdTrip.to})
                    actualTrip._from = stdTrip._from
                    actualTrip.to = stdTrip.to
            # TODO se non si può eliminare lasciamo così o sostituiamo?

        # Otherwise, add a new city
        else:
            if params.DEBUG:
                file.write("let's add a city\n")
            if (
                np.random.randint(0, 101) <= params.CAP_ADD_NEW_CITY
            ):  # Check if we want to create a liked city or a normal one
                # Create a liked city
                new_city = np.random.choice(driver.likedCities)
                while (
                    new_city == stdTrip._from
                    or new_city == stdTrip.to
                    or (i > 0 and new_city == (actualRoute.aRoute[i - 1])._from)
                ):
                    new_city = np.random.choice(driver.likedCities)

                if i > 0:
                    actualRoute.aRoute[i - 1].to = new_city  # update({"to": new_city})
                # actualTrip.update({"from": new_city})
                # actualTrip.update({"to": stdTrip._from})
                actualTrip._from = new_city
                actualTrip.to = stdTrip._from
                # actualTripCityAdded.update({"from": stdTrip._from})
                # actualTripCityAdded.update({"to": stdTrip.to})
                actualTripCityAdded._from = stdTrip._from
                actualTripCityAdded.to = stdTrip.to

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
                    or (i > 0 and new_city == (actualRoute.aRoute[i - 1])._from)
                ):
                    new_city = np.random.choice(driver.cities)

                if i > 0:
                    actualRoute.aRoute[i - 1].to = new_city  # update({"to": new_city})
                # actualTrip.update({"from": new_city})
                # actualTrip.update({"to": stdTrip._from})
                actualTrip._from = new_city
                actualTrip.to = stdTrip._from
                # actualTripCityAdded.update({"from": stdTrip._from})
                # actualTripCityAdded.update({"to": stdTrip.to})
                actualTripCityAdded._from = stdTrip._from
                actualTripCityAdded.to = stdTrip.to

                if params.DEBUG:
                    file.write(
                        f"second dice is FALSE -> let's add a normal city: {new_city}\n"
                    )

    # We don't have to change anything :P
    else:
        if params.DEBUG:
            file.write("first dice is FALSE -> I'm not going to modify anithyng\n")
        # actualTrip.update({"from": stdTrip._from})
        # actualTrip.update({"to": stdTrip.to})
        actualTrip._from = stdTrip._from
        actualTrip.to = stdTrip.to

    return actualTrip, actualTripCityAdded


def modify_merch(
    merch: str,
    quantity: int,
    driver: Driver,
    trip: Trip,
    # stdTrip: Trip,
) -> Tuple[Trip, Trip]:
    # If the product is liked we add more
    if merch in driver.likedProducts:
        new_quantity = quantity + np.random.randint(
            params.MIN_PRODUCTS_TO_ADD, params.MAX_PRODUCTS_TO_ADD
        )
        trip.merchandise.update({merch: new_quantity})

    # If the product is disliked we don't add it
    elif merch in driver.dislikedProducts:
        return trip

    # If not liked or disliked
    else:
        # If true modify the quantity
        if np.random.randint(0, 101) <= params.CAP_TO_MODIFY_PRODUCT:
            # If true add more
            if np.random.randint(0, 2):
                new_quantity = quantity + np.random.randint(
                    params.MIN_PRODUCTS_TO_ADD, params.MAX_PRODUCTS_TO_ADD
                )

            # If false remove some
            else:
                new_quantity = quantity - np.random.randint(
                    params.MIN_PRODUCTS_TO_ADD, params.MAX_PRODUCTS_TO_ADD
                )
            trip.merchandise.update({merch: new_quantity})

        # Otherwise modify the whole product
        else:
            key_difference = list(set(sl) - set(trip.merchandise.keys()))
            new_key = np.random.choice(key_difference)
            trip.merchandise.update({new_key: random_item_value()})

    return trip


# Generate the merchandise
def genMerchandise(
    driver: Driver,
    stdTrip: Trip,
    actualTrip: Trip,
    actualTripCityAdded: Trip,
    file,
) -> Tuple[Trip, Trip]:
    # COULD BE USEFUL likedProducts = np.random.choice(sl, size=np.random.randint(0, params.MAX_LIKED_PRODUCTS), replace=False)
    if (actualTripCityAdded.is_empty()):
        for merch, quantity in stdTrip.merchandise.items():
            if len(stdTrip.merchandise) >= params.MAXPRODUCTS:
                break
            # We want to change the products
            if np.random.randint(0, 101) <= driver.productsCrazyness:
                actualTrip = modify_merch(
                    merch, quantity, driver, actualTrip
                )

            # We don't have to change anything :P
            else:
                actualTrip.merchandise.update({merch: quantity})
    else:
        for merch, quantity in stdTrip.merchandise.items():
            if len(stdTrip.merchandise) >= params.MAXPRODUCTS:
                break
            # We want to change the products
            if np.random.randint(0, 101) <= driver.productsCrazyness:
                actualTripCityAdded = modify_merch(
                    merch, quantity, driver, actualTripCityAdded
                )

            # We don't have to change anything :P
            else:
                actualTripCityAdded.merchandise.update({merch: quantity})
        
        # create a totally new merchandise dictionary for the new city
        actualTrip.merchandise.update(merch_maker(params.MINPRODUCTS, params.MAXPRODUCTS))


    return actualTrip, actualTripCityAdded


def generateActualRoute(std_route: StdRoute, driver: Driver) -> ActRoute:
    global act_route_counter
    # Create actual route
    actualRoute: ActRoute = ActRoute("", "", "", [])
    id: int = "a" + str(act_route_counter)
    act_route_counter += 1
    # actualRoute.update({"id": id})
    # actualRoute.update({"driver": driver.id})
    # actualRoute.update({"sroute:": std_route.id})
    # actualRoute.update({"route": []})
    actualRoute.id = id
    actualRoute.driver_id = driver.id
    actualRoute.sRoute_id = std_route.id
    actualRoute.aRoute = []

    if not os.path.exists("./tests/operations/driver_" + str(driver.id)):
        os.makedirs("./tests/operations/driver_" + str(driver.id))
    with open(f"./tests/operations/driver_{driver.id}/{std_route.id}.txt", "w") as file:
        i = 0
        for stdTrip in std_route.route:
            if params.DEBUG:
                file.write(f"ciclo numero {i}, driver numero {driver.id}\n")

            """ CITIES """
            actualTrip, actualTripCityAdded = genCities(
                driver, stdTrip, actualRoute, i, file
            )

            # If we removed the city skip products
            if actualTrip == {}:
                if params.DEBUG:
                    file.write("\n\n")
                continue

             # For now we just skip the trip if the from and to are the same
            if actualTrip._from == "" and  actualTrip.to == "":
                continue

            """ PRODUCTS """  # TODO it's not complete
            actualTrip, actualTripCityAdded = genMerchandise(
                driver, stdTrip, actualTrip, actualTripCityAdded, file
            )

            # Add the trip to the route
            actualRoute.aRoute.append(actualTrip)
            if not actualTripCityAdded.is_empty():
                actualRoute.aRoute.append(actualTripCityAdded)
                i += 1
            i += 1

            if params.DEBUG:
                file.write("\n\n")

        # to_dict() so it's serializable
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

    # cast all elements to dictionary
    actRoutes_list_dict = [actRoute.to_dict() for actRoute in actualRoutes]
    # Save the actual routes on a json file
    with open("./data/" + params.AROUTES_FILENAME, "w") as f:
        f.write(json.dumps(actRoutes_list_dict, indent=4))

    return actualRoutes


if __name__ == "__main__":
    delete_folder("./tests/operations/")
    os.makedirs("./tests/operations/")
    actRoute_generator()
