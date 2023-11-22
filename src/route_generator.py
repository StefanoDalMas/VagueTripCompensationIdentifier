# system imports
import random
import json
from typing import List, Dict, Tuple

# custom imports
from tools import cities_products as cp
from tools.parameters import Parameters as p




def load_config() -> Tuple[int, int, int, int, int, str]:
    ENTRIES = int(p.ENTRIES)
    MINTRIP = int(p.MINTRIP)
    MAXTRIP = int(p.MAXTRIP)
    MINPRODUCTS = int(p.MINPRODUCTS)
    MAXPRODUCTS = int(p.MAXPRODUCTS)
    FILENAME = str(p.FILENAME)
    return ENTRIES, MINTRIP, MAXTRIP, MINPRODUCTS, MAXPRODUCTS, FILENAME




def standardRouteGenerator(entries:int, minTrip:int, maxTrip:int, minProducts:int, maxProducts:int, fileName:str):
    # open "data/standard.json, if it's not there, create it"
    with open("data/" + fileName, "w") as f:
        json_array = []
        for entry in range(entries):
            json_data = {}
            trips_number = random.randint(minTrip, maxTrip)
            route = []
            last = None
            for trip in range(trips_number):
                json_trip = {}
                if last != None:
                    start = last
                else:
                    start = cp.random_city()
                end = cp.random_city()
                while start == end:
                    end = cp.random_city()
                last = end
                merchandise = cp.merch_maker(minProducts, maxProducts)
                json_trip.update({"from": start, "to": end, "merchandise": merchandise})
                route.append(json_trip)
                length = 0
                for e in route:
                    length += 1
                # print length of route

            json_data.update({"id": "s" + str(entry)})
            json_data.update({"route": route})

            json_array.append(json_data)
        f.write(json.dumps(json_array, indent=4))


if __name__ == "__main__":
    ENTRIES, MINTRIP, MAXTRIP, MINPRODUCTS, MAXPRODUCTS, FILENAME = load_config()

    if (MINTRIP > MAXTRIP or MINPRODUCTS > MAXPRODUCTS):
        exit("wrong argument: make sure to pass correct values for min and max arguments")
    standardRouteGenerator(ENTRIES, MINTRIP, MAXTRIP, MINPRODUCTS, MAXPRODUCTS, FILENAME)
    
