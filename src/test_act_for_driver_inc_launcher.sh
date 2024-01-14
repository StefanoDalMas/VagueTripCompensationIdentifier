#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <folder_name>"
    exit 1
fi

folder_name=$1

echo "+ genero database" 
python3 /home/lorenzo/Desktop/VagueTripCompensationIdentifier/src/generate_dataset.py
echo "+ database generato"

echo "+ calcolo soluzioni"
python3 /home/lorenzo/Desktop/VagueTripCompensationIdentifier/src/solution.py
echo "+ soluzioni calcolate"

echo "+ copio cartelle e rimuovo tmp"
# Esegui i comandi copy
mkdir /media/lorenzo/Volume/DataMining/ACT_FOR_DRIVER_INCREMENTATION/$folder_name
cp -r /home/lorenzo/Desktop/VagueTripCompensationIdentifier/src/results /media/lorenzo/Volume/DataMining/ACT_FOR_DRIVER_INCREMENTATION/$folder_name 
cp -r /home/lorenzo/Desktop/VagueTripCompensationIdentifier/src/data /media/lorenzo/Volume/DataMining/ACT_FOR_DRIVER_INCREMENTATION/$folder_name
echo "+ cartelle copiate e tmp rimossi"

echo "+ calcolo values"
python3 /home/lorenzo/Desktop/VagueTripCompensationIdentifier/src/some_dataset_tests.py 2
echo "+ values calcolati"

echo "leggo da file i values"
read -r mean_sim < "/media/lorenzo/Volume/DataMining/ACT_FOR_DRIVER_INCREMENTATION/act_for_driver_inc_tmp.txt"
echo -e "mean_sim: $mean_sim" > /media/lorenzo/Volume/DataMining/ACT_FOR_DRIVER_INCREMENTATION/$folder_name/sim_value.txt
echo "+ values salvati sul file"