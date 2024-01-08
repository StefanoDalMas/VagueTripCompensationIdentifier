import time

from tools.parameters import Parameters as params

import actRoute_generator
import stdRoute_generator
import drivers_generator


def check_params():
    print("Checking parameters...")
    if params.ENTRIES < 1:
        raise Exception("ENTRIES must be greater than 0")
    if params.MINTRIP < 1:
        raise Exception("MINTRIP must be greater than 0")
    if params.MAXTRIP < 1:
        raise Exception("MAXTRIP must be greater than 0")
    if params.MINPRODUCTS < 1:
        raise Exception("MINPRODUCTS must be greater than 0")
    if params.MAXPRODUCTS < 1:
        raise Exception("MAXPRODUCTS must be greater than 0")
    if params.MINTRIP > params.MAXTRIP:
        raise Exception("MINTRIP must be less than MAXTRIP")
    if params.MINPRODUCTS > params.MAXPRODUCTS:
        raise Exception("MINPRODUCTS must be less than MAXPRODUCTS")
    if params.MIN_ROUTES_TO_DRIVERS > params.ENTRIES:
        raise Exception("MIN_ROUTES_TO_DRIVERS must be less than ENTRIES")
    if params.MAX_ROUTES_TO_DRIVERS > params.ENTRIES:
        raise Exception("MAX_ROUTES_TO_DRIVERS must be less than ENTRIES")
    if params.MIN_LIKED_CITIES < 4:
        raise Exception("MIN_LIKED_CITIES must be more than 4")
    if params.MIN_CITIES < 4:
        raise Exception("MIN_CITIES must be more than 4")
    print("Parameters OK")


if __name__ == "__main__":
    start = time.time()
    check_params()
    drivers_generator.drivers_generator()

    end = time.time()
    print(f"driver generation time: {end-start}")
    print("Drivers generated")

    start = time.time()
    stdRoute_generator.stdRoute_generator(
        params.ENTRIES,
        params.MINTRIP,
        params.MAXTRIP,
        params.MINPRODUCTS,
        params.MAXPRODUCTS,
        params.SROUTES_FILENAME,
    )
    end = time.time()
    print(f"standard generation time: {end-start}")
    print("Standard routes generated")

    start = time.time()
    actRoute_generator.actRoute_generator()
    end = time.time()
    print(f"actual generation time: {end-start}")
    print("Actual routes generated")
