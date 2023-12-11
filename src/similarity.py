import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from classes.Trip import Trip
from typing import List

def calculate_similarity(stdTrip: Trip, actTrip: Trip):
    # Estrai le merci trasportate
    merchandise1 = np.array(list(stdTrip.merchandise.values()))
    merchandise2 = np.array(list(actTrip.merchandise.values()))

    # Trova la lunghezza massima tra i due vettori
    max_length = max(len(merchandise1), len(merchandise2))

    # Aggiungi zeri per allineare le lunghezze dei vettori
    merchandise1 = np.pad(merchandise1, (0, max_length - len(merchandise1)), 'constant')
    merchandise2 = np.pad(merchandise2, (0, max_length - len(merchandise2)), 'constant')

    # Normalizza i vettori
    norm_merchandise1 = merchandise1 / np.linalg.norm(merchandise1)
    norm_merchandise2 = merchandise2 / np.linalg.norm(merchandise2)

    # Calcola la similarità coseno
    similarity = cosine_similarity([norm_merchandise1.flatten()], [norm_merchandise2.flatten()])[0, 0]

    return similarity

# Esempio di utilizzo
stdTrip = Trip("", "", {"w": 1, "f": 2, "n": 16, "a": 100})
actTrip = Trip("", "", {"a": 1, "f": 234, "n": 16, "w": 9999, "s": 45})

print(calculate_similarity(stdTrip, actTrip))
