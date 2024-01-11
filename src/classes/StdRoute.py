# system imports
from typing import List, Dict, Tuple 

# custom imports
from classes.Trip import Trip

class StdRoute():

    def __init__(self, id:str, route:List[Trip]) -> None:
        self.id = id
        self.route = route

    def __str__(self):
        route_str = "["+" ".join(map(str, self.route))+"]"
        return f"id: {self.id}\nsRoute: \n{route_str}\n"

    def to_dict(self):
        return {
            "id": self.id,
            "route": [trip.to_dict() for trip in self.route],
        }
