import time
import os

from point_1.rec_standard import point_1
from point_2.top_similarities import point_2
from point_3.perfectRoute import point_3


if __name__ == "__main__":
    if not os.path.exists("./results/"):
        os.makedirs("./results/")

    # point 1
    p1 = time.time()
    print("Started point 1")
    point_1()
    print("Finished point 1")
    end_p1 = time.time()
    print("Time elapsed point 1: ", end_p1 - p1)

    print("")

    # point 2
    p2 = time.time()
    print("Started point 2")
    point_2()
    print("Finished point 2")
    end_p2 = time.time()
    print("Time elapsed point 2: ", end_p2 - p2)

    print("")

    # point 3
    p3 = time.time()
    print("Started point 3")
    point_3()
    print("Finished point 3")
    end_p3 = time.time()
    print("Time elapsed point 3: ", end_p3 - p3)

    print("")
    print("Helleryonee!!")
