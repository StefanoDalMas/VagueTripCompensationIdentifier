import json
import os
from typing import Dict, List
from classes.Trip import Trip
from classes.ActRoute import ActRoute
from classes.StdRoute import StdRoute
from tools.parameters import Parameters as params
from similarity import generate_similarities



def compute_mean_similarity(sim_drivers_routes:params.driver_similarities) -> float:
    pass

def generate_top_5_similarities(sim_drivers_routes: Dict[str, Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    top_5_similarities = {}
    for driver, routes in sim_drivers_routes.items():
        sorted_routes = sorted(routes.items(), key=lambda x: x[1], reverse=True)
        top_5_similarities[driver] = dict(sorted_routes[:5])
    return top_5_similarities

def make_driver_json(top_5_dict:params.driver_similarities) -> None:
    #print in a file called "driver.json" something like this
    #[
    # {driver:C, routes:[s10, s20, s2, s6, s10}}, 
    # {driver:A, routes:[s1, s2, s22, s61, s102]}, 
    # ….
    # ]
    result = []
    for driver_id, route_data in top_5_dict.items():
        result.append({
            "driver": driver_id,
            "routes": list(route_data.keys())
        })
    if not os.path.exists("./results"):
        os.makedirs("./results")
    with open("./results/driver.json", "w") as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    #point 2 of the assignment
    #print the current working directory
    print(os.getcwd())
    sim_drivers_routes:params.driver_similarities = generate_similarities()
    top_5_dict:params.driver_similarities = generate_top_5_similarities(sim_drivers_routes)
    make_driver_json(top_5_dict)
    
    
    print("yes")

