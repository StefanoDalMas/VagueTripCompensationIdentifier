import unittest
import json
import os
from pprint import pprint
from typing import List
from actRoute_generator import actRoute_generator
from classes.ActRoute import ActRoute 

class TestRoutesGenerator(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testStdRoutes(self):
        #checks if from and to are right
        actual_routes : List[ActRoute] = actRoute_generator()
        for route in actual_routes:
            last = None
            trips = route.get("route")
            if trips == None:
                assert(1==0)
            for trip in trips:
                if last != None:
                    assert(trip.get("from") == last) 
                last = trip.get("to")

if __name__ == "__main__":
    unittest.main()
