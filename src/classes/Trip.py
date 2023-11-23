# system imports
from typing import List, Dict, Tuple 

class Trip():

    def __init__(self, _from:str, to:str, merchandise:dict) -> None:
        self._from = _from
        self.to = to
        self.merchandise = merchandise

    def __str__(self):
        merchandise_str = " ".join([f"{key}: {value}" for key, value in self.merchandise.items()])
        return f"from: {self._from}\nto: {self.to}\nMerchandise:\n{merchandise_str}\n"

    def to_dict(self):
        return {
            "from": self._from,
            "to": self.to,
            "merchandise": self.merchandise
        }
