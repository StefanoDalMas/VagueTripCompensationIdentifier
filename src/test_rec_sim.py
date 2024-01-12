from typing import List
from classes.StdRoute import StdRoute
from point_2.top_similarities import test_rec_sim
from point_1.rec_standard import point_1
from dataset_generator.actRoute_generator import actRoute_generator
import sys

if __name__ == "__main__":
    # calculate mean similarity from std_routes
    mean_std_sim: float = test_rec_sim()
    print(" - With std: " + str(mean_std_sim))

    # generate rec_std_rouotes
    # point_1()

    # generate act_routes from rec_std_routes
    print(" - regenerating actual based on rec_std")
    actRoute_generator(is_rec_std = True)
    print(" - Done")
    

    # calculate mean similarity from rec_std_routes
    mean_rec_sim: float = test_rec_sim()
    print(" - With rec_std: " + str(mean_rec_sim))

    with open("/home/lorenzo/Desktop/CRAZY_INCREMENTATION/tmp_values.txt", 'w') as file:
        # Scrivi la stringa nel file
        file.write(""+str(mean_std_sim)+" "+str(mean_rec_sim))