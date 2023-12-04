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
    print("Parameters OK")


if __name__ == "__main__":
    check_params()
    drivers_generator.drivers_generator()
    print("Drivers generated")
    stdRoute_generator.stdRoute_generator(
        params.ENTRIES,
        params.MINTRIP,
        params.MAXTRIP,
        params.MINPRODUCTS,
        params.MAXPRODUCTS,
        params.SROUTES_FILENAME,
    )
    print("Standard routes generated")
    actRoute_generator.actRoute_generator()
    print("Actual routes generated")
