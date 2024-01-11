from tools.cities_products import italian_cities as ic
from tools.cities_products import shopping_list as sl
from typing import Dict, List, Tuple
from classes.ActRoute import ActRoute
from typing import Dict


class Parameters:

    #typedefs
    driverSimilarities = Dict[str,Dict[str,float]]
    driverActuals = Dict[str, List[ActRoute]]
    driverCalLikedCities = Dict[str, Tuple[Dict[str, int], int]]

    DEBUG: bool = False 
    # Standard routes
    ENTRIES: int = 20
    MINTRIP: int = 30
    MAXTRIP: int = 65
    MINPRODUCTS: int = 30
    MAXPRODUCTS: int = 100
    # MIN_RANDOM_VALUE = 2 # Minimum value for every product
    # MAX_RANDOM_VALUE = 30 # Maximum value for every product

    # Paths
    SROUTES_FILENAME: str = "standard.json"
    AROUTES_FILENAME: str = "actual.json"
    DRIVERS_FILENAME: str = "drivers.json"

    # Drivers
    N_DRIVERS = 40
    MAX_LIKED_CITIES: int = int(len(ic)*0.3)
    MIN_LIKED_CITIES: int = 4 # do not lower this value under 4!!!
    MIN_CITIES: int = 4 # do not lower this value under 4!!!
    MAX_CITIES: int = int(len(ic)*0.3)
    MAX_LIKED_PRODUCTS: int = int(len(sl)*0.3)
    MAX_DISLIKED_PRODUCTS: int = int(len(sl)*0.3)

    # Actual routes
    MIN_ROUTES_TO_DRIVERS: int = 5
    MAX_ROUTES_TO_DRIVERS: int = 15
    CAP_ADD_NEW_CITY: int = 70
    #Products
    MIN_PRODUCTS_TO_ADD: int = 20
    MAX_PRODUCTS_TO_ADD: int = 80
    CAP_TO_MODIFY_PRODUCT: int = 60

    # Similarity
    MERCH_PENALITY = 0.15
    DELETE_PENALITY = 1.0
    MODIFY_PENALITY = 0.3
    MAX_WINDOW_SIZE = 3

    # Threshold
    THRESHOLD_MOLTIPLICATOR = 0.38

    # Point 3 apriori
    MIN_SUPPORT = 0.03
    MIN_LIFT = 1

    # Point 1 Truncated SVD
    N_ITERS = 5 # Number of iterations for the truncated SVD