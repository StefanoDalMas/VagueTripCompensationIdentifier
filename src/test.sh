#!/bin/bash

numbers=$(python3 /home/lorenzo/Desktop/VagueTripCompensationIdentifier/src/test.py 2>&1)   

read -r var1 var2 <<< "$numbers"

