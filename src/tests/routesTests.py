import unittest
import json
import os
from pprint import pprint
from typing import List

from tools.parameters import Parameters as params
from dataset_generator.actRoute_generator import actRoute_generator
from dataset_generator.stdRoute_generator import stdRoute_generator
from dataset_generator.drivers_generator import drivers_generator
from classes.ActRoute import ActRoute 
from classes.StdRoute import StdRoute
from classes.Driver import Driver

class TestRoutesGenerator(unittest.TestCase):
    actual_route: List[ActRoute] 
    standard_route: List[StdRoute]
    drivers: List[Driver]
    
    @classmethod
    def setUpClass(cls):
        cls.drivers = drivers_generator()
        print("drivers_generator GOOD")
        cls.standard_routes = stdRoute_generator(params.ENTRIES, params.MINTRIP, params.MAXTRIP, params.MINPRODUCTS, params.MAXPRODUCTS, params.SROUTES_FILENAME)
        print("stdRoute_generator GOOD")
        cls.actual_routes = actRoute_generator()
        print("actRoute_generator GOOD")
            
    @classmethod
    def tearDownClass(cls):
        pass

# standard_routes has no type
    def testStdFromToSameNode(self):
        print("Testing if there are no minimal loops in the standard routes")
        for route in self.standard_routes:
            trips = route.get("route")
            if trips == None:
                assert(1==0)
            for trip in trips:
                assert(trip.get("from")!=trip.get("to"))
        assert(True==True)

    def testActFromToSameNode(self):
        print("Testing if there are no minimal loops in the actual routes")
        for route in self.actual_routes:
            trips = route.aRoute
            if trips == None:
                assert(1 == 0)
            for trip in trips:
                assert(trip._from != trip.to)
        assert(True == True)

# standard_routes has no type
    def testStdFromToLinked(self):
        print("Testing if all STANDARD routes are linked")
        for route in self.standard_routes:
            last = None
            trips = route.get("route")
            if trips == None:
                assert(1==0)
            for trip in trips:
                if last != None:
                    assert(trip.get("from") == last) 
                last = trip.get("to")

    def testActFromToLinked(self):
        print("Testing if all ACTUAL routes are linked")
        #checks if from and to are right
        for route in self.actual_routes:
            last = None
            trips = route.aRoute
            if trips == None:
                assert(1==0)
            for trip in trips:
                if last != None:
                    assert(trip._from == last) 
                last = trip.to



if __name__ == "__main__":
    unittest.main()
