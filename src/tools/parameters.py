import numpy as np
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
    ENTRIES: int = 60
    MINTRIP: int = 100
    MAXTRIP: int = 200
    MINPRODUCTS: int = 100
    MAXPRODUCTS: int = 200
    # MIN_RANDOM_VALUE = 2 # Minimum value for every product
    # MAX_RANDOM_VALUE = 30 # Maximum value for every product

    # Paths
    SROUTES_FILENAME: str = "standard.json"
    AROUTES_FILENAME: str = "actual.json"
    DRIVERS_FILENAME: str = "drivers.json"

    # Drivers
    N_DRIVERS = 50
    crazyness = np.random.randint(0, 101) # Default 0, 101
    CITY_CRAZINESS = crazyness # Default 0, 101
    PRODUCT_CRAZINESS = crazyness # Default 0, 101
    MAX_LIKED_CITIES: int = int(len(ic)*0.3)
    MIN_LIKED_CITIES: int = 4 # do not lower this value under 4!!!
    MIN_CITIES: int = 4 # do not lower this value under 4!!!
    MAX_CITIES: int = int(len(ic)*0.3)
    MAX_LIKED_PRODUCTS: int = int(len(sl)*0.3)
    MAX_DISLIKED_PRODUCTS: int = int(len(sl)*0.3)

    # Actual routes
    MIN_ROUTES_TO_DRIVERS: int = 20
    MAX_ROUTES_TO_DRIVERS: int = 45
    CAP_ADD_NEW_CITY: int = 70
    #Products
    MIN_PRODUCTS_TO_ADD: int = 20
    MAX_PRODUCTS_TO_ADD: int = 80
    CAP_TO_MODIFY_PRODUCT: int = 60

    # Similarity
    MERCH_PENALITY = 0.15
    DELETE_PENALITY = 0.7
    MODIFY_PENALITY = 0.3
    MAX_WINDOW_SIZE = 100

    # Threshold
    THRESHOLD_MOLTIPLICATOR = 0.38

    # Point 1 Truncated SVD
    N_ITERS = 5 # Number of iterations for the truncated SVD
    PROD_VALUE_MULTIPLICATOR = 0.3 # Multiplicator for the merch value

    # Point 3 apriori
    MIN_SUPPORT = 0.05
    MIN_LIFT = 1
