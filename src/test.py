# script.py

import sys

def main_function():
    # Tua logica qui
    result = 42
    result2 = 453
    
    # Ritorna il risultato
    return ""+str(result)+" "+str(result2)

if __name__ == "__main__":
    # Chiamando main_function e utilizzando sys.exit per terminare lo script e ritornare un valore
    sys.exit(main_function())
    

