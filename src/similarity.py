import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from classes.Trip import Trip

def calculate_similarity(stdTrip: Trip, actTrip: Trip):
    # Estrai le merci trasportate
    merchandise1 = np.array(list(stdTrip.merchandise.values()))
    merchandise2 = np.array(list(actTrip.merchandise.values()))

    #Sort the merchandise based on the keys
    merchandise1 = merchandise1[np.argsort(list(stdTrip.merchandise.keys()))]
    merchandise2 = merchandise2[np.argsort(list(actTrip.merchandise.keys()))]

    # Normalizza i vettori
    norm_merchandise1 = merchandise1 / np.linalg.norm(merchandise1)
    norm_merchandise2 = merchandise2 / np.linalg.norm(merchandise2)

    # Calcola la similarità coseno
    similarity = cosine_similarity(
        [norm_merchandise1], [norm_merchandise2]
    )[0, 0]

    return similarity

# Esempio di utilizzo
stdTrip = Trip("", "", {"w": 1, "f": 2, "n": 16, "a": 100})
actTrip = Trip("", "", {"w": 1, "f": 2, "a": 100, "n": 16})

print(calculate_similarity(stdTrip, actTrip))
