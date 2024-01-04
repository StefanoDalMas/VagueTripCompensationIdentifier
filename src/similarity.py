from typing import List, Dict, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from classes.Trip import Trip
from classes.ActRoute import ActRoute
from classes.StdRoute import StdRoute
from classes.DriverRoutesSimilarity import DriverRoutesSimilarity
from tools.parameters import Parameters as params
from actRoute_generator import getStdRoutes, getActRoutes


def dict_padding(stdTrip: Trip, ActTrip: Trip) -> Tuple[Trip, Trip]:
    keys_to_ensure = set(stdTrip.merchandise.keys()) | set(ActTrip.merchandise.keys())

    for key in keys_to_ensure:
        if key not in stdTrip.merchandise:
            stdTrip.merchandise[key] = 0
        if key not in ActTrip.merchandise:
            ActTrip.merchandise[key] = 0

    return stdTrip, ActTrip


# Calculate the similarity of merch between two trips (cosine similarity)
def trip_merch_similarity(stdTrip: Trip, actTrip: Trip):
    stdTrip, actTrip = dict_padding(stdTrip, actTrip)

    merchandise1 = np.array(list(stdTrip.merchandise.values()))
    merchandise2 = np.array(list(actTrip.merchandise.values()))

    # check if merchandise2 is an arry of zeros
    if np.all(merchandise2 == 0):
        return 1.0

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
def route_similarity(stdRoute: StdRoute, actRoute: ActRoute) -> float:
    similarity = 0.0
    penality = 0.0

    route_std = stdRoute.route
    route_act = actRoute.aRoute
    i, j = 0, 0

    while i < len(route_std) and j < len(route_act):
        # If the two routes have the same from
        if route_std[i]._from == route_act[j]._from:
            similarity += (
                1
                - trip_merch_similarity(route_std[i], route_act[j])
                * params.MERCH_PENALITY
            )
            i += 1
            j += 1

        else:
            window_cities = []
            window_index = j + 1
            counter = 0
            while counter < params.MAX_WINDOW_SIZE and window_index < len(route_act):
                # Keep adding cities to the window until the next city is the same as the city in the standard route
                if route_std[i]._from != route_act[window_index]._from:
                    window_cities.append(route_act[window_index]._from)
                    window_index += 1
                    counter += 1
                else:
                    penality += len(window_cities) * params.MODIFY_PENALITY
                    # Doesn't make sense because we generate the new city with random values
                    # similarity += 1 - trip_merch_similarity(route_std[i], route_act[j]) * MERCH_PENALITY
                    i += 1
                    j += 1
                    break

            if counter == params.MAX_WINDOW_SIZE or window_index == len(route_act):
                penality += params.DELETE_PENALITY
                i += 1
                j += 1

    if len(route_act) > len(route_std):
        penality += (len(route_act) - len(route_std)) * params.MODIFY_PENALITY

    max = len(route_std) if len(route_std) > len(route_act) else len(route_act)

    return (penality + similarity) / max


# TODO: save results in dictionary
# {driver5, {route5:0.9, route6:0.8, route7:0.7}}
def generate_similarities() -> Dict[str,Dict[str,float]]:
    std_routes: List[StdRoute] = getStdRoutes()
    act_routes: List[ActRoute] = getActRoutes()

    driver_sim: Dict[str,Dict[str,float]] = {}
    # find corresponding route
    for i in range(len(act_routes)):
        id = act_routes[i].sRoute_id
        std_route = None
        for j in range(len(std_routes)):
            if std_routes[j].id == id:
                std_route = std_routes[j]
                break
        # compute similarity and add it to the list
        if std_route != None:
            if act_routes[i].driver_id in driver_sim:
                driver_sim[act_routes[i].driver_id].update({act_routes[i].sRoute_id: route_similarity(std_route, act_routes[i])})
            else:
                driver_sim.update({act_routes[i].driver_id:{act_routes[i].sRoute_id: route_similarity(std_route, act_routes[i])}})
        else:
            raise Exception("Standard route not found")

    # Convert the dictionary to a list of tuple
    return driver_sim


if __name__ == "__main__":
    results = generate_similarities()
    print(results)
