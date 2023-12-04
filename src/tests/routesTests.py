import unittest
import json
import os
from pprint import pprint
from typing import List
from actRoute_generator import actRoute_generator
from classes.ActRoute import ActRoute 

class TestRoutesGenerator(unittest.TestCase):
    actual_route: List[ActRoute] 
    standard_route: List[ActRoute] 
    
    def setUp(self):
        self.actual_routes = actRoute_generator()

    def tearDown(self):
        pass

    def testActToFromLinked(self):
        print("Testing if all routes are linked")
        #checks if from and to are right
        for route in self.actual_routes:
            last = None
            trips = route.get("route")
            if trips == None:
                assert(1==0)
            for trip in trips:
                if last != None:
                    assert(trip.get("from") == last) 
                last = trip.get("to")

    def testActFromToSameNode(self):
        print("Testing if there are no minimal loops")
        for route in self.actual_routes:
            trips = route.get("route")
            if trips == None:
                assert(1==0)
            for trip in trips:
                assert(trip.get("from")!=trip.get("to"))
        assert(True==True)

if __name__ == "__main__":
    unittest.main()
