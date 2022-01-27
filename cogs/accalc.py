#!/usr/bin/env python3
import os
import sys
import time
import pandas as pd

__DESCRIPTION__ = """calculates acceleration on a calculated resultant.\nUSAGE: calculate [file] [optional:name of object in file]"""
start_time = time.time()

"""[General director set]
Sets the working directory to the current directory \
that the __main__ file is being executed from
"""
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def calculate(file, name=None):
    untapped_data = pd.read_csv(file)
    foo = 0
    if not name:
        try:
            while (foo <= untapped_data.shape[0]):

                # Indexing the DataFrame
                current_name = untapped_data['object_name'][foo]
                current_mass_grams = untapped_data['object_mass'][foo]
                current_thrust = untapped_data['object_thrust'][[foo]]

                # Convert grams to kilograms = G/1000
                current_mass_kilograms = current_mass_grams / 1000

                # Calculate weight through gravity = KG * 9.8 // Converts to Newtons
                current_weight_n = current_mass_kilograms * 9.8

                # Calculate the resultant force
                current_resultant_force = current_thrust - current_weight_n

                # Calculate the acceleration m/s²
                current_acceleration = current_resultant_force / current_mass_kilograms

                # print(int(current_resultant_force))
                untapped_data.at[foo, 'resultantForce'] = str(
                    round(float(current_resultant_force), 2)) + " N"
                untapped_data.at[foo, 'acceleration'] = str(
                    round(float(current_acceleration), 2)) + " m/s²"

                # Pointer
                foo += 1

        except Exception as e:
            untapped_data.to_csv("../modified_data.csv", index=False)
            time_calculation = round(time.time() - start_time, 2)
            if time_calculation < 100:
                ending = "ms"
            else:
                ending = "secs"
                time_calculation = time_calculation/10
            print(
                f"Calculations finished\n\n---------LOG---------\n{e}\nTime Taken: {time_calculation}{ending}\n")
    elif name:
        data = untapped_data.loc[untapped_data['object_name'] == name]
        if "Empty DataFrame" in str(data):
            print(f"No data found for {name}")
        else:
            print("----------------------------------------------------------------")
            print(
                f"----------------------Data for  {name}------------------------")
            print("----------------------------------------------------------------")
            print(str(data))
    else:

        print("Unable to access CSV")
