import json
import sys
from typing import Dict, List, Tuple
from classes.ActRoute import ActRoute
from classes.Trip import Trip
from point_2.top_similarities import test_rec_sim, route_similarity
from point_1.rec_standard import common_fn_call
from dataset_generator.actRoute_generator import actRoute_generator, generateActualRoute, getDrivers, getStdRoutes


# make sure to run this file only from the bash launcher files on Lorenzo's machine
# you have to manually change the value for the test. The bash scripts and this script automate only the run of a single dataset


# --------------------------- FIRST ----------------------------
def crazyness_incrementation() -> None:

    print(" (TEST) crazyness_incrementation() has been called")

    # calculate mean similarity from std_routes
    mean_std_sim: float = test_rec_sim()
    print(" - With std: " + str(mean_std_sim))

    # generate act_routes from rec_std_routes
    print(" - regenerating actual based on rec_std")
    actRoute_generator(std_is_rec = True)
    print(" - Done")
    
    # calculate mean similarity from rec_std_routes
    mean_rec_sim: float = test_rec_sim()
    print(" - With rec_std: " + str(mean_rec_sim))

    with open("/media/lorenzo/Volume/DataMining/CRAZY_INCREMENTATION/inc_crazyness_tmp.txt", 'w') as file:
        # write string on file
        file.write(str(mean_std_sim)+" "+str(mean_rec_sim))
    
    print(" (TEST) crazyness_incrementation() done")



# --------------------------- SECOND ----------------------------
# Get the standard routes from the json file
def getPerfectRoutes() -> Dict[int, List[Trip]]:
    # reading sRoutes from json    
    file_path = "./results/perfectRoute.json"
    with open(file_path, "r") as perfectRoute_file:
        driver_perfect_list_json = json.load(perfectRoute_file)

    # Create objects from the data
    driver_perfect_list: Dict[int, List[Trip]] = {}
    for driver_perfect_json in driver_perfect_list_json:
        driver:int = driver_perfect_json["driver"]
        route: List[Trip] = []
        for perfect_trip in driver_perfect_json["route"]:
            route.append(Trip(perfect_trip["from"], perfect_trip["to"], perfect_trip["merchandise"]))
        
        driver_perfect_list.update({driver: route})
    
    return driver_perfect_list

    # small number of drivers
    # big crazyness
def actual_for_driver_incrementation() -> None:

    print(" (TEST) actual_for_driver_incrementation() has been called")

    # get perfect routes and drivers
    driver_perfect = getPerfectRoutes()
    local_drivers = getDrivers()

    # calculate for each driver the new_actual starting from the perfect route
    driver_new_actual: Dict[int, ActRoute] = {}
    for driver, perfect_route in driver_perfect.items():
        # search for the correct driver in local_drivers
        for local_driver in local_drivers:
            if local_driver.id == driver: 
                new_actual = generateActualRoute(perfect_route, local_driver, std_is_perfect = True)
        driver_new_actual.update({driver: new_actual})

    # calculate for each driver the similarity between his perfect and new_actual
    perfect_new_act_sim: Dict[int, float] = {}
    for driver, perfect_route in driver_perfect.items():
        perfect_new_act_sim.update({driver: route_similarity(perfect_route, driver_new_actual.get(driver), std_is_perfect = True)})
    
    # calculate mean similarity between all drivers
    mean_sim = sum(perfect_new_act_sim.values()) / len(perfect_new_act_sim)

    with open("/media/lorenzo/Volume/DataMining/ACT_FOR_DRIVER_INCREMENTATION/act_for_driver_inc_tmp.txt", 'w') as file:
        # write similarity value to file for bash script
        file.write(str(mean_sim))
    
    print(" (TEST) actual_for_driver_incrementation() done")


if __name__ == "__main__":

    num_arguments = len(sys.argv) - 1
    if num_arguments > 0:

        test_controller = sys.argv[1]

        if test_controller == "1":
            # test with incremental crazyness
            crazyness_incrementation()
        elif test_controller == "2":
            # test with incremental actual routes for each driver
            actual_for_driver_incrementation()
        else:
            print("Wrong argument: use \n- 1 for crazyness_incrementation()\n- 2 for actual_for_driver_incrementation()")

    else:
        print("use \n- 1 for crazyness_incrementation()\n- 2 for actual_for_driver_incrementation()")
    
