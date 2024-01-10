import json
import os
from typing import List, Dict, Tuple

import numpy as np


from tools.parameters import Parameters as params
from classes.ActRoute import ActRoute
from classes.StdRoute import StdRoute
from actRoute_generator import getStdRoutes, getActRoutes


def get_std_act_routes() -> Tuple[List[StdRoute], List[ActRoute]]:
    return getStdRoutes(), getActRoutes()


def get_drivers_experience(act_routes: List[ActRoute]) -> Dict[str, float]:
    drivers_actual_count: Dict[str, int] = {}
    # Find how much actual routes each driver has done
    for actual in act_routes:
        driver_id = actual.driver_id
        if driver_id in drivers_actual_count:
            routes_count = drivers_actual_count.get(driver_id)
            drivers_actual_count.update({driver_id: routes_count + 1})
        else:
            drivers_actual_count.update({driver_id: 1})

    drivers_exp: Dict[str, float] = {}
    # Compute the experience for each driver
    avg = sum(drivers_actual_count.values()) / len(drivers_actual_count)
    for driver_id, driver_count in drivers_actual_count.items():
        drivers_exp.update({driver_id: driver_count / avg})

    return drivers_exp


def std_to_actuals_dict(
    std_routes: List[StdRoute], act_routes: List[ActRoute]
) -> Dict[str, List[ActRoute]]:
    std_to_actuals: Dict[str, List[ActRoute]] = {}
    for std_route in std_routes:
        id = std_route.id
        for act_route in act_routes:
            if act_route.sRoute_id == id:
                if id not in std_to_actuals:
                    std_to_actuals.update({id: [act_route]})
                else:
                    std_to_actuals.get(id).append(act_route)

    return std_to_actuals


def init_cities_dict(
    std_routes: List[StdRoute], act_routes: List[ActRoute]
) -> Dict[str, float]:
    cities = set()
    dict_cities: Dict[str, float] = {}

    for std_route in std_routes:
        for trip in std_route.route:
            cities.add(trip._from)
        cities.add(trip.to)

    for act_route in act_routes:
        for trip in act_route.aRoute:
            cities.add(trip._from)
        cities.add(trip.to)

    for city in cities:
        dict_cities.update({city: 0.0})

    return dict_cities

def init_products_dict(std_routes: List[StdRoute], act_routes: List[ActRoute]) -> Dict[str, float]:
    products = set()
    dict_products: Dict[str, float] = {}

    for std_route in std_routes:
        for trip in std_route.route:
            for product in trip.merchandise:
                products.add(product)

    for act_route in act_routes:
        for trip in act_route.aRoute:
            for product in trip.merchandise:
                products.add(product)

    for product in products:
        dict_products.update({product: 0.0})

    return dict_products


def populate_utility_matrix(
    drivers_exp: Dict[str, float],
    std_to_actuals: Dict[str, List[ActRoute]],
    items_rank: Dict[str, float],
    is_merch: bool = False,
) -> Dict[str, Dict[str, float]]:
    utility_matrix: Dict[str, Dict[str, float]] = {}
    for std_route_id, actual_routes in std_to_actuals.items():
        for actual_route in actual_routes:
            for trip in actual_route.aRoute:
                # If we are populating the utility matrix for products, we need to consider the merchandise
                if is_merch:
                    for product in trip.merchandise:
                        value = items_rank.get(product) + drivers_exp.get(actual_route.driver_id)
                        items_rank.update({product: value})
                # If we are populating the utility matrix for cities, we need to consider the cities
                else:
                    city = trip._from
                    value = items_rank.get(city) + drivers_exp.get(actual_route.driver_id)
                    items_rank.update({city: value})

            if not is_merch:
                value = items_rank.get(trip.to) + drivers_exp.get(actual_route.driver_id)
                items_rank.update({trip.to: value})

        # Normalize the values between 0 and 5
        max_value = max(items_rank.values())
        min_value = min(items_rank.values())
        for key, value in items_rank.items():
            value = items_rank.get(key)
            if value > 0.0:
                items_rank.update(
                    {key: (value - min_value) / (max_value - min_value) * 4 + 1}
                )

        # Update the utility matrix
        utility_matrix.update({std_route_id: items_rank.copy()})

        # Init all cities to 0
        for key in items_rank:
            items_rank.update({key: 0.0})

    return utility_matrix


# The first element of the Tuple is the list of liked cities, the second is the list of disliked cities
def get_liked_disliked_items(
    utility_matrix: Dict[str, Dict[str, float]]
) -> Dict[str, Tuple[List[str], List[str]]]:
    liked_disliked_items: Dict[str, Dict[int, List[str]]] = {}
    for std_route_id, items in utility_matrix.items():
        dict_rating: Dict[int, List[str]] = {1: [], 2: [], 3: [], 4: [], 5: []}
        for item, rating in items.items():
            # round the rating to the nearest integer
            key = int(round(rating))
            if key == 0:
                key = 1
            dict_rating[key].append(item)
        liked_disliked_items.update({std_route_id: dict_rating})

    # now we create the tuple of liked cities for each standard route
    res_dict: Dict[str, Tuple[List[str], List[str]]] = {}
    for std_route_id, dict_rating in liked_disliked_items.items():
        liked_list: List[str] = dict_rating.get(5)
        for item in dict_rating.get(4):
            liked_list.append(item)
        disliked_list: List[str] = dict_rating.get(1)
        for item in dict_rating.get(2):
            disliked_list.append(item)
        res_dict.update({std_route_id: (liked_list, disliked_list)})

    return res_dict

# TODO: implement algoritmo furbo rather than inserting random values!
def complete_utility_matrix(utility_matrix: Dict[str, Dict[str, float]]):
    # If there are cities with value 0, add random values between 1 and 5
    for std_route_id, items in utility_matrix.items():
        for item, value in items.items():
            if value == 0.0:
                items.update({item: np.random.random() * 5})
        utility_matrix.update({std_route_id: items})

    return utility_matrix


def common_fn_call() -> (
    Tuple[List[StdRoute], List[ActRoute], Dict[str, float], Dict[str, List[ActRoute]]]
):
    # Get standard and actual routes from dataset
    (
        std_routes,
        act_routes,
    ) = get_std_act_routes()  # Return type: Tuple[List[StdRoute], List[ActRoute]]

    # Get for each driver its experience (how much actual routes he has done)
    drivers_exp: Dict[str, float] = get_drivers_experience(act_routes)
    print("  - Done creating the dict driver experience")

    # Get for each standard route, all its actual routes
    std_to_actuals: Dict[str, List[ActRoute]] = std_to_actuals_dict(
        std_routes, act_routes
    )
    print("  - Done creating the dict standard routes to actual routes")

    return std_routes, act_routes, drivers_exp, std_to_actuals


def cities(
    std_routes: List[StdRoute],
    act_routes: List[ActRoute],
    drivers_exp: Dict[str, float],
    std_to_actuals: Dict[str, List[ActRoute]],
) -> Dict[str, Tuple[List[str], List[str]]]:
    # Get all cities ever visited
    all_cities: Dict[str, float] = init_cities_dict(std_routes, act_routes)
    print("  - Done creating the dict all cities")

    # Populate the utility matrix for reccomendation system
    utility_matrix: Dict[str, Dict[str, float]] = populate_utility_matrix(
        drivers_exp, std_to_actuals, all_cities
    )
    print("  - Done creating the utility matrix")

    complete_matrix: Dict[str, Dict[str, float]] = complete_utility_matrix(
        utility_matrix
    )
    print("  - Done completing the utility matrix")

    # the first element of the Tuple is the list of liked cities, the second is the list of disliked cities
    liked_disliked_cities: Dict[
        str, Tuple[List[str], List[str]]
    ] = get_liked_disliked_items(complete_matrix)
    print("  - Done creating the dict liked and disliked cities")

    return liked_disliked_cities

def products(
    std_routes: List[StdRoute],
    act_routes: List[ActRoute],
    drivers_exp: Dict[str, float],
    std_to_actuals: Dict[str, List[ActRoute]],
):
    # Get all cities ever visited
    all_products: Dict[str, float] = init_products_dict(std_routes, act_routes)
    print("  - Done creating the dict all cities")

    # Populate the utility matrix for reccomendation system
    utility_matrix: Dict[str, Dict[str, float]] = populate_utility_matrix(
        drivers_exp, std_to_actuals, all_products, True
    )
    print("  - Done creating the utility matrix")

    complete_matrix: Dict[str, Dict[str, float]] = complete_utility_matrix(
        utility_matrix
    )
    print("  - Done completing the utility matrix")

    # the first element of the Tuple is the list of liked cities, the second is the list of disliked cities
    liked_disliked_cities: Dict[
        str, Tuple[List[str], List[str]]
    ] = get_liked_disliked_items(complete_matrix)
    print("  - Done creating the dict liked and disliked cities")

    return liked_disliked_cities


def point_1() -> None:
    # Some common function calls
    std_routes, act_routes, drivers_exp, std_to_actuals = common_fn_call()

    liked_disliked_cities: Dict[str, Tuple[List[str], List[str]]] = cities(std_routes, act_routes, drivers_exp, std_to_actuals)
    liked_disliked_merch: Dict[str, Tuple[List[str], List[str]]] = products(std_routes, act_routes, drivers_exp, std_to_actuals)
    print(liked_disliked_merch)

    # modifica la std route e ogni volta che trova una città che non ci piace la sostituisce con una città che ci piace di più
    # salva la rec standard in un file json


if __name__ == "__main__":
    point_1()

    # prendiamo per ogni standard, tutte le sue actual e contiamo le occorrenze delle città e creiamo una matrice standardRoute x città
    # scegliamo le n città più frequenti e le k meno frequenti e le aggiungiamo / togliamo alla standard route per tenerla di lunghezza simile
    # Per i prodotti è uguale
