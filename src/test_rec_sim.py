from point_2.top_similarities import test_rec_sim
from point_1.rec_standard import point_1
from dataset_generator.actRoute_generator import actRoute_generator

if __name__ == "__main__":
    # Calculate mean similarity from std_routes
    mean_std_sim: float = test_rec_sim()
    print(" - With std: " + str(mean_std_sim))

    # Generate rec_std_rouotes
    # point_1()

    # Generate act_routes from rec_std_routes
    print(" - regenerating actual based on rec_std")
    actRoute_generator(is_rec_std=True)
    print(" - Done")

    # Calculate mean similarity from rec_std_routes
    mean_rec_sim: float = test_rec_sim()
    print(" - With rec_std: " + str(mean_rec_sim))

    with open("/home/lorenzo/Desktop/CRAZY_INCREMENTATION/tmp_values.txt", "w") as file:
        file.write("" + str(mean_std_sim) + " " + str(mean_rec_sim))
