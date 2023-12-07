from tools.cities_products import italian_cities as ic
from tools.cities_products import shopping_list as sl


class Parameters:

    DEBUG: bool = False 
    # Standard routes
    ENTRIES: int = 200
    MINTRIP: int = 10
    MAXTRIP: int = 30
    MINPRODUCTS: int = 1
    MAXPRODUCTS: int = 10
    MIN_RANDOM_VALUE = 2 # Minimum value for every product
    MAX_RANDOM_VALUE = 30 # Maximum value for every product

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
    MIN_ROUTES_TO_DRIVERS: int = 40
    MAX_ROUTES_TO_DRIVERS: int = 100
    CAP_ADD_NEW_CITY: int = 70
    #Products
    MIN_PRODUCTS_TO_ADD: int = 1
    MAX_PRODUCTS_TO_ADD: int = 5
    CAP_TO_MODIFY_PRODUCT: int = 60
