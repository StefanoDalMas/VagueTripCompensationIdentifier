import json
import os
from typing import Dict, List, Tuple, Any
from classes.Trip import Trip
from classes.ActRoute import ActRoute
from classes.StdRoute import StdRoute
from tools.parameters import Parameters as params
from similarity import generate_similarities
from actRoute_generator import getStdRoutes, getActRoutes
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd

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
def calculate_liked_cities(
    driver_actuals: params.driverActuals,
) -> Dict[str, List[str]]:
    std_routes: List[StdRoute] = getStdRoutes()
    driver_liked_cities: params.driverCalLikedCities = {}

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

                actual_dict.update({trip._from: value})

            # contiamo le città della standard associata
            std_id = actual.sRoute_id
            for standard in std_routes:
                if standard.id == std_id:
                    for trip in standard.route:
                        value = 1
                        if trip._from in standard_dict:
                            value = standard_dict.get(trip._from)
                            value += 1

                        standard_dict.update({trip._from: value})

            # facciamo sottrazione tra i dizionari e la aggiungiamo al totale
            calculated_liked_cities = update_dict(
                calculated_liked_cities, dict_difference(actual_dict, standard_dict)
            )

        # crea threshold per decidere se città è buona o meno
        max_value = max(calculated_liked_cities.values())
        threshold = int(max_value * params.THRESHOLD_MOLTIPLICATOR)

        calc_liked_cities_thr_tuple: Tuple[Dict[str, int], int] = (
            calculated_liked_cities,
            threshold,
        )

        driver_liked_cities.update({driver: calc_liked_cities_thr_tuple})

        threshold = 0
        actual_dict = {}
        standard_dict = {}
        calculated_liked_cities = {}
        calc_liked_cities_thr_tuple = {}

    return get_favourite_cities_dict(driver_liked_cities)


def dict_difference(dict1: Dict[str, int], dict2: Dict[str, int]) -> Dict[str, int]:
    result: Dict[str, int] = {}
    for item in dict1:
        if item in dict2:
            if dict1.get(item) - dict2.get(item) > 0:
                result.update({item: dict1.get(item) - dict2.get(item)})

    return result


def update_dict(dict1: Dict[str, int], dict2: Dict[str, int]) -> Dict[str, int]:
    if dict1 == None and dict2 == None:
        return {}
    else:
        if dict1 == None:
            return dict2
        if dict2 == None:
            return dict1

        keys_set = set(dict1) | set(dict2)
        for key in keys_set:
            dict1.update({key: (dict1.get(key, 0) + dict2.get(key, 0))})
        return dict1


def get_favourite_cities_dict(
    dict: params.driverCalLikedCities,
) -> Dict[str, List[str]]:
    res_dict: Dict[str, List[str]] = {}
    for driver, tuple in dict.items():
        res_list: List[str] = []
        for city, occurrencies in tuple[0].items():
            if occurrencies > tuple[1]:
                res_list.append(city)
        res_dict.update({driver: res_list})
    return res_dict


def calculate_liked_merchandise(
    driver_actuals: params.driverActuals,
) -> Dict[str, List[Any]]:
    dict_all_merch: Dict[str, List[List[str]]] = {}
    act_routes_list : List[List[List[str]]] = []
    route_list: List[List[str]] = []
    for (
        driver,
        actual_list,
    ) in driver_actuals.items():  # {driver: [ActRoute,ActRoute,...]]}
        for actual in actual_list:  # [ActRoute,ActRoute,...]
            trip_list: List[str] = []  # [beer,wine,diapers,nuts,...]
            for trip in actual.aRoute:  # [Trip,Trip,...]
                for merch in trip.merchandise.keys():  # [beer,wine,diapers,nuts,...]
                    trip_list.append(merch)
                route_list.append(trip_list)  # [[beer,wine,diapers],[chips],...]
                trip_list = []
            act_routes_list.append(route_list)
            route_list = []
        dict_all_merch.update({driver: act_routes_list})
        route_list = []

    # for each driver apply the apriori to the baskets of all merchandise of all routes taken by him
    for driver, routes_list in dict_all_merch.items():
        # slice the list to get only the first 20 routes
        # transactions = transactions[:100]
        for transactions in routes_list:
            te = TransactionEncoder()
            te_ary = te.fit(transactions).transform(transactions)
            df = pd.DataFrame(te_ary, columns=te.columns_)
            frequent_itemsets = apriori(df, min_support=0.05, use_colnames=True,verbose=1,low_memory=True)

            # Generate association rules
            rules = association_rules(
                frequent_itemsets, metric="confidence", min_threshold=0.1
            )

            print("Frequent Itemsets:")
            print(frequent_itemsets)

            print("\nAssociation Rules:")
            print(rules)
    #     dict_all_merch.update({driver: rules})

    return dict_all_merch


if __name__ == "__main__":
    # dict[0] -> dictionary, dict[1] -> threshold
    fav_cities: Dict[str, List[str]] = calculate_liked_cities(get_driver_actuals())

    # next step : get best merchandise for each driver
    # get all actrouts for each driver
    # for each route, get all trips and convert each merch in a list
    # make all baskets of a route a list of lists [[beer,wine],[diapers,nuts],...]
    # use apriori to get best merchandise

    fav_merchandise: Dict[str, List[Any]] = calculate_liked_merchandise(
        get_driver_actuals()
    )

    # make me a test matrix with data like this [["milk","wine","beer"],["beer","diapers"],...]
    # take a lot of things like beer, coke, flour, and so on

    print("stop")
    # next step : generate perfect route using fav_cities and fav_merchandise
