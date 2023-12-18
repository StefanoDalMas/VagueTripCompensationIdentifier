import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from classes.Trip import Trip


def dict_padding(stdTrip: Trip, ActTrip: Trip) -> (Trip, Trip):
    keys_to_ensure = set(stdTrip.merchandise.keys()) | set(ActTrip.merchandise.keys())

    for key in keys_to_ensure:
        if key not in stdTrip.merchandise:
            stdTrip.merchandise[key] = 0
        if key not in ActTrip.merchandise:
            ActTrip.merchandise[key] = 0

    return stdTrip, ActTrip


# Calculate the similarity of merch between two trips (cosine similarity)
def trip_merch_similarity(stdTrip: Trip, actTrip: Trip):
    merchandise1 = np.array(list(stdTrip.merchandise.values()))
    merchandise2 = np.array(list(actTrip.merchandise.values()))

    # Sort the merchandise based on the keys
    merchandise1 = merchandise1[np.argsort(list(stdTrip.merchandise.keys()))]
    merchandise2 = merchandise2[np.argsort(list(actTrip.merchandise.keys()))]

    # Normalize vectors
    norm_merchandise1 = merchandise1 / np.linalg.norm(merchandise1)
    norm_merchandise2 = merchandise2 / np.linalg.norm(merchandise2)

    # Calculate cosine similarity
    similarity = cosine_similarity([norm_merchandise1], [norm_merchandise2])[0, 0]

    return similarity


# Calculate the similarity of routes between two routes
def route_similarity(stdTrip: Trip, actTrip: Trip):
    return 0


if __name__ == "__main__":
    stdTrip = Trip("", "", {"w": 1000, "f": 2, "n": 16, "a": 100})
    actTrip = Trip("", "", {"w": 1000, "f": 2, "z": 50, "n": 16, "l": 1000})

    stdTrip, actTrip = dict_padding(stdTrip, actTrip)

    print("Similarity: " + str(trip_merch_similarity(stdTrip, actTrip)))
