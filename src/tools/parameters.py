from tools.cities_products import italian_cities as ic
from tools.cities_products import shopping_list as sl


class Parameters:
    ENTRIES=10
    MINTRIP=10
    MAXTRIP=30
    MINPRODUCTS=5
    MAXPRODUCTS=50
    SROUTES_FILENAME="standard.json"
    AROUTES_FILENAME="actual.json"
    DRIVERS_FILENAME="drivers.json"
    N_DRIVERS = 5
    MAX_LIKED_CITIES = int(len(ic)*0.3)
    MAX_DISLIKED_CITIES = int(len(ic)*0.3)
    MAX_LIKED_PRODUCTS = int(len(sl)*0.3)
    MAX_DISLIKED_PRODUCTS = int(len(sl)*0.3)
