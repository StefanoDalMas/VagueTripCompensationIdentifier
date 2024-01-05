import json
import os
from typing import Dict, List
from classes.Trip import Trip
from classes.ActRoute import ActRoute
from classes.StdRoute import StdRoute
from tools.parameters import Parameters as params
from similarity import generate_similarities
from actRoute_generator import getStdRoutes, getActRoutes

# {driver: {città: quantità}}

# funzine che restituisca un dizionario con le città e i corrispondenti contatori
# funzione che fa la differenza tra due oggetti descritti sopra



# volgiamo creare una struttura dati che sia così
# {driver: List[ActRoute]}
def get_driver_actuals() -> params.driverActuals:
    act_routes: List[ActRoute] = getActRoutes()

    driver_actuals: params.driverActuals = {}
    # find corresponding route
    for actual in act_routes:
        driver_id = actual.driver_id
        if driver_id in driver_actuals:
            list = driver_actuals.get(driver_id)
            list.append(actual)
            driver_actuals.update({driver_id: list})
        else:
            driver_actuals.update({driver_id: [actual]})

    return driver_actuals


# vogliamo creare questo
#  {driver: {città: quantità}}
def calculate_liked_cities(driver_actuals: params.driverActuals):
    std_routes: List[StdRoute] = getStdRoutes()
    driver_liked_cities: Dict[str, Dict[str, int]]

    actual_dict: Dict[str, int] = {}
    standard_dict: Dict[str, int] = {}

    for driver, actual_list in driver_actuals.items():
        for actual in actual_list:
            # contiamo le città per una actual
            for trip in actual.aRoute:
                value = 1
                if trip._from in actual_dict:
                    value = actual_dict.get(trip._from)
                    value += 1

                actual_dict.update({trip._from: value })
 
            # contiamo le città della standard associata
            std_id = actual.sRoute_id
            for standard in std_routes:
                if standard.id == std_id:
                    for trip in standard.route:
                        value = 1
                        if trip._from in standard_dict:
                            value = standard_dict.get(trip._from)
                            value += 1

                        standard_dict.update({trip._from: value })

            # facciamo sottrazione tra i dizionari
            res = dict_difference(actual_dict, standard_dict)
            print(res)
            # fai funzione dict_difference
            # crea threshold per decidere se città è buona o meno
            # crea threshold partendo da media di numero di città presenti in actual_dict e standard_dict e poi fai media tra le due medie
            # metti una costante nei parametri che indica la percentuale per calcolare la threshold sulla media risultante

    return driver_liked_cities

def dict_difference(dict1, dict2):
    result = {}
    all_keys = set(dict1.keys()).union(dict2.keys())

    for key in all_keys:
        value1 = dict1.get(key, 0)
        value2 = dict2.get(key, 0)
        difference = value1 - value2
        if difference != 0:
            result[key] = difference

    return result

def count_city():
    std_routes: List[StdRoute] = getStdRoutes()
    act_routes: List[ActRoute] = getActRoutes()

    for act_route in act_routes:
        driver = act_route.driver_id



if __name__ == "__main__":
    calculate_liked_cities(get_driver_actuals())