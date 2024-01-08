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
from tools.cities_products import shopping_list as sl


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


def calculate_liked_merchandise(driver_actuals: params.driverActuals) -> Dict[str, List[Any]]:
    dict_all_merch: Dict[str, List[List[str]]] = {}
    act_routes_list : List[List[List[str]]] = []
    route_list: List[List[str]] = []
    trip_list: List[str] = []  # [beer,wine,diapers,nuts,...]
    for driver, actual_list in driver_actuals.items():  # {driver: [ActRoute,ActRoute,...]]}
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

    # for each driver apply the apriori to the baskets of all merchandise of all routes taken by him
    dict_rules: Dict[str, List[List[Tuple[List[str], List[str]]]]] = {}
    rules_route_list: List[Tuple[List[str], List[str]]] = [] #[([antecedent], [consequent])]
    for driver, routes_list in dict_all_merch.items():
        for route_goods in routes_list:
            te = TransactionEncoder()
            te_ary = te.fit(route_goods).transform(route_goods)
            df = pd.DataFrame(te_ary, columns=te.columns_)
            frequent_itemsets = apriori(df, min_support=0.1, use_colnames=True,verbose=0,low_memory=True)

            # Generate association rules
            rules = association_rules(
                frequent_itemsets, metric="lift", min_threshold=1.5
            )

            antecedents = rules["antecedents"]
            consequents = rules["consequents"]

            antecedents_tmp = []
            for antecedent_set in antecedents:
                antecedents_tmp.append(frozenset_to_list(antecedent_set))

            consequents_tmp = []
            for consequents_set in consequents:
                consequents_tmp.append(frozenset_to_list(consequents_set))

            for i in range(len(antecedents_tmp)):
                rules_route_list.append((antecedents_tmp[i], consequents_tmp[i]))


        dict_rules.update({driver: rules_route_list})
        rules_route_list = []
        # MANCA DA CAPIRE COME CONTROLLARE E TOGLIERE I DUPLICATI
        # MANCA DA CALIBRARE LE COSTANTI DELL'ALGORITMO A NOSTRO PIACIMENTO

        # DIREI DI CAMBIARE NOME A QUESTA FUNZIONE TIPO IN calculate_rules PERCHÈ È GIÀ TROPPO GRANDE
        # POI SE NE FA UN'ALTRA DOVE SI PRENDONO LE REGOLE E SI BUTTA FUORI Dict[driver, [liked cities]]

    return dict_rules

def frozenset_to_list(frozenset):
    new_list: List[str] = []
    for item in frozenset:
        new_list.append(item)
    return new_list

def calculate_route_lenght(driver_actuals: params.driverActuals, std_routes: List[StdRoute]) -> int:
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
    actual_total_lenght = 0 # used to calculate the base distance. Then we add/substract the mean difference between actual and standard
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

                    perc_diff = (len(actual.aRoute) - len(standard.route)) / min(len(standard.route), len(actual.aRoute))
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
            driver_len_dict.update({driver: int(actual_mean_lenght + driver_len_variation)})
        else:
            if actual_mean_lenght - driver_len_variation <= 0:
                driver_len_dict.update({driver: actual_mean_lenght})
            else:
                driver_len_dict.update({driver: int(actual_mean_lenght - driver_len_variation)})

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



if __name__ == "__main__":
    # dict[0] -> dictionary, dict[1] -> threshold
    # fav_cities: Dict[str, List[str]] = calculate_liked_cities(get_driver_actuals())

    # next step : get best merchandise for each driver
    # get all actrouts for each driver
    # for each route, get all trips and convert each merch in a list
    # make all baskets of a route a list of lists [[beer,wine],[diapers,nuts],...]
    # use apriori to get best merchandise

    prova = calculate_route_lenght(get_driver_actuals(), getStdRoutes())

    fav_merchandise: Dict[str, List[Any]] = calculate_liked_merchandise(
        get_driver_actuals()
    )


    # make me a test matrix with data like this [["milk","wine","beer"],["beer","diapers"],...]
    # take a lot of things like beer, coke, flour, and so on

    print("stop")
    # next step : generate perfect route using fav_cities and fav_merchandise
