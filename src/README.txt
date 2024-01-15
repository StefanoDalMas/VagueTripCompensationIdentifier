# VagueTripCompensationIdentifier
Data Mining Project 2023-2024

# Project Structure

src/
├── classes # All classes used in the project
│  ├── ActRoute.py
│  ├── Driver.py
│  ├── StdRoute.py
│  └── Trip.py
├── data # Dataset
├── dataset_generator
│  ├── actRoute_generator.py
│  ├── drivers_generator.py
│  └── stdRoute_generator.py
├── generate_dataset.py # File that generates dataset
├── point_1 # Point 1 solution
│  └── rec_standard.py
├── point_2 # Point 2 solution
│  └── top_similarities.py
├── point_3 # Point 3 solution
│  └── perfectRoute.py
├── README.txt
├── results # Generated results
├── solution.py # File that generates results
├── some_dataset_tests.py
├── test_act_for_driver_inc_launcher.sh
├── test_act_for_driver_win_inc_launcher.sh
├── test_crazy_inc_launcher.sh
├── tests # Tests for dataset generator
│  ├── driversTests.py
│  └── routesTests.py
└── tools
   ├── __init__.py
   ├── cities_products.py
   ├── parameters.py # Parameters for dataset and solutions
   ├── parameters_local.py
   └── utils.py

## Requirements
- python 3.10.12 +

## Getting started
1. Clone this repository with:

    git clone https://github.comStefanoDalMasVagueTripCompensationIdentifier.git

    cd VagueTripCompensationIdentifier/src

2. Setup virtual environment:

    # Create virtual enviroment
    python3 -m venv .venv

    # Activate virtual enviroment
    source .venv/bin/activate

3. Install dependencies:

    pip install -r requirements.txt

## How to start the program

1. At this point it is possible to create the dataset with our generator(a.) or you can insert yours in the data folder(b.)

    i. It's possible to play with some parameters that guide our generator to create the dataset. You can find them in the `tools/parameters.py` file.
    To launch the generator run:

        python3 generate_dataset.py

    ii. Copy your `actual.json` and `standard.json` files in the `data` folder.
    You can use the command:
    
        cp -r <your_data_folder_path> ./

2. run the following command to calculate the solutions on the given dataset:

    python3 solution.py
