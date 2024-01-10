import heapq
import json
import os
from typing import Dict, List, Tuple, Any, Union
import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.preprocessing import TransactionEncoder
from collections import Counter

from classes.Trip import Trip
from classes.ActRoute import ActRoute
from classes.StdRoute import StdRoute
from tools.parameters import Parameters as params
from top_similarities import generate_similarities
from actRoute_generator import getStdRoutes, getActRoutes
from tools.cities_products import random_item_value


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
            difference: Dict[str, int] = dict_difference(actual_dict, standard_dict)
            if difference != {}:
                calculated_liked_cities = update_dict(
                    calculated_liked_cities, difference
                )
            else:
                calculated_liked_cities = update_dict(
                    calculated_liked_cities, actual_dict
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


# For each driver get all his actual routes and for each route get all trips and convert each merch in a list
def get_drivers_merch(
    driver_actuals: params.driverActuals,
) -> Dict[str, List[List[str]]]:
    dict_all_merch: Dict[str, List[List[str]]] = {}
    act_routes_list: List[List[List[str]]] = []
    route_list: List[List[str]] = []
    trip_list: List[str] = []  # [beer,wine,diapers,nuts,...]
    for (
        driver,
        actual_list,
    ) in driver_actuals.items():  # {driver: [ActRoute,ActRoute,...]]}
        for actual in actual_list:  # [ActRoute,ActRoute,...]
            for trip in actual.aRoute:  # [Trip,Trip,...]
                for merch in trip.merchandise.keys():  # [beer,wine,diapers,nuts,...]
                    trip_list.append(merch)
                route_list.append(trip_list)  # [[beer,wine,diapers],[chips],...]
                trip_list = []
            act_routes_list.append(route_list)
            route_list = []
        dict_all_merch.update({driver: act_routes_list})
        act_routes_list = []

    return dict_all_merch


def frozenset_to_list(frozenset):
    new_list: List[str] = []
    for item in frozenset:
        new_list.append(item)
    return new_list


def rules_to_dict(rules: List[Tuple[str, str]]) -> Dict[str, List[Tuple[str, str]]]:
    antecedents = rules["antecedents"]
    consequents = rules["consequents"]

    # Convert frozenset to list
    antecedents_list: List[str] = []
    for antecedent_set in antecedents:
        antecedents_list.append(frozenset_to_list(antecedent_set))

    # Convert frozenset to list
    consequents_list: List[str] = []
    for consequents_set in consequents:
        consequents_list.append(frozenset_to_list(consequents_set))

    # Create list of rules
    rules_driver_list: List[Tuple[str, str]] = []
    for i in range(len(antecedents_list)):
        rule = (antecedents_list[i], consequents_list[i])
        # Check that the rule is not already in the list
        if (
            rule not in rules_driver_list
        ):  # MANCA DA CAPIRE COME CONTROLLARE E TOGLIERE I DUPLICATI (FATTO)
            rules_driver_list.append(rule)

    return rules_driver_list


# For each driver apply the apriori to the baskets of all merchandise of all routes taken by him
def find_ass_rules(
    dict_all_merch: Dict[str, List[List[str]]]
) -> Dict[str, List[Tuple[str, str]]]:
    dict_rules: Dict[str, List[Tuple[str, str]]] = {}
    for driver, routes_list in dict_all_merch.items():
        transactions = []
        for route in routes_list:
            for trip_list in route:
                transactions.append(trip_list)

        # Transaction Encoding
        te = TransactionEncoder()
        te_ary = te.fit(transactions).transform(transactions)
        df = pd.DataFrame(te_ary, columns=te.columns_)

        # Generate frequent itemsets
        frequent_itemsets = fpgrowth(
            df, min_support=params.MIN_SUPPORT, use_colnames=True
        )  # Adjust min_support

        if frequent_itemsets.empty:
            continue

        # Generate association rules
        rules = association_rules(
            frequent_itemsets, metric="lift", min_threshold=params.MIN_LIFT
        )

        # For each driver we have a list of rules [(antecedents, consequents), ...]
        dict_rules.update({driver: rules_to_dict(rules)})

    return dict_rules


def calculate_liked_merchandise(
    driver_actuals: params.driverActuals,
) -> Dict[str, List[Tuple[str, str]]]:
    # For each driver get all his actual routes and for each route get all trips and convert each merch in a list
    dict_all_merch = get_drivers_merch(driver_actuals)

    # For each driver apply the apriori to the baskets of all merchandise of all routes taken by him
    dict_rules: Dict[str, List[Tuple[str, str]]] = find_ass_rules(dict_all_merch)

    # DIREI DI CAMBIARE NOME A QUESTA FUNZIONE TIPO IN calculate_rules PERCHÈ È GIÀ TROPPO GRANDE
    # POI SE NE FA UN'ALTRA DOVE SI PRENDONO LE REGOLE E SI BUTTA FUORI Dict[driver, [liked cities]]

    return dict_rules


def calculate_route_lenght(
    driver_actuals: params.driverActuals, std_routes: List[StdRoute]
) -> Dict[str, int]:
    # contatore che tiene traccia di quante volte aumenta dimensione (o diminuisce)
    # calcola per ogni coppia actual-standard la percentuale di aumento/diminuzione
    # fai la media tra tutte le percentuali di aumento/diminuzione per ogni driver
    # se aumenta più volte, allora aggiungi alla media la percentuale risultante, se no sottraila

    # if positive -> bigger number of increasing routes
    # if negative -> bigger number of decreasing routes
    driver_len_dict: Dict[str, int] = {}
    counter = 0
    perc_diff = 0
    total_perc_diff = 0
    actual_total_lenght = 0  # used to calculate the base distance. Then we add/substract the mean difference between actual and standard
    total_perc_diff_mean = 0
    actual_mean_lenght = 0
    for driver, actual_list in driver_actuals.items():
        for actual in actual_list:
            actual_total_lenght += len(actual.aRoute)
            std_id = actual.sRoute_id
            for standard in std_routes:
                if standard.id == std_id:
                    # DA LEGGERE
                    # nel calcolo di perc_diff ho messo .. / min() per contrastare il problema che vi dicevo nell'audio
                    # esempio
                    #       len(actual)     len(standard)
                    # 1        200               50
                    # 2         50              200
                    # in questo esempio mi aspetto che la media dei cambiamenti sia 0 ma
                    # se uso il calcolo corretto per trovare la differenza percentuale ottengo
                    #
                    #     1:   ( 200 - 50 ) / 50 = 150 / 50 = 3
                    #     2:   ( 50 - 200 ) / 200 = -150 / 200 = -0.75
                    #  media = ( 3 + (-0.75) ) / 2 = 2.25 / 2 = 1.125 -> != 0

                    # visto che noi abbiamo la stessa modifica vogliamo una media di 0 in questo caso, ma otteniamo != 0
                    # per fare 0 basta dividere sempre per il numero più piccolo, e basterà il segno a bilanciare la media

                    perc_diff = (len(actual.aRoute) - len(standard.route)) / min(
                        len(standard.route), len(actual.aRoute)
                    )
                    # if perc_diff positive -> actual is bigger
                    # if perc_diff negative -> actual is smaller
                    if perc_diff >= 0:
                        counter += 1
                    else:
                        counter -= 1

                    total_perc_diff += perc_diff

        # faccio la media delle lunghezze delle actual
        actual_mean_lenght = int(actual_total_lenght / len(actual_list))
        # faccio la media delle percentuali ->
        total_perc_diff_mean = abs(total_perc_diff / len(actual_list))

        # DA LEGGERE
        # qua c'è un altro "problema"
        # Non è scontato che dopo la sottrazione della differenza media dal valore di partenza si ottenga un numero positivo (ovviamente vale sono per il caso di sottrazione)
        # Ci sono diversi approcci seguibili:
        #   - prendere il valore assoluto (non lo considererei molto perchè a volte ci sono anche degli 0 o comunque numeri bassi
        #       e questo non risolverebbe questi casi)
        #   - non considerare la modifica e tenere la lunghezza media calcolata (actual_mean_lenght) che non è malvagio secondo me (ho implementato questa per ora)
        #   - mettere un valore di default (bah)
        #   - mettere un valore sotto il quale non si può andare (bah)

        driver_len_variation = int(actual_mean_lenght * total_perc_diff_mean)
        if counter > 0:
            driver_len_dict.update(
                {driver: int(actual_mean_lenght + driver_len_variation)}
            )
        else:
            if actual_mean_lenght - driver_len_variation <= 0:
                driver_len_dict.update({driver: actual_mean_lenght})
            else:
                driver_len_dict.update(
                    {driver: int(actual_mean_lenght - driver_len_variation)}
                )

        # DA LEGGERE
        # alla fine con i dati che ho io vedo quasi sempre che la lunghezza della actual diminuisce rispetto alla standard.
        # Questo dipende dal dataset però.. probabilmente nel nostro dataset è molto più probabile rimuovere una città che aggiungerne una.

        counter = 0
        perc_diff = 0
        total_perc_diff = 0
        actual_total_lenght = 0
        total_perc_diff_mean = 0
        actual_mean_lenght = 0

    return driver_len_dict


def calculate_merch_lenght(driver_actuals: params.driverActuals) -> Dict[str, int]:
    driver_merch_len: Dict[str, int] = {}
    for driver, actual_list in driver_actuals.items():
        avg_route = 0
        for actual in actual_list:
            tot_merch = 0
            for trip in actual.aRoute:
                tot_merch += len(trip.merchandise)
            avg_route += int(tot_merch / len(actual.aRoute))
        driver_merch_len.update({driver: int(avg_route / len(actual_list))})

    return driver_merch_len


def max_merch_to_rules(
    max_merch: str,
    rules: List[Union[Tuple[str, str], Tuple[List[str], List[str]]]],
    new_merch_list: List[str],
) -> List[str]:
    while True:
        old_max_merch = max_merch
        for rule in rules:
            if isinstance(rule[0], list):
                if max_merch in rule[0]:
                    new_merch_list.extend(rule[1])
                    max_merch = rule[1][0] if rule[1] else max_merch
            else:
                if max_merch == rule[0]:
                    new_merch_list.append(rule[1])
                    max_merch = rule[1]
        if old_max_merch == max_merch:
            break

    return list(set(new_merch_list))


def find_max_merch(
    driver_actuals: params.driverActuals,
) -> Dict[str, List[str]]:
    res: Dict[str, List[str]] = {}
    for driver, actual_list in driver_actuals.items():
        merch_list: List[str] = []
        for actual in actual_list:
            for trip in actual.aRoute:
                for merch in trip.merchandise.keys():
                    merch_list.append(merch)
        count = Counter(merch_list)
        res.update({driver: [merch for merch, freq in count.most_common()]})
    return res


def save_results(drivers_perfect_routes: Dict[str, List[Trip]]) -> None:
    result = []
    for driver_id, route_data in drivers_perfect_routes.items():
        route_solution: List[Trip] = []
        for trip in route_data:
            merch_dict: Dict[str, int] = {}
            for merch, quantity in trip.merchandise.items():
                merch_dict.update({merch: quantity})
            route_solution.append(Trip(trip._from, trip.to, merch_dict).to_dict())

        result.append({"driver": driver_id, "route": route_solution})

    if not os.path.exists("./results"):
        os.makedirs("./results")
    with open("./results/perfectRoute.json", "w") as f:
        json.dump(result, f, indent=4)


def gen_drivers_route(
    driver_actuals: params.driverActuals,
    fav_cities: Dict[str, List[str]],
    fav_merch: Dict[str, List[Tuple[str, str]]],
    driver_routes_len: Dict[str, int],
    driver_merch_len: Dict[str, int],
    max_merch_dict: Dict[str, List[str]],
) -> Dict[str, List[Trip]]:
    drivers_perfect_routes: Dict[str, List[Trip]] = {}
    for driver, actual_list in driver_actuals.items():  # For each route
        len_route = driver_routes_len.get(driver)
        len_merch = driver_merch_len.get(driver)
        cities = fav_cities.get(driver)
        merch = fav_merch.get(driver)

        # Generate route
        route: List[Trip] = []
        for i in range(len_route):  # For each trip
            new_merch_list: List[Tuple[str, int]] = []
            delta_len: int = 0
            count: int = 0
            for j in range(len_merch):
                if delta_len != 0:
                    delta_len -= 1
                    continue
                elif delta_len == 0:
                    if count < len(max_merch_dict[driver]):
                        max_merch: str = max_merch_dict[driver][count]
                        count += 1
                    else:
                        max_merch: str = merch[np.random.randint(0, len(merch))]
                # Find the max value of the merch in the actuals

                # get the first element of max_merch_dict[driver] and remove it from the list

                new_merch_list.append(max_merch)
                old_len: int = len(new_merch_list)
                new_merch_list = max_merch_to_rules(max_merch, merch, new_merch_list)
                delta_len: int = len(new_merch_list) - old_len

            new_new_merch_list: Dict[str, int] = {}
            for merch in new_merch_list:
                new_new_merch_list.update({merch: random_item_value()})

            route.append(
                Trip(
                    cities[np.random.randint(0, len(cities))],
                    cities[np.random.randint(0, len(cities))],
                    new_new_merch_list,
                )
            )

        drivers_perfect_routes.update({driver: route})

    return drivers_perfect_routes


def gen_perfect_route(
    driver_actuals: params.driverActuals,
    fav_cities: Dict[str, List[str]],
    fav_merch: Dict[str, List[Tuple[str, str]]],
    driver_routes_len: Dict[str, int],
    driver_merch_len: Dict[str, int],
) -> Dict[str, List[Trip]]:
    max_merch_dict: Dict[str, List[str]] = find_max_merch(driver_actuals)

    results = gen_drivers_route(
        driver_actuals,
        fav_cities,
        fav_merch,
        driver_routes_len,
        driver_merch_len,
        max_merch_dict,
    )

    return results


# Generate point 3
def point_3() -> None:
    # Get all drivers routes
    driver_actuals: params.driverActuals = get_driver_actuals()
    print("  - Done getting drivers routes")

    # Find favourite cities for each driver
    fav_cities: Dict[str, List[str]] = calculate_liked_cities(driver_actuals)
    print("  - Done getting favourite cities")

    # Get average route length for each driver
    driver_routes_len: Dict[str, int] = calculate_route_lenght(
        driver_actuals, getStdRoutes()
    )
    print("  - Done getting average route length")

    # Get merch rules for each driver
    fav_merchandise: Dict[str, List[Tuple[str, str]]] = calculate_liked_merchandise(
        get_driver_actuals()
    )
    print("  - Done getting favourite merchandise")

    # Get average merch length for each driver
    driver_merch_len: Dict[str, int] = calculate_merch_lenght(driver_actuals)
    print("  - Done getting average merchandise length")

    # Generate perfect route
    results = gen_perfect_route(
        driver_actuals, fav_cities, fav_merchandise, driver_routes_len, driver_merch_len
    )
    print("  - Done generating perfect route")

    # Save results
    save_results(results)
    print("  - Done generating perfectRoute.json")


if __name__ == "__main__":
    point_3()
