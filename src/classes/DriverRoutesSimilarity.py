from typing import List, Dict

# {driver5, {route5:0.9, route6:0.8, route7:0.7}} 
class DriverRoutesSimilarity():
    driver_id:str
    routes_to_similarity:Dict[str,float]

    def __init__(self, driver_id: str, routes_to_similarity: Dict[str,float]) -> None:
        self.driver_id = driver_id
        self.routes_to_similarity = routes_to_similarity

    def __str__(self):
        return f"Driver {self.driver_id} routes similarity: {self.routes_to_similarity.items()}"

    def to_dict(self):
        return {
            "driver": self.driver_id,
            "routes": self.routes_to_similarity
        }