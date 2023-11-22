from typing import List, Dict, Tuple 
import numpy
from tools.cities_products import italian_cities as ic

class Driver():
    crazyProduct: int
    crazyCity: int
    likedCities: List[str]
    likedProducts: List[str]
    dislikedCities: List[str]
    dislikedProducts: List[str]

    def __init__(self, crazyProduct:int, crazyCity:int, likedCities:List[str], likedProducts:List[str], dislikedCities:List[str], dislikedProducts:List[str]) -> None:
        self.crazyProduct = crazyProduct
        self.crazyCity = crazyCity
        self.likedCities = likedCities
        self.likedProducts = likedProducts
        self.dislikedCities = dislikedCities
        self.dislikedProducts = dislikedProducts

    def __str__(self):
        return f"{self.crazyProduct}\n{self.crazyCity}\n{self.likedCities}\n{self.likedProducts}\n{self.dislikedCities}\n{self.dislikedProducts}\n"

N_DRIVERS = 100
DRIVERS_FILENAME = "drivers.json"

if __name__ == "__main__":

    driver = Driver(2,32, ["DSAGF"], ["DSAGF"], ["DSAGF"], ["DSAGF"])

    with open("data/" + DRIVERS_FILENAME, "w") as f:
        for n in range(N_DRIVERS):
            crazyProduct = numpy.random.randint(0, 101)
            crazyCity = numpy.random.randint(0, 101)
            likedCities = random.sample(ic, numpy.random.randint(0, 101))
            likedProducts = 
            dislikedCities = 
            dislikedProducts = 

            driver = Driver(2,32, ["DSAGF"], ["DSAGF"], ["DSAGF"], ["DSAGF"])

    print(driver)