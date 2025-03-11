
import os

import numpy as np
from netCDF4 import Dataset
from os import path


ROOT_FOLDER = path.abspath(path.join(path.dirname(__file__), '..'))
DATA_FOLDER = path.join(ROOT_FOLDER, "data")


def get_file_abs_path(file_name:str):
    file_path = path.join(DATA_FOLDER, file_name)

    if not path.exists(file_path):
        raise ValueError(f"File does not exist:\n{file_path}")
    else:
        return file_path


def get_all_available_nc_files():
    file_dict = {}

    for f in os.listdir(DATA_FOLDER):
        if f.endswith(".nc"):
            file_dict[f] = get_file_abs_path(f)

    return file_dict


def nc_choice_menu():
    all_nc_files = get_all_available_nc_files()
    num = 0
    print("Choose a NC file('Q' for escaping):")
    for f in all_nc_files.keys():
        print(f"({num}) {f}")
        num += 1

    file_index = choose_nc(len(all_nc_files)-1)
    if file_index is None:
        return

    choosen_file = all_nc_files[list(all_nc_files.keys())[file_index]]

    open_nc_file(choosen_file)


def choose_nc(max_index):
    while True:
        ins = input()
        if ins.isdigit():
            ins = int(ins)
            if 0 <= ins <= max_index:
                return ins
        elif ins.lower() == "q":
            break
        print("Sorry that input is not valid")

def open_nc_file(file_path:str):
    nc_file = Dataset(file_path)
    print(nc_file.variables.keys())

    pressure_levels = nc_file.variables["pressure_level"][:]  # (19,)

    # Temperatur extrahieren (Mittelwert über Zeit und Breite/Länge)
    temperature = np.mean(nc_file.variables["t"][:], axis=(0, 2, 3))  # (19,)

    # Print-Ausgabe
    print("Pressure Level (hPa) | Temperature (K)")
    print("-" * 35)

    for p, t in zip(pressure_levels, temperature):
        print(f"{p:>15} hPa | {t:.2f} K")



if __name__ == '__main__':
    nc_choice_menu()


# Zielparameter:
# Temperatur x und humidity y
# wir brauchen:
# eine funktion die die datei richtig öffnet & daraus einen pandas dataframe bauen & zurückgeben
# eine funktion die basierend auf den daten mehrere scatterplots baut (daher prüfung ob columns vorhanden die man braucht)
#
# applikationsziel:
# Auswahl einer datei & ausgabe der entsprechenden plots.
#
#
# Ziel:
# x achse = Zeit
# y achse = höhe(druck)
# gradient coloring der gesammten map, basierend auf temperatur
# scatter plot basierend auf humidity, je größer/undurchsichtiger der punkt, desto höher der wert
# Legende dazu mit farbascala temperatur & größen/durchsichtbarkeit erklärung von scatters

