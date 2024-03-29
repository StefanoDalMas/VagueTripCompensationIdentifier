# system imports
from typing import List

# custom imports
from classes.Trip import Trip


class ActRoute:
    def __init__(
        self, id: str, driver_id: str, sRoute_id: str, aRoute: List[Trip]
    ) -> None:
        self.id = id
        self.driver_id = driver_id
        self.sRoute_id = sRoute_id
        self.aRoute = aRoute

    def __str__(self):
        aRoute_str = "[" + " ".join(map(str, self.aRoute)) + "]"
        return f"id: {self.id}\ndriver_id: {self.driver_id}\nsRoute: {self.sRoute_id}\nroute:\n{aRoute_str}\n"

    def to_dict(self):
        return {
            "id": self.id,
            "driver": self.driver_id,
            "sroute": self.sRoute_id,
            "route": [trip.to_dict() for trip in self.aRoute],
        }
