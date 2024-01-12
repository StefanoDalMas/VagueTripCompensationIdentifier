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
cp -r /home/lorenzo/Desktop/VagueTripCompensationIdentifier/src/results /home/lorenzo/Desktop/CRAZY_INCREMENTATION/$folder_name
rm /home/lorenzo/Desktop/CRAZY_INCREMENTATION/$folder_name/results/tmp.txt
cp -r /home/lorenzo/Desktop/VagueTripCompensationIdentifier/src/data /home/lorenzo/Desktop/CRAZY_INCREMENTATION/$folder_name
rm /home/lorenzo/Desktop/CRAZY_INCREMENTATION/$folder_name/data/tmp.txt
echo "+ cartelle copiate e tmp rimossi"

echo "+ calcolo values"
python3 /home/lorenzo/Desktop/VagueTripCompensationIdentifier/src/test_rec_sim.py  
echo "+ values calcolati"

echo "leggo da file i values"
read -r std rec < "/home/lorenzo/Desktop/CRAZY_INCREMENTATION/tmp_values.txt"
echo -e "std: $std\nrec: $rec" > /home/lorenzo/Desktop/CRAZY_INCREMENTATION/$folder_name/values.txt
echo "+ values salvati sul file"