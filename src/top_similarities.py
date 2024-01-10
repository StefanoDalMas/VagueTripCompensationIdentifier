import json
import os
from typing import List, Dict, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from classes.Trip import Trip
from classes.ActRoute import ActRoute
from classes.StdRoute import StdRoute
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


def generate_similarities() -> params.driverSimilarities:
    std_routes: List[StdRoute] = getStdRoutes()
    act_routes: List[ActRoute] = getActRoutes()

    driver_sim: params.driverSimilarities = {}
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
                driver_sim[act_routes[i].driver_id].update(
                    {
                        act_routes[i].sRoute_id: route_similarity(
                            std_route, act_routes[i]
                        )
                    }
                )
            else:
                driver_sim.update(
                    {
                        act_routes[i].driver_id: {
                            act_routes[i].sRoute_id: route_similarity(
                                std_route, act_routes[i]
                            )
                        }
                    }
                )
        else:
            raise Exception("Standard route not found")

    # Convert the dictionary to a list of tuple
    return driver_sim


def generate_top_5_similarities(
    sim_drivers_routes: Dict[str, Dict[str, float]]
) -> Dict[str, Dict[str, float]]:
    top_5_similarities = {}
    for driver, routes in sim_drivers_routes.items():
        sorted_routes = sorted(routes.items(), key=lambda x: x[1], reverse=True)
        top_5_similarities[driver] = dict(sorted_routes[:5])
    return top_5_similarities


def save_results(top_5_dict: params.driverSimilarities) -> None:
    # print in a file called "driver.json" something like this
    # [
    # {driver:C, routes:[s10, s20, s2, s6, s10}},
    # {driver:A, routes:[s1, s2, s22, s61, s102]},
    # ….
    # ]
    result = []
    for driver_id, route_data in top_5_dict.items():
        result.append({"driver": driver_id, "routes": list(route_data.keys())})
    if not os.path.exists("./results"):
        os.makedirs("./results")
    with open("./results/driver.json", "w") as f:
        json.dump(result, f, indent=4)


# Point 2 of the assignment
def point_2() -> None:
    # Use online algorithm (window) to evaluate the existence of a city in a route
    sim_drivers_routes: params.driverSimilarities = generate_similarities()
    print("  - Done generating similarities")

    top_5_dict: params.driverSimilarities = generate_top_5_similarities(
        sim_drivers_routes
    )
    print("  - Done generating top 5 similarities")

    save_results(top_5_dict)
    print("  - Done generating driver.json")


if __name__ == "__main__":
    point_2()
