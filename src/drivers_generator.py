from typing import List, Dict, Tuple 
import numpy as np
from tools.cities_products import italian_cities as ic
from tools.cities_products import shopping_list as sl
import json
from classes.Driver import Driver

# used to cast ndarrays in lists
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

N_DRIVERS = 5
DRIVERS_FILENAME = "drivers.json"
MAX_LIKED_CITIES = int(len(ic)*0.3)
MAX_DISLIKED_CITIES = int(len(ic)*0.3)
MAX_LIKED_PRODUCTS = int(len(sl)*0.3)
MAX_DISLIKED_PRODUCTS = int(len(sl)*0.3)


if __name__ == "__main__":

    drivers = []
    for n in range(N_DRIVERS):
        # driver id
        id = n

        # cities-related values
        citiesCrazyness = np.random.randint(0, 101)
        likedCities = np.random.choice(ic, size=np.random.randint(0, MAX_LIKED_CITIES), replace=False)
        icMinusLiked_set = set(ic) - set(likedCities)
        icMinusLiked = list(icMinusLiked_set)
        dislikedCities = np.random.choice(icMinusLiked, size=np.random.randint(0, MAX_DISLIKED_CITIES), replace=False)
        cities_set = set(icMinusLiked) - set(dislikedCities)
        cities = list(cities_set)

        # product-related values
        productCrazyness = np.random.randint(0, 101)
        likedProducts = np.random.choice(sl, size=np.random.randint(0, MAX_LIKED_PRODUCTS), replace=False)
        slMinusLiked_set = set(sl) - set(likedProducts)
        slMinusLiked = list(slMinusLiked_set)
        dislikedProducts = np.random.choice(slMinusLiked, size=np.random.randint(0, MAX_DISLIKED_PRODUCTS), replace=False)
        products_set = set(slMinusLiked) - set(dislikedProducts)
        products = list(products_set)

        # driver creation
        driver = Driver(id, citiesCrazyness, productCrazyness, likedCities, likedProducts,
                        dislikedCities, dislikedProducts, cities, products)
        drivers.append(driver)

        print(f"-DRIVER {n}-")
        print(f"CITIES\n likedCities={len(likedCities)}\n dislikedCities={len(dislikedCities)}\n cities={len(cities)}\n")
        print(f"PRODUCTS\n likedProducts={len(likedProducts)}\n dislikedProducts={len(dislikedProducts)}\n products={len(products)}\n")


    # cast all elements to dictionary
    driver_list_dict = [driver.to_dict() for driver in drivers]

    # print to file
    with open("./data/" + DRIVERS_FILENAME, "w") as f:
        json.dump(driver_list_dict, f, indent=4, cls=NumpyEncoder)