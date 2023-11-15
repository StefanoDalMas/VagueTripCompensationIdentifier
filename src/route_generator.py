# system imports
import argparse
import random
import json
from typing import List, Dict, Tuple

# custom imports
from tools import cities_products as cp


def config() -> Tuple[int, int, int, int, int, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--entries",
        type=int,
        help="How many entries are going to be generated",
        default=100,
    )
    parser.add_argument(
        "-mint", "--mintrip", type=int, help="Minimum number of route", default=1
    )
    parser.add_argument(
        "-maxt", "--maxtrip", type=int, help="Maximum number of route", default=3
    )
    parser.add_argument(
        "-minp", "--minproducts", type=int, help="Minimum number of products", default=1
    )
    parser.add_argument(
        "-maxp", "--maxproducts", type=int, help="Maximum number of products", default=3
    )
    parser.add_argument(
        "-fn",
        "--filename",
        type=str,
        help="Filename to save the data",
        default="standard",
    )
    args = parser.parse_args()
    return (
        args.entries,
        args.mintrip,
        args.maxtrip,
        args.minproducts,
        args.maxproducts,
        args.filename + ".json",
    )


if __name__ == "__main__":
    ENTRIES, MINTRIP, MAXTRIP, MINPRODUCTS, MAXPRODUCTS, FILENAME = config()
    if (MINTRIP > MAXTRIP or MINPRODUCTS > MAXPRODUCTS):
        exit("wrong argument: make sure to pass correct values for min and max arguments")

    # open "data/standard.json, if it's not there, create it"
    with open("data/" + FILENAME, "w") as f:
        json_array = []
        for entry in range(ENTRIES):
            json_data = {}
            trips_number = random.randint(MINTRIP, MAXTRIP)
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
                merchandise = cp.merch_maker(MINPRODUCTS, MAXPRODUCTS)
                json_trip.update({"from": start, "to": end, "merchandise": merchandise})
                route.append(json_trip)
                length = 0
                for e in route:
                    length += 1
                for r in route:
                    print(r, "\n")
                print("len is ", length, "\n")
                print("length of route: " + str(len(route)))
                # print length of route

            json_data.update({"id": "s" + str(entry)})
            json_data.update({"route": route})

            json_array.append(json_data)
        f.write(json.dumps(json_array, indent=4))
