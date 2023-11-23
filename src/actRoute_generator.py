import json
from classes.Driver import Driver

DRIVERS_FILENAME = "drivers.json"

# reading stdRoutes
with open("./data/" + DRIVERS_FILENAME, "r") as driversFile:
    # Read the JSON data
    driversJson = json.load(driversFile)

# Create objects from the data
drivers = []
for driverJson in driversJson:
    driver = Driver(
        driverJson["id"],
        driverJson["citiesCrazyness"],
        driverJson["productCrazyness"],
        driverJson["likedCities"],
        driverJson["likedProducts"],
        driverJson["dislikedCities"],
        driverJson["dislikedProducts"],
        driverJson["cities"],
        driverJson["products"],
)
    drivers.append(driver)

for i in range(len(drivers)):
    print(drivers[i])


# reading drivers

