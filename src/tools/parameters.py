from tools.cities_products import italian_cities as ic
from tools.cities_products import shopping_list as sl


class Parameters:

    DEBUG: bool = False 
    # Standard routes
    ENTRIES: int = 2000
    MINTRIP: int = 10
    MAXTRIP: int = 30
    MINPRODUCTS: int = 1
    MAXPRODUCTS: int = 2

    # Paths
    SROUTES_FILENAME: str = "standard.json"
    AROUTES_FILENAME: str = "actual.json"
    DRIVERS_FILENAME: str = "drivers.json"

    # Drivers
    N_DRIVERS = 40
    MAX_LIKED_CITIES: int = int(len(ic)*0.3)
    MIN_LIKED_CITIES: int = 4 # do not lower this value under 4!!!
    MAX_DISLIKED_CITIES: int = int(len(ic)*0.3)
    MAX_LIKED_PRODUCTS: int = int(len(sl)*0.3)
    MAX_DISLIKED_PRODUCTS: int = int(len(sl)*0.3)

    # Actual routes
    MIN_ROUTES_TO_DRIVERS: int = 40
    MAX_ROUTES_TO_DRIVERS: int = 100
    CAP_ADD_NEW_CITY: int = 70
