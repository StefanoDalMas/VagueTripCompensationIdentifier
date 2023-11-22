from typing import List, Dict, Tuple 
import numpy as np
from tools.cities_products import italian_cities as ic
from tools.cities_products import shopping_list as sl
import json


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Driver():
    id: int
    citiesCrazyness: int
    productCrazyness: int
    likedCities: List[str]
    likedProducts: List[str]
    dislikedCities: List[str]
    dislikedProducts: List[str]
    cities: List[str]
    products: List[str]

    def __init__(self, id:int, productCrazyness:int, citiesCrazyness:int, likedCities:List[str], likedProducts:List[str], dislikedCities:List[str], dislikedProducts:List[str], cities:List[str], products:List[str]) -> None:
        self.id = id
        self.productCrazyness = productCrazyness
        self.citiesCrazyness = citiesCrazyness
        self.likedCities = likedCities
        self.likedProducts = likedProducts
        self.dislikedCities = dislikedCities
        self.dislikedProducts = dislikedProducts
        self.cities = cities
        self.products = products

    def __str__(self):
        return f"{self.id}\n{self.productCrazyness}\n{self.citiesCrazyness}\n{self.likedCities}\n{self.likedProducts}\n{self.dislikedCities}\n{self.dislikedProducts}\n{self.cities}\n{self.products}\n"

    def to_dict(self):
        return {
            "id": self.id,
            "productCrazyness": self.productCrazyness,
            "citiesCrazyness": self.citiesCrazyness,
            "likedCities": self.likedCities,
            "likedProducts": self.likedProducts,
            "dislikedCities": self.dislikedCities,
            "dislikedProducts": self.dislikedProducts,
            "cities": self.cities,
            "products": self.products
        }

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
        driver = Driver(id, productCrazyness, citiesCrazyness, likedCities, likedProducts, dislikedCities, dislikedProducts, cities, products)
        drivers.append(driver)

        print(f"-DRIVER {n}-")
        print(f"CITIES\n likedCities={len(likedCities)}\n dislikedCities={len(dislikedCities)}\n cities={len(cities)}\n")
        print(f"PRODUCTS\n likedProducts={len(likedProducts)}\n dislikedProducts={len(dislikedProducts)}\n products={len(products)}\n")


    # cast all elements to dictionary
    driver_list_dict = [driver.to_dict() for driver in drivers]

    # print to file
    with open("./data/" + DRIVERS_FILENAME, "w") as f:
        json.dump(driver_list_dict, f, indent=4, cls=NumpyEncoder)