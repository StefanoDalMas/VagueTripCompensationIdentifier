from typing import List


class Driver:
    def __init__(
        self,
        id: int,
        citiesCrazyness: int,
        productsCrazyness: int,
        likedCities: List[str],
        likedProducts: List[str],
        dislikedCities: List[str],
        dislikedProducts: List[str],
        cities: List[str],
        products: List[str],
    ) -> None:
        self.id = id
        self.citiesCrazyness = citiesCrazyness
        self.productsCrazyness = productsCrazyness
        self.likedCities = likedCities
        self.likedProducts = likedProducts
        self.dislikedCities = dislikedCities
        self.dislikedProducts = dislikedProducts
        self.cities = cities
        self.products = products

    def __str__(self):
        return f"{self.id}\n{self.citiesCrazyness}\n{self.productsCrazyness}\n{self.likedCities}\n{self.likedProducts}\n{self.dislikedCities}\n{self.dislikedProducts}\n{self.cities}\n{self.products}\n"

    def to_dict(self):
        return {
            "id": self.id,
            "citiesCrazyness": self.citiesCrazyness,
            "productsCrazyness": self.productsCrazyness,
            "likedCities": self.likedCities,
            "likedProducts": self.likedProducts,
            "dislikedCities": self.dislikedCities,
            "dislikedProducts": self.dislikedProducts,
            "cities": self.cities,
            "products": self.products,
        }
