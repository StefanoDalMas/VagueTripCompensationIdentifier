import time

from tools.parameters import Parameters as params
from recStandard import point_1
from top_similarities import point_2
from perfectRoute import point_3


if __name__ == "__main__":
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

    print("Helleryonee!!")
