# system imports
from typing import Dict
import numpy as np


class Trip:
    _from: str = ""
    to: str = ""
    merchandise: Dict[str, int] = {}

    def __init__(self, _from: str, to: str, merchandise: Dict[str, int]) -> None:
        self._from = _from
        self.to = to
        self.merchandise = merchandise

    def __str__(self):
        merchandise_str = " ".join(
            [f"{key}: {value}" for key, value in self.merchandise.items()]
        )
        return f"from: {self._from}\nto: {self.to}\nMerchandise:\n{merchandise_str}\n"

    def to_dict(self):
        return {"from": self._from, "to": self.to, "merchandise": self.merchandise}

    def is_empty(self):
        if self._from == "" and self.to == "" and self.merchandise == {}:
            return True
        return False

    def dict_to_vector(self):
        # Estrai le chiavi e i valori dal dizionario
        keys = list(self.merchandise.keys())
        values = list(self.merchandise.values())

        # Crea un vettore NumPy
        vector = np.zeros(len(keys), dtype=int)

        # Assegna i valori alle posizioni corrispondenti nel vettore
        for key, value in zip(keys, values):
            vector[int(key)] = value

        return vector
