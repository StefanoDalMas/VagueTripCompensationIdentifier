# system imports
import random
import json
from typing import List, Dict, Tuple

# custom imports
from tools import cities_products as cp
from tools.parameters import Parameters as params
from classes.StdRoute import StdRoute


def stdRoute_generator(
    entries: int,
    minTrip: int,
    maxTrip: int,
    minProducts: int,
    maxProducts: int,
    fileName: str,
) -> List[StdRoute]:
    # open "data/standard.json, if it's not there, create it"
    try:
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
                    json_trip.update(
                        {"from": start, "to": end, "merchandise": merchandise}
                    )
                    route.append(json_trip)
                    length = 0
                    for _ in route:
                        length += 1
                    # print length of route

                json_data.update({"id": "s" + str(entry)})
                json_data.update({"route": route})

                json_array.append(json_data)
            f.write(json.dumps(json_array, indent=4))
            return json_array
    except FileNotFoundError:
        print("ERROR: no file found in the data folder during stdRoute generation")
    except OSError as e:
        print("ERROR: OSError during stdRoute generation")
    except Exception as e:
        print("ERROR: whacky exception raised ", e)


if __name__ == "__main__":
    stdRoute_generator(
        params.ENTRIES,
        params.MINTRIP,
        params.MAXTRIP,
        params.MINPRODUCTS,
        params.MAXPRODUCTS,
        params.SROUTES_FILENAME,
    )
