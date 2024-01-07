import json
import os
from typing import Dict, List, Tuple
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
def calculate_liked_cities(driver_actuals: params.driverActuals) -> params.driverCalLikedCities:
    std_routes: List[StdRoute] = getStdRoutes()
    driver_liked_cities: Dict[str, Dict[str, int]] = {}

    actual_dict: Dict[str, int] = {}
    standard_dict: Dict[str, int] = {}
    calculated_liked_cities: Dict[str, int] = {}

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

           
            # facciamo sottrazione tra i dizionari e la aggiungiamo al totale
            calculated_liked_cities = update_dict(calculated_liked_cities, dict_difference(actual_dict, standard_dict))




        # crea threshold per decidere se città è buona o meno
        max_value = max(calculated_liked_cities.values())
        threshold = int(max_value * params.THRESHOLD_MOLTIPLICATOR)


        calc_liked_cities_thr_tuple: Tuple[Dict[str, int], int] = (calculated_liked_cities, threshold)
            
        driver_liked_cities.update({driver: calc_liked_cities_thr_tuple})

        threshold = 0
        actual_dict = {}
        standard_dict = {}
        calculated_liked_cities = {}
        calc_liked_cities_thr_tuple = {}

    return driver_liked_cities

def dict_difference(dict1: Dict[str, int], dict2: Dict[str, int]) -> Dict[str, int]:
    result = {}
    for item in dict1:
        if item in dict2:
            if dict1.get(item) - dict2.get(item) > 0:
                result.update({item: dict1.get(item) - dict2.get(item)})

    return result

def update_dict(dict1: Dict[str, int], dict2: Dict[str, int]) -> Dict[str, int]:
    if dict1 == None and dict2 == None:
        return {}
    else:
        if (dict1 == None):
            return dict2
        if (dict2 == None):
            return dict1
        
        keys_set = set(dict1) | set(dict2)
        for key in keys_set:
            dict1.update({key: (dict1.get(key, 0) + dict2.get(key, 0))})
        return dict1


if __name__ == "__main__":
    # dict[0] -> dictionary, dict[1] -> threshold
    dict = calculate_liked_cities(get_driver_actuals())
    print("stop")