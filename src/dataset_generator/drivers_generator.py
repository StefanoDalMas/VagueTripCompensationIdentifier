from typing import List
import numpy as np
from tools.cities_products import italian_cities as ic
from tools.cities_products import shopping_list as sl
import json
import os
from classes.Driver import Driver
from tools.parameters import Parameters as params


# Used to cast ndarrays in lists
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def drivers_generator() -> List[Driver]:
    drivers: List[Driver] = []
    for n in range(params.N_DRIVERS):
        # Driver id
        id = n

        # Cities-related values
        citiesCrazyness = params.CITY_CRAZINESS
        likedCities = np.random.choice(
            ic,
            size=np.random.randint(params.MIN_LIKED_CITIES, params.MAX_LIKED_CITIES),
            replace=False,
        )
        icMinusLiked_set = set(ic) - set(likedCities)
        icMinusLiked = list(icMinusLiked_set)
        cities = np.random.choice(
            icMinusLiked,
            size=np.random.randint(params.MIN_CITIES, params.MAX_CITIES),
            replace=False,
        )
        dislikedCities_set = set(icMinusLiked) - set(cities)
        dislikedCities = list(dislikedCities_set)

        # Product-related values
        productCrazyness = params.PRODUCT_CRAZINESS
        likedProducts = np.random.choice(
            sl, size=np.random.randint(0, params.MAX_LIKED_PRODUCTS), replace=False
        )
        slMinusLiked_set = set(sl) - set(likedProducts)
        slMinusLiked = list(slMinusLiked_set)
        dislikedProducts = np.random.choice(
            slMinusLiked,
            size=np.random.randint(0, params.MAX_DISLIKED_PRODUCTS),
            replace=False,
        )
        products_set = set(slMinusLiked) - set(dislikedProducts)
        products = list(products_set)

        # Driver creation
        driver = Driver(
            id,
            citiesCrazyness,
            productCrazyness,
            likedCities,
            likedProducts,
            dislikedCities,
            dislikedProducts,
            cities,
            products,
        )
        drivers.append(driver)

    # Cast all elements to dictionary
    driver_list_dict = [driver.to_dict() for driver in drivers]

    # Print to file
    if not os.path.exists("./data"):
        os.makedirs("./data")
    with open("./data/" + params.DRIVERS_FILENAME, "w") as f:
        json.dump(driver_list_dict, f, indent=4, cls=NumpyEncoder)
    return drivers


if __name__ == "__main__":
    drivers_generator()
