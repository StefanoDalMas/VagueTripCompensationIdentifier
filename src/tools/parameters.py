from tools.cities_products import italian_cities as ic
from tools.cities_products import shopping_list as sl


class Parameters:
    # Standard routes
    ENTRIES=20
    MINTRIP=100
    MAXTRIP=300
    MINPRODUCTS=1
    MAXPRODUCTS=2

    # Paths
    SROUTES_FILENAME="standard.json"
    AROUTES_FILENAME="actual.json"
    DRIVERS_FILENAME="drivers.json"

    # Drivers
    N_DRIVERS = 5
    MAX_LIKED_CITIES = int(len(ic)*0.3)
    MAX_DISLIKED_CITIES = int(len(ic)*0.3)
    MAX_LIKED_PRODUCTS = int(len(sl)*0.3)
    MAX_DISLIKED_PRODUCTS = int(len(sl)*0.3)

    # Actual routes
    # N_ACTUAL_ROUTES = 5
    MIN_ROUTES_TO_DRIVERS = 1
    MAX_ROUTES_TO_DRIVERS = 3
