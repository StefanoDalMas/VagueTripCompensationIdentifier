import json
import os
import numpy as np
from typing import List, Dict, Tuple
from numpy import ndarray
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import csr_matrix

from tools.parameters import Parameters as params
from classes.ActRoute import ActRoute
from classes.StdRoute import StdRoute
from actRoute_generator import getStdRoutes, getActRoutes


# Returns a tuple of two lists: the first one contains all the standard routes, the second one contains all the actual routes
def get_std_act_routes() -> Tuple[List[StdRoute], List[ActRoute]]:
    return getStdRoutes(), getActRoutes()


# Returns a dictionary where the key is the driver id and the value is the experience of the driver
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


# Returns a dictionary where the key is the standard route id and the value is a list of actual routes
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


# Init all cities to rating 0
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


def init_products_dict(
    std_routes: List[StdRoute], act_routes: List[ActRoute]
) -> Dict[str, float]:
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


# Populates a utility matrix based on drivers' experience, actual routes, item rankings, and whether it is for merchandise or cities.
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
                        value = items_rank.get(product) + drivers_exp.get(
                            actual_route.driver_id
                        )
                        items_rank.update({product: value})
                # If we are populating the utility matrix for cities, we need to consider the cities
                else:
                    city = trip._from
                    value = items_rank.get(city) + drivers_exp.get(
                        actual_route.driver_id
                    )
                    items_rank.update({city: value})

            if not is_merch:
                value = items_rank.get(trip.to) + drivers_exp.get(
                    actual_route.driver_id
                )
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

    # Now we create the tuple of liked cities for each standard route
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


def enumerate_cities_products(
    utility_matrix: Dict[str, Dict[str, float]]
) -> Dict[int, str]:
    col_map_dict: Dict[int, str] = {}
    route: Dict[str, float] = utility_matrix.get("s0")
    for i, item in enumerate(route):
        col_map_dict.update({i: item})

    return col_map_dict


def matrix_dict_to_list(
    utility_matrix: Dict[str, Dict[str, float]]
) -> List[List[float]]:
    matrix: List[List[float]] = []
    for route, merch_dict in utility_matrix.items():
        row: List[float] = []
        for merch, value in merch_dict.items():
            row.append(value)
        matrix.append(row)

    return matrix


def compute_svd_reconstruct_matrix(res_matrix) -> ndarray:
    # Apply SVD
    svd = TruncatedSVD(n_components=2, n_iter=params.N_ITERS, random_state=42)
    svd.fit(res_matrix)
    res_matrix = svd.transform(res_matrix)

    # Reconstruct the matrix
    return np.dot(res_matrix, svd.components_)


def complete_reconstructed_matrix(
    np_matrix: ndarray, reconstructed_matrix: ndarray
) -> ndarray:
    filled_matrix = np_matrix.copy()
    # Iterate through the original matrix and replace missing values with corresponding values from the reconstructed matrix
    for i in range(np_matrix.shape[0]):
        for j in range(np_matrix.shape[1]):
            if np_matrix[i, j] == 0:  # Assuming 0 represents a missing value
                filled_matrix[i, j] = reconstructed_matrix[i, j]

    abs_matrix: ndarray = np.abs(filled_matrix)

    return abs_matrix


# Takes the completed matrix (by SVD) and converts it to a dictionary
def list_to_ditc_matrix(
    filled_matrix: List[List[float]], col_map_dict: Dict[int, str]
) -> Dict[str, Dict[str, float]]:
    complete_utility_matrix: Dict[str, Dict[str, float]] = {}
    for i, row in enumerate(filled_matrix):
        dict_row: Dict[str, float] = {}
        for j, value in enumerate(row):
            dict_row.update({col_map_dict.get(j): value})
        complete_utility_matrix.update({f"s{i}": dict_row})

    return complete_utility_matrix


# Takes in a utility matrix as input, applies Singular Value
# Decomposition (SVD) to reconstruct the matrix, fills in missing values in the reconstructed matrix,
# and returns the completed utility matrix as a dictionary.
def complete_utility_matrix(
    utility_matrix: Dict[str, Dict[str, float]]
) -> Dict[str, Dict[str, float]]:
    # Mapping string to int for the columns
    col_map_dict: Dict[int, str] = enumerate_cities_products(utility_matrix)

    # Create a matrix containg the values of the utility matrix
    matrix: List[List[float]] = matrix_dict_to_list(utility_matrix)

    # Convert the matrix to a numpy array
    np_matrix = np.array(matrix)

    # Convert np array to csr matrix (compressed sparse row matrix)
    res_matrix = csr_matrix(np_matrix)

    # Apply SVD and reconstruct the matrix
    reconstructed_matrix: ndarray = compute_svd_reconstruct_matrix(res_matrix)

    # Fill the missing values in the reconstructed matrix
    filled_matrix: List[List[float]] = complete_reconstructed_matrix(
        np_matrix, reconstructed_matrix
    )

    # Convert the matrix to a dictionary
    complete_utility_matrix = list_to_ditc_matrix(filled_matrix, col_map_dict)

    return complete_utility_matrix


# Common functions for cities and products
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

    # Get for each standard route, all its actual routes
    std_to_actuals: Dict[str, List[ActRoute]] = std_to_actuals_dict(
        std_routes, act_routes
    )

    return std_routes, act_routes, drivers_exp, std_to_actuals


def cities(
    std_routes: List[StdRoute],
    act_routes: List[ActRoute],
    drivers_exp: Dict[str, float],
    std_to_actuals: Dict[str, List[ActRoute]],
) -> Dict[str, Tuple[List[str], List[str]]]:
    # Get all cities ever visited
    all_cities: Dict[str, float] = init_cities_dict(std_routes, act_routes)

    # Populate the utility matrix for reccomendation system
    utility_matrix: Dict[str, Dict[str, float]] = populate_utility_matrix(
        drivers_exp, std_to_actuals, all_cities
    )

    complete_matrix: Dict[str, Dict[str, float]] = complete_utility_matrix(
        utility_matrix
    )

    # the first element of the Tuple is the list of liked cities, the second is the list of disliked cities
    liked_disliked_cities: Dict[
        str, Tuple[List[str], List[str]]
    ] = get_liked_disliked_items(complete_matrix)

    return liked_disliked_cities


def products(
    std_routes: List[StdRoute],
    act_routes: List[ActRoute],
    drivers_exp: Dict[str, float],
    std_to_actuals: Dict[str, List[ActRoute]],
):
    # Get all cities ever visited
    all_products: Dict[str, float] = init_products_dict(std_routes, act_routes)

    # Populate the utility matrix for reccomendation system
    utility_matrix: Dict[str, Dict[str, float]] = populate_utility_matrix(
        drivers_exp, std_to_actuals, all_products, True
    )

    complete_matrix: Dict[str, Dict[str, float]] = complete_utility_matrix(
        utility_matrix
    )

    # the first element of the Tuple is the list of liked cities, the second is the list of disliked cities
    liked_disliked_cities: Dict[
        str, Tuple[List[str], List[str]]
    ] = get_liked_disliked_items(complete_matrix)

    return liked_disliked_cities

#TODO: farla
def generate_rec_std(
    liked_disliked_cities: Dict[str, Tuple[List[str], List[str]]],
    liked_disliked_merch: Dict[str, Tuple[List[str], List[str]]],
) -> None:
    pass


def point_1() -> None:
    # Some common function calls
    std_routes, act_routes, drivers_exp, std_to_actuals = common_fn_call()

    liked_disliked_cities: Dict[str, Tuple[List[str], List[str]]] = cities(
        std_routes, act_routes, drivers_exp, std_to_actuals
    )
    print("  - Done liked disliked cities")

    liked_disliked_merch: Dict[str, Tuple[List[str], List[str]]] = products(
        std_routes, act_routes, drivers_exp, std_to_actuals
    )
    print("  - Done liked disliked merch")

    # modifica la std route e ogni volta che trova una città che non ci piace la sostituisce con una città che ci piace di più
    # salva la rec standard in un file json
    generate_rec_std(liked_disliked_cities, liked_disliked_merch)
    print("  - Done generating rec standard")


if __name__ == "__main__":
    point_1()

    # prendiamo per ogni standard, tutte le sue actual e contiamo le occorrenze delle città e creiamo una matrice standardRoute x città
    # scegliamo le n città più frequenti e le k meno frequenti e le aggiungiamo / togliamo alla standard route per tenerla di lunghezza simile
    # Per i prodotti è uguale
